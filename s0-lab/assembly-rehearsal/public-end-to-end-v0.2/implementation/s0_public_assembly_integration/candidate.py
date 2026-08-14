"""One exact, diagnostic-only call to the authenticated offline bridge."""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from s0_public_runtime_preloader import (
    AssemblyArtifactBundle,
    OfflinePreloaderInputs,
    StaticMaterialBundle,
    prepare_assembly_runtime_launch,
)

_SUCCESS_TRACE = (
    "OFFLINE-NEW",
    "OFFLINE-PUBLIC-ARTIFACTS-AUTHENTICATED",
    "OFFLINE-PLAN-VALIDATED",
    "OFFLINE-DIAGNOSTIC-COMPLETE",
)
_REJECTED_TRACE = ("OFFLINE-NEW", "OFFLINE-REJECTED")
_RPNP_IMPLEMENTATION_MANIFEST_SHA256 = "5022d517864cae19520a1e3e34a683965609abf0ef29e167b30a11bade4a32c2"
_INTEGRATION_V01_MANIFEST_SHA256 = "f55352771432404f4c2e9337665184e18afde076b8b3efe7a455ee6694d60e6b"
_INTEGRATION_V02_MANIFEST_SHA256 = "1349c6c4c97d24256f98216eb86a353451891419044b61d22c5c14d7eded5e7c"


@dataclass(frozen=True)
class PublicInputClosure:
    rpnp_implementation_manifest_raw: bytes
    rpnp_implementation_targets: Mapping[str, bytes]
    integration_v01_manifest_raw: bytes
    integration_v01_targets: Mapping[str, bytes]
    integration_v02_manifest_raw: bytes
    integration_v02_targets: Mapping[str, bytes]


def _verify_manifest(raw: bytes, targets: Mapping[str, bytes], expected_hash: str, expected_rows: int) -> None:
    if type(raw) is not bytes or hashlib.sha256(raw).hexdigest() != expected_hash or not raw.endswith(b"\n"):
        raise ValueError("public input manifest differs from its exact pin")
    if type(targets) not in {dict, type(MappingProxyType({}))}:
        raise ValueError("public input targets are not one exact mapping")
    target_items = tuple(targets.items())
    if any(type(path) is not str or type(value) is not bytes for path, value in target_items):
        raise ValueError("public input target entries are not exact string-to-bytes pairs")
    target_snapshot = MappingProxyType(dict(target_items))
    if len(target_snapshot) != len(target_items):
        raise ValueError("public input target entries are not unique")
    lines = raw[:-1].split(b"\n")
    paths: list[str] = []
    for line in lines:
        digest_raw, separator, path_raw = line.partition(b"  ")
        if separator != b"  " or len(digest_raw) != 64:
            raise ValueError("public input manifest row is malformed")
        digest = digest_raw.decode("ascii")
        path = path_raw.decode("ascii")
        if hashlib.sha256(target_snapshot.get(path, b"")).hexdigest() != digest:
            raise ValueError("public input target differs from its manifest")
        paths.append(path)
    if len(paths) != expected_rows or paths != sorted(paths) or len(set(paths)) != len(paths) or set(target_snapshot) != set(paths):
        raise ValueError("public input manifest closure is not exact")


def _verify_public_input_closure(closure: PublicInputClosure) -> None:
    if type(closure) is not PublicInputClosure:
        raise ValueError("public input closure is not exact")
    _verify_manifest(closure.rpnp_implementation_manifest_raw, closure.rpnp_implementation_targets, _RPNP_IMPLEMENTATION_MANIFEST_SHA256, 11)
    _verify_manifest(closure.integration_v01_manifest_raw, closure.integration_v01_targets, _INTEGRATION_V01_MANIFEST_SHA256, 5)
    _verify_manifest(closure.integration_v02_manifest_raw, closure.integration_v02_targets, _INTEGRATION_V02_MANIFEST_SHA256, 6)


def _canonical_json(value: dict[str, object]) -> bytes:
    return (json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")


@dataclass(frozen=True)
class OfflineIntegrationDiagnostic:
    raw: bytes
    sha256: str
    state_trace: tuple[str, ...]
    terminal_state: str
    failure_class: str | None
    candidate_only: bool = True
    native_api_reachable: bool = False
    rehearsal_pass: bool = False

    def __post_init__(self) -> None:
        if type(self.raw) is not bytes or hashlib.sha256(self.raw).hexdigest() != self.sha256:
            raise ValueError("offline integration diagnostic is not byte-bound")
        if self.state_trace not in {_SUCCESS_TRACE, _REJECTED_TRACE}:
            raise ValueError("offline integration state trace is not exact")
        if self.terminal_state != self.state_trace[-1]:
            raise ValueError("offline integration terminal state differs from its trace")
        if (self.failure_class is None) != (self.state_trace == _SUCCESS_TRACE):
            raise ValueError("offline integration failure disposition is not exact")
        if self.candidate_only is not True or self.native_api_reachable is not False or self.rehearsal_pass is not False:
            raise ValueError("offline integration diagnostic cannot carry live authority")


def _diagnostic(value: dict[str, object], trace: tuple[str, ...], failure: str | None) -> OfflineIntegrationDiagnostic:
    raw = _canonical_json(value)
    return OfflineIntegrationDiagnostic(raw, hashlib.sha256(raw).hexdigest(), trace, trace[-1], failure)


def _rejected(failure: str) -> OfflineIntegrationDiagnostic:
    return _diagnostic(
        {
            "candidate_only": True,
            "failure_class": failure,
            "native_api_reachable": False,
            "rehearsal_pass": False,
            "schema_id": "S0-PUBLIC-ASSEMBLY-RUNTIME-PRELOADER-OFFLINE-DIAGNOSTIC-1",
            "state_trace": list(_REJECTED_TRACE),
            "terminal_state": _REJECTED_TRACE[-1],
        },
        _REJECTED_TRACE,
        failure,
    )


def prepare_offline_integration_diagnostic(
    *,
    artifacts: AssemblyArtifactBundle,
    closure: PublicInputClosure,
    profile_raw: bytes,
    schema_raw: bytes,
    static_material: StaticMaterialBundle,
    inputs: OfflinePreloaderInputs,
) -> OfflineIntegrationDiagnostic:
    """Reauthenticate original bytes and emit data that can never authorize live work."""

    try:
        _verify_public_input_closure(closure)
        prepared = prepare_assembly_runtime_launch(
            artifacts=artifacts,
            profile_raw=profile_raw,
            schema_raw=schema_raw,
            static_material=static_material,
            inputs=inputs,
        )
    except Exception:
        return _rejected("offline-input-or-plan-rejected")
    if prepared.candidate_only is not True or prepared.native_api_reachable is not False:
        return _rejected("offline-authority-boundary-rejected")
    return _diagnostic(
        {
            "candidate_only": True,
            "effective_runtime_package_sha256": prepared.effective_runtime_package_sha256,
            "failure_class": None,
            "launch_evidence_sha256": prepared.evidence.sha256,
            "native_api_reachable": False,
            "rehearsal_pass": False,
            "runtime_profile_sha256": prepared.runtime_profile_sha256,
            "schema_id": "S0-PUBLIC-ASSEMBLY-RUNTIME-PRELOADER-OFFLINE-DIAGNOSTIC-1",
            "state_trace": list(_SUCCESS_TRACE),
            "terminal_state": _SUCCESS_TRACE[-1],
        },
        _SUCCESS_TRACE,
        None,
    )

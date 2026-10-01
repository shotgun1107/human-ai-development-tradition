"""Deterministic offline launch evidence and admission-frame candidates."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Mapping

from .canonical import canonical_json_bytes, load_json_bytes, require_sha256, sha256_bytes
from .errors import RuntimeProfileError
from .semantic import (
    ArtifactMaterial,
    HandleObservation,
    OFFLINE_POSTCREATION_RELATIONS,
    PostcreationObservation,
    _snapshot_postcreation_observation,
    validate_postcreation_relation,
)


_LOCATOR = re.compile(r"^0x[0-9a-f]{16}$")
_VIRTUAL_PATH = re.compile(r"^[A-Za-z0-9._/-]+$")


@dataclass(frozen=True)
class LaunchControl:
    raw: bytes
    application_path: str
    command_line: str
    environment_block: tuple[str, ...]
    current_directory: str
    preloader_virtual_path: str
    application_virtual_path: str
    bootstrap_virtual_path: str
    verifier_virtual_path: str


def _require_virtual_path(value: object, label: str) -> str:
    if (
        type(value) is not str
        or _VIRTUAL_PATH.fullmatch(value) is None
        or len(value) > 1024
        or value.startswith("/")
        or value.endswith("/")
        or "//" in value
        or any(part in {"", ".", ".."} or len(part) > 255 or part.endswith(".") for part in value.split("/"))
    ):
        raise RuntimeProfileError(f"{label} is not one canonical virtual path")
    return value


def load_launch_control(raw: bytes) -> LaunchControl:
    """Parse the only admitted process-input source from authenticated bytes."""

    value = load_json_bytes(raw, canonical=True)
    if not isinstance(value, dict) or set(value) != {
        "application_path",
        "application_virtual_path",
        "bootstrap_virtual_path",
        "command_line",
        "current_directory",
        "environment_block",
        "preloader_virtual_path",
        "verifier_virtual_path",
    }:
        raise RuntimeProfileError("launch control object is not exact")
    for name in ("application_path", "command_line", "current_directory"):
        item = value[name]
        if type(item) is not str or not item or "\x00" in item:
            raise RuntimeProfileError("launch control string input is malformed")
    environment = value["environment_block"]
    if not isinstance(environment, list) or any(
        type(item) is not str or "=" not in item or "\x00" in item
        for item in environment
    ):
        raise RuntimeProfileError("launch control environment block is malformed")
    environment_block = tuple(environment)
    if environment_block != tuple(sorted(set(environment_block))):
        raise RuntimeProfileError("launch control environment block is not sorted and unique")
    return LaunchControl(
        raw=raw,
        application_path=value["application_path"],
        command_line=value["command_line"],
        environment_block=environment_block,
        current_directory=value["current_directory"],
        preloader_virtual_path=_require_virtual_path(
            value["preloader_virtual_path"], "preloader virtual path"
        ),
        application_virtual_path=_require_virtual_path(
            value["application_virtual_path"], "application virtual path"
        ),
        bootstrap_virtual_path=_require_virtual_path(
            value["bootstrap_virtual_path"], "bootstrap virtual path"
        ),
        verifier_virtual_path=_require_virtual_path(
            value["verifier_virtual_path"], "verifier virtual path"
        ),
    )


@dataclass(frozen=True)
class LaunchMaterialSet:
    preloader: ArtifactMaterial
    application: ArtifactMaterial
    bootstrap: ArtifactMaterial
    verifier: ArtifactMaterial


@dataclass(frozen=True)
class LaunchIdentity:
    run_nonce: str
    external_pin_digest: str
    workspace_root: str
    runtime_profile_v0_1_sha256: str
    runtime_profile_v0_2_sha256: str
    runtime_profile_v0_3_sha256: str
    runtime_profile_v0_4_sha256: str
    preloader_image_sha256: str
    runtime_package_sha256: str
    launch_control_sha256: str
    application_virtual_path: str
    application_sha256: str
    bootstrap_virtual_path: str
    bootstrap_sha256: str
    verifier_virtual_path: str
    verifier_sha256: str

    def __post_init__(self) -> None:
        for value in (
            self.run_nonce,
            self.external_pin_digest,
            self.runtime_profile_v0_1_sha256,
            self.runtime_profile_v0_2_sha256,
            self.runtime_profile_v0_3_sha256,
            self.runtime_profile_v0_4_sha256,
            self.preloader_image_sha256,
            self.runtime_package_sha256,
            self.launch_control_sha256,
            self.application_sha256,
            self.bootstrap_sha256,
            self.verifier_sha256,
        ):
            require_sha256(value, "launch identity hash or nonce")
        _canonical_workspace(self.workspace_root)


@dataclass(frozen=True)
class OfflineLaunchEvidenceDiagnostic:
    raw: bytes
    sha256: str
    handles: tuple[HandleObservation, ...]
    candidate_only: bool = True

    def __post_init__(self) -> None:
        if self.candidate_only is not True or sha256_bytes(self.raw) != self.sha256:
            raise RuntimeProfileError("launch evidence is not a byte-bound offline candidate")


@dataclass(frozen=True)
class OfflineAdmissionDiagnostic:
    raw: bytes
    sha256: str
    actual_verifier_pid: int
    launch_evidence_sha256: str
    offline_postcreation_relations: tuple[str, ...]
    candidate_only: bool = True

    def __post_init__(self) -> None:
        if self.candidate_only is not True or sha256_bytes(self.raw) != self.sha256:
            raise RuntimeProfileError("admission diagnostic is not a byte-bound offline candidate")
        if self.offline_postcreation_relations != OFFLINE_POSTCREATION_RELATIONS:
            raise RuntimeProfileError("postcreation relation set is incomplete")


def build_launch_identity(
    *,
    run_nonce: str,
    runtime_package_manifest_raw: bytes,
    control: LaunchControl,
    material: LaunchMaterialSet,
    external_pin_digest: str,
    workspace_root: str,
    profile_hashes: tuple[str, str, str, str],
) -> LaunchIdentity:
    require_sha256(run_nonce, "launch run nonce")
    if type(profile_hashes) is not tuple or len(profile_hashes) != 4:
        raise RuntimeProfileError("evidence requires four predecessor hashes")
    if type(runtime_package_manifest_raw) is not bytes:
        raise RuntimeProfileError("runtime package manifest is not exact bytes")
    if type(control) is not LaunchControl or (
        material.preloader.virtual_path,
        material.application.virtual_path,
        material.bootstrap.virtual_path,
        material.verifier.virtual_path,
    ) != (
        control.preloader_virtual_path,
        control.application_virtual_path,
        control.bootstrap_virtual_path,
        control.verifier_virtual_path,
    ):
        raise RuntimeProfileError("launch control and launch materials differ")
    return LaunchIdentity(
        run_nonce=run_nonce,
        external_pin_digest=external_pin_digest,
        workspace_root=workspace_root,
        runtime_profile_v0_1_sha256=profile_hashes[0],
        runtime_profile_v0_2_sha256=profile_hashes[1],
        runtime_profile_v0_3_sha256=profile_hashes[2],
        runtime_profile_v0_4_sha256=profile_hashes[3],
        preloader_image_sha256=material.preloader.sha256,
        runtime_package_sha256=sha256_bytes(runtime_package_manifest_raw),
        launch_control_sha256=sha256_bytes(control.raw),
        application_virtual_path=material.application.virtual_path,
        application_sha256=material.application.sha256,
        bootstrap_virtual_path=material.bootstrap.virtual_path,
        bootstrap_sha256=material.bootstrap.sha256,
        verifier_virtual_path=material.verifier.virtual_path,
        verifier_sha256=material.verifier.sha256,
    )


def _ascii_field(name: str, value: object) -> bytes:
    if type(name) is not str or not name or "=" in name or "\n" in name:
        raise RuntimeProfileError("evidence field name is not exact ASCII text")
    text = str(value)
    if not text or any(ord(char) < 0x20 or ord(char) > 0x7E for char in text):
        raise RuntimeProfileError("evidence field value is not printable ASCII")
    if "=" in text or "\n" in text or "\r" in text:
        raise RuntimeProfileError("evidence field value contains a delimiter")
    return f"{name}={text}\n".encode("ascii")


def build_offline_launch_evidence_diagnostic(
    profile: Mapping[str, object],
    identity: LaunchIdentity,
    handles: tuple[HandleObservation, ...],
) -> OfflineLaunchEvidenceDiagnostic:
    process = profile["process_creation_policy"]
    launch = profile["launch_handle_set_evidence"]
    if not isinstance(process, Mapping) or not isinstance(launch, Mapping):
        raise RuntimeProfileError("launch profile objects are absent")
    if type(handles) is not tuple or len(handles) != 5:
        raise RuntimeProfileError("launch evidence requires exactly five handles")
    expected = tuple(
        (item["role"], item["kind"], item["access"])
        for item in process["ordered_handles"]
    )
    actual = tuple((item.role, item.kind, item.access) for item in handles)
    locators = tuple(item.locator for item in handles)
    if actual != expected:
        raise RuntimeProfileError("launch evidence handle order or policy differs")
    if (
        any(_LOCATOR.fullmatch(value) is None for value in locators)
        or len(set(locators)) != 5
        or any(value in {"0x0000000000000000", "0xffffffffffffffff"} for value in locators)
    ):
        raise RuntimeProfileError("launch evidence locator set is invalid")

    if launch.get("evidence_schema_id") != "S0-LAUNCH-HANDLE-SET-EVIDENCE-2":
        raise RuntimeProfileError("v1/v2 launch policy mixing rejects")
    fields = {
        "schema_id": "S0-LAUNCH-HANDLE-SET-EVIDENCE-2",
        "run_nonce": identity.run_nonce,
        "external_pin_digest": identity.external_pin_digest,
        "workspace_root": identity.workspace_root,
        "preloader_image_sha256": identity.preloader_image_sha256,
        "runtime_package_sha256": identity.runtime_package_sha256,
        "launch_control_sha256": identity.launch_control_sha256,
        "runtime_profile_v0_1_sha256": identity.runtime_profile_v0_1_sha256,
        "runtime_profile_v0_2_sha256": identity.runtime_profile_v0_2_sha256,
        "runtime_profile_v0_3_sha256": identity.runtime_profile_v0_3_sha256,
        "runtime_profile_v0_4_sha256": identity.runtime_profile_v0_4_sha256,
        "application_virtual_path": identity.application_virtual_path,
        "application_sha256": identity.application_sha256,
        "bootstrap_virtual_path": identity.bootstrap_virtual_path,
        "bootstrap_sha256": identity.bootstrap_sha256,
        "verifier_virtual_path": identity.verifier_virtual_path,
        "verifier_sha256": identity.verifier_sha256,
        "creation_flags_numeric": process["creation_flags_numeric"],
        "startupinfoex_dwflags": str(process["startupinfoex_dwflags"]),
        "b_inherit_handles": "true" if process["b_inherit_handles"] else "false",
        "attribute_count": str(process["attribute_count"]),
        "attribute_id_numeric": process["attribute_id_numeric"],
        "handle_array_bytes_x64": str(process["handle_array_bytes_x64"]),
        "handle_count": str(process["handle_count"]),
        "precreation_verifier_pid": "0",
    }
    for index, handle in enumerate(handles):
        fields[f"handle_{index}_role"] = handle.role
        fields[f"handle_{index}_kind"] = handle.kind
        fields[f"handle_{index}_access"] = handle.access
        fields[f"handle_{index}_locator"] = handle.locator
    raw = serialize_launch_evidence_v2(fields)
    return OfflineLaunchEvidenceDiagnostic(raw, sha256_bytes(raw), handles)


def build_offline_admission_diagnostic(
    profile: Mapping[str, object],
    *,
    evidence: OfflineLaunchEvidenceDiagnostic,
    observation: PostcreationObservation,
    runtime_profile_v0_4_sha256: str,
    effective_runtime_package_sha256: str,
) -> OfflineAdmissionDiagnostic:
    require_sha256(runtime_profile_v0_4_sha256, "v0.4 profile hash")
    require_sha256(effective_runtime_package_sha256, "runtime package hash")
    observed = _snapshot_postcreation_observation(observation)
    relations = validate_postcreation_relation(
        observed,
        expected_evidence_sha256=evidence.sha256,
    )
    policy = profile["admission_frame_policy"]
    if not isinstance(policy, Mapping):
        raise RuntimeProfileError("admission frame policy is absent")
    value: dict[str, object] = {
        "candidate_only": True,
        "claimed_createprocess_result_policy_id": observed.success_policy_id,
        "claimed_guard_observation_policy_id": policy["guard_observation_policy_id"],
        "claimed_kernel_semantics_policy_id": policy["kernel_semantics_policy_id"],
        "claimed_preloader_responsibility_id": policy["preloader_responsibility_id"],
        "effective_runtime_package_sha256": effective_runtime_package_sha256,
        "offline_launch_evidence_diagnostic_sha256": evidence.sha256,
        "observation_source": observed.source,
        "observed_actual_verifier_pid": observed.actual_verifier_pid,
        "rehearsal_pass": False,
        "runtime_profile_v0_1_sha256": profile["v0_1_profile_sha256"],
        "runtime_profile_v0_2_sha256": profile["v0_2_profile_sha256"],
        "runtime_profile_v0_3_sha256": profile["v0_3_profile_sha256"],
        "runtime_profile_v0_4_sha256": runtime_profile_v0_4_sha256,
        "schema_id": "S0-OFFLINE-ADMISSION-DIAGNOSTIC-1",
        "target_admission_schema_id": policy["schema_id"],
        "target_launch_evidence_schema_id": "S0-LAUNCH-HANDLE-SET-EVIDENCE-2",
    }
    raw = canonical_json_bytes(value)
    if len(raw) > policy["maximum_bytes"]:
        raise RuntimeProfileError("admission frame exceeds its exact bound")
    forbidden = ("locator", "handle_value", "numeric_handle")
    if any(any(token in key for token in forbidden) for key in value):
        raise RuntimeProfileError("admission frame exposes forbidden locator authority")
    if any(type(item) is str and _LOCATOR.fullmatch(item) for item in value.values()):
        raise RuntimeProfileError("admission frame exposes a forbidden locator value")
    return OfflineAdmissionDiagnostic(
        raw=raw,
        sha256=sha256_bytes(raw),
        actual_verifier_pid=observed.actual_verifier_pid,
        launch_evidence_sha256=evidence.sha256,
        offline_postcreation_relations=relations,
    )


EVIDENCE_V2_FIELDS = (
    "schema_id",
    "run_nonce",
    "external_pin_digest",
    "workspace_root",
    "preloader_image_sha256",
    "runtime_package_sha256",
    "launch_control_sha256",
    "runtime_profile_v0_1_sha256",
    "runtime_profile_v0_2_sha256",
    "runtime_profile_v0_3_sha256",
    "runtime_profile_v0_4_sha256",
    "application_virtual_path",
    "application_sha256",
    "bootstrap_virtual_path",
    "bootstrap_sha256",
    "verifier_virtual_path",
    "verifier_sha256",
    "creation_flags_numeric",
    "startupinfoex_dwflags",
    "b_inherit_handles",
    "attribute_count",
    "attribute_id_numeric",
    "handle_array_bytes_x64",
    "handle_count",
    "handle_0_role",
    "handle_0_kind",
    "handle_0_access",
    "handle_0_locator",
    "handle_1_role",
    "handle_1_kind",
    "handle_1_access",
    "handle_1_locator",
    "handle_2_role",
    "handle_2_kind",
    "handle_2_access",
    "handle_2_locator",
    "handle_3_role",
    "handle_3_kind",
    "handle_3_access",
    "handle_3_locator",
    "handle_4_role",
    "handle_4_kind",
    "handle_4_access",
    "handle_4_locator",
    "precreation_verifier_pid",
)
_EVIDENCE_V2_CONSTANTS = {
    "schema_id": "S0-LAUNCH-HANDLE-SET-EVIDENCE-2",
    "creation_flags_numeric": "0x08080404",
    "startupinfoex_dwflags": "0",
    "b_inherit_handles": "true",
    "attribute_count": "1",
    "attribute_id_numeric": "0x00020002",
    "handle_array_bytes_x64": "40",
    "handle_count": "5",
    "handle_0_role": "admission-read",
    "handle_0_kind": "byte-stream-pipe-endpoint",
    "handle_0_access": "read-not-write-data",
    "handle_1_role": "commit-request-write",
    "handle_1_kind": "byte-stream-pipe-endpoint",
    "handle_1_access": "write-not-read-data",
    "handle_2_role": "commit-reply-read",
    "handle_2_kind": "byte-stream-pipe-endpoint",
    "handle_2_access": "read-not-write-data",
    "handle_3_role": "output-root",
    "handle_3_kind": "directory",
    "handle_3_access": "file-list-directory-read-attributes-synchronize-only",
    "handle_4_role": "preloader-process",
    "handle_4_kind": "process",
    "handle_4_access": "process-query-limited-information-synchronize-only",
    "precreation_verifier_pid": "0"
}

def _canonical_workspace(value: str) -> None:
    if (
        not 3 <= len(value) <= 32766
        or not "A" <= value[0] <= "Z"
        or value[1:3] != ":\\"
        or (len(value) > 3 and value.endswith("\\"))
        or any(char in value for char in '/="<>|?*')
    ):
        raise RuntimeProfileError("evidence workspace root is not canonical")
    if len(value) > 3:
        for component in value[3:].split("\\"):
            if (
                not component or component in {".", ".."} or len(component) > 255
                or component[-1] in {".", " "} or ":" in component
            ):
                raise RuntimeProfileError("evidence workspace component is not canonical")


def serialize_launch_evidence_v2(fields: Mapping[str, str]) -> bytes:
    """Encode data in the production v2 grammar; this creates no authority."""

    if not isinstance(fields, Mapping) or set(fields) != set(EVIDENCE_V2_FIELDS):
        raise RuntimeProfileError("evidence v2 requires all and only its 45 fields")
    snapshot = dict(fields)
    for name in EVIDENCE_V2_FIELDS:
        value = snapshot[name]
        if type(value) is not str or not value or any(
            ord(char) < 32 or ord(char) > 126 or char == "=" for char in value
        ):
            raise RuntimeProfileError("evidence v2 field is not delimiter-free ASCII")
        if name in _EVIDENCE_V2_CONSTANTS:
            if value != _EVIDENCE_V2_CONSTANTS[name]:
                raise RuntimeProfileError("evidence v2 constant differs")
        elif name == "run_nonce" or name == "external_pin_digest" or name.endswith("_sha256"):
            require_sha256(value, name)
        elif name == "workspace_root":
            _canonical_workspace(value)
        elif name.endswith("_virtual_path"):
            _require_virtual_path(value, name)
        elif name.endswith("_locator"):
            if _LOCATOR.fullmatch(value) is None or not 0 < int(value[2:], 16) < 0xFFFFFFFFFFFFFFFA:
                raise RuntimeProfileError("evidence v2 locator differs")
        else:
            raise RuntimeProfileError("evidence v2 field is unclassified")
    if len({snapshot[f"handle_{i}_locator"] for i in range(5)}) != 5:
        raise RuntimeProfileError("evidence v2 handles are not distinct")
    raw = b"".join(_ascii_field(name, snapshot[name]) for name in EVIDENCE_V2_FIELDS)
    if len(raw) > 65536:
        raise RuntimeProfileError("evidence v2 exceeds its byte bound")
    return raw


def parse_launch_evidence_v2(raw: bytes) -> dict[str, str]:
    """Independently parse supplied production bytes without trusting a wrapper."""

    if (
        type(raw) is not bytes or not raw or len(raw) > 65536
        or not raw.endswith(b"\n") or b"\r" in raw
    ):
        raise RuntimeProfileError("evidence v2 framing differs")
    try:
        lines = raw.decode("ascii", errors="strict").split("\n")
    except UnicodeDecodeError as exc:
        raise RuntimeProfileError("evidence v2 encoding differs") from exc
    if len(lines) != 46 or lines[-1] != "":
        raise RuntimeProfileError("evidence v2 field count differs")
    fields: dict[str, str] = {}
    for name, line in zip(EVIDENCE_V2_FIELDS, lines[:-1], strict=True):
        if line.count("=") != 1:
            raise RuntimeProfileError("evidence v2 field delimiter differs")
        observed, value = line.split("=", 1)
        if observed != name:
            raise RuntimeProfileError("evidence v2 field order or version differs")
        fields[name] = value
    if serialize_launch_evidence_v2(fields) != raw:
        raise RuntimeProfileError("evidence v2 is not canonical")
    return fields


def validate_launch_evidence_v2(raw: bytes, *, expected_fields: Mapping[str, str]) -> dict[str, str]:
    """Compare production bytes to independently supplied expected identities."""
    parsed = parse_launch_evidence_v2(raw)
    if raw != serialize_launch_evidence_v2(expected_fields):
        raise RuntimeProfileError("evidence v2 differs from expected launch identities")
    return parsed

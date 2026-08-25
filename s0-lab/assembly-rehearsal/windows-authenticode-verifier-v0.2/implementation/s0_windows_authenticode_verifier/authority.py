"""Authenticate installed source bytes as a trusted-host consistency check."""

from __future__ import annotations

from pathlib import Path
import re

from .canonical import VerificationError, require_sha256, sha256_hex
from .model import VerificationAuthority


_BASE = "s0-lab/assembly-rehearsal/windows-authenticode-verifier-v0.2"
_PACKAGE = f"{_BASE}/implementation/s0_windows_authenticode_verifier"
IMPLEMENTATION_MANIFEST = f"{_BASE}/verification/implementation-files.sha256"
POLICY_MANIFEST = f"{_BASE}/verification/policy-contract-files.sha256"
ACQUISITION_MANIFEST = f"{_BASE}/verification/acquisition-validator-files.sha256"
NATIVE_MANIFEST = f"{_BASE}/verification/native-verifier-files.sha256"
SEMANTIC_MANIFEST = f"{_BASE}/verification/semantic-validator-files.sha256"
ORCHESTRATOR_MANIFEST = f"{_BASE}/verification/runtime-orchestrator-files.sha256"

POLICY_TARGETS = (f"{_PACKAGE}/contract.py",)
ACQUISITION_TARGETS = (f"{_PACKAGE}/acquisition.py",)
NATIVE_TARGETS = (f"{_PACKAGE}/win32.py",)
SEMANTIC_TARGETS = (
    f"{_PACKAGE}/canonical.py",
    f"{_PACKAGE}/model.py",
    f"{_PACKAGE}/semantic.py",
)
ORCHESTRATOR_TARGETS = (
    f"{_PACKAGE}/__init__.py",
    f"{_PACKAGE}/authority.py",
    f"{_PACKAGE}/verifier.py",
)
IMPLEMENTATION_TARGETS = tuple(
    sorted(
        POLICY_TARGETS
        + ACQUISITION_TARGETS
        + NATIVE_TARGETS
        + SEMANTIC_TARGETS
        + ORCHESTRATOR_TARGETS
        + (
            POLICY_MANIFEST,
            ACQUISITION_MANIFEST,
            NATIVE_MANIFEST,
            SEMANTIC_MANIFEST,
            ORCHESTRATOR_MANIFEST,
        )
    )
)

_ROW = re.compile(rb"^([0-9a-f]{64})  ([A-Za-z0-9._/-]+)$")


def _workspace() -> Path:
    source = Path(__file__).resolve()
    for parent in source.parents:
        if (parent / "AGENTS.md").is_file():
            return parent
    raise VerificationError("workspace authority root is unavailable")


def _authenticate_manifest(
    workspace: Path,
    logical_path: str,
    expected_sha256: str | None,
    expected_targets: tuple[str, ...],
) -> bytes:
    raw = (workspace / logical_path).read_bytes()
    if expected_sha256 is not None and sha256_hex(raw) != require_sha256(
        expected_sha256, name="implementation manifest"
    ):
        raise VerificationError("implementation manifest pin differs")
    if not raw.endswith(b"\n") or b"\r" in raw or raw.startswith(b"\xef\xbb\xbf"):
        raise VerificationError("manifest byte grammar differs")
    rows = raw[:-1].split(b"\n")
    paths: list[str] = []
    for row in rows:
        match = _ROW.fullmatch(row)
        if match is None:
            raise VerificationError("manifest row grammar differs")
        digest = match.group(1).decode("ascii")
        path = match.group(2).decode("ascii")
        target = (workspace / path).read_bytes()
        if sha256_hex(target) != digest:
            raise VerificationError("manifest target hash differs")
        paths.append(path)
    if tuple(paths) != tuple(sorted(paths)) or tuple(paths) != expected_targets:
        raise VerificationError("manifest target closure differs")
    return raw


def authenticate_installed_implementation(
    expected_implementation_manifest_sha256: str,
    *,
    expected_acquisition_record_sha256: str,
    expected_acquisition_authority_manifest_sha256: str,
) -> VerificationAuthority:
    """Bind disk bytes and external acquisition pins without claiming runtime authority."""

    workspace = _workspace()
    outer = _authenticate_manifest(
        workspace,
        IMPLEMENTATION_MANIFEST,
        expected_implementation_manifest_sha256,
        IMPLEMENTATION_TARGETS,
    )
    policy = _authenticate_manifest(workspace, POLICY_MANIFEST, None, POLICY_TARGETS)
    acquisition = _authenticate_manifest(
        workspace,
        ACQUISITION_MANIFEST,
        None,
        ACQUISITION_TARGETS,
    )
    native = _authenticate_manifest(workspace, NATIVE_MANIFEST, None, NATIVE_TARGETS)
    semantic = _authenticate_manifest(workspace, SEMANTIC_MANIFEST, None, SEMANTIC_TARGETS)
    _authenticate_manifest(workspace, ORCHESTRATOR_MANIFEST, None, ORCHESTRATOR_TARGETS)
    return VerificationAuthority(
        implementation_manifest_sha256=sha256_hex(outer),
        policy_manifest_sha256=sha256_hex(policy),
        acquisition_validator_manifest_sha256=sha256_hex(acquisition),
        native_verifier_manifest_sha256=sha256_hex(native),
        semantic_validator_manifest_sha256=sha256_hex(semantic),
        acquisition_record_sha256=require_sha256(
            expected_acquisition_record_sha256,
            name="acquisition record",
        ),
        acquisition_authority_manifest_sha256=require_sha256(
            expected_acquisition_authority_manifest_sha256,
            name="acquisition authority manifest",
        ),
    )

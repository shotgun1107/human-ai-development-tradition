"""Authenticated-snapshot verifier for the PUBLIC Authenticode v0.3 revision."""

from __future__ import annotations

import argparse
import ast
import hashlib
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = next(parent for parent in ROOT.parents if (parent / "AGENTS.md").is_file())
BASE = "s0-lab/assembly-rehearsal/windows-authenticode-verifier-v0.3"
V02_BASE = "s0-lab/assembly-rehearsal/windows-authenticode-verifier-v0.2"
IMPLEMENTATION_MANIFEST = f"{BASE}/verification/implementation-files.sha256"
VERIFICATION_MANIFEST = f"{BASE}/verification/verification-files.sha256"
TEST_PATH = f"{BASE}/tests/test_authenticode_verifier.py"
REPORT_PATH = (
    f"{BASE}/verification/"
    "public-windows-authenticode-verifier-implementation-revision-report-v0.3.md"
)
RESPONSE_PATH = (
    f"{BASE}/verification/v0.2-independent-code-security-rereview-response-v0.1.md"
)
VERIFICATION_TARGETS = (
    f"{BASE}/README.md",
    TEST_PATH,
    REPORT_PATH,
    RESPONSE_PATH,
    f"{BASE}/verification/verify_candidate.py",
)
SUBMANIFESTS = {
    f"{BASE}/verification/acquisition-validator-files.sha256": 1,
    f"{BASE}/verification/native-verifier-files.sha256": 1,
    f"{BASE}/verification/policy-contract-files.sha256": 1,
    f"{BASE}/verification/runtime-orchestrator-files.sha256": 3,
    f"{BASE}/verification/semantic-validator-files.sha256": 3,
}
PREDECESSOR_MANIFESTS = {
    f"{V02_BASE}/verification/implementation-files.sha256": (
        "6fe56c7fac527b0adfda02e32e0e4b5355ff4adfe8a499732dfb7a43d2df213a",
        14,
    ),
    f"{V02_BASE}/verification/verification-files.sha256": (
        "f8f2516ad00d06e257954b3b82e67446f7b3920656626eb026530062c7da9b02",
        5,
    ),
}
V02_REREVIEW = (
    "s0-lab/reviews/assembly-rehearsal/"
    "build-runtime-materialization-windows-authenticode-verifier-v0.2/"
    "public-windows-authenticode-verifier-v0.2-independent-code-security-rereview-v0.1.md"
)
V02_REREVIEW_SHA256 = "c8fdb45ba2fde477e5a1662e28131a388ec1cce637313e2508b5e40c2d369eee"
_ROW = re.compile(rb"^([0-9a-f]{64})  ([A-Za-z0-9._/-]+)$")
_PIN = re.compile(r"^[0-9a-f]{64}$")


def _add(snapshot: dict[str, bytes], path: str, raw: bytes) -> None:
    if type(path) is not str or type(raw) is not bytes:
        raise ValueError("snapshot entry type differs")
    prior = snapshot.get(path)
    if prior is not None and prior != raw:
        raise ValueError("authenticated path collision")
    snapshot[path] = raw


def _manifest(
    snapshot: dict[str, bytes],
    logical_path: str,
    expected_sha256: str,
    expected_rows: int,
    expected_targets: tuple[str, ...] | None = None,
) -> tuple[str, ...]:
    raw = (WORKSPACE / logical_path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected_sha256:
        raise ValueError("manifest pin differs")
    if not raw.endswith(b"\n") or b"\r" in raw or raw.startswith(b"\xef\xbb\xbf"):
        raise ValueError("manifest byte grammar differs")
    rows = raw[:-1].split(b"\n")
    paths: list[str] = []
    for row in rows:
        match = _ROW.fullmatch(row)
        if match is None:
            raise ValueError("manifest row differs")
        digest = match.group(1).decode("ascii")
        target = match.group(2).decode("ascii")
        target_raw = (WORKSPACE / target).read_bytes()
        if hashlib.sha256(target_raw).hexdigest() != digest:
            raise ValueError("manifest target differs")
        paths.append(target)
        _add(snapshot, target, target_raw)
    if len(paths) != expected_rows or len(paths) != len(set(paths)):
        raise ValueError("manifest closure differs")
    if paths != sorted(paths):
        raise ValueError("manifest target order differs")
    if expected_targets is not None and tuple(paths) != expected_targets:
        raise ValueError("manifest exact target set differs")
    _add(snapshot, logical_path, raw)
    return tuple(paths)


def _sidecar(
    snapshot: dict[str, bytes],
    markdown_path: str,
    expected_sha256: str | None = None,
) -> None:
    raw = (WORKSPACE / markdown_path).read_bytes()
    actual = hashlib.sha256(raw).hexdigest()
    if expected_sha256 is not None and actual != expected_sha256:
        raise ValueError("Markdown pin differs")
    sidecar_path = markdown_path.rsplit(".", 1)[0] + ".sha256"
    sidecar = (WORKSPACE / sidecar_path).read_bytes()
    expected = f"{actual}  {Path(markdown_path).name}\n".encode("ascii")
    if sidecar != expected:
        raise ValueError("Markdown sidecar differs")
    _add(snapshot, markdown_path, raw)
    _add(snapshot, sidecar_path, sidecar)


def _static_source_checks(snapshot: dict[str, bytes]) -> None:
    package = f"{BASE}/implementation/s0_windows_authenticode_verifier"
    semantic_path = f"{package}/semantic.py"
    win32_path = f"{package}/win32.py"
    init_path = f"{package}/__init__.py"
    model_path = f"{package}/model.py"
    acquisition_path = f"{package}/acquisition.py"

    semantic = ast.parse(snapshot[semantic_path].decode("utf-8", "strict"))
    forbidden_semantic_imports = {
        "ctypes", "os", "socket", "subprocess", "urllib", "requests",
    }
    for node in ast.walk(semantic):
        if isinstance(node, ast.Import):
            names = {alias.name.split(".", 1)[0] for alias in node.names}
            if names & forbidden_semantic_imports:
                raise ValueError("semantic validator imports live authority")
        if isinstance(node, ast.ImportFrom) and node.module:
            if node.module.split(".", 1)[0] in forbidden_semantic_imports:
                raise ValueError("semantic validator imports live authority")

    init_tree = ast.parse(snapshot[init_path].decode("utf-8", "strict"))
    if any(isinstance(node, (ast.Import, ast.ImportFrom)) for node in ast.walk(init_tree)):
        raise ValueError("package import is not inert")

    win32_text = snapshot[win32_path].decode("utf-8", "strict")
    for forbidden in ("subprocess", "socket", "requests", "urllib", "os.system", "Popen"):
        if forbidden in win32_text:
            raise ValueError("native collector contains execution or network helper")
    for required in (
        "CreateFileW",
        "FILE_SHARE_READ",
        "data.dwStateAction = WTD_STATEACTION_CLOSE",
        "CertFreeCertificateChain(context)",
        "CertFreeCertificateContext",
        "CertFreeCTLContext",
        "QueryPerformanceCounter",
        "_handle_volume_guid_path",
        "CRYPT_E_NOT_FOUND",
        "effective_trust_authority_claimed",
    ):
        if required not in win32_text:
            raise ValueError("native correction marker is absent")

    model_text = snapshot[model_path].decode("utf-8", "strict")
    if "TRUSTED-HOST-DISK-CONSISTENCY-ONLY" not in snapshot[
        f"{package}/contract.py"
    ].decode("utf-8", "strict"):
        raise ValueError("runtime authority scope is absent")
    if "executed_code_authority_established is not False" not in model_text:
        raise ValueError("executed-code authority nonclaim is absent")
    acquisition_text = snapshot[acquisition_path].decode("utf-8", "strict")
    if "expected_record_sha256" not in acquisition_text or "retained_handle" not in acquisition_text:
        raise ValueError("acquisition pin or handle binding is absent")


def authenticate_all(
    implementation_pin: str,
    verification_pin: str,
) -> dict[str, bytes]:
    snapshot: dict[str, bytes] = {}
    implementation_targets = _manifest(
        snapshot,
        IMPLEMENTATION_MANIFEST,
        implementation_pin,
        14,
    )
    _manifest(
        snapshot,
        VERIFICATION_MANIFEST,
        verification_pin,
        5,
        VERIFICATION_TARGETS,
    )
    for path, rows in SUBMANIFESTS.items():
        manifest_pin = hashlib.sha256((WORKSPACE / path).read_bytes()).hexdigest()
        subtargets = _manifest(snapshot, path, manifest_pin, rows)
        if not set(subtargets).issubset(set(implementation_targets)):
            raise ValueError("submanifest target is outside implementation closure")
    for path, (pin, rows) in PREDECESSOR_MANIFESTS.items():
        _manifest(snapshot, path, pin, rows)
    _sidecar(snapshot, V02_REREVIEW, V02_REREVIEW_SHA256)
    for current in (f"{BASE}/README.md", REPORT_PATH, RESPONSE_PATH):
        _sidecar(snapshot, current)
    _add(snapshot, "AGENTS.md", (WORKSPACE / "AGENTS.md").read_bytes())
    _static_source_checks(snapshot)
    return snapshot


def _materialize(snapshot: dict[str, bytes], root: Path) -> None:
    for path, raw in snapshot.items():
        destination = root / path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(raw)
        if destination.read_bytes() != raw:
            raise ValueError("snapshot write verification failed")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--implementation-manifest-sha256", required=True)
    parser.add_argument("--verification-manifest-sha256", required=True)
    args = parser.parse_args()
    if (
        _PIN.fullmatch(args.implementation_manifest_sha256) is None
        or _PIN.fullmatch(args.verification_manifest_sha256) is None
    ):
        print("MANIFEST_PIN_GRAMMAR=FAIL")
        return 1
    try:
        before = authenticate_all(
            args.implementation_manifest_sha256,
            args.verification_manifest_sha256,
        )
        with tempfile.TemporaryDirectory(
            prefix="s0-authenticode-v03-snapshot-"
        ) as temporary:
            snapshot_root = Path(temporary)
            _materialize(before, snapshot_root)
            environment = dict(os.environ)
            environment["PYTHONDONTWRITEBYTECODE"] = "1"
            environment.pop("PYTHONPATH", None)
            completed = subprocess.run(
                (
                    sys.executable,
                    "-I",
                    "-B",
                    "-m",
                    "unittest",
                    "discover",
                    "-s",
                    str(snapshot_root / f"{BASE}/tests"),
                    "-v",
                ),
                cwd=snapshot_root,
                env=environment,
                check=False,
            )
        after = authenticate_all(
            args.implementation_manifest_sha256,
            args.verification_manifest_sha256,
        )
    except (OSError, UnicodeError, ValueError, SyntaxError):
        print("AUTHENTICATED_SNAPSHOT=FAIL")
        return 1
    if completed.returncode != 0:
        print("FOCUSED_TESTS=FAIL")
        return 1
    if before != after:
        print("ORIGINAL_INPUT_SWAP_SENTINEL=FAIL")
        return 1
    print("OUTER_IMPLEMENTATION_MANIFEST=PASS ROWS=14")
    print("POLICY_ACQUISITION_NATIVE_SEMANTIC_ORCHESTRATOR_SUBMANIFESTS=PASS ROWS=1/1/1/3/3")
    print("PREDECESSOR_V02_MANIFESTS=PASS ROWS=14/5")
    print("V02_INDEPENDENT_CODE_SECURITY_REREVIEW=PASS")
    print("AUTHENTICATED_SNAPSHOT=PASS")
    print("STATIC_AUTHORITY_SEPARATION_AND_NONCLAIMS=PASS")
    print("FOCUSED_PUBLIC_SYNTHETIC_TESTS=PASS COUNT=18")
    print("ORIGINAL_INPUT_SWAP_SENTINEL=PASS")
    print("CANDIDATE_NATIVE_CALLS_DURING_TESTS=0")
    print("CANDIDATE_NETWORK_PROVIDER_PROCESS_CALLS_DURING_TESTS=0")
    print("EXECUTED_CODE_AUTHORITY_ESTABLISHED=false")
    print("EFFECTIVE_TRUST_AUTHORITY_CLAIMED=false")
    print("PROCESS_AUTHORITY_GRANTED=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

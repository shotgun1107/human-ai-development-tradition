"""Authenticated-snapshot verifier for the PUBLIC Authenticode candidate."""

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
BASE = "s0-lab/assembly-rehearsal/windows-authenticode-verifier-v0.1"
IMPLEMENTATION_MANIFEST = f"{BASE}/verification/implementation-files.sha256"
VERIFICATION_MANIFEST = f"{BASE}/verification/verification-files.sha256"
TEST_PATH = f"{BASE}/tests/test_authenticode_verifier.py"
VERIFICATION_TARGETS = (
    f"{BASE}/README.md",
    TEST_PATH,
    f"{BASE}/verification/public-windows-authenticode-verifier-implementation-candidate-report-v0.1.md",
    f"{BASE}/verification/verify_candidate.py",
)
SUBMANIFESTS = {
    f"{BASE}/verification/policy-contract-files.sha256": 1,
    f"{BASE}/verification/native-verifier-files.sha256": 1,
    f"{BASE}/verification/semantic-validator-files.sha256": 3,
    f"{BASE}/verification/runtime-orchestrator-files.sha256": 3,
}
PREDECESSOR_MANIFESTS = {
    "s0-lab/control/assembly-rehearsal/build-runtime-materialization-windows-authenticode-trust-profile-v0.2/trust-profile-package-files.sha256": (
        "315f89b1b13151ab9abe2aaff7ae64d23afa959ace8bd37f52ec4e872cc807c0",
        8,
    ),
    "s0-lab/control/assembly-rehearsal/build-runtime-materialization-external-pin-recovery-v0.2/recovery-package-files.sha256": (
        "1994a35319047cbca7418bb68293bab174642d7ce06484f24a0a234577f06b83",
        4,
    ),
}
AUXILIARY_PINS = {
    "s0-lab/reviews/assembly-rehearsal/build-runtime-materialization-windows-authenticode-trust-profile-v0.2/public-windows-authenticode-trust-profile-v0.2-independent-review-v0.1.md": "f3e738c3d1bee80014b033e16681cadfdb1847087aa84ac855ee089bc26c7a45",
    "s0-lab/reviews/assembly-rehearsal/build-runtime-materialization-external-pin-recovery-v0.2/public-build-runtime-external-pin-recovery-v0.2-independent-review-result-preservation-record-v0.1.md": "3cb76b0d2da2e303efb6f1a8353946180ca3c5d962ba9983747cfa67ad064f80",
}
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
    expected_sha256: str | None,
    expected_rows: int,
    expected_targets: tuple[str, ...] | None = None,
    require_sorted: bool = True,
) -> tuple[str, ...]:
    raw = (WORKSPACE / logical_path).read_bytes()
    if expected_sha256 is not None and hashlib.sha256(raw).hexdigest() != expected_sha256:
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
    if require_sorted and paths != sorted(paths):
        raise ValueError("manifest target order differs")
    if expected_targets is not None and tuple(paths) != expected_targets:
        raise ValueError("manifest exact target set differs")
    _add(snapshot, logical_path, raw)
    return tuple(paths)


def _sidecar(snapshot: dict[str, bytes], markdown_path: str, expected_sha256: str) -> None:
    raw = (WORKSPACE / markdown_path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected_sha256:
        raise ValueError("auxiliary Markdown pin differs")
    sidecar_path = markdown_path.rsplit(".", 1)[0] + ".sha256"
    sidecar = (WORKSPACE / sidecar_path).read_bytes()
    expected = f"{expected_sha256}  {Path(markdown_path).name}\n".encode("ascii")
    if sidecar != expected:
        raise ValueError("auxiliary Markdown sidecar differs")
    _add(snapshot, markdown_path, raw)
    _add(snapshot, sidecar_path, sidecar)


def _static_source_checks(snapshot: dict[str, bytes]) -> None:
    semantic_path = f"{BASE}/implementation/s0_windows_authenticode_verifier/semantic.py"
    win32_path = f"{BASE}/implementation/s0_windows_authenticode_verifier/win32.py"
    verifier_path = f"{BASE}/implementation/s0_windows_authenticode_verifier/verifier.py"
    semantic = ast.parse(snapshot[semantic_path].decode("utf-8", "strict"))
    forbidden_semantic_imports = {"ctypes", "os", "socket", "subprocess", "urllib", "requests"}
    for node in ast.walk(semantic):
        if isinstance(node, ast.Import):
            names = {alias.name.split(".", 1)[0] for alias in node.names}
            if names & forbidden_semantic_imports:
                raise ValueError("semantic validator imports live authority")
        if isinstance(node, ast.ImportFrom) and node.module:
            if node.module.split(".", 1)[0] in forbidden_semantic_imports:
                raise ValueError("semantic validator imports live authority")
    win32_text = snapshot[win32_path].decode("utf-8", "strict")
    for forbidden in ("subprocess", "socket", "requests", "urllib", "os.system", "Popen"):
        if forbidden in win32_text:
            raise ValueError("native collector contains an unapproved execution or network helper")
    verifier_text = snapshot[verifier_path].decode("utf-8", "strict")
    if "authenticate_installed_implementation" not in verifier_text:
        raise ValueError("runtime entry does not authenticate installed bytes")


def authenticate_all(implementation_pin: str, verification_pin: str) -> dict[str, bytes]:
    snapshot: dict[str, bytes] = {}
    implementation_targets = _manifest(snapshot, IMPLEMENTATION_MANIFEST, implementation_pin, 12)
    _manifest(snapshot, VERIFICATION_MANIFEST, verification_pin, 4, VERIFICATION_TARGETS)
    for path, rows in SUBMANIFESTS.items():
        subtargets = _manifest(snapshot, path, None, rows)
        if not set(subtargets).issubset(set(implementation_targets)):
            raise ValueError("submanifest target is outside implementation closure")
    for path, (pin, rows) in PREDECESSOR_MANIFESTS.items():
        _manifest(snapshot, path, pin, rows, require_sorted=False)
    for path, pin in AUXILIARY_PINS.items():
        _sidecar(snapshot, path, pin)
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
    if _PIN.fullmatch(args.implementation_manifest_sha256) is None or _PIN.fullmatch(args.verification_manifest_sha256) is None:
        print("MANIFEST_PIN_GRAMMAR=FAIL")
        return 1
    try:
        before = authenticate_all(args.implementation_manifest_sha256, args.verification_manifest_sha256)
        with tempfile.TemporaryDirectory(prefix="s0-authenticode-v01-snapshot-") as temporary:
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
        after = authenticate_all(args.implementation_manifest_sha256, args.verification_manifest_sha256)
    except (OSError, UnicodeError, ValueError, SyntaxError):
        print("AUTHENTICATED_SNAPSHOT=FAIL")
        return 1
    if completed.returncode != 0:
        print("FOCUSED_TESTS=FAIL")
        return 1
    if before != after:
        print("ORIGINAL_INPUT_SWAP_SENTINEL=FAIL")
        return 1
    print("OUTER_IMPLEMENTATION_MANIFEST=PASS ROWS=12")
    print("POLICY_NATIVE_SEMANTIC_ORCHESTRATOR_SUBMANIFESTS=PASS ROWS=1/1/3/3")
    print("PREDECESSOR_PROFILE_AND_RECOVERY_MANIFESTS=PASS ROWS=8/4")
    print("V02_PROFILE_AND_RECOVERY_REVIEWS=PASS")
    print("AUTHENTICATED_SNAPSHOT=PASS")
    print("STATIC_AUTHORITY_SEPARATION=PASS")
    print("FOCUSED_PUBLIC_SYNTHETIC_TESTS=PASS")
    print("ORIGINAL_INPUT_SWAP_SENTINEL=PASS")
    print("CANDIDATE_NATIVE_CALLS_DURING_TESTS=0")
    print("CANDIDATE_NETWORK_PROVIDER_PROCESS_CALLS_DURING_TESTS=0")
    print("REAL_EXECUTABLE_SIGNATURE_RESULT=NOT-CLAIMED")
    print("PROCESS_AUTHORITY_GRANTED=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

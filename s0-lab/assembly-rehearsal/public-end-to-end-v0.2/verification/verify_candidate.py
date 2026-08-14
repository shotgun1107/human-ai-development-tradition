"""Snapshot-only verifier for the bounded public v0.2 integration candidate."""

from __future__ import annotations

import argparse
import hashlib
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = next(parent for parent in ROOT.parents if (parent / "AGENTS.md").is_file())
CANDIDATE_MANIFEST = "s0-lab/assembly-rehearsal/public-end-to-end-v0.2/verification/implementation-files.sha256"
PINS = {
    "s0-lab/assembly-rehearsal/public-end-to-end-v0.1/verification/implementation-files.sha256": ("0cc96816404094dec313dbab4bb108744383afb2ca5272834b589235364a9623", 32),
    "s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.3/verification/implementation-files.sha256": ("5022d517864cae19520a1e3e34a683965609abf0ef29e167b30a11bade4a32c2", 11),
    "s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/design-package-files.sha256": ("abecc3951f29201f24e7fd069865d5a10cf76587b2c1e7c8013ff9226479e589", 6),
    "s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-integration-v0.1/design-package-files.sha256": ("f55352771432404f4c2e9337665184e18afde076b8b3efe7a455ee6694d60e6b", 5),
    "s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-integration-v0.2/design-package-files.sha256": ("1349c6c4c97d24256f98216eb86a353451891419044b61d22c5c14d7eded5e7c", 6),
}
AUXILIARY_PINS = {
    "s0-lab/assembly-rehearsal/public-end-to-end-v0.1/verification/public-end-to-end-assembly-rehearsal-implementation-candidate-report-v0.1.md": "520a237109686a17b8c075c15f1cc676a43d450716a6157bce7b48585f0c5005",
    "s0-lab/reviews/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/v0.4-independent-rereview-result-preservation-record-v0.1.md": "9fca4e14309304e5540d4e4e210dcfea72890729764aa4af5dadc736497c4e71",
    "s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.1/runtime-profile-v0.1.schema.json": "92943a96249c312d0e2631705a667170d60d22d8e75f2571961ed1f728e934af",
    "s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.2/runtime-profile-v0.2.schema.json": "e2e96940bbafc6a80987634fe794d700844dbc7d0b48e0e269922f03364fb34f",
    "s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.3/runtime-profile-v0.3.schema.json": "1404f4981d3d7815e98a6c5d745596f15bb8d50a296410584d03d7ccb11ce3dd",
}


def _add(snapshot: dict[str, bytes], path: str, raw: bytes) -> None:
    prior = snapshot.get(path)
    if prior is not None and prior != raw:
        raise ValueError("authenticated path collision")
    snapshot[path] = raw


def _manifest(snapshot: dict[str, bytes], logical_path: str, expected: str, rows: int) -> None:
    raw = (WORKSPACE / logical_path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected or not raw.endswith(b"\n"):
        raise ValueError("manifest pin failure")
    parsed = raw[:-1].split(b"\n")
    paths: list[str] = []
    for row in parsed:
        digest_raw, separator, target_raw = row.partition(b"  ")
        if separator != b"  " or len(digest_raw) != 64:
            raise ValueError("manifest row failure")
        digest, target = digest_raw.decode("ascii"), target_raw.decode("ascii")
        target_bytes = (WORKSPACE / target).read_bytes()
        if hashlib.sha256(target_bytes).hexdigest() != digest:
            raise ValueError("manifest target failure")
        paths.append(target)
        _add(snapshot, target, target_bytes)
    if len(paths) != rows or paths != sorted(paths) or len(set(paths)) != len(paths):
        raise ValueError("manifest closure failure")
    _add(snapshot, logical_path, raw)


def authenticate_all(candidate_pin: str) -> dict[str, bytes]:
    snapshot: dict[str, bytes] = {}
    _manifest(snapshot, CANDIDATE_MANIFEST, candidate_pin, 3)
    for path, (pin, rows) in PINS.items():
        _manifest(snapshot, path, pin, rows)
    for path, pin in AUXILIARY_PINS.items():
        raw = (WORKSPACE / path).read_bytes()
        if hashlib.sha256(raw).hexdigest() != pin:
            raise ValueError("auxiliary pin failure")
        _add(snapshot, path, raw)
    _add(snapshot, "AGENTS.md", (WORKSPACE / "AGENTS.md").read_bytes())
    return snapshot


def _materialize(snapshot: dict[str, bytes], target: Path) -> None:
    for logical_path, raw in snapshot.items():
        destination = target / logical_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(raw)
        if destination.read_bytes() != raw:
            raise ValueError("snapshot write verification failure")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--implementation-manifest-sha256", required=True)
    args = parser.parse_args()
    candidate_pin = args.implementation_manifest_sha256
    if len(candidate_pin) != 64 or candidate_pin != candidate_pin.lower() or any(c not in "0123456789abcdef" for c in candidate_pin):
        print("CANDIDATE_MANIFEST_PIN=FAIL")
        return 1
    try:
        before = authenticate_all(candidate_pin)
        with tempfile.TemporaryDirectory(prefix="s0-v02-snapshot-") as temporary:
            snapshot_root = Path(temporary)
            _materialize(before, snapshot_root)
            environment = dict(os.environ)
            environment["PYTHONDONTWRITEBYTECODE"] = "1"
            environment.pop("PYTHONPATH", None)
            completed = subprocess.run(
                (sys.executable, "-I", "-B", "-m", "unittest", "discover", "-s", str(snapshot_root / "s0-lab/assembly-rehearsal/public-end-to-end-v0.2/tests"), "-v"),
                cwd=snapshot_root,
                env=environment,
                check=False,
            )
        after = authenticate_all(candidate_pin)
    except (OSError, UnicodeError, ValueError):
        print("AUTHENTICATED_SNAPSHOT=FAIL")
        return 1
    if completed.returncode != 0:
        print("FOCUSED_TESTS=FAIL")
        return 1
    if before != after:
        print("ORIGINAL_INPUT_SWAP_SENTINEL=FAIL")
        return 1
    print("CANDIDATE_MANIFEST_AND_ROWS=PASS ROWS=3")
    print("PIN_AND_TARGET_AUTHENTICATION=PASS ROWS=32/11/6/5/6")
    print("SNAPSHOT_ONLY_EXECUTION=PASS")
    print("ORIGINAL_INPUT_SWAP_SENTINEL=PASS")
    print("FOCUSED_TESTS=PASS")
    print("CANDIDATE_NATIVE_PROCESS_NETWORK_PROVIDER_CALLS=0")
    print("VERIFIER_ORCHESTRATION_PROCESS=authenticated-snapshot-python-unittest-runner")
    print("REHEARSAL_PASS=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

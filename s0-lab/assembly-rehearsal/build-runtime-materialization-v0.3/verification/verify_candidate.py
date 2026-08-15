"""Authenticated-snapshot verifier for the non-executing PUBLIC candidate."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = next(parent for parent in ROOT.parents if (parent / "AGENTS.md").is_file())
CANDIDATE_MANIFEST = (
    "s0-lab/assembly-rehearsal/build-runtime-materialization-v0.3/verification/implementation-files.sha256"
)
DESIGN_MANIFESTS = {
    "s0-lab/control/assembly-rehearsal/build-runtime-materialization-v0.1/design-package-files.sha256": (
        "bdf3cd280c65adcb4a1a4c965a3e2512e460eb2c03f498274bddfe5879ba5e1c",
        6,
    ),
    "s0-lab/control/assembly-rehearsal/build-runtime-materialization-v0.2/design-package-files.sha256": (
        "47b956ca352f0e8ac969cdd36b801234c1436cefe50308c1e4d7c2b4e9bf1304",
        7,
    ),
    "s0-lab/control/assembly-rehearsal/build-runtime-materialization-v0.3/design-package-files.sha256": (
        "1d3ddfa20c6e0413b7d0420c17e35e3c2251bba77ee6421cc40d92b40e9c5277",
        9,
    ),
    "s0-lab/control/assembly-rehearsal/build-runtime-materialization-v0.4/design-package-files.sha256": (
        "7af9c640f90f4cf42b85b77bb4851af6f33b71890b64355b62e449d58e528884",
        9,
    ),
    "s0-lab/control/assembly-rehearsal/build-runtime-materialization-v0.5/design-package-files.sha256": (
        "ca52a47378c9cbd46eae5d94fec8466562c40d702dfdc8d2e1f63c61e4b3f98c",
        7,
    ),
}
AUXILIARY_PINS = {
    "s0-lab/reviews/assembly-rehearsal/build-runtime-materialization-v0.5/public-assembly-build-runtime-materialization-design-v0.5-independent-review-v0.1.md": "5353431dfa8bc36b7d86c0ece1eabf88bad0cb598f1a8f73092cdebf2c95e2f9",
    "s0-lab/control/assembly-rehearsal/build-runtime-materialization-v0.5-control-integration/control-integration-decision-v0.1.md": "d4fc2bc7ea6a6f606efd9395be230e8aec408cf07a48c246825409cfac7f3eaf",
    "s0-lab/reviews/assembly-rehearsal/build-runtime-materialization-implementation-v0.1/public-build-runtime-materialization-implementation-v0.1-independent-review-v0.1.md": "fc4c9d979fd8643d10e7f50cb8adff66b3844495808c1ea85bc77dbecfd7143b",
    "s0-lab/reviews/assembly-rehearsal/build-runtime-materialization-implementation-v0.2/public-build-runtime-materialization-implementation-v0.2-independent-review-v0.1.md": "321f8a29edabbd2592e60cac3c58c46af3cba35e157956cf710b92615df9af59",
}
_ROW = re.compile(rb"^([0-9a-f]{64})  ([A-Za-z0-9._/-]+)$")
_PIN = re.compile(r"^[0-9a-f]{64}$")


def _add(snapshot: dict[str, bytes], logical_path: str, raw: bytes) -> None:
    if type(logical_path) is not str or type(raw) is not bytes:
        raise ValueError("snapshot entry type differs")
    prior = snapshot.get(logical_path)
    if prior is not None and prior != raw:
        raise ValueError("authenticated path collision")
    snapshot[logical_path] = raw


def _manifest(
    snapshot: dict[str, bytes], logical_path: str, expected_sha256: str, expected_rows: int
) -> None:
    raw = (WORKSPACE / logical_path).read_bytes()
    if hashlib.sha256(raw).hexdigest() != expected_sha256 or not raw.endswith(b"\n") or b"\r" in raw:
        raise ValueError("manifest pin or byte grammar differs")
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
    _add(snapshot, logical_path, raw)


def authenticate_all(candidate_pin: str) -> dict[str, bytes]:
    snapshot: dict[str, bytes] = {}
    _manifest(snapshot, CANDIDATE_MANIFEST, candidate_pin, 10)
    for path, (pin, rows) in DESIGN_MANIFESTS.items():
        _manifest(snapshot, path, pin, rows)
    for path, pin in AUXILIARY_PINS.items():
        raw = (WORKSPACE / path).read_bytes()
        if hashlib.sha256(raw).hexdigest() != pin:
            raise ValueError("auxiliary public pin differs")
        _add(snapshot, path, raw)
    _add(snapshot, "AGENTS.md", (WORKSPACE / "AGENTS.md").read_bytes())
    return snapshot


def _materialize(snapshot: dict[str, bytes], root: Path) -> None:
    for logical_path, raw in snapshot.items():
        destination = root / logical_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(raw)
        if destination.read_bytes() != raw:
            raise ValueError("snapshot write verification failed")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--implementation-manifest-sha256", required=True)
    arguments = parser.parse_args()
    candidate_pin = arguments.implementation_manifest_sha256
    if _PIN.fullmatch(candidate_pin) is None:
        print("CANDIDATE_MANIFEST_PIN=FAIL")
        return 1
    try:
        before = authenticate_all(candidate_pin)
        with tempfile.TemporaryDirectory(prefix="s0-brm-v03-snapshot-") as temporary:
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
                    str(
                        snapshot_root
                        / "s0-lab/assembly-rehearsal/build-runtime-materialization-v0.3/tests"
                    ),
                    "-v",
                ),
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
    print("CANDIDATE_MANIFEST_AND_ROWS=PASS ROWS=10")
    print("DESIGN_MANIFEST_AND_TARGET_AUTHENTICATION=PASS ROWS=6/7/9/9/7")
    print("APPROVING_REVIEW_CONTROL_DECISION_AND_V01_V02_IMPLEMENTATION_REVIEWS=PASS")
    print("JSONSCHEMA_DEPENDENCY_STATUS=BLOCKED-MISSING-EXTERNAL-PIN")
    print("SNAPSHOT_ONLY_TEST_EXECUTION=PASS")
    print("ORIGINAL_INPUT_SWAP_SENTINEL=PASS")
    print("FOCUSED_TESTS=PASS")
    print("CANDIDATE_FILESYSTEM_PROCESS_NATIVE_NETWORK_PROVIDER_CALLS=0")
    print("VERIFIER_ORCHESTRATION_PROCESS=authenticated-snapshot-python-unittest-runner")
    print("EXTERNAL_PIN_STATUS=BLOCKED-MISSING-EXTERNAL-PIN")
    print("BUILD_EXECUTION_AUTHORIZED=false")
    print("RUNTIME_MATERIALIZED=false")
    print("REHEARSAL_PASS=false")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

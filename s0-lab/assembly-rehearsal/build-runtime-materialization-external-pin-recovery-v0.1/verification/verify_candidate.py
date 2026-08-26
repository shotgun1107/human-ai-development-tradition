"""Run the frozen external-pin recovery tests from an authenticated snapshot."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Final


_SCHEMA: Final = "s0-public-external-pin-recovery-verification-v1"
_CANDIDATE_ROOT: Final = Path(__file__).resolve().parents[1]
_PACKAGE_RELATIVE: Final = Path("implementation/s0_public_external_pin_recovery")
_TEST_RELATIVE: Final = Path("tests/test_external_pin_recovery.py")
_EXPECTED_SHA256: Final = {
    "implementation/s0_public_external_pin_recovery/__init__.py": (
        "1919191fa86c033a960a212fda17bb50858eaf5a1e553bbe55f7fe35f35701f1"
    ),
    "implementation/s0_public_external_pin_recovery/errors.py": (
        "7757b2657e3d077c381a453ffe4dc884bc437b19b492b90c1560003fdf2c04ae"
    ),
    "implementation/s0_public_external_pin_recovery/pins.py": (
        "19c414fb275d8892783e25aa63f32e1653995c8387781f897ec7621fd0301888"
    ),
    "implementation/s0_public_external_pin_recovery/canonical.py": (
        "c57253e58a7e277fd9f2e88a72b10ab079bf271e42ebe9d924789b3618b13bed"
    ),
    "implementation/s0_public_external_pin_recovery/acquisition.py": (
        "d4f5671acac2e82e8d1595b62963dc80a233816fdb1e7c1b6d09ba8361fb1c93"
    ),
    "implementation/s0_public_external_pin_recovery/materialize.py": (
        "9f205aaa19e14e3e92e39cfa5068eb56661582b86289179d47405ebcc5d21df0"
    ),
    "implementation/s0_public_external_pin_recovery/candidate.py": (
        "b97313b6d83557cd86ee0c2dc7a2682dabe7531ada7814fbfd9eac73adcb45ed"
    ),
}
_COUNT_LABELS: Final = {
    "failures": "failures",
    "errors": "errors",
    "skipped": "skipped",
    "expected failures": "expected_failures",
    "unexpected successes": "unexpected_successes",
}


class VerificationError(Exception):
    """A deterministic fail-closed verifier error."""

    def __init__(self, code: str, details: dict[str, object] | None = None) -> None:
        super().__init__(code)
        self.code = code
        self.details = details or {}


def _portable(path: Path) -> str:
    return path.as_posix()


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _read_required_input(relative: Path, *, test_input: bool = False) -> bytes:
    source = _CANDIDATE_ROOT / relative
    if not source.is_file():
        code = "required_test_missing" if test_input else "candidate_input_missing"
        raise VerificationError(code, {"input": _portable(relative)})
    try:
        return source.read_bytes()
    except OSError as exc:
        code = "required_test_unreadable" if test_input else "candidate_input_unreadable"
        raise VerificationError(code, {"input": _portable(relative)}) from exc


def _copy_exclusively(target: Path, relative: Path, data: bytes) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        with target.open("xb") as output:
            output.write(data)
    except OSError as exc:
        raise VerificationError(
            "snapshot_copy_failed", {"input": _portable(relative)}
        ) from exc


def _rehash_exact(root: Path, relative_paths: tuple[Path, ...]) -> dict[str, str | None]:
    hashes: dict[str, str | None] = {}
    for relative in relative_paths:
        try:
            hashes[_portable(relative)] = _sha256((root / relative).read_bytes())
        except OSError:
            hashes[_portable(relative)] = None
    return hashes


def _parse_unittest_counts(output: str) -> dict[str, int]:
    lines = tuple(line.strip() for line in output.splitlines())
    ran_matches = [
        match
        for line in lines
        if (match := re.fullmatch(r"Ran (\d+) tests? in .+", line)) is not None
    ]
    status_matches = [
        match
        for line in lines
        if (
            match := re.fullmatch(r"(OK|FAILED)(?: \(([^)]*)\))?", line)
        )
        is not None
    ]
    if not ran_matches or not status_matches:
        raise VerificationError("unittest_summary_unparseable")

    run_count = int(ran_matches[-1].group(1))
    status_match = status_matches[-1]
    counts = {
        "run": run_count,
        "passed": 0,
        "failures": 0,
        "errors": 0,
        "skipped": 0,
        "expected_failures": 0,
        "unexpected_successes": 0,
    }
    detail = status_match.group(2)
    if detail:
        for item in detail.split(", "):
            label, separator, value = item.rpartition("=")
            mapped = _COUNT_LABELS.get(label)
            if not separator or mapped is None or not value.isdigit():
                raise VerificationError("unittest_summary_unparseable")
            counts[mapped] = int(value)

    nonpassing = sum(
        counts[key]
        for key in (
            "failures",
            "errors",
            "skipped",
            "expected_failures",
            "unexpected_successes",
        )
    )
    counts["passed"] = run_count - nonpassing
    if counts["passed"] < 0:
        raise VerificationError("unittest_summary_inconsistent")
    return counts


def _run() -> tuple[dict[str, object], int]:
    implementation_paths = tuple(Path(relative) for relative in _EXPECTED_SHA256)
    all_paths = (*implementation_paths, _TEST_RELATIVE)
    authenticated_bytes: dict[Path, bytes] = {}

    for relative in implementation_paths:
        data = _read_required_input(relative)
        actual = _sha256(data)
        expected = _EXPECTED_SHA256[_portable(relative)]
        if actual != expected:
            raise VerificationError(
                "candidate_hash_mismatch",
                {
                    "actual": actual,
                    "expected": expected,
                    "input": _portable(relative),
                },
            )
        authenticated_bytes[relative] = data

    test_bytes = _read_required_input(_TEST_RELATIVE, test_input=True)
    authenticated_bytes[_TEST_RELATIVE] = test_bytes
    original_pre = {
        _portable(relative): _sha256(authenticated_bytes[relative])
        for relative in all_paths
    }

    with tempfile.TemporaryDirectory(prefix="s0-external-pin-recovery-") as temporary:
        snapshot_root = Path(temporary)
        for relative in all_paths:
            _copy_exclusively(
                snapshot_root / relative, relative, authenticated_bytes[relative]
            )

        snapshot_pre = _rehash_exact(snapshot_root, all_paths)
        if snapshot_pre != original_pre:
            raise VerificationError("snapshot_copy_hash_mismatch")

        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        command = (
            sys.executable,
            "-I",
            "-B",
            "-m",
            "unittest",
            "discover",
            "-s",
            str(snapshot_root / "tests"),
            "-v",
        )
        try:
            completed = subprocess.run(
                command,
                cwd=snapshot_root,
                env=environment,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
        except OSError as exc:
            raise VerificationError("isolated_child_start_failed") from exc

        stdout = completed.stdout.decode("utf-8", errors="replace")
        stderr = completed.stderr.decode("utf-8", errors="replace")
        counts = _parse_unittest_counts("\n".join((stdout, stderr)))
        snapshot_post = _rehash_exact(snapshot_root, all_paths)
        original_post = _rehash_exact(_CANDIDATE_ROOT, all_paths)

    original_mismatches = sorted(
        relative
        for relative in original_pre
        if original_post.get(relative) != original_pre[relative]
    )
    snapshot_mismatches = sorted(
        relative
        for relative in snapshot_pre
        if snapshot_post.get(relative) != snapshot_pre[relative]
    )
    original_stable = not original_mismatches
    snapshot_stable = not snapshot_mismatches
    passed = (
        completed.returncode == 0
        and counts["run"] > 0
        and counts["failures"] == 0
        and counts["errors"] == 0
        and counts["unexpected_successes"] == 0
        and original_stable
        and snapshot_stable
    )
    verifier_exit = 0 if passed else 1
    result: dict[str, object] = {
        "child": {
            "counts": counts,
            "exit_code": completed.returncode,
            "isolated": True,
            "python_dont_write_bytecode": True,
        },
        "exit_codes": {"child": completed.returncode, "verifier": verifier_exit},
        "expected_candidate_sha256": dict(_EXPECTED_SHA256),
        "original_inputs": {
            "post_run_sha256": original_post,
            "pre_run_sha256": original_pre,
            "swap_sentinel": {
                "mismatches": original_mismatches,
                "passed": original_stable,
            },
        },
        "schema": _SCHEMA,
        "snapshot": {
            "mutation_sentinel": {
                "mismatches": snapshot_mismatches,
                "passed": snapshot_stable,
            },
            "post_run_sha256": snapshot_post,
            "pre_run_sha256": snapshot_pre,
        },
        "status": "passed" if passed else "failed",
    }
    return result, verifier_exit


def _emit(document: dict[str, object]) -> None:
    sys.stdout.write(json.dumps(document, ensure_ascii=True, sort_keys=True, separators=(",", ":")))
    sys.stdout.write("\n")


def main() -> int:
    try:
        document, exit_code = _run()
    except VerificationError as exc:
        document = {
            "details": exc.details,
            "error": exc.code,
            "exit_codes": {"verifier": 2},
            "schema": _SCHEMA,
            "status": "error",
        }
        exit_code = 2
    _emit(document)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())

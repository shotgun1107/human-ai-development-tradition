"""Run the explicitly user-authorized live plus suite verification for correction cycle 3."""

from __future__ import annotations

import hashlib
import io
import json
import os
import platform
import subprocess
import sys
import time
import unittest
from pathlib import Path


REPOSITORY = Path(r"C:\Users\SSAFY\AppData\Local\Temp\cpr01-862b27cd").resolve(strict=True)
RAW_ROOT = Path(r"C:\Users\SSAFY\AppData\Local\Temp\brm07-6a21dc13\test-verification-r3")
CACHE_ROOT = Path(r"C:\Users\SSAFY\AppData\Local\Temp\brm07-6a21dc13\cache")
FINAL_ROOT = Path(r"C:\Users\SSAFY\AppData\Local\Temp\brm07-6a21dc13\runtime-final-r3")
CANDIDATE = REPOSITORY / "s0-lab/assembly-rehearsal/build-runtime-materialization-v0.7"
IMPLEMENTATION = CANDIDATE / "implementation/s0_public_build_runtime"
EXPECTED_IMPLEMENTATION = {
    "__init__.py": "12ca47b823c8c8cbe1b8f2bb2de912a1695d3bb2550ea7c90947379e88e7b011",
    "__main__.py": "097f9fe6ecccda122f33f26e23ed8de5a5ac26c53d9a2b8bbb218731c3ab69f8",
    "authority.py": "e20b44e726108e711dc4769509dc380acbd0cabd129237054bb20412624d5fef",
    "canonical.py": "17f02071c3514f5c99aae5c96d3d13d4b76d6a312a379bcfd7a06065ecf5fec5",
    "cli.py": "33bc72d474efe81dbb7c320ce54fd47dba1a0dfbf8e3ba6bb7131d63b70016da",
    "errors.py": "5e1235e362756224e6c494271a1d8532e2708767c29e01b462ddffe370600850",
    "materialize.py": "e5c41512658028780e0d479ad170e0f4d3dc9f7453ed71534c28b11e087fbbbe",
    "publication.py": "0184575017506860f39f1ac54b502ea239788ec7476e90350bb710fe3ea1700e",
}


def hash_file(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def write_pair(filename: str, value: object) -> str:
    raw = json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8") + b"\n"
    value_hash = hashlib.sha256(raw).hexdigest()
    (RAW_ROOT / filename).write_bytes(raw)
    (RAW_ROOT / f"{filename}.sha256").write_bytes(f"{value_hash}  {filename}\n".encode("ascii"))
    return value_hash


def git_value(*arguments: str) -> str:
    result = subprocess.run(["git", *arguments], cwd=REPOSITORY, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30, check=True)
    return result.stdout.decode("ascii", "strict").strip()


def main() -> int:
    if RAW_ROOT.exists() or FINAL_ROOT.exists():
        raise SystemExit("cycle-3 raw and final roots must initially be absent")
    RAW_ROOT.mkdir(parents=True)
    observed = {name: hash_file(IMPLEMENTATION / name) for name in EXPECTED_IMPLEMENTATION}
    if observed != EXPECTED_IMPLEMENTATION:
        raise SystemExit("implementation authentication failed before import")
    cache = CACHE_ROOT.resolve(strict=True)
    environment = os.environ.copy()
    environment.update({"PYTHONPATH": str(IMPLEMENTATION.parent), "PYTHONDONTWRITEBYTECODE": "1"})
    live_command = [sys.executable, "-B", "-m", "s0_public_build_runtime", "--repository-root", str(REPOSITORY), "--cache-root", str(cache), "--final-root", str(FINAL_ROOT)]
    live_started = time.monotonic()
    live = subprocess.run(live_command, cwd=REPOSITORY, env=environment, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60, check=False)
    live_elapsed = int((time.monotonic() - live_started) * 1000)
    live_stdout = live.stdout.decode("utf-8", "strict")
    live_stderr = live.stderr.decode("utf-8", "strict")
    live_value = json.loads(live_stdout) if live.returncode == 0 else None
    if live.returncode != 0 or not FINAL_ROOT.is_dir():
        record = {"authenticated_implementation": observed, "live": {"command": live_command, "elapsed_milliseconds": live_elapsed, "exit_code": live.returncode, "stderr": live_stderr, "stdout": live_stdout}, "schema_id": "S0-PUBLIC-BRM-V0.7-TEST-VERIFICATION-RERUN-CYCLE-3-RAW-1", "status": "FAIL-LIVE-BEFORE-SUITE"}
        result_hash = write_pair("rerun-cycle-3-result.json", record)
        print(json.dumps({"live_exit_code": live.returncode, "result_sha256": result_hash, "status": record["status"]}, separators=(",", ":"), sort_keys=True))
        return 1

    sys.path[:0] = [str(IMPLEMENTATION.parent), str(CANDIDATE)]
    os.environ.update({"BRM07_REPOSITORY_ROOT": str(REPOSITORY), "BRM07_TEST_RAW_ROOT": str(RAW_ROOT.resolve(strict=True)), "BRM07_CACHE_ROOT": str(cache), "BRM07_FINAL_ROOT": str(FINAL_ROOT.resolve(strict=True)), "PYTHONDONTWRITEBYTECODE": "1"})
    from tests import test_v07

    stream = io.StringIO()
    suite_started = time.monotonic()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(test_v07))
    suite_elapsed = int((time.monotonic() - suite_started) * 1000)
    audit = None
    audit_error = None
    try:
        audit = test_v07.audit_live_runtime()
    except Exception as error:
        audit_error = {"message": str(error), "type": type(error).__name__}
    passed = result.testsRun - len(result.failures) - len(result.errors) - len(result.skipped)
    status = "PASS" if result.wasSuccessful() and audit_error is None else "FAIL"
    record = {
        "audit": audit, "audit_error": audit_error, "authenticated_implementation": observed,
        "branch": git_value("branch", "--show-current"), "commit": git_value("rev-parse", "HEAD"),
        "live": {"command": live_command, "elapsed_milliseconds": live_elapsed, "exit_code": live.returncode, "parsed_stdout": live_value, "stderr": live_stderr, "stdout": live_stdout},
        "platform": platform.platform(), "python": sys.version,
        "schema_id": "S0-PUBLIC-BRM-V0.7-TEST-VERIFICATION-RERUN-CYCLE-3-RAW-1", "status": status,
        "suite": {"command": [sys.executable, "-B", str(Path(__file__).resolve())], "elapsed_milliseconds": suite_elapsed,
            "errors": [{"test": str(test), "traceback": trace} for test, trace in result.errors],
            "failures": [{"test": str(test), "traceback": trace} for test, trace in result.failures],
            "passed": passed, "skipped": [{"test": str(test), "reason": reason} for test, reason in result.skipped],
            "stderr": "", "stdout": stream.getvalue(), "test_source_sha256": hash_file(CANDIDATE / "tests/test_v07.py"), "tests_run": result.testsRun},
        "tree": git_value("rev-parse", "HEAD^{tree}"),
    }
    result_hash = write_pair("rerun-cycle-3-result.json", record)
    print(json.dumps({"audit": audit_error is None, "errors": len(result.errors), "failures": len(result.failures), "live_exit_code": live.returncode, "passed": passed, "result_sha256": result_hash, "skipped": len(result.skipped), "status": status, "tests_run": result.testsRun}, separators=(",", ":"), sort_keys=True))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

"""Run v0.7 TEST verification and preserve bounded raw evidence outside Git."""

from __future__ import annotations

import argparse
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


def jcs(value: object) -> bytes:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8") + b"\n"


def write_pair(root: Path, filename: str, value: object) -> str:
    raw = jcs(value)
    value_hash = hashlib.sha256(raw).hexdigest()
    (root / filename).write_bytes(raw)
    (root / f"{filename}.sha256").write_bytes(f"{value_hash}  {filename}\n".encode("ascii"))
    return value_hash


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repository-root", required=True)
    parser.add_argument("--raw-root", required=True)
    parser.add_argument("--cache-root", required=True)
    parser.add_argument("--final-root", required=True)
    arguments = parser.parse_args()
    repository = Path(arguments.repository_root).resolve(strict=True)
    raw = Path(arguments.raw_root).resolve(strict=True)
    raw.mkdir(parents=True, exist_ok=True)
    candidate = repository / "s0-lab/assembly-rehearsal/build-runtime-materialization-v0.7"
    implementation = candidate / "implementation"
    sys.path[:0] = [str(implementation), str(candidate)]
    os.environ.update({
        "BRM07_REPOSITORY_ROOT": str(repository),
        "BRM07_TEST_RAW_ROOT": str(raw),
        "BRM07_CACHE_ROOT": str(Path(arguments.cache_root).resolve(strict=True)),
        "BRM07_FINAL_ROOT": str(Path(arguments.final_root).resolve(strict=True)),
        "PYTHONDONTWRITEBYTECODE": "1",
    })
    from tests import test_v07

    started = time.monotonic()
    stream = io.StringIO()
    suite = unittest.defaultTestLoader.loadTestsFromModule(test_v07)
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    elapsed_ms = int((time.monotonic() - started) * 1000)
    audit = None
    audit_error = None
    try:
        audit = test_v07.audit_live_runtime()
    except Exception as error:
        audit_error = {"message": str(error), "type": type(error).__name__}
    status = "PASS" if result.wasSuccessful() and audit_error is None else "FAIL"
    record = {
        "audit": audit,
        "audit_error": audit_error,
        "command": [sys.executable, "-B", str(Path(__file__).resolve()), *sys.argv[1:]],
        "elapsed_milliseconds": elapsed_ms,
        "environment": {"platform": platform.platform(), "python": sys.version, "repository": str(repository)},
        "errors": [{"test": str(test), "traceback": trace} for test, trace in result.errors],
        "failures": [{"test": str(test), "traceback": trace} for test, trace in result.failures],
        "schema_id": "S0-PUBLIC-BRM-V0.7-TEST-VERIFICATION-RAW-1",
        "skipped": [{"test": str(test), "reason": reason} for test, reason in result.skipped],
        "status": status,
        "stderr": "",
        "stdout": stream.getvalue(),
        "tests_run": result.testsRun,
    }
    write_pair(raw, "verification-result.json", record)
    print(json.dumps({"elapsed_milliseconds": elapsed_ms, "errors": len(result.errors), "failures": len(result.failures), "skipped": len(result.skipped), "status": status, "tests_run": result.testsRun}, sort_keys=True, separators=(",", ":")))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

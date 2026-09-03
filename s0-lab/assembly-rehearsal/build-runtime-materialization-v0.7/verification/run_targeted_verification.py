"""Run only newly added diagnostics without repeating isolated candidate failures."""

from __future__ import annotations

import hashlib
import io
import json
import os
import sys
import time
import unittest
from pathlib import Path


REPOSITORY = Path(r"C:\Users\SSAFY\AppData\Local\Temp\cpr01-862b27cd").resolve(strict=True)
RAW_ROOT = Path(r"C:\Users\SSAFY\AppData\Local\Temp\brm07-6a21dc13\test-verification").resolve(strict=True)
CACHE_ROOT = Path(r"C:\Users\SSAFY\AppData\Local\Temp\brm07-6a21dc13\cache")
FINAL_ROOT = Path(r"C:\Users\SSAFY\AppData\Local\Temp\brm07-6a21dc13\runtime-final")
CANDIDATE = REPOSITORY / "s0-lab/assembly-rehearsal/build-runtime-materialization-v0.7"
sys.path[:0] = [str(CANDIDATE / "implementation"), str(CANDIDATE)]
os.environ.update(
    {
        "BRM07_REPOSITORY_ROOT": str(REPOSITORY),
        "BRM07_TEST_RAW_ROOT": str(RAW_ROOT),
        "BRM07_CACHE_ROOT": str(CACHE_ROOT),
        "BRM07_FINAL_ROOT": str(FINAL_ROOT),
        "PYTHONDONTWRITEBYTECODE": "1",
    }
)

from tests import test_v07


def main() -> int:
    names = (
        "tests.test_v07.PathAndFailureTests.test_publish_rename_failure_cleans_staging",
        "tests.test_v07.PathAndFailureTests.test_staging_reparse_replacement_rejected_before_download",
    )
    suite = unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromName(name) for name in names)
    stream = io.StringIO()
    started = time.monotonic()
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    audit = None
    audit_error = None
    try:
        audit = test_v07.audit_live_runtime()
    except Exception as error:
        audit_error = {"type": type(error).__name__, "message": str(error)}
    record = {
        "audit": audit,
        "audit_error": audit_error,
        "elapsed_milliseconds": int((time.monotonic() - started) * 1000),
        "errors": [{"test": str(test), "traceback": trace} for test, trace in result.errors],
        "failures": [{"test": str(test), "traceback": trace} for test, trace in result.failures],
        "purpose": "new publish-boundary, staging-replacement, exact-no-replace, and live-audit diagnostics only; known authority-mint and ZIP-reparse failures were not repeated",
        "schema_id": "S0-PUBLIC-BRM-V0.7-TARGETED-TEST-VERIFICATION-RAW-1",
        "skipped": [{"test": str(test), "reason": reason} for test, reason in result.skipped],
        "status": "PASS" if result.wasSuccessful() and audit_error is None else "FAIL",
        "stderr": "",
        "stdout": stream.getvalue(),
        "tests_run": result.testsRun,
    }
    raw = json.dumps(record, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8") + b"\n"
    filename = "targeted-verification-result.json"
    value_hash = hashlib.sha256(raw).hexdigest()
    (RAW_ROOT / filename).write_bytes(raw)
    (RAW_ROOT / f"{filename}.sha256").write_bytes(f"{value_hash}  {filename}\n".encode("ascii"))
    print(json.dumps({"audit": audit_error is None, "errors": len(result.errors), "failures": len(result.failures), "skipped": len(result.skipped), "status": record["status"], "tests_run": result.testsRun}, separators=(",", ":"), sort_keys=True))
    return 0 if record["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())

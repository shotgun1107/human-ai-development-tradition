"""Discriminate the cycle-2 live publication failure without running the suite."""

from __future__ import annotations

import ctypes
import hashlib
import importlib
import json
import os
import sys
import time
import traceback
from pathlib import Path
from unittest import mock


REPOSITORY = Path(r"C:\Users\SSAFY\AppData\Local\Temp\cpr01-862b27cd").resolve(strict=True)
RAW_ROOT = Path(r"C:\Users\SSAFY\AppData\Local\Temp\brm07-6a21dc13\test-verification-r2").resolve(strict=True)
CACHE_ROOT = Path(r"C:\Users\SSAFY\AppData\Local\Temp\brm07-6a21dc13\cache").resolve(strict=True)
FINAL_ROOT = Path(r"C:\Users\SSAFY\AppData\Local\Temp\brm07-6a21dc13\runtime-final-r2")
IMPLEMENTATION = REPOSITORY / "s0-lab/assembly-rehearsal/build-runtime-materialization-v0.7/implementation"
sys.path.insert(0, str(IMPLEMENTATION))
publication = importlib.import_module("s0_public_build_runtime.publication")
materialize = importlib.import_module("s0_public_build_runtime.materialize")


def write_pair(filename: str, value: object) -> str:
    raw = json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8") + b"\n"
    value_hash = hashlib.sha256(raw).hexdigest()
    (RAW_ROOT / filename).write_bytes(raw)
    (RAW_ROOT / f"{filename}.sha256").write_bytes(f"{value_hash}  {filename}\n".encode("ascii"))
    return value_hash


def main() -> int:
    if FINAL_ROOT.exists():
        raise SystemExit("diagnostic requires the failed-live destination to remain absent")
    events: list[dict[str, object]] = []
    original_pair = materialize._write_pair
    original_absence = publication._relative_absence
    original_rename = publication._rename_by_handle

    def observed_pair(directory, filename, value):
        result = original_pair(directory, filename, value)
        events.append({"event": "write-pair-complete", "filename": filename, "sha256": result})
        return result

    def observed_absence(*args, **kwargs):
        try:
            result = original_absence(*args, **kwargs)
        except Exception as error:
            events.append({"event": "retained-parent-absence-error", "error_type": type(error).__name__, "message": str(error)})
            raise
        events.append({"event": "retained-parent-absence-complete", "observation": result})
        return result

    def observed_rename(*args, **kwargs):
        events.append(
            {
                "event": "rename-call-start",
                "file_information_class_numeric": publication.FILE_INFORMATION_CLASS_NUMERIC,
                "primitive": publication.PUBLICATION_PRIMITIVE_ID,
                "rename_flags_numeric": publication.RENAME_FLAGS_NUMERIC,
            }
        )
        try:
            result = original_rename(*args, **kwargs)
        except Exception as error:
            events.append({"event": "rename-call-error", "error_type": type(error).__name__, "message": str(error), "last_error_after_raise": ctypes.get_last_error()})
            raise
        events.append({"event": "rename-call-complete"})
        return result

    started = time.monotonic()
    caught = None
    caught_traceback = None
    with mock.patch.object(materialize, "_write_pair", side_effect=observed_pair), mock.patch.object(
        publication, "_relative_absence", side_effect=observed_absence
    ), mock.patch.object(publication, "_rename_by_handle", side_effect=observed_rename):
        try:
            materialize.materialize(str(REPOSITORY), str(CACHE_ROOT), str(FINAL_ROOT))
        except Exception as error:
            caught = {"error_type": type(error).__name__, "message": str(error)}
            caught_traceback = traceback.format_exc()
    parent = FINAL_ROOT.parent
    record = {
        "elapsed_milliseconds": int((time.monotonic() - started) * 1000),
        "events": events,
        "exception": caught,
        "final_exists": FINAL_ROOT.exists(),
        "lock_exists": (parent / f".{FINAL_ROOT.name}.s0-brm-v0.7.lock").exists(),
        "schema_id": "S0-PUBLIC-BRM-V0.7-CYCLE-2-LIVE-DIAGNOSTIC-RAW-1",
        "staging_count": len(list(parent.glob(f".{FINAL_ROOT.name}.staging-*"))),
        "traceback": caught_traceback,
    }
    result_hash = write_pair("cycle-2-live-diagnostic.json", record)
    print(json.dumps({"event_count": len(events), "exception": caught, "result_sha256": result_hash}, separators=(",", ":"), sort_keys=True))
    return 0 if caught is not None else 1


if __name__ == "__main__":
    raise SystemExit(main())

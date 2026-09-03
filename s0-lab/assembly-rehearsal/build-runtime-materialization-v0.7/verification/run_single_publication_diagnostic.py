"""One user-authorized retained-handle publication diagnostic; no build, suite, or network."""

from __future__ import annotations

import ctypes
import hashlib
import importlib
import json
import os
import shutil
import sys
import time
from pathlib import Path
from unittest import mock


REPOSITORY = Path(r"C:\Users\SSAFY\AppData\Local\Temp\cpr01-862b27cd").resolve(strict=True)
DIAGNOSTIC_ROOT = Path(r"C:\Users\SSAFY\AppData\Local\Temp\brm07-6a21dc13\test-verification-r3\single-publication-diagnostic")
WORK_ROOT = DIAGNOSTIC_ROOT / "work"
IMPLEMENTATION = REPOSITORY / "s0-lab/assembly-rehearsal/build-runtime-materialization-v0.7/implementation"
PUBLICATION_SHA256 = "0184575017506860f39f1ac54b502ea239788ec7476e90350bb710fe3ea1700e"


def file_hash(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def main() -> int:
    if DIAGNOSTIC_ROOT.exists():
        raise SystemExit("diagnostic root must initially be absent")
    publication_path = IMPLEMENTATION / "s0_public_build_runtime/publication.py"
    if file_hash(publication_path) != PUBLICATION_SHA256:
        raise SystemExit("publication.py authentication failed before import")
    DIAGNOSTIC_ROOT.mkdir(parents=True)
    WORK_ROOT.mkdir()
    source = WORK_ROOT / "staging"
    final = WORK_ROOT / "runtime-final-r3"
    source.mkdir()
    (source / "source-sentinel").write_bytes(b"source-preserved")
    sys.path.insert(0, str(IMPLEMENTATION))
    publication = importlib.import_module("s0_public_build_runtime.publication")
    events: list[dict[str, object]] = []
    sequence = 0

    def event(name: str, **fields: object) -> None:
        nonlocal sequence
        sequence += 1
        events.append({"event": name, "sequence": sequence, **fields})

    transaction = None
    caught = None
    rename_calls = 0
    started = time.monotonic()
    original_absence = publication._relative_absence
    original_rename = publication._rename_by_handle

    def observed_absence(*args, **kwargs):
        event("retained-parent-absence-query-start")
        try:
            result = original_absence(*args, **kwargs)
        except Exception as error:
            event("retained-parent-absence-query-error", error_type=type(error).__name__, message=str(error))
            raise
        event("retained-parent-absence-query-complete", observation=result)
        return result

    def observed_rename(kernel32, source_handle, parent_handle, leaf):
        nonlocal rename_calls
        rename_calls += 1
        name_bytes = leaf.encode("utf-16-le", "strict")
        event(
            "native-rename-call-start",
            buffer_size=ctypes.sizeof(publication._FILE_RENAME_INFO_EX) + len(name_bytes),
            file_information_class_numeric=publication.FILE_INFORMATION_CLASS_NUMERIC,
            file_name_length_bytes=len(name_bytes),
            file_name_offset=publication._FILE_RENAME_INFO_EX.FileName.offset,
            flags_offset=publication._FILE_RENAME_INFO_EX.Flags.offset,
            primitive_id=publication.PUBLICATION_PRIMITIVE_ID,
            rename_flags_numeric=publication.RENAME_FLAGS_NUMERIC,
            root_directory_offset=publication._FILE_RENAME_INFO_EX.RootDirectory.offset,
            structure_size=ctypes.sizeof(publication._FILE_RENAME_INFO_EX),
        )
        try:
            result = original_rename(kernel32, source_handle, parent_handle, leaf)
        except Exception as error:
            event("native-rename-call-error", error_type=type(error).__name__, last_error=ctypes.get_last_error(), message=str(error))
            raise
        event("native-rename-call-complete")
        return result

    try:
        transaction = publication.PublicationTransaction(WORK_ROOT, final)
        event(
            "destination-parent-handle-retained",
            file_id=transaction.parent.identity.file_id,
            volume_serial_number=transaction.parent.identity.volume_serial_number,
        )
        transaction.bind_source(source)
        event(
            "source-handle-retained",
            file_id=transaction.source.identity.file_id,
            same_volume=transaction.source.identity.volume_serial_number == transaction.parent.identity.volume_serial_number,
            volume_serial_number=transaction.source.identity.volume_serial_number,
        )
        transaction.require_unpublished(source)
        event("retained-identities-revalidated")
        with mock.patch.object(publication, "_relative_absence", side_effect=observed_absence), mock.patch.object(
            publication, "_rename_by_handle", side_effect=observed_rename
        ):
            try:
                transaction.publish_no_replace(source)
            except Exception as error:
                caught = {"error_type": type(error).__name__, "message": str(error)}
                event("publication-transaction-error", **caught)
    finally:
        if transaction is not None:
            state_before_close = {
                "published": transaction.published,
                "rename_invoked": transaction._rename_invoked,
                "source_exists": source.exists(),
                "destination_exists": final.exists(),
                "source_sentinel_preserved": (source / "source-sentinel").read_bytes() == b"source-preserved" if source.exists() else False,
            }
            transaction.close()
            event("retained-handles-closed")
        else:
            state_before_close = None
        resolved_work = WORK_ROOT.resolve(strict=True)
        if os.path.commonpath((str(resolved_work), str(DIAGNOSTIC_ROOT.resolve(strict=True)))) != str(DIAGNOSTIC_ROOT.resolve(strict=True)):
            raise RuntimeError("diagnostic cleanup target escaped its root")
        shutil.rmtree(WORK_ROOT)
        event("owned-diagnostic-work-cleaned", work_exists=WORK_ROOT.exists())

    record = {
        "elapsed_milliseconds": int((time.monotonic() - started) * 1000),
        "events": events,
        "exception": caught,
        "network_used": False,
        "primitive_call_count": rename_calls,
        "publication_sha256": PUBLICATION_SHA256,
        "schema_id": "S0-PUBLIC-BRM-V0.7-SINGLE-PUBLICATION-DIAGNOSTIC-RAW-1",
        "state_before_close": state_before_close,
        "suite_run": False,
        "work_root_exists_after_cleanup": WORK_ROOT.exists(),
    }
    raw = json.dumps(record, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8") + b"\n"
    result_hash = hashlib.sha256(raw).hexdigest()
    filename = "single-publication-diagnostic.json"
    (DIAGNOSTIC_ROOT / filename).write_bytes(raw)
    (DIAGNOSTIC_ROOT / f"{filename}.sha256").write_bytes(f"{result_hash}  {filename}\n".encode("ascii"))
    print(json.dumps({"exception": caught, "primitive_call_count": rename_calls, "result_sha256": result_hash, "work_clean": not WORK_ROOT.exists()}, separators=(",", ":"), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

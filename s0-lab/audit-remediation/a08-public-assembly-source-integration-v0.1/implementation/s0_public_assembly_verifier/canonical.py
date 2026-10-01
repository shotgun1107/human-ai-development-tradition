"""Independent strict canonical JSON and v0.5 authority reconstruction."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .errors import auth_failure
from .integrity import INTERFACE_MAP_PATH, read_exact_public_file, verify_v0_5_design_authority


INTERFACE_MAP_SHA256 = "6c2f5ac03ee6cbfad406e96c5cb35ceb5f548e74f04c37e71307b155a18915a4"
RUN_RECORD_BYTES = 2224
RUN_RECORD_SHA256 = "73b2091e7aab315bcafd487965dc8c3304b19afca56132de471c787254b7fda6"
RECEIPT_BYTES = 1173
_LOWER_SHA256 = re.compile(r"^[0-9a-f]{64}$")


def _duplicate_safe_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def parse_strict_json(raw: bytes) -> dict[str, Any]:
    if type(raw) is not bytes or raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw:
        raise ValueError("JSON bytes are not strict UTF-8/LF text")
    try:
        value = json.loads(raw, object_pairs_hook=_duplicate_safe_object)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("invalid strict JSON") from exc
    if type(value) is not dict:
        raise ValueError("JSON root must be an object")
    return value


def canonical_json_bytes(value: dict[str, Any]) -> bytes:
    if type(value) is not dict:
        raise TypeError("canonical root must be an exact object")
    return (
        json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("ascii")


def load_interface_map(workspace_root: Path) -> dict[str, Any]:
    verify_v0_5_design_authority(workspace_root)
    raw = read_exact_public_file(workspace_root, INTERFACE_MAP_PATH, INTERFACE_MAP_SHA256)
    value = parse_strict_json(raw)
    if value.get("schema_id") != "S0-PUBLIC-ASSEMBLY-REHEARSAL-INTERFACE-MAP-5":
        raise auth_failure("v0.5 interface-map schema mismatch")
    return value


def expected_run_record_bytes(workspace_root: Path) -> bytes:
    interface = load_interface_map(workspace_root)
    section = interface.get("run_record_v3")
    if type(section) is not dict or type(section.get("exact_object")) is not dict:
        raise auth_failure("v0.5 interface map lacks exact run-record authority")
    raw = canonical_json_bytes(section["exact_object"])
    import hashlib

    if (
        section.get("schema_id") != "S0-PUBLIC-ASSEMBLY-RUN-RECORD-3"
        or section.get("field_count") != 38
        or section.get("canonical_bytes") != RUN_RECORD_BYTES
        or section.get("canonical_sha256") != RUN_RECORD_SHA256
        or len(section["exact_object"]) != 38
        or len(raw) != RUN_RECORD_BYTES
    ):
        raise auth_failure("run-record field or byte count mismatch")
    if hashlib.sha256(raw).hexdigest() != RUN_RECORD_SHA256:
        raise auth_failure("run-record frozen SHA-256 mismatch")
    return raw


def expected_receipt_bytes(workspace_root: Path, pin_fields: dict[str, str]) -> bytes:
    interface = load_interface_map(workspace_root)
    section = interface.get("receipt_v2")
    if type(section) is not dict or type(section.get("fixed_values")) is not dict:
        raise auth_failure("v0.5 interface map lacks receipt-v2 authority")
    if set(pin_fields) != {
        "assembly_implementation_manifest_sha256",
        "design_package_manifest_sha256",
        "design_independent_review_sha256",
    }:
        raise auth_failure("receipt external pin field set mismatch")
    if any(type(value) is not str or _LOWER_SHA256.fullmatch(value) is None for value in pin_fields.values()):
        raise auth_failure("receipt external pins must be exact lowercase SHA-256 values")
    receipt = dict(section["fixed_values"])
    receipt.update(pin_fields)
    raw = canonical_json_bytes(receipt)
    if (
        section.get("schema_id") != "S0-PUBLIC-ASSEMBLY-PUBLICATION-RECEIPT-2"
        or section.get("field_count") != 21
        or section.get("canonical_byte_length_for_any_admissible_three_digest_tuple") != RECEIPT_BYTES
        or section.get("field_order_for_review") != sorted(receipt)
        or len(receipt) != 21
        or len(raw) != RECEIPT_BYTES
    ):
        raise auth_failure("receipt field or byte count mismatch")
    return raw

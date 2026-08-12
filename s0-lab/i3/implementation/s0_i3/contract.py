"""Authentication and semantic checks for the public I3 contract JSON."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .classifier import STATUS_FIELDS
from .errors import I3BindingError
from .records import ADMISSION_FIELD_ORDER, OUTCOME_FIELD_ORDER


CONTRACT_SHA256 = "ae834becfc393e4f525265aff473ae32d12f349713fb48b2e0bb60ea39fc7ac8"
I2_CONTRACT_SHA256 = "713fc6b44c84126387dc492b93e22d928ba894e18bdc8705049a2ea5cb8cc7da"
I2_IMPLEMENTATION_FILES_SHA256 = (
    "18ccfbcbe73b1170e07bd000376b079528dcf135b806e3f6c77b10efae736bd6"
)
I3_IMPLEMENTATION_V0_1_INDEPENDENT_REVIEW_SHA256 = (
    "ec1ecc1f9aaf9b32ca7d285d898ec5620e05a8327716a0e16eed2d01530b28ca"
)
EXPECTED_CLASSIFICATION_ORDER = (
    "PRE-R",
    "PRE-A",
    "P-CRASH",
    "P-MISSING",
    "P-DUPLICATE",
    "P-DISAGREE-H",
    "P-DISAGREE-Z",
    "P-PARSE-REJECTED",
    "P-VALIDATION-REJECTED",
    "P-STATE-COMMIT-FAILED",
    "P-ACCEPTED",
)


def _duplicate_safe_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for name, value in pairs:
        if name in result:
            raise I3BindingError("public I3 contract contains a duplicate JSON key")
        result[name] = value
    return result


def _require_equal(actual: object, expected: object, label: str) -> None:
    if actual != expected:
        raise I3BindingError(f"public I3 contract mismatch: {label}")


def _sha256(raw: bytes) -> str:
    import hashlib

    return hashlib.sha256(raw).hexdigest()


def verify_contract_bytes(raw: bytes) -> dict[str, Any]:
    if type(raw) is not bytes:
        raise I3BindingError("public I3 contract must be exact bytes")
    if _sha256(raw) != CONTRACT_SHA256:
        raise I3BindingError("public I3 contract SHA-256 mismatch")
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw or not raw.endswith(b"\n"):
        raise I3BindingError("public I3 contract text form is noncanonical")
    try:
        document = json.loads(raw, object_pairs_hook=_duplicate_safe_object)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise I3BindingError("public I3 contract is not strict JSON") from exc
    expected_keys = {
        "schema_id",
        "version",
        "claim_kind",
        "source_bindings",
        "records",
        "interfaces",
        "classification_order",
        "status_fields",
        "stable_errors",
        "unsupported_boundaries",
    }
    _require_equal(set(document), expected_keys, "top-level keys")
    _require_equal(document["schema_id"], "S0-I3-PUBLIC-IMPORT-DECISION-CONTRACT-1", "schema")
    _require_equal(document["version"], "0.2.0", "version")
    _require_equal(
        document["claim_kind"],
        "bounded public model-free implementation revision candidate only",
        "claim kind",
    )
    sources = document["source_bindings"]
    _require_equal(sources["i2_contract_sha256"], I2_CONTRACT_SHA256, "I2 contract")
    _require_equal(
        sources["i2_implementation_files_sha256"],
        I2_IMPLEMENTATION_FILES_SHA256,
        "I2 implementation files",
    )
    _require_equal(
        sources["i3_implementation_v0_1_independent_review_sha256"],
        I3_IMPLEMENTATION_V0_1_INDEPENDENT_REVIEW_SHA256,
        "I3 implementation v0.1 independent review",
    )
    records = document["records"]
    _require_equal(records["import_admission"]["line_count"], 21, "admission count")
    _require_equal(
        tuple(records["import_admission"]["field_order"]),
        ADMISSION_FIELD_ORDER,
        "admission order",
    )
    _require_equal(records["import_outcome"]["line_count"], 26, "outcome count")
    _require_equal(records["import_outcome"]["raw_medium_bytes"], 2048, "medium size")
    _require_equal(
        tuple(records["import_outcome"]["field_order"]),
        OUTCOME_FIELD_ORDER,
        "outcome order",
    )
    _require_equal(records["import_event"]["line_count"], 31, "I2 event count")
    _require_equal(
        records["import_event"]["reuse"],
        "s0_i2 v0.4 exact parser/serializer/lifecycle/global-link",
        "I2 global-link reuse",
    )
    _require_equal(
        tuple(document["interfaces"]["finalize_import_attempt"]),
        (
            "ImportClassification",
            "optional-I2-event-bytes",
            "append_status",
            "signer_context",
            "expected_sequence",
            "expected_previous_event_sha256",
        ),
        "finalizer interface",
    )
    _require_equal(
        tuple(document["classification_order"]),
        EXPECTED_CLASSIFICATION_ORDER,
        "classification order",
    )
    _require_equal(tuple(document["status_fields"]), STATUS_FIELDS, "status fields")
    return document


def verify_contract_file(path: Path) -> dict[str, Any]:
    if not isinstance(path, Path):
        raise I3BindingError("public I3 contract path must be pathlib.Path")
    return verify_contract_bytes(path.read_bytes())

"""Authentication and semantic cross-checks for the public I2 contract."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .canonical import sha256_bytes
from .errors import BindingError
from .records import (
    ADMISSION_FIELD_ORDER,
    EVENT_FIELD_ORDER,
    IMPORT_ROUTE_STATES,
    OUTCOME_FIELD_ORDER,
)
from .vectors import (
    TRI2_VEC_02_ARTIFACT_SHA256,
    TRI2_VEC_02_DECISION_SHA256,
    TRI2_VEC_02_DERIVATION_SHA256,
    TRI2_VEC_02_ROWS,
)


CONTRACT_SHA256 = "1b77c5d8ee0c3c3e91c348ce1e8dc5a1d4794e98e65f0c1dc9f26cc0ecb8244f"
EXPECTED_INVENTORY = {
    "aggregated_role_rows": 32,
    "role_positions": 40,
    "paired_rows": 8,
    "experimental_signers": 21,
    "non_row_roots": 1,
    "registry_ids": 22,
    "experimental_stores": 27,
    "explicit_readers": 46,
    "edges": 64,
    "acceptance_rows": 107,
    "signature_scopes": 3,
    "ledger_namespaces": 3,
}
EXPECTED_LIFECYCLE_VARIANTS = (
    "reserved",
    "admission-frozen",
    "pending",
    "accepted",
    "direct-terminal-reserved",
    "direct-terminal-admission-frozen",
    "parse-rejected",
    "validation-rejected",
    "state-commit-failed",
    "crash",
    "missing",
    "duplicate",
    "disagreement",
)
EXPECTED_CLASSIFICATION_PRECEDENCE = (
    "crash",
    "missing",
    "duplicate",
    "disagreement",
    "parse-rejected",
    "validation-rejected",
    "state-commit-failed",
    "accepted",
)


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise BindingError("public contract contains a duplicate JSON key")
        result[key] = value
    return result


def _require_equal(actual: object, expected: object, label: str) -> None:
    if actual != expected:
        raise BindingError(f"public contract mismatch: {label}")


def verify_contract_bytes(raw: bytes) -> dict[str, Any]:
    if type(raw) is not bytes:
        raise BindingError("public contract must be exact bytes")
    if sha256_bytes(raw) != CONTRACT_SHA256:
        raise BindingError("public contract SHA-256 mismatch")
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw or not raw.endswith(b"\n"):
        raise BindingError("public contract must be BOM-free LF-only bytes with final LF")
    for line in raw.splitlines():
        if line.endswith((b" ", b"\t")):
            raise BindingError("public contract contains trailing whitespace")
    try:
        document = json.loads(raw, object_pairs_hook=_reject_duplicate_pairs)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise BindingError("public contract is not strict JSON") from exc
    if type(document) is not dict:
        raise BindingError("public contract root must be an object")

    _require_equal(
        document.get("schema_id"),
        "S0-TRUST-ROOT-ROLE-ISOLATION-PUBLIC-CONTRACT-1",
        "schema_id",
    )
    _require_equal(document.get("preserved_inventory"), EXPECTED_INVENTORY, "inventory")
    route_states = {
        key: (value["source"], value["destination"])
        for key, value in document.get("route_states", {}).items()
    }
    _require_equal(route_states, IMPORT_ROUTE_STATES, "route states")
    records = document.get("records", {})
    expected_records = {
        "import_admission": ("S0-SIGNER-IMPORT-ADMISSION-2", ADMISSION_FIELD_ORDER),
        "import_outcome": ("S0-SIGNER-IMPORT-OUTCOME-1", OUTCOME_FIELD_ORDER),
        "import_ledger_event": (
            "S0-SIGNER-MEDIA-LEDGER-IMPORT-EVENT-1",
            EVENT_FIELD_ORDER,
        ),
    }
    for name, (schema, fields) in expected_records.items():
        record = records.get(name, {})
        _require_equal(record.get("schema"), schema, f"{name} schema")
        _require_equal(record.get("line_count"), len(fields), f"{name} line count")
        _require_equal(tuple(record.get("field_order", ())), fields, f"{name} field order")
    _require_equal(records["import_outcome"].get("maximum_bytes"), 2048, "outcome maximum bytes")
    _require_equal(
        tuple(document.get("lifecycle_variants", ())),
        EXPECTED_LIFECYCLE_VARIANTS,
        "lifecycle variants",
    )
    _require_equal(
        tuple(document.get("classification_precedence", ())),
        EXPECTED_CLASSIFICATION_PRECEDENCE,
        "classification precedence",
    )
    bindings = document.get("source_bindings", {})
    _require_equal(
        bindings.get("tri2_vec_02_artifact_sha256"),
        TRI2_VEC_02_ARTIFACT_SHA256,
        "vector artifact hash",
    )
    _require_equal(
        bindings.get("tri2_vec_02_derivation_sha256"),
        TRI2_VEC_02_DERIVATION_SHA256,
        "vector derivation hash",
    )
    _require_equal(
        bindings.get("tri2_vec_02_final_decision_sha256"),
        TRI2_VEC_02_DECISION_SHA256,
        "vector decision hash",
    )
    vector = document.get("tri2_vec_02", {})
    _require_equal(vector.get("artifact_id"), "TRI2-VEC-02", "vector artifact ID")
    _require_equal(vector.get("withdrawn_predecessor"), "TRI2-VEC-01", "withdrawn vector")
    _require_equal(
        tuple(tuple(row) for row in vector.get("rows", ())),
        TRI2_VEC_02_ROWS,
        "vector rows",
    )
    return document


def verify_contract_file(path: Path) -> dict[str, Any]:
    if not isinstance(path, Path):
        raise BindingError("public contract path must be pathlib.Path")
    return verify_contract_bytes(path.read_bytes())

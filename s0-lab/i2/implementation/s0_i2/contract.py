"""Exact authentication and semantic checks for the public I2 v0.2 contract."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .canonical import sha256_bytes
from .errors import BindingError
from .records import (
    EVENT_FIELD_ORDER,
    FROZEN_REGISTRY_ROLE_ORDER,
    I1_PUBLIC_RUNTIME_MANIFEST_SHA256,
    IMPORT_ROUTE_STATES,
    NON_ROOT_SIGNER_ROLE_ORDER,
    SignerRegistryContext,
    bind_public_i1_signer_context,
)
from .vectors import (
    TRI2_VEC_02_ARTIFACT_SHA256,
    TRI2_VEC_02_DECISION_SHA256,
    TRI2_VEC_02_DERIVATION_SHA256,
    TRI2_VEC_02_ROWS,
)


CONTRACT_SHA256 = "447b56c39f16c37272edd527d44e06328b5245a51dc8e83bc17a931cad26b2a8"
I1_PUBLIC_RUNTIME_JSON_SHA256 = (
    "fd9e4a474bb5438065dff0a51c24cd2eb4e8e1caa2cbb5d6eb169b540c691d08"
)
EXPECTED_SOURCE_BINDINGS = {
    "trust_root_role_isolation_v0_4_sha256": "5794a2c1d80889af96d2838e951d685a8d0a7d0fad3a209895adb01319dafed3",
    "trust_root_control_integration_sha256": "f172ba01bc37a6a96077f6441aca24cd525f19f034623c752d638a00ec0378c0",
    "identity_authority_matrix_v0_4_sha256": "19f085b320cc718f33c623566eea984f2271ee1906184d246053f01070dea1c8",
    "isolation_acceptance_plan_v0_4_sha256": "f48cd91f71f79d223ce7359d6af543198218ecbd743ca99fdb0c770d1c788d73",
    "tri2_vec_02_control_freeze_sha256": TRI2_VEC_02_DECISION_SHA256,
    "tri2_vec_02_artifact_sha256": TRI2_VEC_02_ARTIFACT_SHA256,
    "tri2_vec_02_derivation_sha256": TRI2_VEC_02_DERIVATION_SHA256,
    "tri2_vec_02_independent_verification_sha256": "fb5df64e3428904d097b0f6130fdc20dbb945f96957934e210377d7dbd842438",
    "i1_public_runtime_manifest_sha256": I1_PUBLIC_RUNTIME_MANIFEST_SHA256,
    "i1_public_runtime_json_sha256": I1_PUBLIC_RUNTIME_JSON_SHA256,
}
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
    "future_units": 8,
    "maximum_concurrency": 3,
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
EXPECTED_SUPPORTED_VALIDATION = (
    "exact import-event byte parsing and serialization",
    "import-event SHA-256",
    "single-event lifecycle tuple structure",
    "route-local R-A-P-C ordering and immutable route binding",
    "caller-supplied global predecessor structural link",
    "emitted event ID duplicate rejection within a supplied contiguous trace",
    "preallocated R-A-P-C ID non-overlap across a supplied multi-route set",
    "exact I1 signer-identifier inventory binding",
    "exact frozen TRI2-VEC-02 evidence binding",
)
EXPECTED_UNSUPPORTED_BOUNDARIES = (
    "import-admission-exact-grammar",
    "import-outcome-exact-grammar",
    "complete-outcome-classification",
    "durable-ledger",
    "project-lifetime-uniqueness",
    "atomic-append",
    "witness-validation",
    "actual-registry-authority",
    "provider-or-platform-enforcement",
)
EXPECTED_FORBIDDEN_CAPABILITIES = (
    "key-generation",
    "signature-generation-or-verification",
    "curve-or-point-operations",
    "private-key-custody",
    "anchor-or-registry-activation",
    "ledger-or-witness-provider",
    "vm-sandbox-account-or-network-enforcement",
    "provider-or-model-session",
    "protected-material",
    "fixture-or-hidden-oracle",
    "executor-judge-scoring-or-statistics",
    "e0-or-s0-execution",
    "central-system-or-project-brain",
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
    if raw.startswith(b"\xef\xbb\xbf"):
        raise BindingError("public contract must be BOM-free")
    if b"\r" in raw:
        raise BindingError("public contract must be LF-only")
    if not raw.endswith(b"\n"):
        raise BindingError("public contract must end with LF")
    for line in raw.splitlines():
        if line.endswith((b" ", b"\t")):
            raise BindingError("public contract contains trailing whitespace")
    try:
        document = json.loads(raw, object_pairs_hook=_reject_duplicate_pairs)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise BindingError("public contract is not strict JSON") from exc
    if type(document) is not dict:
        raise BindingError("public contract root must be an object")

    expected_top_level = {
        "schema_id",
        "version",
        "claim_kind",
        "source_bindings",
        "preserved_inventory",
        "signer_registry",
        "route_states",
        "records",
        "lifecycle_variants",
        "supported_validation",
        "unsupported_boundaries",
        "complete_validation_status",
        "tri2_vec_02",
        "forbidden_capabilities",
    }
    _require_equal(set(document), expected_top_level, "top-level keys")
    _require_equal(
        document["schema_id"],
        "S0-TRUST-ROOT-ROLE-ISOLATION-PUBLIC-CONTRACT-2",
        "schema_id",
    )
    _require_equal(document["version"], "0.2.0", "version")
    _require_equal(
        document["claim_kind"],
        "bounded public construction candidate only",
        "claim kind",
    )
    _require_equal(document["source_bindings"], EXPECTED_SOURCE_BINDINGS, "source bindings")
    _require_equal(document["preserved_inventory"], EXPECTED_INVENTORY, "inventory")

    registry = document["signer_registry"]
    _require_equal(
        set(registry),
        {"authority_kind", "registry_role_order", "non_root_signer_roles"},
        "signer registry keys",
    )
    _require_equal(
        registry["authority_kind"],
        "authenticated public identifier inventory only",
        "signer authority kind",
    )
    _require_equal(
        tuple(registry["registry_role_order"]),
        FROZEN_REGISTRY_ROLE_ORDER,
        "registry role order",
    )
    _require_equal(
        tuple(registry["non_root_signer_roles"]),
        NON_ROOT_SIGNER_ROLE_ORDER,
        "non-root signer order",
    )

    route_states = {
        key: (value["source"], value["destination"])
        for key, value in document["route_states"].items()
    }
    _require_equal(route_states, IMPORT_ROUTE_STATES, "route states")

    records = document["records"]
    _require_equal(set(records), {"import_ledger_event"}, "record boundary")
    event_record = records["import_ledger_event"]
    _require_equal(
        set(event_record),
        {"schema", "line_count", "encoding", "field_order"},
        "import-event keys",
    )
    _require_equal(
        event_record["schema"],
        "S0-SIGNER-MEDIA-LEDGER-IMPORT-EVENT-1",
        "import-event schema",
    )
    _require_equal(event_record["line_count"], 31, "import-event line count")
    _require_equal(
        event_record["encoding"],
        "strict ASCII name=value lines with LF after every line",
        "import-event encoding",
    )
    _require_equal(
        tuple(event_record["field_order"]),
        EVENT_FIELD_ORDER,
        "import-event field order",
    )

    _require_equal(
        tuple(document["lifecycle_variants"]),
        EXPECTED_LIFECYCLE_VARIANTS,
        "lifecycle variants",
    )
    _require_equal(
        tuple(document["supported_validation"]),
        EXPECTED_SUPPORTED_VALIDATION,
        "supported validation",
    )
    _require_equal(
        tuple(document["unsupported_boundaries"]),
        EXPECTED_UNSUPPORTED_BOUNDARIES,
        "unsupported boundaries",
    )
    _require_equal(document["complete_validation_status"], "BLOCKED", "complete status")

    vector = document["tri2_vec_02"]
    _require_equal(
        set(vector), {"artifact_id", "withdrawn_predecessor", "rows"}, "vector keys"
    )
    _require_equal(vector["artifact_id"], "TRI2-VEC-02", "vector artifact ID")
    _require_equal(vector["withdrawn_predecessor"], "TRI2-VEC-01", "withdrawn vector")
    _require_equal(
        tuple(tuple(row) for row in vector["rows"]),
        TRI2_VEC_02_ROWS,
        "vector rows",
    )
    _require_equal(
        tuple(document["forbidden_capabilities"]),
        EXPECTED_FORBIDDEN_CAPABILITIES,
        "forbidden capabilities",
    )

    # Constructing this handle is the mechanical link between the contract's
    # exact I1 manifest identity and the event parser's signer allowlist.
    bind_public_i1_signer_context(
        manifest_sha256=document["source_bindings"]["i1_public_runtime_manifest_sha256"],
        registry_role_order=document["signer_registry"]["registry_role_order"],
    )
    return document


def signer_context_from_contract_bytes(raw: bytes) -> SignerRegistryContext:
    document = verify_contract_bytes(raw)
    return bind_public_i1_signer_context(
        manifest_sha256=document["source_bindings"]["i1_public_runtime_manifest_sha256"],
        registry_role_order=document["signer_registry"]["registry_role_order"],
    )


def verify_contract_file(path: Path) -> dict[str, Any]:
    if not isinstance(path, Path):
        raise BindingError("public contract path must be pathlib.Path")
    return verify_contract_bytes(path.read_bytes())


def signer_context_from_contract_file(path: Path) -> SignerRegistryContext:
    if not isinstance(path, Path):
        raise BindingError("public contract path must be pathlib.Path")
    return signer_context_from_contract_bytes(path.read_bytes())

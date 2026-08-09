"""Authenticated v0.14 public role/store/edge/status topology checks."""

from __future__ import annotations

import json
from copy import deepcopy
from collections.abc import Iterator, Mapping, Sequence
from dataclasses import asdict, dataclass, field
from pathlib import Path
from types import MappingProxyType
from typing import Any, Iterable

from jsonschema import Draft202012Validator

from .auth import (
    authenticate_manifest_file_set,
    bind_external_manifest_grant,
    load_authenticated_manifest,
    sha256_bytes,
)
from .errors import TopologyError
from .json_bytes import parse_strict_json_bytes


FROZEN_PUBLIC_SPEC_MANIFEST_SHA256 = "9fdffa48994626f63527ee6eceff9825f2df45f91dec12889362ee180d94245e"
PUBLIC_SPEC_MANIFEST_PATH = "s0-lab/i1/spec/public-runtime-files.sha256"
PUBLIC_SPEC_PATH = "s0-lab/i1/spec/public-runtime-v0.14.json"
PUBLIC_SPEC_SCHEMA_PATH = "s0-lab/i1/spec/schemas/public-runtime-topology.schema.json"
PUBLIC_SPEC_ALLOWED_PATHS = (
    "s0-lab/i1/spec/public-runtime-v0.14.json",
    "s0-lab/i1/spec/schemas/evidence-bundle-structure.schema.json",
    "s0-lab/i1/spec/schemas/evidence-receipt.schema.json",
    "s0-lab/i1/spec/schemas/one-shot-result.schema.json",
    "s0-lab/i1/spec/schemas/public-runtime-topology.schema.json",
    "s0-lab/i1/spec/schemas/signed-envelope-structure.schema.json",
    "s0-lab/i1/spec/schemas/status-record.schema.json",
)
_TOPOLOGY_PROVENANCE = object()


EXPECTED_ROLE_ROWS = (
    "registrar",
    "public-status-reader",
    "public-record-publisher",
    "public-record-reader",
    "content-intake",
    "simulation-builder",
    "fact-author",
    "label-authors",
    "label-comparison",
    "representation-builder",
    "package-builder-scanner-1",
    "scanner-2",
    "scan-comparison",
    "leakage-reviewers",
    "leakage-comparison",
    "comparator-builders",
    "expected-catalog-generators",
    "catalog-comparison",
    "p1-reviewers",
    "p1-review-comparison",
    "condition-map-schedule-custodian",
    "blinded-map-builders",
    "analysis-map-comparison",
    "dispatcher-transport-recorder",
    "public-executor",
    "raw-output-custodian-anonymizer",
    "semantic-judges",
    "judgment-comparison",
    "comparator-operators",
    "adjudication-comparison",
    "analysis",
    "final-decision-custodian",
)

EXPECTED_ROLE_LABELS = (
    "CONTROL registrar",
    "public status reader",
    "public record publisher",
    "public record reader",
    "content-intake custodian",
    "simulation builder/operator",
    "public fact author",
    "label author A / B",
    "label-comparison custodian",
    "representation builder",
    "package builder / scanner 1",
    "scanner 2",
    "scan-comparison custodian",
    "leakage reviewer 1 / 2",
    "leakage-comparison custodian",
    "comparator builder 1 / 2",
    "expected-catalog generator 1 / 2",
    "catalog-comparison custodian",
    "P1 reviewer 1 / 2",
    "P1-review comparison custodian",
    "condition-map/schedule custodian",
    "blinded-map builder 1 / 2",
    "analysis-map comparison custodian",
    "dispatcher/transport recorder",
    "public executor",
    "raw-output custodian/anonymizer",
    "semantic judge 1 / 2",
    "judgment-comparison custodian",
    "comparator operator 1 / 2",
    "adjudication-comparison custodian",
    "analysis role",
    "final-decision custodian",
)

EXPECTED_PAYLOAD_RECEIPT_SPLIT_EDGES = ("E25", "E27", "E29", "E35", "E48", "E50")
EXPECTED_TOPOLOGY_PROJECTION_SHA256 = "3e631472ab1ab3ed1baee9ef6453a423f253a308be3eb5eea9deefbf368c1a39"
EXPECTED_SOURCE_SHA256 = {
    "protocol": "b1a7216398e51d75fe35a2c54a878d03c7f1163c450e6b8119fbb2ee1e3c0b8c",
    "contract": "49e60378f54391fdcd63da9304b47e1da3a1cab8b3611b20ac6d5957e4d647f0",
    "plan": "a41ddc4d60cfadf2a90225d7fe4d5e0f5b04b90f98a9f9af7ceedd3bb3bb4eee",
    "review_response": "b23215b795f5361fcc72a2670ece32c458a6abb67a2cd9321f6925d770f58ab9",
    "independent_review": "537431d7397bea5eaba960fbdd12d0f830665fc23a56c58f88dd7bf75ff6d605",
    "control_integration_decision": "f287bba1ccf24d34ba5fbb38c7fd8d8291da981753a490a0c8ce9f167944ff65",
}

EXPECTED_STORES = (
    "registrar-receipt-vault",
    "registrar-store",
    "public-decision-store",
    "content-vault",
    "label-vault-A",
    "label-vault-B",
    "agreed-label-vault",
    "representation-vault",
    "signed-package-vault",
    "scan-vault-1",
    "scan-vault-2",
    "leakage-vault-1",
    "leakage-vault-2",
    "comparator-vault-1",
    "comparator-vault-2",
    "generator-vault-1",
    "generator-vault-2",
    "analysis-input-vault",
    "catalog-vault",
    "p1-review-vault-1",
    "p1-review-vault-2",
    "condition-map-vault",
    "analysis-map-vault",
    "raw-output-vault",
    "judgment-vault-1",
    "judgment-vault-2",
    "final-decision-vault",
)

EXPECTED_SIGNER_ROLES = (
    "adjudication-comparison",
    "analysis",
    "analysis-map-comparison",
    "catalog-comparison",
    "comparator-builder-1",
    "comparator-builder-2",
    "comparator-operator-1",
    "comparator-operator-2",
    "content-intake",
    "control-registrar",
    "control-root-authority",
    "final-decision-custodian",
    "judgment-comparison",
    "label-comparison",
    "leakage-comparison",
    "p1-review-comparison",
    "public-record-publisher",
    "representation-builder",
    "scan-comparison",
    "semantic-judge-1",
    "semantic-judge-2",
    "simulation-builder",
)

STATUS_EDGE_ORDER = (
    "E02",
    "E05",
    "E08",
    "E14",
    "E21",
    "E24",
    "E25",
    "E27",
    "E29",
    "E31",
    "E35",
    "E48",
    "E50",
    "E56",
)


def expected_edge_ids() -> tuple[str, ...]:
    return tuple(f"E00{letter}" for letter in "ABCDEFGH") + tuple(
        f"E{number:02d}" for number in range(1, 57)
    )


def expected_states() -> tuple[str, ...]:
    return ("A-0000",) + tuple(
        f"A-{((1 << count) - 1):04x}" for count in range(1, 15)
    )


@dataclass(frozen=True, order=True)
class TopologyIssue:
    category: str
    location: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return asdict(self)


def _deep_freeze(value: Any) -> Any:
    if type(value) is dict:
        return MappingProxyType({key: _deep_freeze(item) for key, item in value.items()})
    if type(value) is list:
        return tuple(_deep_freeze(item) for item in value)
    if type(value) in {str, int, bool} or value is None:
        return value
    raise TopologyError("topology contains an unsupported scalar type")


def _deep_thaw(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {key: _deep_thaw(item) for key, item in value.items()}
    if isinstance(value, tuple):
        return [_deep_thaw(item) for item in value]
    return value


def _require_deep_frozen(value: Any, active: set[int] | None = None) -> None:
    """Reject any container shape that was not produced by ``_deep_freeze``."""

    if active is None:
        active = set()
    if type(value) is MappingProxyType:
        identity = id(value)
        if identity in active:
            raise TopologyError("topology snapshot contains a container cycle")
        active.add(identity)
        try:
            for key, item in value.items():
                if type(key) is not str:
                    raise TopologyError("topology snapshot key is not exact string text")
                _require_deep_frozen(item, active)
        finally:
            active.remove(identity)
        return
    if type(value) is tuple:
        identity = id(value)
        if identity in active:
            raise TopologyError("topology snapshot contains a container cycle")
        active.add(identity)
        try:
            for item in value:
                _require_deep_frozen(item, active)
        finally:
            active.remove(identity)
        return
    if type(value) in {str, int, bool} or value is None:
        return
    raise TopologyError("topology snapshot is not deeply immutable")


def _snapshot_digest(value: Mapping[str, Any]) -> str:
    raw = json.dumps(
        _deep_thaw(value),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return sha256_bytes(raw)


@dataclass(frozen=True, init=False)
class FrozenTopology(Mapping[str, Any]):
    """API-level, deeply immutable topology handle for policy boundaries."""

    spec_sha256: str
    manifest_sha256: str
    snapshot_sha256: str
    _snapshot: Mapping[str, Any] = field(repr=False, compare=False)
    _provenance: object = field(repr=False, compare=False)

    def __init__(
        self,
        spec_sha256: str,
        manifest_sha256: str,
        snapshot_sha256: str,
        snapshot: Mapping[str, Any],
        *,
        _provenance: object,
    ) -> None:
        if _provenance is not _TOPOLOGY_PROVENANCE:
            raise TopologyError("FrozenTopology must come from the pinned public loader")
        object.__setattr__(self, "spec_sha256", spec_sha256)
        object.__setattr__(self, "manifest_sha256", manifest_sha256)
        object.__setattr__(self, "snapshot_sha256", snapshot_sha256)
        object.__setattr__(self, "_snapshot", snapshot)
        object.__setattr__(self, "_provenance", _provenance)

    def __getitem__(self, key: str) -> Any:
        return self._snapshot[key]

    def __iter__(self) -> Iterator[str]:
        return iter(self._snapshot)

    def __len__(self) -> int:
        return len(self._snapshot)

    def to_plain_dict(self) -> dict[str, Any]:
        """Return a detached diagnostic copy; it carries no policy authority."""

        return _deep_thaw(self._snapshot)


def require_frozen_topology(value: object) -> FrozenTopology:
    """Revalidate API provenance, deep immutability, and digest at a boundary."""

    if type(value) is not FrozenTopology or getattr(value, "_provenance", None) is not _TOPOLOGY_PROVENANCE:
        raise TopologyError("policy input is not an authenticated frozen topology")
    _require_deep_frozen(value._snapshot)
    if value.manifest_sha256 != FROZEN_PUBLIC_SPEC_MANIFEST_SHA256:
        raise TopologyError("topology manifest authority mismatch")
    if _snapshot_digest(value._snapshot) != value.snapshot_sha256:
        raise TopologyError("topology snapshot digest changed")
    plain = value.to_plain_dict()
    issues = audit_topology(plain)
    if issues:
        first = issues[0]
        raise TopologyError(f"{first.category} at {first.location}: {first.message}")
    return value


def _issue(
    issues: list[TopologyIssue], category: str, location: str, message: str
) -> None:
    issues.append(TopologyIssue(category, location, message))


def _duplicates(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    duplicate: set[str] = set()
    for value in values:
        if value in seen:
            duplicate.add(value)
        seen.add(value)
    return sorted(duplicate)


def _edge_sort_key(edge: str) -> tuple[int, int | str]:
    if edge.startswith("E00") and len(edge) == 4 and edge[-1].isalpha():
        return (0, edge[-1])
    return (1, int(edge[1:]) if edge[1:].isdigit() else 999)


def _schema_issues(instance: Any, schema: Any) -> list[TopologyIssue]:
    validator = Draft202012Validator(schema)
    result: list[TopologyIssue] = []
    for error in sorted(
        validator.iter_errors(instance),
        key=lambda item: (list(item.absolute_path), list(item.absolute_schema_path)),
    ):
        location = "$" + "".join(
            f"[{part}]" if isinstance(part, int) else f".{part}"
            for part in error.absolute_path
        )
        result.append(TopologyIssue("schema", location, error.message))
    return result


def audit_topology(spec: Mapping[str, Any]) -> list[TopologyIssue]:
    """Diagnose a detached mapping against the closed public inventory.

    This diagnostic accepts ordinary mappings so mutated counterexamples can
    be reported.  Enforcement APIs below accept only :class:`FrozenTopology`.
    """

    if isinstance(spec, FrozenTopology):
        spec = spec.to_plain_dict()
    elif not isinstance(spec, Mapping):
        return [TopologyIssue("topology-type", "$", "topology must be a mapping")]

    issues: list[TopologyIssue] = []
    if spec.get("source_sha256") != EXPECTED_SOURCE_SHA256:
        _issue(issues, "source-hashes", "$.source_sha256", "authorized source hash inventory mismatch")
    projection_keys = (
        "role_rows",
        "stores",
        "edges",
        "signer_roles",
        "payload_receipt_split_edges",
        "status",
    )
    try:
        projection = json.dumps(
            {key: spec[key] for key in projection_keys},
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    except (KeyError, TypeError, UnicodeError):
        _issue(issues, "topology-projection", "$", "topology projection is incomplete or unserializable")
    else:
        if sha256_bytes(projection) != EXPECTED_TOPOLOGY_PROJECTION_SHA256:
            _issue(issues, "topology-projection", "$", "frozen topology projection hash mismatch")
    role_rows = spec.get("role_rows", [])
    stores = spec.get("stores", [])
    edges = spec.get("edges", [])
    role_ids = [row.get("id") for row in role_rows if isinstance(row, dict)]
    role_labels = [row.get("label") for row in role_rows if isinstance(row, dict)]
    store_ids = [row.get("id") for row in stores if isinstance(row, dict)]
    edge_ids = [row.get("id") for row in edges if isinstance(row, dict)]

    if tuple(role_ids) != EXPECTED_ROLE_ROWS:
        _issue(issues, "role-inventory", "$.role_rows", "role-row order or identity mismatch")
    if tuple(role_labels) != EXPECTED_ROLE_LABELS:
        _issue(issues, "role-labels", "$.role_rows", "exact role-row labels mismatch")
    if tuple(store_ids) != EXPECTED_STORES:
        _issue(issues, "store-inventory", "$.stores", "store order or identity mismatch")
    if tuple(edge_ids) != expected_edge_ids():
        _issue(issues, "edge-inventory", "$.edges", "edge order or identity mismatch")
    for category, location, values in (
        ("role-duplicate", "$.role_rows", role_ids),
        ("store-duplicate", "$.stores", store_ids),
        ("edge-duplicate", "$.edges", edge_ids),
    ):
        duplicate = _duplicates(values)
        if duplicate:
            _issue(issues, category, location, f"duplicate identifiers: {duplicate}")

    role_map = {
        row["id"]: row
        for row in role_rows
        if isinstance(row, dict) and isinstance(row.get("id"), str)
    }
    edge_set = set(edge_ids)
    role_producers: dict[str, set[str]] = {edge: set() for edge in edge_set}
    role_consumers: dict[str, set[str]] = {edge: set() for edge in edge_set}
    position_count = 0
    paired_count = 0
    for index, row in enumerate(role_rows):
        if not isinstance(row, dict):
            continue
        location = f"$.role_rows[{index}]"
        positions = row.get("positions", [])
        position_count += len(positions)
        if len(positions) == 2:
            paired_count += 1
        if positions not in (["single"], ["A", "B"], ["1", "2"]):
            _issue(issues, "role-position", location + ".positions", "invalid aggregated-row positions")
        for direction, target in (
            ("inbound_edges", role_consumers),
            ("outbound_edges", role_producers),
        ):
            values = row.get(direction, [])
            if _duplicates(values):
                _issue(issues, "role-edge-duplicate", location + "." + direction, "duplicate edge reference")
            if values != sorted(values, key=_edge_sort_key):
                _issue(issues, "role-edge-order", location + "." + direction, "edge references are not in canonical order")
            for edge in values:
                if edge not in edge_set:
                    _issue(issues, "role-edge", location + "." + direction, f"unknown edge: {edge}")
                else:
                    target[edge].add(row["id"])
    if position_count != 40 or paired_count != 8:
        _issue(issues, "role-position-count", "$.role_rows", "expected 40 positions across eight paired rows")

    store_targets: dict[str, set[str]] = {edge: set() for edge in edge_set}
    store_sources: dict[str, set[str]] = {edge: set() for edge in edge_set}

    def validate_access(
        access: dict[str, Any], location: str, edge_target: dict[str, set[str]], store_id: str
    ) -> None:
        role = access.get("role")
        position = access.get("position")
        row = role_map.get(role)
        if row is None:
            _issue(issues, "store-role", location, f"unknown role row: {role}")
            return
        if position not in row.get("positions", []):
            _issue(issues, "store-position", location, "position is not part of the referenced role row")
        route_edges = access.get("edges", [])
        if _duplicates(route_edges):
            _issue(issues, "store-edge-duplicate", location + ".edges", "duplicate edge reference")
        for edge in route_edges:
            if edge not in edge_set:
                _issue(issues, "store-edge", location + ".edges", f"unknown edge: {edge}")
                continue
            incident = set(row.get("inbound_edges", [])) | set(row.get("outbound_edges", []))
            if edge not in incident:
                _issue(issues, "store-role-edge", location + ".edges", f"edge {edge} is not incident to role row {role}")
            edge_target[edge].add(store_id)

    for index, store in enumerate(stores):
        if not isinstance(store, dict):
            continue
        store_id = store.get("id", "")
        validate_access(store.get("writer", {}), f"$.stores[{index}].writer", store_targets, store_id)
        reader_keys: list[tuple[str, str]] = []
        for reader_index, reader in enumerate(store.get("readers", [])):
            validate_access(
                reader,
                f"$.stores[{index}].readers[{reader_index}]",
                store_sources,
                store_id,
            )
            reader_keys.append((reader.get("role"), reader.get("position")))
        if len(reader_keys) != len(set(reader_keys)):
            _issue(issues, "store-reader-duplicate", f"$.stores[{index}].readers", "duplicate role-position reader")

    for edge in sorted(edge_set, key=_edge_sort_key):
        if not role_producers[edge] and not store_sources[edge]:
            _issue(issues, "edge-source", f"$.edges[{edge}]", "edge has no role or store source")
        if not role_consumers[edge] and not store_targets[edge]:
            _issue(issues, "edge-target", f"$.edges[{edge}]", "edge has no role or store target")

    signer_roles = spec.get("signer_roles", [])
    if tuple(signer_roles) != EXPECTED_SIGNER_ROLES:
        _issue(issues, "signer-inventory", "$.signer_roles", "22-entry signer role order or identity mismatch")
    if tuple(spec.get("payload_receipt_split_edges", [])) != EXPECTED_PAYLOAD_RECEIPT_SPLIT_EDGES:
        _issue(
            issues,
            "payload-receipt-split",
            "$.payload_receipt_split_edges",
            "protected-payload/public-receipt split edge inventory mismatch",
        )

    status = spec.get("status", {})
    if tuple(status.get("edge_order", [])) != STATUS_EDGE_ORDER:
        _issue(issues, "status-edge-order", "$.status.edge_order", "status edge order mismatch")
    if tuple(status.get("states", [])) != expected_states():
        _issue(issues, "status-state-order", "$.status.states", "status state order mismatch")
    receipt_rows = status.get("receipts", [])
    receipt_edges = [row.get("edge") for row in receipt_rows if isinstance(row, dict)]
    if tuple(receipt_edges) != STATUS_EDGE_ORDER:
        _issue(issues, "receipt-edge-order", "$.status.receipts", "receipt rows do not biject with status edges")
    total_receipts = 0
    for index, row in enumerate(receipt_rows):
        if not isinstance(row, dict):
            continue
        edge = row.get("edge")
        entries = row.get("entries", [])
        total_receipts += len(entries)
        expected_count = 3 if edge == "E02" else 2 if edge == "E25" else 1
        if len(entries) != expected_count:
            _issue(issues, "receipt-count", f"$.status.receipts[{index}]", f"edge {edge} receipt count mismatch")
        for entry_index, entry in enumerate(entries):
            if entry.get("producer_role") not in signer_roles:
                _issue(issues, "receipt-signer", f"$.status.receipts[{index}].entries[{entry_index}]", "producer is not an active signer role")
    if total_receipts != 17:
        _issue(issues, "receipt-total", "$.status.receipts", "expected exactly 17 receipts")
    edge_kind = {row.get("id"): row.get("kind") for row in edges if isinstance(row, dict)}
    for edge in STATUS_EDGE_ORDER:
        if edge_kind.get(edge) != "status-evidence":
            _issue(issues, "status-edge-kind", "$.edges", f"{edge} must be status-evidence")

    counts = spec.get("counts", {})
    observed_counts = {
        "role_rows": len(role_rows),
        "role_positions": position_count,
        "paired_role_rows": paired_count,
        "stores": len(stores),
        "edge_rows": len(edges),
        "signer_roles": len(signer_roles),
        "status_edges": len(status.get("edge_order", [])),
        "status_states": len(status.get("states", [])),
        "status_receipts": total_receipts,
        "e51_pairs": len(status.get("states", [])),
    }
    if counts != observed_counts:
        _issue(issues, "declared-counts", "$.counts", "declared and observed topology counts differ")
    return sorted(issues)


def require_valid_topology(spec: Mapping[str, Any]) -> None:
    issues = audit_topology(spec)
    if issues:
        first = issues[0]
        raise TopologyError(f"{first.category} at {first.location}: {first.message}")


def load_public_runtime_spec(workspace_root: Path) -> FrozenTopology:
    """Authenticate the pinned namespace and return an immutable capability."""

    grant = bind_external_manifest_grant(
        expected_manifest_path=PUBLIC_SPEC_MANIFEST_PATH,
        expected_manifest_sha256=FROZEN_PUBLIC_SPEC_MANIFEST_SHA256,
        expected_entry_prefix="s0-lab/i1/spec/",
        expected_allowed_paths=PUBLIC_SPEC_ALLOWED_PATHS,
        purpose="i1-public-topology",
    )
    manifest = load_authenticated_manifest(workspace_root, grant)
    files = authenticate_manifest_file_set(workspace_root, manifest)
    spec = parse_strict_json_bytes(files[PUBLIC_SPEC_PATH].raw, require_object=True)
    schema = parse_strict_json_bytes(files[PUBLIC_SPEC_SCHEMA_PATH].raw, require_object=True)
    schema_issues = _schema_issues(spec, schema)
    if schema_issues:
        first = schema_issues[0]
        raise TopologyError(f"{first.category} at {first.location}: {first.message}")
    require_valid_topology(spec)
    snapshot = _deep_freeze(deepcopy(spec))
    return FrozenTopology(
        files[PUBLIC_SPEC_PATH].sha256,
        manifest.manifest.sha256,
        _snapshot_digest(snapshot),
        snapshot,
        _provenance=_TOPOLOGY_PROVENANCE,
    )


def store_read_scope(
    topology: FrozenTopology, role: str, position: str, store_id: str
) -> str | None:
    """Return the explicit read scope or ``None`` (omission is denial)."""

    topology = require_frozen_topology(topology)
    if any(type(value) is not str for value in (role, position, store_id)):
        raise TopologyError("store policy identifiers must be exact strings")
    for store in topology["stores"]:
        if store.get("id") != store_id:
            continue
        for reader in store.get("readers", []):
            if reader.get("role") == role and reader.get("position") == position:
                return reader.get("scope", "full")
        return None
    return None


def require_store_read(
    topology: FrozenTopology,
    role: str,
    position: str,
    store_id: str,
    *,
    scope: str = "full",
) -> None:
    if type(scope) is not str:
        raise TopologyError("store scope must be exact string text")
    allowed = store_read_scope(topology, role, position, store_id)
    if allowed != scope:
        raise TopologyError("cross-role store input is denied")

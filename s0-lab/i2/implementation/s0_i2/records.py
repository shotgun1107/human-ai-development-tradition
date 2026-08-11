"""Canonical public import admission, outcome, and ledger-event records."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field

from .canonical import (
    ZERO64,
    parse_exact_record,
    require_choice,
    require_decimal,
    require_hex64,
    serialize_exact_record,
    sha256_bytes,
)
from .errors import BindingError, CanonicalRecordError


ROOT_ROLE = "control-root-authority"
FROZEN_REGISTRY_ROLE_ORDER = (
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
    ROOT_ROLE,
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
NON_ROOT_SIGNER_ROLES = frozenset(FROZEN_REGISTRY_ROLE_ORDER) - {ROOT_ROLE}

IMPORT_ROUTE_STATES = {
    "preactivation-context-v1": ("key-generated", "pop-context-bound"),
    "registry-binding-v1": ("pop-issued", "registry-bound"),
    "activation-binding-v1": ("registry-bound", "active"),
}
IMPORT_CLASSES = frozenset(IMPORT_ROUTE_STATES)
EVENT_ID_FIELDS = (
    "reserved_media_event_id",
    "admission_frozen_media_event_id",
    "pending_media_event_id",
    "completion_media_event_id",
)

ADMISSION_FIELD_ORDER = (
    "import_admission_schema",
    "authority_id",
    "campaign_id",
    "ceremony_id",
    "signer_id",
    "import_class",
    "from_state",
    "to_state",
    "package_sha256",
    "package_object_id",
    "attachment_capability_id",
    "result_media_kind",
    "result_media_id",
    *EVENT_ID_FIELDS,
    "outcome_schema",
    "outcome_max_bytes",
    "admission_event_id",
    "decision",
)

OUTCOME_FIELD_ORDER = (
    "import_outcome_schema",
    "tcb_service_id",
    "campaign_id",
    "ceremony_id",
    "signer_id",
    "import_class",
    "from_state",
    "to_state",
    "package_sha256",
    "package_object_id",
    "attachment_capability_id",
    "admission_event_id",
    "admission_record_sha256",
    "result_media_kind",
    "result_media_id",
    *EVENT_ID_FIELDS,
    "before_state",
    "after_state",
    "before_configuration_state_sha256",
    "after_configuration_state_sha256",
    "decision",
    "reason",
    "outcome_body_sha256",
)

EVENT_FIELD_ORDER = (
    "signer_media_event_schema",
    "namespace",
    "sequence",
    "previous_event_sha256",
    "event_id",
    "prior_route_event_id",
    "campaign_id",
    "ceremony_id",
    "signer_id",
    "route_kind",
    "route_class",
    "request_id",
    "attachment_capability_id",
    "admission_event_id",
    "admission_record_sha256",
    "media_object_sha256",
    "media_object_id",
    "result_media_id",
    "result_media_kind",
    *EVENT_ID_FIELDS,
    "outcome_schema",
    "outcome_frame_sha256",
    "outcome_class",
    "before_appliance_state",
    "after_appliance_state",
    "state",
    "terminal_from",
    "decision",
)

assert len(ADMISSION_FIELD_ORDER) == 21
assert len(OUTCOME_FIELD_ORDER) == 26
assert len(EVENT_FIELD_ORDER) == 31

_RECORD_PROVENANCE = object()


@dataclass(frozen=True)
class ImportAdmission:
    raw: bytes
    fields: tuple[tuple[str, str], ...]
    record_sha256: str
    _provenance: object = field(repr=False, compare=False)

    def __getitem__(self, field_name: str) -> str:
        return dict(self.fields)[field_name]


@dataclass(frozen=True)
class ImportOutcome:
    raw: bytes
    fields: tuple[tuple[str, str], ...]
    frame_sha256: str
    _provenance: object = field(repr=False, compare=False)

    def __getitem__(self, field_name: str) -> str:
        return dict(self.fields)[field_name]


@dataclass(frozen=True)
class ImportLedgerEvent:
    raw: bytes
    fields: tuple[tuple[str, str], ...]
    event_sha256: str
    sequence: int
    _provenance: object = field(repr=False, compare=False)

    def __getitem__(self, field_name: str) -> str:
        return dict(self.fields)[field_name]


def _require_non_root_signer(value: str) -> None:
    if value not in NON_ROOT_SIGNER_ROLES:
        raise CanonicalRecordError("signer_id is not an exact non-root registry role")


def _require_route_mapping(fields: Mapping[str, str], class_field: str) -> None:
    route_class = require_choice(fields[class_field], class_field, IMPORT_CLASSES)
    source, destination = IMPORT_ROUTE_STATES[route_class]
    if fields["from_state"] != source or fields["to_state"] != destination:
        raise CanonicalRecordError("import class source/destination mapping mismatch")


def _require_common_identifiers(fields: Mapping[str, str]) -> None:
    for name in (
        "campaign_id",
        "ceremony_id",
        "package_sha256",
        "package_object_id",
        "attachment_capability_id",
    ):
        require_hex64(fields[name], name)
    require_hex64(fields["result_media_id"], "result_media_id", nonzero=True)
    ids = tuple(require_hex64(fields[name], name, nonzero=True) for name in EVENT_ID_FIELDS)
    if len(set(ids)) != len(ids):
        raise CanonicalRecordError("preallocated event IDs must be pairwise distinct")


def parse_import_admission(raw: bytes) -> ImportAdmission:
    fields = parse_exact_record(
        raw, ADMISSION_FIELD_ORDER, label="import admission"
    )
    if fields["import_admission_schema"] != "S0-SIGNER-IMPORT-ADMISSION-2":
        raise CanonicalRecordError("wrong import admission schema")
    if fields["authority_id"] != "control-host-preflight":
        raise CanonicalRecordError("wrong import admission authority")
    _require_non_root_signer(fields["signer_id"])
    _require_route_mapping(fields, "import_class")
    _require_common_identifiers(fields)
    if fields["result_media_kind"] != "import-outcome-v1":
        raise CanonicalRecordError("wrong result media kind")
    if fields["outcome_schema"] != "S0-SIGNER-IMPORT-OUTCOME-1":
        raise CanonicalRecordError("wrong import outcome schema binding")
    if fields["outcome_max_bytes"] != "2048":
        raise CanonicalRecordError("outcome_max_bytes must be exactly 2048")
    if fields["admission_event_id"] != fields["admission_frozen_media_event_id"]:
        raise CanonicalRecordError("admission event ID must equal the frozen event ID")
    if fields["decision"] != "approved":
        raise CanonicalRecordError("import admission decision must be approved")
    return ImportAdmission(raw, tuple(fields.items()), sha256_bytes(raw), _RECORD_PROVENANCE)


def serialize_import_admission(values: Mapping[str, object]) -> bytes:
    raw = serialize_exact_record(
        values, ADMISSION_FIELD_ORDER, label="import admission"
    )
    parse_import_admission(raw)
    return raw


def _validate_outcome_tuple(fields: Mapping[str, str]) -> None:
    source, destination = IMPORT_ROUTE_STATES[fields["import_class"]]
    before_hash = fields["before_configuration_state_sha256"]
    after_hash = fields["after_configuration_state_sha256"]
    decision = fields["decision"]
    reason = fields["reason"]
    before = fields["before_state"]
    after = fields["after_state"]

    allowed = False
    if decision == "accepted" and reason == "none":
        allowed = (
            before == source
            and after == destination
            and before_hash != ZERO64
            and after_hash != ZERO64
            and before_hash != after_hash
        )
    elif decision == "rejected" and reason in {
        "parse-rejected",
        "validation-rejected",
    }:
        allowed = (
            before == source
            and after == source
            and before_hash != ZERO64
            and before_hash == after_hash
        )
    elif decision == "rejected" and reason == "state-commit-failed":
        allowed = (
            before == source
            and after == "indeterminate"
            and before_hash != ZERO64
            and after_hash == ZERO64
        )
    if not allowed:
        raise CanonicalRecordError("outcome decision/reason/state/hash tuple is invalid")


def parse_import_outcome(raw: bytes) -> ImportOutcome:
    fields = parse_exact_record(
        raw, OUTCOME_FIELD_ORDER, label="import outcome", max_bytes=2048
    )
    if fields["import_outcome_schema"] != "S0-SIGNER-IMPORT-OUTCOME-1":
        raise CanonicalRecordError("wrong import outcome schema")
    if fields["tcb_service_id"] != "S0-IMPORT-TRANSITION-TCB-1":
        raise CanonicalRecordError("wrong TCB import service")
    _require_non_root_signer(fields["signer_id"])
    _require_route_mapping(fields, "import_class")
    _require_common_identifiers(fields)
    for name in ("admission_event_id", "admission_record_sha256"):
        require_hex64(fields[name], name)
    if fields["admission_event_id"] != fields["admission_frozen_media_event_id"]:
        raise CanonicalRecordError("outcome admission event binding mismatch")
    if fields["result_media_kind"] != "import-outcome-v1":
        raise CanonicalRecordError("wrong result media kind")
    for name in (
        "before_configuration_state_sha256",
        "after_configuration_state_sha256",
        "outcome_body_sha256",
    ):
        require_hex64(fields[name], name)
    require_choice(fields["decision"], "decision", frozenset({"accepted", "rejected"}))
    require_choice(
        fields["reason"],
        "reason",
        frozenset({
            "none",
            "parse-rejected",
            "validation-rejected",
            "state-commit-failed",
        }),
    )
    body = serialize_exact_record(
        {name: fields[name] for name in OUTCOME_FIELD_ORDER[:-1]},
        OUTCOME_FIELD_ORDER[:-1],
        label="import outcome body",
    )
    if sha256_bytes(body) != fields["outcome_body_sha256"]:
        raise CanonicalRecordError("outcome body hash mismatch")
    _validate_outcome_tuple(fields)
    return ImportOutcome(raw, tuple(fields.items()), sha256_bytes(raw), _RECORD_PROVENANCE)


def serialize_import_outcome(values_without_body_hash: Mapping[str, object]) -> bytes:
    if not isinstance(values_without_body_hash, Mapping):
        raise CanonicalRecordError("import outcome values must be a mapping")
    expected = set(OUTCOME_FIELD_ORDER[:-1])
    if set(values_without_body_hash) != expected:
        raise CanonicalRecordError("import outcome body fields do not match the schema")
    body = serialize_exact_record(
        values_without_body_hash,
        OUTCOME_FIELD_ORDER[:-1],
        label="import outcome body",
    )
    values = dict(values_without_body_hash)
    values["outcome_body_sha256"] = sha256_bytes(body)
    raw = serialize_exact_record(values, OUTCOME_FIELD_ORDER, label="import outcome")
    parse_import_outcome(raw)
    return raw


def parse_import_event(raw: bytes) -> ImportLedgerEvent:
    fields = parse_exact_record(raw, EVENT_FIELD_ORDER, label="import ledger event")
    if fields["signer_media_event_schema"] != "S0-SIGNER-MEDIA-LEDGER-IMPORT-EVENT-1":
        raise CanonicalRecordError("wrong import ledger-event schema")
    if fields["namespace"] != "signer-media":
        raise CanonicalRecordError("wrong ledger namespace")
    sequence = require_decimal(fields["sequence"], "sequence")
    previous = require_hex64(fields["previous_event_sha256"], "previous_event_sha256")
    if (sequence == 0) != (previous == ZERO64):
        raise CanonicalRecordError("global predecessor zero rule mismatch")
    for name in (
        "event_id",
        "prior_route_event_id",
        "campaign_id",
        "ceremony_id",
        "attachment_capability_id",
        "admission_event_id",
        "admission_record_sha256",
        "media_object_sha256",
        "media_object_id",
        "outcome_frame_sha256",
    ):
        require_hex64(fields[name], name)
    _require_non_root_signer(fields["signer_id"])
    if fields["route_kind"] != "import" or fields["request_id"] != ZERO64:
        raise CanonicalRecordError("import route constants mismatch")
    require_choice(fields["route_class"], "route_class", IMPORT_CLASSES)
    require_hex64(fields["result_media_id"], "result_media_id", nonzero=True)
    if fields["result_media_kind"] != "import-outcome-v1":
        raise CanonicalRecordError("wrong result media kind")
    ids = tuple(require_hex64(fields[name], name, nonzero=True) for name in EVENT_ID_FIELDS)
    if len(set(ids)) != len(ids):
        raise CanonicalRecordError("preallocated event IDs must be pairwise distinct")
    if fields["outcome_schema"] != "S0-SIGNER-IMPORT-OUTCOME-1":
        raise CanonicalRecordError("wrong outcome schema binding")
    require_choice(
        fields["outcome_class"],
        "outcome_class",
        frozenset({
            "none",
            "accepted",
            "parse-rejected",
            "validation-rejected",
            "state-commit-failed",
            "crash",
            "missing",
            "duplicate",
            "disagreement",
        }),
    )
    require_choice(
        fields["before_appliance_state"],
        "before_appliance_state",
        frozenset({"none", "key-generated", "pop-issued", "registry-bound"}),
    )
    require_choice(
        fields["after_appliance_state"],
        "after_appliance_state",
        frozenset({
            "none",
            "key-generated",
            "pop-context-bound",
            "pop-issued",
            "registry-bound",
            "active",
            "indeterminate",
        }),
    )
    require_choice(
        fields["state"],
        "state",
        frozenset({"reserved", "admission-frozen", "pending", "consumed", "terminal"}),
    )
    require_choice(
        fields["terminal_from"],
        "terminal_from",
        frozenset({"none", "reserved", "admission-frozen", "pending"}),
    )
    require_choice(
        fields["decision"],
        "decision",
        frozenset({"reserved", "approved", "executing", "accepted", "rejected"}),
    )
    return ImportLedgerEvent(
        raw, tuple(fields.items()), sha256_bytes(raw), sequence, _RECORD_PROVENANCE
    )


def serialize_import_event(values: Mapping[str, object]) -> bytes:
    raw = serialize_exact_record(values, EVENT_FIELD_ORDER, label="import ledger event")
    parse_import_event(raw)
    return raw


def require_import_admission(value: object) -> ImportAdmission:
    if type(value) is not ImportAdmission or value._provenance is not _RECORD_PROVENANCE:
        raise BindingError("import admission is not an authenticated parsed handle")
    parsed = parse_import_admission(value.raw)
    if parsed.fields != value.fields or parsed.record_sha256 != value.record_sha256:
        raise BindingError("import admission handle changed after parsing")
    return value


def require_import_outcome(value: object) -> ImportOutcome:
    if type(value) is not ImportOutcome or value._provenance is not _RECORD_PROVENANCE:
        raise BindingError("import outcome is not an authenticated parsed handle")
    parsed = parse_import_outcome(value.raw)
    if parsed.fields != value.fields or parsed.frame_sha256 != value.frame_sha256:
        raise BindingError("import outcome handle changed after parsing")
    return value


def require_import_event(value: object) -> ImportLedgerEvent:
    if type(value) is not ImportLedgerEvent or value._provenance is not _RECORD_PROVENANCE:
        raise BindingError("import event is not an authenticated parsed handle")
    parsed = parse_import_event(value.raw)
    if (
        parsed.fields != value.fields
        or parsed.event_sha256 != value.event_sha256
        or parsed.sequence != value.sequence
    ):
        raise BindingError("import event handle changed after parsing")
    return value


def validate_outcome_binding(outcome: ImportOutcome, admission: ImportAdmission) -> None:
    require_import_outcome(outcome)
    require_import_admission(admission)
    bindings = {
        "campaign_id": "campaign_id",
        "ceremony_id": "ceremony_id",
        "signer_id": "signer_id",
        "import_class": "import_class",
        "from_state": "from_state",
        "to_state": "to_state",
        "package_sha256": "package_sha256",
        "package_object_id": "package_object_id",
        "attachment_capability_id": "attachment_capability_id",
        "admission_event_id": "admission_event_id",
        "result_media_kind": "result_media_kind",
        "result_media_id": "result_media_id",
        "reserved_media_event_id": "reserved_media_event_id",
        "admission_frozen_media_event_id": "admission_frozen_media_event_id",
        "pending_media_event_id": "pending_media_event_id",
        "completion_media_event_id": "completion_media_event_id",
    }
    for outcome_name, admission_name in bindings.items():
        if outcome[outcome_name] != admission[admission_name]:
            raise BindingError(f"outcome/admission binding mismatch: {outcome_name}")
    if outcome["admission_record_sha256"] != admission.record_sha256:
        raise BindingError("outcome admission record hash mismatch")

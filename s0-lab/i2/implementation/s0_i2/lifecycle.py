"""Fail-closed outcome classification and import-route lifecycle checks."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field

from .canonical import ZERO64, require_hex64, sha256_bytes
from .errors import BindingError, CanonicalRecordError, LifecycleError
from .records import (
    EVENT_ID_FIELDS,
    IMPORT_ROUTE_STATES,
    ImportAdmission,
    ImportLedgerEvent,
    ImportOutcome,
    parse_import_outcome,
    require_import_admission,
    require_import_event,
    validate_outcome_binding,
)


_CLASSIFICATION_PROVENANCE = object()


@dataclass(frozen=True)
class OutcomeClassification:
    outcome_class: str
    frame_sha256: str
    frame: ImportOutcome | None
    _provenance: object = field(repr=False, compare=False)


def _classification(
    outcome_class: str, frame_sha256: str, frame: ImportOutcome | None
) -> OutcomeClassification:
    return OutcomeClassification(
        outcome_class, frame_sha256, frame, _CLASSIFICATION_PROVENANCE
    )


def classify_outcome_medium(
    raw_medium: bytes,
    admission: ImportAdmission,
    *,
    abnormal_end: bool,
    outcome_media_count: int = 1,
    host_evidence_agrees: bool = True,
    anti_replay_agrees: bool = True,
) -> OutcomeClassification:
    """Apply the frozen classification precedence to one 2,048-byte medium."""

    try:
        require_import_admission(admission)
    except BindingError as exc:
        raise CanonicalRecordError(str(exc)) from exc
    for value, label in (
        (abnormal_end, "abnormal_end"),
        (host_evidence_agrees, "host_evidence_agrees"),
        (anti_replay_agrees, "anti_replay_agrees"),
    ):
        if type(value) is not bool:
            raise CanonicalRecordError(f"{label} must be exact Boolean")
    if type(outcome_media_count) is not int or isinstance(outcome_media_count, bool):
        raise CanonicalRecordError("outcome_media_count must be an exact integer")
    if outcome_media_count < 0:
        raise CanonicalRecordError("outcome_media_count cannot be negative")
    if type(raw_medium) is not bytes:
        raise CanonicalRecordError("raw outcome medium must be exact bytes")

    if abnormal_end:
        return _classification("crash", ZERO64, None)
    if outcome_media_count == 0:
        return _classification("missing", ZERO64, None)
    if outcome_media_count > 1:
        return _classification("duplicate", ZERO64, None)
    if len(raw_medium) != 2048:
        return _classification("disagreement", ZERO64, None)
    if raw_medium == b"\x00" * 2048:
        return _classification("missing", ZERO64, None)

    zero_at = raw_medium.find(b"\x00")
    if zero_at == -1:
        frame_bytes = raw_medium
        tail = b""
    else:
        frame_bytes = raw_medium[:zero_at]
        tail = raw_medium[zero_at:]
    if any(tail):
        return _classification("duplicate", ZERO64, None)
    if frame_bytes.count(b"import_outcome_schema=") > 1:
        return _classification("duplicate", ZERO64, None)
    if not frame_bytes or not frame_bytes.endswith(b"\n"):
        return _classification("missing", ZERO64, None)

    try:
        frame = parse_import_outcome(frame_bytes)
    except CanonicalRecordError:
        return _classification("disagreement", ZERO64, None)

    try:
        validate_outcome_binding(frame, admission)
    except BindingError:
        return _classification("disagreement", frame.frame_sha256, frame)
    if not host_evidence_agrees or not anti_replay_agrees:
        return _classification("disagreement", frame.frame_sha256, frame)
    outcome_class = (
        "accepted" if frame["decision"] == "accepted" else frame["reason"]
    )
    return _classification(outcome_class, frame.frame_sha256, frame)


def validate_event_global_link(
    event: ImportLedgerEvent,
    *,
    expected_sequence: int,
    expected_previous_event_sha256: str,
) -> None:
    """Verify one event against separately supplied global-ledger evidence."""

    try:
        require_import_event(event)
    except BindingError as exc:
        raise LifecycleError(str(exc)) from exc
    if type(expected_sequence) is not int or isinstance(expected_sequence, bool):
        raise LifecycleError("expected sequence must be an exact integer")
    if expected_sequence < 0:
        raise LifecycleError("expected sequence cannot be negative")
    try:
        require_hex64(expected_previous_event_sha256, "expected previous event hash")
    except CanonicalRecordError as exc:
        raise LifecycleError(str(exc)) from exc
    if event.sequence != expected_sequence:
        raise LifecycleError("global ledger sequence mismatch")
    if event["previous_event_sha256"] != expected_previous_event_sha256:
        raise LifecycleError("global ledger predecessor hash mismatch")


def _admission_tuple(event: ImportLedgerEvent) -> tuple[str, str, str, str]:
    return (
        event["admission_event_id"],
        event["admission_record_sha256"],
        event["media_object_sha256"],
        event["media_object_id"],
    )


def _variant(event: ImportLedgerEvent, admission: ImportAdmission) -> str:
    source, destination = IMPORT_ROUTE_STATES[admission["import_class"]]
    values = (
        event["event_id"],
        event["prior_route_event_id"],
        _admission_tuple(event),
        event["outcome_frame_sha256"],
        event["outcome_class"],
        event["before_appliance_state"],
        event["after_appliance_state"],
        event["state"],
        event["terminal_from"],
        event["decision"],
    )
    r = admission["reserved_media_event_id"]
    a = admission["admission_frozen_media_event_id"]
    p = admission["pending_media_event_id"]
    c = admission["completion_media_event_id"]
    adm0 = (ZERO64, ZERO64, ZERO64, ZERO64)
    adm1 = (a, admission.record_sha256, admission["package_sha256"], admission["package_object_id"])

    fixed: dict[str, tuple[object, ...]] = {
        "reserved": (r, ZERO64, adm0, ZERO64, "none", "none", "none", "reserved", "none", "reserved"),
        "admission-frozen": (a, r, adm1, ZERO64, "none", "none", "none", "admission-frozen", "none", "approved"),
        "pending": (p, a, adm1, ZERO64, "none", source, "none", "pending", "none", "executing"),
        "direct-terminal-reserved": (c, r, adm0, ZERO64, "none", "none", "none", "terminal", "reserved", "rejected"),
        "direct-terminal-admission-frozen": (c, a, adm1, ZERO64, "none", "none", "none", "terminal", "admission-frozen", "rejected"),
    }
    for name, expected in fixed.items():
        if values == expected:
            return name

    completion = values[:3] + values[4:]
    completion_rows: dict[str, tuple[object, ...]] = {
        "accepted": (c, p, adm1, "accepted", source, destination, "consumed", "none", "accepted"),
        "parse-rejected": (c, p, adm1, "parse-rejected", source, source, "terminal", "pending", "rejected"),
        "validation-rejected": (c, p, adm1, "validation-rejected", source, source, "terminal", "pending", "rejected"),
        "state-commit-failed": (c, p, adm1, "state-commit-failed", source, "indeterminate", "terminal", "pending", "rejected"),
        "crash": (c, p, adm1, "crash", source, "indeterminate", "terminal", "pending", "rejected"),
        "missing": (c, p, adm1, "missing", source, "indeterminate", "terminal", "pending", "rejected"),
        "duplicate": (c, p, adm1, "duplicate", source, "indeterminate", "terminal", "pending", "rejected"),
        "disagreement": (c, p, adm1, "disagreement", source, "indeterminate", "terminal", "pending", "rejected"),
    }
    for name, expected in completion_rows.items():
        if completion == expected:
            frame_hash = event["outcome_frame_sha256"]
            if name in {"accepted", "parse-rejected", "validation-rejected", "state-commit-failed"} and frame_hash == ZERO64:
                continue
            if name in {"crash", "missing", "duplicate"} and frame_hash != ZERO64:
                continue
            return name
    raise LifecycleError("event does not match exactly one frozen lifecycle variant")


def _require_event_bindings(event: ImportLedgerEvent, admission: ImportAdmission) -> None:
    pairs = {
        "campaign_id": "campaign_id",
        "ceremony_id": "ceremony_id",
        "signer_id": "signer_id",
        "route_class": "import_class",
        "attachment_capability_id": "attachment_capability_id",
        "result_media_id": "result_media_id",
        "result_media_kind": "result_media_kind",
        "reserved_media_event_id": "reserved_media_event_id",
        "admission_frozen_media_event_id": "admission_frozen_media_event_id",
        "pending_media_event_id": "pending_media_event_id",
        "completion_media_event_id": "completion_media_event_id",
        "outcome_schema": "outcome_schema",
    }
    for event_name, admission_name in pairs.items():
        if event[event_name] != admission[admission_name]:
            raise BindingError(f"event/admission binding mismatch: {event_name}")


def validate_import_route(
    events: Sequence[ImportLedgerEvent],
    admission: ImportAdmission,
    *,
    outcome: OutcomeClassification | None = None,
) -> tuple[ImportLedgerEvent, ...]:
    """Validate route-local records; global links must also be checked separately."""

    try:
        require_import_admission(admission)
    except BindingError as exc:
        raise LifecycleError(str(exc)) from exc
    if isinstance(events, (str, bytes)):
        raise LifecycleError("events must be an ordered parsed-event sequence")
    normalized = tuple(events)
    if not normalized or any(type(event) is not ImportLedgerEvent for event in normalized):
        raise LifecycleError("events must be exact parsed import events")
    try:
        for event in normalized:
            require_import_event(event)
    except BindingError as exc:
        raise LifecycleError(str(exc)) from exc
    if len({event["event_id"] for event in normalized}) != len(normalized):
        raise LifecycleError("route event ID reuse is forbidden")

    variants: list[str] = []
    previous_route_id = ZERO64
    for event in normalized:
        _require_event_bindings(event, admission)
        if event["prior_route_event_id"] != previous_route_id:
            raise LifecycleError("route predecessor event ID mismatch")
        variants.append(_variant(event, admission))
        previous_route_id = event["event_id"]

    path = tuple(variants)
    early_paths = {
        ("reserved", "direct-terminal-reserved"),
        ("reserved", "admission-frozen", "direct-terminal-admission-frozen"),
    }
    completed_prefix = ("reserved", "admission-frozen", "pending")
    if path in early_paths:
        if outcome is not None:
            raise LifecycleError("pre-pending terminal must not claim an outcome classification")
        return normalized
    if len(path) != 4 or path[:3] != completed_prefix:
        raise LifecycleError("route lifecycle path is forbidden")
    if (
        type(outcome) is not OutcomeClassification
        or outcome._provenance is not _CLASSIFICATION_PROVENANCE
    ):
        raise LifecycleError("post-pending completion requires exact outcome classification")

    completion = normalized[-1]
    if path[-1] != outcome.outcome_class:
        raise LifecycleError("completion class does not match host classification")
    if completion["outcome_frame_sha256"] != outcome.frame_sha256:
        raise LifecycleError("completion frame hash does not match host classification")
    if outcome.frame is not None:
        validate_outcome_binding(outcome.frame, admission)
    if outcome.outcome_class == "accepted" and completion["state"] != "consumed":
        raise LifecycleError("accepted outcome requires durable consumed completion")
    if outcome.outcome_class != "accepted" and completion["state"] != "terminal":
        raise LifecycleError("non-accepted outcome must be terminal")
    return normalized

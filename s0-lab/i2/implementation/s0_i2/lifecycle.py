"""Structural import-event lifecycle and supplied-trace chain checks.

These checks deliberately do not claim durable ledger state, witness evidence,
or semantic outcome correctness.  They validate only authenticated public
event bytes and explicit caller-supplied structural context.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import NoReturn

from .canonical import (
    ZERO64,
    decimal_successor,
    normalize_decimal,
    require_hex64,
)
from .errors import BindingError, CanonicalRecordError, LifecycleError, UnsupportedBoundaryError
from .records import (
    EVENT_ID_FIELDS,
    IMPORT_ROUTE_STATES,
    ImportLedgerEvent,
    SignerRegistryContext,
    require_import_event,
    require_signer_registry_context,
)


_ROUTE_CONTEXT_PROVENANCE = object()


@dataclass(frozen=True)
class ImportRouteContext:
    """Explicit immutable bindings needed for structural route validation."""

    signer_context: SignerRegistryContext
    campaign_id: str
    ceremony_id: str
    signer_id: str
    route_class: str
    attachment_capability_id: str
    admission_record_sha256: str
    media_object_sha256: str
    media_object_id: str
    result_media_id: str
    reserved_media_event_id: str
    admission_frozen_media_event_id: str
    pending_media_event_id: str
    completion_media_event_id: str
    _provenance: object = field(repr=False, compare=False)


def bind_import_route_context(
    *,
    signer_context: SignerRegistryContext,
    campaign_id: str,
    ceremony_id: str,
    signer_id: str,
    route_class: str,
    attachment_capability_id: str,
    admission_record_sha256: str,
    media_object_sha256: str,
    media_object_id: str,
    result_media_id: str,
    reserved_media_event_id: str,
    admission_frozen_media_event_id: str,
    pending_media_event_id: str,
    completion_media_event_id: str,
) -> ImportRouteContext:
    context = require_signer_registry_context(signer_context)
    if type(signer_id) is not str or signer_id not in context.non_root_signer_role_order:
        raise BindingError("route signer is not an authenticated non-root registry role")
    if type(route_class) is not str or route_class not in IMPORT_ROUTE_STATES:
        raise BindingError("route class is outside the authenticated vocabulary")
    values = {
        "campaign_id": campaign_id,
        "ceremony_id": ceremony_id,
        "attachment_capability_id": attachment_capability_id,
        "admission_record_sha256": admission_record_sha256,
        "media_object_sha256": media_object_sha256,
        "media_object_id": media_object_id,
        "result_media_id": result_media_id,
        "reserved_media_event_id": reserved_media_event_id,
        "admission_frozen_media_event_id": admission_frozen_media_event_id,
        "pending_media_event_id": pending_media_event_id,
        "completion_media_event_id": completion_media_event_id,
    }
    try:
        for name, value in values.items():
            require_hex64(
                value,
                name,
                nonzero=name == "result_media_id" or name in EVENT_ID_FIELDS,
            )
    except CanonicalRecordError as exc:
        raise BindingError(str(exc)) from exc
    event_ids = tuple(values[name] for name in EVENT_ID_FIELDS)
    if len(set(event_ids)) != len(event_ids):
        raise BindingError("preallocated route event IDs must be pairwise distinct")
    if result_media_id in event_ids:
        raise BindingError(
            "result_media_id must not collide with a preallocated route event ID"
        )
    return ImportRouteContext(
        context,
        campaign_id,
        ceremony_id,
        signer_id,
        route_class,
        attachment_capability_id,
        admission_record_sha256,
        media_object_sha256,
        media_object_id,
        result_media_id,
        reserved_media_event_id,
        admission_frozen_media_event_id,
        pending_media_event_id,
        completion_media_event_id,
        _ROUTE_CONTEXT_PROVENANCE,
    )


def require_import_route_context(value: object) -> ImportRouteContext:
    if (
        type(value) is not ImportRouteContext
        or value._provenance is not _ROUTE_CONTEXT_PROVENANCE
    ):
        raise BindingError("import route context is not an authenticated handle")
    rebound = bind_import_route_context(
        signer_context=value.signer_context,
        campaign_id=value.campaign_id,
        ceremony_id=value.ceremony_id,
        signer_id=value.signer_id,
        route_class=value.route_class,
        attachment_capability_id=value.attachment_capability_id,
        admission_record_sha256=value.admission_record_sha256,
        media_object_sha256=value.media_object_sha256,
        media_object_id=value.media_object_id,
        result_media_id=value.result_media_id,
        reserved_media_event_id=value.reserved_media_event_id,
        admission_frozen_media_event_id=value.admission_frozen_media_event_id,
        pending_media_event_id=value.pending_media_event_id,
        completion_media_event_id=value.completion_media_event_id,
    )
    if rebound != value:
        raise BindingError("import route context changed after binding")
    return value


def classify_outcome_medium(*_args: object, **_kwargs: object) -> NoReturn:
    """Fail closed: the exact outcome grammar/classifier is not authenticated."""

    raise UnsupportedBoundaryError(
        "BLOCKED: complete-outcome-classification is not authenticated by the public v0.3 inputs"
    )


def validate_durable_ledger(*_args: object, **_kwargs: object) -> NoReturn:
    raise UnsupportedBoundaryError(
        "BLOCKED: durable-ledger is outside the public v0.3 implementation boundary"
    )


def validate_witness(*_args: object, **_kwargs: object) -> NoReturn:
    raise UnsupportedBoundaryError(
        "BLOCKED: witness-validation is outside the public v0.3 implementation boundary"
    )


def validate_event_global_link(
    event: ImportLedgerEvent,
    *,
    expected_sequence: str | int,
    expected_previous_event_sha256: str,
) -> None:
    """Check one event against separately supplied predecessor evidence."""

    try:
        require_import_event(event)
        sequence = normalize_decimal(expected_sequence, "expected sequence")
        previous = require_hex64(
            expected_previous_event_sha256, "expected previous event hash"
        )
    except (BindingError, CanonicalRecordError) as exc:
        raise LifecycleError(str(exc)) from exc
    if event.sequence != sequence:
        raise LifecycleError("global ledger sequence mismatch")
    if event["previous_event_sha256"] != previous:
        raise LifecycleError("global ledger predecessor hash mismatch")


def validate_event_global_chain(
    events: Sequence[ImportLedgerEvent],
    *,
    expected_start_sequence: str | int,
    expected_previous_event_sha256: str,
) -> tuple[ImportLedgerEvent, ...]:
    """Validate a contiguous chain inside only the supplied in-memory trace."""

    if isinstance(events, (str, bytes)):
        raise LifecycleError("events must be an ordered parsed-event sequence")
    normalized = tuple(events)
    if not normalized:
        raise LifecycleError("global event trace must be non-empty")
    try:
        sequence = normalize_decimal(expected_start_sequence, "expected start sequence")
        previous = require_hex64(
            expected_previous_event_sha256, "expected previous event hash"
        )
    except CanonicalRecordError as exc:
        raise LifecycleError(str(exc)) from exc
    seen_event_ids: set[str] = set()
    for event in normalized:
        if type(event) is not ImportLedgerEvent:
            raise LifecycleError("events must be exact parsed import events")
        validate_event_global_link(
            event,
            expected_sequence=sequence,
            expected_previous_event_sha256=previous,
        )
        if event["event_id"] in seen_event_ids:
            raise LifecycleError("event ID reuse within supplied trace is forbidden")
        seen_event_ids.add(event["event_id"])
        sequence = decimal_successor(sequence, "expected sequence")
        previous = event.event_sha256
    return normalized


def _admission_tuple(event: ImportLedgerEvent) -> tuple[str, str, str, str]:
    return (
        event["admission_event_id"],
        event["admission_record_sha256"],
        event["media_object_sha256"],
        event["media_object_id"],
    )


def _require_event_bindings(
    event: ImportLedgerEvent, context: ImportRouteContext
) -> None:
    expected = {
        "campaign_id": context.campaign_id,
        "ceremony_id": context.ceremony_id,
        "signer_id": context.signer_id,
        "route_class": context.route_class,
        "attachment_capability_id": context.attachment_capability_id,
        "result_media_id": context.result_media_id,
        "result_media_kind": "import-outcome-v1",
        "reserved_media_event_id": context.reserved_media_event_id,
        "admission_frozen_media_event_id": context.admission_frozen_media_event_id,
        "pending_media_event_id": context.pending_media_event_id,
        "completion_media_event_id": context.completion_media_event_id,
        "outcome_schema": "S0-SIGNER-IMPORT-OUTCOME-1",
    }
    for field_name, expected_value in expected.items():
        if event[field_name] != expected_value:
            raise BindingError(f"event/route binding mismatch: {field_name}")


def classify_event_variant(
    event: ImportLedgerEvent, context: ImportRouteContext
) -> str:
    """Classify one event's structural lifecycle tuple, not its outcome truth."""

    try:
        route = require_import_route_context(context)
        require_import_event(event, signer_context=route.signer_context)
        _require_event_bindings(event, route)
    except (BindingError, CanonicalRecordError) as exc:
        raise LifecycleError(str(exc)) from exc

    source, destination = IMPORT_ROUTE_STATES[route.route_class]
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
    reserved = route.reserved_media_event_id
    admission_frozen = route.admission_frozen_media_event_id
    pending = route.pending_media_event_id
    completion = route.completion_media_event_id
    admission_zero = (ZERO64, ZERO64, ZERO64, ZERO64)
    admission_bound = (
        admission_frozen,
        route.admission_record_sha256,
        route.media_object_sha256,
        route.media_object_id,
    )
    fixed: dict[str, tuple[object, ...]] = {
        "reserved": (
            reserved,
            ZERO64,
            admission_zero,
            ZERO64,
            "none",
            "none",
            "none",
            "reserved",
            "none",
            "reserved",
        ),
        "admission-frozen": (
            admission_frozen,
            reserved,
            admission_bound,
            ZERO64,
            "none",
            "none",
            "none",
            "admission-frozen",
            "none",
            "approved",
        ),
        "pending": (
            pending,
            admission_frozen,
            admission_bound,
            ZERO64,
            "none",
            source,
            "none",
            "pending",
            "none",
            "executing",
        ),
        "direct-terminal-reserved": (
            completion,
            reserved,
            admission_zero,
            ZERO64,
            "none",
            "none",
            "none",
            "terminal",
            "reserved",
            "rejected",
        ),
        "direct-terminal-admission-frozen": (
            completion,
            admission_frozen,
            admission_bound,
            ZERO64,
            "none",
            "none",
            "none",
            "terminal",
            "admission-frozen",
            "rejected",
        ),
    }
    for name, expected in fixed.items():
        if values == expected:
            return name

    without_frame_hash = values[:3] + values[4:]
    completion_rows: dict[str, tuple[object, ...]] = {
        "accepted": (
            completion,
            pending,
            admission_bound,
            "accepted",
            source,
            destination,
            "consumed",
            "none",
            "accepted",
        ),
        "parse-rejected": (
            completion,
            pending,
            admission_bound,
            "parse-rejected",
            source,
            source,
            "terminal",
            "pending",
            "rejected",
        ),
        "validation-rejected": (
            completion,
            pending,
            admission_bound,
            "validation-rejected",
            source,
            source,
            "terminal",
            "pending",
            "rejected",
        ),
        "state-commit-failed": (
            completion,
            pending,
            admission_bound,
            "state-commit-failed",
            source,
            "indeterminate",
            "terminal",
            "pending",
            "rejected",
        ),
        "crash": (
            completion,
            pending,
            admission_bound,
            "crash",
            source,
            "indeterminate",
            "terminal",
            "pending",
            "rejected",
        ),
        "missing": (
            completion,
            pending,
            admission_bound,
            "missing",
            source,
            "indeterminate",
            "terminal",
            "pending",
            "rejected",
        ),
        "duplicate": (
            completion,
            pending,
            admission_bound,
            "duplicate",
            source,
            "indeterminate",
            "terminal",
            "pending",
            "rejected",
        ),
        "disagreement": (
            completion,
            pending,
            admission_bound,
            "disagreement",
            source,
            "indeterminate",
            "terminal",
            "pending",
            "rejected",
        ),
    }
    for name, expected in completion_rows.items():
        if without_frame_hash != expected:
            continue
        frame_hash = event["outcome_frame_sha256"]
        if name in {
            "accepted",
            "parse-rejected",
            "validation-rejected",
            "state-commit-failed",
        } and frame_hash == ZERO64:
            continue
        if name in {"crash", "missing", "duplicate"} and frame_hash != ZERO64:
            continue
        return name
    raise LifecycleError("event does not match exactly one frozen lifecycle variant")


def validate_import_route(
    events: Sequence[ImportLedgerEvent],
    context: ImportRouteContext,
) -> tuple[ImportLedgerEvent, ...]:
    """Validate an exact terminal R/A/P/C path inside the supplied trace."""

    try:
        route = require_import_route_context(context)
    except (BindingError, CanonicalRecordError) as exc:
        raise LifecycleError(str(exc)) from exc
    if isinstance(events, (str, bytes)):
        raise LifecycleError("events must be an ordered parsed-event sequence")
    normalized = tuple(events)
    if not normalized or any(type(event) is not ImportLedgerEvent for event in normalized):
        raise LifecycleError("events must be exact parsed import events")
    try:
        for event in normalized:
            require_import_event(event, signer_context=route.signer_context)
    except (BindingError, CanonicalRecordError) as exc:
        raise LifecycleError(str(exc)) from exc
    event_ids = tuple(event["event_id"] for event in normalized)
    if len(set(event_ids)) != len(event_ids):
        raise LifecycleError("route event ID reuse within supplied trace is forbidden")

    variants: list[str] = []
    expected_prior_route_id = ZERO64
    for event in normalized:
        variant = classify_event_variant(event, route)
        if event["prior_route_event_id"] != expected_prior_route_id:
            raise LifecycleError("route predecessor event ID mismatch")
        variants.append(variant)
        expected_prior_route_id = event["event_id"]

    path = tuple(variants)
    allowed_early_paths = {
        ("reserved", "direct-terminal-reserved"),
        ("reserved", "admission-frozen", "direct-terminal-admission-frozen"),
    }
    completion_variants = {
        "accepted",
        "parse-rejected",
        "validation-rejected",
        "state-commit-failed",
        "crash",
        "missing",
        "duplicate",
        "disagreement",
    }
    if path in allowed_early_paths:
        return normalized
    if (
        len(path) == 4
        and path[:3] == ("reserved", "admission-frozen", "pending")
        and path[3] in completion_variants
    ):
        return normalized
    raise LifecycleError("route lifecycle path is forbidden")


def _route_identity(context: ImportRouteContext) -> tuple[object, ...]:
    """Return the complete supplied-scope immutable route identity."""

    return (
        context.signer_context.manifest_sha256,
        context.signer_context.registry_role_order,
        context.campaign_id,
        context.ceremony_id,
        context.signer_id,
        context.route_class,
        context.attachment_capability_id,
        context.admission_record_sha256,
        context.media_object_sha256,
        context.media_object_id,
        context.result_media_id,
        context.reserved_media_event_id,
        context.admission_frozen_media_event_id,
        context.pending_media_event_id,
        context.completion_media_event_id,
    )


def validate_supplied_route_set(
    route_groups: Sequence[
        tuple[ImportRouteContext, Sequence[ImportLedgerEvent]]
    ],
) -> tuple[tuple[ImportRouteContext, tuple[ImportLedgerEvent, ...]], ...]:
    """Validate single-owner route and identifier bindings in this supplied set.

    Every immutable route identity may occur exactly once.  Each route owns
    exactly five supplied-scope identifiers: its result-media ID and its four
    preallocated event IDs.  All five must be disjoint from every other route,
    including IDs not emitted by an early-terminal route.  Emitted event IDs
    are also checked independently across the supplied set.  This is not
    project-lifetime uniqueness or durable registry authority.
    """

    if isinstance(route_groups, (str, bytes)):
        raise LifecycleError("route groups must be an ordered sequence")
    groups = tuple(route_groups)
    if not groups:
        raise LifecycleError("supplied route set must be non-empty")

    validated: list[tuple[ImportRouteContext, tuple[ImportLedgerEvent, ...]]] = []
    seen_route_identities: set[tuple[object, ...]] = set()
    identifier_owners: dict[str, tuple[object, ...]] = {}
    emitted_event_ids: set[str] = set()
    for group in groups:
        if (
            isinstance(group, (str, bytes))
            or not isinstance(group, Sequence)
            or len(group) != 2
        ):
            raise LifecycleError("each route group must be a context/events pair")
        context, events = group
        try:
            route = require_import_route_context(context)
        except (BindingError, CanonicalRecordError) as exc:
            raise LifecycleError(str(exc)) from exc
        normalized_events = validate_import_route(events, route)
        identity = _route_identity(route)
        if identity in seen_route_identities:
            raise LifecycleError(
                "immutable route identity occurs more than once in supplied set"
            )
        seen_route_identities.add(identity)

        route_identifiers = (
            route.result_media_id,
            route.reserved_media_event_id,
            route.admission_frozen_media_event_id,
            route.pending_media_event_id,
            route.completion_media_event_id,
        )
        for identifier in route_identifiers:
            prior_identity = identifier_owners.get(identifier)
            if prior_identity is not None:
                raise LifecycleError(
                    "result-media or preallocated event identifier overlaps a distinct supplied route"
                )
            identifier_owners[identifier] = identity

        for event in normalized_events:
            event_id = event["event_id"]
            if event_id in emitted_event_ids:
                raise LifecycleError(
                    "emitted event ID reuse across supplied routes is forbidden"
                )
            emitted_event_ids.add(event_id)
        validated.append((route, normalized_events))
    return tuple(validated)

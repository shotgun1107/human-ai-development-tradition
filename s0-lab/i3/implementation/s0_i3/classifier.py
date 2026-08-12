"""Total ordered public classification for one supplied import attempt."""

from __future__ import annotations

from dataclasses import dataclass, field

from s0_i2.errors import I2Error
from s0_i2.lifecycle import ImportRouteContext, require_import_route_context
from s0_i2.records import IMPORT_ROUTE_STATES, SignerRegistryContext

from .errors import I3BindingError, I3Error, I3InputError
from .models import ImportClassification, make_classification
from .records import (
    OUTCOME_MEDIA_BYTES,
    OUTCOME_SCHEMA_PREFIX,
    ZERO64,
    ImportAdmission,
    ImportOutcome,
    parse_import_admission,
    parse_import_outcome_frame,
    route_bindings_from_admission,
    route_bindings_from_outcome,
    validate_outcome_binding,
)


PHASES = frozenset({"reserved", "admission-frozen", "pending"})
END_OBSERVATIONS = frozenset({"not-started", "normal", "abnormal", "unknown"})
EVIDENCE_STATUSES = frozenset({"exact", "conflict", "unavailable"})
STATUS_FIELDS = (
    "launch_admission_status",
    "iso_attachment_status",
    "outcome_medium_status",
    "detachment_and_raw_read_status",
    "route_event_binding_status",
    "anti_replay_status",
    "host_state_status",
    "ledger_witness_snapshot_status",
)
_FACT_PROVENANCE = object()
_MISSING = object()


@dataclass(frozen=True)
class ClassificationFactSet:
    last_durable_phase: str
    end_observation: str
    outcome_media_observations: tuple[bytes, ...]
    launch_admission_status: str
    iso_attachment_status: str
    outcome_medium_status: str
    detachment_and_raw_read_status: str
    route_event_binding_status: str
    anti_replay_status: str
    host_state_status: str
    ledger_witness_snapshot_status: str
    _provenance: object = field(repr=False, compare=False)


@dataclass(frozen=True)
class _MediumScan:
    count: int
    medium_exact: bool
    all_zero: bool
    schema_prefix_count: int
    complete_at_zero: bool
    complete_candidate_count: int
    candidate_at_zero_end: int | None
    nonzero_tail: bool
    canonical_outcome: ImportOutcome | None


def _closed_text(value: object, label: str, domain: frozenset[str]) -> str:
    if type(value) is not str or value not in domain:
        raise I3InputError(f"{label} is outside its closed typed domain")
    return value


def bind_classification_fact_set(
    *,
    last_durable_phase: object = _MISSING,
    end_observation: object = _MISSING,
    outcome_media_observations: object = _MISSING,
    launch_admission_status: object = _MISSING,
    iso_attachment_status: object = _MISSING,
    outcome_medium_status: object = _MISSING,
    detachment_and_raw_read_status: object = _MISSING,
    route_event_binding_status: object = _MISSING,
    anti_replay_status: object = _MISSING,
    host_state_status: object = _MISSING,
    ledger_witness_snapshot_status: object = _MISSING,
    **unexpected: object,
) -> ClassificationFactSet:
    supplied_values = (
        last_durable_phase,
        end_observation,
        outcome_media_observations,
        launch_admission_status,
        iso_attachment_status,
        outcome_medium_status,
        detachment_and_raw_read_status,
        route_event_binding_status,
        anti_replay_status,
        host_state_status,
        ledger_witness_snapshot_status,
    )
    if unexpected or any(value is _MISSING for value in supplied_values):
        raise I3InputError("fact set has missing or unknown members")
    phase = _closed_text(last_durable_phase, "last_durable_phase", PHASES)
    end = _closed_text(end_observation, "end_observation", END_OBSERVATIONS)
    if type(outcome_media_observations) not in (tuple, list):
        raise I3InputError(
            "outcome_media_observations must be an eager tuple or list, not scalar bytes or a lazy producer"
        )
    media = tuple(outcome_media_observations)
    if any(type(member) is not bytes for member in media):
        raise I3InputError("every outcome media observation must be exact bytes")
    supplied = {
        "launch_admission_status": launch_admission_status,
        "iso_attachment_status": iso_attachment_status,
        "outcome_medium_status": outcome_medium_status,
        "detachment_and_raw_read_status": detachment_and_raw_read_status,
        "route_event_binding_status": route_event_binding_status,
        "anti_replay_status": anti_replay_status,
        "host_state_status": host_state_status,
        "ledger_witness_snapshot_status": ledger_witness_snapshot_status,
    }
    statuses = {
        name: _closed_text(value, name, EVIDENCE_STATUSES)
        for name, value in supplied.items()
    }
    return ClassificationFactSet(
        phase,
        end,
        media,
        *(statuses[name] for name in STATUS_FIELDS),
        _FACT_PROVENANCE,
    )


def require_classification_fact_set(value: object) -> ClassificationFactSet:
    if (
        type(value) is not ClassificationFactSet
        or value._provenance is not _FACT_PROVENANCE
    ):
        raise I3InputError("fact set is not an authenticated I3 handle")
    rebound = bind_classification_fact_set(
        last_durable_phase=value.last_durable_phase,
        end_observation=value.end_observation,
        outcome_media_observations=value.outcome_media_observations,
        **{name: getattr(value, name) for name in STATUS_FIELDS},
    )
    if rebound != value:
        raise I3InputError("fact set changed after binding")
    return value


def _line_block_end(raw: bytes, offset: int, line_count: int) -> int | None:
    position = offset
    for _ in range(line_count):
        position = raw.find(b"\n", position)
        if position < 0:
            return None
        position += 1
    return position


def _prefix_positions(raw: bytes) -> tuple[int, ...]:
    positions: list[int] = []
    start = 0
    while True:
        position = raw.find(OUTCOME_SCHEMA_PREFIX, start)
        if position < 0:
            return tuple(positions)
        positions.append(position)
        start = position + 1


def _scan_medium(
    media: tuple[bytes, ...], *, signer_context: SignerRegistryContext
) -> _MediumScan:
    if len(media) != 1:
        return _MediumScan(len(media), False, False, 0, False, 0, None, False, None)
    raw = media[0]
    exact = len(raw) == OUTCOME_MEDIA_BYTES
    positions = _prefix_positions(raw)
    complete_at_zero_end = _line_block_end(raw, 0, 26)
    complete_candidates = tuple(
        (offset, end)
        for offset in positions
        if (end := _line_block_end(raw, offset, 26)) is not None
    )
    candidate_zero_end = next(
        (end for offset, end in complete_candidates if offset == 0), None
    )
    nonzero_tail = (
        candidate_zero_end is not None
        and any(byte != 0 for byte in raw[candidate_zero_end:])
    )
    canonical: ImportOutcome | None = None
    if (
        exact
        and positions == (0,)
        and len(complete_candidates) == 1
        and candidate_zero_end is not None
        and not nonzero_tail
    ):
        try:
            canonical = parse_import_outcome_frame(
                raw[:candidate_zero_end], signer_context=signer_context
            )
        except I3Error:
            canonical = None
    return _MediumScan(
        1,
        exact,
        all(byte == 0 for byte in raw),
        len(positions),
        complete_at_zero_end is not None,
        len(complete_candidates),
        candidate_zero_end,
        nonzero_tail,
        canonical,
    )


def _try_admission(
    raw: bytes | None, *, signer_context: SignerRegistryContext
) -> ImportAdmission | None:
    if raw is None:
        return None
    try:
        return parse_import_admission(raw, signer_context=signer_context)
    except I3Error:
        return None


def _status_values(facts: ClassificationFactSet) -> tuple[str, ...]:
    return tuple(getattr(facts, name) for name in STATUS_FIELDS)


def _route_from_optional(
    admission: ImportAdmission | None,
) -> tuple[tuple[str, str], ...] | None:
    return None if admission is None else route_bindings_from_admission(admission)


def _route_from_context(context: ImportRouteContext) -> tuple[tuple[str, str], ...]:
    source, destination = IMPORT_ROUTE_STATES[context.route_class]
    return (
        ("campaign_id", context.campaign_id),
        ("ceremony_id", context.ceremony_id),
        ("signer_id", context.signer_id),
        ("route_class", context.route_class),
        ("from_state", source),
        ("to_state", destination),
        ("attachment_capability_id", context.attachment_capability_id),
        ("admission_record_sha256", context.admission_record_sha256),
        ("media_object_sha256", context.media_object_sha256),
        ("media_object_id", context.media_object_id),
        ("result_media_id", context.result_media_id),
        ("reserved_media_event_id", context.reserved_media_event_id),
        ("admission_frozen_media_event_id", context.admission_frozen_media_event_id),
        ("pending_media_event_id", context.pending_media_event_id),
        ("completion_media_event_id", context.completion_media_event_id),
    )


def _pending_result(
    *,
    row: str,
    outcome_class: str,
    frame_hash: str,
    source: str,
    after: str,
    route_bindings: tuple[tuple[str, str], ...] | None,
) -> ImportClassification:
    required = "consumed-accepted" if outcome_class == "accepted" else "terminal-rejected"
    return make_classification(
        selected_row=row,
        last_durable_phase="pending",
        outcome_class=outcome_class,
        outcome_frame_sha256=frame_hash,
        before_appliance_state=source,
        after_appliance_state=after,
        required_completion_kind=required,
        route_bindings=route_bindings,
    )


def classify_import_attempt(
    admission_bytes: bytes | None,
    facts: ClassificationFactSet,
    *,
    route_context: ImportRouteContext,
    **unexpected: object,
) -> ImportClassification:
    """Classify one fully supplied fact set using the frozen row precedence."""

    if unexpected:
        raise I3InputError("classification has an unknown or separate count argument")
    if admission_bytes is not None and type(admission_bytes) is not bytes:
        raise I3InputError("admission evidence must be absent or exact bytes")
    try:
        route = require_import_route_context(route_context)
    except I2Error as exc:
        raise I3InputError("route_context is not an authenticated I2 handle") from exc
    signer_context = route.signer_context
    expected_route = _route_from_context(route)
    expected_route_map = dict(expected_route)
    fact_set = require_classification_fact_set(facts)
    admission = _try_admission(admission_bytes, signer_context=signer_context)
    admission_route = _route_from_optional(admission)

    if fact_set.last_durable_phase == "reserved":
        return make_classification(
            selected_row="PRE-R",
            last_durable_phase="reserved",
            outcome_class="none",
            outcome_frame_sha256=ZERO64,
            before_appliance_state="none",
            after_appliance_state="none",
            required_completion_kind="direct-terminal-reserved",
            route_bindings=expected_route,
        )
    if fact_set.last_durable_phase == "admission-frozen":
        return make_classification(
            selected_row="PRE-A",
            last_durable_phase="admission-frozen",
            outcome_class="none",
            outcome_frame_sha256=ZERO64,
            before_appliance_state="none",
            after_appliance_state="none",
            required_completion_kind="direct-terminal-admission-frozen",
            route_bindings=expected_route,
        )

    scan = _scan_medium(
        fact_set.outcome_media_observations, signer_context=signer_context
    )
    source = expected_route_map["from_state"]
    if fact_set.end_observation == "abnormal":
        return _pending_result(
            row="P-CRASH",
            outcome_class="crash",
            frame_hash=ZERO64,
            source=source,
            after="indeterminate",
            route_bindings=expected_route,
        )

    duplicate = (
        scan.count > 1
        or scan.schema_prefix_count > 1
        or scan.complete_candidate_count > 1
        or (scan.candidate_at_zero_end is not None and scan.nonzero_tail)
    )
    missing = (
        fact_set.end_observation == "normal"
        and scan.count == 1
        and scan.medium_exact
        and not duplicate
        and (
            scan.all_zero
            or (not scan.complete_at_zero and scan.complete_candidate_count == 0)
        )
    )
    if missing:
        return _pending_result(
            row="P-MISSING",
            outcome_class="missing",
            frame_hash=ZERO64,
            source=source,
            after="indeterminate",
            route_bindings=expected_route,
        )
    if duplicate:
        return _pending_result(
            row="P-DUPLICATE",
            outcome_class="duplicate",
            frame_hash=ZERO64,
            source=source,
            after="indeterminate",
            route_bindings=expected_route,
        )

    outcome = scan.canonical_outcome
    if outcome is not None:
        outcome_route = route_bindings_from_outcome(outcome)
        bindings_exact = False
        if admission is not None:
            try:
                validate_outcome_binding(
                    outcome, admission, signer_context=signer_context
                )
                bindings_exact = (
                    admission_route == expected_route
                    and outcome_route == expected_route
                )
            except I3BindingError:
                bindings_exact = False
        external_exact = (
            fact_set.end_observation == "normal"
            and bindings_exact
            and all(value == "exact" for value in _status_values(fact_set))
        )
        if not external_exact:
            return _pending_result(
                row="P-DISAGREE-H",
                outcome_class="disagreement",
                frame_hash=outcome.outcome_frame_sha256,
                source=expected_route_map["from_state"],
                after="indeterminate",
                route_bindings=expected_route,
            )
        row_by_class = {
            "parse-rejected": "P-PARSE-REJECTED",
            "validation-rejected": "P-VALIDATION-REJECTED",
            "state-commit-failed": "P-STATE-COMMIT-FAILED",
            "accepted": "P-ACCEPTED",
        }
        after_by_class = {
            "parse-rejected": outcome["from_state"],
            "validation-rejected": outcome["from_state"],
            "state-commit-failed": "indeterminate",
            "accepted": outcome["to_state"],
        }
        return _pending_result(
            row=row_by_class[outcome.outcome_class],
            outcome_class=outcome.outcome_class,
            frame_hash=outcome.outcome_frame_sha256,
            source=outcome["from_state"],
            after=after_by_class[outcome.outcome_class],
            route_bindings=expected_route,
        )

    return _pending_result(
        row="P-DISAGREE-Z",
        outcome_class="disagreement",
        frame_hash=ZERO64,
        source=source,
        after="indeterminate",
        route_bindings=expected_route,
    )

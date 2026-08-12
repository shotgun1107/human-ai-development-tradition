"""Pure completion-event matching against the unchanged public I2 codec."""

from __future__ import annotations

from s0_i2 import (
    bind_import_route_context,
    classify_event_variant,
    parse_import_event,
    validate_event_global_link,
)
from s0_i2.errors import I2Error
from s0_i2.records import SignerRegistryContext

from .errors import I3EventError, I3InputError
from .models import (
    ImportClassification,
    ImportDecision,
    make_decision,
    require_classification,
)


APPEND_STATUSES = frozenset({"persisted", "conflict", "unavailable", "failed"})


def _event_variant_for(classification: ImportClassification) -> str:
    if classification.last_durable_phase == "reserved":
        return "direct-terminal-reserved"
    if classification.last_durable_phase == "admission-frozen":
        return "direct-terminal-admission-frozen"
    return classification.outcome_class


def validate_completion_event(
    classification: ImportClassification,
    event_bytes: bytes,
    *,
    signer_context: SignerRegistryContext,
    expected_sequence: str | int | None,
    expected_previous_event_sha256: str | None,
) -> None:
    result = require_classification(classification)
    if type(event_bytes) is not bytes:
        raise I3InputError("completion event must be exact bytes")
    if result.route_bindings is None:
        raise I3EventError("classification has no canonical route evidence")
    route = dict(result.route_bindings)
    try:
        context = bind_import_route_context(
            signer_context=signer_context,
            campaign_id=route["campaign_id"],
            ceremony_id=route["ceremony_id"],
            signer_id=route["signer_id"],
            route_class=route["route_class"],
            attachment_capability_id=route["attachment_capability_id"],
            admission_record_sha256=route["admission_record_sha256"],
            media_object_sha256=route["media_object_sha256"],
            media_object_id=route["media_object_id"],
            result_media_id=route["result_media_id"],
            reserved_media_event_id=route["reserved_media_event_id"],
            admission_frozen_media_event_id=route[
                "admission_frozen_media_event_id"
            ],
            pending_media_event_id=route["pending_media_event_id"],
            completion_media_event_id=route["completion_media_event_id"],
        )
        event = parse_import_event(event_bytes, signer_context=signer_context)
        validate_event_global_link(
            event,
            expected_sequence=expected_sequence,
            expected_previous_event_sha256=expected_previous_event_sha256,
        )
        variant = classify_event_variant(event, context)
    except (I2Error, KeyError) as exc:
        raise I3EventError("completion event is noncanonical or route-incompatible") from exc
    if variant != _event_variant_for(result):
        raise I3EventError("completion event class does not match classification")
    exact = {
        "outcome_frame_sha256": result.outcome_frame_sha256,
        "outcome_class": result.outcome_class,
        "before_appliance_state": result.before_appliance_state,
        "after_appliance_state": result.after_appliance_state,
    }
    for name, expected in exact.items():
        if event[name] != expected:
            raise I3EventError(f"completion event mismatch: {name}")


def finalize_import_attempt(
    classification: ImportClassification,
    event_bytes: bytes | None,
    append_status: str,
    *,
    signer_context: SignerRegistryContext,
    expected_sequence: str | int | None = None,
    expected_previous_event_sha256: str | None = None,
) -> ImportDecision:
    result = require_classification(classification)
    if type(append_status) is not str or append_status not in APPEND_STATUSES:
        raise I3InputError("append_status is outside its closed typed domain")
    if event_bytes is not None and type(event_bytes) is not bytes:
        raise I3InputError("completion event must be absent or exact bytes")
    if append_status != "persisted" or event_bytes is None:
        return make_decision("no-completion-claim")
    try:
        validate_completion_event(
            result,
            event_bytes,
            signer_context=signer_context,
            expected_sequence=expected_sequence,
            expected_previous_event_sha256=expected_previous_event_sha256,
        )
    except I3EventError:
        return make_decision("no-completion-claim")
    if result.outcome_class == "accepted":
        return make_decision(
            "consumed-accepted",
            destination_authority="available",
            destination_state=result.after_appliance_state,
        )
    return make_decision("terminal-rejected")

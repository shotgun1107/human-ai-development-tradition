"""Immutable in-memory models for public I3 classification and finalization."""

from __future__ import annotations

from dataclasses import dataclass, field

from .errors import I3BindingError


_CLASSIFICATION_PROVENANCE = object()
_DECISION_PROVENANCE = object()


@dataclass(frozen=True)
class ImportClassification:
    selected_row: str
    last_durable_phase: str
    outcome_class: str
    outcome_frame_sha256: str
    before_appliance_state: str
    after_appliance_state: str
    required_completion_kind: str
    destination_authority: str
    route_bindings: tuple[tuple[str, str], ...] | None
    _provenance: object = field(repr=False, compare=False)

    def route_value(self, name: str) -> str:
        if self.route_bindings is None:
            raise I3BindingError("classification has no canonical route evidence")
        try:
            return dict(self.route_bindings)[name]
        except KeyError as exc:
            raise I3BindingError("classification route binding is incomplete") from exc


@dataclass(frozen=True)
class ImportDecision:
    disposition: str
    destination_authority: str
    destination_state: str
    _provenance: object = field(repr=False, compare=False)


def make_classification(
    *,
    selected_row: str,
    last_durable_phase: str,
    outcome_class: str,
    outcome_frame_sha256: str,
    before_appliance_state: str,
    after_appliance_state: str,
    required_completion_kind: str,
    route_bindings: tuple[tuple[str, str], ...] | None,
) -> ImportClassification:
    return ImportClassification(
        selected_row,
        last_durable_phase,
        outcome_class,
        outcome_frame_sha256,
        before_appliance_state,
        after_appliance_state,
        required_completion_kind,
        "unavailable",
        route_bindings,
        _CLASSIFICATION_PROVENANCE,
    )


def require_classification(value: object) -> ImportClassification:
    if (
        type(value) is not ImportClassification
        or value._provenance is not _CLASSIFICATION_PROVENANCE
    ):
        raise I3BindingError("classification is not an authenticated I3 handle")
    return value


def make_decision(
    disposition: str,
    *,
    destination_authority: str = "unavailable",
    destination_state: str = "unavailable",
) -> ImportDecision:
    return ImportDecision(
        disposition,
        destination_authority,
        destination_state,
        _DECISION_PROVENANCE,
    )


def require_decision(value: object) -> ImportDecision:
    if type(value) is not ImportDecision or value._provenance is not _DECISION_PROVENANCE:
        raise I3BindingError("decision is not an authenticated I3 handle")
    return value

"""Authenticated public context and canonical 31-line import events.

The public v0.4 input set authenticates the import-event grammar.  It does not
authenticate complete admission or outcome grammars, so those entry points are
kept as explicit fail-closed boundaries rather than inferred implementations.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import NoReturn

from .canonical import (
    ZERO64,
    parse_exact_record,
    require_choice,
    require_decimal,
    require_hex64,
    serialize_exact_record,
    sha256_bytes,
)
from .errors import BindingError, CanonicalRecordError, UnsupportedBoundaryError


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
NON_ROOT_SIGNER_ROLE_ORDER = tuple(
    role for role in FROZEN_REGISTRY_ROLE_ORDER if role != ROOT_ROLE
)
NON_ROOT_SIGNER_ROLES = frozenset(NON_ROOT_SIGNER_ROLE_ORDER)

I1_PUBLIC_RUNTIME_MANIFEST_SHA256 = (
    "9fdffa48994626f63527ee6eceff9825f2df45f91dec12889362ee180d94245e"
)

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
assert len(EVENT_FIELD_ORDER) == 31

UNSUPPORTED_BOUNDARIES = frozenset(
    {
        "import-admission-exact-grammar",
        "import-outcome-exact-grammar",
        "complete-outcome-classification",
        "durable-ledger",
        "project-lifetime-uniqueness",
        "atomic-append",
        "witness-validation",
        "actual-registry-authority",
        "provider-or-platform-enforcement",
    }
)

_CONTEXT_PROVENANCE = object()
_RECORD_PROVENANCE = object()


@dataclass(frozen=True)
class SignerRegistryContext:
    """Handle bound to the exact public I1 manifest and signer inventory."""

    manifest_sha256: str
    registry_role_order: tuple[str, ...]
    non_root_signer_role_order: tuple[str, ...]
    _provenance: object = field(repr=False, compare=False)


@dataclass(frozen=True)
class ImportLedgerEvent:
    raw: bytes
    fields: tuple[tuple[str, str], ...]
    event_sha256: str
    sequence: str
    _signer_context: SignerRegistryContext = field(repr=False, compare=False)
    _provenance: object = field(repr=False, compare=False)

    def __getitem__(self, field_name: str) -> str:
        return dict(self.fields)[field_name]

    @property
    def signer_context(self) -> SignerRegistryContext:
        return self._signer_context


def bind_public_i1_signer_context(
    *,
    manifest_sha256: str,
    registry_role_order: Sequence[str],
) -> SignerRegistryContext:
    """Bind the exact public I1 manifest identity and its 22 registry roles.

    This is a public identity/topology binding, not key possession, signature
    verification, process isolation, or runtime authorization.
    """

    try:
        require_hex64(manifest_sha256, "I1 public runtime manifest SHA-256")
    except CanonicalRecordError as exc:
        raise BindingError(str(exc)) from exc
    if manifest_sha256 != I1_PUBLIC_RUNTIME_MANIFEST_SHA256:
        raise BindingError("I1 public runtime manifest SHA-256 mismatch")
    if isinstance(registry_role_order, (str, bytes)):
        raise BindingError("registry roles must be an exact ordered sequence")
    normalized = tuple(registry_role_order)
    if any(type(role) is not str for role in normalized):
        raise BindingError("registry roles must contain exact strings")
    if normalized != FROZEN_REGISTRY_ROLE_ORDER:
        raise BindingError("I1 registry role identity or order mismatch")
    return SignerRegistryContext(
        manifest_sha256,
        normalized,
        NON_ROOT_SIGNER_ROLE_ORDER,
        _CONTEXT_PROVENANCE,
    )


def require_signer_registry_context(value: object) -> SignerRegistryContext:
    if (
        type(value) is not SignerRegistryContext
        or value._provenance is not _CONTEXT_PROVENANCE
    ):
        raise BindingError("signer registry context is not an authenticated handle")
    rebound = bind_public_i1_signer_context(
        manifest_sha256=value.manifest_sha256,
        registry_role_order=value.registry_role_order,
    )
    if (
        rebound.registry_role_order != value.registry_role_order
        or rebound.non_root_signer_role_order != value.non_root_signer_role_order
    ):
        raise BindingError("signer registry context changed after binding")
    return value


def _require_non_root_signer(
    value: object, signer_context: SignerRegistryContext
) -> str:
    context = require_signer_registry_context(signer_context)
    if type(value) is not str or value not in context.non_root_signer_role_order:
        raise CanonicalRecordError(
            "signer_id is not an authenticated non-root I1 registry role"
        )
    return value


def _blocked(boundary: str) -> NoReturn:
    raise UnsupportedBoundaryError(
        f"BLOCKED: {boundary} is not authenticated by the public v0.4 inputs"
    )


def parse_import_admission(_raw: bytes) -> NoReturn:
    _blocked("import-admission-exact-grammar")


def serialize_import_admission(_values: Mapping[str, object]) -> NoReturn:
    _blocked("import-admission-exact-grammar")


def parse_import_outcome(_raw: bytes) -> NoReturn:
    _blocked("import-outcome-exact-grammar")


def serialize_import_outcome(_values: Mapping[str, object]) -> NoReturn:
    _blocked("import-outcome-exact-grammar")


def validate_outcome_binding(_outcome: object, _admission: object) -> NoReturn:
    _blocked("import-outcome-exact-grammar")


def validate_complete_import(*_args: object, **_kwargs: object) -> NoReturn:
    _blocked("durable-ledger")


def parse_import_event(
    raw: bytes, *, signer_context: SignerRegistryContext
) -> ImportLedgerEvent:
    """Parse the authenticated exact 31-line ASCII/LF import-event record."""

    context = require_signer_registry_context(signer_context)
    fields = parse_exact_record(raw, EVENT_FIELD_ORDER, label="import ledger event")
    if fields["signer_media_event_schema"] != "S0-SIGNER-MEDIA-LEDGER-IMPORT-EVENT-1":
        raise CanonicalRecordError("wrong import ledger-event schema")
    if fields["namespace"] != "signer-media":
        raise CanonicalRecordError("wrong ledger namespace")
    sequence = require_decimal(fields["sequence"], "sequence")
    previous = require_hex64(fields["previous_event_sha256"], "previous_event_sha256")
    if (sequence == "0") != (previous == ZERO64):
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
    _require_non_root_signer(fields["signer_id"], context)
    if fields["route_kind"] != "import" or fields["request_id"] != ZERO64:
        raise CanonicalRecordError("import route constants mismatch")
    require_choice(fields["route_class"], "route_class", IMPORT_CLASSES)
    require_hex64(fields["result_media_id"], "result_media_id", nonzero=True)
    if fields["result_media_kind"] != "import-outcome-v1":
        raise CanonicalRecordError("wrong result media kind")
    ids = tuple(
        require_hex64(fields[name], name, nonzero=True) for name in EVENT_ID_FIELDS
    )
    if len(set(ids)) != len(ids):
        raise CanonicalRecordError("preallocated event IDs must be pairwise distinct")
    if fields["result_media_id"] in ids:
        raise CanonicalRecordError(
            "result_media_id must not collide with a preallocated event ID"
        )
    if fields["outcome_schema"] != "S0-SIGNER-IMPORT-OUTCOME-1":
        raise CanonicalRecordError("wrong outcome schema binding")
    require_choice(
        fields["outcome_class"],
        "outcome_class",
        frozenset(
            {
                "none",
                "accepted",
                "parse-rejected",
                "validation-rejected",
                "state-commit-failed",
                "crash",
                "missing",
                "duplicate",
                "disagreement",
            }
        ),
    )
    require_choice(
        fields["before_appliance_state"],
        "before_appliance_state",
        frozenset({"none", "key-generated", "pop-issued", "registry-bound"}),
    )
    require_choice(
        fields["after_appliance_state"],
        "after_appliance_state",
        frozenset(
            {
                "none",
                "key-generated",
                "pop-context-bound",
                "pop-issued",
                "registry-bound",
                "active",
                "indeterminate",
            }
        ),
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
        raw,
        tuple(fields.items()),
        sha256_bytes(raw),
        sequence,
        context,
        _RECORD_PROVENANCE,
    )


def serialize_import_event(
    values: Mapping[str, object], *, signer_context: SignerRegistryContext
) -> bytes:
    raw = serialize_exact_record(values, EVENT_FIELD_ORDER, label="import ledger event")
    parse_import_event(raw, signer_context=signer_context)
    return raw


def import_event_sha256(
    raw: bytes, *, signer_context: SignerRegistryContext
) -> str:
    """Hash only after the bytes pass the authenticated event parser."""

    return parse_import_event(raw, signer_context=signer_context).event_sha256


def require_import_event(
    value: object, *, signer_context: SignerRegistryContext | None = None
) -> ImportLedgerEvent:
    if type(value) is not ImportLedgerEvent or value._provenance is not _RECORD_PROVENANCE:
        raise BindingError("import event is not an authenticated parsed handle")
    bound_context = require_signer_registry_context(value.signer_context)
    if signer_context is not None:
        supplied_context = require_signer_registry_context(signer_context)
        if (
            supplied_context.manifest_sha256 != bound_context.manifest_sha256
            or supplied_context.registry_role_order != bound_context.registry_role_order
        ):
            raise BindingError("event signer context mismatch")
    parsed = parse_import_event(value.raw, signer_context=bound_context)
    if (
        parsed.fields != value.fields
        or parsed.event_sha256 != value.event_sha256
        or parsed.sequence != value.sequence
    ):
        raise BindingError("import event handle changed after parsing")
    return value

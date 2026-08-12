"""Exact 21-line admission and 26-line outcome codecs for public I3."""

from __future__ import annotations

import hashlib
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field

from s0_i2.errors import BindingError as I2BindingError
from s0_i2.records import (
    IMPORT_ROUTE_STATES,
    NON_ROOT_SIGNER_ROLES,
    SignerRegistryContext,
    require_signer_registry_context,
)

from .errors import (
    I3BindingError,
    I3ByteError,
    I3FieldError,
    I3HashError,
    I3RouteError,
    I3TupleError,
    I3ValueError,
)


ZERO64 = "0" * 64
HEX64 = re.compile(r"^[0-9a-f]{64}$")
ADMISSION_SCHEMA = "S0-SIGNER-IMPORT-ADMISSION-2"
OUTCOME_SCHEMA = "S0-SIGNER-IMPORT-OUTCOME-1"
OUTCOME_SCHEMA_PREFIX = (
    b"import_outcome_schema=S0-SIGNER-IMPORT-OUTCOME-1\n"
)
OUTCOME_MEDIA_BYTES = 2048

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
    "reserved_media_event_id",
    "admission_frozen_media_event_id",
    "pending_media_event_id",
    "completion_media_event_id",
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
    "reserved_media_event_id",
    "admission_frozen_media_event_id",
    "pending_media_event_id",
    "completion_media_event_id",
    "before_state",
    "after_state",
    "before_configuration_state_sha256",
    "after_configuration_state_sha256",
    "decision",
    "reason",
    "outcome_body_sha256",
)
EVENT_ID_FIELDS = (
    "reserved_media_event_id",
    "admission_frozen_media_event_id",
    "pending_media_event_id",
    "completion_media_event_id",
)
COMMON_BINDING_FIELDS = (
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
)

_ADMISSION_PROVENANCE = object()
_OUTCOME_PROVENANCE = object()


@dataclass(frozen=True)
class ImportAdmission:
    raw: bytes
    fields: tuple[tuple[str, str], ...]
    admission_record_sha256: str
    signer_context: SignerRegistryContext = field(repr=False, compare=False)
    _provenance: object = field(repr=False, compare=False)

    def __getitem__(self, name: str) -> str:
        return dict(self.fields)[name]


@dataclass(frozen=True)
class ImportOutcome:
    raw: bytes
    fields: tuple[tuple[str, str], ...]
    outcome_body_sha256: str
    outcome_frame_sha256: str
    outcome_class: str
    signer_context: SignerRegistryContext = field(repr=False, compare=False)
    _provenance: object = field(repr=False, compare=False)

    def __getitem__(self, name: str) -> str:
        return dict(self.fields)[name]


def _context(value: object) -> SignerRegistryContext:
    try:
        return require_signer_registry_context(value)
    except I2BindingError as exc:
        raise I3BindingError(str(exc)) from exc


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _parse_record(
    raw: object,
    order: Sequence[str],
    *,
    label: str,
    max_bytes: int | None = None,
) -> dict[str, str]:
    if type(raw) is not bytes:
        raise I3ByteError(f"{label} must be exact bytes")
    if not raw:
        raise I3ByteError(f"{label} must be non-empty")
    if max_bytes is not None and len(raw) > max_bytes:
        raise I3ByteError(f"{label} exceeds {max_bytes} bytes")
    if raw.startswith(b"\xef\xbb\xbf"):
        raise I3ByteError(f"{label} contains a UTF-8 BOM")
    if b"\r" in raw:
        raise I3ByteError(f"{label} must be LF-only")
    if b"\x00" in raw:
        raise I3ByteError(f"{label} contains NUL")
    if not raw.endswith(b"\n"):
        raise I3ByteError(f"{label} must end with LF")
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise I3ByteError(f"{label} must be ASCII") from exc
    lines = text[:-1].split("\n")
    if any(not line for line in lines):
        raise I3ByteError(f"{label} contains a blank line")
    if any(line.endswith((" ", "\t")) for line in lines):
        raise I3ByteError(f"{label} contains trailing whitespace")
    if len(lines) != len(order):
        raise I3FieldError(f"{label} must contain exactly {len(order)} fields")
    result: dict[str, str] = {}
    for index, (line, expected) in enumerate(zip(lines, order, strict=True), 1):
        if "=" not in line:
            raise I3FieldError(f"{label} line {index} has no field separator")
        name, value = line.split("=", 1)
        if name != expected:
            raise I3FieldError(f"{label} line {index} must be {expected}")
        if not value:
            raise I3FieldError(f"{label} field {expected} is empty")
        result[name] = value
    return result


def _serialize(values: Mapping[str, object], order: Sequence[str], label: str) -> bytes:
    if not isinstance(values, Mapping):
        raise I3FieldError(f"{label} values must be a mapping")
    if len(values) != len(order) or set(values) != set(order):
        raise I3FieldError(f"{label} fields do not match the exact schema")
    lines: list[str] = []
    for name in order:
        value = values[name]
        if type(value) is not str:
            raise I3ValueError(f"{name} must be exact string text")
        if not value or any(character in value for character in ("\n", "\r", "\x00")):
            raise I3ByteError(f"{name} cannot be serialized canonically")
        if value.endswith((" ", "\t")):
            raise I3ByteError(f"{name} has trailing whitespace")
        lines.append(f"{name}={value}")
    try:
        return ("\n".join(lines) + "\n").encode("ascii")
    except UnicodeEncodeError as exc:
        raise I3ByteError(f"{label} must be ASCII") from exc


def _hex(value: str, name: str, *, nonzero: bool = False) -> str:
    if not HEX64.fullmatch(value):
        raise I3ValueError(f"{name} must be 64 lowercase hexadecimal characters")
    if nonzero and value == ZERO64:
        raise I3ValueError(f"{name} must be nonzero")
    return value


def _signer(value: str, context: SignerRegistryContext) -> str:
    _context(context)
    if value not in NON_ROOT_SIGNER_ROLES:
        raise I3ValueError("signer_id is not an authenticated non-root I1 role")
    return value


def _route(fields: Mapping[str, str]) -> tuple[str, str]:
    route = fields["import_class"]
    if route not in IMPORT_ROUTE_STATES:
        raise I3RouteError("import_class is outside the frozen route vocabulary")
    source, destination = IMPORT_ROUTE_STATES[route]
    if fields["from_state"] != source or fields["to_state"] != destination:
        raise I3RouteError("import class and source/destination states disagree")
    return source, destination


def _validate_identifiers(fields: Mapping[str, str]) -> None:
    _hex(fields["result_media_id"], "result_media_id", nonzero=True)
    values = [
        _hex(fields[name], name, nonzero=True) for name in EVENT_ID_FIELDS
    ]
    values.append(fields["result_media_id"])
    if len(set(values)) != len(values):
        raise I3BindingError("result-media and R/A/P/C identifiers must be distinct")


def parse_import_admission(
    raw: bytes, *, signer_context: SignerRegistryContext
) -> ImportAdmission:
    context = _context(signer_context)
    fields = _parse_record(raw, ADMISSION_FIELD_ORDER, label="import admission")
    literals = {
        "import_admission_schema": ADMISSION_SCHEMA,
        "authority_id": "control-host-preflight",
        "result_media_kind": "import-outcome-v1",
        "outcome_schema": OUTCOME_SCHEMA,
        "outcome_max_bytes": "2048",
        "decision": "approved",
    }
    for name, expected in literals.items():
        if fields[name] != expected:
            raise I3ValueError(f"{name} must be {expected}")
    for name in (
        "campaign_id",
        "ceremony_id",
        "package_sha256",
        "package_object_id",
        "attachment_capability_id",
    ):
        _hex(fields[name], name)
    _signer(fields["signer_id"], context)
    _route(fields)
    _validate_identifiers(fields)
    _hex(fields["admission_event_id"], "admission_event_id", nonzero=True)
    if fields["admission_event_id"] != fields["admission_frozen_media_event_id"]:
        raise I3BindingError("admission_event_id must equal A")
    return ImportAdmission(
        raw,
        tuple(fields.items()),
        _sha(raw),
        context,
        _ADMISSION_PROVENANCE,
    )


def require_import_admission(
    value: object, *, signer_context: SignerRegistryContext
) -> ImportAdmission:
    context = _context(signer_context)
    if (
        type(value) is not ImportAdmission
        or value._provenance is not _ADMISSION_PROVENANCE
    ):
        raise I3BindingError("admission is not an authenticated parsed handle")
    parsed = parse_import_admission(value.raw, signer_context=context)
    if parsed.fields != value.fields or parsed.admission_record_sha256 != value.admission_record_sha256:
        raise I3BindingError("admission handle changed after parsing")
    return value


def serialize_import_admission(
    value: ImportAdmission | Mapping[str, object],
    *,
    signer_context: SignerRegistryContext,
) -> bytes:
    if type(value) is ImportAdmission:
        return require_import_admission(value, signer_context=signer_context).raw
    raw = _serialize(value, ADMISSION_FIELD_ORDER, "import admission")
    return parse_import_admission(raw, signer_context=signer_context).raw


def hash_import_admission(
    value: ImportAdmission | bytes, *, signer_context: SignerRegistryContext
) -> str:
    if type(value) is ImportAdmission:
        return require_import_admission(value, signer_context=signer_context).admission_record_sha256
    return parse_import_admission(value, signer_context=signer_context).admission_record_sha256


def _outcome_tuple(fields: Mapping[str, str], source: str, destination: str) -> str:
    before = _hex(
        fields["before_configuration_state_sha256"],
        "before_configuration_state_sha256",
        nonzero=True,
    )
    after = _hex(
        fields["after_configuration_state_sha256"],
        "after_configuration_state_sha256",
    )
    actual = (
        fields["decision"],
        fields["reason"],
        fields["before_state"],
        fields["after_state"],
    )
    if actual == ("accepted", "none", source, destination) and after != ZERO64 and after != before:
        return "accepted"
    if actual == ("rejected", "parse-rejected", source, source) and after == before:
        return "parse-rejected"
    if actual == ("rejected", "validation-rejected", source, source) and after == before:
        return "validation-rejected"
    if actual == ("rejected", "state-commit-failed", source, "indeterminate") and after == ZERO64:
        return "state-commit-failed"
    raise I3TupleError("outcome decision/reason/state/configuration tuple is invalid")


def parse_import_outcome_frame(
    raw: bytes, *, signer_context: SignerRegistryContext
) -> ImportOutcome:
    context = _context(signer_context)
    fields = _parse_record(
        raw,
        OUTCOME_FIELD_ORDER,
        label="import outcome frame",
        max_bytes=OUTCOME_MEDIA_BYTES,
    )
    literals = {
        "import_outcome_schema": OUTCOME_SCHEMA,
        "tcb_service_id": "S0-IMPORT-TRANSITION-TCB-1",
        "result_media_kind": "import-outcome-v1",
    }
    for name, expected in literals.items():
        if fields[name] != expected:
            raise I3ValueError(f"{name} must be {expected}")
    for name in (
        "campaign_id",
        "ceremony_id",
        "package_sha256",
        "package_object_id",
        "attachment_capability_id",
        "admission_event_id",
        "admission_record_sha256",
    ):
        _hex(fields[name], name)
    _signer(fields["signer_id"], context)
    source, destination = _route(fields)
    _validate_identifiers(fields)
    lines = raw.splitlines(keepends=True)
    body_hash = _sha(b"".join(lines[:25]))
    _hex(fields["outcome_body_sha256"], "outcome_body_sha256")
    if fields["outcome_body_sha256"] != body_hash:
        raise I3HashError("outcome body SHA-256 mismatch")
    outcome_class = _outcome_tuple(fields, source, destination)
    return ImportOutcome(
        raw,
        tuple(fields.items()),
        body_hash,
        _sha(raw),
        outcome_class,
        context,
        _OUTCOME_PROVENANCE,
    )


def require_import_outcome(
    value: object, *, signer_context: SignerRegistryContext
) -> ImportOutcome:
    context = _context(signer_context)
    if type(value) is not ImportOutcome or value._provenance is not _OUTCOME_PROVENANCE:
        raise I3BindingError("outcome is not an authenticated parsed handle")
    parsed = parse_import_outcome_frame(value.raw, signer_context=context)
    if (
        parsed.fields != value.fields
        or parsed.outcome_body_sha256 != value.outcome_body_sha256
        or parsed.outcome_frame_sha256 != value.outcome_frame_sha256
        or parsed.outcome_class != value.outcome_class
    ):
        raise I3BindingError("outcome handle changed after parsing")
    return value


def serialize_import_outcome(
    value: ImportOutcome | Mapping[str, object],
    *,
    signer_context: SignerRegistryContext,
) -> bytes:
    if type(value) is ImportOutcome:
        return require_import_outcome(value, signer_context=signer_context).raw
    raw = _serialize(value, OUTCOME_FIELD_ORDER, "import outcome frame")
    return parse_import_outcome_frame(raw, signer_context=signer_context).raw


def hash_import_outcome_frame(
    value: ImportOutcome | bytes, *, signer_context: SignerRegistryContext
) -> str:
    if type(value) is ImportOutcome:
        return require_import_outcome(value, signer_context=signer_context).outcome_frame_sha256
    return parse_import_outcome_frame(value, signer_context=signer_context).outcome_frame_sha256


def validate_outcome_binding(
    outcome: ImportOutcome,
    admission: ImportAdmission,
    *,
    signer_context: SignerRegistryContext,
) -> None:
    parsed_outcome = require_import_outcome(outcome, signer_context=signer_context)
    parsed_admission = require_import_admission(admission, signer_context=signer_context)
    for name in COMMON_BINDING_FIELDS:
        if parsed_outcome[name] != parsed_admission[name]:
            raise I3BindingError(f"admission/outcome binding mismatch: {name}")
    if parsed_outcome["admission_event_id"] != parsed_admission["admission_event_id"]:
        raise I3BindingError("admission/outcome binding mismatch: admission_event_id")
    if parsed_outcome["admission_record_sha256"] != parsed_admission.admission_record_sha256:
        raise I3BindingError("admission/outcome binding mismatch: admission hash")


def route_bindings_from_admission(admission: ImportAdmission) -> tuple[tuple[str, str], ...]:
    return (
        ("campaign_id", admission["campaign_id"]),
        ("ceremony_id", admission["ceremony_id"]),
        ("signer_id", admission["signer_id"]),
        ("route_class", admission["import_class"]),
        ("from_state", admission["from_state"]),
        ("to_state", admission["to_state"]),
        ("attachment_capability_id", admission["attachment_capability_id"]),
        ("admission_record_sha256", admission.admission_record_sha256),
        ("media_object_sha256", admission["package_sha256"]),
        ("media_object_id", admission["package_object_id"]),
        ("result_media_id", admission["result_media_id"]),
        ("reserved_media_event_id", admission["reserved_media_event_id"]),
        ("admission_frozen_media_event_id", admission["admission_frozen_media_event_id"]),
        ("pending_media_event_id", admission["pending_media_event_id"]),
        ("completion_media_event_id", admission["completion_media_event_id"]),
    )


def route_bindings_from_outcome(outcome: ImportOutcome) -> tuple[tuple[str, str], ...]:
    return (
        ("campaign_id", outcome["campaign_id"]),
        ("ceremony_id", outcome["ceremony_id"]),
        ("signer_id", outcome["signer_id"]),
        ("route_class", outcome["import_class"]),
        ("from_state", outcome["from_state"]),
        ("to_state", outcome["to_state"]),
        ("attachment_capability_id", outcome["attachment_capability_id"]),
        ("admission_record_sha256", outcome["admission_record_sha256"]),
        ("media_object_sha256", outcome["package_sha256"]),
        ("media_object_id", outcome["package_object_id"]),
        ("result_media_id", outcome["result_media_id"]),
        ("reserved_media_event_id", outcome["reserved_media_event_id"]),
        ("admission_frozen_media_event_id", outcome["admission_frozen_media_event_id"]),
        ("pending_media_event_id", outcome["pending_media_event_id"]),
        ("completion_media_event_id", outcome["completion_media_event_id"]),
    )

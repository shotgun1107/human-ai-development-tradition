"""Exact public v0.14 section-4 codecs and recipient recomputation.

Only records explicitly governed by plan sections 4.1 and 4.3--4.6 use the
generic signed envelope here.  Signature decisions and already trusted public
key assignments are injected.  This module creates no keys, registry, root,
private material, or cryptographic implementation.
"""

from __future__ import annotations

import hashlib
import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from types import MappingProxyType
from typing import Any, Protocol

from .auth import sha256_bytes
from .errors import CanonicalRecordError
from .topology import (
    EXPECTED_SIGNER_ROLES,
    STATUS_EDGE_ORDER,
    FrozenTopology,
    expected_states,
    require_frozen_topology,
)


_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_HEX128 = re.compile(r"^[0-9a-f]{128}$")
_TOKEN = re.compile(r"^[a-z0-9-]+$")
_ZERO64 = "0" * 64
_MAX_DECIMAL_DIGITS = 20
_SIGNER_AUTHORITY_PROVENANCE = object()
_COMPARISON_RULES = {
    "E43": ("semantic-judge-1", "semantic-judge-2", "judgment-comparison"),
    "E45": (
        "comparator-operator-1",
        "comparator-operator-2",
        "adjudication-comparison",
    ),
}


class SignatureVerifier(Protocol):
    """External registry-backed signature decision, injected by the caller."""

    def verify(
        self,
        *,
        signer_role: str,
        signer_key_sha256: str,
        preimage: bytes,
        signature_hex: str,
    ) -> bool: ...


@dataclass(frozen=True, init=False)
class SignerAuthority(Mapping[str, str]):
    """API-level immutable binding of trusted role/key assignments."""

    topology_sha256: str
    binding_sha256: str
    _key_ids: Mapping[str, str] = field(repr=False, compare=False)
    _provenance: object = field(repr=False, compare=False)

    def __init__(
        self,
        topology_sha256: str,
        binding_sha256: str,
        key_ids: Mapping[str, str],
        *,
        _provenance: object,
    ) -> None:
        if _provenance is not _SIGNER_AUTHORITY_PROVENANCE:
            raise CanonicalRecordError(
                "SignerAuthority must bind an externally trusted assignment digest"
            )
        object.__setattr__(self, "topology_sha256", topology_sha256)
        object.__setattr__(self, "binding_sha256", binding_sha256)
        object.__setattr__(self, "_key_ids", key_ids)
        object.__setattr__(self, "_provenance", _provenance)

    def __getitem__(self, key: str) -> str:
        return self._key_ids[key]

    def __iter__(self):
        return iter(self._key_ids)

    def __len__(self) -> int:
        return len(self._key_ids)


def _signer_binding_bytes(
    topology_sha256: str, assignments: tuple[tuple[str, str], ...]
) -> bytes:
    lines = [
        "I1-EXTERNAL-SIGNER-ASSIGNMENT-1",
        f"topology_sha256={topology_sha256}",
        f"entry_count={len(assignments)}",
    ]
    for index, (role, key_id) in enumerate(assignments, 1):
        lines.extend(
            (
                f"entry_{index}_role={role}",
                f"entry_{index}_key_id={key_id}",
            )
        )
    return ("\n".join(lines) + "\n").encode("ascii")


def signer_assignment_binding_sha256(
    topology: FrozenTopology, assignments: Sequence[tuple[str, str]]
) -> str:
    """Compute the binding digest that an external authority must pin."""

    topology = require_frozen_topology(topology)
    normalized = _normalize_signer_assignments(assignments)
    return hashlib.sha256(
        _signer_binding_bytes(topology.snapshot_sha256, normalized)
    ).hexdigest()


def _normalize_signer_assignments(
    assignments: Sequence[tuple[str, str]],
) -> tuple[tuple[str, str], ...]:
    if isinstance(assignments, (str, bytes, Mapping)):
        raise CanonicalRecordError(
            "signer assignments must be an exact ordered role/key sequence"
        )
    normalized: list[tuple[str, str]] = []
    for item in assignments:
        if type(item) is not tuple or len(item) != 2:
            raise CanonicalRecordError("signer assignment entry must be an exact pair")
        role, key_id = item
        if type(role) is not str or type(key_id) is not str:
            raise CanonicalRecordError("signer assignment values must be exact strings")
        if not _TOKEN.fullmatch(role) or not _HEX64.fullmatch(key_id):
            raise CanonicalRecordError("signer assignment syntax is invalid")
        normalized.append((role, key_id))
    if tuple(role for role, _key in normalized) != EXPECTED_SIGNER_ROLES:
        raise CanonicalRecordError("signer assignment role order or inventory mismatch")
    key_ids = tuple(key for _role, key in normalized)
    if len(set(key_ids)) != len(key_ids):
        raise CanonicalRecordError("duplicate signer key assignment is forbidden")
    return tuple(normalized)


def bind_external_signer_authority(
    topology: FrozenTopology,
    assignments: Sequence[tuple[str, str]],
    *,
    expected_binding_sha256: str,
) -> SignerAuthority:
    """Bind assignments only when they match an out-of-band expected digest."""

    topology = require_frozen_topology(topology)
    if type(expected_binding_sha256) is not str or not _HEX64.fullmatch(
        expected_binding_sha256
    ):
        raise CanonicalRecordError("expected signer binding must be lowercase SHA-256")
    normalized = _normalize_signer_assignments(assignments)
    actual = hashlib.sha256(
        _signer_binding_bytes(topology.snapshot_sha256, normalized)
    ).hexdigest()
    if actual != expected_binding_sha256:
        raise CanonicalRecordError("external signer-assignment binding mismatch")
    return SignerAuthority(
        topology.snapshot_sha256,
        actual,
        MappingProxyType(dict(normalized)),
        _provenance=_SIGNER_AUTHORITY_PROVENANCE,
    )


def _require_signer_authority(
    value: object, topology: FrozenTopology | None = None
) -> SignerAuthority:
    if type(value) is not SignerAuthority or getattr(value, "_provenance", None) is not _SIGNER_AUTHORITY_PROVENANCE:
        raise CanonicalRecordError("signer key authority is not authenticated")
    if not isinstance(value._key_ids, MappingProxyType):
        raise CanonicalRecordError("signer key authority is not immutable")
    normalized = _normalize_signer_assignments(tuple(value._key_ids.items()))
    actual = hashlib.sha256(
        _signer_binding_bytes(value.topology_sha256, normalized)
    ).hexdigest()
    if actual != value.binding_sha256:
        raise CanonicalRecordError("signer key authority digest changed")
    if topology is not None:
        topology = require_frozen_topology(topology)
        if value.topology_sha256 != topology.snapshot_sha256:
            raise CanonicalRecordError("signer authority/topology binding mismatch")
    return value


@dataclass(frozen=True)
class SignedEnvelope:
    raw: bytes
    signer_role: str
    signer_key_sha256: str
    record_bytes: bytes
    record_sha256: str
    signature_hex: str
    preimage: bytes


@dataclass(frozen=True)
class EvidenceReceipt:
    raw: bytes
    edge: str
    producer_role: str
    artifact_kind: str
    artifact_sha256: str


@dataclass(frozen=True)
class EvidenceBundle:
    raw: bytes
    edge: str
    envelopes: tuple[SignedEnvelope, ...]
    receipts: tuple[EvidenceReceipt, ...]
    control_integration_manifest_sha256: str | None


@dataclass(frozen=True)
class StatusRecord:
    raw: bytes
    sequence: int
    previous_record_sha256: str
    event_edge: str
    event_commitment_sha256: str
    evidence_mask: str
    status_code: str
    monotonic_timestamp_ns: int


@dataclass(frozen=True)
class StatusPair:
    envelope: SignedEnvelope
    record: StatusRecord
    bundle: EvidenceBundle


@dataclass(frozen=True)
class ComparisonRecord:
    raw: bytes
    edge: str
    left_role: str
    left_envelope_sha256: str
    left_record_sha256: str
    right_role: str
    right_envelope_sha256: str
    right_record_sha256: str
    agreed_record_sha256: str


@dataclass(frozen=True)
class VerifiedComparison:
    left_envelope: SignedEnvelope
    right_envelope: SignedEnvelope
    comparison_envelope: SignedEnvelope
    comparison_record: ComparisonRecord
    comparison_digest: str
    agreed_record_bytes: bytes


@dataclass(frozen=True)
class PublicationRecord:
    raw: bytes
    source_record_sha256: str
    published_record_sha256: str
    monotonic_timestamp_ns: int


@dataclass(frozen=True)
class VerifiedPublication:
    publication_envelope: SignedEnvelope
    publication_record: PublicationRecord
    published_record_bytes: bytes


def _exact_str(value: object, label: str) -> str:
    if type(value) is not str:
        raise CanonicalRecordError(f"{label} must be exact string text")
    return value


def _exact_int(value: object, label: str) -> int:
    if type(value) is not int:
        raise CanonicalRecordError(f"{label} must be an exact integer, not boolean")
    return value


def _canonical_bytes(raw: bytes, label: str) -> None:
    if type(raw) is not bytes:
        raise CanonicalRecordError(f"{label} must be exact bytes")
    if not raw or raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw or not raw.endswith(b"\n"):
        raise CanonicalRecordError(
            f"{label} must be non-empty BOM-free LF-only bytes with final LF"
        )
    try:
        raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise CanonicalRecordError(f"{label} must be ASCII") from exc


def _decimal(value: bytes, label: str) -> int:
    if type(value) is not bytes:
        raise CanonicalRecordError(f"{label} must be exact decimal bytes")
    try:
        text = value.decode("ascii")
    except UnicodeDecodeError as exc:
        raise CanonicalRecordError(f"{label} is not ASCII decimal") from exc
    if len(text) > _MAX_DECIMAL_DIGITS:
        raise CanonicalRecordError(f"{label} exceeds the decimal digit ceiling")
    if not re.fullmatch(r"0|[1-9][0-9]*", text):
        raise CanonicalRecordError(f"{label} is not canonical decimal")
    try:
        return int(text)
    except (ValueError, OverflowError) as exc:
        raise CanonicalRecordError(f"{label} could not be parsed") from exc


def _take_line(raw: bytes, cursor: int, label: str) -> tuple[bytes, int]:
    end = raw.find(b"\n", cursor)
    if end < 0:
        raise CanonicalRecordError(f"missing LF after {label}")
    return raw[cursor:end], end + 1


def _field(line: bytes, prefix: bytes, label: str) -> bytes:
    if not line.startswith(prefix):
        raise CanonicalRecordError(f"missing or reordered {label}")
    return line[len(prefix) :]


def signature_preimage(
    record_bytes: bytes, signer_role: str, signer_key_sha256: str
) -> bytes:
    """Build the exact v0.14 preimage without signing it."""

    _canonical_bytes(record_bytes, "record_bytes")
    signer_role = _exact_str(signer_role, "signer role")
    signer_key_sha256 = _exact_str(signer_key_sha256, "signer key ID")
    if not _TOKEN.fullmatch(signer_role) or not _HEX64.fullmatch(signer_key_sha256):
        raise CanonicalRecordError("invalid signer role or key ID")
    return (
        b"URC-0.14-SIGNED-ARTIFACT\n"
        + f"signer_role={signer_role}\n".encode("ascii")
        + f"signer_key_sha256={signer_key_sha256}\n".encode("ascii")
        + f"record_length={len(record_bytes)}\n".encode("ascii")
        + record_bytes
        + f"record_sha256={sha256_bytes(record_bytes)}\n".encode("ascii")
    )


def assemble_signed_envelope(preimage: bytes, signature_hex: str) -> bytes:
    """Frame an externally supplied signature; no signing is performed."""

    if type(preimage) is not bytes:
        raise CanonicalRecordError("signature preimage must be exact bytes")
    signature_hex = _exact_str(signature_hex, "signature")
    if not _HEX128.fullmatch(signature_hex):
        raise CanonicalRecordError("signature must be 128 lowercase hex characters")
    return (
        preimage
        + b"signature_algorithm=Ed25519\n"
        + f"signature_hex={signature_hex}\n".encode("ascii")
    )


def parse_signed_envelope(
    raw: bytes,
    signer_authority: SignerAuthority,
    verifier: SignatureVerifier,
    *,
    required_role: str | None = None,
) -> SignedEnvelope:
    """Validate one generic envelope against immutable role/key authority."""

    authority = _require_signer_authority(signer_authority)
    if required_role is not None:
        required_role = _exact_str(required_role, "required signer role")
    _canonical_bytes(raw, "signed envelope")
    cursor = 0
    line, cursor = _take_line(raw, cursor, "envelope schema")
    if line != b"URC-0.14-SIGNED-ARTIFACT":
        raise CanonicalRecordError("signed envelope schema mismatch")
    line, cursor = _take_line(raw, cursor, "signer_role")
    signer_role = _field(line, b"signer_role=", "signer_role").decode("ascii")
    if not _TOKEN.fullmatch(signer_role):
        raise CanonicalRecordError("invalid signer role syntax")
    line, cursor = _take_line(raw, cursor, "signer_key_sha256")
    signer_key_sha256 = _field(
        line, b"signer_key_sha256=", "signer_key_sha256"
    ).decode("ascii")
    if not _HEX64.fullmatch(signer_key_sha256):
        raise CanonicalRecordError("invalid signer key ID syntax")
    expected_key = authority.get(signer_role)
    if expected_key is None or expected_key != signer_key_sha256:
        raise CanonicalRecordError("signer role/key assignment mismatch")
    if required_role is not None and signer_role != required_role:
        raise CanonicalRecordError("unexpected signer role")
    line, cursor = _take_line(raw, cursor, "record_length")
    record_length = _decimal(
        _field(line, b"record_length=", "record_length"), "record_length"
    )
    if record_length < 1 or cursor + record_length > len(raw):
        raise CanonicalRecordError("record length is out of bounds")
    record_bytes = raw[cursor : cursor + record_length]
    cursor += record_length
    _canonical_bytes(record_bytes, "record_bytes")
    line, cursor = _take_line(raw, cursor, "record_sha256")
    record_sha256 = _field(
        line, b"record_sha256=", "record_sha256"
    ).decode("ascii")
    if not _HEX64.fullmatch(record_sha256) or record_sha256 != sha256_bytes(
        record_bytes
    ):
        raise CanonicalRecordError("record hash mismatch")
    preimage_end = cursor
    line, cursor = _take_line(raw, cursor, "signature_algorithm")
    if line != b"signature_algorithm=Ed25519":
        raise CanonicalRecordError("signature algorithm mismatch")
    line, cursor = _take_line(raw, cursor, "signature_hex")
    signature_hex = _field(line, b"signature_hex=", "signature_hex").decode(
        "ascii"
    )
    if not _HEX128.fullmatch(signature_hex):
        raise CanonicalRecordError("invalid signature syntax")
    if cursor != len(raw):
        raise CanonicalRecordError("trailing signed-envelope bytes")
    preimage = raw[:preimage_end]
    try:
        decision = verifier.verify(
            signer_role=signer_role,
            signer_key_sha256=signer_key_sha256,
            preimage=preimage,
            signature_hex=signature_hex,
        )
    except AttributeError as exc:
        raise CanonicalRecordError("injected signature verifier is invalid") from exc
    if decision is not True:
        raise CanonicalRecordError("injected signature verification failed")
    return SignedEnvelope(
        raw,
        signer_role,
        signer_key_sha256,
        record_bytes,
        record_sha256,
        signature_hex,
        preimage,
    )


def _receipt_table(topology: FrozenTopology) -> Mapping[str, tuple[tuple[str, str], ...]]:
    topology = require_frozen_topology(topology)
    return MappingProxyType(
        {
            row["edge"]: tuple(
                (entry["producer_role"], entry["artifact_kind"])
                for entry in row["entries"]
            )
            for row in topology["status"]["receipts"]
        }
    )


def serialize_evidence_receipt(
    topology: FrozenTopology,
    edge: str,
    producer_role: str,
    artifact_kind: str,
    artifact_sha256: str,
) -> bytes:
    edge = _exact_str(edge, "evidence edge")
    producer_role = _exact_str(producer_role, "producer role")
    artifact_kind = _exact_str(artifact_kind, "artifact kind")
    artifact_sha256 = _exact_str(artifact_sha256, "artifact digest")
    expected = _receipt_table(topology).get(edge)
    if expected is None or (producer_role, artifact_kind) not in expected:
        raise CanonicalRecordError("receipt edge/producer/kind combination is not allowed")
    if not _HEX64.fullmatch(artifact_sha256):
        raise CanonicalRecordError("invalid artifact digest")
    return (
        "evidence_receipt_schema=URC-0.14-STATUS-EVIDENCE-1\n"
        f"edge={edge}\n"
        f"producer_role={producer_role}\n"
        f"artifact_kind={artifact_kind}\n"
        f"artifact_sha256={artifact_sha256}\n"
        "required_check_result=accepted\n"
    ).encode("ascii")


def parse_evidence_receipt(
    record_bytes: bytes, topology: FrozenTopology
) -> EvidenceReceipt:
    _canonical_bytes(record_bytes, "evidence receipt")
    lines = record_bytes[:-1].split(b"\n")
    if (
        len(lines) != 6
        or lines[0]
        != b"evidence_receipt_schema=URC-0.14-STATUS-EVIDENCE-1"
    ):
        raise CanonicalRecordError("evidence receipt schema or field count mismatch")
    edge = _field(lines[1], b"edge=", "edge").decode("ascii")
    producer = _field(lines[2], b"producer_role=", "producer_role").decode(
        "ascii"
    )
    kind = _field(lines[3], b"artifact_kind=", "artifact_kind").decode("ascii")
    digest = _field(lines[4], b"artifact_sha256=", "artifact_sha256").decode(
        "ascii"
    )
    if lines[5] != b"required_check_result=accepted":
        raise CanonicalRecordError("required check result is not accepted")
    if not _HEX64.fullmatch(digest):
        raise CanonicalRecordError("artifact digest syntax mismatch")
    expected = _receipt_table(topology).get(edge)
    if expected is None or (producer, kind) not in expected:
        raise CanonicalRecordError("receipt edge/producer/kind combination is not allowed")
    return EvidenceReceipt(record_bytes, edge, producer, kind, digest)


def serialize_root_bundle(control_integration_manifest_sha256: str) -> bytes:
    value = _exact_str(
        control_integration_manifest_sha256, "CONTROL integration manifest digest"
    )
    if not _HEX64.fullmatch(value):
        raise CanonicalRecordError("invalid CONTROL integration manifest digest")
    return (
        "evidence_bundle_schema=URC-0.14-STATUS-BUNDLE-1\n"
        "edge=ROOT\n"
        "entry_count=0\n"
        f"control_integration_manifest_sha256={value}\n"
    ).encode("ascii")


def serialize_evidence_bundle(
    topology: FrozenTopology, edge: str, envelope_bytes: Sequence[bytes]
) -> bytes:
    edge = _exact_str(edge, "non-genesis bundle edge")
    expected = _receipt_table(topology).get(edge)
    if expected is None:
        raise CanonicalRecordError("invalid non-genesis bundle edge")
    if isinstance(envelope_bytes, (str, bytes)):
        raise CanonicalRecordError("receipt envelopes must be an exact sequence")
    values = tuple(envelope_bytes)
    if len(values) != len(expected):
        raise CanonicalRecordError("bundle edge or receipt count mismatch")
    raw = (
        "evidence_bundle_schema=URC-0.14-STATUS-BUNDLE-1\n"
        f"edge={edge}\n"
        f"entry_count={len(values)}\n"
    ).encode("ascii")
    for index, envelope in enumerate(values, 1):
        _canonical_bytes(envelope, "receipt envelope")
        raw += (
            f"entry_{index}_envelope_length={len(envelope)}\n".encode("ascii")
            + envelope
        )
    return raw


def parse_evidence_bundle(
    raw: bytes,
    topology: FrozenTopology,
    signer_authority: SignerAuthority,
    verifier: SignatureVerifier,
    *,
    expected_control_integration_manifest_sha256: str,
) -> EvidenceBundle:
    topology = require_frozen_topology(topology)
    authority = _require_signer_authority(signer_authority, topology)
    expected_manifest = _exact_str(
        expected_control_integration_manifest_sha256,
        "expected CONTROL integration manifest digest",
    )
    if not _HEX64.fullmatch(expected_manifest):
        raise CanonicalRecordError("expected ROOT manifest digest is invalid")
    _canonical_bytes(raw, "evidence bundle")
    cursor = 0
    line, cursor = _take_line(raw, cursor, "bundle schema")
    if line != b"evidence_bundle_schema=URC-0.14-STATUS-BUNDLE-1":
        raise CanonicalRecordError("evidence bundle schema mismatch")
    line, cursor = _take_line(raw, cursor, "bundle edge")
    edge = _field(line, b"edge=", "edge").decode("ascii")
    line, cursor = _take_line(raw, cursor, "entry_count")
    count = _decimal(_field(line, b"entry_count=", "entry_count"), "entry_count")
    if edge == "ROOT":
        if count != 0:
            raise CanonicalRecordError("ROOT bundle must have zero receipts")
        line, cursor = _take_line(
            raw, cursor, "CONTROL integration manifest digest"
        )
        manifest_digest = _field(
            line,
            b"control_integration_manifest_sha256=",
            "control_integration_manifest_sha256",
        ).decode("ascii")
        if not _HEX64.fullmatch(manifest_digest) or manifest_digest != expected_manifest:
            raise CanonicalRecordError("ROOT manifest anchor mismatch")
        if cursor != len(raw):
            raise CanonicalRecordError("trailing ROOT bundle bytes")
        return EvidenceBundle(raw, edge, (), (), manifest_digest)

    expected = _receipt_table(topology).get(edge)
    if expected is None or count != len(expected):
        raise CanonicalRecordError("bundle edge or receipt count mismatch")
    envelopes: list[SignedEnvelope] = []
    receipts: list[EvidenceReceipt] = []
    for index, (expected_role, expected_kind) in enumerate(expected, 1):
        line, cursor = _take_line(raw, cursor, f"entry_{index}_envelope_length")
        length = _decimal(
            _field(
                line,
                f"entry_{index}_envelope_length=".encode("ascii"),
                f"entry_{index}_envelope_length",
            ),
            f"entry_{index}_envelope_length",
        )
        if length < 1 or cursor + length > len(raw):
            raise CanonicalRecordError("receipt envelope length is out of bounds")
        envelope_raw = raw[cursor : cursor + length]
        cursor += length
        envelope = parse_signed_envelope(
            envelope_raw, authority, verifier, required_role=expected_role
        )
        receipt = parse_evidence_receipt(envelope.record_bytes, topology)
        if (
            receipt.edge != edge
            or receipt.producer_role != expected_role
            or receipt.artifact_kind != expected_kind
        ):
            raise CanonicalRecordError("receipt bundle entry order or identity mismatch")
        envelopes.append(envelope)
        receipts.append(receipt)
    if cursor != len(raw):
        raise CanonicalRecordError("trailing evidence-bundle bytes")
    return EvidenceBundle(raw, edge, tuple(envelopes), tuple(receipts), None)


def _status_relation(sequence: int) -> tuple[str, str, str]:
    if sequence == 0:
        return "ROOT", "0000", "A-0000"
    if sequence < 1 or sequence > len(STATUS_EDGE_ORDER):
        raise CanonicalRecordError("status sequence is out of bounds")
    mask = f"{((1 << sequence) - 1):04x}"
    return STATUS_EDGE_ORDER[sequence - 1], mask, "A-" + mask


def serialize_status_record(
    sequence: int,
    previous_record_sha256: str,
    event_edge: str,
    event_commitment_sha256: str,
    evidence_mask: str,
    monotonic_timestamp_ns: int,
) -> bytes:
    sequence = _exact_int(sequence, "status sequence")
    timestamp = _exact_int(monotonic_timestamp_ns, "monotonic timestamp")
    previous = _exact_str(previous_record_sha256, "previous record digest")
    edge = _exact_str(event_edge, "status event edge")
    commitment = _exact_str(event_commitment_sha256, "event commitment")
    mask = _exact_str(evidence_mask, "evidence mask")
    expected_edge, expected_mask, status = _status_relation(sequence)
    if edge != expected_edge or mask != expected_mask:
        raise CanonicalRecordError("status sequence/event/mask relation mismatch")
    if sequence == 0 and previous != _ZERO64:
        raise CanonicalRecordError("ROOT previous-record digest must be zero")
    if not _HEX64.fullmatch(previous) or not _HEX64.fullmatch(commitment):
        raise CanonicalRecordError("status digest syntax mismatch")
    if timestamp < 0 or len(str(timestamp)) > _MAX_DECIMAL_DIGITS:
        raise CanonicalRecordError("monotonic timestamp is out of bounds")
    return (
        "status_schema=URC-0.14-STATUS-1\n"
        f"sequence={sequence}\n"
        f"previous_record_sha256={previous}\n"
        f"event_edge={edge}\n"
        f"event_commitment_sha256={commitment}\n"
        f"evidence_mask={mask}\n"
        f"status_code={status}\n"
        f"monotonic_timestamp_ns={timestamp}\n"
    ).encode("ascii")


def parse_status_record(record_bytes: bytes) -> StatusRecord:
    _canonical_bytes(record_bytes, "status record")
    lines = record_bytes[:-1].split(b"\n")
    if len(lines) != 8 or lines[0] != b"status_schema=URC-0.14-STATUS-1":
        raise CanonicalRecordError("status schema or field count mismatch")
    sequence = _decimal(_field(lines[1], b"sequence=", "sequence"), "sequence")
    previous = _field(
        lines[2], b"previous_record_sha256=", "previous_record_sha256"
    ).decode("ascii")
    event = _field(lines[3], b"event_edge=", "event_edge").decode("ascii")
    commitment = _field(
        lines[4], b"event_commitment_sha256=", "event_commitment_sha256"
    ).decode("ascii")
    mask = _field(lines[5], b"evidence_mask=", "evidence_mask").decode("ascii")
    status = _field(lines[6], b"status_code=", "status_code").decode("ascii")
    timestamp = _decimal(
        _field(lines[7], b"monotonic_timestamp_ns=", "monotonic_timestamp_ns"),
        "monotonic_timestamp_ns",
    )
    expected_event, expected_mask, expected_status = _status_relation(sequence)
    if not _HEX64.fullmatch(previous) or not _HEX64.fullmatch(commitment):
        raise CanonicalRecordError("status digest syntax mismatch")
    if (
        event != expected_event
        or mask != expected_mask
        or status != expected_status
        or (sequence == 0 and previous != _ZERO64)
    ):
        raise CanonicalRecordError("status sequence/event/mask relation mismatch")
    return StatusRecord(
        record_bytes,
        sequence,
        previous,
        event,
        commitment,
        mask,
        status,
        timestamp,
    )


def validate_status_chain(
    raw_pairs: Sequence[tuple[bytes, bytes]],
    topology: FrozenTopology,
    signer_authority: SignerAuthority,
    verifier: SignatureVerifier,
    *,
    expected_control_integration_manifest_sha256: str,
) -> tuple[StatusPair, ...]:
    """Validate a non-empty genesis-through-prefix sequence of E51 pairs."""

    topology = require_frozen_topology(topology)
    authority = _require_signer_authority(signer_authority, topology)
    if isinstance(raw_pairs, (str, bytes)):
        raise CanonicalRecordError("status chain must be an exact pair sequence")
    pairs = tuple(raw_pairs)
    if not pairs or len(pairs) > 15:
        raise CanonicalRecordError("status chain must contain a 1..15 pair prefix")
    result: list[StatusPair] = []
    previous: StatusRecord | None = None
    states = expected_states()
    for index, item in enumerate(pairs):
        if type(item) is not tuple or len(item) != 2:
            raise CanonicalRecordError("status chain item must be an exact pair")
        envelope_raw, bundle_raw = item
        bundle = parse_evidence_bundle(
            bundle_raw,
            topology,
            authority,
            verifier,
            expected_control_integration_manifest_sha256=expected_control_integration_manifest_sha256,
        )
        envelope = parse_signed_envelope(
            envelope_raw,
            authority,
            verifier,
            required_role="control-registrar",
        )
        record = parse_status_record(envelope.record_bytes)
        expected_event = "ROOT" if index == 0 else STATUS_EDGE_ORDER[index - 1]
        expected_previous = _ZERO64 if previous is None else sha256_bytes(previous.raw)
        if record.sequence != index:
            raise CanonicalRecordError("status sequence is not a contiguous prefix")
        if record.previous_record_sha256 != expected_previous:
            raise CanonicalRecordError("status previous-record hash mismatch")
        if record.event_edge != expected_event or bundle.edge != expected_event:
            raise CanonicalRecordError("status/bundle event order mismatch")
        if record.event_commitment_sha256 != sha256_bytes(bundle.raw):
            raise CanonicalRecordError("status event commitment mismatch")
        if record.status_code != states[index] or record.evidence_mask != states[index][2:]:
            raise CanonicalRecordError("status prefix mask mismatch")
        if previous is not None and record.monotonic_timestamp_ns <= previous.monotonic_timestamp_ns:
            raise CanonicalRecordError("status timestamp did not strictly increase")
        pair = StatusPair(envelope, record, bundle)
        result.append(pair)
        previous = record
    return tuple(result)


def serialize_comparison_record(
    edge: str,
    left_envelope_raw: bytes,
    right_envelope_raw: bytes,
    signer_authority: SignerAuthority,
    verifier: SignatureVerifier,
) -> bytes:
    """Authenticate both sources and build an exact E43/E45 record."""

    edge = _exact_str(edge, "comparison edge")
    if edge not in _COMPARISON_RULES:
        raise CanonicalRecordError("comparison edge must be E43 or E45")
    left_role, right_role, _custodian = _COMPARISON_RULES[edge]
    authority = _require_signer_authority(signer_authority)
    left = parse_signed_envelope(
        left_envelope_raw, authority, verifier, required_role=left_role
    )
    right = parse_signed_envelope(
        right_envelope_raw, authority, verifier, required_role=right_role
    )
    if left.record_bytes != right.record_bytes:
        raise CanonicalRecordError("comparison source records are not byte-identical")
    agreed = sha256_bytes(left.record_bytes)
    return (
        "comparison_schema=URC-0.14-COMPARISON-1\n"
        f"edge={edge}\n"
        f"left_role={left_role}\n"
        f"left_envelope_sha256={sha256_bytes(left.raw)}\n"
        f"left_record_sha256={left.record_sha256}\n"
        f"right_role={right_role}\n"
        f"right_envelope_sha256={sha256_bytes(right.raw)}\n"
        f"right_record_sha256={right.record_sha256}\n"
        f"agreed_record_sha256={agreed}\n"
        "comparison_result=equal\n"
    ).encode("ascii")


def parse_comparison_record(record_bytes: bytes) -> ComparisonRecord:
    _canonical_bytes(record_bytes, "comparison record")
    lines = record_bytes[:-1].split(b"\n")
    if len(lines) != 10 or lines[0] != b"comparison_schema=URC-0.14-COMPARISON-1":
        raise CanonicalRecordError("comparison schema or field count mismatch")
    edge = _field(lines[1], b"edge=", "edge").decode("ascii")
    if edge not in _COMPARISON_RULES:
        raise CanonicalRecordError("comparison edge must be E43 or E45")
    expected_left, expected_right, _custodian = _COMPARISON_RULES[edge]
    left_role = _field(lines[2], b"left_role=", "left_role").decode("ascii")
    left_envelope = _field(
        lines[3], b"left_envelope_sha256=", "left_envelope_sha256"
    ).decode("ascii")
    left_record = _field(
        lines[4], b"left_record_sha256=", "left_record_sha256"
    ).decode("ascii")
    right_role = _field(lines[5], b"right_role=", "right_role").decode("ascii")
    right_envelope = _field(
        lines[6], b"right_envelope_sha256=", "right_envelope_sha256"
    ).decode("ascii")
    right_record = _field(
        lines[7], b"right_record_sha256=", "right_record_sha256"
    ).decode("ascii")
    agreed = _field(
        lines[8], b"agreed_record_sha256=", "agreed_record_sha256"
    ).decode("ascii")
    if lines[9] != b"comparison_result=equal":
        raise CanonicalRecordError("comparison result is not equal")
    if left_role != expected_left or right_role != expected_right:
        raise CanonicalRecordError("comparison source role/order mismatch")
    digests = (left_envelope, left_record, right_envelope, right_record, agreed)
    if any(not _HEX64.fullmatch(value) for value in digests):
        raise CanonicalRecordError("comparison digest syntax mismatch")
    if left_record != right_record or left_record != agreed:
        raise CanonicalRecordError("comparison common-record digest mismatch")
    return ComparisonRecord(
        record_bytes,
        edge,
        left_role,
        left_envelope,
        left_record,
        right_role,
        right_envelope,
        right_record,
        agreed,
    )


def verify_comparison_delivery(
    edge: str,
    delivery: Sequence[object],
    signer_authority: SignerAuthority,
    verifier: SignatureVerifier,
) -> VerifiedComparison:
    """Repeat every recipient check over the exact ordered five-part delivery."""

    edge = _exact_str(edge, "comparison edge")
    if edge not in _COMPARISON_RULES:
        raise CanonicalRecordError("comparison edge must be E43 or E45")
    if isinstance(delivery, (str, bytes)):
        raise CanonicalRecordError("comparison delivery must be an exact sequence")
    values = tuple(delivery)
    if len(values) != 5:
        raise CanonicalRecordError("comparison delivery must contain exactly five parts")
    left_raw, right_raw, comparison_raw, named_digest, agreed_record = values
    if any(type(value) is not bytes for value in (left_raw, right_raw, comparison_raw, agreed_record)):
        raise CanonicalRecordError("comparison envelope and agreed-record parts must be exact bytes")
    named_digest = _exact_str(named_digest, "comparison digest")
    if not _HEX64.fullmatch(named_digest):
        raise CanonicalRecordError("comparison digest syntax mismatch")
    left_role, right_role, custodian = _COMPARISON_RULES[edge]
    authority = _require_signer_authority(signer_authority)
    left = parse_signed_envelope(left_raw, authority, verifier, required_role=left_role)
    right = parse_signed_envelope(right_raw, authority, verifier, required_role=right_role)
    comparison_envelope = parse_signed_envelope(
        comparison_raw, authority, verifier, required_role=custodian
    )
    comparison = parse_comparison_record(comparison_envelope.record_bytes)
    if comparison.edge != edge:
        raise CanonicalRecordError("comparison delivery edge mismatch")
    if left.record_bytes != right.record_bytes or left.record_bytes != agreed_record:
        raise CanonicalRecordError("comparison delivered records are not byte-identical")
    expected = (
        sha256_bytes(left.raw),
        left.record_sha256,
        sha256_bytes(right.raw),
        right.record_sha256,
        sha256_bytes(agreed_record),
    )
    observed = (
        comparison.left_envelope_sha256,
        comparison.left_record_sha256,
        comparison.right_envelope_sha256,
        comparison.right_record_sha256,
        comparison.agreed_record_sha256,
    )
    if observed != expected:
        raise CanonicalRecordError("comparison envelope/record digest binding mismatch")
    if named_digest != sha256_bytes(comparison.raw):
        raise CanonicalRecordError("named comparison digest must hash exact record bytes")
    return VerifiedComparison(
        left,
        right,
        comparison_envelope,
        comparison,
        named_digest,
        agreed_record,
    )


def serialize_publication_record(
    source_record_bytes: bytes,
    published_record_bytes: bytes,
    monotonic_timestamp_ns: int,
) -> bytes:
    """Build the exact publication record only for byte-identical decisions."""

    if type(source_record_bytes) is not bytes or type(published_record_bytes) is not bytes:
        raise CanonicalRecordError("publication source and stored record must be exact bytes")
    if not source_record_bytes or source_record_bytes != published_record_bytes:
        raise CanonicalRecordError("publication source and stored record are not byte-identical")
    timestamp = _exact_int(monotonic_timestamp_ns, "publication timestamp")
    if timestamp < 0 or len(str(timestamp)) > _MAX_DECIMAL_DIGITS:
        raise CanonicalRecordError("publication timestamp is out of bounds")
    digest = sha256_bytes(source_record_bytes)
    return (
        "publication_schema=URC-0.14-PUBLICATION-1\n"
        "publisher_role=public-record-publisher\n"
        "source_edge=E53\n"
        f"source_record_sha256={digest}\n"
        "published_store=public-decision-store\n"
        f"published_record_sha256={digest}\n"
        "publication_result=byte-identical\n"
        f"monotonic_timestamp_ns={timestamp}\n"
    ).encode("ascii")


def parse_publication_record(record_bytes: bytes) -> PublicationRecord:
    _canonical_bytes(record_bytes, "publication record")
    lines = record_bytes[:-1].split(b"\n")
    expected_constants = {
        0: b"publication_schema=URC-0.14-PUBLICATION-1",
        1: b"publisher_role=public-record-publisher",
        2: b"source_edge=E53",
        4: b"published_store=public-decision-store",
        6: b"publication_result=byte-identical",
    }
    if len(lines) != 8 or any(lines[index] != value for index, value in expected_constants.items()):
        raise CanonicalRecordError("publication schema, constant, or field order mismatch")
    source_digest = _field(
        lines[3], b"source_record_sha256=", "source_record_sha256"
    ).decode("ascii")
    published_digest = _field(
        lines[5], b"published_record_sha256=", "published_record_sha256"
    ).decode("ascii")
    timestamp = _decimal(
        _field(lines[7], b"monotonic_timestamp_ns=", "monotonic_timestamp_ns"),
        "monotonic_timestamp_ns",
    )
    if (
        not _HEX64.fullmatch(source_digest)
        or not _HEX64.fullmatch(published_digest)
        or source_digest != published_digest
    ):
        raise CanonicalRecordError("publication source/stored digest equality mismatch")
    return PublicationRecord(record_bytes, source_digest, published_digest, timestamp)


def verify_publication_delivery(
    delivery: Sequence[bytes],
    signer_authority: SignerAuthority,
    verifier: SignatureVerifier,
) -> VerifiedPublication:
    """Verify E54/E55 source, stored bytes, signer, and receipt bindings."""

    if isinstance(delivery, (str, bytes)):
        raise CanonicalRecordError("publication delivery must be an exact sequence")
    values = tuple(delivery)
    if len(values) != 3 or any(type(value) is not bytes for value in values):
        raise CanonicalRecordError("publication delivery must contain three exact byte parts")
    source_record, published_record, publication_envelope_raw = values
    if not source_record or source_record != published_record:
        raise CanonicalRecordError("published decision bytes differ from the E53 source")
    authority = _require_signer_authority(signer_authority)
    envelope = parse_signed_envelope(
        publication_envelope_raw,
        authority,
        verifier,
        required_role="public-record-publisher",
    )
    record = parse_publication_record(envelope.record_bytes)
    digest = sha256_bytes(source_record)
    if record.source_record_sha256 != digest or record.published_record_sha256 != digest:
        raise CanonicalRecordError("publication receipt does not bind delivered decision bytes")
    return VerifiedPublication(envelope, record, published_record)


def verify_e56_publication_receipt(
    publication_envelope_raw: bytes,
    e56_receipt_envelope_raw: bytes,
    topology: FrozenTopology,
    signer_authority: SignerAuthority,
    verifier: SignatureVerifier,
) -> EvidenceReceipt:
    """Verify E56 binds the full publication envelope hash exactly once."""

    topology = require_frozen_topology(topology)
    authority = _require_signer_authority(signer_authority, topology)
    publication_envelope = parse_signed_envelope(
        publication_envelope_raw,
        authority,
        verifier,
        required_role="public-record-publisher",
    )
    parse_publication_record(publication_envelope.record_bytes)
    receipt_envelope = parse_signed_envelope(
        e56_receipt_envelope_raw,
        authority,
        verifier,
        required_role="public-record-publisher",
    )
    receipt = parse_evidence_receipt(receipt_envelope.record_bytes, topology)
    if (
        receipt.edge != "E56"
        or receipt.producer_role != "public-record-publisher"
        or receipt.artifact_kind != "publication-receipt-envelope-digest"
        or receipt.artifact_sha256 != sha256_bytes(publication_envelope.raw)
    ):
        raise CanonicalRecordError("E56 publication-envelope digest binding mismatch")
    return receipt

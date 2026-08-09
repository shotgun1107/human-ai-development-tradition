"""Exact public section-4 record and envelope validators.

Only records explicitly governed by URC-0.14 plan section 4 use the generic
signed envelope here.  Inherited artifacts with other signing specifications
are outside this gate.  Signature verification is injected; this module has no
cryptographic dependency and creates no keys or signatures.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Mapping, Protocol, Sequence

from .auth import sha256_bytes
from .errors import CanonicalRecordError
from .topology import STATUS_EDGE_ORDER, expected_states


_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_HEX128 = re.compile(r"^[0-9a-f]{128}$")
_TOKEN = re.compile(r"^[a-z0-9-]+$")
_ZERO64 = "0" * 64


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


def _canonical_bytes(raw: bytes, label: str) -> None:
    if not raw or raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw or not raw.endswith(b"\n"):
        raise CanonicalRecordError(f"{label} must be non-empty BOM-free LF-only bytes with final LF")
    try:
        raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise CanonicalRecordError(f"{label} must be ASCII") from exc


def _decimal(value: bytes, label: str) -> int:
    try:
        text = value.decode("ascii")
    except UnicodeDecodeError as exc:
        raise CanonicalRecordError(f"{label} is not ASCII decimal") from exc
    if not re.fullmatch(r"0|[1-9][0-9]*", text):
        raise CanonicalRecordError(f"{label} is not canonical decimal")
    return int(text)


def _take_line(raw: bytes, cursor: int, label: str) -> tuple[bytes, int]:
    end = raw.find(b"\n", cursor)
    if end < 0:
        raise CanonicalRecordError(f"missing LF after {label}")
    return raw[cursor:end], end + 1


def _field(line: bytes, prefix: bytes, label: str) -> bytes:
    if not line.startswith(prefix):
        raise CanonicalRecordError(f"missing or reordered {label}")
    return line[len(prefix) :]


def signature_preimage(record_bytes: bytes, signer_role: str, signer_key_sha256: str) -> bytes:
    """Build the exact preimage without signing it."""

    _canonical_bytes(record_bytes, "record_bytes")
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

    if not _HEX128.fullmatch(signature_hex):
        raise CanonicalRecordError("signature must be 128 lowercase hex characters")
    return (
        preimage
        + b"signature_algorithm=Ed25519\n"
        + f"signature_hex={signature_hex}\n".encode("ascii")
    )


def parse_signed_envelope(
    raw: bytes,
    signer_key_ids: Mapping[str, str],
    verifier: SignatureVerifier,
    *,
    required_role: str | None = None,
) -> SignedEnvelope:
    """Validate one exact generic envelope with an injected verifier."""

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
    expected_key = signer_key_ids.get(signer_role)
    if expected_key is None or expected_key != signer_key_sha256:
        raise CanonicalRecordError("signer role/key assignment mismatch")
    if required_role is not None and signer_role != required_role:
        raise CanonicalRecordError("unexpected signer role")
    line, cursor = _take_line(raw, cursor, "record_length")
    record_length = _decimal(_field(line, b"record_length=", "record_length"), "record_length")
    if record_length < 1 or cursor + record_length > len(raw):
        raise CanonicalRecordError("record length is out of bounds")
    record_bytes = raw[cursor : cursor + record_length]
    cursor += record_length
    _canonical_bytes(record_bytes, "record_bytes")
    line, cursor = _take_line(raw, cursor, "record_sha256")
    record_sha256 = _field(line, b"record_sha256=", "record_sha256").decode("ascii")
    if not _HEX64.fullmatch(record_sha256) or record_sha256 != sha256_bytes(record_bytes):
        raise CanonicalRecordError("record hash mismatch")
    preimage_end = cursor
    line, cursor = _take_line(raw, cursor, "signature_algorithm")
    if line != b"signature_algorithm=Ed25519":
        raise CanonicalRecordError("signature algorithm mismatch")
    line, cursor = _take_line(raw, cursor, "signature_hex")
    signature_hex = _field(line, b"signature_hex=", "signature_hex").decode("ascii")
    if not _HEX128.fullmatch(signature_hex):
        raise CanonicalRecordError("invalid signature syntax")
    if cursor != len(raw):
        raise CanonicalRecordError("trailing signed-envelope bytes")
    preimage = raw[:preimage_end]
    decision = verifier.verify(
        signer_role=signer_role,
        signer_key_sha256=signer_key_sha256,
        preimage=preimage,
        signature_hex=signature_hex,
    )
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


def serialize_evidence_receipt(
    edge: str, producer_role: str, artifact_kind: str, artifact_sha256: str
) -> bytes:
    if not re.fullmatch(r"E[0-9]{2}", edge):
        raise CanonicalRecordError("invalid evidence edge")
    if not _TOKEN.fullmatch(producer_role) or not _TOKEN.fullmatch(artifact_kind):
        raise CanonicalRecordError("invalid receipt role or artifact kind")
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


def _receipt_table(spec: Mapping[str, Any]) -> dict[str, list[tuple[str, str]]]:
    return {
        row["edge"]: [
            (entry["producer_role"], entry["artifact_kind"])
            for entry in row["entries"]
        ]
        for row in spec["status"]["receipts"]
    }


def parse_evidence_receipt(record_bytes: bytes, spec: Mapping[str, Any]) -> EvidenceReceipt:
    _canonical_bytes(record_bytes, "evidence receipt")
    lines = record_bytes[:-1].split(b"\n")
    if len(lines) != 6 or lines[0] != b"evidence_receipt_schema=URC-0.14-STATUS-EVIDENCE-1":
        raise CanonicalRecordError("evidence receipt schema or field count mismatch")
    edge = _field(lines[1], b"edge=", "edge").decode("ascii")
    producer = _field(lines[2], b"producer_role=", "producer_role").decode("ascii")
    kind = _field(lines[3], b"artifact_kind=", "artifact_kind").decode("ascii")
    digest = _field(lines[4], b"artifact_sha256=", "artifact_sha256").decode("ascii")
    if lines[5] != b"required_check_result=accepted":
        raise CanonicalRecordError("required check result is not accepted")
    if not _HEX64.fullmatch(digest):
        raise CanonicalRecordError("artifact digest syntax mismatch")
    expected = _receipt_table(spec).get(edge)
    if expected is None or (producer, kind) not in expected:
        raise CanonicalRecordError("receipt edge/producer/kind combination is not allowed")
    return EvidenceReceipt(record_bytes, edge, producer, kind, digest)


def serialize_root_bundle(control_integration_manifest_sha256: str) -> bytes:
    if not _HEX64.fullmatch(control_integration_manifest_sha256):
        raise CanonicalRecordError("invalid CONTROL integration manifest digest")
    return (
        "evidence_bundle_schema=URC-0.14-STATUS-BUNDLE-1\n"
        "edge=ROOT\n"
        "entry_count=0\n"
        f"control_integration_manifest_sha256={control_integration_manifest_sha256}\n"
    ).encode("ascii")


def serialize_evidence_bundle(edge: str, envelope_bytes: Sequence[bytes]) -> bytes:
    if edge == "ROOT" or not re.fullmatch(r"E[0-9]{2}", edge):
        raise CanonicalRecordError("invalid non-genesis bundle edge")
    raw = (
        "evidence_bundle_schema=URC-0.14-STATUS-BUNDLE-1\n"
        f"edge={edge}\n"
        f"entry_count={len(envelope_bytes)}\n"
    ).encode("ascii")
    for index, envelope in enumerate(envelope_bytes, 1):
        _canonical_bytes(envelope, "receipt envelope")
        raw += f"entry_{index}_envelope_length={len(envelope)}\n".encode("ascii") + envelope
    return raw


def parse_evidence_bundle(
    raw: bytes,
    spec: Mapping[str, Any],
    signer_key_ids: Mapping[str, str],
    verifier: SignatureVerifier,
    *,
    expected_control_integration_manifest_sha256: str,
) -> EvidenceBundle:
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
        line, cursor = _take_line(raw, cursor, "CONTROL integration manifest digest")
        manifest_digest = _field(
            line,
            b"control_integration_manifest_sha256=",
            "control_integration_manifest_sha256",
        ).decode("ascii")
        if (
            not _HEX64.fullmatch(manifest_digest)
            or manifest_digest != expected_control_integration_manifest_sha256
        ):
            raise CanonicalRecordError("ROOT manifest anchor mismatch")
        if cursor != len(raw):
            raise CanonicalRecordError("trailing ROOT bundle bytes")
        return EvidenceBundle(raw, edge, (), (), manifest_digest)

    table = _receipt_table(spec)
    expected = table.get(edge)
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
            envelope_raw,
            signer_key_ids,
            verifier,
            required_role=expected_role,
        )
        receipt = parse_evidence_receipt(envelope.record_bytes, spec)
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


def serialize_status_record(
    sequence: int,
    previous_record_sha256: str,
    event_edge: str,
    event_commitment_sha256: str,
    evidence_mask: str,
    monotonic_timestamp_ns: int,
) -> bytes:
    if sequence < 0 or sequence > 14:
        raise CanonicalRecordError("status sequence is out of bounds")
    if event_edge != "ROOT" and event_edge not in STATUS_EDGE_ORDER:
        raise CanonicalRecordError("status event edge syntax mismatch")
    if not _HEX64.fullmatch(previous_record_sha256) or not _HEX64.fullmatch(event_commitment_sha256):
        raise CanonicalRecordError("status digest syntax mismatch")
    if not re.fullmatch(r"[0-9a-f]{4}", evidence_mask):
        raise CanonicalRecordError("status mask syntax mismatch")
    if monotonic_timestamp_ns < 0:
        raise CanonicalRecordError("negative monotonic timestamp")
    return (
        "status_schema=URC-0.14-STATUS-1\n"
        f"sequence={sequence}\n"
        f"previous_record_sha256={previous_record_sha256}\n"
        f"event_edge={event_edge}\n"
        f"event_commitment_sha256={event_commitment_sha256}\n"
        f"evidence_mask={evidence_mask}\n"
        f"status_code=A-{evidence_mask}\n"
        f"monotonic_timestamp_ns={monotonic_timestamp_ns}\n"
    ).encode("ascii")


def parse_status_record(record_bytes: bytes) -> StatusRecord:
    _canonical_bytes(record_bytes, "status record")
    lines = record_bytes[:-1].split(b"\n")
    if len(lines) != 8 or lines[0] != b"status_schema=URC-0.14-STATUS-1":
        raise CanonicalRecordError("status schema or field count mismatch")
    sequence = _decimal(_field(lines[1], b"sequence=", "sequence"), "sequence")
    previous = _field(lines[2], b"previous_record_sha256=", "previous_record_sha256").decode("ascii")
    event = _field(lines[3], b"event_edge=", "event_edge").decode("ascii")
    commitment = _field(lines[4], b"event_commitment_sha256=", "event_commitment_sha256").decode("ascii")
    mask = _field(lines[5], b"evidence_mask=", "evidence_mask").decode("ascii")
    status = _field(lines[6], b"status_code=", "status_code").decode("ascii")
    timestamp = _decimal(
        _field(lines[7], b"monotonic_timestamp_ns=", "monotonic_timestamp_ns"),
        "monotonic_timestamp_ns",
    )
    if (
        sequence > 14
        or (event != "ROOT" and event not in STATUS_EDGE_ORDER)
        or not _HEX64.fullmatch(previous)
        or not _HEX64.fullmatch(commitment)
    ):
        raise CanonicalRecordError("status sequence or digest syntax mismatch")
    if not re.fullmatch(r"[0-9a-f]{4}", mask) or status != "A-" + mask:
        raise CanonicalRecordError("status mask/code mismatch")
    return StatusRecord(record_bytes, sequence, previous, event, commitment, mask, status, timestamp)


def validate_status_chain(
    raw_pairs: Sequence[tuple[bytes, bytes]],
    spec: Mapping[str, Any],
    signer_key_ids: Mapping[str, str],
    verifier: SignatureVerifier,
    *,
    expected_control_integration_manifest_sha256: str,
) -> tuple[StatusPair, ...]:
    """Validate a non-empty genesis-through-prefix sequence of E51 pairs."""

    if not raw_pairs or len(raw_pairs) > 15:
        raise CanonicalRecordError("status chain must contain a 1..15 pair prefix")
    result: list[StatusPair] = []
    previous: StatusRecord | None = None
    states = expected_states()
    for index, (envelope_raw, bundle_raw) in enumerate(raw_pairs):
        bundle = parse_evidence_bundle(
            bundle_raw,
            spec,
            signer_key_ids,
            verifier,
            expected_control_integration_manifest_sha256=expected_control_integration_manifest_sha256,
        )
        envelope = parse_signed_envelope(
            envelope_raw,
            signer_key_ids,
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

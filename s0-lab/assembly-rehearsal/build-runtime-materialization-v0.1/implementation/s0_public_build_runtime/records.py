"""Canonical diagnostic record construction without filesystem publication."""

from __future__ import annotations

from dataclasses import dataclass

from .canonical import jcs_lf, require_sha256, sha256_hex
from .errors import CanonicalError


@dataclass(frozen=True)
class RecordEvidence:
    body_raw: bytes
    body_canonical_sha256: str
    body_closed_file_sha256: str
    body_readback_sha256: str

    def __post_init__(self) -> None:
        if type(self.body_raw) is not bytes:
            raise CanonicalError("record body must be exact bytes")
        for value in (
            self.body_canonical_sha256,
            self.body_closed_file_sha256,
            self.body_readback_sha256,
        ):
            require_sha256(value)
        actual = sha256_hex(self.body_raw)
        if len({actual, self.body_canonical_sha256, self.body_closed_file_sha256, self.body_readback_sha256}) != 1:
            raise CanonicalError("record body close/readback identities differ")


def construct_in_memory_record(body: dict[str, object]) -> RecordEvidence:
    if type(body) is not dict:
        raise CanonicalError("record body must be an exact object")
    raw = jcs_lf(body)
    digest = sha256_hex(raw)
    return RecordEvidence(raw, digest, digest, digest)

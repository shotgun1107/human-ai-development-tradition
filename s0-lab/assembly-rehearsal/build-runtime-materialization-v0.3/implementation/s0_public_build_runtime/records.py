"""Canonical in-memory diagnostics without false filesystem observations."""

from __future__ import annotations

from dataclasses import dataclass

from .canonical import jcs_lf, require_sha256, sha256_hex
from .errors import CanonicalError


@dataclass(frozen=True, slots=True)
class InMemoryRecordDiagnostic:
    body_raw: bytes
    body_canonical_sha256: str
    observation_status: str = "UNAVAILABLE-NOT-MATERIALIZED"
    closed_file_observation: None = None
    readback_observation: None = None

    def __post_init__(self) -> None:
        if type(self.body_raw) is not bytes:
            raise CanonicalError("record body must be exact bytes")
        require_sha256(self.body_canonical_sha256)
        actual = sha256_hex(self.body_raw)
        if actual != self.body_canonical_sha256:
            raise CanonicalError("in-memory record body identity differs")
        if (
            self.observation_status != "UNAVAILABLE-NOT-MATERIALIZED"
            or self.closed_file_observation is not None
            or self.readback_observation is not None
        ):
            raise CanonicalError("unperformed filesystem observation was represented as evidence")


def construct_in_memory_record(body: dict[str, object]) -> InMemoryRecordDiagnostic:
    if type(body) is not dict:
        raise CanonicalError("record body must be an exact object")
    raw = jcs_lf(body)
    digest = sha256_hex(raw)
    return InMemoryRecordDiagnostic(raw, digest)

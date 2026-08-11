"""Opaque binding to the frozen public TRI2-VEC-02 evidence package."""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass, field

from .canonical import HEX64_PATTERN
from .errors import VectorBindingError


TRI2_VEC_02_ARTIFACT_SHA256 = "a5195c25bf206a31ab59b2ce8e34a092d0e3921b1f252675b3ab7a859cb49668"
TRI2_VEC_02_DERIVATION_SHA256 = "cf10458557273de394a0b119afd2dc61d9301a9e9e6f8bb677926d367e0daf2d"
TRI2_VEC_02_DECISION_SHA256 = "271ff05d7af484b072264a5c1f9d6a6bb157b0a6766613da5c6ddae8b994475c"
TRI2_VEC_02_ROWS = (
    ("TRI2-VEC-02-01", "c7176a703d4dd84fba3c0b760d10670f2a2053fa2c39ccc64ec7fd7792ac037a"),
    ("TRI2-VEC-02-02", "c7176a703d4dd84fba3c0b760d10670f2a2053fa2c39ccc64ec7fd7792ac03fa"),
    ("TRI2-VEC-02-03", "26e8958fc2b227b045c3f489f2ef98f0d5dfac05d3c63339b13802886d53fc05"),
    ("TRI2-VEC-02-04", "26e8958fc2b227b045c3f489f2ef98f0d5dfac05d3c63339b13802886d53fc85"),
)
_VECTOR_PROVENANCE = object()


@dataclass(frozen=True)
class FrozenVectorPackage:
    artifact_id: str
    artifact_sha256: str
    derivation_sha256: str
    decision_sha256: str
    rows: tuple[tuple[str, str], ...]
    _provenance: object = field(repr=False, compare=False)


def bind_frozen_tri2_vec_02(
    *,
    artifact_id: str,
    artifact_sha256: str,
    derivation_sha256: str,
    decision_sha256: str,
    rows: Sequence[tuple[str, str]],
) -> FrozenVectorPackage:
    """Bind only the exact independently verified and CONTROL-frozen package."""

    if artifact_id != "TRI2-VEC-02":
        raise VectorBindingError("only TRI2-VEC-02 has public vector authority")
    supplied_hashes = (artifact_sha256, derivation_sha256, decision_sha256)
    if any(type(value) is not str or not HEX64_PATTERN.fullmatch(value) for value in supplied_hashes):
        raise VectorBindingError("vector evidence hashes must be lowercase SHA-256")
    expected_hashes = (
        TRI2_VEC_02_ARTIFACT_SHA256,
        TRI2_VEC_02_DERIVATION_SHA256,
        TRI2_VEC_02_DECISION_SHA256,
    )
    if supplied_hashes != expected_hashes:
        raise VectorBindingError("vector evidence hash binding mismatch")
    if isinstance(rows, (str, bytes)):
        raise VectorBindingError("vector rows must be an exact ordered sequence")
    normalized: list[tuple[str, str]] = []
    for row in rows:
        if type(row) is not tuple or len(row) != 2 or any(type(item) is not str for item in row):
            raise VectorBindingError("each vector row must be an exact string pair")
        normalized.append(row)
    if tuple(normalized) != TRI2_VEC_02_ROWS:
        raise VectorBindingError("vector row identity, order, or bytes mismatch")
    if len({value for _row_id, value in normalized}) != 4:
        raise VectorBindingError("four pairwise-distinct vector rows are required")
    if any(len(value) != 64 or not HEX64_PATTERN.fullmatch(value) for _row_id, value in normalized):
        raise VectorBindingError("each vector must be exactly 32 lowercase-hex bytes")
    return FrozenVectorPackage(
        artifact_id,
        artifact_sha256,
        derivation_sha256,
        decision_sha256,
        tuple(normalized),
        _VECTOR_PROVENANCE,
    )


def require_frozen_vector_package(value: object) -> FrozenVectorPackage:
    if type(value) is not FrozenVectorPackage or value._provenance is not _VECTOR_PROVENANCE:
        raise VectorBindingError("vector package is not an authenticated frozen handle")
    rebound = bind_frozen_tri2_vec_02(
        artifact_id=value.artifact_id,
        artifact_sha256=value.artifact_sha256,
        derivation_sha256=value.derivation_sha256,
        decision_sha256=value.decision_sha256,
        rows=value.rows,
    )
    if rebound.rows != value.rows:
        raise VectorBindingError("vector package changed after binding")
    return value

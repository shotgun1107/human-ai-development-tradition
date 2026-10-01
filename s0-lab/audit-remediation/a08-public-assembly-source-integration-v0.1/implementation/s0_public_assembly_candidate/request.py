"""Exact reconstruction of the frozen eight-field public request."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any

from .canonical import canonical_json_bytes, load_strict_json_bytes
from .constants import (
    BLOCK_ID,
    PACKAGE_SHA256,
    QUESTIONS_SHA256,
    REHEARSAL_ID,
    REPRESENTATION_ID,
    REQUEST_BYTES,
    REQUEST_SHA256,
)


class RequestError(ValueError):
    """The logical or materialized request is not the frozen request."""


@dataclass(frozen=True)
class ReconstructedRequest:
    value: dict[str, Any]
    raw: bytes
    sha256: str


def reconstruct_request(package_raw: bytes, questions_raw: bytes) -> ReconstructedRequest:
    if hashlib.sha256(package_raw).hexdigest() != PACKAGE_SHA256:
        raise RequestError("input package hash mismatch")
    if hashlib.sha256(questions_raw).hexdigest() != QUESTIONS_SHA256:
        raise RequestError("questions hash mismatch")
    package = load_strict_json_bytes(package_raw, require_object=True)
    questions = load_strict_json_bytes(questions_raw, require_object=True)
    value = {
        "schema_id": "S0-PUBLIC-ASSEMBLY-REQUEST-1",
        "rehearsal_id": REHEARSAL_ID,
        "block_id": BLOCK_ID,
        "representation_id": REPRESENTATION_ID,
        "input_package_sha256": PACKAGE_SHA256,
        "questions_sha256": QUESTIONS_SHA256,
        "input_package": package,
        "questions": questions,
    }
    if len(value) != 8:
        raise RequestError("request field count mismatch")
    raw = canonical_json_bytes(value)
    digest = hashlib.sha256(raw).hexdigest()
    if len(raw) != REQUEST_BYTES or digest != REQUEST_SHA256:
        raise RequestError("reconstructed request bytes mismatch")
    return ReconstructedRequest(value=value, raw=raw, sha256=digest)


def require_materialized_request(
    reconstructed: ReconstructedRequest,
    artifact_raw: bytes,
) -> None:
    if type(artifact_raw) is not bytes:
        raise RequestError("materialized request must be exact bytes")
    if artifact_raw != reconstructed.raw:
        raise RequestError("materialized request differs from reconstruction")
    if len(artifact_raw) != REQUEST_BYTES:
        raise RequestError("materialized request byte length mismatch")
    if hashlib.sha256(artifact_raw).hexdigest() != REQUEST_SHA256:
        raise RequestError("materialized request hash mismatch")


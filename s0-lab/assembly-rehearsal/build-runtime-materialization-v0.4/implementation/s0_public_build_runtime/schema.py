"""Closed schema boundary until an exact dependency closure is authorized."""

from __future__ import annotations

from typing import Mapping

from .errors import SemanticError

SCHEMA_DEPENDENCY_STATUS = "BLOCKED-MISSING-EXTERNAL-PIN"


def authenticate_schema_registry(schema_bytes: Mapping[str, bytes]) -> None:
    """Reject every schema request until dependency bytes receive an external pin."""

    del schema_bytes
    raise SemanticError("schema dependency closure is BLOCKED-MISSING-EXTERNAL-PIN")


def validate_profile(profile_raw: bytes, effective_schema_raw: bytes, schema_bytes: Mapping[str, bytes]) -> dict[str, object]:
    del profile_raw, effective_schema_raw, schema_bytes
    raise SemanticError("profile validation is BLOCKED-MISSING-EXTERNAL-PIN")

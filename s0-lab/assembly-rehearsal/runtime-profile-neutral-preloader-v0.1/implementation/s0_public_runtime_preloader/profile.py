"""Authentication and nonforgeable authority for one runtime profile."""

from __future__ import annotations

import copy
import weakref
from types import MappingProxyType
from typing import Mapping

from .canonical import load_json_bytes, require_sha256, sha256_bytes
from .errors import RuntimeProfileError
from .schema import FixedDraft202012Validator
from .semantic import RELATIONS, SemanticEvidence, validate_semantic_relations


RUNTIME_PROFILE_SCHEMA_SHA256 = (
    "3cdcf7e39d39536213f5ab577970f39643b13aa542d854176c213590a16f92dd"
)
RUNTIME_PROFILE_SCHEMA_ID = (
    "urn:s0:public-assembly:runtime-profile-neutral-preloader:runtime-profile:4"
)
SEMANTIC_VALIDATOR_POLICY_ID = "runtime-profile-v0.4-semantic-relations-validator"

_AUTHORITY_TOKEN = object()


def _freeze(value: object) -> object:
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(child) for key, child in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(child) for child in value)
    return value


class AuthenticatedRuntimeProfile:
    """Process-local authority created only after schema and semantic checks."""

    __slots__ = ("_profile", "profile_sha256", "relations", "_sealed", "__weakref__")

    def __init__(
        self,
        token: object,
        profile: Mapping[str, object],
        profile_sha256: str,
        relations: tuple[str, ...],
    ) -> None:
        if token is not _AUTHORITY_TOKEN:
            raise RuntimeProfileError("runtime profile authority is not publicly constructible")
        object.__setattr__(self, "_sealed", False)
        object.__setattr__(self, "_profile", _freeze(copy.deepcopy(dict(profile))))
        object.__setattr__(self, "profile_sha256", profile_sha256)
        object.__setattr__(self, "relations", relations)
        object.__setattr__(self, "_sealed", True)

    def __copy__(self) -> object:
        raise TypeError("runtime profile authority cannot be copied")

    def __deepcopy__(self, memo: dict[int, object]) -> object:
        raise TypeError("runtime profile authority cannot be deep-copied")

    def __reduce__(self) -> object:
        raise TypeError("runtime profile authority cannot be serialized")

    def __setattr__(self, name: str, value: object) -> None:
        if getattr(self, "_sealed", False):
            raise RuntimeProfileError("runtime profile authority is immutable")
        object.__setattr__(self, name, value)

    @property
    def profile(self) -> Mapping[str, object]:
        return self._profile


_ISSUED_AUTHORITIES: weakref.WeakSet[AuthenticatedRuntimeProfile] = weakref.WeakSet()


def is_authenticated_runtime_profile(value: object) -> bool:
    return (
        type(value) is AuthenticatedRuntimeProfile
        and value in _ISSUED_AUTHORITIES
        and getattr(value, "_sealed", False) is True
    )


def authenticate_runtime_profile(
    *,
    profile_raw: bytes,
    schema_raw: bytes,
    schema_sha256: str,
    semantic_evidence: SemanticEvidence,
) -> AuthenticatedRuntimeProfile:
    """Authenticate exact bytes and issue one immutable process-local authority."""

    require_sha256(schema_sha256, "runtime profile schema pin")
    if schema_sha256 != RUNTIME_PROFILE_SCHEMA_SHA256 or sha256_bytes(schema_raw) != schema_sha256:
        raise RuntimeProfileError("runtime profile schema pin or bytes mismatch")
    schema = load_json_bytes(schema_raw, canonical=False)
    profile = load_json_bytes(profile_raw, canonical=True)
    if type(schema) is not dict or type(profile) is not dict:
        raise RuntimeProfileError("schema and profile roots must both be objects")
    if profile.get("schema_id") != RUNTIME_PROFILE_SCHEMA_ID:
        raise RuntimeProfileError("runtime profile schema ID is not exact")
    validator = FixedDraft202012Validator(schema)
    validator.validate(profile)
    profile_hash = sha256_bytes(profile_raw)
    if semantic_evidence.current_profile_sha256 != profile_hash:
        raise RuntimeProfileError("semantic evidence is not bound to the profile bytes")
    semantic_validator = profile["semantic_validator"]
    assert isinstance(semantic_validator, dict)
    if semantic_validator["policy_id"] != SEMANTIC_VALIDATOR_POLICY_ID:
        raise RuntimeProfileError("semantic validator policy is not this reviewed implementation")
    relations = validate_semantic_relations(profile, semantic_evidence)
    if relations != RELATIONS:
        raise RuntimeProfileError("semantic relation execution set is incomplete")
    authority = AuthenticatedRuntimeProfile(_AUTHORITY_TOKEN, profile, profile_hash, relations)
    _ISSUED_AUTHORITIES.add(authority)
    return authority

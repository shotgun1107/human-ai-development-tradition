"""Data-only validation of a runtime profile candidate.

The returned snapshot is deliberately not a capability or live authority.
Every consumer must revalidate the original profile, schema, and static byte
material in the same operation that prepares candidate output.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from .canonical import load_json_bytes, require_sha256, sha256_bytes
from .errors import RuntimeProfileError
from .schema import FixedDraft202012Validator
from .semantic import (
    BYTE_VERIFIED_RELATIONS,
    DEFERRED_STATIC_RELATIONS,
    StaticMaterialBundle,
    validate_static_relations,
)


RUNTIME_PROFILE_SCHEMA_SHA256 = (
    "3cdcf7e39d39536213f5ab577970f39643b13aa542d854176c213590a16f92dd"
)
PREDECESSOR_SCHEMA_SHA256 = (
    "92943a96249c312d0e2631705a667170d60d22d8e75f2571961ed1f728e934af",
    "e2e96940bbafc6a80987634fe794d700844dbc7d0b48e0e269922f03364fb34f",
    "1404f4981d3d7815e98a6c5d745596f15bb8d50a296410584d03d7ccb11ce3dd",
)
RUNTIME_PROFILE_SCHEMA_ID = (
    "urn:s0:public-assembly:runtime-profile-neutral-preloader:runtime-profile:4"
)
SEMANTIC_VALIDATOR_POLICY_ID = "runtime-profile-v0.4-semantic-relations-validator"


def _freeze(value: object) -> object:
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(child) for key, child in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(child) for child in value)
    return value


@dataclass(frozen=True)
class ValidatedProfileCandidate:
    """Reviewable data snapshot; explicitly never accepted as authority."""

    profile: Mapping[str, object]
    profile_raw: bytes
    profile_sha256: str
    static_relations: tuple[str, ...]
    deferred_static_relations: tuple[str, ...] = DEFERRED_STATIC_RELATIONS
    candidate_only: bool = True

    def __post_init__(self) -> None:
        if self.candidate_only is not True:
            raise RuntimeProfileError("validated profile result must remain candidate-only")
        if type(self.profile_raw) is not bytes:
            raise RuntimeProfileError("validated profile result lacks exact source bytes")
        require_sha256(self.profile_sha256, "validated candidate profile hash")
        if self.profile_sha256 != sha256_bytes(self.profile_raw):
            raise RuntimeProfileError("validated candidate profile hash is not byte-bound")
        if self.static_relations != BYTE_VERIFIED_RELATIONS:
            raise RuntimeProfileError("validated candidate byte relation set is incomplete")
        if self.deferred_static_relations != DEFERRED_STATIC_RELATIONS:
            raise RuntimeProfileError("validated candidate deferred relation set is not exact")
        object.__setattr__(self, "profile", _freeze(copy.deepcopy(dict(self.profile))))


def validate_runtime_profile_candidate(
    *,
    profile_raw: bytes,
    schema_raw: bytes,
    static_material: StaticMaterialBundle,
) -> ValidatedProfileCandidate:
    """Validate exact static bytes without issuing any reusable authority."""

    if sha256_bytes(schema_raw) != RUNTIME_PROFILE_SCHEMA_SHA256:
        raise RuntimeProfileError("runtime profile schema bytes differ from the frozen pin")
    schema = load_json_bytes(schema_raw, canonical=False)
    profile = load_json_bytes(profile_raw, canonical=True)
    if type(schema) is not dict or type(profile) is not dict:
        raise RuntimeProfileError("schema and profile roots must both be objects")
    if profile.get("schema_id") != RUNTIME_PROFILE_SCHEMA_ID:
        raise RuntimeProfileError("runtime profile schema ID is not exact")
    semantic_validator = profile.get("semantic_validator")
    if not isinstance(semantic_validator, Mapping):
        raise RuntimeProfileError("semantic validator profile object is absent")
    if semantic_validator.get("policy_id") != SEMANTIC_VALIDATOR_POLICY_ID:
        raise RuntimeProfileError("semantic validator policy is not exact")
    FixedDraft202012Validator(schema).validate(profile)
    relations = validate_static_relations(
        profile,
        profile_raw,
        static_material,
        predecessor_schema_hashes=PREDECESSOR_SCHEMA_SHA256,
    )
    if relations != BYTE_VERIFIED_RELATIONS:
        raise RuntimeProfileError("static byte relation execution is incomplete")
    return ValidatedProfileCandidate(
        profile=profile,
        profile_raw=profile_raw,
        profile_sha256=sha256_bytes(profile_raw),
        static_relations=relations,
    )

"""Draft 2020-12 registry checks over authenticated schema bytes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

from .canonical import strict_json
from .errors import SemanticError


@dataclass(frozen=True)
class SchemaRegistryResult:
    schema_ids: tuple[str, ...]
    schema_count: int


def authenticate_schema_registry(schema_bytes: Mapping[str, bytes]) -> tuple[Registry, SchemaRegistryResult]:
    if type(schema_bytes) is not dict or not schema_bytes:
        raise SemanticError("schema byte registry must be a nonempty exact dict")
    registry = Registry()
    identifiers: list[str] = []
    for logical_path, raw in schema_bytes.items():
        if type(logical_path) is not str or type(raw) is not bytes:
            raise SemanticError("schema byte registry entry type differs")
        schema = strict_json(raw)
        if type(schema) is not dict or type(schema.get("$id")) is not str:
            raise SemanticError("schema is missing one exact $id")
        try:
            Draft202012Validator.check_schema(schema)
            resource = Resource.from_contents(schema)
        except Exception as error:
            raise SemanticError("Draft 2020-12 schema validation failed") from error
        identifier = schema["$id"]
        if identifier in identifiers:
            raise SemanticError("schema $id is not unique")
        identifiers.append(identifier)
        registry = registry.with_resource(identifier, resource)
    return registry, SchemaRegistryResult(tuple(identifiers), len(identifiers))


def validate_profile(profile_raw: bytes, effective_schema_raw: bytes, schema_bytes: Mapping[str, bytes]) -> dict[str, object]:
    profile = strict_json(profile_raw)
    schema = strict_json(effective_schema_raw)
    if type(profile) is not dict or type(schema) is not dict:
        raise SemanticError("profile or schema root differs")
    registry, _ = authenticate_schema_registry(dict(schema_bytes))
    try:
        Draft202012Validator(schema, registry=registry).validate(profile)
    except Exception as error:
        raise SemanticError("profile does not validate against the authenticated schema registry") from error
    return profile

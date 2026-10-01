"""Dependency-free executor for the authenticated v0.4 schema vocabulary.

This is not a general JSON Schema implementation.  It deliberately supports
the complete, closed keyword set used by the externally authenticated v0.4
schema and rejects unsupported executable keywords.
"""

from __future__ import annotations

import re
from typing import Mapping

from .errors import RuntimeProfileError


_ANNOTATIONS = {"$id", "$schema", "title"}
_EXECUTABLE = {
    "$defs",
    "$ref",
    "additionalProperties",
    "allOf",
    "const",
    "enum",
    "items",
    "else",
    "if",
    "maxItems",
    "maxLength",
    "maximum",
    "minItems",
    "minLength",
    "minimum",
    "not",
    "oneOf",
    "pattern",
    "prefixItems",
    "properties",
    "required",
    "then",
    "type",
    "uniqueItems",
}


def _copy_schema_json(value: object) -> object:
    """Create a private JSON-only snapshot of caller-owned schema data."""

    if type(value) is dict:
        if any(type(key) is not str for key in value):
            raise RuntimeProfileError("schema contains a non-text object key")
        return {key: _copy_schema_json(child) for key, child in value.items()}
    if type(value) is list:
        return [_copy_schema_json(child) for child in value]
    if type(value) is float:
        if value != value or value in {float("inf"), float("-inf")}:
            raise RuntimeProfileError("schema contains a non-finite number")
        return value
    if value is None or type(value) in {str, int, bool}:
        return value
    raise RuntimeProfileError("schema contains a non-JSON value")


def _same_json(left: object, right: object) -> bool:
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        assert isinstance(right, dict)
        return set(left) == set(right) and all(_same_json(left[k], right[k]) for k in left)
    if isinstance(left, list):
        assert isinstance(right, list)
        return len(left) == len(right) and all(_same_json(a, b) for a, b in zip(left, right))
    return bool(left == right)


class FixedDraft202012Validator:
    """Validate instances against the exact keyword surface used by v0.4."""

    def __init__(self, schema: Mapping[str, object]) -> None:
        if type(schema) is not dict:
            raise RuntimeProfileError("schema root is not one object")
        snapshot = _copy_schema_json(schema)
        if type(snapshot) is not dict:
            raise RuntimeProfileError("schema snapshot is not one object")
        if snapshot.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            raise RuntimeProfileError("schema dialect is not Draft 2020-12")
        self._schema = snapshot
        self._audit_schema_keywords(snapshot, "#")

    def _audit_schema_keywords(self, value: object, path: str) -> None:
        if type(value) is not dict:
            raise RuntimeProfileError("schema node is not an object", path=path)
        # Keys under properties/$defs are instance or definition names,
        # not JSON Schema keywords.
        for key, child in value.items():
            if path.endswith("/properties") or path.endswith("/$defs"):
                self._audit_schema_keywords(child, f"{path}/{key}")
                continue
            if key not in _ANNOTATIONS | _EXECUTABLE:
                raise RuntimeProfileError("schema uses an unsupported keyword", path=f"{path}/{key}")
            self._audit_keyword_value(key, child, f"{path}/{key}")
            if key in {"properties", "$defs"}:
                if type(child) is not dict:
                    raise RuntimeProfileError("schema map keyword is not an object", path=f"{path}/{key}")
                for name, nested in child.items():
                    self._audit_schema_keywords(nested, f"{path}/{key}/{name}")
            elif key in {"allOf", "oneOf", "prefixItems"}:
                if type(child) is not list:
                    raise RuntimeProfileError("schema array keyword is not an array", path=f"{path}/{key}")
                for index, nested in enumerate(child):
                    self._audit_schema_keywords(nested, f"{path}/{key}/{index}")
            elif key in {"items", "not", "if", "then", "else", "additionalProperties"} and isinstance(child, dict):
                self._audit_schema_keywords(child, f"{path}/{key}")

    @staticmethod
    def _audit_keyword_value(key: str, value: object, path: str) -> None:
        if key in {"$id", "$ref", "$schema", "pattern", "title"}:
            if type(value) is not str:
                raise RuntimeProfileError("schema text keyword has the wrong type", path=path)
            return
        if key == "type":
            if type(value) is not str or value not in {
                "array",
                "boolean",
                "integer",
                "null",
                "number",
                "object",
                "string",
            }:
                raise RuntimeProfileError("schema type keyword is not supported", path=path)
            return
        if key in {"$defs", "properties"}:
            if type(value) is not dict:
                raise RuntimeProfileError("schema map keyword is not an object", path=path)
            return
        if key in {"allOf", "oneOf", "prefixItems"}:
            if type(value) is not list:
                raise RuntimeProfileError("schema array keyword is not an array", path=path)
            return
        if key == "required":
            if (
                type(value) is not list
                or any(type(item) is not str for item in value)
                or len(set(value)) != len(value)
            ):
                raise RuntimeProfileError("schema required keyword is not exact", path=path)
            return
        if key == "enum":
            if type(value) is not list or not value:
                raise RuntimeProfileError("schema enum keyword is not exact", path=path)
            return
        if key in {"additionalProperties", "items"}:
            if type(value) not in {bool, dict}:
                raise RuntimeProfileError("schema boolean-or-object keyword is not exact", path=path)
            return
        if key in {"if", "then", "else", "not"}:
            if type(value) is not dict:
                raise RuntimeProfileError("schema branch keyword is not an object", path=path)
            return
        if key in {"maxItems", "maxLength", "minItems", "minLength"}:
            if type(value) is not int or value < 0:
                raise RuntimeProfileError("schema nonnegative bound is not exact", path=path)
            return
        if key in {"maximum", "minimum"}:
            if type(value) not in {int, float}:
                raise RuntimeProfileError("schema numeric bound is not exact", path=path)
            return
        if key == "uniqueItems" and type(value) is not bool:
            raise RuntimeProfileError("schema uniqueItems keyword is not boolean", path=path)

    def validate(self, instance: object) -> None:
        self._validate(self._schema, instance, "#")

    def _resolve_ref(self, reference: object) -> Mapping[str, object]:
        if type(reference) is not str or not reference.startswith("#/"):
            raise RuntimeProfileError("schema reference is not a local JSON pointer")
        node: object = self._schema
        for raw in reference[2:].split("/"):
            token = raw.replace("~1", "/").replace("~0", "~")
            if type(node) is not dict or token not in node:
                raise RuntimeProfileError("schema reference target is absent")
            node = node[token]
        if type(node) is not dict:
            raise RuntimeProfileError("schema reference target is not a schema object")
        return node

    def _validate(self, schema: Mapping[str, object], instance: object, path: str) -> None:
        reference = schema.get("$ref")
        if reference is not None:
            self._validate(self._resolve_ref(reference), instance, path)

        for nested in schema.get("allOf", []):
            if type(nested) is not dict:
                raise RuntimeProfileError("allOf member is not a schema", path=path)
            self._validate(nested, instance, path)

        if "oneOf" in schema:
            matches = 0
            for nested in schema["oneOf"]:
                if type(nested) is not dict:
                    raise RuntimeProfileError("oneOf member is not a schema", path=path)
                try:
                    self._validate(nested, instance, path)
                except RuntimeProfileError:
                    continue
                matches += 1
            if matches != 1:
                raise RuntimeProfileError("instance does not match exactly one oneOf member", path=path)

        if "if" in schema:
            condition = schema["if"]
            if type(condition) is not dict:
                raise RuntimeProfileError("if member is not a schema", path=path)
            try:
                self._validate(condition, instance, path)
            except RuntimeProfileError:
                branch = schema.get("else")
            else:
                branch = schema.get("then")
            if branch is not None:
                if type(branch) is not dict:
                    raise RuntimeProfileError("conditional branch is not a schema", path=path)
                self._validate(branch, instance, path)

        if "not" in schema:
            nested = schema["not"]
            if type(nested) is not dict:
                raise RuntimeProfileError("not member is not a schema", path=path)
            try:
                self._validate(nested, instance, path)
            except RuntimeProfileError:
                pass
            else:
                raise RuntimeProfileError("instance matches a forbidden schema", path=path)

        if "const" in schema and not _same_json(instance, schema["const"]):
            raise RuntimeProfileError("instance differs from a required constant", path=path)
        if "enum" in schema:
            choices = schema["enum"]
            if type(choices) is not list or not any(_same_json(instance, item) for item in choices):
                raise RuntimeProfileError("instance is outside its exact enumeration", path=path)

        expected_type = schema.get("type")
        if expected_type is not None and not self._has_type(instance, expected_type):
            raise RuntimeProfileError("instance has the wrong JSON type", path=path)

        if isinstance(instance, str) and "pattern" in schema:
            pattern = schema["pattern"]
            if type(pattern) is not str or re.search(pattern, instance) is None:
                raise RuntimeProfileError("string does not match its required pattern", path=path)
        if isinstance(instance, str):
            if "minLength" in schema and len(instance) < schema["minLength"]:
                raise RuntimeProfileError("string is shorter than its minimum", path=path)
            if "maxLength" in schema and len(instance) > schema["maxLength"]:
                raise RuntimeProfileError("string is longer than its maximum", path=path)

        if type(instance) in {int, float} and type(instance) is not bool:
            if "minimum" in schema and instance < schema["minimum"]:
                raise RuntimeProfileError("number is below its minimum", path=path)
            if "maximum" in schema and instance > schema["maximum"]:
                raise RuntimeProfileError("number is above its maximum", path=path)

        if isinstance(instance, list):
            if "minItems" in schema and len(instance) < schema["minItems"]:
                raise RuntimeProfileError("array is shorter than its minimum", path=path)
            if "maxItems" in schema and len(instance) > schema["maxItems"]:
                raise RuntimeProfileError("array is longer than its maximum", path=path)
            if schema.get("uniqueItems") is True:
                for index, item in enumerate(instance):
                    if any(_same_json(item, prior) for prior in instance[:index]):
                        raise RuntimeProfileError("array items are not unique", path=path)
            prefix = schema.get("prefixItems", [])
            if type(prefix) is not list:
                raise RuntimeProfileError("prefixItems is not an array", path=path)
            for index, child in enumerate(prefix[: len(instance)]):
                if type(child) is not dict:
                    raise RuntimeProfileError("prefixItems member is not a schema", path=path)
                self._validate(child, instance[index], f"{path}/{index}")
            if "items" in schema:
                item_schema = schema["items"]
                remaining = instance[len(prefix) :]
                if item_schema is False:
                    if remaining:
                        raise RuntimeProfileError("array contains items forbidden by false schema", path=path)
                    return
                if item_schema is True:
                    return
                if type(item_schema) is not dict:
                    raise RuntimeProfileError("items is not a schema", path=path)
                for index, item in enumerate(remaining, start=len(prefix)):
                    self._validate(item_schema, item, f"{path}/{index}")

        if isinstance(instance, dict):
            required = schema.get("required", [])
            if type(required) is not list or any(type(item) is not str for item in required):
                raise RuntimeProfileError("required is not an exact string array", path=path)
            for key in required:
                if key not in instance:
                    raise RuntimeProfileError("required property is absent", path=f"{path}/{key}")
            properties = schema.get("properties", {})
            if type(properties) is not dict:
                raise RuntimeProfileError("properties is not an object", path=path)
            additional = schema.get("additionalProperties", True)
            if type(additional) not in {bool, dict}:
                raise RuntimeProfileError("additionalProperties is not a schema", path=path)
            extra = set(instance) - set(properties)
            if additional is False:
                if extra:
                    raise RuntimeProfileError("unknown property is forbidden", path=f"{path}/{sorted(extra)[0]}")
            elif type(additional) is dict:
                for key in sorted(extra):
                    self._validate(additional, instance[key], f"{path}/{key}")
            for key, value in instance.items():
                if key in properties:
                    child = properties[key]
                    if type(child) is not dict:
                        raise RuntimeProfileError("property schema is not an object", path=f"{path}/{key}")
                    self._validate(child, value, f"{path}/{key}")

    @staticmethod
    def _has_type(instance: object, expected: object) -> bool:
        if expected == "object":
            return type(instance) is dict
        if expected == "array":
            return type(instance) is list
        if expected == "string":
            return type(instance) is str
        if expected == "integer":
            return type(instance) is int
        if expected == "number":
            return type(instance) in {int, float}
        if expected == "boolean":
            return type(instance) is bool
        if expected == "null":
            return instance is None
        raise RuntimeProfileError("schema declares an unsupported JSON type")

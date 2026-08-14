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
    "maximum",
    "minimum",
    "not",
    "pattern",
    "properties",
    "required",
    "type",
}


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
        if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
            raise RuntimeProfileError("schema dialect is not Draft 2020-12")
        self._schema = schema
        self._audit_schema_keywords(schema, "#")

    def _audit_schema_keywords(self, value: object, path: str) -> None:
        if isinstance(value, dict):
            # Keys under properties/$defs are instance or definition names,
            # not JSON Schema keywords.
            for key, child in value.items():
                if path.endswith("/properties") or path.endswith("/$defs"):
                    self._audit_schema_keywords(child, f"{path}/{key}")
                    continue
                if key not in _ANNOTATIONS | _EXECUTABLE:
                    raise RuntimeProfileError("schema uses an unsupported keyword", path=f"{path}/{key}")
                if key in {"properties", "$defs"}:
                    if type(child) is not dict:
                        raise RuntimeProfileError("schema map keyword is not an object", path=f"{path}/{key}")
                    for name, nested in child.items():
                        self._audit_schema_keywords(nested, f"{path}/{key}/{name}")
                elif key in {"allOf"}:
                    if type(child) is not list:
                        raise RuntimeProfileError("schema allOf is not an array", path=f"{path}/{key}")
                    for index, nested in enumerate(child):
                        self._audit_schema_keywords(nested, f"{path}/{key}/{index}")
                elif key in {"items", "not", "additionalProperties"} and isinstance(child, dict):
                    self._audit_schema_keywords(child, f"{path}/{key}")

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

        if type(instance) in {int, float} and type(instance) is not bool:
            if "minimum" in schema and instance < schema["minimum"]:
                raise RuntimeProfileError("number is below its minimum", path=path)
            if "maximum" in schema and instance > schema["maximum"]:
                raise RuntimeProfileError("number is above its maximum", path=path)

        if isinstance(instance, list) and "items" in schema:
            item_schema = schema["items"]
            if type(item_schema) is not dict:
                raise RuntimeProfileError("items is not a schema", path=path)
            for index, item in enumerate(instance):
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
            if schema.get("additionalProperties") is False:
                extra = set(instance) - set(properties)
                if extra:
                    raise RuntimeProfileError("unknown property is forbidden", path=f"{path}/{sorted(extra)[0]}")
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


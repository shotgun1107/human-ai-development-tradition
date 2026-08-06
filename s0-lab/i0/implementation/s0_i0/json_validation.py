"""Draft 2020-12 validation with stable, machine-readable errors."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import SchemaError, ValidationError


@dataclass(frozen=True, order=True)
class StableValidationError:
    category: str
    instance_path: str
    schema_path: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return asdict(self)


def load_json(path: Path) -> tuple[Any, bytes]:
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("file is not valid UTF-8") from exc
    try:
        return json.loads(text), raw
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"invalid JSON at line {exc.lineno}, column {exc.colno}"
        ) from exc


def _json_path(parts: Iterable[object]) -> str:
    path = "$"
    for part in parts:
        if isinstance(part, int):
            path += f"[{part}]"
        else:
            path += "." + str(part).replace("~", "~0").replace("/", "~1")
    return path


def _stable_error(error: ValidationError) -> StableValidationError:
    return StableValidationError(
        category="schema",
        instance_path=_json_path(error.absolute_path),
        schema_path=_json_path(error.absolute_schema_path),
        message=error.message,
    )


def check_schema(schema: Any) -> list[StableValidationError]:
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        return [
            StableValidationError(
                category="schema-definition",
                instance_path=_json_path(exc.absolute_path),
                schema_path=_json_path(exc.absolute_schema_path),
                message=exc.message,
            )
        ]
    return []


def validate_instance(instance: Any, schema: Any) -> list[StableValidationError]:
    definition_errors = check_schema(schema)
    if definition_errors:
        return definition_errors
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = (_stable_error(error) for error in validator.iter_errors(instance))
    return sorted(errors)

"""Strict generic JSON byte primitives.

These helpers deliberately do not implement the closed effective response
schema.  They enforce only representation properties available to this gate.
"""

from __future__ import annotations

import json
import math
import unicodedata
from typing import Any

from .errors import JsonBytesError


def _object_without_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise JsonBytesError("duplicate JSON object member")
        result[key] = value
    return result


def _walk_strings(value: Any) -> None:
    if isinstance(value, str):
        if any(0xD800 <= ord(char) <= 0xDFFF for char in value):
            raise JsonBytesError("unpaired surrogate code point is forbidden")
        if unicodedata.normalize("NFC", value) != value:
            raise JsonBytesError("JSON strings must be NFC-normalized")
    elif isinstance(value, list):
        for item in value:
            _walk_strings(item)
    elif isinstance(value, dict):
        for key, item in value.items():
            _walk_strings(key)
            _walk_strings(item)


def _finite_float(text: str) -> float:
    if type(text) is not str or len(text) > 128:
        raise JsonBytesError("JSON number exceeds its representation ceiling")
    try:
        value = float(text)
    except (OverflowError, ValueError) as exc:
        raise JsonBytesError("invalid JSON number") from exc
    if not math.isfinite(value):
        raise JsonBytesError("non-finite JSON number is forbidden")
    return value


def _bounded_int(text: str) -> int:
    if type(text) is not str or len(text.lstrip("-")) > 20:
        raise JsonBytesError("JSON integer exceeds the 20-digit ceiling")
    try:
        return int(text)
    except (OverflowError, ValueError) as exc:
        raise JsonBytesError("invalid JSON integer") from exc


def parse_strict_json_bytes(raw: bytes, *, require_object: bool = False) -> Any:
    """Decode BOM-free strict UTF-8 JSON with duplicate/surrogate/NFC checks."""

    if type(raw) is not bytes:
        raise JsonBytesError("JSON input must be exact bytes")
    if type(require_object) is not bool:
        raise JsonBytesError("require_object must be exact boolean")
    if raw.startswith(b"\xef\xbb\xbf"):
        raise JsonBytesError("UTF-8 BOM is forbidden")
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise JsonBytesError("input is not strict UTF-8") from exc
    try:
        value = json.loads(
            text,
            object_pairs_hook=_object_without_duplicates,
            parse_int=_bounded_int,
            parse_float=_finite_float,
            parse_constant=lambda _value: (_ for _ in ()).throw(
                JsonBytesError("non-finite JSON number is forbidden")
            ),
        )
    except JsonBytesError:
        raise
    except json.JSONDecodeError as exc:
        raise JsonBytesError(
            f"invalid JSON at line {exc.lineno}, column {exc.colno}"
        ) from exc
    except (OverflowError, ValueError) as exc:
        raise JsonBytesError("invalid bounded JSON number") from exc
    _walk_strings(value)
    if require_object and not isinstance(value, dict):
        raise JsonBytesError("top-level JSON value must be an object")
    return value

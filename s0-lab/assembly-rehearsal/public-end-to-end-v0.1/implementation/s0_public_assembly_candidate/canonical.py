"""Strict JSON parsing and the frozen ASCII canonical encoding."""

from __future__ import annotations

import json
from typing import Any


class StrictJsonError(ValueError):
    """A JSON input or value violates the frozen public rules."""


def _reject_duplicate_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise StrictJsonError("duplicate JSON object key")
        result[key] = value
    return result


def _reject_nonfinite(token: str) -> object:
    raise StrictJsonError(f"non-finite JSON number is forbidden: {token}")


def load_strict_json_bytes(raw: bytes, *, require_object: bool = False) -> Any:
    if type(raw) is not bytes:
        raise StrictJsonError("JSON input must be exact bytes")
    if raw.startswith(b"\xef\xbb\xbf"):
        raise StrictJsonError("JSON input must be BOM-free")
    try:
        text = raw.decode("utf-8", errors="strict")
        value = json.loads(
            text,
            object_pairs_hook=_reject_duplicate_pairs,
            parse_constant=_reject_nonfinite,
        )
    except StrictJsonError:
        raise
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise StrictJsonError("JSON input is not strict UTF-8 JSON") from exc
    if require_object and type(value) is not dict:
        raise StrictJsonError("JSON root must be an object")
    return value


def canonical_json_bytes(value: Any) -> bytes:
    try:
        text = json.dumps(
            value,
            ensure_ascii=True,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
    except (TypeError, ValueError) as exc:
        raise StrictJsonError("value is not canonically serializable JSON") from exc
    try:
        return (text + "\n").encode("ascii", errors="strict")
    except UnicodeEncodeError as exc:
        raise StrictJsonError("ensure_ascii canonicalization failed") from exc


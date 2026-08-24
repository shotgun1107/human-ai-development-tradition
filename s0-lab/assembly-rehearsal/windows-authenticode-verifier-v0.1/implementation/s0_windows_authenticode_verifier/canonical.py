"""Strict PUBLIC byte codecs for the Authenticode verifier."""

from __future__ import annotations

import hashlib
import json
import re
from typing import Iterable, Mapping


class VerificationError(ValueError):
    """Deterministic fail-closed verification error."""


_SHA256 = re.compile(r"^[0-9a-f]{64}$")


def sha256_hex(raw: bytes) -> str:
    if type(raw) is not bytes:
        raise VerificationError("hash input must be exact bytes")
    return hashlib.sha256(raw).hexdigest()


def require_sha256(value: object, *, name: str, nonzero: bool = True) -> str:
    if type(value) is not str or _SHA256.fullmatch(value) is None:
        raise VerificationError(f"{name} must be lowercase SHA-256 text")
    if nonzero and value == "0" * 64:
        raise VerificationError(f"{name} must be nonzero")
    return value


def _pairs(values: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in values:
        if type(key) is not str or key in result:
            raise VerificationError("JSON object keys must be unique exact text")
        result[key] = value
    return result


def strict_json_object(raw: bytes) -> dict[str, object]:
    if type(raw) is not bytes or not raw or not raw.endswith(b"\n"):
        raise VerificationError("JSON must be nonempty exact bytes with final LF")
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw or b"\x00" in raw:
        raise VerificationError("JSON contains a forbidden byte")
    try:
        text = raw.decode("utf-8", "strict")
    except UnicodeDecodeError as error:
        raise VerificationError("JSON is not strict UTF-8") from error
    if any(line.endswith((" ", "\t")) for line in text.splitlines()):
        raise VerificationError("JSON contains trailing line whitespace")
    try:
        value = json.loads(
            text,
            object_pairs_hook=_pairs,
            parse_constant=lambda item: (_ for _ in ()).throw(
                VerificationError(f"nonfinite JSON is forbidden: {item}")
            ),
        )
    except VerificationError:
        raise
    except (TypeError, ValueError, json.JSONDecodeError) as error:
        raise VerificationError("JSON parse failed") from error
    if type(value) is not dict:
        raise VerificationError("JSON root must be one exact object")
    return value


def _utf16_key(value: str) -> bytes:
    try:
        return value.encode("utf-16-be", "strict")
    except UnicodeEncodeError as error:
        raise VerificationError("JSON key is not valid Unicode") from error


def _canonical_copy(value: object) -> object:
    if value is None or type(value) in {bool, str}:
        return value
    if type(value) is int:
        if not -(2**53 - 1) <= value <= 2**53 - 1:
            raise VerificationError("integer is outside the exact JSON range")
        return value
    if type(value) is list or type(value) is tuple:
        return [_canonical_copy(item) for item in value]
    if type(value) is dict:
        if any(type(key) is not str for key in value):
            raise VerificationError("JSON key must be exact text")
        return {
            key: _canonical_copy(value[key])
            for key in sorted(value, key=_utf16_key)
        }
    raise VerificationError("unsupported canonical JSON value")


def canonical_json_lf(value: object) -> bytes:
    try:
        return (
            json.dumps(
                _canonical_copy(value),
                ensure_ascii=False,
                separators=(",", ":"),
                allow_nan=False,
            ).encode("utf-8", "strict")
            + b"\n"
        )
    except (TypeError, ValueError, UnicodeError) as error:
        raise VerificationError("canonical JSON encoding failed") from error


def exact_keys(value: object, expected: Iterable[str], *, name: str) -> dict[str, object]:
    if type(value) is not dict:
        raise VerificationError(f"{name} must be one exact object")
    exact = tuple(expected)
    if set(value) != set(exact) or len(value) != len(exact):
        raise VerificationError(f"{name} fields differ")
    return value


def exact_list(value: object, *, name: str, minimum: int = 0) -> list[object]:
    if type(value) is not list or len(value) < minimum:
        raise VerificationError(f"{name} must be one exact bounded list")
    return value


def exact_bool(value: object, *, name: str) -> bool:
    if type(value) is not bool:
        raise VerificationError(f"{name} must be exact Boolean")
    return value


def exact_int(value: object, *, name: str, minimum: int | None = None) -> int:
    if type(value) is not int or type(value) is bool:
        raise VerificationError(f"{name} must be exact integer")
    if minimum is not None and value < minimum:
        raise VerificationError(f"{name} is below its minimum")
    return value


def exact_text(value: object, *, name: str) -> str:
    if type(value) is not str or not value:
        raise VerificationError(f"{name} must be nonempty exact text")
    return value


def manifest_bytes(rows: Mapping[str, bytes]) -> bytes:
    if type(rows) is not dict or not rows:
        raise VerificationError("manifest rows must be a nonempty exact mapping")
    lines: list[str] = []
    for path in sorted(rows, key=lambda item: item.encode("ascii", "strict")):
        raw = rows[path]
        if type(path) is not str or type(raw) is not bytes:
            raise VerificationError("manifest row type differs")
        if "\\" in path or path.startswith("/") or ".." in path.split("/"):
            raise VerificationError("manifest path is not one safe logical path")
        lines.append(f"{sha256_hex(raw)}  {path}")
    return ("\n".join(lines) + "\n").encode("ascii")


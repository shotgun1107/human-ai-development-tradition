"""Exact ASCII/LF helpers for the public I2 record formats."""

from __future__ import annotations

import hashlib
import re
from collections.abc import Mapping, Sequence
from types import MappingProxyType

from .errors import CanonicalRecordError


HEX64_PATTERN = re.compile(r"^[0-9a-f]{64}$")
TOKEN_PATTERN = re.compile(r"^[a-z0-9-]+$")
DECIMAL_PATTERN = re.compile(r"^(0|[1-9][0-9]*)$")
ZERO64 = "0" * 64


def sha256_bytes(raw: bytes) -> str:
    if type(raw) is not bytes:
        raise CanonicalRecordError("hash input must be exact bytes")
    return hashlib.sha256(raw).hexdigest()


def require_exact_text(value: object, label: str) -> str:
    if type(value) is not str:
        raise CanonicalRecordError(f"{label} must be exact string text")
    return value


def require_hex64(value: object, label: str, *, nonzero: bool = False) -> str:
    text = require_exact_text(value, label)
    if not HEX64_PATTERN.fullmatch(text):
        raise CanonicalRecordError(f"{label} must be 64 lowercase hexadecimal characters")
    if nonzero and text == ZERO64:
        raise CanonicalRecordError(f"{label} must be nonzero")
    return text


def require_token(value: object, label: str) -> str:
    text = require_exact_text(value, label)
    if not TOKEN_PATTERN.fullmatch(text):
        raise CanonicalRecordError(f"{label} must be a lowercase token")
    return text


def require_decimal(value: object, label: str) -> int:
    text = require_exact_text(value, label)
    if not DECIMAL_PATTERN.fullmatch(text):
        raise CanonicalRecordError(f"{label} must be canonical unsigned decimal")
    if len(text) > 20:
        raise CanonicalRecordError(f"{label} exceeds the decimal digit ceiling")
    return int(text)


def require_choice(value: object, label: str, choices: frozenset[str]) -> str:
    text = require_exact_text(value, label)
    if text not in choices:
        raise CanonicalRecordError(f"{label} is outside the frozen vocabulary")
    return text


def parse_exact_record(
    raw: bytes,
    field_order: Sequence[str],
    *,
    label: str,
    max_bytes: int | None = None,
) -> Mapping[str, str]:
    """Parse an exact ordered ``name=value`` ASCII/LF record."""

    if type(raw) is not bytes:
        raise CanonicalRecordError(f"{label} must be exact bytes")
    if not raw:
        raise CanonicalRecordError(f"{label} must be non-empty")
    if max_bytes is not None and len(raw) > max_bytes:
        raise CanonicalRecordError(f"{label} exceeds {max_bytes} bytes")
    if raw.startswith(b"\xef\xbb\xbf"):
        raise CanonicalRecordError(f"{label} must not contain a UTF-8 BOM")
    if b"\r" in raw:
        raise CanonicalRecordError(f"{label} must be LF-only")
    if b"\x00" in raw:
        raise CanonicalRecordError(f"{label} must not contain NUL")
    if not raw.endswith(b"\n"):
        raise CanonicalRecordError(f"{label} must end with LF")
    try:
        text = raw.decode("ascii")
    except UnicodeDecodeError as exc:
        raise CanonicalRecordError(f"{label} must be ASCII") from exc

    lines = text[:-1].split("\n")
    expected = tuple(field_order)
    if len(lines) != len(expected):
        raise CanonicalRecordError(
            f"{label} must contain exactly {len(expected)} lines"
        )

    values: dict[str, str] = {}
    for index, (line, field_name) in enumerate(zip(lines, expected, strict=True), 1):
        if not line:
            raise CanonicalRecordError(f"{label} line {index} must not be blank")
        if line.endswith((" ", "\t")):
            raise CanonicalRecordError(
                f"{label} line {index} has trailing whitespace"
            )
        prefix = field_name + "="
        if not line.startswith(prefix):
            raise CanonicalRecordError(
                f"{label} line {index} must be field {field_name}"
            )
        value = line[len(prefix) :]
        if not value:
            raise CanonicalRecordError(f"{label} field {field_name} must not be empty")
        values[field_name] = value
    return MappingProxyType(values)


def serialize_exact_record(
    values: Mapping[str, object],
    field_order: Sequence[str],
    *,
    label: str,
) -> bytes:
    if not isinstance(values, Mapping):
        raise CanonicalRecordError(f"{label} values must be a mapping")
    expected = tuple(field_order)
    if set(values) != set(expected) or len(values) != len(expected):
        raise CanonicalRecordError(f"{label} fields do not match the exact schema")
    lines: list[str] = []
    for field_name in expected:
        value = require_exact_text(values[field_name], field_name)
        if not value or "\n" in value or "\r" in value or "\x00" in value:
            raise CanonicalRecordError(f"{field_name} cannot be serialized canonically")
        if value.endswith((" ", "\t")):
            raise CanonicalRecordError(f"{field_name} has trailing whitespace")
        lines.append(f"{field_name}={value}")
    raw = ("\n".join(lines) + "\n").encode("ascii")
    parse_exact_record(raw, expected, label=label)
    return raw

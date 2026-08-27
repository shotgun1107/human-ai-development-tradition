"""Strict byte codecs for external-artifact authority acquisition v0.1."""

from __future__ import annotations

import base64
import binascii
import hashlib
import json
import re
from urllib.parse import urlsplit

from .errors import AuthorityError


MAX_EXACT_JSON_INTEGER = 2**53 - 1
_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_BASE64URL = re.compile(r"^[A-Za-z0-9_-]+$")


def sha256_hex(raw: bytes) -> str:
    if type(raw) is not bytes:
        raise AuthorityError("sha256_input_not_exact_bytes")
    return hashlib.sha256(raw).hexdigest()


def require_sha256(value: object, *, label: str) -> str:
    if type(value) is not str or _SHA256.fullmatch(value) is None:
        raise AuthorityError(f"{label}_sha256_invalid")
    return value


def require_exact_bool(value: object, *, label: str) -> bool:
    if type(value) is not bool:
        raise AuthorityError(f"{label}_boolean_invalid")
    return value


def require_exact_int(
    value: object,
    *,
    label: str,
    minimum: int | None = None,
    maximum: int | None = None,
) -> int:
    if type(value) is not int:
        raise AuthorityError(f"{label}_integer_invalid")
    if value < -MAX_EXACT_JSON_INTEGER or value > MAX_EXACT_JSON_INTEGER:
        raise AuthorityError(f"{label}_integer_not_exact_json")
    if minimum is not None and value < minimum:
        raise AuthorityError(f"{label}_integer_below_bound")
    if maximum is not None and value > maximum:
        raise AuthorityError(f"{label}_integer_above_bound")
    return value


def require_size(value: object, *, label: str, maximum: int) -> int:
    return require_exact_int(value, label=label, minimum=1, maximum=maximum)


def require_exact_text(
    value: object,
    *,
    label: str,
    maximum_length: int = 32767,
) -> str:
    if (
        type(value) is not str
        or not value
        or len(value) > maximum_length
        or "\x00" in value
    ):
        raise AuthorityError(f"{label}_text_invalid")
    return value


def require_https_url(value: object, *, label: str) -> str:
    text = require_exact_text(value, label=label, maximum_length=4096)
    try:
        text.encode("ascii", "strict")
        parsed = urlsplit(text)
    except (UnicodeError, ValueError) as exc:
        raise AuthorityError(f"{label}_url_invalid") from exc
    if (
        parsed.scheme != "https"
        or not parsed.netloc
        or parsed.hostname is None
        or parsed.username is not None
        or parsed.password is not None
        or parsed.fragment
        or parsed.hostname != parsed.hostname.lower()
        or parsed.port is not None
        or not parsed.path.startswith("/")
        or "\\" in parsed.path
    ):
        raise AuthorityError(f"{label}_url_invalid")
    return text


def exact_object(value: object, *, label: str) -> dict[str, object]:
    if type(value) is not dict or any(type(key) is not str for key in value):
        raise AuthorityError(f"{label}_object_invalid")
    return value


def exact_list(value: object, *, label: str) -> list[object]:
    if type(value) is not list:
        raise AuthorityError(f"{label}_list_invalid")
    return value


def require_exact_keys(
    value: object,
    expected: tuple[str, ...],
    *,
    label: str,
) -> dict[str, object]:
    item = exact_object(value, label=label)
    if len(item) != len(expected) or set(item) != set(expected):
        raise AuthorityError(f"{label}_fields_invalid")
    return item


def _reject_float(_: str) -> object:
    raise AuthorityError("json_float_forbidden")


def _reject_constant(_: str) -> object:
    raise AuthorityError("json_nonfinite_forbidden")


def _exact_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if type(key) is not str or key in result:
            raise AuthorityError("json_duplicate_or_nontext_key")
        result[key] = value
    return result


def _validate_json_tree(value: object, *, label: str) -> None:
    value_type = type(value)
    if value is None or value_type is bool or value_type is str:
        return
    if value_type is int:
        require_exact_int(value, label=label)
        return
    if value_type is list:
        for child in value:
            _validate_json_tree(child, label=label)
        return
    if value_type is dict:
        for key, child in value.items():
            if type(key) is not str:
                raise AuthorityError(f"{label}_json_key_invalid")
            _validate_json_tree(child, label=label)
        return
    raise AuthorityError(f"{label}_json_type_invalid")


def strict_json_value(raw: bytes, *, label: str, maximum_size: int) -> object:
    if type(raw) is not bytes or not raw or len(raw) > maximum_size:
        raise AuthorityError(f"{label}_json_byte_bound_invalid")
    if raw.startswith(b"\xef\xbb\xbf") or b"\x00" in raw:
        raise AuthorityError(f"{label}_json_forbidden_bytes")
    try:
        text = raw.decode("utf-8", "strict")
    except UnicodeDecodeError as exc:
        raise AuthorityError(f"{label}_json_utf8_invalid") from exc
    try:
        value = json.loads(
            text,
            object_pairs_hook=_exact_pairs,
            parse_float=_reject_float,
            parse_constant=_reject_constant,
        )
    except AuthorityError:
        raise
    except (TypeError, ValueError, json.JSONDecodeError) as exc:
        raise AuthorityError(f"{label}_json_parse_failed") from exc
    _validate_json_tree(value, label=label)
    return value


def strict_json_object(raw: bytes, *, label: str, maximum_size: int) -> dict[str, object]:
    return exact_object(
        strict_json_value(raw, label=label, maximum_size=maximum_size),
        label=label,
    )


def _utf16_key(value: str) -> bytes:
    try:
        return value.encode("utf-16-be", "strict")
    except UnicodeEncodeError as exc:
        raise AuthorityError("canonical_json_key_unicode_invalid") from exc


def _canonical_copy(value: object, seen: set[int]) -> object:
    value_type = type(value)
    if value is None or value_type is bool or value_type is str:
        return value
    if value_type is int:
        return require_exact_int(value, label="canonical_json")
    if value_type is list or value_type is tuple:
        identity = id(value)
        if identity in seen:
            raise AuthorityError("canonical_json_alias_or_cycle")
        seen.add(identity)
        return [_canonical_copy(item, seen) for item in value]
    if value_type is dict:
        identity = id(value)
        if identity in seen:
            raise AuthorityError("canonical_json_alias_or_cycle")
        seen.add(identity)
        if any(type(key) is not str for key in value):
            raise AuthorityError("canonical_json_key_invalid")
        return {
            key: _canonical_copy(value[key], seen)
            for key in sorted(value, key=_utf16_key)
        }
    raise AuthorityError("canonical_json_type_invalid")


def canonical_json_lf(value: object) -> bytes:
    try:
        return (
            json.dumps(
                _canonical_copy(value, set()),
                ensure_ascii=False,
                allow_nan=False,
                separators=(",", ":"),
            ).encode("utf-8", "strict")
            + b"\n"
        )
    except AuthorityError:
        raise
    except (TypeError, ValueError, UnicodeError) as exc:
        raise AuthorityError("canonical_json_encoding_failed") from exc


def canonical_sha256(value: object) -> str:
    return sha256_hex(canonical_json_lf(value))


def decode_base64(value: object, *, label: str, maximum_size: int) -> bytes:
    text = require_exact_text(value, label=label, maximum_length=4 * maximum_size + 8)
    try:
        raw = base64.b64decode(text, validate=True)
    except (ValueError, binascii.Error) as exc:
        raise AuthorityError(f"{label}_base64_invalid") from exc
    if len(raw) > maximum_size:
        raise AuthorityError(f"{label}_base64_size_exceeded")
    return raw


def encode_base64url_nopad(raw: bytes) -> str:
    if type(raw) is not bytes:
        raise AuthorityError("base64url_input_not_exact_bytes")
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def decode_base64url_nopad(
    value: object,
    *,
    label: str,
    expected_size: int | None = None,
) -> bytes:
    text = require_exact_text(value, label=label, maximum_length=4096)
    if "=" in text or _BASE64URL.fullmatch(text) is None:
        raise AuthorityError(f"{label}_base64url_invalid")
    try:
        raw = base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))
    except (ValueError, binascii.Error) as exc:
        raise AuthorityError(f"{label}_base64url_invalid") from exc
    if expected_size is not None and len(raw) != expected_size:
        raise AuthorityError(f"{label}_base64url_size_invalid")
    if encode_base64url_nopad(raw) != text:
        raise AuthorityError(f"{label}_base64url_not_canonical")
    return raw


__all__ = [
    "AuthorityError",
    "canonical_json_lf",
    "canonical_sha256",
    "decode_base64",
    "decode_base64url_nopad",
    "encode_base64url_nopad",
    "exact_list",
    "exact_object",
    "require_exact_bool",
    "require_exact_int",
    "require_exact_keys",
    "require_exact_text",
    "require_https_url",
    "require_sha256",
    "require_size",
    "sha256_hex",
    "strict_json_object",
    "strict_json_value",
]

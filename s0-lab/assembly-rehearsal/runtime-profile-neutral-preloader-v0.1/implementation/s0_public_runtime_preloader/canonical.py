"""Canonical public JSON and manifest primitives with duplicate rejection."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import PurePosixPath
from types import MappingProxyType
from typing import Mapping

from .errors import RuntimeProfileError


_MANIFEST_ROW = re.compile(rb"^([0-9a-f]{64})  ([A-Za-z0-9._/-]+)$")
_SHA256 = re.compile(r"^[0-9a-f]{64}$")


def sha256_bytes(raw: bytes) -> str:
    if type(raw) is not bytes:
        raise TypeError("hash input must be exact bytes")
    return hashlib.sha256(raw).hexdigest()


def require_sha256(value: str, label: str) -> str:
    if type(value) is not str or _SHA256.fullmatch(value) is None:
        raise RuntimeProfileError(f"{label} is not one lowercase SHA-256")
    return value


def _no_duplicate_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise RuntimeProfileError("JSON contains a duplicate object key")
        result[key] = value
    return result


def _reject_nonfinite(value: str) -> object:
    raise RuntimeProfileError(f"JSON contains forbidden non-finite number: {value}")


def load_json_bytes(raw: bytes, *, canonical: bool) -> object:
    if type(raw) is not bytes or not raw or raw.startswith(b"\xef\xbb\xbf"):
        raise RuntimeProfileError("JSON bytes are absent or BOM-prefixed")
    if b"\r" in raw or not raw.endswith(b"\n"):
        raise RuntimeProfileError("JSON bytes are not LF-only with final LF")
    try:
        text = raw.decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise RuntimeProfileError("JSON bytes are not strict UTF-8") from exc
    if any(line.endswith((" ", "\t")) for line in text.splitlines()):
        raise RuntimeProfileError("JSON contains trailing whitespace")
    try:
        value = json.loads(
            text,
            object_pairs_hook=_no_duplicate_object,
            parse_constant=_reject_nonfinite,
        )
    except (json.JSONDecodeError, RuntimeProfileError) as exc:
        if isinstance(exc, RuntimeProfileError):
            raise
        raise RuntimeProfileError("JSON is not syntactically valid") from exc
    if canonical and canonical_json_bytes(value) != raw:
        raise RuntimeProfileError("JSON is not canonical ASCII JSON")
    return value


def canonical_json_bytes(value: object) -> bytes:
    try:
        return (
            json.dumps(
                value,
                allow_nan=False,
                ensure_ascii=True,
                sort_keys=True,
                separators=(",", ":"),
            )
            + "\n"
        ).encode("ascii")
    except (TypeError, ValueError, UnicodeEncodeError) as exc:
        raise RuntimeProfileError("value is not canonical public JSON") from exc


def safe_virtual_path(value: str) -> str:
    if type(value) is not str or not value or "\\" in value or "\x00" in value:
        raise RuntimeProfileError("virtual path is not canonical POSIX text")
    pure = PurePosixPath(value)
    if (
        pure.is_absolute()
        or value.startswith("/")
        or value.endswith("/")
        or "//" in value
        or any(part in {"", ".", ".."} or ":" in part for part in pure.parts)
    ):
        raise RuntimeProfileError("virtual path escapes its public namespace")
    return value


def parse_manifest(raw: bytes, *, expected_rows: int | None = None) -> Mapping[str, str]:
    if type(raw) is not bytes or raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw:
        raise RuntimeProfileError("manifest bytes are not canonical")
    if not raw.endswith(b"\n") or not raw:
        raise RuntimeProfileError("manifest lacks its final LF")
    entries: dict[str, str] = {}
    previous: str | None = None
    for line in raw[:-1].split(b"\n"):
        match = _MANIFEST_ROW.fullmatch(line)
        if match is None:
            raise RuntimeProfileError("manifest row is not canonical")
        digest = match.group(1).decode("ascii")
        path = safe_virtual_path(match.group(2).decode("ascii"))
        if path in entries or (previous is not None and path <= previous):
            raise RuntimeProfileError("manifest rows are not unique ASCII-sorted paths")
        entries[path] = digest
        previous = path
    if not entries or (expected_rows is not None and len(entries) != expected_rows):
        raise RuntimeProfileError("manifest row count is not exact")
    return MappingProxyType(entries)

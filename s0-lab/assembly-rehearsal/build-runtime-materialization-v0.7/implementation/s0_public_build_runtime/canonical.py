"""Strict bytes, JSON, digest, and path primitives."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from .errors import CanonicalError

_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_MANIFEST_ROW = re.compile(rb"^([0-9a-f]{64})  ([A-Za-z0-9._/-]+)$")


def sha256_hex(raw: bytes) -> str:
    if type(raw) is not bytes:
        raise CanonicalError("hash input must be exact bytes")
    return hashlib.sha256(raw).hexdigest()


def hash_file_object(handle: object, *, maximum_bytes: int | None = None) -> tuple[int, str]:
    if type(maximum_bytes) not in {int, type(None)} or type(maximum_bytes) is bool:
        raise CanonicalError("file hash bound type differs")
    if maximum_bytes is not None and maximum_bytes < 0:
        raise CanonicalError("file hash bound is negative")
    digest = hashlib.sha256()
    total = 0
    handle.seek(0)
    while True:
        chunk = handle.read(1024 * 1024)
        if not chunk:
            break
        if type(chunk) is not bytes:
            raise CanonicalError("file returned non-byte content")
        total += len(chunk)
        if maximum_bytes is not None and total > maximum_bytes:
            raise CanonicalError("file exceeds its byte bound")
        digest.update(chunk)
    handle.seek(0)
    return total, digest.hexdigest()


def require_sha256(value: object) -> str:
    if type(value) is not str or _SHA256.fullmatch(value) is None:
        raise CanonicalError("SHA-256 must be lowercase hexadecimal text")
    return value


def strict_json(raw: bytes) -> object:
    if type(raw) is not bytes or not raw or not raw.endswith(b"\n"):
        raise CanonicalError("JSON must be nonempty exact bytes with one final LF")
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw or b"\x00" in raw:
        raise CanonicalError("JSON contains a forbidden byte")
    try:
        text = raw.decode("utf-8", "strict")
    except UnicodeDecodeError as error:
        raise CanonicalError("JSON is not strict UTF-8") from error
    if any(line.endswith((" ", "\t")) for line in text.splitlines()):
        raise CanonicalError("JSON contains trailing line whitespace")

    def pairs(values: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in values:
            if type(key) is not str or key in result:
                raise CanonicalError("JSON object key is not unique exact text")
            result[key] = value
        return result

    try:
        return json.loads(
            text,
            object_pairs_hook=pairs,
            parse_constant=lambda value: (_ for _ in ()).throw(
                CanonicalError(f"nonfinite JSON value is forbidden: {value}")
            ),
        )
    except CanonicalError:
        raise
    except (TypeError, ValueError, json.JSONDecodeError) as error:
        raise CanonicalError("JSON parse failed") from error


def _jcs_value(value: object) -> object:
    if value is None or type(value) in {bool, str}:
        return value
    if type(value) is int:
        if not -(2**53 - 1) <= value <= 2**53 - 1:
            raise CanonicalError("integer is outside the exact JCS range")
        return value
    if type(value) is list or type(value) is tuple:
        return [_jcs_value(item) for item in value]
    if type(value) is dict:
        if any(type(key) is not str for key in value):
            raise CanonicalError("JCS key must be exact text")
        try:
            keys = sorted(value, key=lambda key: key.encode("utf-16-be", "strict"))
        except UnicodeEncodeError as error:
            raise CanonicalError("JCS key is invalid Unicode") from error
        return {key: _jcs_value(value[key]) for key in keys}
    raise CanonicalError("unsupported JCS value type")


def jcs_lf(value: object) -> bytes:
    try:
        return json.dumps(
            _jcs_value(value),
            ensure_ascii=False,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8", "strict") + b"\n"
    except (TypeError, ValueError, UnicodeError) as error:
        raise CanonicalError("JCS encoding failed") from error


def parse_hash_manifest(raw: bytes, *, expected_rows: int) -> tuple[tuple[str, str], ...]:
    if type(expected_rows) is not int or type(expected_rows) is bool or expected_rows <= 0:
        raise CanonicalError("manifest row bound differs")
    if not raw.endswith(b"\n") or raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw:
        raise CanonicalError("manifest byte grammar differs")
    lines = raw[:-1].split(b"\n")
    if len(lines) != expected_rows:
        raise CanonicalError("manifest row count differs")
    result: list[tuple[str, str]] = []
    for line in lines:
        match = _MANIFEST_ROW.fullmatch(line)
        if match is None:
            raise CanonicalError("manifest row grammar differs")
        result.append((match.group(1).decode("ascii"), match.group(2).decode("ascii")))
    if len({path for _, path in result}) != len(result):
        raise CanonicalError("manifest paths are not unique")
    return tuple(result)


def read_exact(path: Path, *, maximum_bytes: int) -> bytes:
    if not isinstance(path, Path) or type(maximum_bytes) is not int or type(maximum_bytes) is bool or maximum_bytes <= 0:
        raise CanonicalError("bounded read arguments differ")
    with path.open("rb") as handle:
        raw = handle.read(maximum_bytes + 1)
        if len(raw) > maximum_bytes or handle.read(1):
            raise CanonicalError("file exceeds its byte bound")
    return raw


def sidecar_bytes(filename: str, digest: str) -> bytes:
    require_sha256(digest)
    if type(filename) is not str or not filename or any(ch in filename for ch in "/\\\r\n\x00"):
        raise CanonicalError("sidecar filename differs")
    try:
        return f"{digest}  {filename}\n".encode("ascii", "strict")
    except UnicodeEncodeError as error:
        raise CanonicalError("sidecar filename is not ASCII") from error

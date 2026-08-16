"""Pure byte-level codecs used before any candidate execution authority exists."""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from types import MappingProxyType
from typing import Iterable, Mapping

from .errors import CanonicalError

_SHA256 = re.compile(r"^[0-9a-f]{64}$")
_VIRTUAL_PATH = re.compile(r"^[A-Za-z0-9._-]+(?:/[A-Za-z0-9._-]+)*$")


def sha256_hex(raw: bytes) -> str:
    if type(raw) is not bytes:
        raise CanonicalError("hash input must be exact bytes")
    return hashlib.sha256(raw).hexdigest()


def require_sha256(value: str, *, nonzero: bool = False) -> str:
    if type(value) is not str or _SHA256.fullmatch(value) is None:
        raise CanonicalError("SHA-256 must be exact lowercase hexadecimal text")
    if nonzero and value == "0" * 64:
        raise CanonicalError("SHA-256 must be nonzero")
    return value


def strict_json(raw: bytes) -> object:
    if type(raw) is not bytes or not raw or not raw.endswith(b"\n"):
        raise CanonicalError("JSON must be nonempty exact bytes with final LF")
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


def _require_jcs_value(value: object) -> None:
    if value is None or type(value) in {bool, str}:
        return
    if type(value) is int:
        if not -(2**53 - 1) <= value <= 2**53 - 1:
            raise CanonicalError("integer is outside the exact JCS-safe range")
        return
    if type(value) is list:
        for item in value:
            _require_jcs_value(item)
        return
    if type(value) is dict:
        for key, item in value.items():
            if type(key) is not str:
                raise CanonicalError("JCS object key must be exact text")
            _require_jcs_value(item)
        return
    raise CanonicalError("unsupported JCS value type")


def jcs_lf(value: object) -> bytes:
    """RFC 8785-compatible for this contract's integer/ASCII JSON domain."""

    _require_jcs_value(value)
    try:
        encoded = json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8", "strict")
    except (UnicodeError, ValueError, TypeError) as error:
        raise CanonicalError("JCS encoding failed") from error
    return encoded + b"\n"


def deep_freeze(value: object) -> object:
    """Return an exact recursively immutable copy of a JSON-domain value."""

    if value is None or type(value) in {bool, int, str, bytes}:
        return value
    if type(value) is list or type(value) is tuple:
        return tuple(deep_freeze(item) for item in value)
    if type(value) is dict or type(value) is type(MappingProxyType({})):
        frozen: dict[str, object] = {}
        for key, item in value.items():
            if type(key) is not str:
                raise CanonicalError("immutable mapping key must be exact text")
            frozen[key] = deep_freeze(item)
        return MappingProxyType(frozen)
    raise CanonicalError("unsupported immutable value type")


def deep_thaw_json(value: object) -> object:
    """Return an exact mutable JSON-domain copy for canonical serialization."""

    if value is None or type(value) in {bool, int, str}:
        return value
    if type(value) is tuple:
        return [deep_thaw_json(item) for item in value]
    if type(value) is type(MappingProxyType({})):
        return {key: deep_thaw_json(item) for key, item in value.items()}
    raise CanonicalError("value is not an exact deeply frozen JSON value")


def semantic_relations_preimage(relations: Iterable[str]) -> bytes:
    exact = tuple(relations)
    if len(exact) != 68 or any(type(value) is not str for value in exact):
        raise CanonicalError("effective relation inventory must contain 68 exact strings")
    if len(set(exact)) != len(exact):
        raise CanonicalError("effective relation inventory contains duplicates")
    lines = ["S0-BRM-SEMANTIC-RELATIONS-5", "relation_count=68"]
    for index, relation in enumerate(exact):
        try:
            relation.encode("ascii", "strict")
        except UnicodeEncodeError as error:
            raise CanonicalError("semantic relation is not ASCII") from error
        if not relation or any(character in relation for character in "\r\n\t "):
            raise CanonicalError("semantic relation is not one exact token")
        lines.extend((f"index={index}", f"relation={relation}"))
    return ("\n".join(lines) + "\n").encode("ascii")


def canonical_virtual_path(path: str) -> str:
    if type(path) is not str or not path:
        raise CanonicalError("virtual path is not nonempty bounded ASCII")
    try:
        encoded = path.encode("ascii", "strict")
    except UnicodeEncodeError as error:
        raise CanonicalError("virtual path is not nonempty bounded ASCII") from error
    if len(encoded) > 1024:
        raise CanonicalError("virtual path is not nonempty bounded ASCII")
    if _VIRTUAL_PATH.fullmatch(path) is None or "\\" in path or ":" in path:
        raise CanonicalError("virtual path grammar is invalid")
    reserved = {"con", "prn", "aux", "nul"}
    reserved.update(f"com{number}" for number in range(1, 10))
    reserved.update(f"lpt{number}" for number in range(1, 10))
    for segment in path.split("/"):
        if segment in {".", ".."} or segment.endswith("."):
            raise CanonicalError("virtual path segment is invalid")
        if segment.split(".", 1)[0].lower() in reserved:
            raise CanonicalError("virtual path uses a reserved Windows name")
    return path


@dataclass(frozen=True)
class TargetRow:
    path: str
    byte_length: int
    sha256: str

    def __post_init__(self) -> None:
        canonical_virtual_path(self.path)
        if type(self.byte_length) is not int or type(self.byte_length) is bool or self.byte_length < 0:
            raise CanonicalError("target byte length is invalid")
        require_sha256(self.sha256)


def target_set_preimage(rows: Iterable[TargetRow]) -> bytes:
    exact = tuple(rows)
    if not exact:
        raise CanonicalError("target set is empty")
    paths = tuple(row.path for row in exact)
    if paths != tuple(sorted(paths, key=lambda value: value.encode("ascii"))) or len(set(paths)) != len(paths):
        raise CanonicalError("target rows are not unique unsigned-ASCII path order")
    lines = [
        "schema_id=S0-BRM-TARGET-SET-PREIMAGE-1",
        f"target_count={len(exact)}",
        f"total_target_bytes={sum(row.byte_length for row in exact)}",
    ]
    for row in exact:
        lines.extend(
            (
                f"path_byte_length={len(row.path.encode('ascii'))}",
                f"path={row.path}",
                f"target_byte_length={row.byte_length}",
                f"target_sha256={row.sha256}",
            )
        )
    return ("\n".join(lines) + "\n").encode("ascii")


def freeze_exact_mapping(value: Mapping[str, bytes]) -> dict[str, bytes]:
    if type(value) is not dict:
        raise CanonicalError("byte mapping must be an exact dict")
    items = tuple(value.items())
    if any(type(key) is not str or type(raw) is not bytes for key, raw in items):
        raise CanonicalError("byte mapping entries must be exact string-to-bytes pairs")
    frozen = dict(items)
    if len(frozen) != len(items):
        raise CanonicalError("byte mapping keys are not unique")
    return frozen

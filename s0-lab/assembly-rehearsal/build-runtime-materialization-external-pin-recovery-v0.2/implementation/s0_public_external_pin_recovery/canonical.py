"""Strict JSON canonicalization and hashing for implementation v0.2."""

from __future__ import annotations

import hashlib
import json
from typing import TypeAlias


JsonScalar: TypeAlias = bool | int | str | None
JsonValue: TypeAlias = JsonScalar | list["JsonValue"] | dict[str, "JsonValue"]


def validate_json_value(value: object) -> None:
    """Validate an exact, unaliased tree of built-in JSON value types.

    Floats, non-string dictionary keys, subclasses of supported built-ins,
    cycles, and shared list or dictionary instances are rejected.
    """

    seen_containers: set[int] = set()

    def validate(item: object, path: str) -> None:
        item_type = type(item)

        if item is None or item_type is bool or item_type is int or item_type is str:
            return

        if item_type is list:
            identity = id(item)
            if identity in seen_containers:
                raise ValueError(f"aliased or cyclic JSON container at {path}")
            seen_containers.add(identity)
            for index, child in enumerate(item):
                validate(child, f"{path}[{index}]")
            return

        if item_type is dict:
            identity = id(item)
            if identity in seen_containers:
                raise ValueError(f"aliased or cyclic JSON container at {path}")
            seen_containers.add(identity)
            for key, child in item.items():
                if type(key) is not str:
                    raise TypeError(f"JSON object key at {path} is not an exact string")
                validate(child, f"{path}[{key!r}]")
            return

        raise TypeError(f"unsupported JSON value type at {path}: {item_type.__name__}")

    validate(value, "$")


def canonical_json_bytes(value: object) -> bytes:
    """Return deterministic compact UTF-8 JSON after strict validation."""

    validate_json_value(value)
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def sha256_hex(data: bytes) -> str:
    """Return the lowercase hexadecimal SHA-256 digest of exact bytes."""

    if type(data) is not bytes:
        raise TypeError("SHA-256 input must be exact bytes")
    return hashlib.sha256(data).hexdigest()


def canonical_sha256(value: object) -> str:
    """Return the SHA-256 digest of a value's canonical JSON bytes."""

    return sha256_hex(canonical_json_bytes(value))

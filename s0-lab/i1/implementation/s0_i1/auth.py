"""Read-once authentication for frozen public bytes.

The bytes returned by this module are the bytes that were hashed.  Consumers
must parse ``AuthenticatedBytes.raw`` and never reopen the path.  This removes
the authenticate-then-reopen TOCTOU pattern.  Path checks also reject explicit
traversal, symbolic links, and Windows reparse points where the host exposes
that metadata.
"""

from __future__ import annotations

import hashlib
import os
import re
import stat
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Mapping

from .errors import AuthenticationError, UnsafePathError


_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_MANIFEST_LINE = re.compile(rb"^([0-9a-f]{64})  ([A-Za-z0-9._/-]+)$")
_REPARSE_ATTRIBUTE = 0x400
_AUTHENTICATED_PROVENANCE = object()


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


@dataclass(frozen=True, init=False)
class AuthenticatedBytes:
    """An immutable same-bytes authentication result."""

    relative_path: str
    sha256: str
    raw: bytes
    authority_sha256: str
    authority_kind: str
    _provenance: object = field(repr=False, compare=False)

    def __init__(
        self,
        relative_path: str,
        sha256: str,
        raw: bytes,
        authority_sha256: str,
        authority_kind: str,
        *,
        _provenance: object,
    ) -> None:
        if _provenance is not _AUTHENTICATED_PROVENANCE:
            raise AuthenticationError("AuthenticatedBytes must come from an authenticated reader")
        object.__setattr__(self, "relative_path", relative_path)
        object.__setattr__(self, "sha256", sha256)
        object.__setattr__(self, "raw", raw)
        object.__setattr__(self, "authority_sha256", authority_sha256)
        object.__setattr__(self, "authority_kind", authority_kind)
        object.__setattr__(self, "_provenance", _provenance)


@dataclass(frozen=True)
class _ReadBytes:
    relative_path: str
    sha256: str
    raw: bytes


def has_authenticated_provenance(value: object) -> bool:
    return (
        isinstance(value, AuthenticatedBytes)
        and getattr(value, "_provenance", None) is _AUTHENTICATED_PROVENANCE
    )


def _authenticated(
    read: _ReadBytes, *, authority_sha256: str, authority_kind: str
) -> AuthenticatedBytes:
    return AuthenticatedBytes(
        read.relative_path,
        read.sha256,
        read.raw,
        authority_sha256,
        authority_kind,
        _provenance=_AUTHENTICATED_PROVENANCE,
    )


@dataclass(frozen=True)
class ManifestAnchor:
    """An exact public manifest identity and entry namespace."""

    manifest_path: str
    manifest_sha256: str
    entry_prefix: str

    def __post_init__(self) -> None:
        _safe_relative(self.manifest_path)
        if not _HEX64.fullmatch(self.manifest_sha256):
            raise AuthenticationError("manifest anchor digest must be lowercase SHA-256")
        prefix = _safe_relative(self.entry_prefix.rstrip("/")) + "/"
        object.__setattr__(self, "entry_prefix", prefix)


@dataclass(frozen=True)
class AuthenticatedManifest:
    anchor: ManifestAnchor
    manifest: AuthenticatedBytes
    entries: Mapping[str, str]


def _safe_relative(value: str | Path) -> str:
    raw = str(value)
    if not raw or "\\" in raw or "\x00" in raw:
        raise UnsafePathError("path must be non-empty canonical POSIX-relative text")
    pure = PurePosixPath(raw)
    if pure.is_absolute() or raw.startswith("/"):
        raise UnsafePathError("absolute paths are forbidden")
    if any(part in {"", ".", ".."} for part in pure.parts):
        raise UnsafePathError("path traversal or normalization is forbidden")
    if any(":" in part for part in pure.parts):
        raise UnsafePathError("drive-qualified and alternate-stream paths are forbidden")
    canonical = pure.as_posix()
    if canonical != raw:
        raise UnsafePathError("path must already be canonical POSIX-relative text")
    return canonical


def _is_reparse(info: os.stat_result) -> bool:
    attributes = getattr(info, "st_file_attributes", 0)
    return stat.S_ISLNK(info.st_mode) or bool(attributes & _REPARSE_ATTRIBUTE)


def _checked_candidate(workspace_root: Path, relative: str) -> tuple[Path, os.stat_result]:
    root = workspace_root.resolve(strict=True)
    if not root.is_dir():
        raise UnsafePathError("workspace root is not a directory")
    current = root
    for component in PurePosixPath(relative).parts:
        current = current / component
        try:
            info = os.lstat(current)
        except FileNotFoundError as exc:
            raise UnsafePathError("workspace-relative input does not exist") from exc
        except OSError as exc:
            raise UnsafePathError("workspace-relative path could not be inspected") from exc
        if _is_reparse(info):
            raise UnsafePathError("symbolic-link or reparse-backed paths are forbidden")
    try:
        resolved = current.resolve(strict=True)
        resolved.relative_to(root)
    except (OSError, ValueError) as exc:
        raise UnsafePathError("path escapes the workspace") from exc
    if resolved != current:
        raise UnsafePathError("path substitution through an alias is forbidden")
    final_info = os.lstat(current)
    if not stat.S_ISREG(final_info.st_mode):
        raise UnsafePathError("authenticated input must be a regular file")
    return current, final_info


def _same_identity(left: os.stat_result, right: os.stat_result) -> bool:
    left_key = (getattr(left, "st_dev", 0), getattr(left, "st_ino", 0))
    right_key = (getattr(right, "st_dev", 0), getattr(right, "st_ino", 0))
    if left_key != (0, 0) and right_key != (0, 0):
        return left_key == right_key
    return (
        left.st_size,
        getattr(left, "st_mtime_ns", int(left.st_mtime * 1_000_000_000)),
    ) == (
        right.st_size,
        getattr(right, "st_mtime_ns", int(right.st_mtime * 1_000_000_000)),
    )


def _read_once(workspace_root: Path, value: str | Path, *, max_bytes: int | None = None) -> _ReadBytes:
    relative = _safe_relative(value)
    candidate, path_info = _checked_candidate(workspace_root, relative)
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_CLOEXEC", 0)
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(candidate, flags)
    except OSError as exc:
        raise UnsafePathError("authenticated input could not be opened safely") from exc
    try:
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode) or not _same_identity(path_info, before):
            raise UnsafePathError("path changed before authenticated open")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(descriptor, 65536)
            if not chunk:
                break
            total += len(chunk)
            if max_bytes is not None and total > max_bytes:
                raise AuthenticationError("authenticated input exceeds its byte ceiling")
            chunks.append(chunk)
        after = os.fstat(descriptor)
        if not _same_identity(before, after) or before.st_size != after.st_size:
            raise UnsafePathError("authenticated input changed during read")
    finally:
        os.close(descriptor)
    raw = b"".join(chunks)
    if len(raw) != before.st_size:
        raise UnsafePathError("authenticated input length changed during read")
    return _ReadBytes(relative, sha256_bytes(raw), raw)


def load_authenticated_manifest(workspace_root: Path, anchor: ManifestAnchor) -> AuthenticatedManifest:
    """Authenticate and parse one exact public manifest without reopening it."""

    read = _read_once(workspace_root, anchor.manifest_path)
    if read.sha256 != anchor.manifest_sha256:
        raise AuthenticationError("manifest anchor hash mismatch")
    manifest = _authenticated(
        read,
        authority_sha256=anchor.manifest_sha256,
        authority_kind="manifest-anchor",
    )
    if b"\r" in manifest.raw or manifest.raw.startswith(b"\xef\xbb\xbf"):
        raise AuthenticationError("manifest must be BOM-free LF-only ASCII")
    if not manifest.raw.endswith(b"\n"):
        raise AuthenticationError("manifest must end in LF")
    entries: dict[str, str] = {}
    for line in manifest.raw[:-1].split(b"\n"):
        match = _MANIFEST_LINE.fullmatch(line)
        if match is None:
            raise AuthenticationError("invalid manifest line")
        digest = match.group(1).decode("ascii")
        relative = _safe_relative(match.group(2).decode("ascii"))
        if not relative.startswith(anchor.entry_prefix):
            raise AuthenticationError("manifest entry escapes its frozen namespace")
        if relative == anchor.manifest_path or relative in entries:
            raise AuthenticationError("manifest contains a self-entry or duplicate path")
        entries[relative] = digest
    if not entries:
        raise AuthenticationError("manifest must contain at least one entry")
    return AuthenticatedManifest(anchor, manifest, MappingProxyType(entries))


def authenticate_manifest_entry(
    workspace_root: Path,
    manifest: AuthenticatedManifest,
    value: str | Path,
    *,
    max_bytes: int | None = None,
) -> AuthenticatedBytes:
    """Read once, authenticate, and return the exact bytes to be consumed."""

    relative = _safe_relative(value)
    expected = manifest.entries.get(relative)
    if expected is None:
        raise AuthenticationError("path is not in the authenticated public manifest")
    read = _read_once(workspace_root, relative, max_bytes=max_bytes)
    if read.sha256 != expected:
        raise AuthenticationError("authenticated public file hash mismatch")
    return _authenticated(
        read,
        authority_sha256=manifest.manifest.sha256,
        authority_kind="manifest-entry",
    )


def authenticate_manifest_file_set(
    workspace_root: Path, manifest: AuthenticatedManifest
) -> Mapping[str, AuthenticatedBytes]:
    """Authenticate the complete manifest namespace and reject extra files."""

    prefix_path = workspace_root / PurePosixPath(manifest.anchor.entry_prefix.rstrip("/"))
    if not prefix_path.is_dir():
        raise AuthenticationError("manifest namespace directory is missing")
    discovered: set[str] = set()
    for path in prefix_path.rglob("*"):
        relative = path.relative_to(workspace_root).as_posix()
        if path.is_symlink() or _is_reparse(os.lstat(path)):
            raise UnsafePathError("manifest namespace contains a reparse-backed path")
        if path.is_file() and relative != manifest.anchor.manifest_path:
            discovered.add(relative)
    if discovered != set(manifest.entries):
        raise AuthenticationError("manifest namespace file set mismatch")
    return MappingProxyType(
        {
            relative: authenticate_manifest_entry(workspace_root, manifest, relative)
            for relative in sorted(manifest.entries)
        }
    )

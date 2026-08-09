"""Read-once authentication for frozen public bytes.

Trust is supplied explicitly at this boundary.  An adjacent manifest or a
caller-constructed data object is never a trust root: callers must first bind
the exact out-of-band manifest identity, namespace, allowed paths, and purpose
into an API-level :class:`ManifestGrant`.  Authenticated values retain that exact
capability identity so later policy boundaries can require it.

Complete-namespace authentication performs an enumerate/read/re-enumerate/
rehash/final-enumerate sequence.  The returned bytes are the first bytes that
were authenticated; consumers never reopen their paths.  The final checks make
the successful claim a stable observed snapshot, not a promise that a mutable
filesystem will remain unchanged after return.
"""

from __future__ import annotations

import hashlib
import os
import re
import stat
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Mapping, Sequence

from .errors import AuthenticationError, UnsafePathError


_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_PURPOSE = re.compile(r"^[a-z0-9][a-z0-9._-]{0,127}$")
_MANIFEST_LINE = re.compile(rb"^([0-9a-f]{64})  ([A-Za-z0-9._/-]+)$")
_REPARSE_ATTRIBUTE = 0x400
_GRANT_PROVENANCE = object()
_MANIFEST_PROVENANCE = object()
_AUTHENTICATED_PROVENANCE = object()


def sha256_bytes(raw: bytes) -> str:
    if type(raw) is not bytes:
        raise AuthenticationError("SHA-256 input must be exact bytes")
    return hashlib.sha256(raw).hexdigest()


def _safe_relative(value: str | Path) -> str:
    if type(value) not in {str, Path}:
        raise UnsafePathError("path must be exact string or Path text")
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


def _grant_binding_bytes(
    manifest_path: str,
    manifest_sha256: str,
    entry_prefix: str,
    allowed_paths: tuple[str, ...],
    purpose: str,
) -> bytes:
    lines = [
        "I1-EXTERNAL-MANIFEST-GRANT-1",
        f"manifest_path={manifest_path}",
        f"manifest_sha256={manifest_sha256}",
        f"entry_prefix={entry_prefix}",
        f"purpose={purpose}",
        f"allowed_count={len(allowed_paths)}",
    ]
    lines.extend(f"allowed_{index}={path}" for index, path in enumerate(allowed_paths, 1))
    return ("\n".join(lines) + "\n").encode("ascii")


@dataclass(frozen=True, init=False)
class ManifestGrant:
    """API-level binding of an externally trusted manifest identity and grant."""

    manifest_path: str
    manifest_sha256: str
    entry_prefix: str
    allowed_paths: tuple[str, ...]
    purpose: str
    identity_sha256: str
    _provenance: object = field(repr=False, compare=False)

    def __init__(
        self,
        manifest_path: str,
        manifest_sha256: str,
        entry_prefix: str,
        allowed_paths: tuple[str, ...],
        purpose: str,
        identity_sha256: str,
        *,
        _provenance: object,
    ) -> None:
        if _provenance is not _GRANT_PROVENANCE:
            raise AuthenticationError(
                "ManifestGrant must bind an explicitly supplied trusted identity"
            )
        object.__setattr__(self, "manifest_path", manifest_path)
        object.__setattr__(self, "manifest_sha256", manifest_sha256)
        object.__setattr__(self, "entry_prefix", entry_prefix)
        object.__setattr__(self, "allowed_paths", allowed_paths)
        object.__setattr__(self, "purpose", purpose)
        object.__setattr__(self, "identity_sha256", identity_sha256)
        object.__setattr__(self, "_provenance", _provenance)


def bind_external_manifest_grant(
    *,
    expected_manifest_path: str,
    expected_manifest_sha256: str,
    expected_entry_prefix: str,
    expected_allowed_paths: Sequence[str],
    purpose: str,
) -> ManifestGrant:
    """Bind exact out-of-band trust inputs into an API-level capability.

    This function does not discover or endorse any digest.  Its ``expected_*``
    arguments must come from the independently trusted caller.  Re-hashing a
    nearby manifest and feeding the discovered value back here is self-trust.
    Module-private markers are not a security boundary against hostile code in
    this same Python interpreter; the integration caller must already be trusted.
    """

    if type(expected_manifest_path) is not str:
        raise AuthenticationError("expected manifest path must be exact string text")
    manifest_path = _safe_relative(expected_manifest_path)
    if type(expected_manifest_sha256) is not str or not _HEX64.fullmatch(
        expected_manifest_sha256
    ):
        raise AuthenticationError("expected manifest digest must be lowercase SHA-256")
    if type(expected_entry_prefix) is not str:
        raise AuthenticationError("expected entry prefix must be exact string text")
    prefix = _safe_relative(expected_entry_prefix.rstrip("/")) + "/"
    if type(purpose) is not str or not _PURPOSE.fullmatch(purpose):
        raise AuthenticationError("manifest grant purpose syntax is invalid")
    if isinstance(expected_allowed_paths, (str, bytes)):
        raise AuthenticationError("allowed manifest paths must be a sequence of paths")
    paths = tuple(_safe_relative(path) for path in expected_allowed_paths)
    if not paths or paths != tuple(sorted(paths)) or len(paths) != len(set(paths)):
        raise AuthenticationError(
            "allowed manifest paths must be non-empty, unique, and sorted"
        )
    if any(not path.startswith(prefix) or path == manifest_path for path in paths):
        raise AuthenticationError("allowed manifest path escapes its exact namespace")
    binding = _grant_binding_bytes(
        manifest_path,
        expected_manifest_sha256,
        prefix,
        paths,
        purpose,
    )
    return ManifestGrant(
        manifest_path,
        expected_manifest_sha256,
        prefix,
        paths,
        purpose,
        hashlib.sha256(binding).hexdigest(),
        _provenance=_GRANT_PROVENANCE,
    )


def require_manifest_grant(grant: object) -> ManifestGrant:
    if type(grant) is not ManifestGrant or getattr(grant, "_provenance", None) is not _GRANT_PROVENANCE:
        raise AuthenticationError("manifest grant provenance is invalid")
    paths = getattr(grant, "allowed_paths", ())
    if type(paths) is not tuple:
        raise AuthenticationError("manifest grant path inventory is not immutable")
    expected_binding = _grant_binding_bytes(
        grant.manifest_path,
        grant.manifest_sha256,
        grant.entry_prefix,
        paths,
        grant.purpose,
    )
    if hashlib.sha256(expected_binding).hexdigest() != grant.identity_sha256:
        raise AuthenticationError("manifest grant binding digest mismatch")
    return grant


@dataclass(frozen=True, init=False)
class AuthenticatedBytes:
    """Immutable same-bytes result bound to one exact external grant."""

    relative_path: str
    sha256: str
    raw: bytes
    authority_sha256: str
    authority_path: str
    authority_kind: str
    grant_purpose: str
    grant_identity_sha256: str
    _grant: ManifestGrant = field(repr=False, compare=False)
    _provenance: object = field(repr=False, compare=False)

    def __init__(
        self,
        relative_path: str,
        sha256: str,
        raw: bytes,
        authority_sha256: str,
        authority_path: str,
        authority_kind: str,
        grant_purpose: str,
        grant_identity_sha256: str,
        *,
        _grant: ManifestGrant,
        _provenance: object,
    ) -> None:
        if _provenance is not _AUTHENTICATED_PROVENANCE:
            raise AuthenticationError(
                "AuthenticatedBytes must come from an authenticated reader"
            )
        require_manifest_grant(_grant)
        object.__setattr__(self, "relative_path", relative_path)
        object.__setattr__(self, "sha256", sha256)
        object.__setattr__(self, "raw", raw)
        object.__setattr__(self, "authority_sha256", authority_sha256)
        object.__setattr__(self, "authority_path", authority_path)
        object.__setattr__(self, "authority_kind", authority_kind)
        object.__setattr__(self, "grant_purpose", grant_purpose)
        object.__setattr__(self, "grant_identity_sha256", grant_identity_sha256)
        object.__setattr__(self, "_grant", _grant)
        object.__setattr__(self, "_provenance", _provenance)


@dataclass(frozen=True)
class _ReadBytes:
    relative_path: str
    sha256: str
    raw: bytes


def has_authenticated_provenance(
    value: object,
    *,
    required_grant: ManifestGrant | None = None,
    expected_authority_sha256: str | None = None,
    expected_authority_path: str | None = None,
    expected_relative_path: str | None = None,
    expected_purpose: str | None = None,
) -> bool:
    if type(value) is not AuthenticatedBytes:
        return False
    if getattr(value, "_provenance", None) is not _AUTHENTICATED_PROVENANCE:
        return False
    try:
        grant = require_manifest_grant(getattr(value, "_grant", None))
    except AuthenticationError:
        return False
    if required_grant is not None and grant is not required_grant:
        return False
    checks = (
        (expected_authority_sha256, value.authority_sha256),
        (expected_authority_path, value.authority_path),
        (expected_relative_path, value.relative_path),
        (expected_purpose, value.grant_purpose),
    )
    if any(expected is not None and expected != actual for expected, actual in checks):
        return False
    if value.authority_kind == "manifest-anchor":
        path_is_granted = value.relative_path == grant.manifest_path
    elif value.authority_kind == "manifest-entry":
        path_is_granted = value.relative_path in grant.allowed_paths
    else:
        path_is_granted = False
    if (
        value.authority_sha256 != grant.manifest_sha256
        or value.authority_path != grant.manifest_path
        or value.grant_purpose != grant.purpose
        or value.grant_identity_sha256 != grant.identity_sha256
        or not path_is_granted
        or type(value.raw) is not bytes
        or type(value.sha256) is not str
        or value.sha256 != hashlib.sha256(value.raw).hexdigest()
    ):
        return False
    return True


def _authenticated(read: _ReadBytes, *, grant: ManifestGrant, authority_kind: str) -> AuthenticatedBytes:
    require_manifest_grant(grant)
    return AuthenticatedBytes(
        read.relative_path,
        read.sha256,
        read.raw,
        grant.manifest_sha256,
        grant.manifest_path,
        authority_kind,
        grant.purpose,
        grant.identity_sha256,
        _grant=grant,
        _provenance=_AUTHENTICATED_PROVENANCE,
    )


@dataclass(frozen=True, init=False)
class AuthenticatedManifest:
    grant: ManifestGrant
    manifest: AuthenticatedBytes
    entries: Mapping[str, str]
    entries_sha256: str
    _provenance: object = field(repr=False, compare=False)

    def __init__(
        self,
        grant: ManifestGrant,
        manifest: AuthenticatedBytes,
        entries: Mapping[str, str],
        entries_sha256: str,
        *,
        _provenance: object,
    ) -> None:
        if _provenance is not _MANIFEST_PROVENANCE:
            raise AuthenticationError(
                "AuthenticatedManifest must come from an authenticated reader"
            )
        require_manifest_grant(grant)
        object.__setattr__(self, "grant", grant)
        object.__setattr__(self, "manifest", manifest)
        object.__setattr__(self, "entries", entries)
        object.__setattr__(self, "entries_sha256", entries_sha256)
        object.__setattr__(self, "_provenance", _provenance)


def _entries_binding(entries: Mapping[str, str]) -> bytes:
    return b"".join(
        f"{digest}  {relative}\n".encode("ascii")
        for relative, digest in sorted(entries.items())
    )


def _require_authenticated_manifest(value: object) -> AuthenticatedManifest:
    if type(value) is not AuthenticatedManifest or getattr(value, "_provenance", None) is not _MANIFEST_PROVENANCE:
        raise AuthenticationError("authenticated manifest provenance is invalid")
    grant = require_manifest_grant(value.grant)
    if not has_authenticated_provenance(
        value.manifest,
        required_grant=grant,
        expected_authority_sha256=grant.manifest_sha256,
        expected_authority_path=grant.manifest_path,
        expected_relative_path=grant.manifest_path,
        expected_purpose=grant.purpose,
    ):
        raise AuthenticationError("authenticated manifest binding is invalid")
    if not isinstance(value.entries, MappingProxyType):
        raise AuthenticationError("authenticated manifest entries are not immutable")
    if tuple(sorted(value.entries)) != grant.allowed_paths:
        raise AuthenticationError("authenticated manifest grant inventory mismatch")
    if hashlib.sha256(_entries_binding(value.entries)).hexdigest() != value.entries_sha256:
        raise AuthenticationError("authenticated manifest entry binding changed")
    return value


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


def _checked_directory(workspace_root: Path, relative: str) -> Path:
    root = workspace_root.resolve(strict=True)
    current = root
    for component in PurePosixPath(relative).parts:
        current = current / component
        try:
            info = os.lstat(current)
        except OSError as exc:
            raise UnsafePathError("manifest namespace directory could not be inspected") from exc
        if _is_reparse(info):
            raise UnsafePathError("manifest namespace contains a reparse-backed path")
        if not stat.S_ISDIR(info.st_mode):
            raise UnsafePathError("manifest namespace component is not a directory")
    if current.resolve(strict=True) != current:
        raise UnsafePathError("manifest namespace directory is substituted")
    return current


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


def _read_once(
    workspace_root: Path, value: str | Path, *, max_bytes: int | None = None
) -> _ReadBytes:
    if max_bytes is not None and (type(max_bytes) is not int or max_bytes < 0):
        raise AuthenticationError("authenticated byte ceiling must be an exact nonnegative integer")
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
    return _ReadBytes(relative, hashlib.sha256(raw).hexdigest(), raw)


def _enumerate_namespace(workspace_root: Path, manifest: AuthenticatedManifest) -> tuple[str, ...]:
    value = _require_authenticated_manifest(manifest)
    prefix = value.grant.entry_prefix.rstrip("/")
    prefix_path = _checked_directory(workspace_root, prefix)
    root = workspace_root.resolve(strict=True)
    discovered: list[str] = []
    pending = [prefix_path]
    while pending:
        directory = pending.pop()
        try:
            entries = sorted(os.scandir(directory), key=lambda item: item.name)
        except OSError as exc:
            raise UnsafePathError("manifest namespace could not be enumerated") from exc
        for entry in entries:
            path = Path(entry.path)
            try:
                info = os.lstat(path)
            except OSError as exc:
                raise UnsafePathError("manifest namespace entry could not be inspected") from exc
            if _is_reparse(info):
                raise UnsafePathError("manifest namespace contains a reparse-backed path")
            if stat.S_ISDIR(info.st_mode):
                pending.append(path)
            elif stat.S_ISREG(info.st_mode):
                relative = path.relative_to(root).as_posix()
                if relative != value.grant.manifest_path:
                    discovered.append(relative)
            else:
                raise UnsafePathError("manifest namespace contains a non-regular entry")
    return tuple(sorted(discovered))


def _revalidate_manifest_file(workspace_root: Path, manifest: AuthenticatedManifest) -> None:
    value = _require_authenticated_manifest(manifest)
    current = _read_once(workspace_root, value.grant.manifest_path)
    if current.sha256 != value.grant.manifest_sha256 or current.raw != value.manifest.raw:
        raise AuthenticationError("trusted manifest changed after authentication")


def load_authenticated_manifest(
    workspace_root: Path, grant: ManifestGrant
) -> AuthenticatedManifest:
    """Authenticate one manifest against an opaque external trust grant."""

    grant = require_manifest_grant(grant)
    read = _read_once(workspace_root, grant.manifest_path)
    if read.sha256 != grant.manifest_sha256:
        raise AuthenticationError("manifest external trust hash mismatch")
    manifest = _authenticated(read, grant=grant, authority_kind="manifest-anchor")
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
        if not relative.startswith(grant.entry_prefix):
            raise AuthenticationError("manifest entry escapes its frozen namespace")
        if relative == grant.manifest_path or relative in entries:
            raise AuthenticationError("manifest contains a self-entry or duplicate path")
        entries[relative] = digest
    if tuple(sorted(entries)) != grant.allowed_paths:
        raise AuthenticationError("manifest entries do not equal the externally granted file set")
    immutable_entries = MappingProxyType(dict(sorted(entries.items())))
    return AuthenticatedManifest(
        grant,
        manifest,
        immutable_entries,
        hashlib.sha256(_entries_binding(immutable_entries)).hexdigest(),
        _provenance=_MANIFEST_PROVENANCE,
    )


def authenticate_manifest_entry(
    workspace_root: Path,
    manifest: AuthenticatedManifest,
    value: str | Path,
    *,
    max_bytes: int | None = None,
) -> AuthenticatedBytes:
    """Read once and bind exact entry bytes to the manifest's external grant."""

    manifest = _require_authenticated_manifest(manifest)
    relative = _safe_relative(value)
    expected = manifest.entries.get(relative)
    if expected is None:
        raise AuthenticationError("path is not in the externally granted manifest file set")
    _revalidate_manifest_file(workspace_root, manifest)
    read = _read_once(workspace_root, relative, max_bytes=max_bytes)
    if read.sha256 != expected:
        raise AuthenticationError("authenticated public file hash mismatch")
    _revalidate_manifest_file(workspace_root, manifest)
    return _authenticated(read, grant=manifest.grant, authority_kind="manifest-entry")


def authenticate_manifest_file_set(
    workspace_root: Path, manifest: AuthenticatedManifest
) -> Mapping[str, AuthenticatedBytes]:
    """Return a stable observed snapshot of the complete granted namespace."""

    manifest = _require_authenticated_manifest(manifest)
    expected_paths = manifest.grant.allowed_paths
    _revalidate_manifest_file(workspace_root, manifest)
    if _enumerate_namespace(workspace_root, manifest) != expected_paths:
        raise AuthenticationError("manifest namespace initial file set mismatch")

    authenticated = {
        relative: authenticate_manifest_entry(workspace_root, manifest, relative)
        for relative in expected_paths
    }
    if _enumerate_namespace(workspace_root, manifest) != expected_paths:
        raise AuthenticationError("manifest namespace changed after authenticated reads")

    for relative in expected_paths:
        current = _read_once(workspace_root, relative)
        first = authenticated[relative]
        if current.sha256 != first.sha256 or current.raw != first.raw:
            raise AuthenticationError("manifest namespace content changed during stability recheck")

    _revalidate_manifest_file(workspace_root, manifest)
    if _enumerate_namespace(workspace_root, manifest) != expected_paths:
        raise AuthenticationError("manifest namespace changed during final stability recheck")
    return MappingProxyType(authenticated)

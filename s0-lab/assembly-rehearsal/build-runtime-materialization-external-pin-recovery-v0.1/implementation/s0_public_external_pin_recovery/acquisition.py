"""Exclusive, chunk-injected acquisition for externally pinned artifacts.

This module deliberately has no transport implementation.  A caller must
provide both the observed transport metadata and the received byte chunks.
"""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import os
from pathlib import Path
import stat
from typing import Iterable, Mapping

from .canonical import canonical_json_bytes, canonical_sha256
from .errors import AcquisitionError
from .pins import ArtifactPin


DEFAULT_MAX_CHUNK_SIZE = 1024 * 1024
DEFAULT_MAX_ARTIFACT_SIZE = 24 * 1024 * 1024 * 1024
_REPARSE_POINT = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)


@dataclass(frozen=True, slots=True)
class AcquisitionCheckpoint:
    """A stable identity/content observation made on the one open handle."""

    label: str
    st_dev: int
    st_ino: int
    size: int
    sha256: str

    def to_mapping(self) -> Mapping[str, object]:
        return {
            "label": self.label,
            "sha256": self.sha256,
            "size": self.size,
            "st_dev": self.st_dev,
            "st_ino": self.st_ino,
        }


@dataclass(frozen=True, slots=True)
class AcquisitionEvidence:
    """Immutable evidence for one non-reusable acquisition attempt."""

    artifact_name: str
    filename: str
    source_uri: str
    redirect_count: int
    destination: str
    expected_size: int | None
    expected_sha256: str | None
    observed_size: int
    observed_sha256: str
    authenticated: bool
    process_authority: bool
    reuse_authority: bool
    status: str
    checkpoints: tuple[AcquisitionCheckpoint, ...]

    def to_mapping(self) -> Mapping[str, object]:
        """Return the canonical, deterministic public evidence mapping."""

        return {
            "artifact_name": self.artifact_name,
            "authenticated": self.authenticated,
            "checkpoints": [item.to_mapping() for item in self.checkpoints],
            "destination": self.destination,
            "expected_sha256": self.expected_sha256,
            "expected_size": self.expected_size,
            "filename": self.filename,
            "observed_sha256": self.observed_sha256,
            "observed_size": self.observed_size,
            "process_authority": self.process_authority,
            "redirect_count": self.redirect_count,
            "reuse_authority": self.reuse_authority,
            "source_uri": self.source_uri,
            "status": self.status,
        }

    def canonical_bytes(self) -> bytes:
        return canonical_json_bytes(self.to_mapping())

    def evidence_sha256(self) -> str:
        return canonical_sha256(self.to_mapping())


def acquire_pinned_artifact(
    pin: ArtifactPin,
    *,
    chunks: Iterable[bytes],
    observed_uri: str,
    redirect_count: int,
    destination: str | os.PathLike[str],
    repository_root: str | os.PathLike[str],
    max_chunk_size: int = DEFAULT_MAX_CHUNK_SIZE,
) -> AcquisitionEvidence:
    """Materialize exactly one pin from caller-injected chunks.

    The destination is opened once with exclusive creation and is never
    removed or reused by this function, including after a failure.
    """

    _validate_transport(pin, observed_uri, redirect_count)
    expected_size, expected_sha256, total_limit = _validate_pin(pin)
    chunk_limit = _positive_int(max_chunk_size, "invalid_max_chunk_size")
    if chunk_limit > DEFAULT_MAX_CHUNK_SIZE:
        raise AcquisitionError("max_chunk_size_bound_exceeded")
    target, parent_before = _validate_destination(
        pin, destination, repository_root
    )

    flags = os.O_RDWR | os.O_CREAT | os.O_EXCL
    flags |= getattr(os, "O_BINARY", 0)
    flags |= getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)

    try:
        descriptor = os.open(target, flags, 0o600)
    except FileExistsError as exc:
        raise AcquisitionError("destination_not_fresh") from exc
    except OSError as exc:
        raise AcquisitionError("destination_open_failed") from exc

    try:
        created = _checked_fstat(descriptor, "created_file_invalid")
        if created.st_size != 0:
            raise AcquisitionError("created_file_not_empty")
        _verify_path_binding(target, created)

        digest = hashlib.sha256()
        observed_size = 0
        saw_chunk = False
        try:
            for chunk in chunks:
                data = _validated_chunk(chunk, chunk_limit)
                saw_chunk = True
                prospective_size = observed_size + len(data)
                if prospective_size > total_limit:
                    raise AcquisitionError("artifact_size_bound_exceeded")
                _write_all(descriptor, data)
                digest.update(data)
                observed_size = prospective_size
        except AcquisitionError:
            raise
        except Exception as exc:
            raise AcquisitionError("chunk_stream_failed") from exc

        if not saw_chunk and expected_size != 0:
            raise AcquisitionError("empty_chunk_stream")
        observed_sha256 = digest.hexdigest()
        post_write = _checked_fstat(descriptor, "post_write_file_invalid")
        _require_same_identity(created, post_write)
        if post_write.st_size != observed_size:
            raise AcquisitionError("post_write_size_mismatch")

        try:
            os.fsync(descriptor)
        except OSError as exc:
            raise AcquisitionError("destination_sync_failed") from exc
        post_sync = _checked_fstat(descriptor, "post_sync_file_invalid")
        _require_stable_checkpoint(post_write, post_sync, observed_size)
        persisted_sha256 = _hash_open_file(
            descriptor, observed_size, chunk_limit
        )
        if persisted_sha256 != observed_sha256:
            raise AcquisitionError("persisted_sha256_mismatch")
        post_hash = _checked_fstat(descriptor, "post_hash_file_invalid")
        _require_stable_checkpoint(post_sync, post_hash, observed_size)
        path_stat = _verify_path_binding(target, post_hash)

        parent_after = _safe_lstat(target.parent, "destination_parent_unavailable")
        _require_same_identity(parent_before, parent_after)
        if expected_size is not None and observed_size != expected_size:
            raise AcquisitionError("expected_size_mismatch")
        if expected_sha256 is not None and observed_sha256 != expected_sha256:
            raise AcquisitionError("expected_sha256_mismatch")

        authenticated = pin.authenticated
        checkpoints = (
            _checkpoint("post_write", post_write, observed_sha256),
            _checkpoint("post_sync", post_sync, persisted_sha256),
            _checkpoint("post_hash", post_hash, persisted_sha256),
            _checkpoint("path_binding", path_stat, persisted_sha256),
        )
        _require_evidence_stability(checkpoints)
        return AcquisitionEvidence(
            artifact_name=pin.filename,
            filename=pin.filename,
            source_uri=observed_uri,
            redirect_count=redirect_count,
            destination=str(target),
            expected_size=expected_size,
            expected_sha256=expected_sha256,
            observed_size=observed_size,
            observed_sha256=observed_sha256,
            authenticated=authenticated,
            process_authority=False,
            reuse_authority=False,
            status="authenticated" if authenticated else "unauthenticated",
            checkpoints=checkpoints,
        )
    finally:
        try:
            os.close(descriptor)
        except OSError as exc:
            raise AcquisitionError("destination_close_failed") from exc


def acquire_artifact(
    pin: ArtifactPin,
    *,
    chunks: Iterable[bytes],
    observed_uri: str,
    redirect_count: int,
    destination: str | os.PathLike[str],
    repository_root: str | os.PathLike[str],
    max_chunk_size: int = DEFAULT_MAX_CHUNK_SIZE,
) -> AcquisitionEvidence:
    """Compatibility spelling for :func:`acquire_pinned_artifact`."""

    return acquire_pinned_artifact(
        pin,
        chunks=chunks,
        observed_uri=observed_uri,
        redirect_count=redirect_count,
        destination=destination,
        repository_root=repository_root,
        max_chunk_size=max_chunk_size,
    )


def _validate_transport(
    pin: ArtifactPin, observed_uri: str, redirect_count: int
) -> None:
    if not isinstance(pin.url, str) or not pin.url:
        raise AcquisitionError("invalid_pin_uri")
    if not isinstance(observed_uri, str) or observed_uri != pin.url:
        raise AcquisitionError("source_uri_mismatch")
    if (
        isinstance(redirect_count, bool)
        or not isinstance(redirect_count, int)
        or redirect_count != 0
    ):
        raise AcquisitionError("redirect_not_permitted")


def _validate_pin(pin: ArtifactPin) -> tuple[int | None, str | None, int]:
    if (
        not isinstance(pin.filename, str)
        or not pin.filename
        or Path(pin.filename).name != pin.filename
    ):
        raise AcquisitionError("invalid_pin_filename")

    expected_size = pin.size
    if expected_size is not None:
        expected_size = _nonnegative_int(expected_size, "invalid_expected_size")
    total_limit = (
        expected_size
        if expected_size is not None
        else DEFAULT_MAX_ARTIFACT_SIZE
    )

    expected_sha256 = pin.sha256
    if expected_sha256 is not None:
        if (
            not isinstance(expected_sha256, str)
            or len(expected_sha256) != 64
            or expected_sha256 != expected_sha256.lower()
            or any(character not in "0123456789abcdef" for character in expected_sha256)
        ):
            raise AcquisitionError("invalid_expected_sha256")
    if type(pin.authenticated) is not bool:
        raise AcquisitionError("invalid_authenticated_state")
    if pin.authenticated and expected_sha256 is None:
        raise AcquisitionError("authenticated_pin_missing_sha256")
    return expected_size, expected_sha256, total_limit


def _validate_destination(
    pin: ArtifactPin,
    destination: str | os.PathLike[str],
    repository_root: str | os.PathLike[str],
) -> tuple[Path, os.stat_result]:
    root = Path(repository_root)
    requested = Path(destination)
    if not root.is_absolute() or not requested.is_absolute():
        raise AcquisitionError("paths_must_be_absolute")
    try:
        resolved_root = root.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise AcquisitionError("repository_root_unavailable") from exc
    if not resolved_root.is_dir():
        raise AcquisitionError("repository_root_not_directory")
    if requested.name != pin.filename:
        raise AcquisitionError("destination_filename_mismatch")

    try:
        os.lstat(requested)
    except FileNotFoundError:
        pass
    except OSError as exc:
        raise AcquisitionError("destination_probe_failed") from exc
    else:
        raise AcquisitionError("destination_not_fresh")

    _reject_linked_ancestors(requested.parent)
    try:
        resolved_parent = requested.parent.resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise AcquisitionError("destination_parent_unavailable") from exc
    target = resolved_parent / requested.name
    if _is_within(target, resolved_root):
        raise AcquisitionError("destination_inside_repository")
    parent_stat = _safe_lstat(resolved_parent, "destination_parent_unavailable")
    if not stat.S_ISDIR(parent_stat.st_mode) or _is_reparse(parent_stat):
        raise AcquisitionError("destination_parent_unsafe")
    return target, parent_stat


def _reject_linked_ancestors(parent: Path) -> None:
    current = parent
    while True:
        item = _safe_lstat(current, "destination_parent_unavailable")
        if stat.S_ISLNK(item.st_mode) or _is_reparse(item):
            raise AcquisitionError("destination_parent_unsafe")
        if not stat.S_ISDIR(item.st_mode):
            raise AcquisitionError("destination_parent_not_directory")
        if current.parent == current:
            return
        current = current.parent


def _is_within(candidate: Path, root: Path) -> bool:
    try:
        os.path.commonpath((str(candidate), str(root)))
    except ValueError:
        return False
    return os.path.commonpath((str(candidate), str(root))) == str(root)


def _safe_lstat(path: Path, error_code: str) -> os.stat_result:
    try:
        return os.lstat(path)
    except OSError as exc:
        raise AcquisitionError(error_code) from exc


def _is_reparse(item: os.stat_result) -> bool:
    attributes = getattr(item, "st_file_attributes", None)
    if attributes is None:
        return False
    if type(attributes) is not int:
        return True
    return bool(attributes & _REPARSE_POINT)


def _checked_fstat(descriptor: int, error_code: str) -> os.stat_result:
    try:
        item = os.fstat(descriptor)
    except OSError as exc:
        raise AcquisitionError(error_code) from exc
    if not stat.S_ISREG(item.st_mode) or _is_reparse(item):
        raise AcquisitionError(error_code)
    return item


def _verify_path_binding(target: Path, handle_stat: os.stat_result) -> os.stat_result:
    path_stat = _safe_lstat(target, "destination_binding_unavailable")
    if stat.S_ISLNK(path_stat.st_mode) or _is_reparse(path_stat):
        raise AcquisitionError("destination_binding_unsafe")
    _require_same_identity(handle_stat, path_stat)
    return path_stat


def _require_same_identity(first: os.stat_result, second: os.stat_result) -> None:
    if (first.st_dev, first.st_ino) != (second.st_dev, second.st_ino):
        raise AcquisitionError("destination_identity_changed")


def _require_stable_checkpoint(
    first: os.stat_result, second: os.stat_result, expected_size: int
) -> None:
    _require_same_identity(first, second)
    if first.st_size != expected_size or second.st_size != expected_size:
        raise AcquisitionError("destination_size_changed")


def _checkpoint(
    label: str, item: os.stat_result, sha256: str
) -> AcquisitionCheckpoint:
    return AcquisitionCheckpoint(
        label=label,
        st_dev=item.st_dev,
        st_ino=item.st_ino,
        size=item.st_size,
        sha256=sha256,
    )


def _require_evidence_stability(
    checkpoints: tuple[AcquisitionCheckpoint, ...],
) -> None:
    reference = checkpoints[0]
    for item in checkpoints[1:]:
        if (
            item.st_dev,
            item.st_ino,
            item.size,
            item.sha256,
        ) != (
            reference.st_dev,
            reference.st_ino,
            reference.size,
            reference.sha256,
        ):
            raise AcquisitionError("evidence_checkpoint_changed")


def _validated_chunk(chunk: object, max_size: int) -> bytes:
    if not isinstance(chunk, (bytes, bytearray, memoryview)):
        raise AcquisitionError("chunk_not_bytes")
    data = bytes(chunk)
    if not data:
        raise AcquisitionError("chunk_not_positive")
    if len(data) > max_size:
        raise AcquisitionError("chunk_size_bound_exceeded")
    return data


def _write_all(descriptor: int, data: bytes) -> None:
    view = memoryview(data)
    offset = 0
    while offset < len(view):
        try:
            written = os.write(descriptor, view[offset:])
        except OSError as exc:
            raise AcquisitionError("destination_write_failed") from exc
        if written <= 0:
            raise AcquisitionError("destination_write_incomplete")
        offset += written


def _hash_open_file(descriptor: int, expected_size: int, block_size: int) -> str:
    try:
        os.lseek(descriptor, 0, os.SEEK_SET)
    except OSError as exc:
        raise AcquisitionError("destination_seek_failed") from exc
    digest = hashlib.sha256()
    observed_size = 0
    while observed_size < expected_size:
        request_size = min(block_size, expected_size - observed_size)
        try:
            data = os.read(descriptor, request_size)
        except OSError as exc:
            raise AcquisitionError("destination_readback_failed") from exc
        if not data:
            raise AcquisitionError("destination_readback_incomplete")
        digest.update(data)
        observed_size += len(data)
    try:
        trailing = os.read(descriptor, 1)
    except OSError as exc:
        raise AcquisitionError("destination_readback_failed") from exc
    if trailing:
        raise AcquisitionError("destination_readback_size_mismatch")
    return digest.hexdigest()


def _positive_int(value: object, error_code: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        raise AcquisitionError(error_code)
    return value


def _nonnegative_int(value: object, error_code: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise AcquisitionError(error_code)
    return value


__all__ = [
    "AcquisitionCheckpoint",
    "AcquisitionEvidence",
    "DEFAULT_MAX_ARTIFACT_SIZE",
    "DEFAULT_MAX_CHUNK_SIZE",
    "acquire_artifact",
    "acquire_pinned_artifact",
]

"""Closed-pin, injected-byte acquisition using retained Windows handles."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import os
from typing import Callable, Iterable, Mapping, NamedTuple

from .canonical import canonical_json_bytes, canonical_sha256
from .errors import AcquisitionError
from .pins import ArtifactPin, PinSnapshot, _resolve_approved_pin_snapshot
from .win32_secure import SecureCreatedFile, WindowsFileSnapshot, secure_create_file


DEFAULT_MAX_CHUNK_SIZE = 1024 * 1024
DEFAULT_MAX_ARTIFACT_SIZE = 24 * 1024 * 1024 * 1024


class _PinSnapshot(NamedTuple):
    """One immutable trusted pin value copied from frozen primitive authority."""

    pin_id: str
    filename: str
    url: str
    expected_sha256: str | None
    expected_size: int | None
    max_size: int


@dataclass(frozen=True, slots=True)
class AcquisitionCheckpoint:
    """One identity, length, and digest observation on the retained file."""

    label: str
    volume_serial: int
    file_id: str
    size: int
    sha256: str

    def to_mapping(self) -> Mapping[str, object]:
        return {
            "file_id": self.file_id,
            "label": self.label,
            "sha256": self.sha256,
            "size": self.size,
            "volume_serial": self.volume_serial,
        }


@dataclass(frozen=True, slots=True)
class AcquisitionEvidence:
    """Deterministic evidence; it never grants process or reuse authority."""

    pin_id: str
    artifact_name: str
    filename: str
    source_uri: str
    redirect_count: int
    destination: str
    expected_size: int | None
    expected_sha256: str | None
    max_size: int
    observed_size: int
    observed_sha256: str
    authenticated: bool
    process_authority: bool
    reuse_authority: bool
    status: str
    checkpoints: tuple[AcquisitionCheckpoint, ...]

    def to_mapping(self) -> Mapping[str, object]:
        return {
            "artifact_name": self.artifact_name,
            "authenticated": self.authenticated,
            "checkpoints": [item.to_mapping() for item in self.checkpoints],
            "destination": self.destination,
            "expected_sha256": self.expected_sha256,
            "expected_size": self.expected_size,
            "filename": self.filename,
            "max_size": self.max_size,
            "observed_sha256": self.observed_sha256,
            "observed_size": self.observed_size,
            "pin_id": self.pin_id,
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


def _acquire_pinned_artifact_impl(
    pin_or_id: ArtifactPin | str,
    *,
    resolve_pin: Callable[[ArtifactPin | str], _PinSnapshot],
    chunks: Iterable[bytes],
    observed_uri: str,
    redirect_count: int,
    destination: str | os.PathLike[str],
    repository_root: str | os.PathLike[str],
    max_chunk_size: int = DEFAULT_MAX_CHUNK_SIZE,
) -> AcquisitionEvidence:
    """Acquire one allowlisted pin without transport or caller-minted authority."""

    pin = resolve_pin(pin_or_id)
    _validate_transport(pin, observed_uri, redirect_count)
    chunk_limit = _positive_int(max_chunk_size, "invalid_max_chunk_size")
    if chunk_limit > DEFAULT_MAX_CHUNK_SIZE:
        raise AcquisitionError("max_chunk_size_bound_exceeded")

    secure_file = secure_create_file(
        repository_root=repository_root,
        destination=destination,
        expected_filename=pin.filename,
    )
    evidence: AcquisitionEvidence | None = None
    primary_error: BaseException | None = None
    try:
        evidence = _acquire_to_retained_file(
            pin,
            secure_file,
            chunks,
            observed_uri,
            redirect_count,
            chunk_limit,
        )
    except BaseException as exc:
        primary_error = exc
        raise
    finally:
        try:
            secure_file.close()
        except AcquisitionError:
            if primary_error is None:
                raise
    if evidence is None:
        raise AcquisitionError("acquisition_evidence_unavailable")
    return evidence


def _freeze_pin_resolver(
    snapshot_resolver: Callable[[ArtifactPin | str], PinSnapshot],
) -> Callable[[ArtifactPin | str], _PinSnapshot]:
    resolver = snapshot_resolver
    trusted_type = _PinSnapshot
    error_type = AcquisitionError
    maximum_size = DEFAULT_MAX_ARTIFACT_SIZE

    def resolve_pin_once(pin_or_id: ArtifactPin | str) -> _PinSnapshot:
        try:
            snapshot = resolver(pin_or_id)
        except Exception as exc:
            raise error_type("pin_not_approved") from exc
        if type(snapshot) is not tuple or len(snapshot) != 6:
            raise error_type("pin_not_canonical")
        pin_id, filename, url, expected_sha256, expected_size, max_size = snapshot
        if type(pin_id) is not str or not pin_id:
            raise error_type("invalid_pin_id")
        if type(filename) is not str or not filename:
            raise error_type("invalid_pin_filename")
        if type(url) is not str or not url:
            raise error_type("invalid_pin_uri")
        if expected_sha256 is not None and (
            type(expected_sha256) is not str
            or len(expected_sha256) != 64
            or any(character not in "0123456789abcdef" for character in expected_sha256)
        ):
            raise error_type("invalid_expected_sha256")
        if expected_size is not None and (
            type(expected_size) is not int or expected_size < 0
        ):
            raise error_type("invalid_expected_size")
        if type(max_size) is not int or max_size <= 0:
            raise error_type("invalid_max_artifact_size")
        if max_size > maximum_size:
            raise error_type("max_artifact_size_bound_exceeded")
        if expected_size is not None and expected_size > max_size:
            raise error_type("expected_size_bound_exceeded")
        return trusted_type(*snapshot)

    return resolve_pin_once


def _freeze_acquirer(
    resolve_pin: Callable[[ArtifactPin | str], _PinSnapshot],
):
    implementation = _acquire_pinned_artifact_impl

    def acquire_pinned_artifact(
        pin_or_id: ArtifactPin | str,
        *,
        chunks: Iterable[bytes],
        observed_uri: str,
        redirect_count: int,
        destination: str | os.PathLike[str],
        repository_root: str | os.PathLike[str],
        max_chunk_size: int = DEFAULT_MAX_CHUNK_SIZE,
    ) -> AcquisitionEvidence:
        return implementation(
            pin_or_id,
            resolve_pin=resolve_pin,
            chunks=chunks,
            observed_uri=observed_uri,
            redirect_count=redirect_count,
            destination=destination,
            repository_root=repository_root,
            max_chunk_size=max_chunk_size,
        )

    return acquire_pinned_artifact


def _freeze_acquire_alias(acquirer):
    trusted_acquirer = acquirer

    def acquire_artifact(
        pin_or_id: ArtifactPin | str,
        *,
        chunks: Iterable[bytes],
        observed_uri: str,
        redirect_count: int,
        destination: str | os.PathLike[str],
        repository_root: str | os.PathLike[str],
        max_chunk_size: int = DEFAULT_MAX_CHUNK_SIZE,
    ) -> AcquisitionEvidence:
        """Compatibility spelling for :func:`acquire_pinned_artifact`."""

        return trusted_acquirer(
            pin_or_id,
            chunks=chunks,
            observed_uri=observed_uri,
            redirect_count=redirect_count,
            destination=destination,
            repository_root=repository_root,
            max_chunk_size=max_chunk_size,
        )

    return acquire_artifact


_trusted_pin_resolver = _freeze_pin_resolver(_resolve_approved_pin_snapshot)
acquire_pinned_artifact = _freeze_acquirer(_trusted_pin_resolver)
acquire_artifact = _freeze_acquire_alias(acquire_pinned_artifact)
del _acquire_pinned_artifact_impl
del _freeze_acquire_alias
del _freeze_acquirer
del _freeze_pin_resolver
del _resolve_approved_pin_snapshot
del _trusted_pin_resolver


def _validate_transport(
    pin: _PinSnapshot, observed_uri: str, redirect_count: int
) -> None:
    if type(observed_uri) is not str or observed_uri != pin.url:
        raise AcquisitionError("source_uri_mismatch")
    if type(redirect_count) is not int or redirect_count != 0:
        raise AcquisitionError("redirect_not_permitted")


def _acquire_to_retained_file(
    pin: _PinSnapshot,
    secure_file: SecureCreatedFile,
    chunks: Iterable[bytes],
    observed_uri: str,
    redirect_count: int,
    chunk_limit: int,
) -> AcquisitionEvidence:
    streaming_digest = hashlib.sha256()
    observed_size = 0
    saw_chunk = False
    try:
        iterator = iter(chunks)
        for chunk in iterator:
            data = _validated_chunk(chunk, chunk_limit)
            saw_chunk = True
            prospective_size = observed_size + len(data)
            if prospective_size > pin.max_size:
                raise AcquisitionError("artifact_size_bound_exceeded")
            if pin.expected_size is not None and prospective_size > pin.expected_size:
                raise AcquisitionError("expected_size_exceeded")
            secure_file.write_all(data)
            streaming_digest.update(data)
            observed_size = prospective_size
    except AcquisitionError:
        raise
    except Exception as exc:
        raise AcquisitionError("chunk_stream_failed") from exc

    if not saw_chunk and pin.expected_size != 0:
        raise AcquisitionError("empty_chunk_stream")
    streamed_sha256 = streaming_digest.hexdigest()
    post_write = secure_file.snapshot("post_write_file_invalid")
    if post_write.length != observed_size:
        raise AcquisitionError("post_write_size_mismatch")

    secure_file.flush()
    post_flush = secure_file.snapshot("post_flush_file_invalid")
    _require_same_snapshot(post_write, post_flush, observed_size)
    persisted_sha256 = secure_file.readback_sha256(observed_size, chunk_limit)
    if persisted_sha256 != streamed_sha256:
        raise AcquisitionError("persisted_sha256_mismatch")
    post_readback = secure_file.snapshot("post_readback_file_invalid")
    _require_same_snapshot(post_flush, post_readback, observed_size)

    if pin.expected_size is not None and observed_size != pin.expected_size:
        raise AcquisitionError("expected_size_mismatch")
    if pin.expected_sha256 is not None and persisted_sha256 != pin.expected_sha256:
        raise AcquisitionError("expected_sha256_mismatch")

    final_binding = secure_file.final_reauthenticate(observed_size)
    _require_same_snapshot(post_readback, final_binding, observed_size)
    checkpoints = (
        _checkpoint("post_write", post_write, streamed_sha256),
        _checkpoint("post_flush", post_flush, streamed_sha256),
        _checkpoint("post_readback", post_readback, persisted_sha256),
        _checkpoint("final_binding", final_binding, persisted_sha256),
    )
    _require_evidence_stability(checkpoints)

    authenticated = pin.expected_sha256 is not None
    return AcquisitionEvidence(
        pin_id=pin.pin_id,
        artifact_name=pin.filename,
        filename=pin.filename,
        source_uri=observed_uri,
        redirect_count=redirect_count,
        destination=secure_file.destination,
        expected_size=pin.expected_size,
        expected_sha256=pin.expected_sha256,
        max_size=pin.max_size,
        observed_size=observed_size,
        observed_sha256=persisted_sha256,
        authenticated=authenticated,
        process_authority=False,
        reuse_authority=False,
        status="acquired-authenticated" if authenticated else "acquired-unauthenticated",
        checkpoints=checkpoints,
    )


def _checkpoint(
    label: str, snapshot: WindowsFileSnapshot, sha256: str
) -> AcquisitionCheckpoint:
    return AcquisitionCheckpoint(
        label=label,
        volume_serial=snapshot.identity.volume_serial,
        file_id=snapshot.identity.file_id,
        size=snapshot.length,
        sha256=sha256,
    )


def _require_same_snapshot(
    first: WindowsFileSnapshot, second: WindowsFileSnapshot, expected_size: int
) -> None:
    if first.identity != second.identity:
        raise AcquisitionError("destination_identity_changed")
    if first.length != expected_size or second.length != expected_size:
        raise AcquisitionError("destination_size_changed")


def _require_evidence_stability(
    checkpoints: tuple[AcquisitionCheckpoint, ...],
) -> None:
    reference = checkpoints[0]
    for item in checkpoints[1:]:
        if (
            item.volume_serial,
            item.file_id,
            item.size,
            item.sha256,
        ) != (
            reference.volume_serial,
            reference.file_id,
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


def _positive_int(value: object, error_code: str) -> int:
    if type(value) is not int or value <= 0:
        raise AcquisitionError(error_code)
    return value


def _nonnegative_int(value: object, error_code: str) -> int:
    if type(value) is not int or value < 0:
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

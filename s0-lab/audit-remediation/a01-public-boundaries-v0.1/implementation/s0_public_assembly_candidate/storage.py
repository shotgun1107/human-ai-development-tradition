"""Exact bounded reads and controller-owned output-file handling."""

from __future__ import annotations

import hashlib
import os
import stat
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

from .constants import (
    OUTPUT_NAMES,
    RECEIPT_FINAL_NAME,
    RECEIPT_PENDING_NAME,
    RUN_RECORD_FINAL_NAME,
    RUN_RECORD_PENDING_NAME,
)


class StorageError(RuntimeError):
    """A fixed input or candidate-owned output operation failed."""


class ReservationError(StorageError):
    """The newly supplied output root could not be reserved."""


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _is_reparse(info: os.stat_result) -> bool:
    attributes = getattr(info, "st_file_attributes", 0)
    marker = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return bool(attributes & marker)


def _safe_relative(value: str) -> PurePosixPath:
    if type(value) is not str or not value or "\\" in value or ":" in value:
        raise StorageError("workspace path is not an exact safe relative path")
    relative = PurePosixPath(value)
    if relative.is_absolute() or ".." in relative.parts or "." in relative.parts:
        raise StorageError("workspace path escapes its fixed namespace")
    return relative


def checked_workspace_root(workspace_root: Path) -> Path:
    if not isinstance(workspace_root, Path):
        raise StorageError("workspace root must be pathlib.Path")
    try:
        lexical_info = os.lstat(workspace_root)
        if stat.S_ISLNK(lexical_info.st_mode) or _is_reparse(lexical_info):
            raise StorageError("workspace root must not be link or reparse-backed")
        root = workspace_root.resolve(strict=True)
        info = os.lstat(root)
    except StorageError:
        raise
    except OSError as exc:
        raise StorageError("workspace root is unavailable") from exc
    if not stat.S_ISDIR(info.st_mode) or _is_reparse(info):
        raise StorageError("workspace root is not a regular directory root")
    return root


def workspace_path(workspace_root: Path, relative: str) -> Path:
    root = checked_workspace_root(workspace_root)
    pure = _safe_relative(relative)
    current = root
    for part in pure.parts:
        current = current / part
        try:
            info = os.lstat(current)
        except OSError as exc:
            raise StorageError("fixed workspace path is unavailable") from exc
        if stat.S_ISLNK(info.st_mode) or _is_reparse(info):
            raise StorageError("fixed workspace path traverses a link or reparse point")
    return current


def read_workspace_file(
    workspace_root: Path,
    relative: str,
    *,
    expected_sha256: str,
    expected_bytes: int | None = None,
) -> bytes:
    path = workspace_path(workspace_root, relative)
    try:
        info = os.lstat(path)
    except OSError as exc:
        raise StorageError("fixed workspace file is unavailable") from exc
    if not stat.S_ISREG(info.st_mode):
        raise StorageError("fixed workspace input is not a regular file")
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_CLOEXEC", 0)
    flags |= getattr(os, "O_NOFOLLOW", 0)
    try:
        descriptor = os.open(path, flags)
    except OSError as exc:
        raise StorageError("fixed workspace input could not be opened") from exc
    try:
        before = os.fstat(descriptor)
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 65536)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(descriptor)
    except OSError as exc:
        raise StorageError("fixed workspace input could not be read stably") from exc
    finally:
        os.close(descriptor)
    if (
        before.st_dev != after.st_dev
        or before.st_ino != after.st_ino
        or before.st_size != after.st_size
    ):
        raise StorageError("fixed workspace input identity changed during read")
    raw = b"".join(chunks)
    if len(raw) != before.st_size:
        raise StorageError("fixed workspace input length changed during read")
    if expected_bytes is not None and len(raw) != expected_bytes:
        raise StorageError("fixed workspace input has the wrong byte length")
    if sha256_bytes(raw) != expected_sha256:
        raise StorageError("fixed workspace input hash mismatch")
    return raw


def _write_all(descriptor: int, raw: bytes) -> None:
    offset = 0
    while offset < len(raw):
        written = os.write(descriptor, raw[offset:])
        if type(written) is not int or written <= 0:
            raise StorageError("candidate output write made no progress")
        offset += written


@dataclass
class OutputReservation:
    root: Path
    record_descriptor: int | None
    pending_owned: set[str] = field(default_factory=lambda: {RUN_RECORD_PENDING_NAME})
    final_owned: set[str] = field(default_factory=set)
    uncertain_publications: set[str] = field(default_factory=set)

    @classmethod
    def reserve(cls, output_root: Path) -> "OutputReservation":
        if not isinstance(output_root, Path):
            raise ReservationError("output root must be pathlib.Path")
        try:
            lexical_info = os.lstat(output_root)
            if stat.S_ISLNK(lexical_info.st_mode) or _is_reparse(lexical_info):
                raise ReservationError("output root must not be link or reparse-backed")
            root = output_root.resolve(strict=True)
            info = os.lstat(root)
        except ReservationError:
            raise
        except OSError as exc:
            raise ReservationError("output root is unavailable") from exc
        if not stat.S_ISDIR(info.st_mode) or _is_reparse(info):
            raise ReservationError("output root is not a regular directory")
        try:
            with os.scandir(root) as entries:
                if next(entries, None) is not None:
                    raise ReservationError("output root is not empty")
        except ReservationError:
            raise
        except OSError as exc:
            raise ReservationError("output root could not be enumerated") from exc
        if any((root / name).exists() or (root / name).is_symlink() for name in OUTPUT_NAMES):
            raise ReservationError("one of the four output names already exists")
        flags = (
            os.O_WRONLY
            | os.O_CREAT
            | os.O_EXCL
            | getattr(os, "O_BINARY", 0)
            | getattr(os, "O_CLOEXEC", 0)
        )
        try:
            descriptor = os.open(root / RUN_RECORD_PENDING_NAME, flags, 0o600)
        except OSError as exc:
            raise ReservationError("record pending reservation failed") from exc
        return cls(root=root, record_descriptor=descriptor)

    def _write_close_verify(
        self,
        *,
        descriptor: int,
        path: Path,
        raw: bytes,
        expected_sha256: str,
    ) -> None:
        try:
            _write_all(descriptor, raw)
            os.fsync(descriptor)
            written_info = os.fstat(descriptor)
        finally:
            os.close(descriptor)
        flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_CLOEXEC", 0)
        flags |= getattr(os, "O_NOFOLLOW", 0)
        try:
            read_descriptor = os.open(path, flags)
            try:
                reopened_info = os.fstat(read_descriptor)
                chunks: list[bytes] = []
                while True:
                    chunk = os.read(read_descriptor, 65536)
                    if not chunk:
                        break
                    chunks.append(chunk)
            finally:
                os.close(read_descriptor)
        except OSError as exc:
            raise StorageError("candidate pending output could not be reopened") from exc
        if (
            written_info.st_dev != reopened_info.st_dev
            or written_info.st_ino != reopened_info.st_ino
            or written_info.st_size != reopened_info.st_size
        ):
            raise StorageError("candidate pending output identity changed before read-back")
        persisted = b"".join(chunks)
        if persisted != raw or sha256_bytes(persisted) != expected_sha256:
            raise StorageError("candidate pending output read-back mismatch")

    def write_reserved_record(self, raw: bytes, expected_sha256: str) -> None:
        descriptor = self.record_descriptor
        if descriptor is None:
            raise StorageError("record pending descriptor is unavailable")
        self.record_descriptor = None
        self._write_close_verify(
            descriptor=descriptor,
            path=self.root / RUN_RECORD_PENDING_NAME,
            raw=raw,
            expected_sha256=expected_sha256,
        )

    def write_receipt(self, raw: bytes, expected_sha256: str) -> None:
        path = self.root / RECEIPT_PENDING_NAME
        flags = (
            os.O_WRONLY
            | os.O_CREAT
            | os.O_EXCL
            | getattr(os, "O_BINARY", 0)
            | getattr(os, "O_CLOEXEC", 0)
        )
        try:
            descriptor = os.open(path, flags, 0o600)
        except OSError as exc:
            raise StorageError("receipt pending reservation failed") from exc
        self.pending_owned.add(RECEIPT_PENDING_NAME)
        self._write_close_verify(
            descriptor=descriptor,
            path=path,
            raw=raw,
            expected_sha256=expected_sha256,
        )

    def begin_publication(self, kind: str) -> None:
        if kind not in {"record", "receipt"}:
            raise StorageError("unknown publication kind")
        self.uncertain_publications.add(kind)

    def confirm_publication(self, kind: str) -> None:
        if kind == "record":
            pending, final = RUN_RECORD_PENDING_NAME, RUN_RECORD_FINAL_NAME
        elif kind == "receipt":
            pending, final = RECEIPT_PENDING_NAME, RECEIPT_FINAL_NAME
        else:
            raise StorageError("unknown publication kind")
        self.uncertain_publications.discard(kind)
        self.pending_owned.discard(pending)
        self.final_owned.add(final)

    def cleanup(self) -> tuple[str, str]:
        failed = False
        if self.record_descriptor is not None:
            try:
                os.close(self.record_descriptor)
            except OSError:
                failed = True
            self.record_descriptor = None

        uncertain_names = {
            RUN_RECORD_PENDING_NAME if kind == "record" else RECEIPT_PENDING_NAME
            for kind in self.uncertain_publications
        }
        for name in tuple(sorted(self.pending_owned - uncertain_names)):
            path = self.root / name
            try:
                if path.exists() or path.is_symlink():
                    path.unlink()
            except OSError:
                failed = True

        for name in tuple(sorted(self.final_owned)):
            path = self.root / name
            try:
                if path.exists() or path.is_symlink():
                    path.unlink()
            except OSError:
                failed = True

        for kind in tuple(sorted(self.uncertain_publications)):
            if kind == "record":
                pending, final = RUN_RECORD_PENDING_NAME, RUN_RECORD_FINAL_NAME
            else:
                pending, final = RECEIPT_PENDING_NAME, RECEIPT_FINAL_NAME
            pending_path = self.root / pending
            final_path = self.root / final
            try:
                pending_present = pending_path.exists() or pending_path.is_symlink()
                final_present = final_path.exists() or final_path.is_symlink()
                if pending_present and not final_present:
                    pending_path.unlink()
                    self.pending_owned.discard(pending)
                elif final_present:
                    failed = True
                else:
                    # No acknowledgement and no remaining source cannot prove ownership.
                    failed = True
            except OSError:
                failed = True

        try:
            with os.scandir(self.root) as entries:
                if next(entries, None) is not None:
                    failed = True
        except OSError:
            failed = True

        if failed:
            return "failed", "QUARANTINED-FAILED"
        return "complete", "CLEANED-FAILED"

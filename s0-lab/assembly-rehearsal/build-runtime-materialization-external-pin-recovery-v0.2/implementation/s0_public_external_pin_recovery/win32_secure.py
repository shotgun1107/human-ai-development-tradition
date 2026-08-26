"""Retained-handle Windows file creation with no reparse traversal.

Only Windows is supported.  Destination components are opened one at a time,
relative to the preceding retained directory handle, by ``NtCreateFile``.
The read-only repository exclusion root is retained as one absolute directory
binding.  Every retained handle denies delete sharing while an operation runs.
"""

from __future__ import annotations

import ctypes
from ctypes import wintypes
from dataclasses import dataclass
import hashlib
import ntpath
import os
import re
from typing import Final

from .errors import AcquisitionError


_FILE_READ_DATA: Final = 0x0001
_FILE_LIST_DIRECTORY: Final = 0x0001
_FILE_WRITE_DATA: Final = 0x0002
_FILE_TRAVERSE: Final = 0x0020
_FILE_READ_ATTRIBUTES: Final = 0x0080
_SYNCHRONIZE: Final = 0x00100000
_FILE_SHARE_READ: Final = 0x00000001
_FILE_SHARE_WRITE: Final = 0x00000002
_FILE_ATTRIBUTE_NORMAL: Final = 0x00000080
_FILE_ATTRIBUTE_REPARSE_POINT: Final = 0x00000400
_FILE_OPEN: Final = 0x00000001
_FILE_CREATE: Final = 0x00000002
_FILE_DIRECTORY_FILE: Final = 0x00000001
_FILE_SYNCHRONOUS_IO_NONALERT: Final = 0x00000020
_FILE_NON_DIRECTORY_FILE: Final = 0x00000040
_FILE_OPEN_FOR_BACKUP_INTENT: Final = 0x00004000
_FILE_OPEN_REPARSE_POINT: Final = 0x00200000
_OBJ_CASE_INSENSITIVE: Final = 0x00000040
_OBJ_DONT_REPARSE: Final = 0x00001000
_OPEN_EXISTING: Final = 3
_FILE_FLAG_BACKUP_SEMANTICS: Final = 0x02000000
_FILE_FLAG_OPEN_REPARSE_POINT: Final = 0x00200000
_FILE_BEGIN: Final = 0
_FILE_CURRENT: Final = 1
_FILE_END: Final = 2
_VOLUME_NAME_GUID: Final = 0x00000001
_FILE_STANDARD_INFO_CLASS: Final = 1
_FILE_ATTRIBUTE_TAG_INFO_CLASS: Final = 9
_FILE_ID_INFO_CLASS: Final = 18
_STATUS_OBJECT_NAME_COLLISION: Final = 0xC0000035
_INVALID_HANDLE_VALUE: Final = ctypes.c_void_p(-1).value
_MAX_DWORD: Final = 0xFFFFFFFF
DEFAULT_NATIVE_READ_BLOCK_SIZE: Final = 1024 * 1024


class _UNICODE_STRING(ctypes.Structure):
    _fields_ = (
        ("Length", wintypes.USHORT),
        ("MaximumLength", wintypes.USHORT),
        ("Buffer", wintypes.LPWSTR),
    )


class _OBJECT_ATTRIBUTES(ctypes.Structure):
    _fields_ = (
        ("Length", wintypes.ULONG),
        ("RootDirectory", wintypes.HANDLE),
        ("ObjectName", ctypes.POINTER(_UNICODE_STRING)),
        ("Attributes", wintypes.ULONG),
        ("SecurityDescriptor", wintypes.LPVOID),
        ("SecurityQualityOfService", wintypes.LPVOID),
    )


class _IO_STATUS_VALUE(ctypes.Union):
    _fields_ = (("Status", wintypes.LONG), ("Pointer", wintypes.LPVOID))


class _IO_STATUS_BLOCK(ctypes.Structure):
    _anonymous_ = ("Value",)
    _fields_ = (("Value", _IO_STATUS_VALUE), ("Information", ctypes.c_size_t))


class _FILE_ID_128(ctypes.Structure):
    _fields_ = (("Identifier", ctypes.c_ubyte * 16),)


class _FILE_ID_INFO(ctypes.Structure):
    _fields_ = (
        ("VolumeSerialNumber", ctypes.c_ulonglong),
        ("FileId", _FILE_ID_128),
    )


class _FILE_STANDARD_INFO(ctypes.Structure):
    _fields_ = (
        ("AllocationSize", ctypes.c_longlong),
        ("EndOfFile", ctypes.c_longlong),
        ("NumberOfLinks", wintypes.DWORD),
        ("DeletePending", wintypes.BYTE),
        ("Directory", wintypes.BYTE),
    )


class _FILE_ATTRIBUTE_TAG_INFO(ctypes.Structure):
    _fields_ = (("FileAttributes", wintypes.DWORD), ("ReparseTag", wintypes.DWORD))


if os.name == "nt":
    _kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    _ntdll = ctypes.WinDLL("ntdll")

    _CreateFileW = _kernel32.CreateFileW
    _CreateFileW.argtypes = (
        wintypes.LPCWSTR,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.LPVOID,
        wintypes.DWORD,
        wintypes.DWORD,
        wintypes.HANDLE,
    )
    _CreateFileW.restype = wintypes.HANDLE

    _CloseHandle = _kernel32.CloseHandle
    _CloseHandle.argtypes = (wintypes.HANDLE,)
    _CloseHandle.restype = wintypes.BOOL

    _GetFileInformationByHandleEx = _kernel32.GetFileInformationByHandleEx
    _GetFileInformationByHandleEx.argtypes = (
        wintypes.HANDLE,
        ctypes.c_int,
        wintypes.LPVOID,
        wintypes.DWORD,
    )
    _GetFileInformationByHandleEx.restype = wintypes.BOOL

    _WriteFile = _kernel32.WriteFile
    _WriteFile.argtypes = (
        wintypes.HANDLE,
        wintypes.LPCVOID,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
        wintypes.LPVOID,
    )
    _WriteFile.restype = wintypes.BOOL

    _ReadFile = _kernel32.ReadFile
    _ReadFile.argtypes = (
        wintypes.HANDLE,
        wintypes.LPVOID,
        wintypes.DWORD,
        ctypes.POINTER(wintypes.DWORD),
        wintypes.LPVOID,
    )
    _ReadFile.restype = wintypes.BOOL

    _SetFilePointerEx = _kernel32.SetFilePointerEx
    _SetFilePointerEx.argtypes = (
        wintypes.HANDLE,
        ctypes.c_longlong,
        ctypes.POINTER(ctypes.c_longlong),
        wintypes.DWORD,
    )
    _SetFilePointerEx.restype = wintypes.BOOL

    _FlushFileBuffers = _kernel32.FlushFileBuffers
    _FlushFileBuffers.argtypes = (wintypes.HANDLE,)
    _FlushFileBuffers.restype = wintypes.BOOL

    _GetFinalPathNameByHandleW = _kernel32.GetFinalPathNameByHandleW
    _GetFinalPathNameByHandleW.argtypes = (
        wintypes.HANDLE,
        wintypes.LPWSTR,
        wintypes.DWORD,
        wintypes.DWORD,
    )
    _GetFinalPathNameByHandleW.restype = wintypes.DWORD

    _NtCreateFile = _ntdll.NtCreateFile
    _NtCreateFile.argtypes = (
        ctypes.POINTER(wintypes.HANDLE),
        wintypes.ULONG,
        ctypes.POINTER(_OBJECT_ATTRIBUTES),
        ctypes.POINTER(_IO_STATUS_BLOCK),
        ctypes.POINTER(ctypes.c_longlong),
        wintypes.ULONG,
        wintypes.ULONG,
        wintypes.ULONG,
        wintypes.ULONG,
        wintypes.LPVOID,
        wintypes.ULONG,
    )
    _NtCreateFile.restype = wintypes.LONG


@dataclass(frozen=True, slots=True)
class WindowsFileIdentity:
    """A stable Windows file identifier scoped to a volume."""

    volume_serial: int
    file_id: str


@dataclass(frozen=True, slots=True)
class WindowsFileSnapshot:
    """Identity and length observed on a retained native handle."""

    identity: WindowsFileIdentity
    length: int


@dataclass(frozen=True, slots=True)
class _CapturedPath:
    text: str
    volume_root: str
    components: tuple[str, ...]


class _OwnedHandle:
    __slots__ = ("_value",)

    def __init__(self, value: int) -> None:
        if not value or value == _INVALID_HANDLE_VALUE:
            raise AcquisitionError("invalid_native_handle")
        self._value: int | None = value

    @property
    def value(self) -> int:
        if self._value is None:
            raise AcquisitionError("native_handle_closed")
        return self._value

    def close(self) -> bool:
        value = self._value
        if value is None:
            return True
        self._value = None
        return bool(_CloseHandle(wintypes.HANDLE(value)))


class _DirectoryChain:
    __slots__ = ("captured", "handles", "identities", "_closed")

    def __init__(
        self,
        captured: _CapturedPath,
        handles: tuple[_OwnedHandle, ...],
        identities: tuple[WindowsFileIdentity, ...],
    ) -> None:
        self.captured = captured
        self.handles = handles
        self.identities = identities
        self._closed = False

    @property
    def final_handle(self) -> int:
        return self.handles[-1].value

    @property
    def final_identity(self) -> WindowsFileIdentity:
        return self.identities[-1]

    def revalidate(self, error_code: str) -> None:
        if self._closed:
            raise AcquisitionError("directory_chain_closed")
        for handle, expected in zip(self.handles, self.identities, strict=True):
            snapshot = _query_directory(handle.value, error_code)
            if snapshot.identity != expected:
                raise AcquisitionError(error_code)

        reopened: list[_OwnedHandle] = []
        try:
            for index, component in enumerate(self.captured.components):
                parent = self.handles[0].value if index == 0 else reopened[-1].value
                child = _open_relative_directory(parent, component, error_code)
                reopened.append(child)
                if _query_directory(child.value, error_code).identity != self.identities[index + 1]:
                    raise AcquisitionError(error_code)
        finally:
            _close_many(reopened)

    def close(self) -> bool:
        if self._closed:
            return True
        self._closed = True
        return _close_many(list(reversed(self.handles)))


class _RepositoryRootBinding:
    """One read-only absolute binding for the repository exclusion root."""

    __slots__ = ("captured", "handle", "identity", "final_path", "_closed")

    def __init__(
        self,
        captured: _CapturedPath,
        handle: _OwnedHandle,
        identity: WindowsFileIdentity,
        final_path: str,
    ) -> None:
        self.captured = captured
        self.handle = handle
        self.identity = identity
        self.final_path = final_path
        self._closed = False

    @property
    def final_identity(self) -> WindowsFileIdentity:
        return self.identity

    def revalidate(self, error_code: str) -> None:
        if self._closed:
            raise AcquisitionError("repository_root_binding_closed")
        retained = _query_directory(self.handle.value, error_code)
        retained_path = _query_final_path(self.handle.value, error_code)
        if retained.identity != self.identity or retained_path != self.final_path:
            raise AcquisitionError(error_code)

        rebound = _open_repository_root_handle(self.captured, error_code)
        try:
            rebound_snapshot = _query_directory(rebound.value, error_code)
            rebound_path = _query_final_path(rebound.value, error_code)
            if (
                rebound_snapshot.identity != self.identity
                or rebound_path != self.final_path
            ):
                raise AcquisitionError(error_code)
        finally:
            if not rebound.close():
                raise AcquisitionError("repository_root_binding_close_failed")

    def close(self) -> bool:
        if self._closed:
            return True
        self._closed = True
        return self.handle.close()


class SecureCreatedFile:
    """One exclusively created file plus every retained authority handle."""

    __slots__ = (
        "destination",
        "filename",
        "_repository_root",
        "_parent_chain",
        "_tree_root",
        "_parent_components",
        "_file",
        "_identity",
        "_closed",
    )

    def __init__(
        self,
        destination: str,
        filename: str,
        repository_root: _RepositoryRootBinding | None,
        parent_chain: _DirectoryChain | None,
        file_handle: _OwnedHandle,
        identity: WindowsFileIdentity,
        tree_root: SecureDirectoryRoot | None = None,
        parent_components: tuple[str, ...] = (),
    ) -> None:
        self.destination = destination
        self.filename = filename
        self._repository_root = repository_root
        self._parent_chain = parent_chain
        self._tree_root = tree_root
        self._parent_components = parent_components
        self._file = file_handle
        self._identity = identity
        self._closed = False

    @property
    def identity(self) -> WindowsFileIdentity:
        return self._identity

    def snapshot(self, error_code: str = "destination_file_invalid") -> WindowsFileSnapshot:
        snapshot = _query_regular_file(self._file.value, error_code)
        if snapshot.identity != self._identity:
            raise AcquisitionError("destination_identity_changed")
        return snapshot

    def write_all(self, data: bytes) -> None:
        if type(data) is not bytes or not data or len(data) > _MAX_DWORD:
            raise AcquisitionError("destination_write_input_invalid")
        buffer = ctypes.create_string_buffer(data)
        written = wintypes.DWORD()
        if not _WriteFile(
            wintypes.HANDLE(self._file.value),
            buffer,
            len(data),
            ctypes.byref(written),
            None,
        ):
            raise AcquisitionError("destination_write_failed")
        if written.value != len(data):
            raise AcquisitionError("destination_write_incomplete")

    def flush(self) -> None:
        if not _FlushFileBuffers(wintypes.HANDLE(self._file.value)):
            raise AcquisitionError("destination_sync_failed")

    def readback_sha256(self, expected_size: int, block_size: int) -> str:
        if type(expected_size) is not int or expected_size < 0:
            raise AcquisitionError("destination_readback_size_invalid")
        if type(block_size) is not int or block_size <= 0 or block_size > _MAX_DWORD:
            raise AcquisitionError("destination_readback_block_invalid")
        new_position = ctypes.c_longlong()
        if not _SetFilePointerEx(
            wintypes.HANDLE(self._file.value),
            0,
            ctypes.byref(new_position),
            _FILE_BEGIN,
        ):
            raise AcquisitionError("destination_seek_failed")

        digest = hashlib.sha256()
        observed = 0
        while observed < expected_size:
            requested = min(block_size, expected_size - observed)
            buffer = ctypes.create_string_buffer(requested)
            read = wintypes.DWORD()
            if not _ReadFile(
                wintypes.HANDLE(self._file.value),
                buffer,
                requested,
                ctypes.byref(read),
                None,
            ):
                raise AcquisitionError("destination_readback_failed")
            if read.value == 0:
                raise AcquisitionError("destination_readback_incomplete")
            digest.update(buffer.raw[: read.value])
            observed += read.value

        trailing = ctypes.create_string_buffer(1)
        trailing_count = wintypes.DWORD()
        if not _ReadFile(
            wintypes.HANDLE(self._file.value),
            trailing,
            1,
            ctypes.byref(trailing_count),
            None,
        ):
            raise AcquisitionError("destination_readback_failed")
        if trailing_count.value:
            raise AcquisitionError("destination_readback_size_mismatch")
        return digest.hexdigest()

    def final_reauthenticate(self, expected_size: int) -> WindowsFileSnapshot:
        """Recheck file/name binding and both retained directory chains."""

        before = self.snapshot("destination_final_file_invalid")
        if before.length != expected_size:
            raise AcquisitionError("destination_size_changed")
        parent_handle = self._revalidate_binding()

        rebound = _open_relative_file_for_read(
            parent_handle,
            self.filename,
            "destination_binding_unavailable",
        )
        try:
            rebound_snapshot = _query_regular_file(
                rebound.value, "destination_binding_unsafe"
            )
            if rebound_snapshot != before:
                raise AcquisitionError("destination_binding_changed")
        finally:
            if not rebound.close():
                raise AcquisitionError("destination_binding_close_failed")

        self._revalidate_binding()
        after = self.snapshot("destination_final_file_invalid")
        if after != before:
            raise AcquisitionError("destination_final_checkpoint_changed")
        return after

    def _revalidate_binding(self) -> int:
        if self._tree_root is not None:
            self._tree_root.revalidate()
            return self._tree_root._directory_handle(self._parent_components)
        if self._repository_root is None or self._parent_chain is None:
            raise AcquisitionError("created_file_binding_invalid")
        self._repository_root.revalidate("repository_root_identity_changed")
        self._parent_chain.revalidate("destination_parent_identity_changed")
        return self._parent_chain.final_handle

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        file_ok = self._file.close()
        if self._tree_root is not None:
            self._tree_root._release_file()
            parent_ok = True
            repository_ok = True
        else:
            parent_ok = self._parent_chain.close() if self._parent_chain else True
            repository_ok = (
                self._repository_root.close() if self._repository_root else True
            )
        if not (file_ok and parent_ok and repository_ok):
            raise AcquisitionError("secure_handle_close_failed")


class SecureExistingFile:
    """A retained existing file opened relative to a retained parent handle."""

    __slots__ = (
        "path",
        "filename",
        "_repository_root",
        "_parent_chain",
        "_tree_root",
        "_parent_components",
        "_file",
        "_identity",
        "_initial_length",
        "_closed",
    )

    def __init__(
        self,
        *,
        path: str,
        filename: str,
        file_handle: _OwnedHandle,
        snapshot: WindowsFileSnapshot,
        repository_root: _RepositoryRootBinding | None = None,
        parent_chain: _DirectoryChain | None = None,
        tree_root: SecureDirectoryRoot | None = None,
        parent_components: tuple[str, ...] = (),
    ) -> None:
        if tree_root is None and (repository_root is None or parent_chain is None):
            raise AcquisitionError("existing_file_binding_invalid")
        if tree_root is not None and (repository_root is not None or parent_chain is not None):
            raise AcquisitionError("existing_file_binding_invalid")
        self.path = path
        self.filename = filename
        self._repository_root = repository_root
        self._parent_chain = parent_chain
        self._tree_root = tree_root
        self._parent_components = parent_components
        self._file = file_handle
        self._identity = snapshot.identity
        self._initial_length = snapshot.length
        self._closed = False

    @property
    def identity(self) -> WindowsFileIdentity:
        return self._identity

    @property
    def initial_length(self) -> int:
        return self._initial_length

    def snapshot(self, error_code: str = "existing_file_invalid") -> WindowsFileSnapshot:
        snapshot = _query_regular_file(self._file.value, error_code)
        if snapshot.identity != self._identity:
            raise AcquisitionError("existing_file_identity_changed")
        return snapshot

    def readback_sha256(self, expected_size: int, block_size: int) -> str:
        return _readback_sha256(
            self._file.value,
            expected_size,
            block_size,
            "existing_file",
        )

    def read(self, size: int = -1) -> bytes:
        """Read from the retained archive handle; no path reopen occurs."""

        if type(size) is not int or size < -1:
            raise AcquisitionError("existing_file_read_size_invalid")
        if size == -1:
            current = self.tell()
            length = self.snapshot("existing_file_invalid").length
            size = max(0, length - current)
        return _read_handle(self._file.value, size, "existing_file_read_failed")

    def seek(self, offset: int, whence: int = os.SEEK_SET) -> int:
        """Seek the same retained archive handle used for authentication."""

        if type(offset) is not int or type(whence) is not int:
            raise AcquisitionError("existing_file_seek_invalid")
        origins = {
            os.SEEK_SET: _FILE_BEGIN,
            os.SEEK_CUR: _FILE_CURRENT,
            os.SEEK_END: _FILE_END,
        }
        origin = origins.get(whence)
        if origin is None:
            raise AcquisitionError("existing_file_seek_invalid")
        return _seek_handle(
            self._file.value, offset, origin, "existing_file_seek_failed"
        )

    def tell(self) -> int:
        return _seek_handle(
            self._file.value, 0, _FILE_CURRENT, "existing_file_tell_failed"
        )

    def readable(self) -> bool:
        return not self._closed

    def seekable(self) -> bool:
        return not self._closed

    def writable(self) -> bool:
        return False

    @property
    def closed(self) -> bool:
        return self._closed

    def revalidate(self) -> WindowsFileSnapshot:
        before = self.snapshot("existing_file_invalid")
        parent_handle = self._revalidate_binding()
        rebound = _open_relative_file_stable(
            parent_handle, self.filename, "existing_file_binding_unavailable"
        )
        try:
            rebound_snapshot = _query_regular_file(
                rebound.value, "existing_file_binding_unsafe"
            )
            if rebound_snapshot != before:
                raise AcquisitionError("existing_file_binding_changed")
        finally:
            if not rebound.close():
                raise AcquisitionError("existing_file_binding_close_failed")
        self._revalidate_binding()
        after = self.snapshot("existing_file_invalid")
        if after != before:
            raise AcquisitionError("existing_file_checkpoint_changed")
        return after

    def _revalidate_binding(self) -> int:
        if self._tree_root is not None:
            self._tree_root.revalidate()
            return self._tree_root._directory_handle(self._parent_components)
        if self._repository_root is None or self._parent_chain is None:
            raise AcquisitionError("existing_file_binding_invalid")
        self._repository_root.revalidate("repository_root_identity_changed")
        self._parent_chain.revalidate("existing_file_parent_identity_changed")
        return self._parent_chain.final_handle

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        file_ok = self._file.close()
        if self._tree_root is not None:
            self._tree_root._release_file()
            parent_ok = True
            repository_ok = True
        else:
            parent_ok = self._parent_chain.close() if self._parent_chain else True
            repository_ok = (
                self._repository_root.close() if self._repository_root else True
            )
        if not (file_ok and parent_ok and repository_ok):
            raise AcquisitionError("secure_handle_close_failed")


class SecureDirectoryRoot:
    """Fresh retained directory tree rooted outside the repository."""

    __slots__ = (
        "destination",
        "dirname",
        "_repository_root",
        "_parent_chain",
        "_handles",
        "_identities",
        "_active_files",
        "_failed",
        "_closed",
    )

    def __init__(
        self,
        *,
        destination: str,
        dirname: str,
        repository_root: _RepositoryRootBinding,
        parent_chain: _DirectoryChain,
        root_handle: _OwnedHandle,
        root_identity: WindowsFileIdentity,
    ) -> None:
        self.destination = destination
        self.dirname = dirname
        self._repository_root = repository_root
        self._parent_chain = parent_chain
        self._handles: dict[tuple[str, ...], _OwnedHandle] = {(): root_handle}
        self._identities: dict[tuple[str, ...], WindowsFileIdentity] = {
            (): root_identity
        }
        self._active_files = 0
        self._failed = False
        self._closed = False

    @property
    def identity(self) -> WindowsFileIdentity:
        return self._identities[()]

    def create_directory(
        self, components: tuple[str, ...]
    ) -> WindowsFileIdentity:
        """Exclusively create and retain a directory tuple below this root."""

        validated = _validate_components(components)
        self._require_usable()
        if not validated or validated in self._handles:
            raise AcquisitionError("directory_not_fresh")
        try:
            for index in range(1, len(validated) + 1):
                key = validated[:index]
                if key in self._handles:
                    continue
                parent_key = validated[: index - 1]
                created = _create_relative_directory(
                    self._handles[parent_key].value, key[-1]
                )
                try:
                    snapshot = _query_directory(created.value, "created_directory_invalid")
                except Exception:
                    created.close()
                    raise
                self._handles[key] = created
                self._identities[key] = snapshot.identity
            self.revalidate()
            return self._identities[validated]
        except Exception:
            self._failed = True
            raise

    def open_directory(self, components: tuple[str, ...]) -> WindowsFileIdentity:
        """Reopen a retained directory tuple without granting new authority."""

        validated = _validate_components(components, allow_empty=True)
        self._require_usable()
        if validated not in self._handles:
            raise AcquisitionError("directory_not_retained")
        self.revalidate()
        reopened = _open_relative_directory_path(
            self._handles[()].value,
            validated,
            "directory_binding_unavailable",
        )
        if reopened is None:
            return self._identities[()]
        try:
            snapshot = _query_directory(reopened.value, "directory_binding_unsafe")
            if snapshot.identity != self._identities[validated]:
                raise AcquisitionError("directory_binding_changed")
            return snapshot.identity
        finally:
            if not reopened.close():
                raise AcquisitionError("directory_binding_close_failed")

    def create_file(
        self,
        parent_components: tuple[str, ...],
        filename: str,
    ) -> SecureCreatedFile:
        """Exclusively create a file relative to a retained tree directory."""

        parent = _validate_components(parent_components, allow_empty=True)
        leaf = _validate_leaf(filename, "invalid_destination_filename")
        self._require_usable()
        if parent not in self._handles:
            raise AcquisitionError("directory_not_retained")
        created: _OwnedHandle | None = None
        try:
            created = _create_relative_file(self._handles[parent].value, leaf)
            snapshot = _query_regular_file(created.value, "created_file_invalid")
            if snapshot.length != 0:
                raise AcquisitionError("created_file_not_empty")
            self.revalidate()
            self._active_files += 1
            return SecureCreatedFile(
                destination=_join_destination(self.destination, parent, leaf),
                filename=leaf,
                repository_root=None,
                parent_chain=None,
                file_handle=created,
                identity=snapshot.identity,
                tree_root=self,
                parent_components=parent,
            )
        except Exception:
            self._failed = True
            if created is not None:
                created.close()
            raise

    def open_file(
        self,
        parent_components: tuple[str, ...],
        filename: str,
        *,
        expected_identity: WindowsFileIdentity | None = None,
    ) -> SecureExistingFile:
        """Retain an existing output by parent handle and exact leaf name."""

        parent = _validate_components(parent_components, allow_empty=True)
        leaf = _validate_leaf(filename, "invalid_existing_filename")
        expected = _validate_expected_identity(expected_identity)
        self._require_usable()
        if parent not in self._handles:
            raise AcquisitionError("directory_not_retained")
        opened: _OwnedHandle | None = None
        try:
            opened = _open_relative_file_stable(
                self._handles[parent].value, leaf, "existing_file_open_failed"
            )
            snapshot = _query_regular_file(opened.value, "existing_file_invalid")
            if expected is not None and snapshot.identity != expected:
                raise AcquisitionError("existing_file_identity_mismatch")
            self.revalidate()
            self._active_files += 1
            return SecureExistingFile(
                path=_join_destination(self.destination, parent, leaf),
                filename=leaf,
                file_handle=opened,
                snapshot=snapshot,
                tree_root=self,
                parent_components=parent,
            )
        except Exception:
            self._failed = True
            if opened is not None:
                opened.close()
            raise

    def revalidate(self) -> None:
        self._require_usable()
        try:
            self._revalidate_retained_tree()
        except Exception:
            self._failed = True
            raise

    def _revalidate_retained_tree(self) -> None:
        self._require_usable()
        self._repository_root.revalidate("repository_root_identity_changed")
        self._parent_chain.revalidate("destination_parent_identity_changed")

        root_binding = _open_relative_directory_existing(
            self._parent_chain.final_handle,
            self.dirname,
            "directory_root_binding_unavailable",
        )
        try:
            root_snapshot = _query_directory(
                root_binding.value, "directory_root_binding_unsafe"
            )
            if root_snapshot.identity != self._identities[()]:
                raise AcquisitionError("directory_root_binding_changed")
        finally:
            if not root_binding.close():
                raise AcquisitionError("directory_root_binding_close_failed")

        for components, handle in self._handles.items():
            snapshot = _query_directory(handle.value, "directory_tree_invalid")
            if snapshot.identity != self._identities[components]:
                raise AcquisitionError("directory_tree_identity_changed")
            if not components:
                continue
            parent = self._handles[components[:-1]]
            rebound = _open_relative_directory_existing(
                parent.value,
                components[-1],
                "directory_tree_binding_unavailable",
            )
            try:
                rebound_snapshot = _query_directory(
                    rebound.value, "directory_tree_binding_unsafe"
                )
                if rebound_snapshot.identity != snapshot.identity:
                    raise AcquisitionError("directory_tree_binding_changed")
            finally:
                if not rebound.close():
                    raise AcquisitionError("directory_tree_binding_close_failed")

        self._repository_root.revalidate("repository_root_identity_changed")
        self._parent_chain.revalidate("destination_parent_identity_changed")

    def close(self) -> None:
        if self._closed:
            return
        if self._active_files:
            raise AcquisitionError("directory_root_has_open_files")
        self._closed = True
        tree_ok = _close_many(list(reversed(tuple(self._handles.values()))))
        parent_ok = self._parent_chain.close()
        repository_ok = self._repository_root.close()
        if not (tree_ok and parent_ok and repository_ok):
            raise AcquisitionError("secure_handle_close_failed")

    def _require_usable(self) -> None:
        if self._closed:
            raise AcquisitionError("directory_root_closed")
        if self._failed:
            raise AcquisitionError("directory_root_failed")

    def _directory_handle(self, components: tuple[str, ...]) -> int:
        self._require_usable()
        handle = self._handles.get(components)
        if handle is None:
            raise AcquisitionError("directory_not_retained")
        return handle.value

    def _release_file(self) -> None:
        if self._active_files <= 0:
            raise AcquisitionError("directory_root_file_count_invalid")
        self._active_files -= 1


def secure_create_file(
    *,
    repository_root: str | os.PathLike[str],
    destination: str | os.PathLike[str],
    expected_filename: str,
) -> SecureCreatedFile:
    """Exclusively create *destination* outside *repository_root*.

    There is deliberately no path-based creation fallback.  A zero-length
    file may remain after any post-create failure and is never removed here.
    """

    _require_windows()
    filename = _validate_leaf(expected_filename, "invalid_pin_filename")
    repository_path = _capture_absolute_path(
        repository_root, "repository_root_invalid"
    )
    destination_path = _capture_absolute_path(destination, "destination_invalid")
    if not destination_path.components:
        raise AcquisitionError("destination_missing_filename")
    if destination_path.components[-1] != filename:
        raise AcquisitionError("destination_filename_mismatch")

    parent_path = _CapturedPath(
        text=ntpath.dirname(destination_path.text),
        volume_root=destination_path.volume_root,
        components=destination_path.components[:-1],
    )
    repository_binding: _RepositoryRootBinding | None = None
    parent_chain: _DirectoryChain | None = None
    created: _OwnedHandle | None = None
    try:
        repository_binding = _open_repository_root(
            repository_path, "repository_root_unavailable"
        )
        parent_chain = _open_directory_chain(
            parent_path, "destination_parent_unavailable"
        )
        if repository_binding.final_identity in parent_chain.identities:
            raise AcquisitionError("destination_inside_repository")

        created = _create_relative_file(parent_chain.final_handle, filename)
        snapshot = _query_regular_file(created.value, "created_file_invalid")
        if snapshot.length != 0:
            raise AcquisitionError("created_file_not_empty")
        repository_binding.revalidate("repository_root_identity_changed")
        parent_chain.revalidate("destination_parent_identity_changed")
        return SecureCreatedFile(
            destination=destination_path.text,
            filename=filename,
            repository_root=repository_binding,
            parent_chain=parent_chain,
            file_handle=created,
            identity=snapshot.identity,
        )
    except Exception:
        if created is not None:
            created.close()
        if parent_chain is not None:
            parent_chain.close()
        if repository_binding is not None:
            repository_binding.close()
        raise


def secure_create_directory_root(
    *,
    repository_root: str | os.PathLike[str],
    destination: str | os.PathLike[str],
) -> SecureDirectoryRoot:
    """Exclusively create and retain a fresh directory outside the repository."""

    _require_windows()
    repository_path = _capture_absolute_path(
        repository_root, "repository_root_invalid"
    )
    destination_path = _capture_absolute_path(destination, "destination_invalid")
    if not destination_path.components:
        raise AcquisitionError("destination_missing_directory")
    dirname = destination_path.components[-1]
    parent_path = _CapturedPath(
        text=ntpath.dirname(destination_path.text),
        volume_root=destination_path.volume_root,
        components=destination_path.components[:-1],
    )
    repository_binding: _RepositoryRootBinding | None = None
    parent_chain: _DirectoryChain | None = None
    created: _OwnedHandle | None = None
    try:
        repository_binding = _open_repository_root(
            repository_path, "repository_root_unavailable"
        )
        parent_chain = _open_directory_chain(
            parent_path, "destination_parent_unavailable"
        )
        if repository_binding.final_identity in parent_chain.identities:
            raise AcquisitionError("destination_inside_repository")
        created = _create_relative_directory(parent_chain.final_handle, dirname)
        snapshot = _query_directory(created.value, "created_directory_invalid")
        repository_binding.revalidate("repository_root_identity_changed")
        parent_chain.revalidate("destination_parent_identity_changed")
        return SecureDirectoryRoot(
            destination=destination_path.text,
            dirname=dirname,
            repository_root=repository_binding,
            parent_chain=parent_chain,
            root_handle=created,
            root_identity=snapshot.identity,
        )
    except Exception:
        if created is not None:
            created.close()
        if parent_chain is not None:
            parent_chain.close()
        if repository_binding is not None:
            repository_binding.close()
        raise


def secure_open_existing_file(
    *,
    repository_root: str | os.PathLike[str],
    path: str | os.PathLike[str],
    expected_identity: WindowsFileIdentity | None = None,
) -> SecureExistingFile:
    """Open an existing external file through retained no-reparse handles."""

    _require_windows()
    expected = _validate_expected_identity(expected_identity)
    repository_path = _capture_absolute_path(
        repository_root, "repository_root_invalid"
    )
    existing_path = _capture_absolute_path(path, "existing_file_path_invalid")
    if not existing_path.components:
        raise AcquisitionError("existing_file_missing_filename")
    filename = existing_path.components[-1]
    parent_path = _CapturedPath(
        text=ntpath.dirname(existing_path.text),
        volume_root=existing_path.volume_root,
        components=existing_path.components[:-1],
    )
    repository_binding: _RepositoryRootBinding | None = None
    parent_chain: _DirectoryChain | None = None
    opened: _OwnedHandle | None = None
    try:
        repository_binding = _open_repository_root(
            repository_path, "repository_root_unavailable"
        )
        parent_chain = _open_directory_chain(
            parent_path, "existing_file_parent_unavailable"
        )
        if repository_binding.final_identity in parent_chain.identities:
            raise AcquisitionError("existing_file_inside_repository")
        opened = _open_relative_file_stable(
            parent_chain.final_handle, filename, "existing_file_open_failed"
        )
        snapshot = _query_regular_file(opened.value, "existing_file_invalid")
        if expected is not None and snapshot.identity != expected:
            raise AcquisitionError("existing_file_identity_mismatch")
        repository_binding.revalidate("repository_root_identity_changed")
        parent_chain.revalidate("existing_file_parent_identity_changed")
        return SecureExistingFile(
            path=existing_path.text,
            filename=filename,
            file_handle=opened,
            snapshot=snapshot,
            repository_root=repository_binding,
            parent_chain=parent_chain,
        )
    except Exception:
        if opened is not None:
            opened.close()
        if parent_chain is not None:
            parent_chain.close()
        if repository_binding is not None:
            repository_binding.close()
        raise


def _require_windows() -> None:
    if os.name != "nt":
        raise AcquisitionError("windows_required")


def _validate_leaf(value: object, error_code: str) -> str:
    if type(value) is not str or not value:
        raise AcquisitionError(error_code)
    if value in (".", "..") or value[-1] in (" ", "."):
        raise AcquisitionError(error_code)
    if any(ord(character) < 32 or character in '\\/:*?"<>|' for character in value):
        raise AcquisitionError(error_code)
    return value


def _validate_components(
    value: object, *, allow_empty: bool = False
) -> tuple[str, ...]:
    if type(value) is not tuple or (not value and not allow_empty):
        raise AcquisitionError("invalid_relative_components")
    return tuple(
        _validate_leaf(component, "invalid_relative_component")
        for component in value
    )


def _validate_expected_identity(
    value: WindowsFileIdentity | None,
) -> WindowsFileIdentity | None:
    if value is None:
        return None
    if type(value) is not WindowsFileIdentity:
        raise AcquisitionError("invalid_expected_identity")
    if type(value.volume_serial) is not int or value.volume_serial < 0:
        raise AcquisitionError("invalid_expected_identity")
    if (
        type(value.file_id) is not str
        or len(value.file_id) != 32
        or value.file_id != value.file_id.lower()
        or any(character not in "0123456789abcdef" for character in value.file_id)
    ):
        raise AcquisitionError("invalid_expected_identity")
    return value


def _join_destination(
    root: str, parent_components: tuple[str, ...], filename: str
) -> str:
    suffix = (*parent_components, filename)
    return root + "\\" + "\\".join(suffix)


def _capture_absolute_path(
    value: str | os.PathLike[str], error_code: str
) -> _CapturedPath:
    try:
        raw = os.fspath(value)
    except (TypeError, ValueError, OSError) as exc:
        raise AcquisitionError(error_code) from exc
    if type(raw) is not str or not raw or "\x00" in raw:
        raise AcquisitionError(error_code)
    normalized = raw.replace("/", "\\")
    drive, tail = ntpath.splitdrive(normalized)
    if not re.fullmatch(r"[A-Za-z]:", drive) or not tail.startswith("\\"):
        raise AcquisitionError(error_code)
    if tail.startswith("\\\\"):
        raise AcquisitionError(error_code)
    raw_components = tail[1:].split("\\") if len(tail) > 1 else []
    if any(not component for component in raw_components):
        raise AcquisitionError(error_code)
    components = tuple(
        _validate_leaf(component, error_code) for component in raw_components
    )
    volume_root = f"\\\\?\\{drive.upper()}\\"
    text = f"{drive.upper()}\\" + "\\".join(components)
    return _CapturedPath(text=text, volume_root=volume_root, components=components)


def _open_directory_chain(
    captured: _CapturedPath, error_code: str
) -> _DirectoryChain:
    handles: list[_OwnedHandle] = []
    identities: list[WindowsFileIdentity] = []
    try:
        root = _open_volume_root(captured.volume_root, error_code)
        handles.append(root)
        identities.append(_query_directory(root.value, error_code).identity)
        for component in captured.components:
            child = _open_relative_directory(handles[-1].value, component, error_code)
            handles.append(child)
            identities.append(_query_directory(child.value, error_code).identity)
        return _DirectoryChain(captured, tuple(handles), tuple(identities))
    except Exception:
        _close_many(list(reversed(handles)))
        raise


def _open_repository_root(
    captured: _CapturedPath, error_code: str
) -> _RepositoryRootBinding:
    handle: _OwnedHandle | None = None
    try:
        handle = _open_repository_root_handle(captured, error_code)
        snapshot = _query_directory(handle.value, error_code)
        final_path = _query_final_path(handle.value, error_code)
        return _RepositoryRootBinding(
            captured=captured,
            handle=handle,
            identity=snapshot.identity,
            final_path=final_path,
        )
    except Exception:
        if handle is not None:
            handle.close()
        raise


def _open_repository_root_handle(
    captured: _CapturedPath, error_code: str
) -> _OwnedHandle:
    absolute_path = f"\\\\?\\{captured.text}"
    handle = _CreateFileW(
        absolute_path,
        _FILE_READ_ATTRIBUTES | _SYNCHRONIZE,
        _FILE_SHARE_READ,
        None,
        _OPEN_EXISTING,
        _FILE_FLAG_BACKUP_SEMANTICS | _FILE_FLAG_OPEN_REPARSE_POINT,
        None,
    )
    value = ctypes.cast(handle, ctypes.c_void_p).value
    if not value or value == _INVALID_HANDLE_VALUE:
        raise AcquisitionError(error_code)
    return _OwnedHandle(value)


def _open_volume_root(volume_root: str, error_code: str) -> _OwnedHandle:
    handle = _CreateFileW(
        volume_root,
        (
            _FILE_LIST_DIRECTORY
            | _FILE_TRAVERSE
            | _FILE_READ_ATTRIBUTES
            | _SYNCHRONIZE
        ),
        _FILE_SHARE_READ | _FILE_SHARE_WRITE,
        None,
        _OPEN_EXISTING,
        _FILE_FLAG_BACKUP_SEMANTICS | _FILE_FLAG_OPEN_REPARSE_POINT,
        None,
    )
    value = ctypes.cast(handle, ctypes.c_void_p).value
    if not value or value == _INVALID_HANDLE_VALUE:
        raise AcquisitionError(error_code)
    owned = _OwnedHandle(value)
    try:
        _query_directory(owned.value, error_code)
        _require_volume_root_binding(owned.value, error_code)
    except Exception:
        owned.close()
        raise
    return owned


def _require_volume_root_binding(handle: int, error_code: str) -> None:
    final_name = _query_final_path(handle, error_code)
    if not re.fullmatch(r"\\\\\?\\Volume\{[0-9A-Fa-f-]+\}", final_name):
        raise AcquisitionError(error_code)


def _query_final_path(handle: int, error_code: str) -> str:
    required = _GetFinalPathNameByHandleW(
        wintypes.HANDLE(handle), None, 0, _VOLUME_NAME_GUID
    )
    if required == 0:
        raise AcquisitionError(error_code)
    buffer = ctypes.create_unicode_buffer(required)
    written = _GetFinalPathNameByHandleW(
        wintypes.HANDLE(handle), buffer, required, _VOLUME_NAME_GUID
    )
    if written == 0 or written >= required:
        raise AcquisitionError(error_code)
    final_name = buffer.value.rstrip("\\")
    if not re.fullmatch(
        r"\\\\\?\\Volume\{[0-9A-Fa-f-]+\}(?:\\.*)?", final_name
    ):
        raise AcquisitionError(error_code)
    return final_name


def _open_relative_directory(
    parent_handle: int, component: str, error_code: str
) -> _OwnedHandle:
    return _nt_create_relative(
        parent_handle=parent_handle,
        name=component,
        desired_access=_FILE_READ_ATTRIBUTES,
        share_access=_FILE_SHARE_READ | _FILE_SHARE_WRITE,
        disposition=_FILE_OPEN,
        options=(
            _FILE_DIRECTORY_FILE
            | _FILE_OPEN_FOR_BACKUP_INTENT
            | _FILE_OPEN_REPARSE_POINT
        ),
        error_code=error_code,
    )


def _create_relative_directory(parent_handle: int, component: str) -> _OwnedHandle:
    return _nt_create_relative(
        parent_handle=parent_handle,
        name=component,
        desired_access=(
            _FILE_LIST_DIRECTORY | _FILE_TRAVERSE | _FILE_READ_ATTRIBUTES | _SYNCHRONIZE
        ),
        share_access=_FILE_SHARE_READ | _FILE_SHARE_WRITE,
        disposition=_FILE_CREATE,
        options=(
            _FILE_DIRECTORY_FILE
            | _FILE_SYNCHRONOUS_IO_NONALERT
            | _FILE_OPEN_FOR_BACKUP_INTENT
            | _FILE_OPEN_REPARSE_POINT
        ),
        error_code="directory_create_failed",
        collision_code="directory_not_fresh",
    )


def _open_relative_directory_existing(
    parent_handle: int, component: str, error_code: str
) -> _OwnedHandle:
    return _open_relative_directory(parent_handle, component, error_code)


def _open_relative_directory_path(
    root_handle: int,
    components: tuple[str, ...],
    error_code: str,
) -> _OwnedHandle | None:
    if not components:
        return None
    opened: list[_OwnedHandle] = []
    try:
        for component in components:
            parent = root_handle if not opened else opened[-1].value
            opened.append(_open_relative_directory(parent, component, error_code))
        result = opened.pop()
        if not _close_many(list(reversed(opened))):
            result.close()
            raise AcquisitionError("directory_binding_close_failed")
        return result
    except Exception:
        _close_many(list(reversed(opened)))
        raise


def _create_relative_file(parent_handle: int, filename: str) -> _OwnedHandle:
    return _nt_create_relative(
        parent_handle=parent_handle,
        name=filename,
        desired_access=(
            _FILE_READ_DATA
            | _FILE_WRITE_DATA
            | _FILE_READ_ATTRIBUTES
            | _SYNCHRONIZE
        ),
        share_access=_FILE_SHARE_READ,
        disposition=_FILE_CREATE,
        options=(
            _FILE_NON_DIRECTORY_FILE
            | _FILE_SYNCHRONOUS_IO_NONALERT
            | _FILE_OPEN_REPARSE_POINT
        ),
        error_code="destination_open_failed",
        collision_code="destination_not_fresh",
    )


def _open_relative_file_for_read(
    parent_handle: int, filename: str, error_code: str
) -> _OwnedHandle:
    return _nt_create_relative(
        parent_handle=parent_handle,
        name=filename,
        desired_access=_FILE_READ_DATA | _FILE_READ_ATTRIBUTES | _SYNCHRONIZE,
        share_access=_FILE_SHARE_READ | _FILE_SHARE_WRITE,
        disposition=_FILE_OPEN,
        options=(
            _FILE_NON_DIRECTORY_FILE
            | _FILE_SYNCHRONOUS_IO_NONALERT
            | _FILE_OPEN_REPARSE_POINT
        ),
        error_code=error_code,
    )


def _open_relative_file_stable(
    parent_handle: int, filename: str, error_code: str
) -> _OwnedHandle:
    return _nt_create_relative(
        parent_handle=parent_handle,
        name=filename,
        desired_access=_FILE_READ_DATA | _FILE_READ_ATTRIBUTES | _SYNCHRONIZE,
        share_access=_FILE_SHARE_READ,
        disposition=_FILE_OPEN,
        options=(
            _FILE_NON_DIRECTORY_FILE
            | _FILE_SYNCHRONOUS_IO_NONALERT
            | _FILE_OPEN_REPARSE_POINT
        ),
        error_code=error_code,
    )


def _nt_create_relative(
    *,
    parent_handle: int,
    name: str,
    desired_access: int,
    share_access: int,
    disposition: int,
    options: int,
    error_code: str,
    collision_code: str | None = None,
) -> _OwnedHandle:
    component = _validate_leaf(name, error_code)
    name_buffer = ctypes.create_unicode_buffer(component)
    byte_length = len(component.encode("utf-16-le"))
    if byte_length > 0xFFFC:
        raise AcquisitionError(error_code)
    unicode_name = _UNICODE_STRING(
        Length=byte_length,
        MaximumLength=byte_length + 2,
        Buffer=ctypes.cast(name_buffer, wintypes.LPWSTR),
    )
    attributes = _OBJECT_ATTRIBUTES(
        Length=ctypes.sizeof(_OBJECT_ATTRIBUTES),
        RootDirectory=wintypes.HANDLE(parent_handle),
        ObjectName=ctypes.pointer(unicode_name),
        Attributes=_OBJ_CASE_INSENSITIVE | _OBJ_DONT_REPARSE,
        SecurityDescriptor=None,
        SecurityQualityOfService=None,
    )
    output = wintypes.HANDLE()
    io_status = _IO_STATUS_BLOCK()
    status = int(
        _NtCreateFile(
            ctypes.byref(output),
            desired_access,
            ctypes.byref(attributes),
            ctypes.byref(io_status),
            None,
            _FILE_ATTRIBUTE_NORMAL,
            share_access,
            disposition,
            options,
            None,
            0,
        )
    )
    if status < 0:
        unsigned_status = status & 0xFFFFFFFF
        if collision_code is not None and unsigned_status == _STATUS_OBJECT_NAME_COLLISION:
            raise AcquisitionError(collision_code)
        raise AcquisitionError(
            f"{error_code}: NtCreateFile status=0x{unsigned_status:08X}"
        )
    value = ctypes.cast(output, ctypes.c_void_p).value
    if not value or value == _INVALID_HANDLE_VALUE:
        raise AcquisitionError(error_code)
    return _OwnedHandle(value)


def _query_identity(handle: int, error_code: str) -> WindowsFileIdentity:
    info = _FILE_ID_INFO()
    if not _GetFileInformationByHandleEx(
        wintypes.HANDLE(handle),
        _FILE_ID_INFO_CLASS,
        ctypes.byref(info),
        ctypes.sizeof(info),
    ):
        raise AcquisitionError(error_code)
    return WindowsFileIdentity(
        volume_serial=int(info.VolumeSerialNumber),
        file_id=bytes(info.FileId.Identifier).hex(),
    )


def _query_common(
    handle: int, error_code: str
) -> tuple[WindowsFileIdentity, _FILE_STANDARD_INFO, _FILE_ATTRIBUTE_TAG_INFO]:
    standard = _FILE_STANDARD_INFO()
    if not _GetFileInformationByHandleEx(
        wintypes.HANDLE(handle),
        _FILE_STANDARD_INFO_CLASS,
        ctypes.byref(standard),
        ctypes.sizeof(standard),
    ):
        raise AcquisitionError(error_code)
    attributes = _FILE_ATTRIBUTE_TAG_INFO()
    if not _GetFileInformationByHandleEx(
        wintypes.HANDLE(handle),
        _FILE_ATTRIBUTE_TAG_INFO_CLASS,
        ctypes.byref(attributes),
        ctypes.sizeof(attributes),
    ):
        raise AcquisitionError(error_code)
    if standard.DeletePending or attributes.FileAttributes & _FILE_ATTRIBUTE_REPARSE_POINT:
        raise AcquisitionError(error_code)
    return _query_identity(handle, error_code), standard, attributes


def _query_directory(handle: int, error_code: str) -> WindowsFileSnapshot:
    identity, standard, _ = _query_common(handle, error_code)
    if not standard.Directory:
        raise AcquisitionError(error_code)
    return WindowsFileSnapshot(identity=identity, length=int(standard.EndOfFile))


def _query_regular_file(handle: int, error_code: str) -> WindowsFileSnapshot:
    identity, standard, _ = _query_common(handle, error_code)
    if standard.Directory or standard.EndOfFile < 0:
        raise AcquisitionError(error_code)
    return WindowsFileSnapshot(identity=identity, length=int(standard.EndOfFile))


def _seek_handle(handle: int, offset: int, origin: int, error_code: str) -> int:
    new_position = ctypes.c_longlong()
    if not _SetFilePointerEx(
        wintypes.HANDLE(handle),
        offset,
        ctypes.byref(new_position),
        origin,
    ):
        raise AcquisitionError(error_code)
    if new_position.value < 0:
        raise AcquisitionError(error_code)
    return int(new_position.value)


def _read_handle(handle: int, size: int, error_code: str) -> bytes:
    if type(size) is not int or size < 0:
        raise AcquisitionError("native_read_size_invalid")
    remaining = size
    chunks: list[bytes] = []
    while remaining:
        requested = min(remaining, DEFAULT_NATIVE_READ_BLOCK_SIZE)
        buffer = ctypes.create_string_buffer(requested)
        read = wintypes.DWORD()
        if not _ReadFile(
            wintypes.HANDLE(handle),
            buffer,
            requested,
            ctypes.byref(read),
            None,
        ):
            raise AcquisitionError(error_code)
        if read.value == 0:
            break
        chunks.append(buffer.raw[: read.value])
        remaining -= read.value
        if read.value < requested:
            break
    return b"".join(chunks)


def _readback_sha256(
    handle: int,
    expected_size: int,
    block_size: int,
    error_prefix: str,
) -> str:
    if type(expected_size) is not int or expected_size < 0:
        raise AcquisitionError(f"{error_prefix}_readback_size_invalid")
    if type(block_size) is not int or block_size <= 0 or block_size > _MAX_DWORD:
        raise AcquisitionError(f"{error_prefix}_readback_block_invalid")
    _seek_handle(handle, 0, _FILE_BEGIN, f"{error_prefix}_seek_failed")
    digest = hashlib.sha256()
    observed = 0
    while observed < expected_size:
        data = _read_handle(
            handle,
            min(block_size, expected_size - observed),
            f"{error_prefix}_readback_failed",
        )
        if not data:
            raise AcquisitionError(f"{error_prefix}_readback_incomplete")
        digest.update(data)
        observed += len(data)
    if _read_handle(handle, 1, f"{error_prefix}_readback_failed"):
        raise AcquisitionError(f"{error_prefix}_readback_size_mismatch")
    return digest.hexdigest()


def _close_many(handles: list[_OwnedHandle]) -> bool:
    result = True
    for handle in handles:
        result = handle.close() and result
    return result


__all__ = [
    "SecureDirectoryRoot",
    "SecureCreatedFile",
    "SecureExistingFile",
    "WindowsFileIdentity",
    "WindowsFileSnapshot",
    "secure_create_directory_root",
    "secure_create_file",
    "secure_open_existing_file",
]

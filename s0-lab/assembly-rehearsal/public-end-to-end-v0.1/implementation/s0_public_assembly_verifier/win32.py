"""Literal Win64/NTFS publication ABI implementation.

This module defines the real adapter but performs no call at import time.
Implementation tests use its no-call binding surface; real file publication is
reserved for a separately opened platform/rehearsal gate.
"""

from __future__ import annotations

import ctypes
import hashlib
import platform
import sys
import weakref
from ctypes import wintypes
from pathlib import Path

from .errors import auth_failure, record_failure
from .models import FileIdentity, FileSnapshot, MoveResult


ABI_PROFILE_ID = "S0-WIN64-NTFS-MOVEFILEEXW-CTYPES-ABI-2"

_INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value
_INVALID_FILE_ATTRIBUTES = 0xFFFFFFFF
_GENERIC_READ = 0x80000000
_FILE_READ_ATTRIBUTES = 0x00000080
_FILE_SHARE_READ = 0x00000001
_FILE_SHARE_WRITE = 0x00000002
_FILE_SHARE_DELETE = 0x00000004
_OPEN_EXISTING = 3
_FILE_ATTRIBUTE_DIRECTORY = 0x00000010
_FILE_ATTRIBUTE_REPARSE_POINT = 0x00000400
_FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000
_FILE_FLAG_BACKUP_SEMANTICS = 0x02000000
_FILE_FLAG_SEQUENTIAL_SCAN = 0x08000000
_ERROR_FILE_NOT_FOUND = 2
_ERROR_PATH_NOT_FOUND = 3
_ERROR_HANDLE_EOF = 38
_DRIVE_FIXED = 3


# Construction, not structural resemblance, distinguishes the platform-
# authenticated backend from a test double.  The registry is process-local and
# never serialized; the candidate runs in a different process and cannot add
# an entry.
_AUTHENTICATED_BACKENDS: weakref.WeakSet[Win32PublicationBackend]


class _ByHandleFileInformation(ctypes.Structure):
    _fields_ = [
        ("dwFileAttributes", wintypes.DWORD),
        ("ftCreationTime", wintypes.FILETIME),
        ("ftLastAccessTime", wintypes.FILETIME),
        ("ftLastWriteTime", wintypes.FILETIME),
        ("dwVolumeSerialNumber", wintypes.DWORD),
        ("nFileSizeHigh", wintypes.DWORD),
        ("nFileSizeLow", wintypes.DWORD),
        ("nNumberOfLinks", wintypes.DWORD),
        ("nFileIndexHigh", wintypes.DWORD),
        ("nFileIndexLow", wintypes.DWORD),
    ]


class _LargeInteger(ctypes.Union):
    _fields_ = [("QuadPart", ctypes.c_int64)]


class _FindStreamData(ctypes.Structure):
    _fields_ = [("StreamSize", _LargeInteger), ("cStreamName", wintypes.WCHAR * 296)]


def _configure_move_file_ex(function: object) -> object:
    function.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32]
    function.restype = ctypes.c_int32
    return function


class MoveFileExBinding:
    """Exact no-replace MoveFileExW binding for the frozen 64-bit profile."""

    def __init__(self) -> None:
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        self._move_file_ex = _configure_move_file_ex(kernel32.MoveFileExW)

    @staticmethod
    def synthetic_no_call_binding(function: object) -> object:
        """Apply the exact signature without loading a DLL or making a call."""

        return _configure_move_file_ex(function)

    def call(self, source: str, destination: str, flags: int = 0) -> MoveResult:
        if type(source) is not str or type(destination) is not str:
            raise auth_failure("MoveFileExW paths must be exact strings")
        if not source.startswith("\\\\?\\") or not destination.startswith("\\\\?\\"):
            raise auth_failure("MoveFileExW paths must use the extended-length prefix")
        if "\x00" in source or "\x00" in destination:
            raise auth_failure("MoveFileExW paths must not contain embedded NUL")
        if type(flags) is not int or flags != 0:
            raise auth_failure("MoveFileExW flags must be exact numeric zero")
        flag_value = ctypes.c_uint32(flags)
        ctypes.set_last_error(0)
        result = self._move_file_ex(source, destination, flag_value)
        if result == 0:
            last_error = ctypes.get_last_error()
        else:
            last_error = 0
        return MoveResult(ctypes.c_int32(result).value, ctypes.c_uint32(last_error).value)


class Win32PublicationBackend:
    """Verifier-owned file inspection and real publication backend."""

    __slots__ = (
        "output_root",
        "_kernel32",
        "_move",
        "_root_identity",
        "_sealed",
        "__weakref__",
    )

    def __init__(self, output_root: Path) -> None:
        _require_supported_process()
        object.__setattr__(self, "_sealed", False)
        object.__setattr__(self, "output_root", _canonical_root(output_root))
        object.__setattr__(
            self,
            "_kernel32",
            ctypes.WinDLL("kernel32", use_last_error=True),
        )
        self._bind_helpers()
        object.__setattr__(self, "_move", MoveFileExBinding())
        object.__setattr__(self, "_root_identity", self._inspect_root_identity())
        filesystem, drive_type = self._volume_profile(self.output_root)
        if filesystem != "NTFS" or drive_type != _DRIVE_FIXED:
            raise auth_failure("output root is not on local NTFS")
        self._require_no_alternate_streams(self.output_root, preflight=True)
        object.__setattr__(self, "_sealed", True)
        _AUTHENTICATED_BACKENDS.add(self)

    def __setattr__(self, name: str, value: object) -> None:
        if getattr(self, "_sealed", False):
            raise AttributeError("authenticated Win32 backend is immutable")
        object.__setattr__(self, name, value)

    def _bind_helpers(self) -> None:
        k32 = self._kernel32
        k32.CreateFileW.argtypes = [
            ctypes.c_wchar_p,
            wintypes.DWORD,
            wintypes.DWORD,
            ctypes.c_void_p,
            wintypes.DWORD,
            wintypes.DWORD,
            wintypes.HANDLE,
        ]
        k32.CreateFileW.restype = wintypes.HANDLE
        k32.GetFileInformationByHandle.argtypes = [
            wintypes.HANDLE,
            ctypes.POINTER(_ByHandleFileInformation),
        ]
        k32.GetFileInformationByHandle.restype = wintypes.BOOL
        k32.ReadFile.argtypes = [
            wintypes.HANDLE,
            ctypes.c_void_p,
            wintypes.DWORD,
            ctypes.POINTER(wintypes.DWORD),
            ctypes.c_void_p,
        ]
        k32.ReadFile.restype = wintypes.BOOL
        k32.CloseHandle.argtypes = [wintypes.HANDLE]
        k32.CloseHandle.restype = wintypes.BOOL
        k32.GetFileAttributesW.argtypes = [ctypes.c_wchar_p]
        k32.GetFileAttributesW.restype = wintypes.DWORD
        k32.FindFirstStreamW.argtypes = [
            ctypes.c_wchar_p,
            ctypes.c_int,
            ctypes.POINTER(_FindStreamData),
            wintypes.DWORD,
        ]
        k32.FindFirstStreamW.restype = wintypes.HANDLE
        k32.FindNextStreamW.argtypes = [wintypes.HANDLE, ctypes.POINTER(_FindStreamData)]
        k32.FindNextStreamW.restype = wintypes.BOOL
        k32.FindClose.argtypes = [wintypes.HANDLE]
        k32.FindClose.restype = wintypes.BOOL
        k32.GetVolumePathNameW.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p, wintypes.DWORD]
        k32.GetVolumePathNameW.restype = wintypes.BOOL
        k32.GetVolumeInformationW.argtypes = [
            ctypes.c_wchar_p,
            ctypes.c_wchar_p,
            wintypes.DWORD,
            ctypes.POINTER(wintypes.DWORD),
            ctypes.POINTER(wintypes.DWORD),
            ctypes.POINTER(wintypes.DWORD),
            ctypes.c_wchar_p,
            wintypes.DWORD,
        ]
        k32.GetVolumeInformationW.restype = wintypes.BOOL
        k32.GetDriveTypeW.argtypes = [ctypes.c_wchar_p]
        k32.GetDriveTypeW.restype = wintypes.UINT

    @property
    def root_identity(self) -> FileIdentity:
        return self._root_identity

    def canonical_event_path(self, path: Path) -> str:
        return str(_root_bound_path(self.output_root, path))

    def path_absent(self, path: Path) -> bool:
        candidate = _extended_path(_root_bound_path(self.output_root, path))
        ctypes.set_last_error(0)
        attributes = int(self._kernel32.GetFileAttributesW(candidate))
        if attributes != _INVALID_FILE_ATTRIBUTES:
            return False
        error = ctypes.get_last_error()
        if error in {_ERROR_FILE_NOT_FOUND, _ERROR_PATH_NOT_FOUND}:
            return True
        raise record_failure("destination absence could not be authenticated")

    def inspect_file(self, path: Path) -> FileSnapshot:
        candidate = _root_bound_path(self.output_root, path)
        self._require_no_alternate_streams(candidate)
        handle = self._open(candidate, directory=False)
        try:
            before = self._information(handle)
            if before.dwFileAttributes & (_FILE_ATTRIBUTE_DIRECTORY | _FILE_ATTRIBUTE_REPARSE_POINT):
                raise record_failure("publication object is not a regular non-reparse file")
            if int(before.nNumberOfLinks) != 1:
                raise record_failure("publication object has a link alias")
            expected_size = (int(before.nFileSizeHigh) << 32) | int(before.nFileSizeLow)
            digest = hashlib.sha256()
            observed_size = 0
            while True:
                buffer = ctypes.create_string_buffer(65536)
                count = wintypes.DWORD(0)
                ok = self._kernel32.ReadFile(handle, buffer, 65536, ctypes.byref(count), None)
                if not ok:
                    raise record_failure("publication object read failed")
                if count.value == 0:
                    break
                chunk = buffer.raw[: count.value]
                digest.update(chunk)
                observed_size += len(chunk)
            after = self._information(handle)
            if (
                _identity(before) != _identity(after)
                or expected_size != observed_size
                or int(after.nNumberOfLinks) != 1
            ):
                raise record_failure("publication object changed during authenticated read")
            snapshot = FileSnapshot(_identity(after), observed_size, digest.hexdigest())
            if snapshot.identity.volume_serial_number != self.root_identity.volume_serial_number:
                raise record_failure("publication object is not on the authenticated root volume")
            return snapshot
        finally:
            self._kernel32.CloseHandle(handle)

    def move_no_replace(self, source: Path, destination: Path) -> MoveResult:
        source_text = _extended_path(_root_bound_path(self.output_root, source))
        destination_text = _extended_path(_root_bound_path(self.output_root, destination))
        return self._move.call(source_text, destination_text, 0)

    def _inspect_root_identity(self) -> FileIdentity:
        handle = self._open(self.output_root, directory=True, preflight=True)
        try:
            info = self._information(handle, preflight=True)
            if not info.dwFileAttributes & _FILE_ATTRIBUTE_DIRECTORY:
                raise auth_failure("output root is not a directory")
            if info.dwFileAttributes & _FILE_ATTRIBUTE_REPARSE_POINT:
                raise auth_failure("output root must not be a reparse point")
            return _identity(info)
        finally:
            self._kernel32.CloseHandle(handle)

    def _open(self, path: Path, *, directory: bool, preflight: bool = False) -> int:
        flags = _FILE_FLAG_OPEN_REPARSE_POINT
        access = _FILE_READ_ATTRIBUTES
        if directory:
            flags |= _FILE_FLAG_BACKUP_SEMANTICS
        else:
            flags |= _FILE_FLAG_SEQUENTIAL_SCAN
            access |= _GENERIC_READ
        handle = self._kernel32.CreateFileW(
            _extended_path(path),
            access,
            _FILE_SHARE_READ | _FILE_SHARE_WRITE | _FILE_SHARE_DELETE,
            None,
            _OPEN_EXISTING,
            flags,
            None,
        )
        if handle == _INVALID_HANDLE_VALUE:
            if preflight:
                raise auth_failure("output root could not be opened without following reparse points")
            raise record_failure("publication object could not be opened without following reparse points")
        return handle

    def _information(self, handle: int, *, preflight: bool = False) -> _ByHandleFileInformation:
        value = _ByHandleFileInformation()
        if not self._kernel32.GetFileInformationByHandle(handle, ctypes.byref(value)):
            if preflight:
                raise auth_failure("output-root file identity query failed")
            raise record_failure("file identity query failed")
        return value

    def _require_no_alternate_streams(self, path: Path, *, preflight: bool = False) -> None:
        data = _FindStreamData()
        ctypes.set_last_error(0)
        handle = self._kernel32.FindFirstStreamW(_extended_path(path), 0, ctypes.byref(data), 0)
        if handle == _INVALID_HANDLE_VALUE:
            if ctypes.get_last_error() == _ERROR_HANDLE_EOF:
                return
            failure = auth_failure if preflight else record_failure
            raise failure("alternate-stream inventory could not be authenticated")
        names: list[str] = []
        try:
            names.append(str(data.cStreamName))
            while self._kernel32.FindNextStreamW(handle, ctypes.byref(data)):
                names.append(str(data.cStreamName))
        finally:
            self._kernel32.FindClose(handle)
        if names != ["::$DATA"]:
            failure = auth_failure if preflight else record_failure
            raise failure("publication object contains an alternate data stream")

    def _volume_profile(self, path: Path) -> tuple[str, int]:
        volume_path = ctypes.create_unicode_buffer(32768)
        if not self._kernel32.GetVolumePathNameW(str(path), volume_path, len(volume_path)):
            raise auth_failure("output-root volume path could not be authenticated")
        volume_text = volume_path.value
        if volume_text.startswith("\\\\"):
            raise auth_failure("output-root volume is network-backed")
        drive_type = int(self._kernel32.GetDriveTypeW(volume_text))
        filesystem = ctypes.create_unicode_buffer(64)
        serial = wintypes.DWORD(0)
        max_component = wintypes.DWORD(0)
        flags = wintypes.DWORD(0)
        if not self._kernel32.GetVolumeInformationW(
            volume_text,
            None,
            0,
            ctypes.byref(serial),
            ctypes.byref(max_component),
            ctypes.byref(flags),
            filesystem,
            len(filesystem),
        ):
            raise auth_failure("output-root filesystem could not be authenticated")
        if serial.value != self.root_identity.volume_serial_number:
            raise auth_failure("volume serial disagrees with output-root identity")
        return filesystem.value, drive_type


_AUTHENTICATED_BACKENDS = weakref.WeakSet()


def _is_authenticated_win32_backend(value: object) -> bool:
    """Accept only an exact, successfully constructed, still-sealed backend."""

    return (
        type(value) is Win32PublicationBackend
        and value in _AUTHENTICATED_BACKENDS
        and getattr(value, "_sealed", False) is True
        and type(getattr(value, "_move", None)) is MoveFileExBinding
    )


def _require_supported_process() -> None:
    if platform.system() != "Windows" or not hasattr(sys, "getwindowsversion"):
        raise auth_failure("supported profile requires 64-bit Windows 10 or 11")
    if sys.version_info[:2] != (3, 12) or ctypes.sizeof(ctypes.c_void_p) * 8 != 64:
        raise auth_failure("supported profile requires 64-bit CPython 3.12.x")
    version = sys.getwindowsversion()
    if version.major != 10 or version.build < 10240:
        raise auth_failure("unsupported Windows version")


def _canonical_root(path: Path) -> Path:
    if not isinstance(path, Path):
        raise auth_failure("output root must be pathlib.Path")
    try:
        resolved = path.resolve(strict=True)
    except OSError as exc:
        raise auth_failure("output root does not exist") from exc
    if resolved != path.absolute() or not resolved.is_dir() or resolved.is_symlink():
        raise auth_failure("output root is not one exact canonical directory")
    if "\x00" in str(resolved):
        raise auth_failure("output root contains embedded NUL")
    return resolved


def _root_bound_path(root: Path, path: Path) -> Path:
    if not isinstance(path, Path):
        raise auth_failure("publication path must be pathlib.Path")
    absolute = path if path.is_absolute() else root / path
    try:
        absolute.parent.resolve(strict=True).relative_to(root)
    except (OSError, ValueError) as exc:
        raise auth_failure("publication path escapes the authenticated output root") from exc
    if absolute.parent.resolve(strict=True) != root or absolute.name not in {
        "run-record.pending",
        "run-record.json",
        "publication-receipt.pending",
        "publication-receipt.json",
    }:
        raise auth_failure("publication path is not one of the four exact root names")
    text = str(absolute)
    tail = text[2:] if len(text) >= 2 and text[1] == ":" else text
    if "\x00" in text or ":" in tail:
        raise auth_failure("publication path contains an alternate-stream or NUL syntax")
    return absolute


def _extended_path(path: Path) -> str:
    text = str(path)
    if text.startswith("\\\\?\\"):
        return text
    if text.startswith("\\\\"):
        return "\\\\?\\UNC\\" + text[2:]
    return "\\\\?\\" + text


def _identity(info: _ByHandleFileInformation) -> FileIdentity:
    return FileIdentity(
        int(info.dwVolumeSerialNumber),
        int(info.nFileIndexHigh),
        int(info.nFileIndexLow),
    )

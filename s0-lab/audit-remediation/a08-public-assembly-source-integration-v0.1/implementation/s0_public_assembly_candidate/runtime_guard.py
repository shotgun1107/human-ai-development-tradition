"""Fail-closed child import/capability sentinels.

This is bounded same-process evidence, not an OS sandbox or verifier authority.
"""

from __future__ import annotations

import builtins
import os
import sys
from pathlib import Path

from .errors import BoundaryViolation


_FORBIDDEN_ROOTS = frozenset(
    {
        "_cffi_backend",
        "_ctypes",
        "_winapi",
        "aiohttp",
        "anthropic",
        "asyncio",
        "boto3",
        "botocore",
        "cffi",
        "ctypes",
        "ftplib",
        "httpx",
        "multiprocessing",
        "openai",
        "paramiko",
        "requests",
        "shutil",
        "smtplib",
        "socket",
        "ssl",
        "subprocess",
        "telnetlib",
        "urllib3",
        "webbrowser",
        "win32api",
        "win32con",
        "win32event",
        "win32file",
        "win32process",
    }
)
_FORBIDDEN_NAMES = frozenset(
    {
        "google.genai",
        "google.generativeai",
        "urllib.request",
    }
)
# Windows may preload this private process primitive while constructing the
# isolated interpreter itself.  Direct imports remain denied, and candidate
# source is separately authenticated/audited; its baseline presence alone
# cannot make sentinel installation impossible.
_PRELOAD_TOLERATED = frozenset({"_winapi"})
_INSTALLED = False
_ORIGINAL_IMPORT = builtins.__import__
_WORKSPACE_ROOT: Path | None = None
_OUTPUT_ROOT: Path | None = None
_ALLOWED_PUBLIC_FILES: frozenset[Path] = frozenset()
_BUNDLE_ROOT: Path | None = None
_VIOLATED = False
_OUTPUT_NAMES = frozenset(
    {
        "run-record.pending",
        "run-record.json",
        "publication-receipt.pending",
        "publication-receipt.json",
    }
)


def _deny(message: str) -> None:
    global _VIOLATED
    _VIOLATED = True
    raise BoundaryViolation(message)


def require_runtime_sentinels_healthy() -> None:
    """Fail every substantive stage after the first denied capability."""

    if not _INSTALLED:
        _deny("child runtime sentinels are not installed")
    if _VIOLATED:
        _deny("child runtime boundary violation is latched")


def require_runtime_sentinels_healthy_if_installed() -> None:
    """Unit diagnostics may omit installation; a child installation may not recover."""

    if _INSTALLED:
        require_runtime_sentinels_healthy()


def _is_forbidden(name: str) -> bool:
    if type(name) is not str or not name:
        return True
    root = name.split(".", 1)[0]
    if root in _FORBIDDEN_ROOTS:
        return True
    if name in _FORBIDDEN_NAMES or any(
        name.startswith(prefix + ".") for prefix in _FORBIDDEN_NAMES
    ):
        return True
    return any("verifier" in part.lower() for part in name.split("."))


def _guarded_import(
    name: str,
    globals: dict[str, object] | None = None,
    locals: dict[str, object] | None = None,
    fromlist: tuple[str, ...] = (),
    level: int = 0,
) -> object:
    if _VIOLATED:
        _deny("child runtime boundary violation is latched")
    if level == 0 and _is_forbidden(name):
        _deny("child import sentinel denied a capability")
    return _ORIGINAL_IMPORT(name, globals, locals, fromlist, level)


class _ForbiddenFinder:
    def find_spec(
        self,
        fullname: str,
        path: object = None,
        target: object = None,
    ) -> None:
        del path, target
        if _VIOLATED:
            _deny("child runtime boundary violation is latched")
        if _is_forbidden(fullname):
            _deny("child import sentinel denied a capability")
        return None


def _audit(event: str, arguments: tuple[object, ...]) -> None:
    if _VIOLATED:
        if event == "os.remove" and _remove_is_exact_owned_output(arguments):
            return
        if event in {"os.listdir", "os.scandir"} and _directory_is_exact_output(
            arguments
        ):
            return
        if (
            event in {"import", "open"}
            or event.startswith("os.")
            or event.startswith("socket.")
            or event.startswith("subprocess.")
            or event.startswith("ctypes.")
        ):
            _deny("child runtime boundary violation is latched")
    if event == "open":
        _guard_file_open(arguments)
        return
    if event in {"os.listdir", "os.scandir"}:
        _guard_directory_enumeration(arguments)
        return
    if event == "os.remove":
        _guard_remove(arguments)
        return
    if event == "os.rename":
        _deny("publication moves are verifier-parent-owned")
    if event in {
        "os.add_dll_directory",
        "os.chmod",
        "os.chown",
        "os.link",
        "os.putenv",
        "os.rmdir",
        "os.startfile",
        "os.startfile/2",
        "os.symlink",
        "os.truncate",
        "os.unsetenv",
    }:
        _deny("child filesystem or environment mutation capability is denied")
    if event.startswith("socket.") or event.startswith("subprocess."):
        _deny("child network/process capability is denied")
    if event.startswith("ctypes."):
        _deny("child direct FFI capability is denied")
    if event in {"os.system", "os.exec", "os.spawn"}:
        _deny("child external-process capability is denied")


def _resolved_lexical_path(value: object) -> Path | None:
    if isinstance(value, int):
        return None
    try:
        path = Path(os.fspath(value))
    except (TypeError, ValueError):
        _deny("child file-open sentinel received a non-path value")
    if not path.is_absolute():
        path = Path.cwd() / path
    return Path(os.path.abspath(path))


def _under(root: Path, path: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _write_requested(arguments: tuple[object, ...]) -> bool:
    mode_or_flags = arguments[1] if len(arguments) > 1 else "r"
    if mode_or_flags is None:
        if len(arguments) < 3 or type(arguments[2]) is not int or arguments[2] < 0:
            _deny("child file-open sentinel received invalid flags")
        mode_or_flags = arguments[2]
    temporary_flag = getattr(os, "O_TEMPORARY", 0)
    if (
        isinstance(mode_or_flags, int) and mode_or_flags & temporary_flag
    ) or (
        len(arguments) > 2
        and type(arguments[2]) is int
        and arguments[2] & temporary_flag
    ):
        _deny("child file-open sentinel denied delete-on-close flags")
    if isinstance(mode_or_flags, int):
        return bool(mode_or_flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND))
    if type(mode_or_flags) is str:
        return any(marker in mode_or_flags for marker in "wax+")
    _deny("child file-open sentinel received an invalid mode")


def _guard_file_open(arguments: tuple[object, ...]) -> None:
    if not arguments:
        _deny("child file-open sentinel received no path")
    path = _resolved_lexical_path(arguments[0])
    if path is None:
        return
    if _WORKSPACE_ROOT is None or _OUTPUT_ROOT is None:
        _deny("child file-open sentinel is not configured")
    if _write_requested(arguments):
        if _under(_OUTPUT_ROOT, path) and path.parent == _OUTPUT_ROOT and path.name in {
            "run-record.pending",
            "publication-receipt.pending",
        }:
            return
        _deny("child file-open sentinel denied a write path")
    if path in _ALLOWED_PUBLIC_FILES:
        return
    if _under(_OUTPUT_ROOT, path) and path.parent == _OUTPUT_ROOT and path.name in {
        "run-record.pending",
        "publication-receipt.pending",
    }:
        return
    _deny("child file-open sentinel denied a read path")


def _guard_directory_enumeration(arguments: tuple[object, ...]) -> None:
    if not arguments:
        _deny("child directory sentinel received no path")
    path = _resolved_lexical_path(arguments[0])
    if path is None:
        _deny("child directory sentinel denied descriptor enumeration")
    if _BUNDLE_ROOT is not None and _under(_BUNDLE_ROOT, path):
        return
    if _OUTPUT_ROOT is not None and path == _OUTPUT_ROOT:
        return
    _deny("child directory sentinel denied a path")


def _directory_is_exact_output(arguments: tuple[object, ...]) -> bool:
    if not arguments or _OUTPUT_ROOT is None:
        return False
    try:
        path = _resolved_lexical_path(arguments[0])
    except BoundaryViolation:
        return False
    return path == _OUTPUT_ROOT


def _remove_is_exact_owned_output(arguments: tuple[object, ...]) -> bool:
    if not arguments or _OUTPUT_ROOT is None:
        return False
    try:
        path = _resolved_lexical_path(arguments[0])
    except BoundaryViolation:
        return False
    return (
        path is not None
        and path.parent == _OUTPUT_ROOT
        and path.name in _OUTPUT_NAMES
    )


def _guard_remove(arguments: tuple[object, ...]) -> None:
    if not _remove_is_exact_owned_output(arguments):
        _deny("child remove sentinel denied a non-owned output path")


def install_runtime_sentinels(
    *,
    workspace_root: Path | None = None,
    output_root: Path | None = None,
    allowed_public_files: frozenset[Path] | None = None,
    bundle_root: Path | None = None,
) -> None:
    """Install before controller/component imports and substantive actions."""

    global _INSTALLED, _WORKSPACE_ROOT, _OUTPUT_ROOT, _ALLOWED_PUBLIC_FILES, _BUNDLE_ROOT
    if workspace_root is not None or output_root is not None or allowed_public_files is not None:
        if not isinstance(workspace_root, Path) or not isinstance(output_root, Path):
            _deny("child file-open sentinel roots are unavailable")
        configured_workspace = Path(os.path.abspath(workspace_root))
        configured_output = Path(os.path.abspath(output_root))
        configured_files = frozenset(
            Path(os.path.abspath(path)) for path in (allowed_public_files or frozenset())
        )
        configured_bundle = None if bundle_root is None else Path(os.path.abspath(bundle_root))
        current = (_WORKSPACE_ROOT, _OUTPUT_ROOT, _ALLOWED_PUBLIC_FILES, _BUNDLE_ROOT)
        proposed = (configured_workspace, configured_output, configured_files, configured_bundle)
        if _WORKSPACE_ROOT is not None and current != proposed:
            _deny("child file-open sentinel cannot be rebound")
        _WORKSPACE_ROOT, _OUTPUT_ROOT, _ALLOWED_PUBLIC_FILES, _BUNDLE_ROOT = proposed
    if _INSTALLED:
        return
    if any(
        _is_forbidden(name) and name not in _PRELOAD_TOLERATED
        for name in sys.modules
    ):
        _deny("a forbidden module was loaded before child sentinels")
    builtins.__import__ = _guarded_import
    sys.meta_path.insert(0, _ForbiddenFinder())
    sys.addaudithook(_audit)
    sys.dont_write_bytecode = True
    _INSTALLED = True


def require_file_open_sentinel_configured() -> None:
    if (
        not _INSTALLED
        or _WORKSPACE_ROOT is None
        or _OUTPUT_ROOT is None
        or _BUNDLE_ROOT is None
        or not _ALLOWED_PUBLIC_FILES
    ):
        _deny("verifier bootstrap did not configure the child file-open sentinel")
    require_runtime_sentinels_healthy()

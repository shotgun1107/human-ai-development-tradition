"""Path-free error messages shared by CLI and technical verification records."""

from __future__ import annotations


def safe_exception_message(exc: Exception) -> str:
    """Return a stable message that never embeds an OS or workspace path."""

    name = type(exc).__name__
    if name in {
        "AuthenticationError",
        "IntegrityError",
        "TransformationError",
        "UnsafePathError",
    }:
        return str(exc)
    if name == "CliUsageError":
        return "invalid command arguments"
    if isinstance(exc, FileExistsError):
        return "output already exists; overwrite is forbidden"
    if isinstance(exc, FileNotFoundError):
        return "workspace-relative input does not exist"
    if isinstance(exc, PermissionError):
        return "workspace file permission denied"
    if isinstance(exc, OSError):
        return "workspace file operation failed"
    if isinstance(exc, UnicodeError):
        return "input is not valid UTF-8"
    if isinstance(exc, ValueError):
        return "input validation failed"
    return "operation failed"

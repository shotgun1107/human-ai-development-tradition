"""Stable public-runtime error types.

These exceptions intentionally carry no absolute filesystem paths and no
experimental content.
"""

from __future__ import annotations


class I1Error(ValueError):
    """Base class for deterministic public I1 validation failures."""


class UnsafePathError(I1Error):
    """A path is absolute, traversing, substituted, or reparse-backed."""


class AuthenticationError(I1Error):
    """Authenticated bytes do not match their frozen public anchor."""


class JsonBytesError(I1Error):
    """Raw bytes are not an accepted strict JSON representation."""


class TopologyError(I1Error):
    """The public role/store/edge/status topology is inconsistent."""


class CanonicalRecordError(I1Error):
    """A section-4 public record is noncanonical or inconsistent."""


class RunnerPolicyError(I1Error):
    """A provider-neutral one-shot runner invariant failed."""


class OutputError(I1Error):
    """A successful result cannot be emitted without overwrite risk."""


def safe_exception_message(exc: Exception) -> str:
    """Return a path-free, stable message for public verification output."""

    if isinstance(exc, I1Error):
        return str(exc)
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
    return "operation failed"

"""Workspace-relative path handling with an intentionally small policy."""

from __future__ import annotations

from pathlib import Path, PurePath


class UnsafePathError(ValueError):
    """Raised when a caller supplies an absolute or traversing path."""


def resolve_workspace_path(
    workspace_root: Path, value: str | Path, *, must_exist: bool = True
) -> Path:
    """Resolve a safe workspace-relative path below *workspace_root*.

    Symlinks are resolved before the containment check, so a relative symlink cannot
    be used to escape the workspace.  The API rejects ``..`` even if normalization
    would ultimately land inside the workspace.
    """

    raw = str(value)
    candidate = PurePath(raw)
    if not raw or candidate.is_absolute() or Path(raw).drive:
        raise UnsafePathError("path must be non-empty and workspace-relative")
    if ".." in candidate.parts:
        raise UnsafePathError("path traversal is not allowed")

    root = workspace_root.resolve(strict=True)
    try:
        resolved = (root / Path(raw)).resolve(strict=must_exist)
    except FileNotFoundError as exc:
        raise UnsafePathError("workspace-relative input does not exist") from exc
    except OSError as exc:
        raise UnsafePathError("workspace-relative path could not be resolved") from exc
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise UnsafePathError("path escapes the workspace") from exc
    return resolved

"""Static proof that the bounded candidate has no native or launch authority."""

from __future__ import annotations

import ast
from pathlib import Path

from .errors import RuntimeProfileError


_FORBIDDEN_IMPORTS = {
    "_ctypes",
    "ctypes",
    "multiprocessing",
    "socket",
    "subprocess",
    "win32api",
    "win32file",
    "win32process",
}
_FORBIDDEN_NAMES = {
    "CreateProcessA",
    "CreateProcessW",
    "NtCreateFile",
    "MoveFileExW",
    "WinDLL",
    "windll",
    "Popen",
}


def audit_bounded_source(root: Path) -> tuple[str, ...]:
    if not isinstance(root, Path) or not root.is_dir() or root.is_symlink():
        raise RuntimeProfileError("bounded source root is unavailable")
    sources = tuple(sorted(path for path in root.rglob("*.py") if path.is_file()))
    if not sources:
        raise RuntimeProfileError("bounded source inventory is empty")
    checked: list[str] = []
    for path in sources:
        if path.is_symlink():
            raise RuntimeProfileError("bounded source contains a symlink")
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=path.name)
        except (OSError, UnicodeDecodeError, SyntaxError) as exc:
            raise RuntimeProfileError("bounded source is not strict valid Python") from exc
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                if any(alias.name.split(".")[0] in _FORBIDDEN_IMPORTS for alias in node.names):
                    raise RuntimeProfileError("bounded source imports native/process authority")
            elif isinstance(node, ast.ImportFrom):
                if (node.module or "").split(".")[0] in _FORBIDDEN_IMPORTS:
                    raise RuntimeProfileError("bounded source imports native/process authority")
            elif isinstance(node, ast.Name) and node.id in _FORBIDDEN_NAMES:
                raise RuntimeProfileError("bounded source names native/process authority")
            elif isinstance(node, ast.Attribute) and node.attr in _FORBIDDEN_NAMES:
                raise RuntimeProfileError("bounded source references native/process authority")
        checked.append(path.name)
    return tuple(checked)


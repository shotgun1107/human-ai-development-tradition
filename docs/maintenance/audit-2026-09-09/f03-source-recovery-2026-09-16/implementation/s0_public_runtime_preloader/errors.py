"""Stable public failures for the bounded runtime/preloader candidate."""

from __future__ import annotations


class RuntimeProfileError(RuntimeError):
    """Fail-closed authentication, schema, semantic, or launch-plan error."""

    def __init__(self, label: str, *, path: str = "#") -> None:
        if type(label) is not str or not label:
            raise TypeError("error label must be nonempty exact text")
        if type(path) is not str or not path.startswith("#"):
            raise TypeError("error path must be one JSON pointer")
        super().__init__(f"{label} at {path}")
        self.label = label
        self.path = path

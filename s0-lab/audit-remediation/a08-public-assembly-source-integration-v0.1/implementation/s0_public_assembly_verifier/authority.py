"""Private, process-local run capability and one-use publication witness."""

from __future__ import annotations

import copy
import threading
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import MoveEvent


_CAPABILITY_TOKEN = object()
_WITNESS_TOKEN = object()


class _IdentityAuthority:
    __slots__ = ()

    def __copy__(self) -> object:
        raise TypeError("authority objects cannot be copied")

    def __deepcopy__(self, memo: dict[int, object]) -> object:
        raise TypeError("authority objects cannot be deep-copied")

    def __reduce__(self) -> object:
        raise TypeError("authority objects cannot be serialized")

    def __repr__(self) -> str:
        return f"<{type(self).__name__} private-process-local>"

    def __eq__(self, other: object) -> bool:
        return self is other

    __hash__ = object.__hash__


class _RunCapability(_IdentityAuthority):
    __slots__ = ("observer", "child", "pipe", "root", "terminal", "_token")

    def __init__(
        self,
        *,
        observer: object,
        child: object,
        pipe: object,
        root: Path,
        token: object,
    ) -> None:
        if token is not _CAPABILITY_TOKEN:
            raise TypeError("run capability has no public constructor")
        self.observer = observer
        self.child = child
        self.pipe = pipe
        self.root = root
        self.terminal = False
        self._token = token


class _PublicationWitness(_IdentityAuthority):
    __slots__ = (
        "observer",
        "capability",
        "child",
        "pipe",
        "root",
        "events",
        "used",
        "lock",
        "_token",
    )

    def __init__(
        self,
        *,
        observer: object,
        capability: _RunCapability,
        child: object,
        pipe: object,
        root: Path,
        events: tuple["MoveEvent", ...],
        token: object,
    ) -> None:
        if token is not _WITNESS_TOKEN:
            raise TypeError("publication witness has no public constructor")
        self.observer = observer
        self.capability = capability
        self.child = child
        self.pipe = pipe
        self.root = root
        self.events = events
        self.used = False
        self.lock = threading.Lock()
        self._token = token


def _issue_capability(*, observer: object, child: object, pipe: object, root: Path) -> _RunCapability:
    return _RunCapability(observer=observer, child=child, pipe=pipe, root=root, token=_CAPABILITY_TOKEN)


def _issue_witness(
    *,
    observer: object,
    capability: _RunCapability,
    events: tuple["MoveEvent", ...],
) -> _PublicationWitness:
    if capability.terminal:
        raise RuntimeError("terminal capability cannot issue another witness")
    capability.terminal = True
    return _PublicationWitness(
        observer=observer,
        capability=capability,
        child=capability.child,
        pipe=capability.pipe,
        root=capability.root,
        events=events,
        token=_WITNESS_TOKEN,
    )


def _is_capability(value: object) -> bool:
    return type(value) is _RunCapability and getattr(value, "_token", None) is _CAPABILITY_TOKEN


def _is_witness(value: object) -> bool:
    return type(value) is _PublicationWitness and getattr(value, "_token", None) is _WITNESS_TOKEN


def _authority_copy_negative_matrix(value: object) -> tuple[bool, bool]:
    """Test helper: both copy paths must reject without exposing construction."""

    shallow_rejected = deep_rejected = False
    try:
        copy.copy(value)
    except TypeError:
        shallow_rejected = True
    try:
        copy.deepcopy(value)
    except TypeError:
        deep_rejected = True
    return shallow_rejected, deep_rejected

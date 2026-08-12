"""Named fail-closed entry points for capabilities outside public I3."""

from __future__ import annotations

from typing import NoReturn

from .errors import I3UnsupportedBoundaryError


def _blocked(name: str) -> NoReturn:
    raise I3UnsupportedBoundaryError(f"BLOCKED_NOT_EXECUTED: {name}")


def validate_durable_ledger(*_args: object, **_kwargs: object) -> NoReturn:
    _blocked("durable-ledger")


def validate_witness(*_args: object, **_kwargs: object) -> NoReturn:
    _blocked("witness-validation")


def enforce_platform_isolation(*_args: object, **_kwargs: object) -> NoReturn:
    _blocked("provider-or-platform-enforcement")


def run_s0(*_args: object, **_kwargs: object) -> NoReturn:
    _blocked("e0-or-s0-execution")

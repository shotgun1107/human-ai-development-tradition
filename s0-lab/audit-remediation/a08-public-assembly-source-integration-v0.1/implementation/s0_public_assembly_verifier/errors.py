"""Stable verifier-side failure classes."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AssemblyFailure(Exception):
    failure_class: str
    observed_transport_calls: int
    diagnostic: str

    def __post_init__(self) -> None:
        if self.failure_class not in {
            "AR-BOUNDARY",
            "AR-AUTH",
            "AR-TRANSFORM",
            "AR-RESERVE",
            "AR-INVOKE",
            "AR-RESPONSE",
            "AR-ANSWER",
            "AR-RECORD",
            "AR-DETERMINISM",
        }:
            raise ValueError("unknown assembly failure class")
        if type(self.observed_transport_calls) is not int or self.observed_transport_calls not in {0, 1}:
            raise ValueError("observed transport calls must be exact zero or one")

    def __str__(self) -> str:
        return f"{self.failure_class}/{self.observed_transport_calls}: {self.diagnostic}"


def auth_failure(diagnostic: str) -> AssemblyFailure:
    return AssemblyFailure("AR-AUTH", 0, diagnostic)


def record_failure(diagnostic: str) -> AssemblyFailure:
    return AssemblyFailure("AR-RECORD", 1, diagnostic)

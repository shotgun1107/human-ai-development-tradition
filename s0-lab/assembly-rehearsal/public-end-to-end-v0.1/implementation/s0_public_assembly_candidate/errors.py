"""Stable failure classes and diagnostic-only failure records."""

from __future__ import annotations

from dataclasses import asdict, dataclass


AR_BOUNDARY = "AR-BOUNDARY"
AR_AUTH = "AR-AUTH"
AR_TRANSFORM = "AR-TRANSFORM"
AR_RESERVE = "AR-RESERVE"
AR_INVOKE = "AR-INVOKE"
AR_RESPONSE = "AR-RESPONSE"
AR_ANSWER = "AR-ANSWER"
AR_DETERMINISM = "AR-DETERMINISM"
AR_RECORD = "AR-RECORD"

FAILURE_CLASSES = frozenset(
    {
        AR_BOUNDARY,
        AR_AUTH,
        AR_TRANSFORM,
        AR_RESERVE,
        AR_INVOKE,
        AR_RESPONSE,
        AR_ANSWER,
        AR_DETERMINISM,
        AR_RECORD,
    }
)


class BoundaryViolation(RuntimeError):
    """A denied path, capability, or operation was attempted."""


class StageFailure(RuntimeError):
    """One ordered controller operation failed."""

    def __init__(self, failure_class: str, operation: str, cause_label: str) -> None:
        if failure_class not in FAILURE_CLASSES:
            raise ValueError("unknown assembly failure class")
        super().__init__(f"{failure_class}: {operation}: {cause_label}")
        self.failure_class = failure_class
        self.operation = operation
        self.cause_label = cause_label


@dataclass(frozen=True)
class FailureDiagnostic:
    """Out-of-band diagnostic; never a success record or PASS authority."""

    schema_id: str
    primary_class: str
    observed_transport_calls: int
    failed_operation: str
    cause_label: str
    state_at_failure: str
    cleanup_status: str
    output_root_status: str
    offline_status: str
    rehearsal_pass: bool

    @classmethod
    def create(
        cls,
        *,
        primary_class: str,
        observed_transport_calls: int,
        failed_operation: str,
        cause_label: str,
        state_at_failure: str,
        cleanup_status: str,
        output_root_status: str,
    ) -> "FailureDiagnostic":
        return cls(
            schema_id="S0-PUBLIC-ASSEMBLY-FAILURE-DIAGNOSTIC-1",
            primary_class=primary_class,
            observed_transport_calls=observed_transport_calls,
            failed_operation=failed_operation,
            cause_label=cause_label,
            state_at_failure=state_at_failure,
            cleanup_status=cleanup_status,
            output_root_status=output_root_status,
            offline_status="offline-not-success-diagnostic-only",
            rehearsal_pass=False,
        )

    @property
    def label(self) -> str:
        return f"{self.primary_class}/{self.observed_transport_calls}"

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class AssemblyRunFailed(RuntimeError):
    def __init__(self, diagnostic: FailureDiagnostic) -> None:
        super().__init__(diagnostic.label)
        self.diagnostic = diagnostic


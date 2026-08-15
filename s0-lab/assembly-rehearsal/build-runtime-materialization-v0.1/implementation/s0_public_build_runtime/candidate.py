"""Bounded PUBLIC candidate that stops before external pins or execution."""

from __future__ import annotations

from dataclasses import dataclass

from .authority import DesignClosure, authenticate_design_closure
from .canonical import jcs_lf, sha256_hex
from .errors import BuildRuntimeError
from .semantics import validate_effective_design

_BLOCKED_TRACE = (
    "CANDIDATE-NEW",
    "PUBLIC-DESIGN-AUTHENTICATED",
    "V0.5-SEMANTICS-VALIDATED",
    "BLOCKED-MISSING-EXTERNAL-PIN",
)
_REJECTED_TRACE = ("CANDIDATE-NEW", "CANDIDATE-REJECTED")


@dataclass(frozen=True)
class BuildRuntimeDiagnostic:
    raw: bytes
    sha256: str
    state_trace: tuple[str, ...]
    terminal_state: str
    primary_failure: str | None
    relation_sha256: str | None
    policy_sha256: str | None
    mutation_row_count: int
    external_pin_status: str
    candidate_only: bool = True
    build_execution_authorized: bool = False
    runtime_materialized: bool = False
    native_api_reachable: bool = False
    rehearsal_pass: bool = False
    s0_executed: bool = False

    def __post_init__(self) -> None:
        if type(self.raw) is not bytes or sha256_hex(self.raw) != self.sha256:
            raise ValueError("candidate diagnostic is not byte-bound")
        if self.state_trace not in {_BLOCKED_TRACE, _REJECTED_TRACE}:
            raise ValueError("candidate diagnostic trace differs")
        if self.terminal_state != self.state_trace[-1]:
            raise ValueError("candidate diagnostic terminal state differs")
        if any(
            value is not False
            for value in (
                self.build_execution_authorized,
                self.runtime_materialized,
                self.native_api_reachable,
                self.rehearsal_pass,
                self.s0_executed,
            )
        ) or self.candidate_only is not True:
            raise ValueError("candidate diagnostic carries forbidden authority")


def _diagnostic(
    *,
    trace: tuple[str, ...],
    failure: str | None,
    relation_sha256: str | None,
    policy_sha256: str | None,
    matrix_count: int,
    external_pin_status: str,
) -> BuildRuntimeDiagnostic:
    value = {
        "build_execution_authorized": False,
        "candidate_only": True,
        "external_pin_status": external_pin_status,
        "mutation_row_count": matrix_count,
        "native_api_reachable": False,
        "policy_sha256": policy_sha256,
        "primary_failure": failure,
        "rehearsal_pass": False,
        "relation_sha256": relation_sha256,
        "runtime_materialized": False,
        "s0_executed": False,
        "schema_id": "S0-PUBLIC-ASSEMBLY-BUILD-RUNTIME-CANDIDATE-DIAGNOSTIC-1",
        "state_trace": list(trace),
        "terminal_state": trace[-1],
    }
    raw = jcs_lf(value)
    return BuildRuntimeDiagnostic(
        raw,
        sha256_hex(raw),
        trace,
        trace[-1],
        failure,
        relation_sha256,
        policy_sha256,
        matrix_count,
        external_pin_status,
    )


def prepare_public_build_runtime_candidate(closure: DesignClosure) -> BuildRuntimeDiagnostic:
    """Authenticate design bytes, reconstruct v0.5, then fail closed on absent pins.

    This function has no filesystem, process, native, network, provider, model,
    or build surface. The ten external pin classes are deliberately not
    accepted as caller-selected arguments by this candidate version.
    """

    try:
        authority = authenticate_design_closure(closure)
        effective = validate_effective_design(authority)
    except (BuildRuntimeError, UnicodeError, TypeError, KeyError, IndexError):
        return _diagnostic(
            trace=_REJECTED_TRACE,
            failure="BR-AUTH/0",
            relation_sha256=None,
            policy_sha256=None,
            matrix_count=0,
            external_pin_status="REJECTED",
        )
    return _diagnostic(
        trace=_BLOCKED_TRACE,
        failure=None,
        relation_sha256=effective.relations_sha256,
        policy_sha256=effective.publication_policy_sha256,
        matrix_count=len(effective.mutation_rows),
        external_pin_status="BLOCKED-MISSING-EXTERNAL-PIN",
    )

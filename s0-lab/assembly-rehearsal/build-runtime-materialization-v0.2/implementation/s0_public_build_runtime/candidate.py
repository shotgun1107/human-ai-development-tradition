"""Bounded PUBLIC candidate that stops before external pins or execution."""

from __future__ import annotations

from dataclasses import dataclass

from .authority import DesignClosure, authenticate_design_closure
from .canonical import jcs_lf, require_sha256, sha256_hex, strict_json
from .errors import BuildRuntimeError
from .semantics import validate_effective_design

_BLOCKED_TRACE = (
    "CANDIDATE-NEW",
    "PUBLIC-DESIGN-AUTHENTICATED",
    "V0.5-SEMANTICS-VALIDATED",
    "BLOCKED-MISSING-EXTERNAL-PIN",
)
_REJECTED_TRACE = ("CANDIDATE-NEW", "CANDIDATE-REJECTED")
_RELATION_SHA256 = "5af2b472f4abf96c446ae56fa90f02d54fa87cdebe4e6129fcc4c3c1de1610db"
_POLICY_SHA256 = "3fd2df85e665c2a7b968d1c75f5c4ef2f85eb16e19682f718be4d3675b4a654b"


_DIAGNOSTIC_KEYS = {
    "build_execution_authorized",
    "candidate_only",
    "external_pin_status",
    "mutation_row_count",
    "native_api_reachable",
    "policy_sha256",
    "primary_failure",
    "rehearsal_pass",
    "relation_sha256",
    "runtime_materialized",
    "s0_executed",
    "schema_id",
    "state_trace",
    "terminal_state",
}


@dataclass(frozen=True, slots=True)
class BuildRuntimeDiagnostic:
    raw: bytes
    sha256: str

    def __post_init__(self) -> None:
        require_sha256(self.sha256)
        if type(self.raw) is not bytes or sha256_hex(self.raw) != self.sha256:
            raise ValueError("candidate diagnostic is not byte-bound")
        value = strict_json(self.raw)
        if type(value) is not dict or set(value) != _DIAGNOSTIC_KEYS or jcs_lf(value) != self.raw:
            raise ValueError("candidate diagnostic canonical record differs")
        trace_raw = value.get("state_trace")
        if type(trace_raw) is not list or any(type(item) is not str for item in trace_raw):
            raise ValueError("candidate diagnostic trace type differs")
        trace = tuple(trace_raw)
        if trace not in {_BLOCKED_TRACE, _REJECTED_TRACE}:
            raise ValueError("candidate diagnostic trace differs")
        if value.get("terminal_state") != trace[-1]:
            raise ValueError("candidate diagnostic terminal state differs")
        if any(
            flag is not False
            for flag in (
                value.get("build_execution_authorized"),
                value.get("runtime_materialized"),
                value.get("native_api_reachable"),
                value.get("rehearsal_pass"),
                value.get("s0_executed"),
            )
        ) or value.get("candidate_only") is not True:
            raise ValueError("candidate diagnostic carries forbidden authority")
        if value.get("schema_id") != "S0-PUBLIC-ASSEMBLY-BUILD-RUNTIME-CANDIDATE-DIAGNOSTIC-2":
            raise ValueError("candidate diagnostic schema differs")
        if trace == _BLOCKED_TRACE:
            for digest_name in ("relation_sha256", "policy_sha256"):
                require_sha256(value.get(digest_name))
            if (
                value.get("primary_failure") is not None
                or value.get("relation_sha256") != _RELATION_SHA256
                or value.get("policy_sha256") != _POLICY_SHA256
                or value.get("mutation_row_count") != 115
                or value.get("external_pin_status") != "BLOCKED-MISSING-EXTERNAL-PIN"
            ):
                raise ValueError("blocked diagnostic fields differ")
        elif (
            value.get("primary_failure") != "BR-AUTH/0"
            or value.get("relation_sha256") is not None
            or value.get("policy_sha256") is not None
            or value.get("mutation_row_count") != 0
            or value.get("external_pin_status") != "REJECTED"
        ):
            raise ValueError("rejected diagnostic fields differ")

    def _value(self, name: str) -> object:
        value = strict_json(self.raw)
        if type(value) is not dict:
            raise ValueError("candidate diagnostic root differs")
        return value[name]

    @property
    def state_trace(self) -> tuple[str, ...]:
        return tuple(self._value("state_trace"))

    @property
    def terminal_state(self) -> str:
        return self._value("terminal_state")

    @property
    def primary_failure(self) -> str | None:
        return self._value("primary_failure")

    @property
    def relation_sha256(self) -> str | None:
        return self._value("relation_sha256")

    @property
    def policy_sha256(self) -> str | None:
        return self._value("policy_sha256")

    @property
    def mutation_row_count(self) -> int:
        return self._value("mutation_row_count")

    @property
    def external_pin_status(self) -> str:
        return self._value("external_pin_status")

    @property
    def candidate_only(self) -> bool:
        return self._value("candidate_only")

    @property
    def build_execution_authorized(self) -> bool:
        return self._value("build_execution_authorized")

    @property
    def runtime_materialized(self) -> bool:
        return self._value("runtime_materialized")

    @property
    def native_api_reachable(self) -> bool:
        return self._value("native_api_reachable")

    @property
    def rehearsal_pass(self) -> bool:
        return self._value("rehearsal_pass")

    @property
    def s0_executed(self) -> bool:
        return self._value("s0_executed")


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
        "schema_id": "S0-PUBLIC-ASSEMBLY-BUILD-RUNTIME-CANDIDATE-DIAGNOSTIC-2",
        "state_trace": list(trace),
        "terminal_state": trace[-1],
    }
    raw = jcs_lf(value)
    return BuildRuntimeDiagnostic(raw, sha256_hex(raw))


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

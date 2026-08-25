"""Immutable byte-bound results for the bounded v0.3 verifier."""

from __future__ import annotations

from dataclasses import dataclass

from .canonical import VerificationError, require_sha256, sha256_hex
from .contract import RUNTIME_AUTHORITY_SCOPE, SUPPLIER_CRITERION_ID


@dataclass(frozen=True)
class VerificationAuthority:
    implementation_manifest_sha256: str
    policy_manifest_sha256: str
    acquisition_validator_manifest_sha256: str
    native_verifier_manifest_sha256: str
    semantic_validator_manifest_sha256: str
    acquisition_record_sha256: str
    acquisition_authority_manifest_sha256: str
    supplier_criterion_id: str = SUPPLIER_CRITERION_ID
    runtime_authority_scope: str = RUNTIME_AUTHORITY_SCOPE
    executed_code_authority_established: bool = False

    def __post_init__(self) -> None:
        require_sha256(self.implementation_manifest_sha256, name="outer implementation manifest")
        require_sha256(self.policy_manifest_sha256, name="policy manifest")
        require_sha256(
            self.acquisition_validator_manifest_sha256,
            name="acquisition validator manifest",
        )
        require_sha256(self.native_verifier_manifest_sha256, name="native verifier manifest")
        require_sha256(self.semantic_validator_manifest_sha256, name="semantic validator manifest")
        require_sha256(self.acquisition_record_sha256, name="acquisition record")
        require_sha256(
            self.acquisition_authority_manifest_sha256,
            name="acquisition authority manifest",
        )
        if self.supplier_criterion_id != SUPPLIER_CRITERION_ID:
            raise VerificationError("supplier criterion authority differs")
        if self.runtime_authority_scope != RUNTIME_AUTHORITY_SCOPE:
            raise VerificationError("runtime authority scope differs")
        if self.executed_code_authority_established is not False:
            raise VerificationError("this implementation does not establish executed-code authority")


@dataclass(frozen=True)
class VerificationResult:
    observation_sha256: str
    trace_raw: bytes
    trace_sha256: str
    decision_raw: bytes
    decision_sha256: str
    trust_policy_pass: bool
    failure_relations: tuple[str, ...]
    runtime_authority_scope: str = RUNTIME_AUTHORITY_SCOPE
    executed_code_authority_established: bool = False
    process_authority_granted: bool = False

    def __post_init__(self) -> None:
        require_sha256(self.observation_sha256, name="observation")
        if type(self.trace_raw) is not bytes or sha256_hex(self.trace_raw) != self.trace_sha256:
            raise VerificationError("semantic trace is not byte-bound")
        if type(self.decision_raw) is not bytes or sha256_hex(self.decision_raw) != self.decision_sha256:
            raise VerificationError("decision is not byte-bound")
        if type(self.trust_policy_pass) is not bool:
            raise VerificationError("trust-policy result is not exact Boolean")
        if type(self.failure_relations) is not tuple or any(
            type(item) is not str for item in self.failure_relations
        ):
            raise VerificationError("failure relation inventory differs")
        if self.runtime_authority_scope != RUNTIME_AUTHORITY_SCOPE:
            raise VerificationError("runtime authority scope differs")
        if self.executed_code_authority_established is not False:
            raise VerificationError("executed-code authority cannot be granted here")
        if self.process_authority_granted is not False:
            raise VerificationError("this gate cannot grant process authority")

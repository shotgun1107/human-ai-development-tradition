"""Fail-closed candidate decision for external-pin recovery v0.2."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from typing import Final


CANDIDATE_ID: Final = "build-runtime-materialization-external-pin-recovery-v0.2"


@dataclass(frozen=True, order=True, slots=True)
class CandidateBlocker:
    blocker_id: str
    description: str


ORIGINAL_BLOCKERS: Final = (
    CandidateBlocker("IR-001", "independent trust review item IR-001 remains unresolved"),
    CandidateBlocker("IR-002", "independent trust review item IR-002 remains unresolved"),
    CandidateBlocker("IR-003", "independent trust review item IR-003 remains unresolved"),
    CandidateBlocker("SUPPLIER-ASSURANCE", "supplier assurance evidence is absent"),
    CandidateBlocker(
        "EFFECTIVE-TRUST-SNAPSHOT",
        "an authenticated effective-trust snapshot is absent",
    ),
    CandidateBlocker(
        "ACQUISITION-PRODUCER",
        "an authenticated acquisition producer is absent",
    ),
    CandidateBlocker(
        "SEMANTIC-VALIDATOR",
        "an independent semantic validator is absent",
    ),
    CandidateBlocker(
        "FRESHNESS-PROVENANCE",
        "authenticated freshness provenance is absent",
    ),
    CandidateBlocker(
        "JSONSCHEMA-TRANSITIVE-CLOSURE",
        "the complete jsonschema transitive dependency closure is absent",
    ),
    CandidateBlocker("NATIVE-SOURCE", "authenticated native-component source is absent"),
    CandidateBlocker(
        "MATERIALIZER-SOURCE",
        "authenticated materializer source provenance is absent",
    ),
    CandidateBlocker(
        "OFFLINE-TOOLCHAIN-LAYOUT",
        "a verified offline toolchain layout is absent",
    ),
    CandidateBlocker("RUNTIME-PROFILE", "a verified runtime profile is absent"),
)

REVIEW_FINDING_BLOCKERS: Final = (
    CandidateBlocker(
        "BRM-EPRI01-IR-001",
        "handle-bound no-reparse creation and parent-swap evidence is absent",
    ),
    CandidateBlocker(
        "BRM-EPRI01-IR-002",
        "stable archive/output identity and final reauthentication evidence is absent",
    ),
    CandidateBlocker(
        "BRM-EPRI01-IR-003",
        "closed immutable pin-authority verification evidence is absent",
    ),
    CandidateBlocker(
        "BRM-EPRI01-IR-004",
        "exact test and complete-manifest verifier binding evidence is absent",
    ),
)

REQUIRED_BLOCKERS: Final = ORIGINAL_BLOCKERS + REVIEW_FINDING_BLOCKERS


@dataclass(frozen=True, slots=True)
class CandidateDecision:
    """Immutable decision whose claims cannot be enabled by caller input."""

    candidate_id: str = field(default=CANDIDATE_ID, init=False)
    blockers: tuple[CandidateBlocker, ...] = field(default=REQUIRED_BLOCKERS, init=False)
    eligible: bool = field(default=False, init=False)
    process_executed: bool = field(default=False, init=False)
    process_authority_granted: bool = field(default=False, init=False)
    installation_claimed: bool = field(default=False, init=False)
    install_validated: bool = field(default=False, init=False)
    build_claimed: bool = field(default=False, init=False)
    build_validated: bool = field(default=False, init=False)
    runtime_claimed: bool = field(default=False, init=False)
    runtime_validated: bool = field(default=False, init=False)
    rehearsal_claimed: bool = field(default=False, init=False)
    rehearsal_validated: bool = field(default=False, init=False)
    s0_claimed: bool = field(default=False, init=False)
    s0_validated: bool = field(default=False, init=False)
    e0_claimed: bool = field(default=False, init=False)
    e0_validated: bool = field(default=False, init=False)
    self_assertions_considered_evidence: bool = field(default=False, init=False)

    @property
    def blocker_ids(self) -> tuple[str, ...]:
        return tuple(blocker.blocker_id for blocker in self.blockers)

    @property
    def blocked(self) -> bool:
        return True


def evaluate_candidate(
    self_assertions: Mapping[str, object] | None = None,
    **additional_self_assertions: object,
) -> CandidateDecision:
    """Return the fixed blocked decision without evaluating caller assertions.

    Only a future authority-bound external-evidence mechanism may revise these
    blockers.  Caller-authored claims, waivers, and truthy flags are ignored.
    """

    del self_assertions, additional_self_assertions
    return CandidateDecision()

"""Immutable fact aggregation and explicit candidate nonclaims."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Final, Mapping

from .buildtools import (
    _BUILD_TOOLS_TRANSITIVE_CLOSURE_BLOCKER,
    BuildToolsPinProposal,
)
from .canonical import canonical_json_lf, sha256_hex
from .errors import AuthorityError
from .metadata import (
    CPythonSourceEvidence,
    MicrosoftReleaseEvidence,
    _consume_issued_metadata_evidence,
    _release_issued_metadata_evidence,
)
from .wheel import (
    JsonschemaClosureEvidence,
    _consume_issued_jsonschema_closure,
    _release_issued_jsonschema_closure,
)


INITIAL_BLOCKERS: Final = (
    "CPYTHON-SIGSTORE-CRYPTOGRAPHIC-VERIFICATION-UNAVAILABLE",
    _BUILD_TOOLS_TRANSITIVE_CLOSURE_BLOCKER,
    "BUILD-TOOLS-AUTHENTICODE-LIVE-RESULT-PENDING",
    "BUILD-TOOLS-PROPOSED-PIN-NOT-CONTROL-PROMOTED",
    "HOST-RUNTIME-AUTHORITY-UNVERIFIED",
    "NETWORK-PRODUCER-AUTHORITY-UNVERIFIED",
    "ACQUISITION-PRODUCER",
    "EFFECTIVE-TRUST-SNAPSHOT",
    "SUPPLIER-ASSURANCE",
    "OFFLINE-TOOLCHAIN-LAYOUT",
    "RUNTIME-PROFILE",
)

NONCLAIM_NAMES: Final = (
    "acquired_or_downloaded_byte_executed",
    "acquired_or_downloaded_byte_imported",
    "acquired_or_downloaded_byte_installed",
    "acquired_or_downloaded_byte_compiled",
    "acquired_or_downloaded_byte_linked",
    "process_authority",
    "active_buildtools_authority",
    "sigstore_cryptographically_verified",
    "host_runtime_authenticated",
    "network_authenticated",
    "producer_authenticated",
    "installation_complete",
    "offline_toolchain_layout_complete",
    "build_complete",
    "runtime_complete",
    "rehearsal_complete",
    "s0_complete",
    "e0_complete",
    "central_system_complete",
    "project_brain_integrated",
    "operational_safety_validated",
    "economic_value_validated",
    "model_to_model_transfer_validated",
)


@dataclass(frozen=True, slots=True)
class CandidateState:
    candidate_id: str
    cpython_source_facts_sha256: str
    microsoft_source_sha256: str
    jsonschema_closure_sha256: str
    buildtools_proposal_sha256: str | None
    buildtools_acquired_path: str | None
    buildtools_verifier_full_path: str | None
    blockers: tuple[str, ...]
    nonclaims: tuple[tuple[str, bool], ...]
    acquired_or_downloaded_byte_executed: bool = False
    imported: bool = False
    installed: bool = False
    compiled: bool = False
    linked: bool = False
    process_authority: bool = False
    active_buildtools_authority: bool = False
    offline_toolchain_layout: bool = False
    build: bool = False
    runtime: bool = False
    rehearsal: bool = False
    s0: bool = False
    e0: bool = False
    central_system: bool = False
    project_brain_integration: bool = False
    operational_safety: bool = False
    economic_value: bool = False
    model_to_model_transfer: bool = False

    def to_mapping(self) -> Mapping[str, object]:
        return {
            "active_buildtools_authority": self.active_buildtools_authority,
            "acquired_or_downloaded_byte_executed": (
                self.acquired_or_downloaded_byte_executed
            ),
            "blockers": list(self.blockers),
            "build": self.build,
            "buildtools_proposal_sha256": self.buildtools_proposal_sha256,
            "buildtools_acquired_path": self.buildtools_acquired_path,
            "buildtools_verifier_full_path": self.buildtools_verifier_full_path,
            "candidate_id": self.candidate_id,
            "central_system": self.central_system,
            "compiled": self.compiled,
            "cpython_source_facts_sha256": self.cpython_source_facts_sha256,
            "e0": self.e0,
            "economic_value": self.economic_value,
            "imported": self.imported,
            "installed": self.installed,
            "jsonschema_closure_sha256": self.jsonschema_closure_sha256,
            "linked": self.linked,
            "microsoft_source_sha256": self.microsoft_source_sha256,
            "model_to_model_transfer": self.model_to_model_transfer,
            "nonclaims": {name: value for name, value in self.nonclaims},
            "offline_toolchain_layout": self.offline_toolchain_layout,
            "operational_safety": self.operational_safety,
            "process_authority": self.process_authority,
            "project_brain_integration": self.project_brain_integration,
            "rehearsal": self.rehearsal,
            "runtime": self.runtime,
            "s0": self.s0,
        }

    def canonical_bytes(self) -> bytes:
        return canonical_json_lf(dict(self.to_mapping()))

    def evidence_sha256(self) -> str:
        return sha256_hex(self.canonical_bytes())


def _cpython_facts_raw(cpython: CPythonSourceEvidence, *, canonical_encoder) -> bytes:
    return canonical_encoder(
        {
            "artifact_sha256": cpython.artifact_sha256,
            "artifact_size": cpython.artifact_size,
            "bundle_sha256": cpython.bundle_sha256,
            "bundle_size": cpython.bundle_size,
            "certificate_chain_verification": cpython.certificate_chain_verification,
            "certificate_der_sha256": cpython.certificate_der_sha256,
            "certificate_der_size": cpython.certificate_der_size,
            "expected_identity": cpython.expected_identity,
            "expected_oidc_issuer": cpython.expected_oidc_issuer,
            "ftp_index_sha256": cpython.ftp_index_sha256,
            "ftp_index_size": cpython.ftp_index_size,
            "release_page_sha256": cpython.release_page_sha256,
            "release_page_size": cpython.release_page_size,
            "release_page_representation": cpython.release_page_representation,
            "release_page_content_encoding": cpython.release_page_content_encoding,
            "release_page_decoded_entity_sha256": (
                cpython.release_page_decoded_entity_sha256
            ),
            "release_page_decoded_entity_size": (
                cpython.release_page_decoded_entity_size
            ),
            "release_page_decoder_authority_established": (
                cpython.release_page_decoder_authority_established
            ),
            "signature_size": cpython.signature_size,
            "signature_verification": cpython.signature_verification,
            "sigstore_cryptographic_verification": (
                cpython.sigstore_cryptographic_verification
            ),
            "tlog_entry_count": cpython.tlog_entry_count,
            "transparency_log_verification": cpython.transparency_log_verification,
        }
    )


def _closure_facts_raw(
    closure: JsonschemaClosureEvidence,
    *,
    canonical_encoder,
) -> bytes:
    return canonical_encoder(
        {
            "dependency_graph": [
                {"dependencies": list(dependencies), "pin_id": pin_id}
                for pin_id, dependencies in closure.dependency_graph
            ],
            "extras_selected": closure.extras_selected,
            "imported": closure.imported,
            "installed": closure.installed,
            "metadata_aggregate_size": closure.metadata_aggregate_size,
            "pypi_json_requires_dist_inventory": [
                {"pin_id": pin_id, "requires_dist": list(requires_dist)}
                for pin_id, requires_dist in (
                    closure.pypi_json_requires_dist_inventory
                )
            ],
            "runtime_authority": closure.runtime_authority,
            "wheel_metadata_requires_dist_inventory": [
                {"pin_id": pin_id, "requires_dist": list(requires_dist)}
                for pin_id, requires_dist in (
                    closure.wheel_metadata_requires_dist_inventory
                )
            ],
            "wheel_aggregate_size": closure.wheel_aggregate_size,
            "wheel_pin_ids": list(closure.wheel_pin_ids),
        }
    )


def _assemble_candidate_state_impl(
    *,
    cpython: CPythonSourceEvidence,
    microsoft: MicrosoftReleaseEvidence,
    jsonschema_closure: JsonschemaClosureEvidence,
    buildtools_proposal: BuildToolsPinProposal | None = None,
    consume_metadata_evidence,
    consume_closure_evidence,
    error_type,
    canonical_encoder,
    hash_bytes,
    cpython_facts_encoder,
    closure_facts_encoder,
    buildtools_blocker,
    initial_blockers,
    nonclaim_names,
    state_type,
) -> CandidateState:
    """Aggregate authenticated facts without promoting any evidence to authority."""

    cpython = consume_metadata_evidence(cpython, "cpython")
    microsoft = consume_metadata_evidence(microsoft, "microsoft")
    jsonschema_closure = consume_closure_evidence(jsonschema_closure)
    if (
        cpython.release_page_decoder_authority_established is not False
        or cpython.sigstore_cryptographic_verification is not False
        or cpython.certificate_chain_verification is not False
        or cpython.transparency_log_verification is not False
        or cpython.signature_verification is not False
    ):
        raise error_type("candidate_sigstore_cryptographic_claim_forbidden")
    if (
        jsonschema_closure.extras_selected is not False
        or jsonschema_closure.imported is not False
        or jsonschema_closure.installed is not False
        or jsonschema_closure.runtime_authority is not False
    ):
        raise error_type("candidate_jsonschema_downstream_claim_forbidden")
    blockers = initial_blockers
    proposal_sha: str | None = None
    proposal_acquired_path: str | None = None
    proposal_verifier_full_path: str | None = None
    if buildtools_proposal is not None:
        raise error_type(buildtools_blocker)
    return state_type(
        candidate_id="build-runtime-materialization-external-artifact-authority-acquisition-v0.1",
        cpython_source_facts_sha256=hash_bytes(
            cpython_facts_encoder(cpython, canonical_encoder=canonical_encoder)
        ),
        microsoft_source_sha256=microsoft.raw_sha256,
        jsonschema_closure_sha256=hash_bytes(
            closure_facts_encoder(
                jsonschema_closure,
                canonical_encoder=canonical_encoder,
            )
        ),
        buildtools_proposal_sha256=proposal_sha,
        buildtools_acquired_path=proposal_acquired_path,
        buildtools_verifier_full_path=proposal_verifier_full_path,
        blockers=blockers,
        nonclaims=tuple((name, False) for name in nonclaim_names),
    )


def _freeze_candidate_assembler():
    implementation = _assemble_candidate_state_impl
    frozen_consume_metadata = _consume_issued_metadata_evidence
    frozen_release_metadata = _release_issued_metadata_evidence
    frozen_consume_closure = _consume_issued_jsonschema_closure
    frozen_release_closure = _release_issued_jsonschema_closure
    frozen_error_type = AuthorityError
    frozen_canonical_encoder = canonical_json_lf
    frozen_hash_bytes = sha256_hex
    frozen_cpython_facts_encoder = _cpython_facts_raw
    frozen_closure_facts_encoder = _closure_facts_raw
    frozen_buildtools_blocker = _BUILD_TOOLS_TRANSITIVE_CLOSURE_BLOCKER
    frozen_initial_blockers = INITIAL_BLOCKERS
    frozen_nonclaim_names = NONCLAIM_NAMES
    frozen_state_type = CandidateState

    def assemble_candidate_state(
        *,
        cpython: CPythonSourceEvidence,
        microsoft: MicrosoftReleaseEvidence,
        jsonschema_closure: JsonschemaClosureEvidence,
        buildtools_proposal: BuildToolsPinProposal | None = None,
    ) -> CandidateState:
        try:
            return implementation(
                cpython=cpython,
                microsoft=microsoft,
                jsonschema_closure=jsonschema_closure,
                buildtools_proposal=buildtools_proposal,
                consume_metadata_evidence=frozen_consume_metadata,
                consume_closure_evidence=frozen_consume_closure,
                error_type=frozen_error_type,
                canonical_encoder=frozen_canonical_encoder,
                hash_bytes=frozen_hash_bytes,
                cpython_facts_encoder=frozen_cpython_facts_encoder,
                closure_facts_encoder=frozen_closure_facts_encoder,
                buildtools_blocker=frozen_buildtools_blocker,
                initial_blockers=frozen_initial_blockers,
                nonclaim_names=frozen_nonclaim_names,
                state_type=frozen_state_type,
            )
        finally:
            frozen_release_metadata(cpython, "cpython")
            frozen_release_metadata(microsoft, "microsoft")
            frozen_release_closure(jsonschema_closure)

    return assemble_candidate_state


assemble_candidate_state = _freeze_candidate_assembler()


__all__ = [
    "CandidateState",
    "INITIAL_BLOCKERS",
    "NONCLAIM_NAMES",
    "assemble_candidate_state",
]

"""Closed Authenticode adapter that can emit only a proposed Build Tools pin."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
import re
from typing import Callable, Final

from s0_windows_authenticode_verifier.contract import (
    ACQUISITION_HANDLE_CONTRACT,
    ACQUISITION_PATH_SEMANTICS_ID,
    ACQUISITION_SCHEMA_ID,
    RUNTIME_AUTHORITY_SCOPE,
)
from s0_windows_authenticode_verifier.model import VerificationResult

from ._issuance import make_bounded_issuance_registry
from .canonical import (
    canonical_json_lf,
    require_exact_int,
    require_exact_text,
    require_sha256,
    sha256_hex,
)
from .errors import AuthorityError
from .metadata import (
    _release_issued_metadata_evidence,
    validate_microsoft_release_metadata,
)
from .pins import (
    AUTHENTICODE_IMPLEMENTATION_MANIFEST_SHA256,
    BUILDTOOLS_ARTIFACT_ID,
    resolve_artifact_snapshot,
    resolve_source_snapshot,
)


_VOLUME = re.compile(r"^[0-9a-f]{16}$")
_FILE_ID = re.compile(r"^[0-9a-f]{32}$")
_FILETIME = re.compile(r"^[0-9a-f]{16}$")
_VOLUME_GUID_PATH = re.compile(
    r"^\\\\\?\\Volume\{[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-"
    r"[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}\}\\"
)
_ORDINARY_DRIVE_PATH = re.compile(r"^[A-Za-z]:\\")
_ORDINARY_UNC_PATH = re.compile(r"^\\\\[^\\]+\\[^\\]+\\")


def _frozen_manifest_mapping() -> dict[str, object]:
    source = resolve_source_snapshot("microsoft-vs-2022-release-history-17.14.39")
    artifact = resolve_artifact_snapshot(BUILDTOOLS_ARTIFACT_ID)
    return {
        "artifact": {
            "authority_state": artifact[6],
            "filename": artifact[1],
            "sha256": artifact[3],
            "size": artifact[4],
            "url": artifact[2],
        },
        "authenticode_implementation_manifest_sha256": (
            AUTHENTICODE_IMPLEMENTATION_MANIFEST_SHA256
        ),
        "schema_id": "S0-EXTERNAL-ARTIFACT-ACQUISITION-AUTHORITY-MANIFEST-1",
        "source": {
            "sha256": source[2],
            "size": source[3],
            "source_id": source[0],
            "url": source[1],
        },
    }


BUILDTOOLS_ACQUISITION_AUTHORITY_MANIFEST_RAW: Final = canonical_json_lf(
    _frozen_manifest_mapping()
)
BUILDTOOLS_ACQUISITION_AUTHORITY_MANIFEST_SHA256: Final = sha256_hex(
    BUILDTOOLS_ACQUISITION_AUTHORITY_MANIFEST_RAW
)


@dataclass(frozen=True, slots=True, weakref_slot=True)
class BuildToolsPinProposal:
    status: str
    artifact_id: str
    filename: str
    url: str
    sha256: str
    size: int
    acquired_path: str
    verifier_full_path: str
    acquisition_record_sha256: str
    acquisition_authority_manifest_sha256: str
    authenticode_implementation_manifest_sha256: str
    authenticode_decision_sha256: str
    trust_policy_pass: bool
    active_authority: bool
    executed_code_authority_established: bool
    process_authority_granted: bool
    acquired_byte_executed: bool
    acquisition_record_raw: bytes = field(repr=False)


def _require_hex(
    value: object,
    grammar: re.Pattern[str],
    *,
    label: str,
    error_type,
) -> str:
    if type(value) is not str or grammar.fullmatch(value) is None:
        raise error_type(f"{label}_hex_invalid")
    return value


def _require_acquired_path(
    value: object,
    *,
    require_text,
    path_grammar,
    error_type,
) -> str:
    path = require_text(value, label="buildtools_acquired_path")
    match = path_grammar.match(path)
    if match is None:
        raise error_type("buildtools_acquired_path_not_volume_guid")
    tail = path[match.end() :]
    if (
        not tail
        or tail.endswith("\\")
        or "/" in tail
        or ":" in tail
        or any(character in tail for character in '*?"<>|')
    ):
        raise error_type("buildtools_acquired_path_invalid")
    if any(
        not component
        or component in {".", ".."}
        or component.endswith((" ", "."))
        for component in tail.split("\\")
    ):
        raise error_type("buildtools_acquired_path_component_invalid")
    return path


def _require_verifier_full_path(
    value: object,
    *,
    require_text,
    drive_grammar,
    unc_grammar,
    volume_guid_grammar,
    error_type,
) -> str:
    path = require_text(value, label="buildtools_verifier_full_path")
    if (
        "/" in path
        or path.startswith(("\\\\?\\", "\\\\.\\"))
        or volume_guid_grammar.match(path) is not None
    ):
        raise error_type("buildtools_verifier_full_path_not_ordinary")
    drive = drive_grammar.match(path)
    unc = unc_grammar.match(path)
    match = drive if drive is not None else unc
    if match is None:
        raise error_type("buildtools_verifier_full_path_not_absolute")
    tail = path[match.end() :]
    if (
        not tail
        or tail.endswith("\\")
        or ":" in tail
        or any(character in tail for character in '*?"<>|')
    ):
        raise error_type("buildtools_verifier_full_path_invalid")
    if any(
        not component
        or component in {".", ".."}
        or component.endswith((" ", "."))
        for component in tail.split("\\")
    ):
        raise error_type("buildtools_verifier_full_path_component_invalid")
    return path


def _build_buildtools_acquisition_record_impl(
    *,
    sequence_id: str,
    producer_process_id: int,
    created_filetime_hex: str,
    acquired_path: str,
    retained_handle: int,
    volume_serial_hex: str,
    file_id_hex: str,
    resolve_artifact,
    artifact_id,
    require_sha,
    require_int,
    require_hex,
    filetime_grammar,
    require_path,
    volume_grammar,
    file_id_grammar,
    canonical_encoder,
    path_semantics_id,
    authority_manifest_sha256,
    handle_contract,
    schema_id,
    error_type,
) -> bytes:
    """Build exact canonical evidence using only the frozen artifact row."""

    artifact = resolve_artifact(artifact_id)
    sequence = require_sha(sequence_id, label="buildtools_sequence")
    process_id = require_int(
        producer_process_id, label="buildtools_producer_process", minimum=1, maximum=0xFFFFFFFF
    )
    created = require_hex(
        created_filetime_hex,
        filetime_grammar,
        label="buildtools_created_filetime",
        error_type=error_type,
    )
    if int(created, 16) <= 0:
        raise error_type("buildtools_created_filetime_not_positive")
    path = require_path(acquired_path)
    handle = require_int(
        retained_handle,
        label="buildtools_retained_handle",
        minimum=1,
        maximum=0xFFFFFFFFFFFFFFFF,
    )
    volume = require_hex(
        volume_serial_hex,
        volume_grammar,
        label="buildtools_volume_serial",
        error_type=error_type,
    )
    file_id = require_hex(
        file_id_hex,
        file_id_grammar,
        label="buildtools_file_id",
        error_type=error_type,
    )
    return canonical_encoder(
        {
            "acquired_path": path,
            "acquired_path_semantics": path_semantics_id,
            "authority_manifest_sha256": authority_manifest_sha256,
            "byte_sha256": artifact[3],
            "created_filetime_hex": created,
            "file_identity": {
                "byte_length": artifact[4],
                "file_id_hex": file_id,
                "reparse_point": False,
                "volume_serial_hex": volume,
            },
            "final_uri": artifact[2],
            "handle_contract": dict(handle_contract),
            "producer_process_id": process_id,
            "redirect_count": 0,
            "requested_uri": artifact[2],
            "retained_handle_hex": f"{handle:016x}",
            "schema_id": schema_id,
            "sequence_id": sequence,
            "transfer_complete": True,
        }
    )


def _freeze_acquired_path_validator():
    implementation = _require_acquired_path
    frozen_require_text = require_exact_text
    frozen_path_grammar = _VOLUME_GUID_PATH
    frozen_error_type = AuthorityError

    def require_acquired_path(value: object) -> str:
        return implementation(
            value,
            require_text=frozen_require_text,
            path_grammar=frozen_path_grammar,
            error_type=frozen_error_type,
        )

    return require_acquired_path


def _freeze_verifier_full_path_validator():
    implementation = _require_verifier_full_path
    frozen_require_text = require_exact_text
    frozen_drive_grammar = _ORDINARY_DRIVE_PATH
    frozen_unc_grammar = _ORDINARY_UNC_PATH
    frozen_volume_guid_grammar = _VOLUME_GUID_PATH
    frozen_error_type = AuthorityError

    def require_verifier_full_path(value: object) -> str:
        return implementation(
            value,
            require_text=frozen_require_text,
            drive_grammar=frozen_drive_grammar,
            unc_grammar=frozen_unc_grammar,
            volume_guid_grammar=frozen_volume_guid_grammar,
            error_type=frozen_error_type,
        )

    return require_verifier_full_path


def _freeze_record_builder():
    implementation = _build_buildtools_acquisition_record_impl
    frozen_resolve_artifact = resolve_artifact_snapshot
    frozen_artifact_id = BUILDTOOLS_ARTIFACT_ID
    frozen_require_sha = require_sha256
    frozen_require_int = require_exact_int
    frozen_require_hex = _require_hex
    frozen_filetime_grammar = _FILETIME
    frozen_require_path = _freeze_acquired_path_validator()
    frozen_volume_grammar = _VOLUME
    frozen_file_id_grammar = _FILE_ID
    frozen_canonical_encoder = canonical_json_lf
    frozen_path_semantics_id = ACQUISITION_PATH_SEMANTICS_ID
    frozen_authority_manifest_sha256 = (
        BUILDTOOLS_ACQUISITION_AUTHORITY_MANIFEST_SHA256
    )
    frozen_handle_contract = dict(ACQUISITION_HANDLE_CONTRACT)
    frozen_schema_id = ACQUISITION_SCHEMA_ID
    frozen_error_type = AuthorityError

    def build_buildtools_acquisition_record(
        *,
        sequence_id: str,
        producer_process_id: int,
        created_filetime_hex: str,
        acquired_path: str,
        retained_handle: int,
        volume_serial_hex: str,
        file_id_hex: str,
    ) -> bytes:
        return implementation(
            sequence_id=sequence_id,
            producer_process_id=producer_process_id,
            created_filetime_hex=created_filetime_hex,
            acquired_path=acquired_path,
            retained_handle=retained_handle,
            volume_serial_hex=volume_serial_hex,
            file_id_hex=file_id_hex,
            resolve_artifact=frozen_resolve_artifact,
            artifact_id=frozen_artifact_id,
            require_sha=frozen_require_sha,
            require_int=frozen_require_int,
            require_hex=frozen_require_hex,
            filetime_grammar=frozen_filetime_grammar,
            require_path=frozen_require_path,
            volume_grammar=frozen_volume_grammar,
            file_id_grammar=frozen_file_id_grammar,
            canonical_encoder=frozen_canonical_encoder,
            path_semantics_id=frozen_path_semantics_id,
            authority_manifest_sha256=frozen_authority_manifest_sha256,
            handle_contract=frozen_handle_contract,
            schema_id=frozen_schema_id,
            error_type=frozen_error_type,
        )

    return build_buildtools_acquisition_record


build_buildtools_acquisition_record = _freeze_record_builder()


def _freeze_buildtools_adapter(
    verifier: Callable[..., VerificationResult],
    *,
    include_issuance_checker: bool = False,
):
    direct_verifier = verifier
    expected_result_type = VerificationResult
    expected_manifest = AUTHENTICODE_IMPLEMENTATION_MANIFEST_SHA256
    expected_runtime_scope = RUNTIME_AUTHORITY_SCOPE
    expected_authority_manifest = BUILDTOOLS_ACQUISITION_AUTHORITY_MANIFEST_SHA256
    build_record = build_buildtools_acquisition_record
    validate_release = validate_microsoft_release_metadata
    resolve_artifact = resolve_artifact_snapshot
    artifact_id = BUILDTOOLS_ARTIFACT_ID
    require_acquired_path = _freeze_acquired_path_validator()
    require_verifier_full_path = _freeze_verifier_full_path_validator()
    hash_bytes = sha256_hex
    proposal_type = BuildToolsPinProposal
    error_type = AuthorityError
    release_metadata_evidence = _release_issued_metadata_evidence
    object_id = id
    materialize = replace
    frozen_type = type
    frozen_getattribute = object.__getattribute__

    def snapshot(value: object) -> tuple[object, ...]:
        if frozen_type(value) is not proposal_type:
            raise error_type("buildtools_proposal_type_not_issued")
        return (
            frozen_getattribute(value, "status"),
            frozen_getattribute(value, "artifact_id"),
            frozen_getattribute(value, "filename"),
            frozen_getattribute(value, "url"),
            frozen_getattribute(value, "sha256"),
            frozen_getattribute(value, "size"),
            frozen_getattribute(value, "acquired_path"),
            frozen_getattribute(value, "verifier_full_path"),
            frozen_getattribute(value, "acquisition_record_sha256"),
            frozen_getattribute(
                value, "acquisition_authority_manifest_sha256"
            ),
            frozen_getattribute(
                value, "authenticode_implementation_manifest_sha256"
            ),
            frozen_getattribute(value, "authenticode_decision_sha256"),
            frozen_getattribute(value, "trust_policy_pass"),
            frozen_getattribute(value, "active_authority"),
            frozen_getattribute(value, "executed_code_authority_established"),
            frozen_getattribute(value, "process_authority_granted"),
            frozen_getattribute(value, "acquired_byte_executed"),
            object_id(frozen_getattribute(value, "acquisition_record_raw")),
        )

    issue, require_issued, _consume_issued, _release_issued = (
        make_bounded_issuance_registry(
            limits={"proposal": 1},
            snapshot=snapshot,
            materialize=materialize,
            error_type=error_type,
            capacity_error="buildtools_proposal_registry_capacity_exceeded",
            invalid_kind_error="buildtools_proposal_registry_kind_invalid",
            not_issued_error="buildtools_proposal_not_issued_or_changed",
        )
    )

    def verify_buildtools_and_propose_pin(
        *,
        release_history_raw: bytes,
        verifier_full_path: str,
        file_handle: int,
        sequence_id: str,
        producer_process_id: int,
        created_filetime_hex: str,
        acquired_path: str,
        volume_serial_hex: str,
        file_id_hex: str,
    ) -> BuildToolsPinProposal:
        release_evidence = validate_release(release_history_raw)
        try:
            verifier_path = require_verifier_full_path(verifier_full_path)
            acquisition_path = require_acquired_path(acquired_path)
            record = build_record(
                sequence_id=sequence_id,
                producer_process_id=producer_process_id,
                created_filetime_hex=created_filetime_hex,
                acquired_path=acquisition_path,
                retained_handle=file_handle,
                volume_serial_hex=volume_serial_hex,
                file_id_hex=file_id_hex,
            )
            record_sha = hash_bytes(record)
            try:
                result = direct_verifier(
                    full_path=verifier_path,
                    file_handle=file_handle,
                    implementation_manifest_sha256=expected_manifest,
                    acquisition_record_raw=record,
                    acquisition_record_sha256=record_sha,
                    acquisition_authority_manifest_sha256=expected_authority_manifest,
                    process_count_before_decision=0,
                )
            except Exception as exc:
                raise error_type("buildtools_authenticode_verifier_failed") from exc
            if type(result) is not expected_result_type:
                raise error_type("buildtools_authenticode_result_type_invalid")
            if result.trust_policy_pass is not True:
                raise error_type("buildtools_authenticode_trust_policy_rejected")
            if result.failure_relations != ():
                raise error_type("buildtools_authenticode_failures_nonempty")
            if result.runtime_authority_scope != expected_runtime_scope:
                raise error_type("buildtools_authenticode_runtime_scope_mismatch")
            if result.executed_code_authority_established is not False:
                raise error_type("buildtools_executed_code_authority_forbidden")
            if result.process_authority_granted is not False:
                raise error_type("buildtools_process_authority_forbidden")
            artifact = resolve_artifact(artifact_id)
            proposal = proposal_type(
                "PROPOSED-AUTHORITY-PIN",
                artifact[0],
                artifact[1],
                artifact[2],
                artifact[3],
                artifact[4],
                acquisition_path,
                verifier_path,
                record_sha,
                expected_authority_manifest,
                expected_manifest,
                result.decision_sha256,
                True,
                False,
                False,
                False,
                False,
                record,
            )
            return issue(proposal, "proposal")
        finally:
            release_metadata_evidence(release_evidence, "microsoft")

    def require_issued_buildtools_proposal(value: object) -> BuildToolsPinProposal:
        return require_issued(value, "proposal")

    if include_issuance_checker:
        return verify_buildtools_and_propose_pin, require_issued_buildtools_proposal
    return verify_buildtools_and_propose_pin


_BUILD_TOOLS_TRANSITIVE_CLOSURE_BLOCKER: Final = (
    "BUILD-TOOLS-AUTHENTICODE-TRANSITIVE-CLOSURE-UNVERIFIED"
)


def _freeze_disabled_public_buildtools_path():
    """Keep the V0.1 API while refusing all public proposal authority."""

    error_type = AuthorityError
    blocker = _BUILD_TOOLS_TRANSITIVE_CLOSURE_BLOCKER

    def verify_buildtools_and_propose_pin(
        *,
        release_history_raw: bytes,
        verifier_full_path: str,
        file_handle: int,
        sequence_id: str,
        producer_process_id: int,
        created_filetime_hex: str,
        acquired_path: str,
        volume_serial_hex: str,
        file_id_hex: str,
    ) -> BuildToolsPinProposal:
        raise error_type(blocker)

    def require_issued_buildtools_proposal(
        value: object,
    ) -> BuildToolsPinProposal:
        raise error_type(blocker)

    return verify_buildtools_and_propose_pin, require_issued_buildtools_proposal


# The private adapter remains a deterministic TEST seam.  Its registry is
# isolated from the public checker and cannot satisfy candidate assembly.
(
    verify_buildtools_and_propose_pin,
    _require_issued_buildtools_proposal,
) = _freeze_disabled_public_buildtools_path()


__all__ = [
    "BUILDTOOLS_ACQUISITION_AUTHORITY_MANIFEST_RAW",
    "BUILDTOOLS_ACQUISITION_AUTHORITY_MANIFEST_SHA256",
    "BuildToolsPinProposal",
    "build_buildtools_acquisition_record",
    "verify_buildtools_and_propose_pin",
]

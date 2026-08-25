"""Fail-closed trusted-host entry for acquisition, native, and semantic checks."""

from __future__ import annotations

import os

from .acquisition import authenticate_acquisition_record
from .authority import authenticate_installed_implementation
from .canonical import VerificationError, canonical_json_lf
from .contract import OBSERVATION_SCHEMA_ID
from .model import VerificationResult
from .semantic import evaluate_observation
from .win32 import NativeVerificationError, collect_observation


def verify_open_file_trusted_host(
    *,
    full_path: str,
    file_handle: int,
    implementation_manifest_sha256: str,
    acquisition_record_raw: bytes,
    acquisition_record_sha256: str,
    acquisition_authority_manifest_sha256: str,
    process_count_before_decision: int = 0,
) -> VerificationResult:
    """Verify without execution and without claiming executed-code authority."""

    authority = authenticate_installed_implementation(
        implementation_manifest_sha256,
        expected_acquisition_record_sha256=acquisition_record_sha256,
        expected_acquisition_authority_manifest_sha256=(
            acquisition_authority_manifest_sha256
        ),
    )
    try:
        acquisition = authenticate_acquisition_record(
            acquisition_record_raw,
            expected_record_sha256=authority.acquisition_record_sha256,
            expected_authority_manifest_sha256=(
                authority.acquisition_authority_manifest_sha256
            ),
            retained_handle=file_handle,
            current_process_id=os.getpid(),
        )
        observation = collect_observation(
            full_path=full_path,
            file_handle=file_handle,
            authority=authority,
            acquisition=acquisition,
            process_count_before_decision=process_count_before_decision,
        )
    except (
        NativeVerificationError,
        VerificationError,
        OSError,
        OverflowError,
        ValueError,
    ):
        observation = canonical_json_lf(
            {
                "native_collection_status": "FAILED-BEFORE-PROCESS",
                "schema_id": OBSERVATION_SCHEMA_ID,
            }
        )
    return evaluate_observation(observation, authority)

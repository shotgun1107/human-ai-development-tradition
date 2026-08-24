"""Fail-closed public entry point for native collection plus semantic decision."""

from __future__ import annotations

from .authority import authenticate_installed_implementation
from .canonical import canonical_json_lf
from .contract import OBSERVATION_SCHEMA_ID
from .model import VerificationResult
from .semantic import evaluate_observation
from .win32 import NativeVerificationError, collect_observation


def verify_open_file(
    *,
    full_path: str,
    file_handle: int,
    implementation_manifest_sha256: str,
    requested_uri: str,
    final_uri: str,
    redirect_count: int,
    process_count_before_decision: int = 0,
) -> VerificationResult:
    """Verify without executing; every native or semantic ambiguity rejects."""

    authority = authenticate_installed_implementation(implementation_manifest_sha256)
    try:
        observation = collect_observation(
            full_path=full_path,
            file_handle=file_handle,
            authority=authority,
            requested_uri=requested_uri,
            final_uri=final_uri,
            redirect_count=redirect_count,
            process_count_before_decision=process_count_before_decision,
        )
    except (NativeVerificationError, OSError, OverflowError, ValueError):
        observation = canonical_json_lf(
            {
                "native_collection_status": "FAILED-BEFORE-PROCESS",
                "schema_id": OBSERVATION_SCHEMA_ID,
            }
        )
    return evaluate_observation(observation, authority)

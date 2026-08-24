"""PUBLIC Windows Authenticode verifier implementation candidate."""

from .canonical import VerificationError, canonical_json_lf, sha256_hex, strict_json_object
from .authority import authenticate_installed_implementation
from .contract import (
    FIXED_BOOTSTRAPPER_URL,
    SEMANTIC_RELATIONS,
    SUPPLIER_CRITERION_ID,
)
from .model import VerificationAuthority, VerificationResult
from .semantic import chain_call_input_sha256, evaluate_observation, policy_input_sha256
from .verifier import verify_open_file
from .win32 import NativeVerificationError, collect_observation

__all__ = [
    "FIXED_BOOTSTRAPPER_URL",
    "NativeVerificationError",
    "SEMANTIC_RELATIONS",
    "SUPPLIER_CRITERION_ID",
    "VerificationAuthority",
    "VerificationError",
    "VerificationResult",
    "canonical_json_lf",
    "authenticate_installed_implementation",
    "chain_call_input_sha256",
    "collect_observation",
    "evaluate_observation",
    "policy_input_sha256",
    "sha256_hex",
    "strict_json_object",
    "verify_open_file",
]

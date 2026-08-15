"""PUBLIC, non-executing S0 build/runtime materialization candidate."""

from .authority import AuthenticatedDesign, DesignClosure, ManifestBundle, authenticate_design_closure
from .candidate import BuildRuntimeDiagnostic, prepare_public_build_runtime_candidate
from .canonical import TargetRow, jcs_lf, semantic_relations_preimage, target_set_preimage
from .planning import (
    DllDirectory,
    DllResolutionPlan,
    DllResolutionRow,
    DllRow,
    RuntimeMaterializationPlan,
    RuntimeRow,
    derive_dll_directories,
    directory_identity_sha256,
    plan_dll_resolution,
    plan_runtime_tree,
    windows_directory_identity_key,
)
from .records import InMemoryRecordDiagnostic, construct_in_memory_record
from .semantics import EffectiveDesign, validate_effective_design

__all__ = [
    "AuthenticatedDesign",
    "BuildRuntimeDiagnostic",
    "DesignClosure",
    "DllDirectory",
    "DllResolutionPlan",
    "DllResolutionRow",
    "DllRow",
    "EffectiveDesign",
    "ManifestBundle",
    "InMemoryRecordDiagnostic",
    "RuntimeMaterializationPlan",
    "RuntimeRow",
    "TargetRow",
    "authenticate_design_closure",
    "construct_in_memory_record",
    "derive_dll_directories",
    "directory_identity_sha256",
    "jcs_lf",
    "plan_dll_resolution",
    "plan_runtime_tree",
    "prepare_public_build_runtime_candidate",
    "semantic_relations_preimage",
    "target_set_preimage",
    "validate_effective_design",
    "windows_directory_identity_key",
]

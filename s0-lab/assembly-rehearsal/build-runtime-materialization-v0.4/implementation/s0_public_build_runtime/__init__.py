"""PUBLIC, non-executing S0 build/runtime materialization candidate."""

from .authority import AuthenticatedDesign, DesignClosure, ManifestBundle, authenticate_design_closure
from .candidate import BuildRuntimeDiagnostic, prepare_public_build_runtime_candidate
from .canonical import TargetRow, jcs_lf, semantic_relations_preimage, target_set_preimage
from .planning import (
    DllDirectoryDiagnostic,
    DllResolutionRowDiagnostic,
    DllResolutionStructureDiagnostic,
    DllRow,
    RuntimeRow,
    RuntimeTreeStructureDiagnostic,
    derive_dll_directories,
    directory_identity_sha256,
    inspect_dll_resolution_structure,
    inspect_runtime_tree_structure,
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
    "DllDirectoryDiagnostic",
    "DllResolutionRowDiagnostic",
    "DllResolutionStructureDiagnostic",
    "DllRow",
    "EffectiveDesign",
    "ManifestBundle",
    "InMemoryRecordDiagnostic",
    "RuntimeRow",
    "RuntimeTreeStructureDiagnostic",
    "TargetRow",
    "authenticate_design_closure",
    "construct_in_memory_record",
    "derive_dll_directories",
    "directory_identity_sha256",
    "jcs_lf",
    "inspect_dll_resolution_structure",
    "inspect_runtime_tree_structure",
    "plan_dll_resolution",
    "plan_runtime_tree",
    "prepare_public_build_runtime_candidate",
    "semantic_relations_preimage",
    "target_set_preimage",
    "validate_effective_design",
    "windows_directory_identity_key",
]

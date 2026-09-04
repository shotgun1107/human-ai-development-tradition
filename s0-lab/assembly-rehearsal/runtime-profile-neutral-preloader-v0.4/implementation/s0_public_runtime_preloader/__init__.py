"""Bounded public runtime-profile/preloader implementation candidate v0.4.

The exported Python surface remains the inherited offline conformance lane.
The native preloader and one-use guard live beside this package and do not
turn these data objects into live authority.
"""

from .errors import RuntimeProfileError
from .evidence import (
    OfflineLaunchEvidenceDiagnostic,
    LaunchMaterialSet,
    OfflineAdmissionDiagnostic,
)
from .integration import (
    AssemblyArtifactBundle,
    AssemblyArtifactValidation,
    prepare_assembly_runtime_launch,
    validate_assembly_artifact_bundle,
)
from .preloader import (
    NeutralPreloader,
    OfflinePreparedLaunch,
    OfflinePreloaderInputs,
    OrderedHandleLocators,
    prepare_offline_admission_diagnostic,
)
from .profile import ValidatedProfileCandidate, validate_runtime_profile_candidate
from .semantic import (
    ArtifactMaterial,
    BinaryMaterial,
    HandleObservation,
    PostcreationObservation,
    PrecreationObservation,
    PredecessorProfileMaterial,
    StaticMaterialBundle,
    SystemImageMaterial,
)

__all__ = [
    "ArtifactMaterial",
    "AssemblyArtifactBundle",
    "AssemblyArtifactValidation",
    "BinaryMaterial",
    "HandleObservation",
    "OfflineLaunchEvidenceDiagnostic",
    "LaunchMaterialSet",
    "NeutralPreloader",
    "OfflineAdmissionDiagnostic",
    "OfflinePreparedLaunch",
    "OfflinePreloaderInputs",
    "OrderedHandleLocators",
    "PostcreationObservation",
    "PrecreationObservation",
    "PredecessorProfileMaterial",
    "RuntimeProfileError",
    "StaticMaterialBundle",
    "SystemImageMaterial",
    "ValidatedProfileCandidate",
    "prepare_assembly_runtime_launch",
    "prepare_offline_admission_diagnostic",
    "validate_assembly_artifact_bundle",
    "validate_runtime_profile_candidate",
]

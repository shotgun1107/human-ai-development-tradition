"""Bounded public runtime-profile and neutral-preloader candidate v0.1."""

from .errors import PlatformGateClosed, RuntimeProfileError
from .evidence import (
    AdmissionFrame,
    LaunchEvidence,
    LaunchIdentity,
    build_admission_frame,
    build_launch_evidence,
)
from .integration import AssemblyCandidatePins, prepare_assembly_runtime_launch
from .preloader import NeutralPreloader, OrderedHandleLocators, PreparedLaunch, PreloaderInputs
from .profile import (
    AuthenticatedRuntimeProfile,
    authenticate_runtime_profile,
    is_authenticated_runtime_profile,
)
from .semantic import (
    AdmissionBinding,
    ArtifactBinding,
    HandleBinding,
    PackageRow,
    SemanticEvidence,
    SystemImageBinding,
)

__all__ = [
    "AdmissionBinding",
    "AdmissionFrame",
    "ArtifactBinding",
    "AssemblyCandidatePins",
    "AuthenticatedRuntimeProfile",
    "HandleBinding",
    "LaunchEvidence",
    "LaunchIdentity",
    "NeutralPreloader",
    "OrderedHandleLocators",
    "PackageRow",
    "PlatformGateClosed",
    "PreparedLaunch",
    "PreloaderInputs",
    "RuntimeProfileError",
    "SemanticEvidence",
    "SystemImageBinding",
    "authenticate_runtime_profile",
    "build_admission_frame",
    "build_launch_evidence",
    "is_authenticated_runtime_profile",
    "prepare_assembly_runtime_launch",
]

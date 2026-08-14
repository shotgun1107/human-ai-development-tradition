"""Pin-only bridge to the existing public assembly candidate."""

from __future__ import annotations

from dataclasses import dataclass

from .canonical import require_sha256
from .errors import RuntimeProfileError
from .preloader import NeutralPreloader, PreloaderInputs, PreparedLaunch
from .profile import AuthenticatedRuntimeProfile


ASSEMBLY_IMPLEMENTATION_MANIFEST_SHA256 = (
    "0cc96816404094dec313dbab4bb108744383afb2ca5272834b589235364a9623"
)
ASSEMBLY_CANDIDATE_REPORT_SHA256 = (
    "520a237109686a17b8c075c15f1cc676a43d450716a6157bce7b48585f0c5005"
)
RUNTIME_DESIGN_PACKAGE_MANIFEST_SHA256 = (
    "abecc3951f29201f24e7fd069865d5a10cf76587b2c1e7c8013ff9226479e589"
)
RUNTIME_DESIGN_REREVIEW_RECORD_SHA256 = (
    "9fca4e14309304e5540d4e4e210dcfea72890729764aa4af5dadc736497c4e71"
)


@dataclass(frozen=True)
class AssemblyCandidatePins:
    implementation_manifest_sha256: str
    candidate_report_sha256: str
    runtime_design_package_manifest_sha256: str
    runtime_design_rereview_record_sha256: str

    def __post_init__(self) -> None:
        values = (
            self.implementation_manifest_sha256,
            self.candidate_report_sha256,
            self.runtime_design_package_manifest_sha256,
            self.runtime_design_rereview_record_sha256,
        )
        for value in values:
            require_sha256(value, "assembly/runtime integration pin")
        if values != (
            ASSEMBLY_IMPLEMENTATION_MANIFEST_SHA256,
            ASSEMBLY_CANDIDATE_REPORT_SHA256,
            RUNTIME_DESIGN_PACKAGE_MANIFEST_SHA256,
            RUNTIME_DESIGN_REREVIEW_RECORD_SHA256,
        ):
            raise RuntimeProfileError("assembly/runtime integration pins are not exact")


def prepare_assembly_runtime_launch(
    *,
    pins: AssemblyCandidatePins,
    authority: AuthenticatedRuntimeProfile,
    inputs: PreloaderInputs,
) -> PreparedLaunch:
    if type(pins) is not AssemblyCandidatePins:
        raise RuntimeProfileError("assembly candidate pin authority is not exact")
    return NeutralPreloader().prepare(authority, inputs)


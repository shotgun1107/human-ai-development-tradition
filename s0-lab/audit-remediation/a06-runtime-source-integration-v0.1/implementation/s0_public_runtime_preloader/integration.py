"""Byte-authenticated bridge to the pinned assembly and v0.4 authorities."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from .canonical import sha256_bytes, verify_manifest_material
from .errors import RuntimeProfileError
from .preloader import (
    NeutralPreloader,
    OfflinePreparedLaunch,
    OfflinePreloaderInputs,
)
from .semantic import StaticMaterialBundle
from .profile import SuccessorProfileMaterial


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
_MAPPING_PROXY_TYPE = type(MappingProxyType({}))


def _copy_byte_mapping(value: Mapping[str, bytes], label: str) -> Mapping[str, bytes]:
    if type(value) not in {dict, _MAPPING_PROXY_TYPE}:
        raise RuntimeProfileError(f"{label} is not one exact dictionary")
    copied: dict[str, bytes] = {}
    for path, raw in value.items():
        if type(path) is not str or type(raw) is not bytes:
            raise RuntimeProfileError(f"{label} contains a non-byte target")
        copied[path] = raw
    return MappingProxyType(copied)


@dataclass(frozen=True)
class AssemblyArtifactBundle:
    implementation_manifest_raw: bytes
    implementation_targets: Mapping[str, bytes]
    candidate_report_raw: bytes
    design_manifest_raw: bytes
    design_targets: Mapping[str, bytes]
    rereview_record_raw: bytes

    def __post_init__(self) -> None:
        for raw in (
            self.implementation_manifest_raw,
            self.candidate_report_raw,
            self.design_manifest_raw,
            self.rereview_record_raw,
        ):
            if type(raw) is not bytes or not raw:
                raise RuntimeProfileError("assembly bridge artifact is not nonempty bytes")
        object.__setattr__(
            self,
            "implementation_targets",
            _copy_byte_mapping(self.implementation_targets, "assembly implementation targets"),
        )
        object.__setattr__(
            self,
            "design_targets",
            _copy_byte_mapping(self.design_targets, "runtime design targets"),
        )


@dataclass(frozen=True)
class AssemblyArtifactValidation:
    implementation_manifest_sha256: str
    candidate_report_sha256: str
    design_manifest_sha256: str
    rereview_record_sha256: str
    implementation_rows: int
    design_rows: int
    candidate_only: bool = True

    def __post_init__(self) -> None:
        if self.candidate_only is not True:
            raise RuntimeProfileError("assembly artifact validation must remain candidate-only")


def validate_assembly_artifact_bundle(
    bundle: AssemblyArtifactBundle,
) -> AssemblyArtifactValidation:
    if type(bundle) is not AssemblyArtifactBundle:
        raise RuntimeProfileError("assembly artifact bundle is not exact")
    observed = (
        sha256_bytes(bundle.implementation_manifest_raw),
        sha256_bytes(bundle.candidate_report_raw),
        sha256_bytes(bundle.design_manifest_raw),
        sha256_bytes(bundle.rereview_record_raw),
    )
    expected = (
        ASSEMBLY_IMPLEMENTATION_MANIFEST_SHA256,
        ASSEMBLY_CANDIDATE_REPORT_SHA256,
        RUNTIME_DESIGN_PACKAGE_MANIFEST_SHA256,
        RUNTIME_DESIGN_REREVIEW_RECORD_SHA256,
    )
    if observed != expected:
        raise RuntimeProfileError("assembly/runtime bridge artifact bytes differ from exact pins")
    implementation_rows = verify_manifest_material(
        bundle.implementation_manifest_raw,
        bundle.implementation_targets,
        expected_rows=32,
    )
    design_rows = verify_manifest_material(
        bundle.design_manifest_raw,
        bundle.design_targets,
        expected_rows=6,
    )
    return AssemblyArtifactValidation(
        implementation_manifest_sha256=observed[0],
        candidate_report_sha256=observed[1],
        design_manifest_sha256=observed[2],
        rereview_record_sha256=observed[3],
        implementation_rows=len(implementation_rows),
        design_rows=len(design_rows),
    )


def prepare_assembly_runtime_launch(
    *,
    artifacts: AssemblyArtifactBundle,
    profile_raw: bytes,
    schema_raw: bytes,
    static_material: StaticMaterialBundle,
    successor: SuccessorProfileMaterial,
    inputs: OfflinePreloaderInputs,
) -> OfflinePreparedLaunch:
    # The validation result is intentionally discarded; callers cannot pass a
    # fabricated reusable pin object in place of exact artifact bytes.
    validate_assembly_artifact_bundle(artifacts)
    return NeutralPreloader().prepare(
        profile_raw=profile_raw,
        schema_raw=schema_raw,
        static_material=static_material,
        successor=successor,
        inputs=inputs,
    )

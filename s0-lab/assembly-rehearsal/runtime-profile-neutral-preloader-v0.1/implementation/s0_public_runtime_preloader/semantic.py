"""Executable v0.4 cross-object semantic relations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from .canonical import require_sha256, safe_virtual_path
from .errors import RuntimeProfileError


RELATIONS = (
    "profile-predecessor-hashes-equal-authenticated-v0.1-v0.2-v0.3-objects",
    "runtime-files-manifest-hash-and-path-equal-package-row",
    "guard-source-build-compiler-linker-imports-binary-loaded-image-form-one-provenance-chain",
    "guard-binary-and-loaded-image-file-identities-equal",
    "kernel32-and-ntdll-profile-identities-equal-loaded-images-and-direct-imports",
    "launch-evidence-five-entries-equal-process-creation-handle-array",
    "postcreation-admission-binds-evidence-current-verifier-pid-and-success-policy",
    "guard-five-locators-equal-launch-evidence-five-positions",
    "root-duplicate-and-retained-original-identify-same-object",
    "package-rows-equal-exact-effective-five-row-order",
)


@dataclass(frozen=True)
class ArtifactBinding:
    virtual_path: str
    sha256: str

    def __post_init__(self) -> None:
        safe_virtual_path(self.virtual_path)
        require_sha256(self.sha256, "artifact binding hash")


@dataclass(frozen=True)
class PackageRow(ArtifactBinding):
    pass


@dataclass(frozen=True)
class SystemImageBinding(ArtifactBinding):
    module_name: str
    file_id: str
    direct_import: str

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.module_name not in {"kernel32", "ntdll"}:
            raise RuntimeProfileError("system image module name is not admitted")
        if type(self.file_id) is not str or len(self.file_id) != 32:
            raise RuntimeProfileError("system image file ID is malformed")
        if type(self.direct_import) is not str or "!" not in self.direct_import:
            raise RuntimeProfileError("system image direct import is malformed")


@dataclass(frozen=True)
class HandleBinding:
    role: str
    kind: str
    access: str
    locator: str

    def __post_init__(self) -> None:
        for value in (self.role, self.kind, self.access, self.locator):
            if type(value) is not str or not value:
                raise RuntimeProfileError("handle binding field is not exact text")


@dataclass(frozen=True)
class AdmissionBinding:
    evidence_sha256: str
    actual_verifier_pid: int
    success_policy_id: str

    def __post_init__(self) -> None:
        require_sha256(self.evidence_sha256, "launch evidence hash")
        if type(self.actual_verifier_pid) is not int or self.actual_verifier_pid <= 0:
            raise RuntimeProfileError("actual verifier PID is invalid")
        if self.success_policy_id != "createprocess-success-bound-v0.4":
            raise RuntimeProfileError("creation success policy is not exact")


@dataclass(frozen=True)
class SemanticEvidence:
    predecessor_profile_hashes: tuple[str, str, str]
    runtime_files_manifest: ArtifactBinding
    provenance_chain: tuple[ArtifactBinding, ...]
    guard_binary_file_id: str
    guard_loaded_image_file_id: str
    system_images: tuple[SystemImageBinding, SystemImageBinding]
    launch_handles: tuple[HandleBinding, ...]
    launch_evidence_sha256: str
    admission: AdmissionBinding
    current_verifier_pid: int
    guard_locators: tuple[str, ...]
    retained_root_file_id: str
    duplicate_root_file_id: str
    package_rows: tuple[PackageRow, ...]
    current_profile_sha256: str
    semantic_validator_implementation: ArtifactBinding

    def __post_init__(self) -> None:
        if len(self.predecessor_profile_hashes) != 3:
            raise RuntimeProfileError("predecessor hash tuple is not exact")
        for digest in (*self.predecessor_profile_hashes, self.launch_evidence_sha256, self.current_profile_sha256):
            require_sha256(digest, "semantic evidence hash")
        if type(self.current_verifier_pid) is not int or self.current_verifier_pid <= 0:
            raise RuntimeProfileError("semantic current PID is invalid")
        for value in (self.guard_binary_file_id, self.guard_loaded_image_file_id, self.retained_root_file_id, self.duplicate_root_file_id):
            if type(value) is not str or len(value) != 32:
                raise RuntimeProfileError("semantic file ID is malformed")


def _artifact(value: Mapping[str, object]) -> ArtifactBinding:
    return ArtifactBinding(str(value["virtual_path"]), str(value["sha256"]))


def _fail(relation: str) -> None:
    raise RuntimeProfileError(f"semantic relation failed: {relation}")


def validate_semantic_relations(
    profile: Mapping[str, object],
    evidence: SemanticEvidence,
) -> tuple[str, ...]:
    """Execute all ten frozen relations or fail on the first mismatch."""

    if tuple(profile.get("semantic_relations", ())) != RELATIONS:
        _fail(RELATIONS[0])

    validator = profile["semantic_validator"]
    assert isinstance(validator, dict)
    if evidence.semantic_validator_implementation != _artifact(validator["implementation"]):
        raise RuntimeProfileError("semantic validator implementation identity is not authenticated")

    predecessor = (
        profile["v0_1_profile_sha256"],
        profile["v0_2_profile_sha256"],
        profile["v0_3_profile_sha256"],
    )
    if predecessor != evidence.predecessor_profile_hashes:
        _fail(RELATIONS[0])

    package = profile["package_closure"]
    assert isinstance(package, dict)
    runtime_manifest = _artifact(package["runtime_files_manifest"])
    if runtime_manifest != evidence.runtime_files_manifest:
        _fail(RELATIONS[1])
    if not evidence.package_rows or evidence.package_rows[0] != PackageRow(
        runtime_manifest.virtual_path,
        runtime_manifest.sha256,
    ):
        _fail(RELATIONS[1])

    guard = profile["bootstrap_guard"]
    assert isinstance(guard, dict)
    provenance_names = (
        "source",
        "build_recipe",
        "compiler",
        "linker",
        "import_manifest",
        "crt_import_manifest",
        "binary",
        "loaded_image",
    )
    expected_chain = tuple(_artifact(guard[name]) for name in provenance_names)
    if evidence.provenance_chain != expected_chain:
        _fail(RELATIONS[2])

    binary = guard["binary"]
    loaded = guard["loaded_image"]
    assert isinstance(binary, dict) and isinstance(loaded, dict)
    if (
        binary["file_id"] != loaded["file_id"]
        or evidence.guard_binary_file_id != binary["file_id"]
        or evidence.guard_loaded_image_file_id != loaded["file_id"]
    ):
        _fail(RELATIONS[3])

    platform = profile["platform_binding"]
    process = profile["process_creation_policy"]
    atomic = profile["atomic_root_policy"]
    assert isinstance(platform, dict) and isinstance(process, dict) and isinstance(atomic, dict)
    expected_images = (
        SystemImageBinding(
            virtual_path=platform["kernel32"]["virtual_path"],
            sha256=platform["kernel32"]["sha256"],
            module_name="kernel32",
            file_id=platform["kernel32"]["file_id"],
            direct_import=process["api"],
        ),
        SystemImageBinding(
            virtual_path=platform["ntdll"]["virtual_path"],
            sha256=platform["ntdll"]["sha256"],
            module_name="ntdll",
            file_id=platform["ntdll"]["file_id"],
            direct_import=atomic["direct_import"],
        ),
    )
    if evidence.system_images != expected_images:
        _fail(RELATIONS[4])

    expected_handles = tuple(
        (item["role"], item["kind"], item["access"])
        for item in process["ordered_handles"]
    )
    observed_handles = tuple((item.role, item.kind, item.access) for item in evidence.launch_handles)
    if observed_handles != expected_handles or len(evidence.launch_handles) != 5:
        _fail(RELATIONS[5])

    if (
        evidence.admission.evidence_sha256 != evidence.launch_evidence_sha256
        or evidence.admission.actual_verifier_pid != evidence.current_verifier_pid
        or evidence.admission.success_policy_id != "createprocess-success-bound-v0.4"
    ):
        _fail(RELATIONS[6])

    launch_locators = tuple(item.locator for item in evidence.launch_handles)
    if evidence.guard_locators != launch_locators:
        _fail(RELATIONS[7])

    if (
        evidence.retained_root_file_id != evidence.duplicate_root_file_id
        or not atomic["duplicate_same_object_required"]
    ):
        _fail(RELATIONS[8])

    expected_names = tuple(package["effective_rows"])
    expected_hashes = (
        runtime_manifest.sha256,
        profile["v0_1_profile_sha256"],
        profile["v0_2_profile_sha256"],
        profile["v0_3_profile_sha256"],
        evidence.current_profile_sha256,
    )
    expected_rows = tuple(PackageRow(name, digest) for name, digest in zip(expected_names, expected_hashes))
    if len(expected_names) != 5 or evidence.package_rows != expected_rows:
        _fail(RELATIONS[9])

    return RELATIONS

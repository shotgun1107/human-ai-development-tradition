"""Byte-backed, staged execution of the ten v0.4 semantic relations.

All public objects in this module are ordinary candidate data.  None is a
runtime authority.  Static relations hash supplied artifact bytes internally;
launch and postcreation relations are explicitly labelled offline observations
until a separately gated native collector exists.
"""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from .canonical import (
    load_json_bytes,
    require_sha256,
    safe_virtual_path,
    sha256_bytes,
    verify_manifest_material,
)
from .errors import RuntimeProfileError
from .schema import FixedDraft202012Validator


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
BYTE_VERIFIED_RELATIONS = (RELATIONS[0], RELATIONS[1], RELATIONS[9])
DEFERRED_STATIC_RELATIONS = (RELATIONS[2], RELATIONS[3], RELATIONS[4])
OFFLINE_PRECREATION_RELATIONS = (RELATIONS[5], RELATIONS[7], RELATIONS[8])
OFFLINE_POSTCREATION_RELATIONS = (RELATIONS[6],)
PROVENANCE_NAMES = (
    "source",
    "build_recipe",
    "compiler",
    "linker",
    "import_manifest",
    "crt_import_manifest",
    "binary",
    "loaded_image",
)
OFFLINE_OBSERVATION_SOURCE = "offline-candidate-observation-v0.2"
_MAPPING_PROXY_TYPE = type(MappingProxyType({}))


@dataclass(frozen=True)
class ArtifactMaterial:
    virtual_path: str
    raw: bytes

    def __post_init__(self) -> None:
        safe_virtual_path(self.virtual_path)
        if type(self.raw) is not bytes or not self.raw:
            raise RuntimeProfileError("artifact material is not nonempty exact bytes")

    @property
    def sha256(self) -> str:
        return sha256_bytes(self.raw)


@dataclass(frozen=True)
class BinaryMaterial(ArtifactMaterial):
    file_id: str
    pe_machine: str
    pe_timestamp: str
    size_of_image: str

    def __post_init__(self) -> None:
        super().__post_init__()
        if type(self.file_id) is not str or len(self.file_id) != 32:
            raise RuntimeProfileError("binary material file ID is malformed")
        for value in (self.pe_machine, self.pe_timestamp, self.size_of_image):
            if type(value) is not str or not value.startswith("0x"):
                raise RuntimeProfileError("binary material PE field is malformed")


@dataclass(frozen=True)
class SystemImageMaterial(BinaryMaterial):
    module_name: str
    volume_serial: str
    required_exports: tuple[tuple[str, str], ...]
    direct_import: str

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.module_name not in {"kernel32", "ntdll"}:
            raise RuntimeProfileError("system image module name is not exact")
        if type(self.volume_serial) is not str or not self.volume_serial.startswith("0x"):
            raise RuntimeProfileError("system image volume serial is malformed")
        if (
            type(self.required_exports) is not tuple
            or not self.required_exports
            or tuple(sorted(self.required_exports)) != self.required_exports
            or len({name for name, _ in self.required_exports}) != len(self.required_exports)
        ):
            raise RuntimeProfileError("system image export observations are not exact")
        for name, value in self.required_exports:
            if type(name) is not str or not name or type(value) is not str or not value.startswith("0x"):
                raise RuntimeProfileError("system image export observation is malformed")
        if type(self.direct_import) is not str or "!" not in self.direct_import:
            raise RuntimeProfileError("system image direct import is malformed")


@dataclass(frozen=True)
class PredecessorProfileMaterial:
    raw: bytes
    schema_raw: bytes
    schema_sha256: str

    def __post_init__(self) -> None:
        if type(self.raw) is not bytes or type(self.schema_raw) is not bytes:
            raise RuntimeProfileError("predecessor profile material is not exact bytes")
        require_sha256(self.schema_sha256, "predecessor schema pin")


@dataclass(frozen=True)
class StaticMaterialBundle:
    predecessors: tuple[
        PredecessorProfileMaterial,
        PredecessorProfileMaterial,
        PredecessorProfileMaterial,
    ]
    runtime_files_manifest: ArtifactMaterial
    runtime_files: Mapping[str, bytes]
    effective_package_manifest_raw: bytes
    effective_package_files: Mapping[str, bytes]
    provenance_chain: tuple[ArtifactMaterial, ...]
    platform_manifest: ArtifactMaterial
    loaded_pe_manifest: ArtifactMaterial
    system_images: tuple[SystemImageMaterial, SystemImageMaterial]
    semantic_validator: ArtifactMaterial

    def __post_init__(self) -> None:
        if type(self.predecessors) is not tuple or len(self.predecessors) != 3:
            raise RuntimeProfileError("predecessor material tuple is not exact")
        if type(self.provenance_chain) is not tuple or len(self.provenance_chain) != 8:
            raise RuntimeProfileError("provenance material tuple is not exact")
        if type(self.system_images) is not tuple or len(self.system_images) != 2:
            raise RuntimeProfileError("system image material tuple is not exact")
        if type(self.effective_package_manifest_raw) is not bytes:
            raise RuntimeProfileError("effective package manifest is not exact bytes")
        for name, value in (
            ("runtime_files", self.runtime_files),
            ("effective_package_files", self.effective_package_files),
        ):
            if type(value) not in {dict, _MAPPING_PROXY_TYPE}:
                raise RuntimeProfileError(f"{name} is not one exact byte dictionary")
            copied: dict[str, bytes] = {}
            for path, raw in value.items():
                canonical_path = safe_virtual_path(path)
                if type(raw) is not bytes:
                    raise RuntimeProfileError(f"{name} contains a non-byte target")
                copied[canonical_path] = raw
            object.__setattr__(self, name, MappingProxyType(copied))


@dataclass(frozen=True)
class HandleObservation:
    role: str
    kind: str
    access: str
    locator: str

    def __post_init__(self) -> None:
        for value in (self.role, self.kind, self.access, self.locator):
            if type(value) is not str or not value:
                raise RuntimeProfileError("handle observation field is not exact text")


@dataclass(frozen=True)
class PrecreationObservation:
    handles: tuple[HandleObservation, ...]
    guard_locators: tuple[str, ...]
    retained_root_file_id: str
    duplicate_root_file_id: str
    source: str = OFFLINE_OBSERVATION_SOURCE

    def __post_init__(self) -> None:
        if self.source != OFFLINE_OBSERVATION_SOURCE:
            raise RuntimeProfileError("precreation observation source is not offline candidate data")
        if type(self.handles) is not tuple or len(self.handles) != 5:
            raise RuntimeProfileError("precreation handle observation is not exact")
        if type(self.guard_locators) is not tuple or len(self.guard_locators) != 5:
            raise RuntimeProfileError("guard locator observation is not exact")
        for value in (self.retained_root_file_id, self.duplicate_root_file_id):
            if type(value) is not str or len(value) != 32:
                raise RuntimeProfileError("root identity observation is malformed")


@dataclass(frozen=True)
class PostcreationObservation:
    launch_evidence_sha256: str
    actual_verifier_pid: int
    current_verifier_pid: int
    success_policy_id: str
    source: str = OFFLINE_OBSERVATION_SOURCE

    def __post_init__(self) -> None:
        if self.source != OFFLINE_OBSERVATION_SOURCE:
            raise RuntimeProfileError("postcreation observation source is not offline candidate data")
        require_sha256(self.launch_evidence_sha256, "postcreation evidence hash")
        if (
            type(self.actual_verifier_pid) is not int
            or type(self.current_verifier_pid) is not int
            or self.actual_verifier_pid <= 0
            or self.current_verifier_pid <= 0
        ):
            raise RuntimeProfileError("postcreation PID observation is malformed")
        if self.success_policy_id != "createprocess-success-bound-v0.4":
            raise RuntimeProfileError("postcreation policy observation is not exact")


def _fail(relation: str) -> None:
    raise RuntimeProfileError(f"semantic relation failed: {relation}")


def _mapping(value: object, label: str) -> Mapping[str, object]:
    if not isinstance(value, Mapping):
        raise RuntimeProfileError(f"{label} is not one object")
    return value


def _match_artifact(profile_value: object, material: ArtifactMaterial, relation: str) -> None:
    expected = _mapping(profile_value, "profile artifact identity")
    if expected.get("virtual_path") != material.virtual_path or expected.get("sha256") != material.sha256:
        _fail(relation)


def _match_binary(profile_value: object, material: BinaryMaterial, relation: str) -> None:
    expected = _mapping(profile_value, "profile binary identity")
    _match_artifact(expected, material, relation)
    for name in ("file_id", "pe_machine", "pe_timestamp", "size_of_image"):
        observed = {
            "file_id": material.file_id,
            "pe_machine": material.pe_machine,
            "pe_timestamp": material.pe_timestamp,
            "size_of_image": material.size_of_image,
        }
        if expected.get(name) != observed[name]:
            _fail(relation)


def _validate_predecessor(
    expected_profile_hash: object,
    material: PredecessorProfileMaterial,
    expected_schema_hash: str,
) -> None:
    relation = RELATIONS[0]
    if material.schema_sha256 != expected_schema_hash or sha256_bytes(material.schema_raw) != expected_schema_hash:
        _fail(relation)
    schema = load_json_bytes(material.schema_raw, canonical=False)
    profile = load_json_bytes(material.raw, canonical=True)
    if type(schema) is not dict or type(profile) is not dict:
        _fail(relation)
    FixedDraft202012Validator(schema).validate(profile)
    if expected_profile_hash != sha256_bytes(material.raw):
        _fail(relation)


def validate_static_relations(
    profile: Mapping[str, object],
    profile_raw: bytes,
    material: StaticMaterialBundle,
    *,
    predecessor_schema_hashes: tuple[str, str, str],
) -> tuple[str, ...]:
    """Verify byte relations and consistency-check, but do not attest platform metadata."""

    if tuple(profile.get("semantic_relations", ())) != RELATIONS:
        raise RuntimeProfileError("semantic relation execution list is not exact")
    if type(predecessor_schema_hashes) is not tuple or len(predecessor_schema_hashes) != 3:
        raise RuntimeProfileError("predecessor schema pin tuple is not exact")

    for expected, observed, schema_hash in zip(
        (
            profile["v0_1_profile_sha256"],
            profile["v0_2_profile_sha256"],
            profile["v0_3_profile_sha256"],
        ),
        material.predecessors,
        predecessor_schema_hashes,
        strict=True,
    ):
        _validate_predecessor(expected, observed, schema_hash)

    package = _mapping(profile["package_closure"], "package closure")
    _match_artifact(package["runtime_files_manifest"], material.runtime_files_manifest, RELATIONS[1])
    verify_manifest_material(
        material.runtime_files_manifest.raw,
        material.runtime_files,
        expected_rows=len(material.runtime_files),
    )

    effective_entries = verify_manifest_material(
        material.effective_package_manifest_raw,
        material.effective_package_files,
        expected_rows=5,
    )
    expected_names = tuple(package["effective_rows"])
    if tuple(effective_entries) != expected_names:
        _fail(RELATIONS[9])
    expected_raws = (
        material.runtime_files_manifest.raw,
        material.predecessors[0].raw,
        material.predecessors[1].raw,
        material.predecessors[2].raw,
        profile_raw,
    )
    if any(material.effective_package_files[name] != raw for name, raw in zip(expected_names, expected_raws, strict=True)):
        _fail(RELATIONS[9])
    if expected_names[0] != material.runtime_files_manifest.virtual_path:
        _fail(RELATIONS[1])

    guard = _mapping(profile["bootstrap_guard"], "bootstrap guard")
    for name, observed in zip(PROVENANCE_NAMES, material.provenance_chain, strict=True):
        if name in {"binary", "loaded_image"}:
            if type(observed) is not BinaryMaterial:
                _fail(RELATIONS[2])
            _match_binary(guard[name], observed, RELATIONS[2])
        else:
            _match_artifact(guard[name], observed, RELATIONS[2])
    binary = material.provenance_chain[-2]
    loaded = material.provenance_chain[-1]
    if (
        type(binary) is not BinaryMaterial
        or type(loaded) is not BinaryMaterial
        or binary.file_id != loaded.file_id
    ):
        _fail(RELATIONS[3])

    platform = _mapping(profile["platform_binding"], "platform binding")
    _match_artifact(platform["platform_manifest"], material.platform_manifest, RELATIONS[4])
    _match_artifact(platform["loaded_pe_manifest"], material.loaded_pe_manifest, RELATIONS[4])
    process = _mapping(profile["process_creation_policy"], "process creation policy")
    atomic = _mapping(profile["atomic_root_policy"], "atomic root policy")
    expected_imports = (process["api"], atomic["direct_import"])
    for name, observed, direct_import in zip(
        ("kernel32", "ntdll"), material.system_images, expected_imports, strict=True
    ):
        expected = _mapping(platform[name], "system image identity")
        _match_binary(expected, observed, RELATIONS[4])
        if (
            observed.module_name != name
            or observed.volume_serial != expected.get("volume_serial")
            or dict(observed.required_exports) != expected.get("required_exports")
            or observed.direct_import != direct_import
        ):
            _fail(RELATIONS[4])

    semantic_validator = _mapping(profile["semantic_validator"], "semantic validator")
    _match_artifact(
        semantic_validator["implementation"], material.semantic_validator, RELATIONS[2]
    )
    return BYTE_VERIFIED_RELATIONS


def validate_precreation_relations(
    profile: Mapping[str, object],
    observation: PrecreationObservation,
    *,
    evidence_handles: tuple[HandleObservation, ...],
    evidence_raw: bytes,
    evidence_sha256: str,
) -> tuple[str, ...]:
    process = _mapping(profile["process_creation_policy"], "process creation policy")
    expected = tuple(
        (row["role"], row["kind"], row["access"])
        for row in process["ordered_handles"]
    )
    actual = tuple((row.role, row.kind, row.access) for row in observation.handles)
    if (
        actual != expected
        or evidence_handles != observation.handles
        or sha256_bytes(evidence_raw) != evidence_sha256
    ):
        _fail(RELATIONS[5])
    locators = tuple(row.locator for row in observation.handles)
    if observation.guard_locators != locators:
        _fail(RELATIONS[7])
    atomic = _mapping(profile["atomic_root_policy"], "atomic root policy")
    if (
        observation.retained_root_file_id != observation.duplicate_root_file_id
        or atomic["duplicate_same_object_required"] is not True
    ):
        _fail(RELATIONS[8])
    return OFFLINE_PRECREATION_RELATIONS


def validate_postcreation_relation(
    observation: PostcreationObservation,
    *,
    expected_evidence_sha256: str,
) -> tuple[str, ...]:
    if (
        observation.launch_evidence_sha256 != expected_evidence_sha256
        or observation.actual_verifier_pid != observation.current_verifier_pid
        or observation.success_policy_id != "createprocess-success-bound-v0.4"
    ):
        _fail(RELATIONS[6])
    return OFFLINE_POSTCREATION_RELATIONS

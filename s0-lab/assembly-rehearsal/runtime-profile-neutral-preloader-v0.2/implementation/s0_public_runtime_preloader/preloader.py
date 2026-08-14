"""Offline neutral-preloader construction with no live authority surface."""

from __future__ import annotations

from dataclasses import dataclass

from .canonical import sha256_bytes
from .errors import RuntimeProfileError
from .evidence import (
    OfflineLaunchEvidenceDiagnostic,
    LaunchMaterialSet,
    OfflineAdmissionDiagnostic,
    build_offline_admission_diagnostic,
    build_offline_launch_evidence_diagnostic,
    build_launch_identity,
    load_launch_control,
)
from .profile import validate_runtime_profile_candidate
from .semantic import (
    BYTE_VERIFIED_RELATIONS,
    DEFERRED_STATIC_RELATIONS,
    OFFLINE_PRECREATION_RELATIONS,
    ArtifactMaterial,
    HandleObservation,
    PostcreationObservation,
    PrecreationObservation,
    StaticMaterialBundle,
    validate_precreation_relations,
)


@dataclass(frozen=True)
class OrderedHandleLocators:
    admission_read: str
    commit_request_write: str
    commit_reply_read: str
    output_root: str
    preloader_process: str

    def ordered(self) -> tuple[str, str, str, str, str]:
        return (
            self.admission_read,
            self.commit_request_write,
            self.commit_reply_read,
            self.output_root,
            self.preloader_process,
        )


@dataclass(frozen=True)
class OfflinePreloaderInputs:
    run_nonce: str
    handle_locators: OrderedHandleLocators
    guard_locators: tuple[str, ...]
    retained_root_file_id: str
    duplicate_root_file_id: str

    def __post_init__(self) -> None:
        if type(self.handle_locators) is not OrderedHandleLocators:
            raise RuntimeProfileError("preloader locator input is not exact")
        if type(self.guard_locators) is not tuple or len(self.guard_locators) != 5:
            raise RuntimeProfileError("guard locator input is not exact")


@dataclass(frozen=True)
class OfflinePreparedLaunch:
    api: str
    application_path: str
    command_line: str
    environment_block: tuple[str, ...]
    current_directory: str
    creation_flags_numeric: int
    startupinfoex_dwflags: int
    b_inherit_handles: bool
    attribute_count: int
    attribute_id_numeric: int
    application_name_policy_id: str
    command_line_policy_id: str
    environment_policy_id: str
    current_directory_policy_id: str
    security_attributes_policy_id: str
    token_policy_id: str
    mitigation_policy_id: str
    job_policy_id: str
    attribute_storage_lifetime: str
    ordered_handle_values: tuple[int, int, int, int, int]
    handle_array_bytes_x64: int
    evidence: OfflineLaunchEvidenceDiagnostic
    runtime_profile_sha256: str
    effective_runtime_package_sha256: str
    static_relations: tuple[str, ...]
    deferred_static_relations: tuple[str, ...]
    offline_precreation_relations: tuple[str, ...]
    candidate_only: bool = True
    native_api_reachable: bool = False

    def __post_init__(self) -> None:
        if self.candidate_only is not True or self.native_api_reachable is not False:
            raise RuntimeProfileError("prepared launch must remain an offline-only candidate")
        if self.static_relations != BYTE_VERIFIED_RELATIONS:
            raise RuntimeProfileError("prepared launch lacks byte relation validation")
        if self.deferred_static_relations != DEFERRED_STATIC_RELATIONS:
            raise RuntimeProfileError("prepared launch deferred relation set is not exact")
        if self.offline_precreation_relations != OFFLINE_PRECREATION_RELATIONS:
            raise RuntimeProfileError("prepared launch offline observation set is incomplete")


class NeutralPreloader:
    """Revalidate raw bytes and construct a deterministic offline plan."""

    __slots__ = ()

    def prepare(
        self,
        *,
        profile_raw: bytes,
        schema_raw: bytes,
        static_material: StaticMaterialBundle,
        inputs: OfflinePreloaderInputs,
    ) -> OfflinePreparedLaunch:
        if type(inputs) is not OfflinePreloaderInputs:
            raise RuntimeProfileError("offline preloader inputs are not exact")
        validated = validate_runtime_profile_candidate(
            profile_raw=profile_raw,
            schema_raw=schema_raw,
            static_material=static_material,
        )
        profile = validated.profile
        process = profile["process_creation_policy"]

        control_raw = static_material.runtime_files.get("runtime/launch-inputs.json")
        if type(control_raw) is not bytes:
            raise RuntimeProfileError("launch control is outside authenticated runtime files")
        control = load_launch_control(control_raw)
        material = LaunchMaterialSet(
            preloader=ArtifactMaterial(
                control.preloader_virtual_path,
                _runtime_file(static_material, control.preloader_virtual_path),
            ),
            application=ArtifactMaterial(
                control.application_virtual_path,
                _runtime_file(static_material, control.application_virtual_path),
            ),
            bootstrap=ArtifactMaterial(
                control.bootstrap_virtual_path,
                _runtime_file(static_material, control.bootstrap_virtual_path),
            ),
            verifier=ArtifactMaterial(
                control.verifier_virtual_path,
                _runtime_file(static_material, control.verifier_virtual_path),
            ),
        )

        identity = build_launch_identity(
            run_nonce=inputs.run_nonce,
            runtime_package_manifest_raw=static_material.effective_package_manifest_raw,
            control=control,
            material=material,
        )
        locators = inputs.handle_locators.ordered()
        handles = tuple(
            HandleObservation(row["role"], row["kind"], row["access"], locator)
            for row, locator in zip(process["ordered_handles"], locators, strict=True)
        )
        evidence = build_offline_launch_evidence_diagnostic(profile, identity, handles)
        observation = PrecreationObservation(
            handles=handles,
            guard_locators=inputs.guard_locators,
            retained_root_file_id=inputs.retained_root_file_id,
            duplicate_root_file_id=inputs.duplicate_root_file_id,
        )
        offline_precreation_relations = validate_precreation_relations(
            profile,
            observation,
            evidence_handles=evidence.handles,
            evidence_raw=evidence.raw,
            evidence_sha256=evidence.sha256,
        )
        values = tuple(int(item.locator[2:], 16) for item in handles)
        if len(values) != 5 or any(value <= 0 or value == 0xFFFFFFFFFFFFFFFF for value in values):
            raise RuntimeProfileError("preloader handle array is invalid")
        return OfflinePreparedLaunch(
            api=process["api"],
            application_path=control.application_path,
            command_line=control.command_line,
            environment_block=control.environment_block,
            current_directory=control.current_directory,
            creation_flags_numeric=int(process["creation_flags_numeric"], 16),
            startupinfoex_dwflags=process["startupinfoex_dwflags"],
            b_inherit_handles=process["b_inherit_handles"],
            attribute_count=process["attribute_count"],
            attribute_id_numeric=int(process["attribute_id_numeric"], 16),
            application_name_policy_id=process["application_name_policy_id"],
            command_line_policy_id=process["command_line_policy_id"],
            environment_policy_id=process["environment_policy_id"],
            current_directory_policy_id=process["current_directory_policy_id"],
            security_attributes_policy_id=process["security_attributes_policy_id"],
            token_policy_id=process["token_policy_id"],
            mitigation_policy_id=process["mitigation_policy_id"],
            job_policy_id=process["job_policy_id"],
            attribute_storage_lifetime=process["attribute_storage_lifetime"],
            ordered_handle_values=values,  # type: ignore[arg-type]
            handle_array_bytes_x64=process["handle_array_bytes_x64"],
            evidence=evidence,
            runtime_profile_sha256=validated.profile_sha256,
            effective_runtime_package_sha256=sha256_bytes(
                static_material.effective_package_manifest_raw
            ),
            static_relations=validated.static_relations,
            deferred_static_relations=validated.deferred_static_relations,
            offline_precreation_relations=offline_precreation_relations,
        )


def _runtime_file(static_material: StaticMaterialBundle, virtual_path: str) -> bytes:
    raw = static_material.runtime_files.get(virtual_path)
    if type(raw) is not bytes:
        raise RuntimeProfileError("launch artifact is outside authenticated runtime files")
    return raw


def prepare_offline_admission_diagnostic(
    *,
    profile_raw: bytes,
    schema_raw: bytes,
    static_material: StaticMaterialBundle,
    inputs: OfflinePreloaderInputs,
    observation: PostcreationObservation,
) -> OfflineAdmissionDiagnostic:
    """Revalidate every raw input and derive all admission claims internally."""

    prepared = NeutralPreloader().prepare(
        profile_raw=profile_raw,
        schema_raw=schema_raw,
        static_material=static_material,
        inputs=inputs,
    )
    validated = validate_runtime_profile_candidate(
        profile_raw=profile_raw,
        schema_raw=schema_raw,
        static_material=static_material,
    )
    return build_offline_admission_diagnostic(
        validated.profile,
        evidence=prepared.evidence,
        observation=observation,
        runtime_profile_v0_4_sha256=prepared.runtime_profile_sha256,
        effective_runtime_package_sha256=prepared.effective_runtime_package_sha256,
    )

"""Data-only validation of a runtime profile candidate.

The returned snapshot is deliberately not a capability or live authority.
Every consumer must revalidate the original profile, schema, and static byte
material in the same operation that prepares candidate output.
"""

from __future__ import annotations

import copy
from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from .canonical import load_json_bytes, require_sha256, sha256_bytes, parse_manifest, verify_manifest_material
from .errors import RuntimeProfileError
from .schema import FixedDraft202012Validator
from .source_audit import NATIVE_API_INVENTORY, validate_native_inventory
from .semantic import (
    BYTE_VERIFIED_RELATIONS,
    DEFERRED_STATIC_RELATIONS,
    StaticMaterialBundle,
    ArtifactMaterial,
    validate_static_relations,
)


RUNTIME_PROFILE_SCHEMA_SHA256 = (
    "3cdcf7e39d39536213f5ab577970f39643b13aa542d854176c213590a16f92dd"
)
PREDECESSOR_SCHEMA_SHA256 = (
    "92943a96249c312d0e2631705a667170d60d22d8e75f2571961ed1f728e934af",
    "e2e96940bbafc6a80987634fe794d700844dbc7d0b48e0e269922f03364fb34f",
    "1404f4981d3d7815e98a6c5d745596f15bb8d50a296410584d03d7ccb11ce3dd",
)
RUNTIME_PROFILE_SCHEMA_ID = (
    "urn:s0:public-assembly:runtime-profile-neutral-preloader:runtime-profile:4"
)
SEMANTIC_VALIDATOR_POLICY_ID = "runtime-profile-v0.4-semantic-relations-validator"


def _freeze(value: object) -> object:
    if isinstance(value, dict):
        return MappingProxyType({key: _freeze(child) for key, child in value.items()})
    if isinstance(value, list):
        return tuple(_freeze(child) for child in value)
    return value


@dataclass(frozen=True)
class ValidatedProfileCandidate:
    """Reviewable data snapshot; explicitly never accepted as authority."""

    profile: Mapping[str, object]
    profile_raw: bytes
    profile_sha256: str
    static_relations: tuple[str, ...]
    deferred_static_relations: tuple[str, ...] = DEFERRED_STATIC_RELATIONS
    candidate_only: bool = True

    def __post_init__(self) -> None:
        if self.candidate_only is not True:
            raise RuntimeProfileError("validated profile result must remain candidate-only")
        if type(self.profile_raw) is not bytes:
            raise RuntimeProfileError("validated profile result lacks exact source bytes")
        require_sha256(self.profile_sha256, "validated candidate profile hash")
        if self.profile_sha256 != sha256_bytes(self.profile_raw):
            raise RuntimeProfileError("validated candidate profile hash is not byte-bound")
        if self.static_relations != BYTE_VERIFIED_RELATIONS:
            raise RuntimeProfileError("validated candidate byte relation set is incomplete")
        if self.deferred_static_relations != DEFERRED_STATIC_RELATIONS:
            raise RuntimeProfileError("validated candidate deferred relation set is not exact")
        object.__setattr__(self, "profile", _freeze(copy.deepcopy(dict(self.profile))))


def validate_runtime_profile_candidate(
    *,
    profile_raw: bytes,
    schema_raw: bytes,
    static_material: StaticMaterialBundle,
) -> ValidatedProfileCandidate:
    """Validate exact static bytes without issuing any reusable authority."""

    if sha256_bytes(schema_raw) != RUNTIME_PROFILE_SCHEMA_SHA256:
        raise RuntimeProfileError("runtime profile schema bytes differ from the frozen pin")
    schema = load_json_bytes(schema_raw, canonical=False)
    profile = load_json_bytes(profile_raw, canonical=True)
    if type(schema) is not dict or type(profile) is not dict:
        raise RuntimeProfileError("schema and profile roots must both be objects")
    if profile.get("schema_id") != RUNTIME_PROFILE_SCHEMA_ID:
        raise RuntimeProfileError("runtime profile schema ID is not exact")
    semantic_validator = profile.get("semantic_validator")
    if not isinstance(semantic_validator, Mapping):
        raise RuntimeProfileError("semantic validator profile object is absent")
    if semantic_validator.get("policy_id") != SEMANTIC_VALIDATOR_POLICY_ID:
        raise RuntimeProfileError("semantic validator policy is not exact")
    FixedDraft202012Validator(schema).validate(profile)
    relations = validate_static_relations(
        profile,
        profile_raw,
        static_material,
        predecessor_schema_hashes=PREDECESSOR_SCHEMA_SHA256,
    )
    if relations != BYTE_VERIFIED_RELATIONS:
        raise RuntimeProfileError("static byte relation execution is incomplete")
    return ValidatedProfileCandidate(
        profile=profile,
        profile_raw=profile_raw,
        profile_sha256=sha256_bytes(profile_raw),
        static_relations=relations,
    )


SUCCESSOR_SCHEMA_SHA256 = "04ae781b7d71e2954378cf7cdf2aa9070634ddc3a25c883ac52fb83ebe139d7e"
SUCCESSOR_MAP_SHA256 = "f6aa0f38ad7eb7bf2715fbc6084c5ce9c05db23eccca1af65956735e1e933623"
_DESIGN_ROOT = "s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-"
_DESIGN_MANIFESTS = (
    (_DESIGN_ROOT + "v0.4/design-package-files.sha256", "abecc3951f29201f24e7fd069865d5a10cf76587b2c1e7c8013ff9226479e589", 6),
    (_DESIGN_ROOT + "v0.5/design-package-files.sha256", "058a8b8bcd8ed2068a6b5c0a8f3c9dc16425f51d8aaaa505b6d6d36f4fab6c98", 7),
    (_DESIGN_ROOT + "v0.5/findclose-amendment-v0.1/amendment-files.sha256", "980144638bb8b16687c22c0f4cea0fe43bf94a63bda4844529670bd9d45a983a", 3),
)
_PREDECESSOR_PROFILE_PINS = (
    "e0f7559d16068cc4cb6589a87fdb2129915ab018a76e41cfc09b4259d543008e",
    "3a0f2fd92629e4a3eb419ab2ae2dbc586bf83ae7152a8b08cfdcabc966028125",
    "9741561972db10c39b824b60364219a07e1e1a440f154b562bae91f864aeb8c5",
    "266087f18cb16ced698fdfc8089a6ca305aac1d5d0278b1ee4c51f23044b3e9e",
)


@dataclass(frozen=True)
class SuccessorProfileMaterial:
    """Supplied bytes for offline checking, never a reusable launch capability."""
    profile_raw: bytes
    schema_raw: bytes
    interface_map_raw: bytes
    design_files: Mapping[str, bytes]
    semantic_validator: ArtifactMaterial
    implementation_manifest_raw: bytes
    implementation_manifest_sha256: str
    implementation_files: Mapping[str, bytes]
    runtime_authority: ArtifactMaterial
    native_sources: Mapping[str, ArtifactMaterial]
    native_binaries: Mapping[str, ArtifactMaterial]
    build_trace: ArtifactMaterial
    import_resolution: Mapping[str, dict[str, tuple[str, str]]]
    crt_imports: Mapping[str, tuple[tuple[str, str], ...]]
    effective_package_manifest_raw: bytes
    effective_package_files: Mapping[str, bytes]


def _successor_design_bytes(material: SuccessorProfileMaterial) -> None:
    files = dict(material.design_files)
    for manifest_path, pin, count in _DESIGN_MANIFESTS:
        raw = files.get(manifest_path)
        if type(raw) is not bytes or sha256_bytes(raw) != pin:
            raise RuntimeProfileError("successor design manifest pin differs")
        rows = parse_manifest(raw, expected_rows=count)
        targets = {path: files.get(path) for path in rows}
        verify_manifest_material(raw, targets, expected_rows=count)
        for path, digest in rows.items():
            if path.endswith(".md"):
                sidecar_path = path[:-3] + ".sha256"
                expected = (digest + "  " + path.rsplit("/", 1)[-1] + "\n").encode("ascii")
                if files.get(sidecar_path) != expected:
                    raise RuntimeProfileError("successor design Markdown sidecar differs")
    acceptance = _DESIGN_ROOT + "v0.5/findclose-amendment-v0.1/control-acceptance-v0.1.md"
    if sha256_bytes(files.get(acceptance)) != "18d9ec532e9d5bbe0f5fb104e58fe696be835c46298c766bf390eb970354bb62":
        raise RuntimeProfileError("accepted amendment control record differs")
    effective = _DESIGN_ROOT + "v0.5/findclose-amendment-v0.1/"
    if (
        files.get(effective + "runtime-profile-v0.5.schema.json") != material.schema_raw
        or files.get(effective + "public-assembly-runtime-profile-neutral-preloader-interface-map-v0.5.json") != material.interface_map_raw
    ):
        raise RuntimeProfileError("effective map/schema mixed with another package")


def _successor_native_bytes(material: SuccessorProfileMaterial) -> None:
    require_sha256(material.implementation_manifest_sha256, "external CONTROL implementation manifest pin")
    if sha256_bytes(material.implementation_manifest_raw) != material.implementation_manifest_sha256:
        raise RuntimeProfileError("corrected implementation source pin differs")
    files = dict(material.implementation_files)
    rows = verify_manifest_material(material.implementation_manifest_raw, files, expected_rows=20)
    if (
        material.runtime_authority.virtual_path not in rows
        or files[material.runtime_authority.virtual_path] != material.runtime_authority.raw
        or material.semantic_validator.virtual_path not in rows
        or files[material.semantic_validator.virtual_path] != material.semantic_validator.raw
    ):
        raise RuntimeProfileError("runtime authority or validator is outside corrected source closure")
    authority = load_json_bytes(material.runtime_authority.raw, canonical=False)
    if authority.get("native_api_inventory") != {
        role: {key: list(values) for key, values in inventory.items()}
        for role, inventory in NATIVE_API_INVENTORY.items()
    }:
        raise RuntimeProfileError("runtime authority API inventory differs")
    trace = load_json_bytes(material.build_trace.raw, canonical=False)
    if (
        trace.get("schema_id") != "S0-RUNTIME-PRELOADER-V0.5-BUILD-TRACE-1"
        or trace.get("effective_interface_map_sha256") != SUCCESSOR_MAP_SHA256
        or trace.get("effective_schema_sha256") != SUCCESSOR_SCHEMA_SHA256
        or trace.get("compiler", {}).get("sha256") != "88c8344236a27a6e727e0a8edc49aaa2690bdc7a9464b9d18cc7abe70a9f1c0d"
        or trace.get("linker", {}).get("sha256") != "ca11e6c45debd34bf652dfe984c5360a531a005ed78bf72852330c9c2590cf0d"
    ):
        raise RuntimeProfileError("native build provenance differs")
    if set(material.native_sources) != {"guard", "preloader", "materializer"} or set(material.native_binaries) != set(material.native_sources):
        raise RuntimeProfileError("native role provenance is incomplete")
    if set(material.import_resolution) != set(material.native_sources) or set(material.crt_imports) != set(material.native_sources):
        raise RuntimeProfileError("native import provenance is incomplete")
    for role in ("guard", "preloader", "materializer"):
        source = material.native_sources[role]
        binary = material.native_binaries[role]
        if type(source) is not ArtifactMaterial or type(binary) is not ArtifactMaterial:
            raise RuntimeProfileError("native provenance material is not exact")
        if source.virtual_path not in rows or files[source.virtual_path] != source.raw:
            raise RuntimeProfileError("native source is outside implementation manifest")
        source_rows = [
            row for row in trace["sources"]
            if row["path"].replace("\\", "/").endswith("/" + source.virtual_path)
        ]
        output_rows = [row for row in trace["outputs"] if row["filename"] == binary.virtual_path.rsplit("/", 1)[-1]]
        if (
            len(source_rows) != 1 or len(output_rows) != 1
            or source_rows[0]["sha256"] != source.sha256 or source_rows[0]["size"] != len(source.raw)
            or output_rows[0]["sha256"] != binary.sha256 or output_rows[0]["size"] != len(binary.raw)
        ):
            raise RuntimeProfileError("actual corrected source/build/binary binding differs")
        validate_native_inventory(
            role, source_raw=source.raw, binary_raw=binary.raw,
            profile_inventory=authority["native_api_inventory"][role],
            import_resolution=dict(material.import_resolution[role]),
            crt_imports=material.crt_imports[role],
        )


def validate_successor_profile_candidate(
    *, profile_raw: bytes, schema_raw: bytes, static_material: StaticMaterialBundle,
    successor: SuccessorProfileMaterial,
) -> ValidatedProfileCandidate:
    """Validate complete historical v0.4, then the accepted v0.5 overlay.

    Loaded identities, platform and concurrency assertions remain deferred.
    Source/PE equality here is an offline byte observation only.
    """
    if type(successor) is not SuccessorProfileMaterial:
        raise RuntimeProfileError("successor material is not exact")
    base = validate_runtime_profile_candidate(
        profile_raw=profile_raw, schema_raw=schema_raw, static_material=static_material,
    )
    if tuple(sha256_bytes(row.raw) for row in static_material.predecessors) + (base.profile_sha256,) != _PREDECESSOR_PROFILE_PINS:
        raise RuntimeProfileError("successor predecessor profile pins differ")
    _successor_design_bytes(successor)
    if sha256_bytes(successor.schema_raw) != SUCCESSOR_SCHEMA_SHA256 or sha256_bytes(successor.interface_map_raw) != SUCCESSOR_MAP_SHA256:
        raise RuntimeProfileError("successor effective schema/map pins differ")
    overlay = load_json_bytes(successor.profile_raw, canonical=True)
    schema = load_json_bytes(successor.schema_raw, canonical=False)
    FixedDraft202012Validator(schema).validate(overlay)
    validator = overlay["semantic_validator"]["implementation"]
    if validator != {"virtual_path": successor.semantic_validator.virtual_path, "sha256": successor.semantic_validator.sha256}:
        raise RuntimeProfileError("successor semantic validator bytes differ")
    _successor_native_bytes(successor)
    package = verify_manifest_material(successor.effective_package_manifest_raw, successor.effective_package_files, expected_rows=6)
    names = ("runtime-files.sha256", "runtime-profile-v0.1.json", "runtime-profile-v0.2.json",
             "runtime-profile-v0.3.json", "runtime-profile-v0.4.json", "runtime-profile-v0.5.json")
    expected = (static_material.runtime_files_manifest.raw, *(row.raw for row in static_material.predecessors), profile_raw, successor.profile_raw)
    if tuple(package) != names or any(successor.effective_package_files[name] != raw for name, raw in zip(names, expected, strict=True)):
        raise RuntimeProfileError("successor complete package composition differs")
    effective = load_json_bytes(profile_raw, canonical=True)
    effective["launch_handle_set_evidence"] = overlay["launch_handle_set_evidence"]
    effective["successor_overlay"] = overlay
    return ValidatedProfileCandidate(
        profile=effective, profile_raw=profile_raw, profile_sha256=base.profile_sha256,
        static_relations=base.static_relations,
    )

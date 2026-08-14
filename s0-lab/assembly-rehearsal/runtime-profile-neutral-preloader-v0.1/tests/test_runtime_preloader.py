from __future__ import annotations

import copy
import dataclasses
import hashlib
import json
import pickle
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve()
PACKAGE_ROOT = HERE.parents[1]
WORKSPACE = next(parent for parent in HERE.parents if (parent / "AGENTS.md").is_file())
IMPLEMENTATION = PACKAGE_ROOT / "implementation"
sys.path.insert(0, str(IMPLEMENTATION))

from s0_public_runtime_preloader.canonical import (  # noqa: E402
    canonical_json_bytes,
    load_json_bytes,
    sha256_bytes,
)
from s0_public_runtime_preloader.errors import (  # noqa: E402
    PlatformGateClosed,
    RuntimeProfileError,
)
from s0_public_runtime_preloader.evidence import (  # noqa: E402
    LaunchIdentity,
    build_admission_frame,
    build_launch_evidence,
)
from s0_public_runtime_preloader.integration import (  # noqa: E402
    ASSEMBLY_CANDIDATE_REPORT_SHA256,
    ASSEMBLY_IMPLEMENTATION_MANIFEST_SHA256,
    RUNTIME_DESIGN_PACKAGE_MANIFEST_SHA256,
    RUNTIME_DESIGN_REREVIEW_RECORD_SHA256,
    AssemblyCandidatePins,
    prepare_assembly_runtime_launch,
)
from s0_public_runtime_preloader.preloader import (  # noqa: E402
    NeutralPreloader,
    OrderedHandleLocators,
    PreloaderInputs,
)
from s0_public_runtime_preloader.profile import (  # noqa: E402
    AuthenticatedRuntimeProfile,
    RUNTIME_PROFILE_SCHEMA_SHA256,
    authenticate_runtime_profile,
)
from s0_public_runtime_preloader.schema import FixedDraft202012Validator  # noqa: E402
from s0_public_runtime_preloader.semantic import (  # noqa: E402
    AdmissionBinding,
    ArtifactBinding,
    HandleBinding,
    PackageRow,
    RELATIONS,
    SemanticEvidence,
    SystemImageBinding,
    validate_semantic_relations,
)
from s0_public_runtime_preloader.source_audit import audit_bounded_source  # noqa: E402


SCHEMA_PATH = (
    WORKSPACE
    / "s0-lab"
    / "control"
    / "assembly-rehearsal"
    / "runtime-profile-neutral-preloader-v0.4"
    / "runtime-profile-v0.4.schema.json"
)
SCHEMA_RAW = SCHEMA_PATH.read_bytes()
SCHEMA = json.loads(SCHEMA_RAW)


def _merge(left: object, right: object) -> object:
    if left is None:
        return copy.deepcopy(right)
    if right is None:
        return copy.deepcopy(left)
    if isinstance(left, dict) and isinstance(right, dict):
        result = copy.deepcopy(left)
        for key, value in right.items():
            result[key] = _merge(result.get(key), value)
        return result
    return copy.deepcopy(right)


def _resolve(schema: dict[str, object]) -> dict[str, object]:
    reference = schema.get("$ref")
    if reference is None:
        return schema
    assert isinstance(reference, str) and reference.startswith("#/")
    node: object = SCHEMA
    for token in reference[2:].split("/"):
        assert isinstance(node, dict)
        node = node[token]
    assert isinstance(node, dict)
    return node


def _sample(schema: dict[str, object]) -> object:
    if "$ref" in schema or "allOf" in schema:
        schema = _combined(schema)
    result: object = None
    if "const" in schema:
        result = copy.deepcopy(schema["const"])
    elif "enum" in schema:
        choices = schema["enum"]
        assert isinstance(choices, list) and choices
        result = copy.deepcopy(choices[0])
    else:
        kind = schema.get("type")
        if kind == "object" or "properties" in schema:
            properties = schema.get("properties", {})
            assert isinstance(properties, dict)
            result = {
                name: _sample(properties[name])
                for name in schema.get("required", [])
            }
        elif kind == "array":
            result = []
        elif kind == "string":
            pattern = schema.get("pattern")
            choices = {
                "^[a-z0-9][a-z0-9._-]{0,127}$": "profile-v0.4",
                "^[0-9a-f]{32}$": "b" * 32,
                "^0x[0-9a-f]{8}$": "0x00000001",
                "^0x[0-9a-f]{16}$": "0x0000000000000001",
                "^[0-9a-f]{64}$": "a" * 64,
                "^[ -~]{1,256}$": "1",
                "^[A-Za-z0-9._/-]+$": "a",
            }
            result = choices.get(pattern, "a")
        elif kind == "integer":
            result = schema.get("minimum", 0)
        elif kind == "boolean":
            result = False
        elif kind == "null":
            result = None
    return result


def _combined(schema: dict[str, object]) -> dict[str, object]:
    result: dict[str, object] = {}
    if "$ref" in schema:
        result = copy.deepcopy(_combined(_resolve(schema)))
    own = {key: value for key, value in schema.items() if key not in {"$ref", "allOf"}}
    prior_required = list(result.get("required", []))
    result = _merge(result, own)  # type: ignore[assignment]
    if "required" in own:
        result["required"] = list(dict.fromkeys(prior_required + list(own["required"])))
    for nested in schema.get("allOf", []):
        assert isinstance(nested, dict)
        if "not" not in nested:
            addition = _combined(nested)
            prior_required = list(result.get("required", []))
            result = _merge(result, addition)  # type: ignore[assignment]
            if "required" in addition:
                result["required"] = list(
                    dict.fromkeys(prior_required + list(addition["required"]))
                )
    return result


def _set_path(root: object, path: tuple[object, ...], value: object) -> None:
    node = root
    for token in path[:-1]:
        node = node[token]  # type: ignore[index]
    node[path[-1]] = value  # type: ignore[index]


def _del_path(root: object, path: tuple[object, ...]) -> None:
    node = root
    for token in path[:-1]:
        node = node[token]  # type: ignore[index]
    del node[path[-1]]  # type: ignore[index]


def _object_paths(
    schema: dict[str, object],
    instance: object,
    path: tuple[object, ...] = (),
) -> list[tuple[tuple[object, ...], dict[str, object], dict[str, object]]]:
    combined = _combined(schema)
    result: list[tuple[tuple[object, ...], dict[str, object], dict[str, object]]] = []
    if isinstance(instance, dict):
        result.append((path, combined, instance))
        properties = combined.get("properties", {})
        assert isinstance(properties, dict)
        for key, value in instance.items():
            child = properties.get(key)
            if isinstance(child, dict):
                result.extend(_object_paths(child, value, path + (key,)))
    return result


def _const_paths(
    schema: dict[str, object],
    instance: object,
    path: tuple[object, ...] = (),
) -> list[tuple[tuple[object, ...], object]]:
    combined = _combined(schema)
    result: list[tuple[tuple[object, ...], object]] = []
    if "const" in combined:
        result.append((path, combined["const"]))
    if isinstance(instance, dict):
        properties = combined.get("properties", {})
        assert isinstance(properties, dict)
        for key, value in instance.items():
            child = properties.get(key)
            if isinstance(child, dict):
                result.extend(_const_paths(child, value, path + (key,)))
    return result


def _profile() -> dict[str, object]:
    profile = _sample(SCHEMA)
    assert isinstance(profile, dict)
    profile["package_closure"]["runtime_files_manifest"]["virtual_path"] = "runtime-files.sha256"
    profile["semantic_validator"]["implementation"]["virtual_path"] = (
        "s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.1/"
        "implementation/s0_public_runtime_preloader/semantic.py"
    )
    return profile


def _artifact(value: dict[str, object]) -> ArtifactBinding:
    return ArtifactBinding(value["virtual_path"], value["sha256"])


def _handles(profile: dict[str, object]) -> tuple[HandleBinding, ...]:
    rows = profile["process_creation_policy"]["ordered_handles"]
    return tuple(
        HandleBinding(row["role"], row["kind"], row["access"], f"0x{index + 1:016x}")
        for index, row in enumerate(rows)
    )


def _semantic_evidence(profile: dict[str, object], profile_hash: str) -> SemanticEvidence:
    guard = profile["bootstrap_guard"]
    chain_names = (
        "source",
        "build_recipe",
        "compiler",
        "linker",
        "import_manifest",
        "crt_import_manifest",
        "binary",
        "loaded_image",
    )
    chain = tuple(_artifact(guard[name]) for name in chain_names)
    platform = profile["platform_binding"]
    process = profile["process_creation_policy"]
    atomic = profile["atomic_root_policy"]
    images = (
        SystemImageBinding(
            platform["kernel32"]["virtual_path"],
            platform["kernel32"]["sha256"],
            "kernel32",
            platform["kernel32"]["file_id"],
            process["api"],
        ),
        SystemImageBinding(
            platform["ntdll"]["virtual_path"],
            platform["ntdll"]["sha256"],
            "ntdll",
            platform["ntdll"]["file_id"],
            atomic["direct_import"],
        ),
    )
    handles = _handles(profile)
    evidence_hash = "c" * 64
    package = profile["package_closure"]
    manifest = _artifact(package["runtime_files_manifest"])
    hashes = (
        manifest.sha256,
        profile["v0_1_profile_sha256"],
        profile["v0_2_profile_sha256"],
        profile["v0_3_profile_sha256"],
        profile_hash,
    )
    package_rows = tuple(
        PackageRow(path, digest)
        for path, digest in zip(package["effective_rows"], hashes)
    )
    return SemanticEvidence(
        predecessor_profile_hashes=(
            profile["v0_1_profile_sha256"],
            profile["v0_2_profile_sha256"],
            profile["v0_3_profile_sha256"],
        ),
        runtime_files_manifest=manifest,
        provenance_chain=chain,
        guard_binary_file_id=guard["binary"]["file_id"],
        guard_loaded_image_file_id=guard["loaded_image"]["file_id"],
        system_images=images,
        launch_handles=handles,
        launch_evidence_sha256=evidence_hash,
        admission=AdmissionBinding(evidence_hash, 1234, "createprocess-success-bound-v0.4"),
        current_verifier_pid=1234,
        guard_locators=tuple(item.locator for item in handles),
        retained_root_file_id="d" * 32,
        duplicate_root_file_id="d" * 32,
        package_rows=package_rows,
        current_profile_sha256=profile_hash,
        semantic_validator_implementation=_artifact(profile["semantic_validator"]["implementation"]),
    )


def _authority() -> tuple[AuthenticatedRuntimeProfile, dict[str, object], SemanticEvidence]:
    profile = _profile()
    raw = canonical_json_bytes(profile)
    evidence = _semantic_evidence(profile, sha256_bytes(raw))
    authority = authenticate_runtime_profile(
        profile_raw=raw,
        schema_raw=SCHEMA_RAW,
        schema_sha256=RUNTIME_PROFILE_SCHEMA_SHA256,
        semantic_evidence=evidence,
    )
    return authority, profile, evidence


class RuntimeSchemaTests(unittest.TestCase):
    def test_authenticated_schema_and_complete_profile_pass(self) -> None:
        authority, _, _ = _authority()
        self.assertEqual(sha256_bytes(SCHEMA_RAW), RUNTIME_PROFILE_SCHEMA_SHA256)
        self.assertEqual(authority.relations, RELATIONS)
        self.assertEqual(len(authority.profile_sha256), 64)

    def test_every_required_property_deletion_rejects(self) -> None:
        profile = _profile()
        validator = FixedDraft202012Validator(SCHEMA)
        mutations = 0
        for object_path, schema, instance in _object_paths(SCHEMA, profile):
            for key in schema.get("required", []):
                self.assertIn(key, instance)
                mutated = copy.deepcopy(profile)
                _del_path(mutated, object_path + (key,))
                with self.assertRaises(RuntimeProfileError):
                    validator.validate(mutated)
                mutations += 1
        self.assertGreaterEqual(mutations, 180)

    def test_unknown_property_at_every_closed_object_rejects(self) -> None:
        profile = _profile()
        validator = FixedDraft202012Validator(SCHEMA)
        mutations = 0
        for object_path, schema, _ in _object_paths(SCHEMA, profile):
            if schema.get("additionalProperties") is False:
                mutated = copy.deepcopy(profile)
                target = mutated
                for token in object_path:
                    target = target[token]
                target["unexpected"] = False
                with self.assertRaises(RuntimeProfileError):
                    validator.validate(mutated)
                mutations += 1
        self.assertGreaterEqual(mutations, 25)

    def test_every_constant_mutation_rejects(self) -> None:
        profile = _profile()
        validator = FixedDraft202012Validator(SCHEMA)
        mutations = 0
        for path, value in _const_paths(SCHEMA, profile):
            mutated = copy.deepcopy(profile)
            if isinstance(value, bool):
                replacement = not value
            elif isinstance(value, int):
                replacement = value + 1
            elif isinstance(value, list):
                replacement = list(reversed(value)) if len(value) > 1 else ["mutated"]
            else:
                replacement = str(value) + "-mutated"
            _set_path(mutated, path, replacement)
            with self.assertRaises(RuntimeProfileError):
                validator.validate(mutated)
            mutations += 1
        self.assertGreaterEqual(mutations, 100)

    def test_duplicate_and_noncanonical_profile_reject(self) -> None:
        with self.assertRaises(RuntimeProfileError):
            load_json_bytes(b'{"a":1,"a":2}\n', canonical=False)
        with self.assertRaises(RuntimeProfileError):
            load_json_bytes(b'{"a": 1}\n', canonical=True)
        for nonfinite in (b'{"a":NaN}\n', b'{"a":Infinity}\n', b'{"a":-Infinity}\n'):
            with self.assertRaises(RuntimeProfileError):
                load_json_bytes(nonfinite, canonical=False)


class SemanticRelationTests(unittest.TestCase):
    def test_each_relation_has_a_negative_mutation(self) -> None:
        _, profile, evidence = _authority()
        mutations = (
            dataclasses.replace(evidence, predecessor_profile_hashes=("f" * 64,) * 3),
            dataclasses.replace(evidence, runtime_files_manifest=ArtifactBinding("runtime-files.sha256", "f" * 64)),
            dataclasses.replace(evidence, provenance_chain=(ArtifactBinding("changed", "f" * 64),) + evidence.provenance_chain[1:]),
            dataclasses.replace(evidence, guard_loaded_image_file_id="e" * 32),
            dataclasses.replace(evidence, system_images=(dataclasses.replace(evidence.system_images[0], sha256="f" * 64), evidence.system_images[1])),
            dataclasses.replace(evidence, launch_handles=tuple(reversed(evidence.launch_handles))),
            dataclasses.replace(evidence, admission=AdmissionBinding(evidence.launch_evidence_sha256, 1235, "createprocess-success-bound-v0.4")),
            dataclasses.replace(evidence, guard_locators=tuple(reversed(evidence.guard_locators))),
            dataclasses.replace(evidence, duplicate_root_file_id="e" * 32),
            dataclasses.replace(evidence, package_rows=tuple(reversed(evidence.package_rows))),
        )
        self.assertEqual(len(mutations), len(RELATIONS))
        for index, mutation in enumerate(mutations):
            with self.subTest(relation=RELATIONS[index]):
                with self.assertRaises(RuntimeProfileError):
                    validate_semantic_relations(profile, mutation)

    def test_validator_implementation_identity_is_mandatory(self) -> None:
        _, profile, evidence = _authority()
        mutation = dataclasses.replace(
            evidence,
            semantic_validator_implementation=ArtifactBinding("changed", "f" * 64),
        )
        with self.assertRaises(RuntimeProfileError):
            validate_semantic_relations(profile, mutation)


class NeutralPreloaderTests(unittest.TestCase):
    def _inputs(self, profile: dict[str, object]) -> PreloaderInputs:
        return PreloaderInputs(
            application_path=r"C:\runtime\python.exe",
            command_line='"C:\\runtime\\python.exe" -I -S -B verifier.py',
            environment_block=("SYSTEMROOT=C:\\Windows", "WINDIR=C:\\Windows"),
            current_directory=r"C:\runtime",
            handle_locators=OrderedHandleLocators(
                "0x0000000000000001",
                "0x0000000000000002",
                "0x0000000000000003",
                "0x0000000000000004",
                "0x0000000000000005",
            ),
            identity=LaunchIdentity(
                run_nonce="1" * 64,
                preloader_image_sha256="2" * 64,
                runtime_package_sha256="3" * 64,
                application_virtual_path="runtime/python.exe",
                application_sha256="4" * 64,
                bootstrap_virtual_path="runtime/bootstrap.py",
                bootstrap_sha256="5" * 64,
                verifier_virtual_path="runtime/verifier.py",
                verifier_sha256="6" * 64,
            ),
        )

    def test_exact_plan_and_evidence_are_deterministic(self) -> None:
        authority, profile, _ = _authority()
        inputs = self._inputs(profile)
        first = NeutralPreloader().prepare(authority, inputs)
        second = NeutralPreloader().prepare(authority, inputs)
        self.assertEqual(first, second)
        self.assertEqual(first.api, "kernel32.dll!CreateProcessW")
        self.assertEqual(first.creation_flags_numeric, 0x08080404)
        self.assertEqual(first.attribute_id_numeric, 0x00020002)
        self.assertEqual(first.ordered_handle_values, (1, 2, 3, 4, 5))
        self.assertEqual(first.handle_array_bytes_x64, 40)
        self.assertTrue(first.evidence.raw.endswith(b"\n"))
        self.assertEqual(hashlib.sha256(first.evidence.raw).hexdigest(), first.evidence.sha256)
        with self.assertRaises(PlatformGateClosed):
            first.invoke_native_process_creation()

    def test_admission_frame_excludes_locator_values(self) -> None:
        authority, profile, _ = _authority()
        launch = NeutralPreloader().prepare(authority, self._inputs(profile))
        frame = build_admission_frame(
            profile,
            evidence=launch.evidence,
            actual_verifier_pid=1234,
            runtime_profile_v0_4_sha256=authority.profile_sha256,
            effective_runtime_package_sha256="7" * 64,
        )
        self.assertNotIn(b"0x0000000000000001", frame.raw)
        self.assertNotIn(b"locator", frame.raw)
        self.assertLessEqual(len(frame.raw), 8192)

    def test_locator_reorder_or_duplicate_rejects(self) -> None:
        _, profile, _ = _authority()
        handles = _handles(profile)
        with self.assertRaises(RuntimeProfileError):
            build_launch_evidence(profile, self._inputs(profile).identity, tuple(reversed(handles)))
        duplicate = dataclasses.replace(handles[-1], locator=handles[0].locator)
        with self.assertRaises(RuntimeProfileError):
            build_launch_evidence(profile, self._inputs(profile).identity, handles[:-1] + (duplicate,))

    def test_exact_assembly_pin_bridge(self) -> None:
        authority, profile, _ = _authority()
        pins = AssemblyCandidatePins(
            ASSEMBLY_IMPLEMENTATION_MANIFEST_SHA256,
            ASSEMBLY_CANDIDATE_REPORT_SHA256,
            RUNTIME_DESIGN_PACKAGE_MANIFEST_SHA256,
            RUNTIME_DESIGN_REREVIEW_RECORD_SHA256,
        )
        launch = prepare_assembly_runtime_launch(
            pins=pins,
            authority=authority,
            inputs=self._inputs(profile),
        )
        self.assertEqual(launch.runtime_profile_sha256, authority.profile_sha256)
        pinned_files = (
            (
                WORKSPACE / "s0-lab/assembly-rehearsal/public-end-to-end-v0.1/verification/implementation-files.sha256",
                ASSEMBLY_IMPLEMENTATION_MANIFEST_SHA256,
            ),
            (
                WORKSPACE / "s0-lab/assembly-rehearsal/public-end-to-end-v0.1/verification/public-end-to-end-assembly-rehearsal-implementation-candidate-report-v0.1.md",
                ASSEMBLY_CANDIDATE_REPORT_SHA256,
            ),
            (
                WORKSPACE / "s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/design-package-files.sha256",
                RUNTIME_DESIGN_PACKAGE_MANIFEST_SHA256,
            ),
            (
                WORKSPACE / "s0-lab/reviews/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/v0.4-independent-rereview-result-preservation-record-v0.1.md",
                RUNTIME_DESIGN_REREVIEW_RECORD_SHA256,
            ),
        )
        for path, expected in pinned_files:
            self.assertEqual(sha256_bytes(path.read_bytes()), expected)
        with self.assertRaises(RuntimeProfileError):
            AssemblyCandidatePins(
                "f" * 64,
                ASSEMBLY_CANDIDATE_REPORT_SHA256,
                RUNTIME_DESIGN_PACKAGE_MANIFEST_SHA256,
                RUNTIME_DESIGN_REREVIEW_RECORD_SHA256,
            )

    def test_authority_is_private_and_immutable(self) -> None:
        authority, _, _ = _authority()
        with self.assertRaises(RuntimeProfileError):
            AuthenticatedRuntimeProfile(object(), {}, "a" * 64, RELATIONS)
        with self.assertRaises(RuntimeProfileError):
            authority.profile_sha256 = "f" * 64
        with self.assertRaises(TypeError):
            copy.copy(authority)
        with self.assertRaises(TypeError):
            copy.deepcopy(authority)
        with self.assertRaises(TypeError):
            pickle.dumps(authority)
        forged = object.__new__(AuthenticatedRuntimeProfile)
        object.__setattr__(forged, "_sealed", True)
        with self.assertRaises(RuntimeProfileError):
            NeutralPreloader().prepare(forged, self._inputs(_profile()))

    def test_candidate_source_has_no_native_or_process_authority(self) -> None:
        checked = audit_bounded_source(IMPLEMENTATION / "s0_public_runtime_preloader")
        self.assertGreaterEqual(len(checked), 8)


if __name__ == "__main__":
    unittest.main()

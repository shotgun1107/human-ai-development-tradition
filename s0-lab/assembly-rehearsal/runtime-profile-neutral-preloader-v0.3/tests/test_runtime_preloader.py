from __future__ import annotations

import copy
import dataclasses
import hashlib
import json
import sys
import unittest
from collections.abc import Mapping
from pathlib import Path


HERE = Path(__file__).resolve()
PACKAGE_ROOT = HERE.parents[1]
WORKSPACE = next(parent for parent in HERE.parents if (parent / "AGENTS.md").is_file())
IMPLEMENTATION = PACKAGE_ROOT / "implementation"
SOURCE_ROOT = IMPLEMENTATION / "s0_public_runtime_preloader"
sys.path.insert(0, str(IMPLEMENTATION))

import s0_public_runtime_preloader as public_api  # noqa: E402
from s0_public_runtime_preloader.canonical import (  # noqa: E402
    canonical_json_bytes,
    load_json_bytes,
    sha256_bytes,
)
from s0_public_runtime_preloader.errors import RuntimeProfileError  # noqa: E402
from s0_public_runtime_preloader.evidence import (  # noqa: E402
    LaunchMaterialSet,
)
from s0_public_runtime_preloader.integration import (  # noqa: E402
    AssemblyArtifactBundle,
    prepare_assembly_runtime_launch,
    validate_assembly_artifact_bundle,
)
from s0_public_runtime_preloader.preloader import (  # noqa: E402
    NeutralPreloader,
    OfflinePreloaderInputs,
    OrderedHandleLocators,
    prepare_offline_admission_diagnostic,
)
from s0_public_runtime_preloader.profile import (  # noqa: E402
    PREDECESSOR_SCHEMA_SHA256,
    RUNTIME_PROFILE_SCHEMA_SHA256,
    ValidatedProfileCandidate,
    validate_runtime_profile_candidate,
)
from s0_public_runtime_preloader.schema import FixedDraft202012Validator  # noqa: E402
from s0_public_runtime_preloader.semantic import (  # noqa: E402
    ArtifactMaterial,
    BinaryMaterial,
    HandleObservation,
    BYTE_VERIFIED_RELATIONS,
    DEFERRED_STATIC_RELATIONS,
    OFFLINE_POSTCREATION_RELATIONS,
    RELATIONS,
    PostcreationObservation,
    PrecreationObservation,
    PredecessorProfileMaterial,
    StaticMaterialBundle,
    SystemImageMaterial,
    validate_postcreation_relation,
    validate_precreation_relations,
)
from s0_public_runtime_preloader.source_audit import (  # noqa: E402
    inspect_source_structure,
    inspect_source_text,
)


SCHEMA_PATHS = tuple(
    WORKSPACE
    / "s0-lab"
    / "control"
    / "assembly-rehearsal"
    / f"runtime-profile-neutral-preloader-v0.{index}"
    / f"runtime-profile-v0.{index}.schema.json"
    for index in range(1, 5)
)
SCHEMA_RAWS = tuple(path.read_bytes() for path in SCHEMA_PATHS)
SCHEMAS = tuple(json.loads(raw) for raw in SCHEMA_RAWS)
SCHEMA_RAW = SCHEMA_RAWS[3]
SCHEMA = SCHEMAS[3]


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


def _resolve(schema: dict[str, object], root_schema: dict[str, object]) -> dict[str, object]:
    reference = schema.get("$ref")
    if reference is None:
        return schema
    assert isinstance(reference, str) and reference.startswith("#/")
    node: object = root_schema
    for token in reference[2:].split("/"):
        assert isinstance(node, dict)
        node = node[token]
    assert isinstance(node, dict)
    return node


def _combined(schema: dict[str, object], root_schema: dict[str, object]) -> dict[str, object]:
    result: dict[str, object] = {}
    if "$ref" in schema:
        result = copy.deepcopy(_combined(_resolve(schema, root_schema), root_schema))
    own = {key: value for key, value in schema.items() if key not in {"$ref", "allOf"}}
    prior_required = list(result.get("required", []))
    result = _merge(result, own)  # type: ignore[assignment]
    if "required" in own:
        result["required"] = list(dict.fromkeys(prior_required + list(own["required"])))
    for nested in schema.get("allOf", []):
        assert isinstance(nested, dict)
        if "not" not in nested:
            addition = _combined(nested, root_schema)
            prior_required = list(result.get("required", []))
            result = _merge(result, addition)  # type: ignore[assignment]
            if "required" in addition:
                result["required"] = list(
                    dict.fromkeys(prior_required + list(addition["required"]))
                )
    return result


_PATTERN_SAMPLES = {
    "^[a-z0-9][a-z0-9._-]{0,127}$": "profile-v0.4",
    "^[0-9a-f]{32}$": "b" * 32,
    "^0x[0-9a-f]{8}$": "0x00000001",
    "^0x[0-9a-f]{16}$": "0x0000000000000001",
    "^[0-9a-f]{64}$": "a" * 64,
    "^[ -~]{1,256}$": "1",
    "^[A-Za-z0-9._/-]+$": "runtime/file.bin",
    "^[A-Z0-9][A-Z0-9._-]*$": "PROFILE",
    "^[A-Za-z0-9._-]+\\.[Dd][Ll][Ll]$": "kernel32.dll",
    "^[A-Za-z0-9][A-Za-z0-9._/-]*$": "runtime/file.bin",
    "^[A-Za-z_][A-Za-z0-9_]*(?:\\.[A-Za-z_][A-Za-z0-9_]*)*$": "module",
    "^runtime(?:/[A-Za-z0-9][A-Za-z0-9._/-]*)?$": "runtime",
    "^runtime/[A-Za-z0-9][A-Za-z0-9._/-]*$": "runtime/file.bin",
    "^(?:runtime|system32)/[A-Za-z0-9][A-Za-z0-9._/-]*$": "runtime/file.bin",
    "^3\\.12\\.[0-9]+$": "3.12.10",
    "\\.pyd$": "runtime/guard.pyd",
}


def _sample(schema: dict[str, object], root_schema: dict[str, object]) -> object:
    if "$ref" in schema or "allOf" in schema:
        schema = _combined(schema, root_schema)
    if "oneOf" in schema:
        choices = schema["oneOf"]
        assert isinstance(choices, list) and choices and isinstance(choices[0], dict)
        schema = _merge(schema, _combined(choices[0], root_schema))  # type: ignore[assignment]
    if "const" in schema:
        return copy.deepcopy(schema["const"])
    if "enum" in schema:
        choices = schema["enum"]
        assert isinstance(choices, list) and choices
        return copy.deepcopy(choices[0])
    kind = schema.get("type")
    if kind == "object" or "properties" in schema:
        properties = schema.get("properties", {})
        assert isinstance(properties, dict)
        return {name: _sample(properties[name], root_schema) for name in schema.get("required", [])}
    if kind == "array":
        prefix = schema.get("prefixItems", [])
        if prefix:
            assert isinstance(prefix, list)
            return [_sample(child, root_schema) for child in prefix]
        count = max(0, int(schema.get("minItems", 0)))
        item_schema = schema.get("items")
        if count and isinstance(item_schema, dict):
            return [_sample(item_schema, root_schema) for _ in range(count)]
        return []
    if kind == "string":
        return _PATTERN_SAMPLES.get(schema.get("pattern"), "a")
    if kind == "integer":
        return schema.get("minimum", 0)
    if kind == "boolean":
        return False
    if kind == "null":
        return None
    return None


def _predecessor_profile_raws() -> tuple[bytes, bytes, bytes]:
    profiles = [_sample(schema, schema) for schema in SCHEMAS[:3]]
    v1 = profiles[0]
    assert isinstance(v1, dict)
    for module in v1["modules"]:
        if module["origin_kind"] in {"builtin", "frozen"}:
            module["virtual_path"] = None
            module["sha256"] = None
    raws = tuple(canonical_json_bytes(profile) for profile in profiles)
    for raw, schema in zip(raws, SCHEMAS[:3], strict=True):
        value = load_json_bytes(raw, canonical=True)
        FixedDraft202012Validator(schema).validate(value)
    return raws  # type: ignore[return-value]


def _manifest_bytes(material: dict[str, bytes]) -> bytes:
    return b"".join(
        f"{sha256_bytes(raw)}  {path}\n".encode("ascii")
        for path, raw in sorted(material.items())
    )


def _artifact(profile_value: dict[str, object], raw: bytes) -> ArtifactMaterial:
    profile_value["sha256"] = sha256_bytes(raw)
    return ArtifactMaterial(profile_value["virtual_path"], raw)


def _binary(profile_value: dict[str, object], raw: bytes) -> BinaryMaterial:
    profile_value["sha256"] = sha256_bytes(raw)
    return BinaryMaterial(
        profile_value["virtual_path"],
        raw,
        profile_value["file_id"],
        profile_value["pe_machine"],
        profile_value["pe_timestamp"],
        profile_value["size_of_image"],
    )


def _system_image(
    name: str,
    profile_value: dict[str, object],
    raw: bytes,
    direct_import: str,
) -> SystemImageMaterial:
    profile_value["sha256"] = sha256_bytes(raw)
    return SystemImageMaterial(
        profile_value["virtual_path"],
        raw,
        profile_value["file_id"],
        profile_value["pe_machine"],
        profile_value["pe_timestamp"],
        profile_value["size_of_image"],
        name,
        profile_value["volume_serial"],
        tuple(sorted(profile_value["required_exports"].items())),
        direct_import,
    )


def _candidate_material() -> tuple[dict[str, object], bytes, StaticMaterialBundle, LaunchMaterialSet]:
    predecessor_raws = _predecessor_profile_raws()
    profile = _sample(SCHEMA, SCHEMA)
    assert isinstance(profile, dict)
    profile["v0_1_profile_sha256"] = sha256_bytes(predecessor_raws[0])
    profile["v0_2_profile_sha256"] = sha256_bytes(predecessor_raws[1])
    profile["v0_3_profile_sha256"] = sha256_bytes(predecessor_raws[2])

    semantic_path = SOURCE_ROOT / "semantic.py"
    semantic_raw = semantic_path.read_bytes()
    runtime_files = {
        "runtime/bootstrap.py": b"bootstrap-v0.2\n",
        "runtime/launch-inputs.json": canonical_json_bytes(
            {
                "application_path": r"C:\runtime\python.exe",
                "application_virtual_path": "runtime/python.exe",
                "bootstrap_virtual_path": "runtime/bootstrap.py",
                "command_line": '"C:\\runtime\\python.exe" -I -S -B verifier.py',
                "current_directory": r"C:\runtime",
                "environment_block": ["SYSTEMROOT=C:\\Windows", "WINDIR=C:\\Windows"],
                "preloader_virtual_path": "runtime/preloader.exe",
                "verifier_virtual_path": "runtime/verifier.py",
            }
        ),
        "runtime/preloader.exe": b"preloader-candidate-v0.2\n",
        "runtime/python.exe": b"python-candidate-v0.2\n",
        "runtime/semantic.py": semantic_raw,
        "runtime/verifier.py": b"verifier-candidate-v0.2\n",
    }
    runtime_manifest_raw = _manifest_bytes(runtime_files)
    package = profile["package_closure"]
    runtime_manifest_identity = package["runtime_files_manifest"]
    runtime_manifest_identity["virtual_path"] = package["effective_rows"][0]
    runtime_manifest = _artifact(runtime_manifest_identity, runtime_manifest_raw)

    guard = profile["bootstrap_guard"]
    provenance: list[ArtifactMaterial] = []
    for name in ("source", "build_recipe", "compiler", "linker", "import_manifest", "crt_import_manifest"):
        provenance.append(_artifact(guard[name], f"{name}-v0.2\n".encode("ascii")))
    guard_binary_raw = b"guard-binary-v0.2\n"
    guard["loaded_image"]["file_id"] = guard["binary"]["file_id"]
    provenance.append(_binary(guard["binary"], guard_binary_raw))
    provenance.append(_binary(guard["loaded_image"], guard_binary_raw))

    platform = profile["platform_binding"]
    platform_manifest = _artifact(platform["platform_manifest"], b"platform-manifest-v0.2\n")
    loaded_pe_manifest = _artifact(platform["loaded_pe_manifest"], b"loaded-pe-manifest-v0.2\n")
    process = profile["process_creation_policy"]
    atomic = profile["atomic_root_policy"]
    system_images = (
        _system_image("kernel32", platform["kernel32"], b"kernel32-v0.2\n", process["api"]),
        _system_image("ntdll", platform["ntdll"], b"ntdll-v0.2\n", atomic["direct_import"]),
    )
    profile["semantic_validator"]["implementation"]["virtual_path"] = "runtime/semantic.py"
    semantic_validator = _artifact(profile["semantic_validator"]["implementation"], semantic_raw)

    profile_raw = canonical_json_bytes(profile)
    effective_names = tuple(package["effective_rows"])
    effective_files = dict(
        zip(
            effective_names,
            (runtime_manifest_raw, *predecessor_raws, profile_raw),
            strict=True,
        )
    )
    effective_manifest_raw = _manifest_bytes(effective_files)
    predecessors = tuple(
        PredecessorProfileMaterial(raw, schema_raw, schema_hash)
        for raw, schema_raw, schema_hash in zip(
            predecessor_raws, SCHEMA_RAWS[:3], PREDECESSOR_SCHEMA_SHA256, strict=True
        )
    )
    static = StaticMaterialBundle(
        predecessors=predecessors,  # type: ignore[arg-type]
        runtime_files_manifest=runtime_manifest,
        runtime_files=runtime_files,
        effective_package_manifest_raw=effective_manifest_raw,
        effective_package_files=effective_files,
        provenance_chain=tuple(provenance),
        platform_manifest=platform_manifest,
        loaded_pe_manifest=loaded_pe_manifest,
        system_images=system_images,
        semantic_validator=semantic_validator,
    )
    launch = LaunchMaterialSet(
        preloader=ArtifactMaterial("runtime/preloader.exe", runtime_files["runtime/preloader.exe"]),
        application=ArtifactMaterial("runtime/python.exe", runtime_files["runtime/python.exe"]),
        bootstrap=ArtifactMaterial("runtime/bootstrap.py", runtime_files["runtime/bootstrap.py"]),
        verifier=ArtifactMaterial("runtime/verifier.py", runtime_files["runtime/verifier.py"]),
    )
    return profile, profile_raw, static, launch


def _inputs() -> OfflinePreloaderInputs:
    locators = OrderedHandleLocators(
        "0x0000000000000001",
        "0x0000000000000002",
        "0x0000000000000003",
        "0x0000000000000004",
        "0x0000000000000005",
    )
    return OfflinePreloaderInputs(
        run_nonce="1" * 64,
        handle_locators=locators,
        guard_locators=locators.ordered(),
        retained_root_file_id="d" * 32,
        duplicate_root_file_id="d" * 32,
    )


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
    combined = _combined(schema, SCHEMA)
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
    combined = _combined(schema, SCHEMA)
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


def _manifest_targets(path: Path) -> tuple[bytes, dict[str, bytes]]:
    raw = path.read_bytes()
    targets: dict[str, bytes] = {}
    for line in raw[:-1].split(b"\n"):
        _, target = line.decode("ascii").split("  ", 1)
        targets[target] = (WORKSPACE / target).read_bytes()
    return raw, targets


def _assembly_bundle() -> AssemblyArtifactBundle:
    old_root = WORKSPACE / "s0-lab/assembly-rehearsal/public-end-to-end-v0.1/verification"
    design_root = WORKSPACE / "s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4"
    implementation_manifest, implementation_targets = _manifest_targets(
        old_root / "implementation-files.sha256"
    )
    design_manifest, design_targets = _manifest_targets(design_root / "design-package-files.sha256")
    return AssemblyArtifactBundle(
        implementation_manifest_raw=implementation_manifest,
        implementation_targets=implementation_targets,
        candidate_report_raw=(
            old_root / "public-end-to-end-assembly-rehearsal-implementation-candidate-report-v0.1.md"
        ).read_bytes(),
        design_manifest_raw=design_manifest,
        design_targets=design_targets,
        rereview_record_raw=(
            WORKSPACE
            / "s0-lab/reviews/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/"
            "v0.4-independent-rereview-result-preservation-record-v0.1.md"
        ).read_bytes(),
    )


class SchemaFamilyTests(unittest.TestCase):
    def test_all_four_profile_schemas_execute(self) -> None:
        predecessor_raws = _predecessor_profile_raws()
        for raw, schema in zip(predecessor_raws, SCHEMAS[:3], strict=True):
            FixedDraft202012Validator(schema).validate(load_json_bytes(raw, canonical=True))
        profile, raw, static, _ = _candidate_material()
        result = validate_runtime_profile_candidate(
            profile_raw=raw,
            schema_raw=SCHEMA_RAW,
            static_material=static,
        )
        self.assertTrue(result.candidate_only)
        self.assertEqual(result.static_relations, BYTE_VERIFIED_RELATIONS)
        self.assertEqual(result.deferred_static_relations, DEFERRED_STATIC_RELATIONS)
        self.assertEqual(result.profile["profile_id"], profile["profile_id"])

    def test_required_unknown_and_constant_mutation_closure(self) -> None:
        profile, _, _, _ = _candidate_material()
        validator = FixedDraft202012Validator(SCHEMA)
        required = unknown = constants = 0
        for object_path, schema, instance in _object_paths(SCHEMA, profile):
            for key in schema.get("required", []):
                self.assertIn(key, instance)
                mutation = copy.deepcopy(profile)
                _del_path(mutation, object_path + (key,))
                with self.assertRaises(RuntimeProfileError):
                    validator.validate(mutation)
                required += 1
            if schema.get("additionalProperties") is False:
                mutation = copy.deepcopy(profile)
                target = mutation
                for token in object_path:
                    target = target[token]
                target["unexpected"] = False
                with self.assertRaises(RuntimeProfileError):
                    validator.validate(mutation)
                unknown += 1
        for path, value in _const_paths(SCHEMA, profile):
            mutation = copy.deepcopy(profile)
            replacement = not value if isinstance(value, bool) else str(value) + "-mutated"
            _set_path(mutation, path, replacement)
            with self.assertRaises(RuntimeProfileError):
                validator.validate(mutation)
            constants += 1
        self.assertEqual((required, unknown, constants), (185, 28, 106))

    def test_strict_json_and_schema_keyword_edges(self) -> None:
        for raw in (b'{"a":NaN}\n', b'{"a":Infinity}\n', b'{"a":1,"a":2}\n'):
            with self.assertRaises(RuntimeProfileError):
                load_json_bytes(raw, canonical=False)
        with self.assertRaises(RuntimeProfileError):
            FixedDraft202012Validator(
                {"$schema": "https://json-schema.org/draft/2020-12/schema", "anyOf": []}
            )
        micro = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "oneOf": [{"const": 1}, {"const": "1"}],
        }
        FixedDraft202012Validator(micro).validate(1)
        with self.assertRaises(RuntimeProfileError):
            FixedDraft202012Validator(micro).validate(True)
        typed_extra = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "additionalProperties": {"type": "integer"},
            "type": "object",
        }
        FixedDraft202012Validator(typed_extra).validate({"value": 1})
        with self.assertRaises(RuntimeProfileError):
            FixedDraft202012Validator(typed_extra).validate({"value": "1"})

    def test_validator_uses_private_schema_snapshot(self) -> None:
        caller_schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "integer",
        }
        validator = FixedDraft202012Validator(caller_schema)
        caller_schema.clear()
        validator.validate(1)
        with self.assertRaises(RuntimeProfileError):
            validator.validate("not-an-integer")
        nested_schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "properties": {"value": {"type": "integer"}},
            "type": "object",
        }
        nested_validator = FixedDraft202012Validator(nested_schema)
        nested_schema["properties"]["value"]["type"] = "string"
        with self.assertRaises(RuntimeProfileError):
            nested_validator.validate({"value": "not-an-integer"})
        with self.assertRaises(RuntimeProfileError):
            FixedDraft202012Validator(
                {
                    "$schema": "https://json-schema.org/draft/2020-12/schema",
                    "uniqueItems": 1,
                }
            )
        for malformed in (
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "properties": {"value": 1},
            },
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "prefixItems": [1],
            },
        ):
            with self.assertRaises(RuntimeProfileError):
                FixedDraft202012Validator(malformed)


class StaticSemanticTests(unittest.TestCase):
    def test_byte_relations_pass_and_platform_relations_remain_deferred(self) -> None:
        _, raw, static, _ = _candidate_material()
        result = validate_runtime_profile_candidate(
            profile_raw=raw, schema_raw=SCHEMA_RAW, static_material=static
        )
        self.assertEqual(result.static_relations, BYTE_VERIFIED_RELATIONS)
        self.assertEqual(result.deferred_static_relations, DEFERRED_STATIC_RELATIONS)
        self.assertTrue(all(relation not in result.static_relations for relation in DEFERRED_STATIC_RELATIONS))
        self.assertEqual(sha256_bytes(SCHEMA_RAW), RUNTIME_PROFILE_SCHEMA_SHA256)

    def test_each_static_relation_and_validator_has_negative_material(self) -> None:
        _, raw, static, _ = _candidate_material()
        mutations = (
            dataclasses.replace(
                static,
                predecessors=(
                    dataclasses.replace(static.predecessors[0], raw=b"{}\n"),
                    *static.predecessors[1:],
                ),
            ),
            dataclasses.replace(
                static,
                runtime_files_manifest=ArtifactMaterial(
                    static.runtime_files_manifest.virtual_path, b"0" * 64 + b"  runtime/x\n"
                ),
            ),
            dataclasses.replace(
                static,
                provenance_chain=(
                    ArtifactMaterial(static.provenance_chain[0].virtual_path, b"changed\n"),
                    *static.provenance_chain[1:],
                ),
            ),
            dataclasses.replace(
                static,
                provenance_chain=(
                    *static.provenance_chain[:-1],
                    dataclasses.replace(static.provenance_chain[-1], file_id="e" * 32),
                ),
            ),
            dataclasses.replace(
                static,
                system_images=(
                    dataclasses.replace(static.system_images[0], direct_import="kernel32.dll!Other"),
                    static.system_images[1],
                ),
            ),
            dataclasses.replace(
                static,
                effective_package_files={
                    **dict(static.effective_package_files),
                    next(reversed(static.effective_package_files)): b"changed\n",
                },
            ),
            dataclasses.replace(
                static,
                semantic_validator=ArtifactMaterial(
                    static.semantic_validator.virtual_path, b"changed-validator\n"
                ),
            ),
        )
        for mutation in mutations:
            with self.subTest(mutation=type(mutation).__name__):
                with self.assertRaises(RuntimeProfileError):
                    validate_runtime_profile_candidate(
                        profile_raw=raw,
                        schema_raw=SCHEMA_RAW,
                        static_material=mutation,
                    )

    def test_forgeable_result_is_never_accepted_as_authority(self) -> None:
        _, raw, static, launch = _candidate_material()
        forged = ValidatedProfileCandidate(
            {}, b"{}\n", sha256_bytes(b"{}\n"), BYTE_VERIFIED_RELATIONS
        )
        object.__setattr__(forged, "profile_sha256", "f" * 64)
        self.assertFalse(hasattr(public_api, "AuthenticatedRuntimeProfile"))
        self.assertFalse(hasattr(public_api, "SemanticEvidence"))
        result = NeutralPreloader().prepare(
            profile_raw=raw,
            schema_raw=SCHEMA_RAW,
            static_material=static,
            inputs=_inputs(),
        )
        self.assertNotEqual(result.runtime_profile_sha256, forged.profile_sha256)

    def test_static_snapshot_rejects_mutable_export_pair(self) -> None:
        _, raw, static, _ = _candidate_material()
        expected_pair = static.system_images[0].required_exports[0]

        class DeceptivePair(list[str]):
            def __iter__(self):
                return iter(expected_pair)

        object.__setattr__(
            static.system_images[0],
            "required_exports",
            (DeceptivePair(["AttackerExport", "0xdeadbeef"]),),
        )
        with self.assertRaises(RuntimeProfileError):
            NeutralPreloader().prepare(
                profile_raw=raw,
                schema_raw=SCHEMA_RAW,
                static_material=static,
                inputs=_inputs(),
            )


class PreloaderTransactionTests(unittest.TestCase):
    def test_plan_is_deterministic_byte_bound_and_never_live(self) -> None:
        _, raw, static, launch = _candidate_material()
        inputs = _inputs()
        first = NeutralPreloader().prepare(
            profile_raw=raw, schema_raw=SCHEMA_RAW, static_material=static, inputs=inputs
        )
        second = NeutralPreloader().prepare(
            profile_raw=raw, schema_raw=SCHEMA_RAW, static_material=static, inputs=inputs
        )
        self.assertEqual(first, second)
        self.assertTrue(first.candidate_only)
        self.assertFalse(first.native_api_reachable)
        self.assertFalse(hasattr(first, "invoke_native_process_creation"))
        self.assertEqual(first.ordered_handle_values, (1, 2, 3, 4, 5))
        self.assertEqual(first.handle_array_bytes_x64, 40)
        self.assertEqual(first.evidence.sha256, hashlib.sha256(first.evidence.raw).hexdigest())
        self.assertEqual(first.evidence.handles[0].role, "admission-read")
        self.assertIn(b"schema_id=S0-OFFLINE-LAUNCH-EVIDENCE-DIAGNOSTIC-1\n", first.evidence.raw)
        self.assertIn(b"candidate_only=true\n", first.evidence.raw)
        self.assertIn(b"rehearsal_pass=false\n", first.evidence.raw)
        self.assertIn(launch.application.sha256.encode("ascii"), first.evidence.raw)
        self.assertIn(
            sha256_bytes(static.runtime_files["runtime/launch-inputs.json"]).encode("ascii"),
            first.evidence.raw,
        )
        self.assertEqual(first.application_path, r"C:\runtime\python.exe")
        self.assertEqual(first.job_policy_id, "public-assembly-process-job-policy-v0.2")

    def test_launch_artifacts_must_be_runtime_manifest_targets(self) -> None:
        _, raw, static, launch = _candidate_material()
        changed_files = {
            **dict(static.runtime_files),
            launch.application.virtual_path: b"changed-app\n",
        }
        changed_static = dataclasses.replace(
            static,
            runtime_files=changed_files,
        )
        with self.assertRaises(RuntimeProfileError):
            NeutralPreloader().prepare(
                profile_raw=raw,
                schema_raw=SCHEMA_RAW,
                static_material=changed_static,
                inputs=_inputs(),
            )

    def test_launch_inputs_exist_only_in_authenticated_control_bytes(self) -> None:
        _, raw, static, _ = _candidate_material()
        self.assertNotIn("launch_control_virtual_path", OfflinePreloaderInputs.__annotations__)
        changed_control = canonical_json_bytes(
            {
                **load_json_bytes(
                    static.runtime_files["runtime/launch-inputs.json"], canonical=True
                ),
                "command_line": "attacker-selected-command",
            }
        )
        with self.assertRaises(RuntimeProfileError):
            NeutralPreloader().prepare(
                profile_raw=raw,
                schema_raw=SCHEMA_RAW,
                static_material=dataclasses.replace(
                    static,
                    runtime_files={
                        **dict(static.runtime_files),
                        "runtime/launch-inputs.json": changed_control,
                    },
                ),
                inputs=_inputs(),
            )

    def test_stateful_runtime_mapping_cannot_change_after_manifest_check(self) -> None:
        _, raw, static, launch = _candidate_material()
        honest = dict(static.runtime_files)
        changed_control = canonical_json_bytes(
            {
                **load_json_bytes(honest["runtime/launch-inputs.json"], canonical=True),
                "command_line": "attacker-selected-command",
            }
        )
        attacker = {
            **honest,
            "runtime/launch-inputs.json": changed_control,
            launch.application.virtual_path: b"attacker-application\n",
        }

        class SwitchingRuntimeFiles(Mapping[str, bytes]):
            def __getitem__(self, key: str) -> bytes:
                return honest[key]

            def __iter__(self):
                return iter(honest)

            def __len__(self) -> int:
                return len(honest)

            def get(self, key: str, default=None):
                return attacker.get(key, default)

        object.__setattr__(static, "runtime_files", SwitchingRuntimeFiles())
        with self.assertRaises(RuntimeProfileError):
            NeutralPreloader().prepare(
                profile_raw=raw,
                schema_raw=SCHEMA_RAW,
                static_material=static,
                inputs=_inputs(),
            )

    def test_guard_locator_and_root_bindings_reject(self) -> None:
        _, raw, static, launch = _candidate_material()
        inputs = _inputs()
        for mutation in (
            dataclasses.replace(inputs, guard_locators=tuple(reversed(inputs.guard_locators))),
            dataclasses.replace(inputs, duplicate_root_file_id="e" * 32),
        ):
            with self.assertRaises(RuntimeProfileError):
                NeutralPreloader().prepare(
                    profile_raw=raw,
                    schema_raw=SCHEMA_RAW,
                    static_material=static,
                    inputs=mutation,
                )

    def test_all_dynamic_relations_have_negative_observations(self) -> None:
        profile, raw, static, launch = _candidate_material()
        prepared = NeutralPreloader().prepare(
            profile_raw=raw,
            schema_raw=SCHEMA_RAW,
            static_material=static,
            inputs=_inputs(),
        )
        handles = prepared.evidence.handles
        wrong_handle = dataclasses.replace(handles[0], role="changed")
        with self.assertRaises(RuntimeProfileError):
            validate_precreation_relations(
                profile,
                PrecreationObservation(
                    handles=(wrong_handle, *handles[1:]),
                    guard_locators=tuple(item.locator for item in handles),
                    retained_root_file_id="d" * 32,
                    duplicate_root_file_id="d" * 32,
                ),
                evidence_handles=prepared.evidence.handles,
                evidence_raw=prepared.evidence.raw,
                evidence_sha256=prepared.evidence.sha256,
            )
        with self.assertRaises(RuntimeProfileError):
            validate_postcreation_relation(
                PostcreationObservation(prepared.evidence.sha256, 1234, 1235, "createprocess-success-bound-v0.4"),
                expected_evidence_sha256=prepared.evidence.sha256,
            )

    def test_offline_admission_is_locator_free_and_relation_bound(self) -> None:
        profile, raw, static, launch = _candidate_material()
        prepared = NeutralPreloader().prepare(
            profile_raw=raw,
            schema_raw=SCHEMA_RAW,
            static_material=static,
            inputs=_inputs(),
        )
        observation = PostcreationObservation(
            prepared.evidence.sha256,
            1234,
            1234,
            "createprocess-success-bound-v0.4",
        )
        result = prepare_offline_admission_diagnostic(
            profile_raw=raw,
            schema_raw=SCHEMA_RAW,
            static_material=static,
            inputs=_inputs(),
            observation=observation,
        )
        self.assertTrue(result.candidate_only)
        self.assertEqual(
            result.offline_postcreation_relations, OFFLINE_POSTCREATION_RELATIONS
        )
        self.assertNotIn(b"locator", result.raw)
        self.assertNotIn(b"0x0000000000000001", result.raw)
        self.assertIn(b'"candidate_only":true', result.raw)
        self.assertIn(b'"rehearsal_pass":false', result.raw)
        self.assertIn(b'"schema_id":"S0-OFFLINE-ADMISSION-DIAGNOSTIC-1"', result.raw)
        diagnostic_value = load_json_bytes(result.raw, canonical=True)
        self.assertNotEqual(
            diagnostic_value["schema_id"], profile["admission_frame_policy"]["schema_id"]
        )
        self.assertFalse(hasattr(public_api, "build_offline_admission_diagnostic"))
        with self.assertRaises(RuntimeProfileError):
            prepare_offline_admission_diagnostic(
                profile_raw=raw,
                schema_raw=SCHEMA_RAW,
                static_material=static,
                inputs=_inputs(),
                observation=dataclasses.replace(
                    observation, launch_evidence_sha256="f" * 64
                ),
            )

    def test_mutated_observation_source_cannot_enter_admission(self) -> None:
        _, raw, static, _ = _candidate_material()
        prepared = NeutralPreloader().prepare(
            profile_raw=raw,
            schema_raw=SCHEMA_RAW,
            static_material=static,
            inputs=_inputs(),
        )
        observation = PostcreationObservation(
            prepared.evidence.sha256,
            1234,
            1234,
            "createprocess-success-bound-v0.4",
        )
        object.__setattr__(observation, "source", "0x0000000000000001")
        with self.assertRaises(RuntimeProfileError):
            prepare_offline_admission_diagnostic(
                profile_raw=raw,
                schema_raw=SCHEMA_RAW,
                static_material=static,
                inputs=_inputs(),
                observation=observation,
            )


class IntegrationAndDiagnosticTests(unittest.TestCase):
    def test_bridge_authenticates_actual_bytes_and_all_manifest_targets(self) -> None:
        bundle = _assembly_bundle()
        result = validate_assembly_artifact_bundle(bundle)
        self.assertEqual((result.implementation_rows, result.design_rows), (32, 6))
        profile, raw, static, launch = _candidate_material()
        prepared = prepare_assembly_runtime_launch(
            artifacts=bundle,
            profile_raw=raw,
            schema_raw=SCHEMA_RAW,
            static_material=static,
            inputs=_inputs(),
        )
        self.assertTrue(prepared.candidate_only)

    def test_bridge_rejects_each_changed_authority_and_target_byte(self) -> None:
        bundle = _assembly_bundle()
        changes = (
            dataclasses.replace(bundle, implementation_manifest_raw=bundle.implementation_manifest_raw + b"x"),
            dataclasses.replace(bundle, candidate_report_raw=bundle.candidate_report_raw + b"x"),
            dataclasses.replace(bundle, design_manifest_raw=bundle.design_manifest_raw + b"x"),
            dataclasses.replace(bundle, rereview_record_raw=bundle.rereview_record_raw + b"x"),
            dataclasses.replace(
                bundle,
                implementation_targets={
                    **dict(bundle.implementation_targets),
                    next(iter(bundle.implementation_targets)): b"changed\n",
                },
            ),
        )
        for change in changes:
            with self.assertRaises(RuntimeProfileError):
                validate_assembly_artifact_bundle(change)

    def test_source_structure_diagnostic_passes_exact_package(self) -> None:
        sources = {
            path.name: path.read_bytes()
            for path in SOURCE_ROOT.iterdir()
            if path.is_file()
        }
        self.assertEqual(len(inspect_source_structure(sources)), 10)

    def test_dynamic_import_lookup_and_introspection_mutations_reject(self) -> None:
        snippets = (
            b'__import__("ct" + "ypes")\n',
            b'getattr(value, "Create" + "ProcessW")\n',
            b'import importlib\n',
            b'import subprocess as safe\n',
            b'eval("1")\n',
            b'danger = eval\ndanger("1")\n',
            b'loader = __import__\nloader("ctypes")\n',
            b'__loader__.get_data("C:/target")\n',
            b'exc.__traceback__.tb_frame.f_builtins["__import__"]("os").system("calc")\n',
            b'value.__class__.__subclasses__()\n',
        )
        for raw in snippets:
            with self.subTest(raw=raw):
                with self.assertRaises(RuntimeProfileError):
                    inspect_source_text("errors.py", raw)
        with self.assertRaises(RuntimeProfileError):
            inspect_source_text("evidence.py", b"import re as safe\nsafe.compile('x')\n")
        for filename, raw in (
            ("canonical.py", b'import pathlib\npathlib.os.system("calc")\n'),
            ("canonical.py", b'import json\nsafe = json\n'),
            ("canonical.py", b'import json\njson = value\njson.loads("{}")\n'),
            ("canonical.py", b'import json\ndef f(json):\n    return json.loads("{}")\n'),
            ("canonical.py", b'import json\nmatch value:\n    case json:\n        json.loads("{}")\n'),
            ("errors.py", b"from .canonical import json\n"),
            ("source_audit.py", b"from pathlib import Path\nPath('x').open('w')\n"),
            ("errors.py", b"open('x', 'w')\n"),
            ("errors.py", b"value.read_text()\n"),
            ("errors.py", b"value.read_bytes()\n"),
            ("errors.py", b"value.iterdir()\n"),
            ("errors.py", b"value.glob('*')\n"),
            ("errors.py", b"value.rglob('*')\n"),
            ("errors.py", b"value.stat()\n"),
            ("errors.py", b"value.lstat()\n"),
            ("errors.py", b"value.exists()\n"),
            ("errors.py", b"value.resolve()\n"),
            ("errors.py", b"value.is_file()\n"),
            ("errors.py", b"value.walk()\n"),
        ):
            with self.subTest(filename=filename, raw=raw):
                with self.assertRaises(RuntimeProfileError):
                    inspect_source_text(filename, raw)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import copy
import hashlib
import json
import sys
from dataclasses import replace
from pathlib import Path


ROOT = Path(r"C:\Users\SSAFY\AppData\Local\Temp\rpnp04-81a7e8cb\final-test-correction9-v1")
REPO = Path(r"C:\Users\SSAFY\AppData\Local\Temp\cpr01-862b27cd")
IMPLEMENTATION = REPO / "s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.4/implementation"
PACKAGE = ROOT / "production-package"
SCHEMAS = (
    Path(r"C:\Users\SSAFY\Documents\ai-development-tradition\s0-lab\control\assembly-rehearsal\runtime-profile-neutral-preloader-v0.1\runtime-profile-v0.1.schema.json"),
    Path(r"C:\Users\SSAFY\Documents\ai-development-tradition\s0-lab\control\assembly-rehearsal\runtime-profile-neutral-preloader-v0.2\runtime-profile-v0.2.schema.json"),
    Path(r"C:\Users\SSAFY\Documents\ai-development-tradition\s0-lab\control\assembly-rehearsal\runtime-profile-neutral-preloader-v0.3\runtime-profile-v0.3.schema.json"),
)
sys.path.insert(0, str(IMPLEMENTATION))

from s0_public_runtime_preloader.canonical import canonical_json_bytes, sha256_bytes  # noqa: E402
from s0_public_runtime_preloader.errors import RuntimeProfileError  # noqa: E402
from s0_public_runtime_preloader.schema import FixedDraft202012Validator  # noqa: E402
from s0_public_runtime_preloader.semantic import (  # noqa: E402
    ArtifactMaterial,
    BinaryMaterial,
    DEFERRED_STATIC_RELATIONS,
    HandleObservation,
    OFFLINE_POSTCREATION_RELATIONS,
    OFFLINE_PRECREATION_RELATIONS,
    PostcreationObservation,
    PrecreationObservation,
    PredecessorProfileMaterial,
    RELATIONS,
    StaticMaterialBundle,
    SystemImageMaterial,
    validate_postcreation_relation,
    validate_precreation_relations,
    validate_static_relations,
)
from s0_public_runtime_preloader.source_audit import (  # noqa: E402
    EXPECTED_FILES,
    inspect_source_structure,
)


def manifest(targets: dict[str, bytes]) -> bytes:
    return b"".join(
        hashlib.sha256(targets[path]).hexdigest().encode("ascii")
        + b"  "
        + path.encode("ascii")
        + b"\n"
        for path in sorted(targets)
    )


def artifact_profile(material: ArtifactMaterial) -> dict[str, str]:
    return {"sha256": material.sha256, "virtual_path": material.virtual_path}


def binary_profile(material: BinaryMaterial) -> dict[str, str]:
    return {
        **artifact_profile(material),
        "file_id": material.file_id,
        "pe_machine": material.pe_machine,
        "pe_timestamp": material.pe_timestamp,
        "size_of_image": material.size_of_image,
    }


def system_profile(material: SystemImageMaterial) -> dict[str, object]:
    return {
        **binary_profile(material),
        "required_exports": dict(material.required_exports),
        "volume_serial": material.volume_serial,
    }


def baseline() -> tuple[dict[str, object], bytes, StaticMaterialBundle, tuple[HandleObservation, ...], bytes, str]:
    profile = json.loads((PACKAGE / "runtime-profile-v0.4.json").read_bytes())
    predecessor_raws = tuple((PACKAGE / f"runtime-profile-v0.{index}.json").read_bytes() for index in range(1, 4))
    schema_raws = tuple(path.read_bytes() for path in SCHEMAS)
    predecessors = tuple(
        PredecessorProfileMaterial(raw, schema_raw, sha256_bytes(schema_raw))
        for raw, schema_raw in zip(predecessor_raws, schema_raws, strict=True)
    )
    profile["v0_1_profile_sha256"], profile["v0_2_profile_sha256"], profile["v0_3_profile_sha256"] = (
        sha256_bytes(raw) for raw in predecessor_raws
    )

    runtime_files = {"runtime/a.bin": b"runtime-a\n", "runtime/b.bin": b"runtime-b\n"}
    runtime_manifest_raw = manifest(runtime_files)
    runtime_manifest = ArtifactMaterial("runtime-files.sha256", runtime_manifest_raw)
    profile["package_closure"]["runtime_files_manifest"] = artifact_profile(runtime_manifest)

    provenance: tuple[ArtifactMaterial, ...] = (
        ArtifactMaterial("guard/source.cpp", b"guard-source\n"),
        ArtifactMaterial("guard/build.json", b"guard-build\n"),
        ArtifactMaterial("tools/compiler.exe", b"compiler\n"),
        ArtifactMaterial("tools/linker.exe", b"linker\n"),
        ArtifactMaterial("guard/imports.txt", b"imports\n"),
        ArtifactMaterial("guard/crt-imports.txt", b"crt-imports\n"),
        BinaryMaterial("guard/guard.pyd", b"guard-binary\n", "b" * 32, "0x00008664", "0x00000001", "0x00001000"),
        BinaryMaterial("guard/loaded-guard.pyd", b"guard-binary\n", "b" * 32, "0x00008664", "0x00000001", "0x00001000"),
    )
    for name, material in zip(
        ("source", "build_recipe", "compiler", "linker", "import_manifest", "crt_import_manifest"),
        provenance[:6],
        strict=True,
    ):
        profile["bootstrap_guard"][name] = artifact_profile(material)
    profile["bootstrap_guard"]["binary"] = binary_profile(provenance[6])
    profile["bootstrap_guard"]["loaded_image"] = binary_profile(provenance[7])

    platform_manifest = ArtifactMaterial("platform/platform.json", b"platform\n")
    loaded_pe_manifest = ArtifactMaterial("platform/loaded.json", b"loaded\n")
    semantic_validator = ArtifactMaterial(
        "runtime/semantic.py",
        (IMPLEMENTATION / "s0_public_runtime_preloader/semantic.py").read_bytes(),
    )
    kernel32 = SystemImageMaterial(
        "system32/kernel32.dll", b"kernel32\n", "c" * 32, "0x00008664", "0x00000001", "0x00001000",
        "kernel32", "0x0000000000000001", (("CreateProcessW", "0x00000001"),),
        str(profile["process_creation_policy"]["api"]),
    )
    ntdll = SystemImageMaterial(
        "system32/ntdll.dll", b"ntdll\n", "d" * 32, "0x00008664", "0x00000001", "0x00001000",
        "ntdll", "0x0000000000000001", (("NtCreateFile", "0x00000001"),),
        str(profile["atomic_root_policy"]["direct_import"]),
    )
    profile["platform_binding"]["platform_manifest"] = artifact_profile(platform_manifest)
    profile["platform_binding"]["loaded_pe_manifest"] = artifact_profile(loaded_pe_manifest)
    profile["platform_binding"]["kernel32"] = system_profile(kernel32)
    profile["platform_binding"]["ntdll"] = system_profile(ntdll)
    profile["semantic_validator"]["implementation"] = artifact_profile(semantic_validator)

    profile_raw = canonical_json_bytes(profile)
    effective_files = {
        "runtime-files.sha256": runtime_manifest_raw,
        "runtime-profile-v0.1.json": predecessor_raws[0],
        "runtime-profile-v0.2.json": predecessor_raws[1],
        "runtime-profile-v0.3.json": predecessor_raws[2],
        "runtime-profile-v0.4.json": profile_raw,
    }
    effective_manifest_raw = manifest(effective_files)
    material = StaticMaterialBundle(
        predecessors=predecessors,
        runtime_files_manifest=runtime_manifest,
        runtime_files=runtime_files,
        effective_package_manifest_raw=effective_manifest_raw,
        effective_package_files=effective_files,
        provenance_chain=provenance,
        platform_manifest=platform_manifest,
        loaded_pe_manifest=loaded_pe_manifest,
        system_images=(kernel32, ntdll),
        semantic_validator=semantic_validator,
    )
    handles = tuple(
        HandleObservation(str(row["role"]), str(row["kind"]), str(row["access"]), f"0x{index + 1:016x}")
        for index, row in enumerate(profile["process_creation_policy"]["ordered_handles"])
    )
    evidence_raw = b"exact-launch-evidence\n"
    evidence_sha = sha256_bytes(evidence_raw)
    return profile, profile_raw, material, handles, evidence_raw, evidence_sha


def static(profile: dict[str, object], profile_raw: bytes, material: StaticMaterialBundle) -> tuple[str, ...]:
    return validate_static_relations(
        profile,
        profile_raw,
        material,
        predecessor_schema_hashes=tuple(sha256_bytes(path.read_bytes()) for path in SCHEMAS),
    )


def precreation(
    profile: dict[str, object],
    handles: tuple[HandleObservation, ...],
    evidence_raw: bytes,
    evidence_sha: str,
    *,
    guard_locators: tuple[str, ...] | None = None,
    duplicate_root: str = "e" * 32,
) -> tuple[str, ...]:
    observation = PrecreationObservation(
        handles=handles,
        guard_locators=guard_locators or tuple(row.locator for row in handles),
        retained_root_file_id="e" * 32,
        duplicate_root_file_id=duplicate_root,
    )
    return validate_precreation_relations(
        profile,
        observation,
        evidence_handles=handles,
        evidence_raw=evidence_raw,
        evidence_sha256=evidence_sha,
    )


def postcreation(evidence_sha: str, *, actual_pid: int = 7, current_pid: int = 7) -> tuple[str, ...]:
    return validate_postcreation_relation(
        PostcreationObservation(evidence_sha, actual_pid, current_pid, "createprocess-success-bound-v0.4"),
        expected_evidence_sha256=evidence_sha,
    )


def assert_reject(action) -> None:
    try:
        action()
    except RuntimeProfileError:
        return
    raise AssertionError("expected RuntimeProfileError")


def run_cases() -> list[dict[str, str]]:
    cases: list[tuple[str, str, object]] = []

    def schema_positive() -> None:
        schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "additionalProperties": False,
            "properties": {
                "mode": {"enum": ["a", "b"], "type": "string"},
                "values": {"items": {"minimum": 1, "type": "integer"}, "minItems": 1, "type": "array", "uniqueItems": True},
            },
            "required": ["mode", "values"],
            "type": "object",
        }
        FixedDraft202012Validator(schema).validate({"mode": "a", "values": [1, 2]})

    def schema_unsupported() -> None:
        assert_reject(lambda: FixedDraft202012Validator({
            "$schema": "https://json-schema.org/draft/2020-12/schema", "format": "uri"
        }))

    def source_positive() -> None:
        source_root = IMPLEMENTATION / "s0_public_runtime_preloader"
        sources = {name: (source_root / name).read_bytes() for name in EXPECTED_FILES}
        assert inspect_source_structure(sources) == EXPECTED_FILES

    def source_negative() -> None:
        source_root = IMPLEMENTATION / "s0_public_runtime_preloader"
        sources = {name: (source_root / name).read_bytes() for name in EXPECTED_FILES}
        sources["errors.py"] += b"import os\n"
        assert_reject(lambda: inspect_source_structure(sources))

    def all_relations() -> None:
        profile, raw, material, handles, evidence_raw, evidence_sha = baseline()
        observed = set(static(profile, raw, material)) | set(DEFERRED_STATIC_RELATIONS)
        observed |= set(precreation(profile, handles, evidence_raw, evidence_sha))
        observed |= set(postcreation(evidence_sha))
        assert observed == set(RELATIONS)

    cases.extend((
        ("schema_supported_vocabulary_positive", "PASS", schema_positive),
        ("schema_unsupported_keyword_rejected", "PASS", schema_unsupported),
        ("source_audit_exact_inventory_positive", "PASS", source_positive),
        ("source_audit_forbidden_import_rejected", "PASS", source_negative),
        ("semantic_all_ten_relations_positive", "PASS", all_relations),
    ))

    def relation_case(index: int) -> None:
        profile, raw, material, handles, evidence_raw, evidence_sha = baseline()
        if index == 0:
            profile["v0_1_profile_sha256"] = "0" * 64
            assert_reject(lambda: static(profile, raw, material))
        elif index == 1:
            profile["package_closure"]["runtime_files_manifest"]["sha256"] = "0" * 64
            assert_reject(lambda: static(profile, raw, material))
        elif index == 2:
            chain = (ArtifactMaterial("guard/source.cpp", b"mutated\n"), *material.provenance_chain[1:])
            assert_reject(lambda: static(profile, raw, replace(material, provenance_chain=chain)))
        elif index == 3:
            profile["bootstrap_guard"]["loaded_image"]["file_id"] = "f" * 32
            loaded = replace(material.provenance_chain[-1], file_id="f" * 32)
            assert_reject(lambda: static(profile, raw, replace(material, provenance_chain=(*material.provenance_chain[:-1], loaded))))
        elif index == 4:
            profile["platform_binding"]["kernel32"]["required_exports"] = {"CreateProcessW": "0x00000002"}
            assert_reject(lambda: static(profile, raw, material))
        elif index == 5:
            changed = (replace(handles[0], role="mutated-role"), *handles[1:])
            assert_reject(lambda: precreation(profile, changed, evidence_raw, evidence_sha))
        elif index == 6:
            assert_reject(lambda: postcreation(evidence_sha, actual_pid=7, current_pid=8))
        elif index == 7:
            changed_locators = ("0x00000000000000ff", *(row.locator for row in handles[1:]))
            assert_reject(lambda: precreation(profile, handles, evidence_raw, evidence_sha, guard_locators=changed_locators))
        elif index == 8:
            assert_reject(lambda: precreation(profile, handles, evidence_raw, evidence_sha, duplicate_root="f" * 32))
        elif index == 9:
            rows = profile["package_closure"]["effective_rows"]
            rows[0], rows[1] = rows[1], rows[0]
            assert_reject(lambda: static(profile, raw, material))
        else:
            raise AssertionError("relation index differs")

    for index in range(10):
        cases.append((f"semantic_relation_{index + 1:02d}_mutation_rejected", "PASS", lambda index=index: relation_case(index)))

    def schema_snapshot() -> None:
        schema = {"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "integer"}
        validator = FixedDraft202012Validator(schema)
        schema["type"] = "string"
        validator.validate(7)

    cases.append(("schema_snapshot_is_caller_mutation_resistant", "PASS", schema_snapshot))

    results: list[dict[str, str]] = []
    for name, expected, action in cases:
        try:
            action()
        except Exception as error:  # test runner must preserve exact failure type and text
            results.append({"actual": "FAIL", "error": f"{type(error).__name__}:{error}", "expected": expected, "name": name})
        else:
            results.append({"actual": "PASS", "error": "", "expected": expected, "name": name})
    return results


def main() -> int:
    result_path = ROOT / "python-named-cases-final-result.json"
    ledger_path = ROOT / "python-named-cases-final-ledger.tsv"
    if result_path.exists() or ledger_path.exists():
        raise SystemExit("Python result already exists")
    results = run_cases()
    inputs = {
        "candidate_source_inventory_sha256": hashlib.sha256(b"".join(
            hashlib.sha256(path.read_bytes()).hexdigest().encode("ascii") + b"  " + path.name.encode("ascii") + b"\n"
            for path in sorted((IMPLEMENTATION / "s0_public_runtime_preloader").glob("*.py"))
        )).hexdigest(),
        "harness_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "profile_v0_1_sha256": sha256_bytes((PACKAGE / "runtime-profile-v0.1.json").read_bytes()),
        "profile_v0_2_sha256": sha256_bytes((PACKAGE / "runtime-profile-v0.2.json").read_bytes()),
        "profile_v0_3_sha256": sha256_bytes((PACKAGE / "runtime-profile-v0.3.json").read_bytes()),
        "profile_v0_4_sha256": sha256_bytes((PACKAGE / "runtime-profile-v0.4.json").read_bytes()),
        "schema_v0_1_sha256": sha256_bytes(SCHEMAS[0].read_bytes()),
        "schema_v0_2_sha256": sha256_bytes(SCHEMAS[1].read_bytes()),
        "schema_v0_3_sha256": sha256_bytes(SCHEMAS[2].read_bytes()),
    }
    output = {
        "case_count": len(results),
        "failed_cases": [row["name"] for row in results if row["actual"] != row["expected"]],
        "inputs": inputs,
        "passed_cases": sum(row["actual"] == row["expected"] for row in results),
        "results": results,
        "schema_id": "S0-RPNP-V0.4-PYTHON-NAMED-CASES-1",
    }
    raw = canonical_json_bytes(output)
    result_path.write_bytes(raw)
    lines = ["name\texpected\tactual\terror"] + [
        "\t".join((row["name"], row["expected"], row["actual"], row["error"].replace("\t", " ").replace("\n", " ")))
        for row in results
    ]
    ledger_path.write_bytes(("\n".join(lines) + "\n").encode("utf-8"))
    print(raw.decode("ascii"), end="")
    return 0 if not output["failed_cases"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

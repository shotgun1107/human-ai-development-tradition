from __future__ import annotations

import ast
import dataclasses
import hashlib
import json
import sys
import unittest
from pathlib import Path
from types import MappingProxyType

HERE = Path(__file__).resolve()
WORKSPACE = next(parent for parent in HERE.parents if (parent / "AGENTS.md").is_file())
IMPLEMENTATION = HERE.parents[1] / "implementation"
sys.path.insert(0, str(IMPLEMENTATION))

from s0_public_build_runtime import (  # noqa: E402
    DesignClosure,
    DllRow,
    ManifestBundle,
    RuntimeRow,
    RuntimeTreeStructureDiagnostic,
    TargetRow,
    authenticate_design_closure,
    construct_in_memory_record,
    derive_dll_directories,
    directory_identity_sha256,
    inspect_dll_resolution_structure,
    inspect_runtime_tree_structure,
    plan_dll_resolution,
    plan_runtime_tree,
    prepare_public_build_runtime_candidate,
    target_set_preimage,
    validate_effective_design,
    windows_directory_identity_key,
)
from s0_public_build_runtime.authority import manifest_contract  # noqa: E402
from s0_public_build_runtime.errors import (  # noqa: E402
    AuthenticationError,
    CanonicalError,
    PlanningError,
    SemanticError,
)
from s0_public_build_runtime.schema import (  # noqa: E402
    authenticate_schema_registry,
    validate_profile,
)

REVIEW = (
    "s0-lab/reviews/assembly-rehearsal/build-runtime-materialization-v0.5/"
    "public-assembly-build-runtime-materialization-design-v0.5-independent-review-v0.1.md"
)
DECISION = (
    "s0-lab/control/assembly-rehearsal/build-runtime-materialization-v0.5-control-integration/"
    "control-integration-decision-v0.1.md"
)


def _manifest_bundle(path: str) -> ManifestBundle:
    raw = (WORKSPACE / path).read_bytes()
    targets: dict[str, bytes] = {}
    for row in raw[:-1].split(b"\n"):
        _, _, target_raw = row.partition(b"  ")
        target = target_raw.decode("ascii")
        targets[target] = (WORKSPACE / target).read_bytes()
    return ManifestBundle(path, raw, targets)


def _closure() -> DesignClosure:
    return DesignClosure(
        tuple(_manifest_bundle(path) for path, _, _ in manifest_contract()),
        (WORKSPACE / REVIEW).read_bytes(),
        (WORKSPACE / DECISION).read_bytes(),
    )


def _runtime_row(
    path: str,
    role: str,
    byte_length: int = 1,
    sha256: str = "1" * 64,
    classification: str = "python-source",
    phase: str = "LOAD",
) -> RuntimeRow:
    return RuntimeRow(
        path,
        role,
        "a" * 64,
        "public/provenance-manifest",
        byte_length,
        sha256,
        classification,
        phase,
    )


class BuildRuntimeCandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.closure = _closure()
        cls.authority = authenticate_design_closure(cls.closure)
        cls.effective = validate_effective_design(cls.authority)

    def test_exact_design_authenticates_and_stops_on_external_pins(self) -> None:
        result = prepare_public_build_runtime_candidate(self.closure)
        self.assertEqual(
            result.state_trace,
            (
                "CANDIDATE-NEW",
                "PUBLIC-DESIGN-AUTHENTICATED",
                "V0.5-SEMANTICS-VALIDATED",
                "BLOCKED-MISSING-EXTERNAL-PIN",
            ),
        )
        self.assertEqual(result.mutation_row_count, 115)
        self.assertEqual(
            result.relation_sha256,
            "5af2b472f4abf96c446ae56fa90f02d54fa87cdebe4e6129fcc4c3c1de1610db",
        )
        self.assertEqual(
            result.policy_sha256,
            "3fd2df85e665c2a7b968d1c75f5c4ef2f85eb16e19682f718be4d3675b4a654b",
        )
        self.assertTrue(result.candidate_only)
        self.assertFalse(result.build_execution_authorized)
        self.assertFalse(result.runtime_materialized)
        self.assertFalse(result.native_api_reachable)
        self.assertFalse(result.rehearsal_pass)
        self.assertFalse(result.s0_executed)

    def test_each_manifest_raw_mutation_rejects(self) -> None:
        for index, bundle in enumerate(self.closure.manifests):
            manifests = list(self.closure.manifests)
            manifests[index] = dataclasses.replace(bundle, raw=bundle.raw + b"x")
            result = prepare_public_build_runtime_candidate(dataclasses.replace(self.closure, manifests=tuple(manifests)))
            self.assertEqual(result.state_trace, ("CANDIDATE-NEW", "CANDIDATE-REJECTED"))
            self.assertEqual(result.primary_failure, "BR-AUTH/0")

    def test_changed_missing_extra_and_nonbytes_targets_reject(self) -> None:
        for index, bundle in enumerate(self.closure.manifests):
            base = dict(bundle.targets)
            first = next(iter(base))
            mutations: list[dict[str, object]] = []
            changed = dict(base)
            changed[first] = base[first] + b"x"
            mutations.append(changed)
            missing = dict(base)
            missing.pop(first)
            mutations.append(missing)
            mutations.append({**base, "public/extra.txt": b"extra\n"})
            mutations.append({**base, first: bytearray(base[first])})
            for targets in mutations:
                manifests = list(self.closure.manifests)
                manifests[index] = dataclasses.replace(bundle, targets=targets)
                result = prepare_public_build_runtime_candidate(
                    dataclasses.replace(self.closure, manifests=tuple(manifests))
                )
                self.assertEqual(result.terminal_state, "CANDIDATE-REJECTED")

    def test_review_and_control_decision_mutations_reject(self) -> None:
        for closure in (
            dataclasses.replace(self.closure, approving_review_raw=self.closure.approving_review_raw + b"x"),
            dataclasses.replace(self.closure, control_decision_raw=self.closure.control_decision_raw + b"x"),
        ):
            result = prepare_public_build_runtime_candidate(closure)
            self.assertEqual(result.terminal_state, "CANDIDATE-REJECTED")

    def _semantic_mutation(self, path: str, mutate) -> None:
        files = dict(self.authority.files)
        value = json.loads(files[path])
        mutate(value)
        files[path] = (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
        forged = dataclasses.replace(self.authority, files=MappingProxyType(files))
        with self.assertRaises((AuthenticationError, SemanticError)):
            validate_effective_design(forged)

    def test_relation_patch_and_policy_authority_mutations_reject(self) -> None:
        v04_map = (
            "s0-lab/control/assembly-rehearsal/build-runtime-materialization-v0.4/"
            "build-runtime-materialization-interface-map-v0.4.json"
        )
        v04_schema = (
            "s0-lab/control/assembly-rehearsal/build-runtime-materialization-v0.4/"
            "build-runtime-materialization-profile-v0.4.schema.json"
        )
        self._semantic_mutation(v04_map, lambda value: value["semantic_relations"].__setitem__(15, "wrong"))
        self._semantic_mutation(
            v04_schema,
            lambda value: value["properties"]["publication_no_replace_policy"]["const"].pop("flags_numeric"),
        )

    def test_authentication_marker_cannot_cover_mutated_pinned_bytes(self) -> None:
        schema_path = (
            "s0-lab/control/assembly-rehearsal/build-runtime-materialization-v0.5/"
            "build-runtime-materialization-profile-v0.5.schema.json"
        )
        files = dict(self.authority.files)
        files[schema_path] = b"{}\n"
        forged = dataclasses.replace(self.authority, files=MappingProxyType(files))
        with self.assertRaises(AuthenticationError):
            forged.require_authenticated()
        with self.assertRaises((AuthenticationError, SemanticError)):
            validate_effective_design(forged)

    def test_effective_policy_is_deeply_immutable(self) -> None:
        access = self.effective.publication_policy["source_handle_required_access"]
        self.assertIs(type(access), tuple)
        with self.assertRaises(AttributeError):
            access.append("DELETE")
        self.assertEqual(
            self.effective.publication_policy_sha256,
            "3fd2df85e665c2a7b968d1c75f5c4ef2f85eb16e19682f718be4d3675b4a654b",
        )
        with self.assertRaises(SemanticError):
            dataclasses.replace(self.effective, publication_policy_sha256="0" * 64)

    def test_effective_design_rejects_invented_matrix_and_resources(self) -> None:
        fake_rows = tuple(
            MappingProxyType(
                {
                    "id": f"FAKE-{index:03d}",
                    "expected_primary_failure": "FAKE/0",
                    "output_created_before_primary_failure": False,
                }
            )
            for index in range(115)
        )
        with self.assertRaises(SemanticError):
            dataclasses.replace(self.effective, mutation_rows=fake_rows)
        fake_resources = MappingProxyType({f"fake_{index}": index + 1 for index in range(12)})
        with self.assertRaises(SemanticError):
            dataclasses.replace(self.effective, resource_limits=fake_resources)

    def test_effective_matrix_and_resource_contract(self) -> None:
        self.assertEqual(len(self.effective.mutation_rows), 115)
        self.assertEqual(len({row["id"] for row in self.effective.mutation_rows}), 115)
        self.assertEqual(len(self.effective.resource_limits), 12)
        for row in self.effective.mutation_rows:
            suffix = "/1" if row["output_created_before_primary_failure"] else "/0"
            self.assertTrue(row["expected_primary_failure"].endswith(suffix))

    def test_target_set_codec_is_exact_and_ordered(self) -> None:
        rows = (
            TargetRow("runtime/a.bin", 3, hashlib.sha256(b"aaa").hexdigest()),
            TargetRow("runtime/b.bin", 4, hashlib.sha256(b"bbbb").hexdigest()),
        )
        raw = target_set_preimage(rows)
        self.assertTrue(raw.startswith(b"schema_id=S0-BRM-TARGET-SET-PREIMAGE-1\n"))
        self.assertTrue(raw.endswith(b"\n"))
        self.assertIn(b"target_count=2\n", raw)
        self.assertIn(b"total_target_bytes=7\n", raw)
        with self.assertRaises(CanonicalError):
            target_set_preimage(tuple(reversed(rows)))

    def test_windows_directory_identity_and_dll_order(self) -> None:
        rows = (
            DllRow("python312.dll", "runtime/bin/python312.dll", "1" * 64),
            DllRow("guard.dll", "runtime/ext/guard.dll", "2" * 64),
        )
        diagnostic = inspect_dll_resolution_structure("runtime/bin/verifier.exe", rows)
        directories = diagnostic.directories
        self.assertEqual([row.path for row in directories], ["runtime/bin", "runtime/ext"])
        self.assertEqual(windows_directory_identity_key("Runtime/Bin"), "runtime/bin")
        self.assertNotEqual(directory_identity_sha256("Runtime/Bin"), directory_identity_sha256("runtime/bin"))
        self.assertEqual([row.name for row in diagnostic.rows], ["python312.dll", "guard.dll"])
        self.assertEqual([row.directory_index for row in diagnostic.rows], [0, 1])
        self.assertEqual(diagnostic.authority_status, "BLOCKED-MISSING-EXTERNAL-PIN")
        for ordered in (rows, tuple(reversed(rows))):
            with self.assertRaises(PlanningError):
                plan_dll_resolution("runtime/bin/verifier.exe", ordered)
        with self.assertRaises(PlanningError):
            derive_dll_directories("runtime/bin/verifier.exe", rows)
        with self.assertRaises(PlanningError):
            inspect_dll_resolution_structure(
                "runtime/bin/verifier.exe",
                (DllRow("wrong.dll", "runtime/bin/other.dll", "1" * 64),),
            )
        with self.assertRaises(PlanningError):
            inspect_dll_resolution_structure(
                "runtime/bin/verifier.exe",
                (
                    DllRow("one.dll", "runtime/Lib/one.dll", "1" * 64),
                    DllRow("two.dll", "runtime/lib/two.dll", "2" * 64),
                ),
            )
        with self.assertRaises(PlanningError):
            DllRow("blocked.dll", "S0-LAB/CONTROL/F0-SEALED/blocked.dll", "1" * 64)

    def test_virtual_path_hostile_forms_reject(self) -> None:
        for path in (
            "/absolute/file",
            "C:/drive/file",
            "a\\b",
            "a//b",
            "a/../b",
            "runtime/CON.txt",
            "runtime/trailing./file",
            "런타임/file",
        ):
            with self.assertRaises((CanonicalError, PlanningError, UnicodeError)):
                _runtime_row(path, "role")

    def test_runtime_plan_is_nonexecuting_and_bounded(self) -> None:
        rows = (
            _runtime_row("runtime/a.py", "application", 3, "1" * 64),
            _runtime_row("runtime/b.dll", "python-dll", 4, "2" * 64, "native-library"),
        )
        diagnostic = inspect_runtime_tree_structure(rows)
        self.assertEqual(diagnostic.file_count, 2)
        self.assertEqual(diagnostic.total_bytes, 7)
        self.assertFalse(diagnostic.execution_authorized)
        self.assertEqual(diagnostic.authority_status, "BLOCKED-MISSING-EXTERNAL-PIN")
        with self.assertRaises(PlanningError):
            plan_runtime_tree(rows)
        with self.assertRaises(PlanningError):
            inspect_runtime_tree_structure(rows, maximum_bytes=6)
        with self.assertRaises(PlanningError):
            inspect_runtime_tree_structure(
                (rows[0], dataclasses.replace(rows[1], semantic_role="application"))
            )

    def test_runtime_plan_authority_and_closed_path_contract(self) -> None:
        rows = (
            _runtime_row("Runtime/A/b", "application", 1, "1" * 64),
            _runtime_row("runtime/a", "dependency", 1, "2" * 64),
        )
        with self.assertRaises(PlanningError):
            inspect_runtime_tree_structure(rows)
        with self.assertRaises(PlanningError):
            inspect_runtime_tree_structure(
                (_runtime_row("runtime/a", "application"),),
                maximum_bytes=2_147_483_649,
            )
        with self.assertRaises(PlanningError):
            _runtime_row("S0-LAB/CONTROL/F0-SEALED", "role")
        with self.assertRaises(PlanningError):
            _runtime_row("S0-LAB/CONTROL/F0-SEALED/public-test.bin", "role")

        class DuckRow:
            path = "runtime/a"
            role = "application"
            byte_length = 1
            sha256 = "1" * 64

        with self.assertRaises(PlanningError):
            inspect_runtime_tree_structure((DuckRow(),))

        valid = inspect_runtime_tree_structure((_runtime_row("runtime/a", "application"),))
        self.assertIs(type(valid), RuntimeTreeStructureDiagnostic)
        with self.assertRaises(TypeError):
            dataclasses.replace(valid, execution_authorized=True)
        with self.assertRaises(PlanningError):
            dataclasses.replace(valid, total_bytes=2)
        backing = dict(valid.path_index)
        view = MappingProxyType(backing)
        backing.clear()
        self.assertEqual(len(view), 0)
        self.assertEqual(len(valid.path_index), 1)

    def test_runtime_row_exact_eight_field_grammar(self) -> None:
        row = _runtime_row("runtime/a.py", "application")
        self.assertEqual(row.virtual_path, "runtime/a.py")
        for mutation in (
            {"byte_length": 0},
            {"classification": "arbitrary"},
            {"semantic_role": "INVALID_ROLE"},
            {"load_or_read_phase": "lowercase"},
            {"provenance_manifest_sha256": "0"},
            {"provenance_path": "../outside"},
        ):
            with self.assertRaises(PlanningError):
                dataclasses.replace(row, **mutation)
        self.assertEqual(len(dataclasses.fields(RuntimeRow)), 8)

    def test_record_is_in_memory_diagnostic_only(self) -> None:
        record = construct_in_memory_record({"candidate_only": True, "result": "diagnostic"})
        self.assertEqual(record.observation_status, "UNAVAILABLE-NOT-MATERIALIZED")
        self.assertIsNone(record.closed_file_observation)
        self.assertIsNone(record.readback_observation)

    def test_diagnostic_fields_are_derived_from_canonical_bytes(self) -> None:
        result = prepare_public_build_runtime_candidate(self.closure)
        with self.assertRaises(TypeError):
            dataclasses.replace(result, external_pin_status="PRESENT")
        value = json.loads(result.raw)
        value["external_pin_status"] = "PRESENT"
        forged_raw = (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
        with self.assertRaises(ValueError):
            type(result)(forged_raw, hashlib.sha256(forged_raw).hexdigest())
        value = json.loads(result.raw)
        value["relation_sha256"] = "0" * 64
        forged_raw = (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
        with self.assertRaises(ValueError):
            type(result)(forged_raw, hashlib.sha256(forged_raw).hexdigest())

    def test_schema_surface_is_unconditionally_blocked_without_dependency_pin(self) -> None:
        with self.assertRaises(SemanticError):
            authenticate_schema_registry({"schema.json": b"{}\n"})
        with self.assertRaises(SemanticError):
            validate_profile(b"{}\n", b"{}\n", {"schema.json": b"{}\n"})

    def test_implementation_has_no_execution_or_ambient_surface(self) -> None:
        implementation_root = IMPLEMENTATION / "s0_public_build_runtime"
        forbidden_imports = {
            "ctypes",
            "jsonschema",
            "os",
            "pathlib",
            "referencing",
            "socket",
            "subprocess",
            "urllib",
        }
        forbidden_calls = {"open", "Popen", "run", "system", "urlopen", "CreateProcessW", "NtCreateFile"}
        for source_path in implementation_root.glob("*.py"):
            tree = ast.parse(source_path.read_text(encoding="utf-8"))
            imports = {
                alias.name.split(".")[0]
                for node in ast.walk(tree)
                if isinstance(node, (ast.Import, ast.ImportFrom))
                for alias in node.names
            }
            calls = {
                getattr(node.func, "attr", getattr(node.func, "id", ""))
                for node in ast.walk(tree)
                if isinstance(node, ast.Call)
            }
            self.assertTrue(imports.isdisjoint(forbidden_imports), source_path.name)
            self.assertTrue(calls.isdisjoint(forbidden_calls), source_path.name)

    def test_mapping_and_dataclass_types_fail_closed(self) -> None:
        first = self.closure.manifests[0]
        with self.assertRaises(AuthenticationError):
            authenticate_design_closure(dataclasses.replace(self.closure, manifests=list(self.closure.manifests)))
        mutated = dataclasses.replace(first, targets=MappingProxyType(dict(first.targets)))
        manifests = (mutated, *self.closure.manifests[1:])
        result = prepare_public_build_runtime_candidate(dataclasses.replace(self.closure, manifests=manifests))
        self.assertEqual(result.terminal_state, "CANDIDATE-REJECTED")


if __name__ == "__main__":
    unittest.main()

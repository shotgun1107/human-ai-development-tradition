from __future__ import annotations

import ast
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve()
ASSEMBLY_ROOT = HERE.parents[1]
WORKSPACE_ROOT = HERE.parents[4]
IMPLEMENTATION_ROOT = ASSEMBLY_ROOT / "implementation"
if str(IMPLEMENTATION_ROOT) not in sys.path:
    sys.path.insert(0, str(IMPLEMENTATION_ROOT))

from s0_public_assembly_verifier.consumer import (  # noqa: E402
    DiagnosticPredicateDecision,
    LiveDecision,
)
from s0_public_assembly_verifier.errors import AssemblyFailure  # noqa: E402
from s0_public_assembly_verifier.harness import (  # noqa: E402
    _COMPONENT_CHILD_CLOSURES,
    _canonical_child_config,
    _parse_child_failure,
    _create_fresh_output_root,
    run_diagnostic_public_candidate,
    run_live_public_candidate,
)


class HarnessContractTests(unittest.TestCase):
    def test_child_component_closure_is_frozen_and_narrow(self) -> None:
        self.assertEqual(tuple(map(len, _COMPONENT_CHILD_CLOSURES)), (7, 7, 7, 8))
        flattened = {path for group in _COMPONENT_CHILD_CLOSURES for path in group}
        self.assertNotIn("s0-lab/i0/implementation/s0_i0/cli.py", flattened)
        self.assertNotIn("s0-lab/i1/implementation/s0_i1/verification.py", flattened)
        self.assertNotIn("s0-lab/i2/implementation/s0_i2/cli.py", flattened)
        self.assertNotIn("s0-lab/i3/implementation/s0_i3/cli.py", flattened)

    def test_live_entry_is_unconditionally_fail_closed(self) -> None:
        with self.assertRaisesRegex(AssemblyFailure, "runtime profile"):
            run_live_public_candidate(
                workspace_root=WORKSPACE_ROOT,
                output_root=WORKSPACE_ROOT,
                implementation_manifest_sha256="0" * 64,
            )

    def test_diagnostic_api_cannot_claim_live_decision(self) -> None:
        annotation = run_diagnostic_public_candidate.__annotations__["return"]
        self.assertEqual(annotation, "DiagnosticPredicateDecision")
        self.assertIsNot(DiagnosticPredicateDecision, LiveDecision)

    def test_child_config_has_no_dependency_injection_field(self) -> None:
        parameters = tuple(_canonical_child_config.__annotations__)
        self.assertNotIn("dependency_root", parameters)

    def test_live_source_never_launches_or_constructs_backend(self) -> None:
        source = Path(
            run_live_public_candidate.__code__.co_filename
        ).read_text(encoding="utf-8")
        tree = ast.parse(source)
        function = next(
            node
            for node in tree.body
            if isinstance(node, ast.FunctionDef)
            and node.name == "run_live_public_candidate"
        )
        calls = {
            getattr(node.func, "attr", getattr(node.func, "id", ""))
            for node in ast.walk(function)
            if isinstance(node, ast.Call)
        }
        self.assertNotIn("_execute_authenticated", calls)
        self.assertNotIn("for_real_win32", calls)
        self.assertNotIn("consume", calls)

    def test_parent_exclusively_creates_one_absent_output_root(self) -> None:
        with tempfile.TemporaryDirectory() as parent:
            output = Path(parent) / "one-run"
            created = _create_fresh_output_root(output)
            self.assertEqual(created, output.resolve(strict=True))
            with self.assertRaisesRegex(AssemblyFailure, "absent"):
                _create_fresh_output_root(output)

    def test_child_failure_parser_requires_all_ten_fixed_fields(self) -> None:
        value = {
            "cause_label": "ValueError",
            "cleanup_status": "not-required",
            "failed_operation": "preflight-authentication",
            "observed_transport_calls": 0,
            "offline_status": "offline-not-success-diagnostic-only",
            "output_root_status": "NOT-RESERVED",
            "primary_class": "AR-AUTH",
            "rehearsal_pass": False,
            "schema_id": "S0-PUBLIC-ASSEMBLY-FAILURE-DIAGNOSTIC-1",
            "state_at_failure": "NEW",
        }
        raw = (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()
        self.assertEqual(_parse_child_failure(raw), ("AR-AUTH", 0))
        for key in tuple(value):
            mutated = dict(value)
            mutated.pop(key)
            raw = (json.dumps(mutated, sort_keys=True, separators=(",", ":")) + "\n").encode()
            with self.assertRaises(Exception):
                _parse_child_failure(raw)
        for key, wrong in (
            ("schema_id", "wrong"),
            ("offline_status", "success"),
            ("rehearsal_pass", True),
        ):
            mutated = dict(value)
            mutated[key] = wrong
            raw = (json.dumps(mutated, sort_keys=True, separators=(",", ":")) + "\n").encode()
            with self.assertRaises(Exception):
                _parse_child_failure(raw)

    def test_actual_isolated_child_fails_closed_without_runtime_profile(self) -> None:
        candidate = IMPLEMENTATION_ROOT / "s0_public_assembly_candidate"
        allowed = {
            path.relative_to(WORKSPACE_ROOT).as_posix()
            for path in candidate.glob("*.py")
        }
        allowed.update(path for group in _COMPONENT_CHILD_CLOSURES for path in group)
        with tempfile.TemporaryDirectory() as parent:
            output = Path(parent) / "isolated-output"
            output.mkdir()
            value = {
                "allowed_read_paths": sorted(allowed),
                "assembly_implementation_manifest_sha256": "0" * 64,
                "candidate_root": (
                    "s0-lab/assembly-rehearsal/public-end-to-end-v0.1/implementation/"
                    "s0_public_assembly_candidate"
                ),
                "design_independent_review_sha256": "1" * 64,
                "design_package_manifest_sha256": "2" * 64,
                "output_root": str(output),
                "schema_id": "S0-PUBLIC-ASSEMBLY-CHILD-CONFIG-1",
                "workspace_root": str(WORKSPACE_ROOT),
            }
            raw = (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()
            completed = subprocess.run(
                (
                    sys.executable,
                    "-I",
                    "-S",
                    "-B",
                    str(IMPLEMENTATION_ROOT / "s0_public_assembly_child_bootstrap.py"),
                ),
                input=raw,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=WORKSPACE_ROOT,
                check=False,
                timeout=10,
            )
            self.assertEqual(completed.returncode, 2)
            self.assertEqual(completed.stdout, b"")
            self.assertEqual(completed.stderr, b"BOOTSTRAP_FAILURE\n")
            self.assertEqual(tuple(output.iterdir()), ())


if __name__ == "__main__":
    unittest.main()

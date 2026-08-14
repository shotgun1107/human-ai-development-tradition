from __future__ import annotations

import ast
import dataclasses
import json
import sys
import unittest
from pathlib import Path
from unittest import mock

HERE = Path(__file__).resolve()
WORKSPACE = next(parent for parent in HERE.parents if (parent / "AGENTS.md").is_file())
INTEGRATION_IMPLEMENTATION = HERE.parents[1] / "implementation"
RPNP_ROOT = WORKSPACE / "s0-lab/assembly-rehearsal/runtime-profile-neutral-preloader-v0.3"
RPNP_IMPLEMENTATION = RPNP_ROOT / "implementation"
RPNP_TESTS = RPNP_ROOT / "tests"
for path in (INTEGRATION_IMPLEMENTATION, RPNP_IMPLEMENTATION, RPNP_TESTS):
    sys.path.insert(0, str(path))

import test_runtime_preloader as synthetic  # noqa: E402
from s0_public_assembly_integration import candidate  # noqa: E402


class OfflineIntegrationTests(unittest.TestCase):
    def _material(self):
        _, profile_raw, static_material, _ = synthetic._candidate_material()
        return (
            synthetic._assembly_bundle(),
            candidate.PublicInputClosure(
                *synthetic._manifest_targets(RPNP_ROOT / "verification/implementation-files.sha256"),
                *synthetic._manifest_targets(WORKSPACE / "s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-integration-v0.1/design-package-files.sha256"),
                *synthetic._manifest_targets(WORKSPACE / "s0-lab/control/assembly-rehearsal/runtime-profile-neutral-preloader-integration-v0.2/design-package-files.sha256"),
            ),
            profile_raw,
            static_material,
            synthetic._inputs(),
        )

    def test_exact_bridge_happy_path_is_offline_diagnostic_only(self) -> None:
        artifacts, closure, profile_raw, static_material, inputs = self._material()
        result = candidate.prepare_offline_integration_diagnostic(
            artifacts=artifacts,
            closure=closure,
            profile_raw=profile_raw,
            schema_raw=synthetic.SCHEMA_RAW,
            static_material=static_material,
            inputs=inputs,
        )
        self.assertEqual(
            result.state_trace,
            (
                "OFFLINE-NEW",
                "OFFLINE-PUBLIC-ARTIFACTS-AUTHENTICATED",
                "OFFLINE-PLAN-VALIDATED",
                "OFFLINE-DIAGNOSTIC-COMPLETE",
            ),
        )
        self.assertTrue(result.candidate_only)
        self.assertFalse(result.native_api_reachable)
        self.assertFalse(result.rehearsal_pass)
        value = json.loads(result.raw)
        self.assertEqual(value["terminal_state"], "OFFLINE-DIAGNOSTIC-COMPLETE")
        self.assertIsNone(value["failure_class"])

    def test_changed_authenticated_byte_rejects_without_partial_success(self) -> None:
        artifacts, closure, profile_raw, static_material, inputs = self._material()
        changed = dataclasses.replace(
            artifacts,
            implementation_manifest_raw=artifacts.implementation_manifest_raw + b"x",
        )
        result = candidate.prepare_offline_integration_diagnostic(
            artifacts=changed,
            closure=closure,
            profile_raw=profile_raw,
            schema_raw=synthetic.SCHEMA_RAW,
            static_material=static_material,
            inputs=inputs,
        )
        self.assertEqual(result.state_trace, ("OFFLINE-NEW", "OFFLINE-REJECTED"))
        self.assertEqual(result.failure_class, "offline-input-or-plan-rejected")

    def test_nonoffline_bridge_result_rejects(self) -> None:
        artifacts, closure, profile_raw, static_material, inputs = self._material()
        prepared = mock.Mock(candidate_only=False, native_api_reachable=True)
        with mock.patch.object(candidate, "prepare_assembly_runtime_launch", return_value=prepared) as bridge:
            result = candidate.prepare_offline_integration_diagnostic(
                artifacts=artifacts,
                closure=closure,
                profile_raw=profile_raw,
                schema_raw=synthetic.SCHEMA_RAW,
                static_material=static_material,
                inputs=inputs,
            )
        bridge.assert_called_once()
        self.assertEqual(result.failure_class, "offline-authority-boundary-rejected")
        self.assertEqual(result.terminal_state, "OFFLINE-REJECTED")

    def test_changed_missing_and_extra_closure_targets_reject_before_bridge(self) -> None:
        artifacts, closure, profile_raw, static_material, inputs = self._material()
        base = dict(closure.rpnp_implementation_targets)
        mutations = []
        changed = dict(base)
        changed[next(iter(changed))] = b"changed\n"
        mutations.append(changed)
        missing = dict(base)
        missing.pop(next(iter(missing)))
        mutations.append(missing)
        mutations.append({**base, "public/extra.txt": b"extra\n"})
        for targets in mutations:
            mutated = dataclasses.replace(closure, rpnp_implementation_targets=targets)
            with mock.patch.object(candidate, "prepare_assembly_runtime_launch") as bridge:
                result = candidate.prepare_offline_integration_diagnostic(
                    artifacts=artifacts,
                    closure=mutated,
                    profile_raw=profile_raw,
                    schema_raw=synthetic.SCHEMA_RAW,
                    static_material=static_material,
                    inputs=inputs,
                )
            bridge.assert_not_called()
            self.assertEqual(result.state_trace, ("OFFLINE-NEW", "OFFLINE-REJECTED"))

    def test_candidate_source_has_no_live_or_ambient_execution_surface(self) -> None:
        source_path = INTEGRATION_IMPLEMENTATION / "s0_public_assembly_integration/candidate.py"
        tree = ast.parse(source_path.read_text(encoding="utf-8"))
        imports = {
            alias.name.split(".")[0]
            for node in ast.walk(tree)
            if isinstance(node, (ast.Import, ast.ImportFrom))
            for alias in node.names
        }
        self.assertTrue(imports.isdisjoint({"ctypes", "os", "pathlib", "socket", "subprocess", "urllib"}))
        calls = {
            getattr(node.func, "attr", getattr(node.func, "id", ""))
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
        }
        self.assertIn("prepare_assembly_runtime_launch", calls)
        self.assertTrue(calls.isdisjoint({"open", "Popen", "run", "system", "urlopen"}))


if __name__ == "__main__":
    unittest.main()

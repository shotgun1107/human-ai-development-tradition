from __future__ import annotations

import ast
import io
import json
import os
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[3]
IMPLEMENTATION = WORKSPACE / "s0-lab" / "i1" / "implementation"
sys.path.insert(0, str(IMPLEMENTATION))

from s0_i1.cli import main as cli_main  # noqa: E402
from s0_i1.verification import build_public_verification_record  # noqa: E402


class VerificationTests(unittest.TestCase):
    def test_verification_record_distinguishes_facts_tests_and_closed_proposals(self):
        record = build_public_verification_record(WORKSPACE)
        self.assertEqual(record["status"], "pass", record["errors"])
        self.assertTrue(record["not_an_s0_run"])
        self.assertEqual(record["authenticated_facts"]["counts"]["edge_rows"], 64)
        self.assertEqual(record["construction_tests"]["topology_issue_count"], 0)
        self.assertGreaterEqual(len(record["closed_proposals_and_boundaries"]), 8)
        self.assertEqual(record["errors"], [])

    def test_runner_module_has_no_provider_network_retry_tool_or_state_backend(self):
        path = IMPLEMENTATION / "s0_i1" / "runner.py"
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        self.assertTrue(
            imported.isdisjoint(
                {"aiohttp", "asyncio", "http", "requests", "socket", "subprocess", "urllib"}
            )
        )
        lowered = source.lower()
        for forbidden in (
            "openai",
            "anthropic",
            "requests.",
            "socket.",
            "retry(",
            "tool_call",
            "persistent_state",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, lowered)

    def test_cli_verify_is_machine_readable_and_path_free(self):
        old = Path.cwd()
        stdout = io.StringIO()
        stderr = io.StringIO()
        try:
            os.chdir(WORKSPACE)
            with redirect_stdout(stdout), redirect_stderr(stderr):
                code = cli_main(["verify"])
        finally:
            os.chdir(old)
        self.assertEqual(code, 0, stderr.getvalue())
        parsed = json.loads(stdout.getvalue())
        self.assertEqual(parsed["status"], "pass")
        self.assertEqual(stderr.getvalue(), "")
        self.assertNotIn(str(WORKSPACE), stdout.getvalue())


if __name__ == "__main__":
    unittest.main()

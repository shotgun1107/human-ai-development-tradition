from __future__ import annotations

import ast
import hashlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from jsonschema import Draft202012Validator, ValidationError


WORKSPACE = Path(__file__).resolve().parents[3]
I1 = WORKSPACE / "s0-lab" / "i1"
IMPLEMENTATION = I1 / "implementation"
sys.path.insert(0, str(IMPLEMENTATION))

from s0_i1.cli import main as cli_main  # noqa: E402
from s0_i1.verification import build_public_verification_record  # noqa: E402


class VerificationTests(unittest.TestCase):
    def _schema(self, name: str):
        return json.loads((I1 / "spec" / "schemas" / name).read_text(encoding="utf-8"))

    def test_verification_record_distinguishes_facts_tests_and_boundaries(self):
        record = build_public_verification_record(WORKSPACE)
        self.assertEqual(record["status"], "pass", record["errors"])
        self.assertTrue(record["not_an_s0_run"])
        self.assertEqual(record["authenticated_facts"]["counts"]["edge_rows"], 64)
        tests = record["construction_tests"]
        self.assertEqual(tests["topology_issue_count"], 0)
        self.assertGreater(tests["schema_instances"]["positive_instances"], 20)
        self.assertGreaterEqual(tests["schema_instances"]["negative_instances"], 10)
        self.assertEqual(tests["schema_instances"]["positive_failures"], [])
        self.assertEqual(tests["schema_instances"]["negative_failures"], [])
        self.assertGreaterEqual(
            len(record["closed_proposals_and_boundaries"]), 8
        )
        self.assertEqual(record["errors"], [])

    def test_published_schemas_reject_official_counterexamples_directly(self):
        digest = "0" * 64
        receipt = Draft202012Validator(self._schema("evidence-receipt.schema.json"))
        valid_receipt = {
            "edge": "E05",
            "producer_role": "content-intake",
            "artifact_kind": "content-digest",
            "artifact_sha256": digest,
            "required_check_result": "accepted",
        }
        receipt.validate(valid_receipt)
        for attack in (
            {**valid_receipt, "edge": "E99"},
            {**valid_receipt, "producer_role": "simulation-builder"},
            {**valid_receipt, "artifact_kind": "power-summary"},
        ):
            with self.assertRaises(ValidationError):
                receipt.validate(attack)

        bundle = Draft202012Validator(
            self._schema("evidence-bundle-structure.schema.json")
        )
        bundle.validate(
            {
                "edge": "ROOT",
                "entry_count": 0,
                "control_integration_manifest_sha256": digest,
                "envelope_sha256": [],
            }
        )
        for attack in (
            {"edge": "ROOT", "entry_count": 0, "envelope_sha256": []},
            {
                "edge": "ROOT",
                "entry_count": 1,
                "control_integration_manifest_sha256": digest,
                "envelope_sha256": [digest],
            },
            {"edge": "E25", "entry_count": 2, "envelope_sha256": [digest]},
            {
                "edge": "E05",
                "entry_count": 1,
                "control_integration_manifest_sha256": digest,
                "envelope_sha256": [digest],
            },
        ):
            with self.assertRaises(ValidationError):
                bundle.validate(attack)

        status = Draft202012Validator(self._schema("status-record.schema.json"))
        valid_status = {
            "sequence": 1,
            "previous_record_sha256": digest,
            "event_edge": "E02",
            "event_commitment_sha256": digest,
            "evidence_mask": "0001",
            "status_code": "A-0001",
            "monotonic_timestamp_ns": 1,
        }
        status.validate(valid_status)
        for attack in (
            {**valid_status, "event_edge": "E99"},
            {**valid_status, "sequence": 2},
            {**valid_status, "evidence_mask": "0002"},
            {**valid_status, "status_code": "A-0002"},
        ):
            with self.assertRaises(ValidationError):
                status.validate(attack)

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
                {
                    "aiohttp",
                    "asyncio",
                    "http",
                    "requests",
                    "socket",
                    "subprocess",
                    "urllib",
                }
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

    def test_verifier_requires_external_manifest_before_candidate_python(self):
        source = (I1 / "tools" / "verify-i1.ps1").read_text(encoding="utf-8")
        self.assertIn("[Parameter(Mandatory = $true)]", source)
        self.assertIn("[ValidatePattern('^[0-9a-f]{64}$')]", source)
        self.assertIn(
            "$ExpectedManifestSha256 -cnotmatch '^[0-9a-f]{64}$'", source
        )
        self.assertIn("$actualManifestHash -cne $ExpectedManifestSha256", source)
        self.assertIn("$Matches[1] -cne $ExpectedManifestSha256", source)
        self.assertIn("$sidecarText -cnotmatch", source)
        self.assertIn("$line -cnotmatch", source)
        self.assertIn("$actual -cne $expected", source)
        preflight = source.index(
            "$initialSnapshot = Get-I1PayloadSnapshot -Phase 'pre-execution'"
        )
        snapshot = source.index("$snapshotRoot = New-AuthenticatedSnapshot")
        python_path = source.index("$env:PYTHONPATH = $snapshotImplementationRoot")
        first_python = source.index('python -c "import sys')
        self.assertLess(preflight, snapshot)
        self.assertLess(snapshot, python_path)
        self.assertLess(preflight, python_path)
        self.assertLess(preflight, first_python)
        self.assertIn("external-expected-manifest-sha256", source)
        self.assertIn("final-stability", source)
        self.assertIn("PayloadBytes", source)
        self.assertIn("Remove-Item -LiteralPath $resolvedSnapshot -Recurse -Force", source)

    def test_verifier_rejects_uppercase_external_digest_before_manifest_access(self):
        with tempfile.TemporaryDirectory(dir=I1 / "tests") as temporary:
            repo = Path(temporary) / "repo"
            tools = repo / "s0-lab" / "i1" / "tools"
            tools.mkdir(parents=True)
            script = tools / "verify-i1.ps1"
            script.write_bytes((I1 / "tools" / "verify-i1.ps1").read_bytes())
            completed = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    str(script),
                    "-ExpectedManifestSha256",
                    "A" * 64,
                ],
                cwd=repo,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn(
                "must be exactly 64 lowercase hexadecimal characters",
                completed.stdout + completed.stderr,
            )
            self.assertNotIn("implementation payload manifest is missing", completed.stdout + completed.stderr)

    def test_verifier_rejects_uppercase_sidecar_and_manifest_row_hashes(self):
        for attack in ("sidecar", "manifest-row"):
            with self.subTest(attack=attack), tempfile.TemporaryDirectory(
                dir=I1 / "tests"
            ) as temporary:
                repo = Path(temporary) / "repo"
                tools = repo / "s0-lab" / "i1" / "tools"
                verification = repo / "s0-lab" / "i1" / "verification"
                package = repo / "s0-lab" / "i1" / "implementation" / "s0_i1"
                tools.mkdir(parents=True)
                verification.mkdir(parents=True)
                package.mkdir(parents=True)
                script = tools / "verify-i1.ps1"
                script.write_bytes((I1 / "tools" / "verify-i1.ps1").read_bytes())
                candidate = package / "__init__.py"
                candidate_bytes = b"# public sentinel\n"
                candidate.write_bytes(candidate_bytes)
                row_hash = hashlib.sha256(candidate_bytes).hexdigest()
                if attack == "manifest-row":
                    row_hash = row_hash.upper()
                manifest_bytes = (
                    f"{row_hash}  implementation/s0_i1/__init__.py\n".encode("ascii")
                )
                manifest_path = verification / "implementation-files.sha256"
                manifest_path.write_bytes(manifest_bytes)
                manifest_hash = hashlib.sha256(manifest_bytes).hexdigest()
                sidecar_hash = (
                    manifest_hash.upper() if attack == "sidecar" else manifest_hash
                )
                (verification / "implementation-manifest.sha256").write_bytes(
                    f"{sidecar_hash}  implementation-files.sha256\n".encode("ascii")
                )
                completed = subprocess.run(
                    [
                        "powershell",
                        "-NoProfile",
                        "-ExecutionPolicy",
                        "Bypass",
                        "-File",
                        str(script),
                        "-ExpectedManifestSha256",
                        manifest_hash,
                    ],
                    cwd=repo,
                    capture_output=True,
                    text=True,
                    timeout=30,
                    check=False,
                )
                self.assertNotEqual(completed.returncode, 0)
                expected_message = (
                    "manifest sidecar-format check failed"
                    if attack == "sidecar"
                    else "implementation manifest row-format check failed"
                )
                self.assertIn(expected_message, completed.stdout + completed.stderr)

    def test_verifier_independently_labels_exact_text_checks(self):
        source = (I1 / "tools" / "verify-i1.ps1").read_text(encoding="utf-8")
        for label in (
            ":non-empty",
            ":BOM(EF-BB-BF)",
            ":UTF-8",
            ":LF-only",
            ":final-LF",
            ":trailing-whitespace",
            ":ASCII",
            "manifest-sidecar:format",
            "manifest-sidecar:corroborates-external-anchor",
        ):
            with self.subTest(label=label):
                self.assertIn(label, source)
        self.assertIn(
            "$Bytes[0] -eq 0xef -and $Bytes[1] -eq 0xbb -and $Bytes[2] -eq 0xbf",
            source,
        )

    def test_coordinated_payload_manifest_sidecar_rewrite_fails_before_import(self):
        with tempfile.TemporaryDirectory(
            dir=I1 / "tests"
        ) as temporary:
            repo = Path(temporary) / "repo"
            tools = repo / "s0-lab" / "i1" / "tools"
            verification = repo / "s0-lab" / "i1" / "verification"
            package = repo / "s0-lab" / "i1" / "implementation" / "s0_i1"
            tools.mkdir(parents=True)
            verification.mkdir(parents=True)
            package.mkdir(parents=True)
            script = tools / "verify-i1.ps1"
            script.write_bytes((I1 / "tools" / "verify-i1.ps1").read_bytes())
            marker = repo / "imported.marker"
            candidate = package / "__init__.py"
            original = b"# original public sentinel\n"
            candidate.write_bytes(original)
            relative = "implementation/s0_i1/__init__.py"
            initial_manifest = (
                f"{hashlib.sha256(original).hexdigest()}  {relative}\n".encode(
                    "ascii"
                )
            )
            expected = hashlib.sha256(initial_manifest).hexdigest()

            corrupted = (
                f"from pathlib import Path\nPath({str(marker)!r}).write_text('executed')\n"
            ).encode("utf-8")
            candidate.write_bytes(corrupted)
            rewritten_manifest = (
                f"{hashlib.sha256(corrupted).hexdigest()}  {relative}\n".encode(
                    "ascii"
                )
            )
            manifest_path = verification / "implementation-files.sha256"
            manifest_path.write_bytes(rewritten_manifest)
            rewritten_hash = hashlib.sha256(rewritten_manifest).hexdigest()
            (verification / "implementation-manifest.sha256").write_bytes(
                f"{rewritten_hash}  implementation-files.sha256\n".encode("ascii")
            )
            completed = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-ExecutionPolicy",
                    "Bypass",
                    "-File",
                    str(script),
                    "-ExpectedManifestSha256",
                    expected,
                ],
                cwd=repo,
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            self.assertNotEqual(completed.returncode, 0)
            self.assertIn(
                "external expected-manifest check failed",
                completed.stdout + completed.stderr,
            )
            self.assertFalse(marker.exists())

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

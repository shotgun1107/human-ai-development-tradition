from __future__ import annotations

import ast
import copy
import hashlib
import inspect
import io
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch


WORKSPACE = Path(__file__).resolve().parents[3]
IMPLEMENTATION = WORKSPACE / "s0-lab" / "i0" / "implementation"
sys.path.insert(0, str(IMPLEMENTATION))

import s0_i0.transform as transform_module  # noqa: E402
from s0_i0.answer_validation import (  # noqa: E402
    validate_answer_candidate_bytes,
    validate_public_answer_file,
)
from s0_i0.authentication import ANSWER_SCHEMA_PATH  # noqa: E402
from s0_i0.cli import main as cli_main  # noqa: E402
from s0_i0.integrity import (  # noqa: E402
    IntegrityError,
    aggregate_facts,
    sha256_bytes,
    verify_public_bundle,
)
from s0_i0.json_validation import validate_instance  # noqa: E402
from s0_i0.paths import UnsafePathError, resolve_workspace_path  # noqa: E402
from s0_i0.schema_suite import (  # noqa: E402
    FROZEN_SCHEMA_HASHES,
    audit_broader_upstream_id_impact,
    validate_public_schema_instances,
)
from s0_i0.transform import PROFILES, TransformationError, transform_canonical  # noqa: E402


BUNDLE = WORKSPACE / "s0-lab" / "public-practice" / "v0.1"
def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class FrozenInputTests(unittest.TestCase):
    def test_all_controlling_hashes_match_before_use(self):
        expected = {
            "AGENTS.md": "14f1d05cca42fd4d7930cad2537bb34bcec17ebcb22630e2f004798123f7a5a2",
            "s0-lab/control/i0/i0-gate-record.md": "835471a3c6956081b33d1b978d46100204a4fe9aa0b852ce56504f170b119c49",
            "s0-lab/control/i0/i0-implementation-brief.md": "166d29683aedee9334e5516c84db73f2f247ca9cc5e5627a387c596bae2340b3",
            "s0-lab/control/i0/i0-environment-record.md": "7504d74a6b3ce5d594c3d6ab5c22e16c1a5db327eee021ae1ed9f2b79dff9266",
            "s0-lab/control/i0/i0-session-record.md": "c5e489bb732fcc3abafc32280d07509e33d876cd218f1acc1862778b747fa922",
            "s0-lab/control/s0-protocol-v0.3.md": "b1a7216398e51d75fe35a2c54a878d03c7f1163c450e6b8119fbb2ee1e3c0b8c",
            "s0-lab/control/f0-public/f0-public-v0.1-freeze-record.md": "3f8e3ef230d7cad298ac555e045d8e9b5755ea82e8f33154d1685d8b526f8a6c",
            "s0-lab/public-practice/v0.1/bundle-files.sha256": "993f44896184617035609f117060c3a16d36bd44a7284178de3c5dd0ea6ec47f",
        }
        for schema_rel, digest in FROZEN_SCHEMA_HASHES.items():
            expected[f"s0-lab/control/{schema_rel}"] = digest
        for relative, digest in expected.items():
            with self.subTest(relative=relative):
                self.assertEqual(hashlib.sha256((WORKSPACE / relative).read_bytes()).hexdigest(), digest)


class SchemaTests(unittest.TestCase):
    def test_designated_eleven_detect_four_defects_not_conformance_pass(self):
        result = validate_public_schema_instances(WORKSPACE)
        self.assertEqual(result["schema_count"], 11)
        # Frozen input defect discovered by I0: four B2 package IDs are 13 chars
        # after PKG-, while run-manifest.schema.json allows exactly 12.
        self.assertEqual(result["error_count"], 4)
        failures = [item for item in result["results"] if item["errors"]]
        self.assertEqual([item["schema"] for item in failures], ["sm1/run-manifest.schema.json"])
        self.assertTrue(all("does not match" in error["message"] for error in failures[0]["errors"]))

    def test_broader_upstream_impact_is_twenty_related_errors(self):
        result = audit_broader_upstream_id_impact(WORKSPACE)
        self.assertEqual(result["designated_error_count"], 4)
        self.assertEqual(result["additional_error_count"], 16)
        self.assertEqual(result["related_error_count"], 20)
        self.assertEqual([item["error_count"] for item in result["results"]], [4, 8, 8])

    def test_schema_suite_authenticates_bundle_before_reading_instances(self):
        with patch(
            "s0_i0.schema_suite.verify_public_bundle",
            side_effect=IntegrityError("authentication sentinel"),
        ) as authenticate:
            with self.assertRaisesRegex(IntegrityError, "authentication sentinel"):
                validate_public_schema_instances(WORKSPACE)
        authenticate.assert_called_once_with(WORKSPACE)

    def test_format_checker_is_explicitly_effective(self):
        schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "properties": {"when": {"type": "string", "format": "date-time"}},
            "required": ["when"],
        }
        errors = validate_instance({"when": "not-a-date"}, schema)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].instance_path, "$.when")

    def test_validation_errors_are_stably_sorted_and_host_path_free(self):
        schema = {"type": "object", "properties": {"a": {"type": "integer"}, "b": {"type": "integer"}}}
        first = [error.as_dict() for error in validate_instance({"a": "x", "b": "y"}, schema)]
        second = [error.as_dict() for error in validate_instance({"a": "x", "b": "y"}, schema)]
        self.assertEqual(first, second)
        self.assertEqual(first, sorted(first, key=lambda item: (item["category"], item["instance_path"], item["schema_path"], item["message"])))
        self.assertNotIn(str(WORKSPACE), json.dumps(first))


class IntegrityTests(unittest.TestCase):
    def test_bundle_file_set_hash_json_aggregate_and_byte_integrity(self):
        result = verify_public_bundle(WORKSPACE)
        self.assertEqual(result["manifest_entries"], 90)
        self.assertEqual(result["json_files"], 56)
        self.assertEqual(len(result["packages"]), 8)
        self.assertTrue(all(ratio <= 0.15 for ratio in result["max_byte_ratios"].values()))

    def test_published_aggregate_algorithm(self):
        canonical = read_json(BUNDLE / "blocks" / "BLK-PRACTICE0001" / "canonical-input.json")
        self.assertEqual(
            aggregate_facts(canonical["facts"]),
            (
                "e0b8581ba242bc992c467fabb48dfa791f50fda926d8368c973de6f632572379",
                "1e3d1371bb74e48536c692eee6606f714d43f9d181a48e1c890b9682c9ff2a0b",
            ),
        )


class TransformationTests(unittest.TestCase):
    BLOCKS = (
        ("BLK-PRACTICE0001", "B1MOSS001"),
        ("BLK-PRACTICE0002", "B2EMBER001"),
    )

    def test_exact_eight_package_regeneration_and_two_run_determinism(self):
        for block, suffix in self.BLOCKS:
            canonical = read_json(BUNDLE / "blocks" / block / "canonical-input.json")
            for profile in sorted(PROFILES):
                with self.subTest(block=block, profile=profile):
                    first = transform_canonical(canonical, profile)
                    second = transform_canonical(canonical, profile)
                    expected = (BUNDLE / "packages" / f"{profile}{suffix}" / "input.json").read_bytes()
                    self.assertEqual(first, second)
                    self.assertEqual(first, expected)
                    self.assertEqual(sha256_bytes(first), sha256_bytes(expected))

    def test_fact_record_project_timestamp_and_text_equality_all_profiles(self):
        for block, _ in self.BLOCKS:
            canonical = read_json(BUNDLE / "blocks" / block / "canonical-input.json")
            expected_facts = canonical["facts"]
            for profile in sorted(PROFILES):
                with self.subTest(block=block, profile=profile):
                    package = json.loads(transform_canonical(canonical, profile))
                    self.assertEqual(package["facts"], expected_facts)

    def test_transform_api_has_no_oracle_or_scoring_input(self):
        self.assertEqual(list(inspect.signature(transform_canonical).parameters), ["canonical", "profile"])
        source = inspect.getsource(transform_module)
        tree = ast.parse(source)
        imported_roots = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported_roots.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported_roots.add(node.module.split(".")[0])
        self.assertLessEqual(
            imported_roots,
            {"__future__", "collections", "copy", "json", "re", "typing"},
        )
        lowered = source.lower()
        for banned in ("pathlib", "open(", "socket", "requests", "urllib", "subprocess", "oracle", "scoring"):
            with self.subTest(banned=banned):
                self.assertNotIn(banned, lowered)


class AnswerValidationTests(unittest.TestCase):
    def _case(self, block: str):
        if block == "B1":
            answer_rel = "s0-lab/public-practice/v0.1/examples/answer.json"
            questions_rel = "s0-lab/public-practice/v0.1/runner/BLK-PRACTICE0001/questions.json"
            input_rel = "s0-lab/public-practice/v0.1/packages/P01B1MOSS001/input.json"
        else:
            answer_rel = "s0-lab/public-practice/v0.1/blocks/BLK-PRACTICE0002/expected-answer-P01.json"
            questions_rel = "s0-lab/public-practice/v0.1/runner/BLK-PRACTICE0002/questions.json"
            input_rel = "s0-lab/public-practice/v0.1/packages/P01B2EMBER001/input.json"
        answer = read_json(WORKSPACE / answer_rel)
        return answer, answer_rel, questions_rel, input_rel

    def _errors(self, answer, questions_rel, input_rel):
        raw = json.dumps(answer, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        return validate_answer_candidate_bytes(
            WORKSPACE,
            raw,
            answer_schema=ANSWER_SCHEMA_PATH,
            questions=questions_rel,
            input_package=input_rel,
        )

    def _assert_forbidden(self, reason: str):
        base, _, questions, input_path = self._case("B1")
        candidate = copy.deepcopy(base)
        candidate["answers"][0]["short_reason"] = reason
        self.assertIn(
            "forbidden-disclosure",
            {error.category for error in self._errors(candidate, questions, input_path)},
        )

    def test_valid_public_answers_for_both_blocks(self):
        for block in ("B1", "B2"):
            with self.subTest(block=block):
                _, answer, questions, input_path = self._case(block)
                self.assertEqual(
                    validate_public_answer_file(
                        WORKSPACE,
                        answer,
                        answer_schema=ANSWER_SCHEMA_PATH,
                        questions=questions,
                        input_package=input_path,
                    ),
                    [],
                )

    def test_missing_duplicate_and_extra_questions(self):
        base, _, questions, input_path = self._case("B1")
        missing = copy.deepcopy(base)
        missing["answers"].pop()
        self.assertIn("question-missing", {e.category for e in self._errors(missing, questions, input_path)})
        duplicate = copy.deepcopy(base)
        duplicate["answers"][-2] = copy.deepcopy(duplicate["answers"][-1])
        duplicate["answers"][-2]["short_reason"] += " Additional public reason."
        self.assertIn("question-duplicate", {e.category for e in self._errors(duplicate, questions, input_path)})
        extra = copy.deepcopy(base)
        item = copy.deepcopy(extra["answers"][-1])
        item["question_id"] = "Q-B1-08"
        extra["answers"][-1] = item
        self.assertIn("question-extra", {e.category for e in self._errors(extra, questions, input_path)})

    def test_invalid_option_bad_citation_and_bad_affected_id(self):
        base, _, questions, input_path = self._case("B1")
        invalid_option = copy.deepcopy(base)
        invalid_option["answers"][0]["decision_option_id"] = "OPT-B1-UNKNOWN"
        self.assertIn("decision-option", {e.category for e in self._errors(invalid_option, questions, input_path)})
        bad_citation = copy.deepcopy(base)
        bad_citation["answers"][0]["cited_record_ids"] = ["R-B1-99"]
        self.assertIn("citation-id", {e.category for e in self._errors(bad_citation, questions, input_path)})
        bad_affected = copy.deepcopy(base)
        bad_affected["answers"][3]["affected_record_ids"] = ["R-B1-99"]
        self.assertIn("affected-id", {e.category for e in self._errors(bad_affected, questions, input_path)})

    def test_unsorted_ids(self):
        base, _, questions, input_path = self._case("B1")
        unsorted = copy.deepcopy(base)
        unsorted["answers"][1]["cited_record_ids"] = ["R-B1-04", "R-B1-02", "R-B1-03"]
        self.assertIn("citation-order", {e.category for e in self._errors(unsorted, questions, input_path)})

    def test_forbidden_each_actual_profile_field(self):
        fields = (
            "ordering_source",
            "boundary_rule",
            "event_order",
            "project_groups",
            "source_record_id",
            "supporting_fact_ids",
            "from_record_id",
            "to_record_id",
            "relation_dictionary",
            "relations",
        )
        for field in fields:
            with self.subTest(field=field):
                self._assert_forbidden(f"The {field} field proves this answer.")

    def test_forbidden_package_profile_identifier(self):
        self._assert_forbidden("P01B1MOSS001 makes this answer preferred.")

    def test_forbidden_fact_ids_field(self):
        self._assert_forbidden("fact_ids")

    def test_forbidden_state_field(self):
        self._assert_forbidden("state")

    def test_forbidden_scope_field(self):
        self._assert_forbidden("scope")

    def test_forbidden_code_field(self):
        self._assert_forbidden("code")

    def test_forbidden_s0_readiness_claim(self):
        self._assert_forbidden("This proves the system is S0 ready.")

    def test_forbidden_implementation_completion_claim(self):
        self._assert_forbidden("The implementation is complete and operational.")

    def test_affected_policy_and_citation_policy(self):
        base, _, questions, input_path = self._case("B1")
        forbidden = copy.deepcopy(base)
        forbidden["answers"][0]["affected_record_ids"] = ["R-B1-01"]
        self.assertIn("affected-forbidden", {e.category for e in self._errors(forbidden, questions, input_path)})
        required = copy.deepcopy(base)
        required["answers"][3]["affected_record_ids"] = []
        self.assertIn("affected-required", {e.category for e in self._errors(required, questions, input_path)})
        citation = copy.deepcopy(base)
        citation["answers"][0]["cited_record_ids"] = []
        self.assertIn("citation-required", {e.category for e in self._errors(citation, questions, input_path)})


class PathAndCliTests(unittest.TestCase):
    def _run_cli(self, args):
        old_cwd = Path.cwd()
        stdout = io.StringIO()
        stderr = io.StringIO()
        try:
            os.chdir(WORKSPACE)
            with redirect_stdout(stdout), redirect_stderr(stderr):
                code = cli_main(args)
        finally:
            os.chdir(old_cwd)
        return code, stdout.getvalue(), stderr.getvalue()

    def _valid_answer_args(self, answer="s0-lab/public-practice/v0.1/examples/answer.json"):
        return [
            "answer-check",
            "--answer",
            answer,
            "--answer-schema",
            ANSWER_SCHEMA_PATH,
            "--questions",
            "s0-lab/public-practice/v0.1/runner/BLK-PRACTICE0001/questions.json",
            "--input",
            "s0-lab/public-practice/v0.1/packages/P01B1MOSS001/input.json",
        ]

    def test_absolute_and_traversal_paths_are_rejected(self):
        with self.assertRaises(UnsafePathError):
            resolve_workspace_path(WORKSPACE, str((WORKSPACE / "AGENTS.md").resolve()))
        with self.assertRaises(UnsafePathError):
            resolve_workspace_path(WORKSPACE, "s0-lab/../AGENTS.md")

    def test_symlink_escape_is_rejected_when_supported(self):
        with tempfile.TemporaryDirectory(dir=WORKSPACE / "s0-lab" / "i0" / "tests") as temp_dir:
            link = Path(temp_dir) / "escape.json"
            external = Path(
                r"C:\Users\SSAFY\AppData\Local\Temp\ai-development-tradition-i0-venv-c9f68f3\Scripts\python.exe"
            )
            try:
                os.symlink(external, link)
            except OSError as exc:
                self.skipTest(f"symlink creation unavailable: {type(exc).__name__}")
            relative = link.relative_to(WORKSPACE).as_posix()
            with self.assertRaises(UnsafePathError):
                resolve_workspace_path(WORKSPACE, relative)

    def test_cli_returns_nonzero_for_absolute_path_failure(self):
        code, _, error = self._run_cli([
            "transform",
            "--canonical",
            str((BUNDLE / "blocks" / "BLK-PRACTICE0001" / "canonical-input.json").resolve()),
            "--profile",
            "P01",
            "--output",
            "s0-lab/i0/verification/unused.json",
        ])
        self.assertEqual(code, 2)
        self.assertEqual(json.loads(error)["status"], "error")

    def test_transform_cli_rejects_authenticated_but_noncanonical_public_json(self):
        code, _, _ = self._run_cli([
            "transform",
            "--canonical",
            "s0-lab/public-practice/v0.1/examples/answer.json",
            "--profile",
            "P01",
            "--output",
            "s0-lab/i0/verification/unused.json",
        ])
        self.assertEqual(code, 2)

    def test_answer_cli_rejects_substituted_answer_schema_questions_and_input(self):
        attacks = {
            "answer": (2, "s0-lab/public-practice/v0.1/blocks/BLK-PRACTICE0001/public-oracle.json"),
            "schema": (4, "s0-lab/control/sm1/question-options.schema.json"),
            "questions": (6, "s0-lab/public-practice/v0.1/blocks/BLK-PRACTICE0001/question-options.json"),
            "input": (8, "s0-lab/public-practice/v0.1/blocks/BLK-PRACTICE0001/canonical-input.json"),
        }
        for label, (index, replacement) in attacks.items():
            with self.subTest(label=label):
                args = self._valid_answer_args()
                args[index] = replacement
                code, _, error = self._run_cli(args)
                self.assertEqual(code, 2)
                self.assertEqual(json.loads(error)["status"], "error")

    def test_untrusted_answer_candidate_below_i0_is_allowed(self):
        with tempfile.TemporaryDirectory(dir=WORKSPACE / "s0-lab" / "i0" / "tests") as temp_dir:
            candidate = Path(temp_dir) / "candidate.json"
            candidate.write_bytes((BUNDLE / "examples" / "answer.json").read_bytes())
            code, output, error = self._run_cli(
                self._valid_answer_args(candidate.relative_to(WORKSPACE).as_posix())
            )
            self.assertEqual(code, 0, error)
            self.assertEqual(json.loads(output)["status"], "pass")

    def test_missing_file_error_is_json_and_leaks_no_host_path(self):
        code, _, error = self._run_cli(
            self._valid_answer_args("s0-lab/i0/missing-candidate.json")
        )
        self.assertEqual(code, 2)
        parsed = json.loads(error)
        self.assertEqual(parsed["status"], "error")
        self.assertNotIn(str(WORKSPACE), error)
        self.assertNotIn(WORKSPACE.name, error)
        self.assertNotIn("C:\\Users", error)

    def test_verify_internal_missing_file_is_path_free_json(self):
        leaked = str(WORKSPACE / "simulated-missing.json")
        simulated = FileNotFoundError(2, "No such file", leaked)
        with patch("pathlib.Path.read_bytes", side_effect=simulated):
            code, output, error = self._run_cli(["verify"])
        self.assertEqual(code, 1)
        self.assertEqual(error, "")
        parsed = json.loads(output)
        self.assertEqual(parsed["status"], "fail")
        self.assertEqual(parsed["errors"][0]["category"], "FileNotFoundError")
        self.assertNotIn(str(WORKSPACE), output)
        self.assertNotIn(WORKSPACE.name, output)
        self.assertNotIn("C:\\Users", output)

    def test_malformed_transform_leaves_no_output_residue(self):
        canonical = "s0-lab/public-practice/v0.1/blocks/BLK-PRACTICE0001/canonical-input.json"
        with tempfile.TemporaryDirectory(dir=WORKSPACE / "s0-lab" / "i0" / "tests") as temp_dir:
            output = Path(temp_dir) / "result.json"
            with patch(
                "s0_i0.cli.transform_canonical",
                side_effect=TransformationError("malformed canonical"),
            ):
                code, _, _ = self._run_cli([
                    "transform",
                    "--canonical",
                    canonical,
                    "--profile",
                    "P01",
                    "--output",
                    output.relative_to(WORKSPACE).as_posix(),
                ])
            self.assertEqual(code, 2)
            self.assertFalse(output.exists())

    def test_existing_transform_output_is_never_overwritten(self):
        canonical = "s0-lab/public-practice/v0.1/blocks/BLK-PRACTICE0001/canonical-input.json"
        with tempfile.TemporaryDirectory(dir=WORKSPACE / "s0-lab" / "i0" / "tests") as temp_dir:
            output = Path(temp_dir) / "result.json"
            output.write_bytes(b"sentinel")
            code, _, error = self._run_cli([
                "transform",
                "--canonical",
                canonical,
                "--profile",
                "P01",
                "--output",
                output.relative_to(WORKSPACE).as_posix(),
            ])
            self.assertEqual(code, 2)
            self.assertEqual(output.read_bytes(), b"sentinel")
            self.assertIn("overwrite is forbidden", error)

    def test_cli_schema_failure_is_nonzero_and_machine_readable(self):
        code, output, _ = self._run_cli(["schema-check"])
        self.assertEqual(code, 1)
        parsed = json.loads(output)
        self.assertEqual(parsed["error_count"], 4)
        self.assertEqual(parsed["broader_upstream_impact"]["related_error_count"], 20)

    def test_cli_usage_error_is_json(self):
        code, _, error = self._run_cli(["transform"])
        self.assertEqual(code, 2)
        self.assertEqual(json.loads(error)["status"], "error")


if __name__ == "__main__":
    unittest.main()

"""Bounded CLI guard/control-flow regression; no complete bundle or S0 run."""
from __future__ import annotations

import ast
import contextlib
import difflib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import time
import types
import unittest
from unittest.mock import patch

TEST_PATH = Path(__file__).resolve()
CANDIDATE = TEST_PATH.parents[1]
PROJECT = CANDIDATE.parents[2]
ORIGINAL = PROJECT / "s0-lab/i0"
MANIFEST = ORIGINAL / "verification/implementation-files.sha256"
BUNDLE = Path("s0-lab/public-practice/v0.1")
PUBLIC_MANIFEST = PROJECT / BUNDLE / "bundle-files.sha256"
PUBLIC_ANSWER = PROJECT / BUNDLE / "examples/answer.json"
TMP = CANDIDATE / "verification/tmp"
EXPECTED_HEAD = "cc76d7e82aeb51dfdc7baba3da0f7993ab2da61a"
EXPECTED_TREE = "82c02f37fd13ecfc8c7b888bb66127989b6d4f34"
EXPECTED_BRANCH = "codex/windows-build-toolchain-environment-v0.1"
PIN_AGENTS = "4aac0c255dea03b85f6fb98b0b89f5b3c3f348e42c4dcaaf423411b818e3a065"
PIN_MANIFEST = "f57514f96a2c30366cdf1f1414524711da20c9410186b3017e3dbf902bb612ae"
PIN_CLI = "819edaf785558b620aa7b79036560d4fb895d7ce513a5cc4173fad04df8e43f9"
PIN_BUNDLE = "e41ee6c71169df646e3c8c0b0e8f3d77e7871d939f651b86a52ea5696feeb637"
PIN_ANSWER = "e66d631210fae9519cd94e618061674f68ac869b04fc38416c8ee50a3f85b43f"
PYTHON = "C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe"
OBSERVATIONS: list[dict] = []
READ_SCOPE: set[Path] | None = None
READ_LOG: list[str] = []
DEPENDENCY_USE: list[str] = []


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_pin(path, expected):
    actual = digest(path)
    if actual != expected:
        raise RuntimeError("frozen input pin mismatch: " + path.relative_to(PROJECT).as_posix())
    return actual


def git_identity():
    result = {}
    for label, args, expected in (
        ("branch", ["branch", "--show-current"], EXPECTED_BRANCH),
        ("head", ["rev-parse", "HEAD"], EXPECTED_HEAD),
        ("tree", ["rev-parse", "HEAD^{tree}"], EXPECTED_TREE),
    ):
        proc = subprocess.run(["git", *args], cwd=PROJECT, stdout=subprocess.PIPE,
                              stderr=subprocess.DEVNULL, text=True, check=False)
        if proc.returncode or proc.stdout.strip() != expected:
            raise RuntimeError("Git identity mismatch: " + label)
        result[label] = proc.stdout.strip()
    return result


def authenticate_inputs():
    pins = {}
    for path, expected in ((PROJECT / "AGENTS.md", PIN_AGENTS), (MANIFEST, PIN_MANIFEST),
                           (PUBLIC_MANIFEST, PIN_BUNDLE), (PUBLIC_ANSWER, PIN_ANSWER)):
        pins[path.relative_to(PROJECT).as_posix()] = check_pin(path, expected)
    rows = {}
    for line in MANIFEST.read_text(encoding="utf-8").splitlines():
        expected, relative = line.split("  ", 1)
        if relative == "requirements.txt" or (
            relative.startswith("implementation/s0_i0/") and relative.endswith(".py")
            and relative.count("/") == 2
        ):
            rows[relative] = expected
    if len(rows) != 12:
        raise RuntimeError("source manifest row count mismatch")
    for root in (ORIGINAL, CANDIDATE):
        for relative, expected in rows.items():
            if root == CANDIDATE and relative == "implementation/s0_i0/cli.py":
                expected = PIN_CLI
            path = root / relative
            pins[path.relative_to(PROJECT).as_posix()] = check_pin(path, expected)
        # Inventory only exact implementation directories; unknown names never printed.
        for directory, allowed in (
            (root / "implementation", {"s0_i0"}),
            (root / "implementation/s0_i0", {Path(r).name for r in rows if r.endswith(".py")}),
        ):
            entries = list(directory.iterdir())
            if {p.name for p in entries} != allowed:
                raise RuntimeError("implementation inventory mismatch; filenames suppressed")
            if any(p.is_symlink() or p.is_junction() for p in entries):
                raise RuntimeError("implementation reparse entry detected")
    return {"git": git_identity(), "pins": pins, "source_count_each": len(rows),
            "implementation_inventory": "exact; no extra entries"}


def forbidden_dependency(*args, **kwargs):
    DEPENDENCY_USE.append("jsonschema operation")
    raise AssertionError("jsonschema import-only double cannot validate anything")


def install_dependency_double():
    if importlib.util.find_spec("jsonschema") is not None:
        raise RuntimeError("unexpected jsonschema visibility; re-freeze dependency inputs")
    dependency = types.ModuleType("jsonschema")
    exceptions = types.ModuleType("jsonschema.exceptions")
    class ForbiddenValidator:
        def __init__(self, *args, **kwargs):
            forbidden_dependency()
        check_schema = staticmethod(forbidden_dependency)
    dependency.Draft202012Validator = ForbiddenValidator
    dependency.FormatChecker = forbidden_dependency
    exceptions.SchemaError = type("SchemaError", (Exception,), {})
    exceptions.ValidationError = type("ValidationError", (Exception,), {})
    dependency.exceptions = exceptions
    sys.modules["jsonschema"] = dependency
    sys.modules["jsonschema.exceptions"] = exceptions


def load_candidate():
    package_dir = CANDIDATE / "implementation/s0_i0"
    spec = importlib.util.spec_from_file_location("s0_i0", package_dir / "__init__.py",
                                                submodule_search_locations=[str(package_dir)])
    package = importlib.util.module_from_spec(spec)
    sys.modules["s0_i0"] = package
    spec.loader.exec_module(package)
    import s0_i0.cli as cli
    import s0_i0.authentication as authentication
    import s0_i0.integrity as integrity
    baseline_path = ORIGINAL / "implementation/s0_i0/cli.py"
    base_spec = importlib.util.spec_from_file_location("s0_i0.baseline_cli", baseline_path)
    baseline = importlib.util.module_from_spec(base_spec)
    sys.modules[base_spec.name] = baseline
    base_spec.loader.exec_module(baseline)
    return cli, authentication, integrity, baseline


def loaded_paths():
    return {name: str(Path(module.__file__).resolve())
            for name, module in sorted(sys.modules.items())
            if getattr(module, "__file__", None)}


def scoped_io_audit(event, args):
    if READ_SCOPE is None:
        return
    if event == "open":
        raw = args[0]
        if not isinstance(raw, (str, bytes, os.PathLike)):
            raise AssertionError("unexpected file descriptor access during CLI case")
        path = Path(os.fsdecode(raw)).absolute()
        if path not in READ_SCOPE:
            raise AssertionError("forbidden content read during CLI case")
        mode, flags = args[1], args[2]
        if (isinstance(mode, str) and any(x in mode for x in "wax+")) or (
            isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT)
        ):
            raise AssertionError("unexpected write during CLI case")
        READ_LOG.append(path.relative_to(TMP).as_posix())
    elif event in {"subprocess.Popen", "os.system", "socket.connect", "socket.bind"}:
        raise AssertionError("forbidden process/network action during CLI case")


class DispatchObserved(Exception):
    """A spy reached the delegated operation; this is never a success result."""


class CliAuthenticationTests(unittest.TestCase):
    def setUp(self):
        self.work = TMP / self._testMethodName
        self.work.mkdir(parents=True, exist_ok=False)
        self.bundle = self.work / BUNDLE
        (self.bundle / "examples").mkdir(parents=True)
        self.manifest = self.bundle / "bundle-files.sha256"
        self.answer = self.bundle / "examples/answer.json"
        self.manifest.write_bytes(PUBLIC_MANIFEST.read_bytes())
        self.answer.write_bytes(PUBLIC_ANSWER.read_bytes())

    def tearDown(self):
        cleanup(self.work)

    def run_case(self, command, scenario, *, baseline=False):
        global READ_SCOPE
        module = BASELINE if baseline else CLI
        if scenario == "manifest_altered":
            self.manifest.write_bytes(self.manifest.read_bytes() + b"\n")
        elif scenario in {"content_matching_manifest", "content_only"}:
            self.answer.write_bytes(self.answer.read_bytes() + b" ")
            if scenario == "content_matching_manifest":
                new_digest = digest(self.answer)
                old = (PIN_ANSWER + "  examples/answer.json").encode()
                replacement = (new_digest + "  examples/answer.json").encode()
                raw = self.manifest.read_bytes()
                self.assertEqual(raw.count(old), 1)
                self.manifest.write_bytes(raw.replace(old, replacement))
        elif scenario == "missing":
            self.manifest.unlink()
        elif scenario == "malformed":
            self.manifest.write_bytes(b"malformed manifest\n")
        events = []
        real_guard = AUTH._authenticate_bundle_manifest
        real_parser = AUTH.parse_bundle_manifest
        real_read_bytes = Path.read_bytes
        def guard(root):
            events.append("guard")
            return real_guard(root)
        def parser(root):
            events.append("parse_manifest")
            return real_parser(root)
        def delegated(root):
            events.append("handler")
            if scenario == "content_only":
                # Deliberately narrow handler double, not verify_public_bundle.
                entries = INTEGRITY.parse_bundle_manifest(root / BUNDLE)
                if INTEGRITY.sha256_bytes((root / BUNDLE / "examples/answer.json").read_bytes()) != entries["examples/answer.json"]:
                    raise INTEGRITY.IntegrityError("narrow-handler example digest mismatch")
            raise DispatchObserved("handler spy reached; full operation not run")
        def read_bytes(path):
            if scenario == "unreadable" and path == self.manifest:
                raise PermissionError(13, "permission denied", str(self.manifest))
            return real_read_bytes(path)
        handlers = {"integrity": "verify_public_bundle", "schema-check": "validate_public_schema_instances",
                    "verify": "build_public_verification_record"}
        out, err = io.StringIO(), io.StringIO()
        original_cwd = Path.cwd()
        start_read = len(READ_LOG)
        try:
            os.chdir(self.work)
            with contextlib.ExitStack() as stack:
                stack.enter_context(patch.object(module, handlers[command], side_effect=delegated))
                stack.enter_context(patch.object(AUTH, "parse_bundle_manifest", side_effect=parser))
                stack.enter_context(patch.object(Path, "read_bytes", read_bytes))
                if not baseline:
                    stack.enter_context(patch.object(module, "_authenticate_bundle_manifest", side_effect=guard))
                stack.enter_context(contextlib.redirect_stdout(out))
                stack.enter_context(contextlib.redirect_stderr(err))
                READ_SCOPE = {self.manifest, self.answer}
                code = module.main([command])
        finally:
            READ_SCOPE = None
            os.chdir(original_cwd)
        record = {"command": command, "scenario": scenario, "baseline_cli": baseline,
                  "events": events, "exit_code": code, "stdout": out.getvalue(),
                  "stderr_json": json.loads(err.getvalue()), "reads": READ_LOG[start_read:],
                  "handler_kind": "narrow example-digest double" if scenario == "content_only" else "raising dispatch spy",
                  "permission_case": "Path.read_bytes PermissionError injection" if scenario == "unreadable" else None}
        OBSERVATIONS.append(record)
        self.assertEqual(code, 2)
        self.assertEqual(out.getvalue(), "")
        self.assertNotIn(str(self.work), err.getvalue())
        self.assertNotIn("C:\\", err.getvalue())
        if baseline or scenario == "original":
            self.assertEqual(record["stderr_json"]["error"]["category"], "DispatchObserved")
            self.assertEqual(events, ["handler"] if baseline else ["guard", "parse_manifest", "handler"])
        elif scenario == "content_only":
            self.assertEqual(events, ["guard", "parse_manifest", "handler"])
            self.assertEqual(record["stderr_json"]["error"]["category"], "IntegrityError")
        else:
            self.assertEqual(events, ["guard"])
            expected = {"missing": "FileNotFoundError", "unreadable": "PermissionError"}.get(scenario, "AuthenticationError")
            self.assertEqual(record["stderr_json"]["error"]["category"], expected)

    def test_minimal_source_diff_and_content_check_wiring(self):
        old = (ORIGINAL / "implementation/s0_i0/cli.py").read_text(encoding="utf-8")
        new = (CANDIDATE / "implementation/s0_i0/cli.py").read_text(encoding="utf-8")
        expected = old.replace("from .authentication import PUBLIC_CANONICALS, authenticate_public_file\n",
            "from .authentication import (\n    PUBLIC_CANONICALS,\n    _authenticate_bundle_manifest,\n    authenticate_public_file,\n)\n", 1)
        expected = expected.replace("        workspace_root = Path.cwd().resolve(strict=True)\n",
            "        workspace_root = Path.cwd().resolve(strict=True)\n        if args.command in {\"integrity\", \"schema-check\", \"verify\"}:\n            _authenticate_bundle_manifest(workspace_root)\n", 1)
        self.assertEqual(new, expected)
        checks = {"integrity.py": ["sha256_bytes(raw) != expected", "disk != set(manifest)"],
                  "schema_suite.py": ["verify_public_bundle(workspace_root)"],
                  "verification.py": ["integrity = verify_public_bundle(workspace_root)", "schemas = validate_public_schema_instances(workspace_root)"]}
        for name, fragments in checks.items():
            candidate = CANDIDATE / "implementation/s0_i0" / name
            self.assertEqual(candidate.read_bytes(), (ORIGINAL / "implementation/s0_i0" / name).read_bytes())
            source = candidate.read_text(encoding="utf-8")
            ast.parse(source)
            for fragment in fragments:
                self.assertIn(fragment, source)

    def test_loaded_candidate_and_baseline_paths(self):
        for name, module in sys.modules.items():
            if name == "s0_i0" or name.startswith("s0_i0."):
                expected = ORIGINAL / "implementation/s0_i0/cli.py" if name.endswith("baseline_cli") else CANDIDATE / "implementation/s0_i0" / ("__init__.py" if name == "s0_i0" else name.rsplit(".", 1)[1] + ".py")
                self.assertEqual(Path(module.__file__).resolve(), expected.resolve())

    def test_jsonschema_double_is_explicit_and_fail_if_used(self):
        self.assertEqual(DEPENDENCY_USE, [])
        with self.assertRaisesRegex(AssertionError, "cannot validate"):
            sys.modules["jsonschema"].Draft202012Validator.check_schema({})
        self.assertEqual(DEPENDENCY_USE, ["jsonschema operation"])
        DEPENDENCY_USE.clear()

    def test_transform_keeps_existing_entry_without_new_guard(self):
        self.check_unguarded("transform", ["--canonical", "unused", "--profile", "P01", "--output", "unused"], "authenticate_public_file")

    def test_answer_keeps_existing_entry_without_new_guard(self):
        self.check_unguarded("answer-check", ["--answer", "unused", "--answer-schema", "unused", "--questions", "unused", "--input", "unused"], "validate_public_answer_file")

    def check_unguarded(self, command, args, existing_entry):
        global READ_SCOPE
        out, err = io.StringIO(), io.StringIO()
        with patch.object(CLI, "_authenticate_bundle_manifest", side_effect=AssertionError("forbidden new guard")) as guard, \
             patch.object(CLI, existing_entry, side_effect=DispatchObserved("existing branch observed")) as handler, \
             contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            try:
                READ_SCOPE = set()
                code = CLI.main([command, *args])
            finally:
                READ_SCOPE = None
        guard.assert_not_called()
        handler.assert_called_once()
        self.assertEqual(code, 2)
        self.assertEqual(json.loads(err.getvalue())["error"]["category"], "DispatchObserved")
        OBSERVATIONS.append({"command": command, "scenario": "existing-entry spy; no content read",
                             "new_guard_calls": 0, "existing_entry_calls": 1, "exit_code": code,
                             "stderr_json": json.loads(err.getvalue()), "actual_full_operation": "UNVERIFIED"})


def cleanup(target):
    # Remove only this test's known scratch descendant after absolute/reparse checks.
    absolute = target.absolute()
    if absolute == TMP or TMP not in absolute.parents or absolute.resolve() != absolute:
        raise RuntimeError("scratch cleanup containment failure")
    for path in (TMP, absolute, *absolute.rglob("*")):
        attributes = path.lstat().st_file_attributes
        if path.is_symlink() or path.is_junction() or attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT:
            raise RuntimeError("scratch cleanup reparse entry detected")
    shutil.rmtree(absolute)


for _command in ("integrity", "schema-check", "verify"):
    for _scenario in ("original", "manifest_altered", "content_matching_manifest", "missing", "unreadable", "malformed", "content_only"):
        def _case(self, command=_command, scenario=_scenario):
            self.run_case(command, scenario)
        setattr(CliAuthenticationTests, "test_" + _command.replace("-", "_") + "_" + _scenario, _case)
    def _baseline_case(self, command=_command):
        self.run_case(command, "content_matching_manifest", baseline=True)
    setattr(CliAuthenticationTests, "test_baseline_" + _command.replace("-", "_"), _baseline_case)


if __name__ == "__main__":
    started = time.time()
    if sys.version_info[:3] != (3, 12, 10) or not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
        raise RuntimeError("required CPython 3.12.10 -I -S -B flags absent")
    if Path(sys.executable).resolve() != Path(PYTHON).resolve():
        raise RuntimeError("interpreter path mismatch")
    pre = authenticate_inputs()
    initial_path = list(sys.path)
    install_dependency_double()
    CLI, AUTH, INTEGRITY, BASELINE = load_candidate()
    sys.addaudithook(scoped_io_audit)
    TMP.mkdir(parents=True, exist_ok=False)
    transcript = io.StringIO()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(CliAuthenticationTests)
    result = unittest.TextTestRunner(stream=transcript, verbosity=2).run(suite)
    post = authenticate_inputs()
    if pre != post:
        raise RuntimeError("input identity changed during tests")
    if list(TMP.iterdir()):
        raise RuntimeError("scratch cleanup incomplete")
    if TMP.resolve() != TMP.absolute() or TMP.is_symlink() or TMP.is_junction():
        raise RuntimeError("scratch root identity mismatch")
    TMP.rmdir()
    source_diff = "".join(difflib.unified_diff(
        (ORIGINAL / "implementation/s0_i0/cli.py").read_text(encoding="utf-8").splitlines(True),
        (CANDIDATE / "implementation/s0_i0/cli.py").read_text(encoding="utf-8").splitlines(True),
        fromfile="original/implementation/s0_i0/cli.py", tofile="candidate/implementation/s0_i0/cli.py"))
    report = {
        "candidate": "a04-i0-cli-authentication-v0.1", "role": "TEST/VERIFICATION",
        "claim": "bounded CLI guard and control-flow regression only",
        "command": '& "' + PYTHON + '" -I -S -B "' + str(TEST_PATH) + '"',
        "runtime": sys.version, "executable": sys.executable, "initial_sys_path": initial_path,
        "loaded_file_paths": loaded_paths(), "test_source_sha256": digest(TEST_PATH),
        "pre": pre, "post": post, "pre_post_equal": pre == post,
        "tests_run": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
        "skips": len(result.skipped), "successful": result.wasSuccessful(),
        "elapsed_seconds": round(time.time() - started, 3), "observations": OBSERVATIONS,
        "minimal_diff": source_diff, "scratch_removed": not TMP.exists(),
        "doubles": {
            "jsonschema": "in-memory import-only module and exceptions; validation/format operations raise AssertionError; real 4.26.0 unavailable under isolated flags",
            "command_handlers": "raising spies; original manifest dispatch is observed without returning a fake PASS",
            "content_check": "narrow handler reads only examples/answer.json and compares real stdlib SHA-256 to real parsed manifest row; not full verify_public_bundle",
            "permission": "exact scratch manifest Path.read_bytes PermissionError injection; not an OS ACL test",
            "baseline": "exact original cli.py loaded with byte-identical candidate dependencies; baseline bypasses manifest authentication",
        },
        "unexpected_dependency_operations": DEPENDENCY_USE,
        "limits": [
            "No complete 90-file integrity, schema, answer, transform, or verification execution; all remain UNVERIFIED.",
            "Only supplied public manifest metadata and example-answer bytes were copied/mutated; no S0/E0 inputs, oracle, scoring content, or provider calls.",
            "Trusted CPython, standard library and OS; interpreter/native/stdlib security closure is UNVERIFIED.",
            "Local workspace and pins remain mutable; no hostile import, authority-rebinding, concurrency, TOCTOU, or read-rebinding proof.",
            "Windows ACL, volume/root authenticity, junction/reparse attack defense, rename/replacement, retained handles and repository exclusion are UNVERIFIED; benign scratch checks only.",
            "No new URL, redirect, download, network, or external artifact authority was introduced or tested.",
            "TEST owns only harness/results/stdout/scratch; no candidate code changes, documentation verdict, independent acceptance, or Git mutation.",
        ],
    }
    (CANDIDATE / "verification/test-stdout.txt").write_text(transcript.getvalue(), encoding="utf-8", newline="\n")
    (CANDIDATE / "verification/test-results.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(transcript.getvalue(), end="")
    print(json.dumps({"tests": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
                      "skips": len(result.skipped), "scratch_removed": not TMP.exists()}))
    raise SystemExit(0 if result.wasSuccessful() else 1)

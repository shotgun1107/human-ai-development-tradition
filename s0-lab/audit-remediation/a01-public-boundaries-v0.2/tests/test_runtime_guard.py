"""Bounded F-02 regression checks and the A01 standard-library test runner."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys


CANDIDATE = Path(__file__).resolve().parents[1]
REPOSITORY = CANDIDATE.parents[2]
IMPLEMENTATION = CANDIDATE / "implementation"
BASELINE = REPOSITORY / "s0-lab/assembly-rehearsal/public-end-to-end-v0.1/implementation"
PYTHON = Path("C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe")
PINNED_HEAD = "cc76d7e82aeb51dfdc7baba3da0f7993ab2da61a"
PINNED_TREE = "82c02f37fd13ecfc8c7b888bb66127989b6d4f34"
PINNED_BRANCH = "codex/windows-build-toolchain-environment-v0.1"
PINS = {
    "s0_public_assembly_candidate/runtime_guard.py": "811f1df27a44d70948f3e37fedcba976189fd5b58ff61a6e029c14d74c768f7a",
    "s0_public_assembly_candidate/errors.py": "be97286ca93c68dba0611efca3795b896da64513aae3e2b053ab30b97f5f3a06",
    "s0_public_assembly_candidate/storage.py": "5564994d7ba4e10d18b0ef4ba5c3fca51fe35cce5609933cd04d10eebd1fcd2c",
    "s0_public_assembly_candidate/constants.py": "912a5e706751e43441da894edefca02f333b0c173fd1bf1c6647d75f2f353025",
    "s0_public_assembly_candidate/__init__.py": "6a925a2543dfa56ecd5de40c2e90d7577d5bc7ac941817396bd91ba4ebae078c",
    "s0_public_assembly_verifier/win32.py": "dd250e352431390885adfb4a95244d96622bc9546bd003f585b1afb579143f68",
    "s0_public_assembly_verifier/errors.py": "70ca57f1704d41e74ca13a2e5174c657b4f9aa6fd41e435ab7f082a95016e4bb",
    "s0_public_assembly_verifier/models.py": "cade60d1a260dd58e6d611a691f2d5907d1992cea5f0a4f702e9476558cc74a8",
    "s0_public_assembly_verifier/__init__.py": "a606ff1972d8b676eec44194d06cf78a28eb4c2e9934517d072106ae99bbcda9",
}
BASELINE_PINS = {name: value for name, value in PINS.items() if not name.endswith("/__init__.py")}
BASELINE_PINS["s0_public_assembly_candidate/runtime_guard.py"] = "be88d4bb151f4fe01a541a6ca7227e940fab53c5eb2d4d9ac8ccfb833675542d"
BASELINE_PINS["s0_public_assembly_verifier/win32.py"] = "db25d1c4db74f684a54f400ea1dd5f1478d0075c15d1460ff5baf0bef28f4996"
AGENTS_PIN = "4aac0c255dea03b85f6fb98b0b89f5b3c3f348e42c4dcaaf423411b818e3a065"
BENIGN = b"A01 bounded public file-read diagnostic.\n"
OLD = REPOSITORY / "s0-lab/audit-remediation/a01-public-boundaries-v0.1"
OLD_PINS = dict(PINS)
OLD_PINS["s0_public_assembly_candidate/runtime_guard.py"] = "693b8f8283cdf476cdeaa263c3021f2a161cd52da08e7c5a877725dc6586eda4"
DIAGNOSTIC_PINS = {
    "tests/test_delete_on_close.py": "8a4c3b5258fb522312ed5d1a7df472c9c48ed34bb6c9e2323930b5d03939d81e",
    "verification/delete-on-close-diagnostic.json": "4bc2307ac793c35e150ed2ace08480e4dad295c2d24646aab5fbc50c6dc1a588",
    "verification/diagnostic-stdout.txt": "b3e58e201e98ccf30a091ab9ce4c58f0b5c19aae3d8150a4ac16ee9b78f51cf3",
}


def checked_owned(path):
    root = CANDIDATE / "verification/tmp"
    assert path.is_absolute()
    path.relative_to(root)
    for current in (path, *path.parents):
        if current.exists():
            assert not (getattr(current.lstat(), "st_file_attributes", 0) & 0x400)
    return path


def authenticate_content():
    candidate = {name: digest(IMPLEMENTATION / name) for name in PINS}
    baseline = {name: digest(BASELINE / name) for name in BASELINE_PINS}
    old = {name: digest(OLD / "implementation" / name) for name in OLD_PINS}
    diagnostic = {name: digest(CANDIDATE / name) for name in DIAGNOSTIC_PINS}
    assert candidate == PINS
    assert baseline == BASELINE_PINS
    assert old == OLD_PINS
    assert diagnostic == DIAGNOSTIC_PINS
    return {"old_candidate_sha256": old, "frozen_diagnostic_sha256": diagnostic}



def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_exact(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    assert Path(module.__file__).resolve() == path.resolve()
    return module


def import_candidate():
    sys.path.insert(0, str(IMPLEMENTATION))
    from s0_public_assembly_candidate import runtime_guard, storage
    for name in ("s0_public_assembly_candidate", "s0_public_assembly_candidate.runtime_guard",
                 "s0_public_assembly_candidate.storage", "s0_public_assembly_candidate.constants",
                 "s0_public_assembly_candidate.errors"):
        relative = name.replace(".", "/") + ("/__init__.py" if "." not in name else ".py")
        assert Path(sys.modules[name].__file__).resolve() == (IMPLEMENTATION / relative).resolve()
    return runtime_guard, storage


def child_main():
    # This path deliberately runs before importing unittest/subprocess/ctypes.
    variant, action, scratch_text = sys.argv[2:]
    authenticate_content()
    guard, storage = import_candidate()
    if variant == "baseline":
        guard = load_exact("s0_public_assembly_candidate._baseline_runtime_guard",
                           BASELINE / "s0_public_assembly_candidate/runtime_guard.py")
    scratch = checked_owned(Path(scratch_text))
    scratch.relative_to((CANDIDATE / "verification/tmp").resolve())
    approved = scratch / "workspace/approved.txt"
    output = scratch / "output"
    expected_hash = hashlib.sha256(BENIGN).hexdigest()
    bound = {name: module.__file__ for name, module in sys.modules.items()
             if name.startswith("s0_public_assembly_candidate")}
    audit_events = []
    def observe(event, arguments):
        if event == "open":
            audit_events.append([str(arguments[0]), arguments[1], arguments[2]])
    sys.addaudithook(observe)
    guard.install_runtime_sentinels(workspace_root=approved.parent, output_root=output,
                                   allowed_public_files=frozenset({approved}),
                                   bundle_root=approved.parent)
    guard.require_file_open_sentinel_configured()
    result = {"variant": variant, "action": action, "imports": bound}
    try:
        if action.startswith("delete:"):
            _, destination, flag_name = action.split(":")
            target = approved if destination == "approved" else output / destination
            flags = os.O_TEMPORARY | getattr(os, flag_name) | getattr(os, "O_BINARY", 0)
            result.update(target=str(target), flags=flags, O_TEMPORARY=os.O_TEMPORARY)
            descriptor = os.open(target, flags)
            try:
                raw = BENIGN
            finally:
                os.close(descriptor)
        elif action == "pathlib":
            raw = approved.read_bytes()
        elif action == "os_open":
            descriptor = os.open(approved, os.O_RDONLY | getattr(os, "O_BINARY", 0))
            try:
                raw = os.read(descriptor, 4096)
            finally:
                os.close(descriptor)
        elif action == "storage":
            raw = storage.read_workspace_file(approved.parent, approved.name,
                                              expected_sha256=expected_hash,
                                              expected_bytes=len(BENIGN))
        elif action == "write_pending":
            first = output / "run-record.pending"
            first.write_bytes(BENIGN)
            second = output / "publication-receipt.pending"
            descriptor = os.open(second, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0))
            try:
                assert os.write(descriptor, BENIGN) == len(BENIGN)
            finally:
                os.close(descriptor)
            assert first.read_bytes() == second.read_bytes() == BENIGN
            raw = BENIGN
        elif action == "denied_read":
            raw = (scratch / "outside.txt").read_bytes()
        elif action == "denied_write":
            descriptor = os.open(approved, os.O_WRONLY)
            os.close(descriptor)
            raw = b"unexpected"
        elif action in {"run-record.json", "publication-receipt.json", "other.pending", "nested/run-record.pending"}:
            raw = (output / action).write_bytes(BENIGN)
        else:
            raise AssertionError("unknown controlled child action")
        assert raw == BENIGN
        guard.require_runtime_sentinels_healthy()
        result.update(status="allowed", data_sha256=expected_hash, byte_length=len(raw))
    except guard.BoundaryViolation as exc:
        result.update(status="denied", diagnostic=str(exc))
        try:
            approved.read_bytes()
        except guard.BoundaryViolation as latched:
            result["latched_read"] = str(latched)
        else:
            raise AssertionError("denial did not latch later file reads")
        try:
            guard.require_runtime_sentinels_healthy()
        except guard.BoundaryViolation as latched:
            result["latched_health"] = str(latched)
        else:
            raise AssertionError("denial did not latch health check")
    result["audit_open_events"] = audit_events
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "--child":
    child_main()
    raise SystemExit(0)


import io
import subprocess
import tempfile
import time
import unittest
from unittest import mock


OBSERVATIONS = []


def authenticate():
    authenticated_content = authenticate_content()
    observed = {path.relative_to(IMPLEMENTATION).as_posix()
                for path in IMPLEMENTATION.rglob("*") if path.is_file()}
    assert observed == set(PINS), "candidate inventory mismatch (names suppressed)"
    candidate_hashes = {name: digest(IMPLEMENTATION / name) for name in PINS}
    baseline_hashes = {name: digest(BASELINE / name) for name in BASELINE_PINS}
    assert candidate_hashes == PINS, "candidate pin mismatch"
    assert baseline_hashes == BASELINE_PINS, "baseline pin mismatch"
    assert digest(REPOSITORY / "AGENTS.md") == AGENTS_PIN, "AGENTS pin mismatch"
    identities = {}
    for name, arguments, expected in (("branch", ["branch", "--show-current"], PINNED_BRANCH),
                                      ("head", ["rev-parse", "HEAD"], PINNED_HEAD),
                                      ("tree", ["rev-parse", "HEAD^{tree}"], PINNED_TREE)):
        result = subprocess.run(["git", "-C", str(REPOSITORY), *arguments],
                                stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, timeout=10)
        assert result.returncode == 0, name + " query failed"
        identities[name] = result.stdout.strip()
        assert identities[name] == expected, name + " mismatch"
    return {**authenticated_content, "candidate_sha256": candidate_hashes, "candidate_inventory_count": len(observed),
            "baseline_sha256": baseline_hashes, "agents_sha256": AGENTS_PIN, **identities}


class RuntimeGuardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.guard, cls.storage = import_candidate()
        cls.tmp_root = CANDIDATE / "verification/tmp"
        checked_owned(cls.tmp_root)
        cls.tmp_root.mkdir(parents=True, exist_ok=True)

    def setUp(self):
        self.guard._VIOLATED = False

    def tearDown(self):
        self.guard._VIOLATED = False

    def run_child(self, action, variant="candidate"):
        with tempfile.TemporaryDirectory(prefix="a01-test-", dir=self.tmp_root) as name:
            scratch = checked_owned(Path(name))
            (scratch / "workspace").mkdir()
            (scratch / "output").mkdir()
            (scratch / "output/nested").mkdir()
            (scratch / "workspace/approved.txt").write_bytes(BENIGN)
            (scratch / "outside.txt").write_bytes(BENIGN)
            protected = [scratch / "workspace/approved.txt", scratch / "outside.txt"]
            if action.startswith("delete:"):
                for output_name in ("run-record.pending", "publication-receipt.pending"):
                    path = scratch / "output" / output_name
                    path.write_bytes(BENIGN)
                    protected.append(path)
            before_bytes = {str(path): path.read_bytes().hex() for path in protected}
            command = [str(PYTHON), "-I", "-S", "-B", str(Path(__file__).resolve()),
                       "--child", variant, action, str(scratch)]
            result = subprocess.run(command, capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stderr, "")
            value = json.loads(result.stdout)
            after_bytes = {str(path): path.read_bytes().hex() if path.exists() else None for path in protected}
            OBSERVATIONS.append({"child_command": command, "result": value,
                                 "before_hex": before_bytes, "after_hex": after_bytes})
            self.assertEqual(after_bytes, before_bytes)
            for path in protected:
                checked_owned(path)
            self.assertEqual((scratch / "workspace/approved.txt").read_bytes(), BENIGN)
        self.assertFalse(scratch.exists(), "owned scratch was not cleaned")
        return value

    def test_real_installed_sentinel_pathlib_read(self):
        self.assertEqual(self.run_child("pathlib")["status"], "allowed")

    def test_real_installed_sentinel_os_open_read(self):
        self.assertEqual(self.run_child("os_open")["status"], "allowed")

    def test_real_installed_sentinel_unchanged_storage_read(self):
        self.assertEqual(self.run_child("storage")["status"], "allowed")

    def test_baseline_discriminates_none_mode_defect(self):
        for action, expected in (("pathlib", "allowed"), ("os_open", "denied"), ("storage", "denied")):
            with self.subTest(action=action):
                value = self.run_child(action, "baseline")
                self.assertEqual(value["status"], expected)
                if expected == "denied":
                    self.assertIn("invalid mode", value["diagnostic"])

    def test_real_pending_writes_only(self):
        self.assertEqual(self.run_child("write_pending")["status"], "allowed")

    def test_real_denied_paths_and_latch(self):
        for action in ("denied_read", "denied_write", "run-record.json", "publication-receipt.json",
                       "other.pending", "nested/run-record.pending"):
            with self.subTest(action=action):
                value = self.run_child(action)
                self.assertEqual(value["status"], "denied")
                self.assertIn("latched", value["latched_read"])
                self.assertIn("latched", value["latched_health"])


    def test_real_delete_on_close_denied_and_bytes_preserved(self):
        for destination in ("approved", "run-record.pending", "publication-receipt.pending"):
            for flag in ("O_RDONLY", "O_WRONLY", "O_RDWR", "O_CREAT", "O_TRUNC", "O_APPEND"):
                with self.subTest(destination=destination, flag=flag):
                    value = self.run_child("delete:" + destination + ":" + flag)
                    self.assertEqual(value["status"], "denied")
                    self.assertIn("delete-on-close", value["diagnostic"])
                    self.assertIn("latched", value["latched_read"])
                    self.assertIn("latched", value["latched_health"])

    def test_delete_capability_all_representations_and_paths(self):
        root = self.tmp_root / "classification-only"
        approved = root / "public.txt"
        pending = root / "output/run-record.pending"
        second_pending = root / "output/publication-receipt.pending"
        temporary = os.O_TEMPORARY
        with mock.patch.multiple(self.guard, _WORKSPACE_ROOT=root, _OUTPUT_ROOT=root / "output",
                                 _ALLOWED_PUBLIC_FILES=frozenset({approved})):
            for path in (approved, pending, second_pending):
                for name in ("O_RDONLY", "O_WRONLY", "O_RDWR", "O_CREAT", "O_TRUNC", "O_APPEND"):
                    flags = temporary | getattr(os, name)
                    representations = ((None, flags), (flags,), (flags, 0), (0, flags),
                                       ("r", flags), ("rb", flags), ("w", flags),
                                       ("a", flags), ("x", flags), ("r+", flags),
                                       (flags, os.O_WRONLY), (os.O_WRONLY, flags))
                    for arguments in representations:
                        with self.subTest(path=path.name, flag=name, arguments=arguments):
                            with self.assertRaisesRegex(self.guard.BoundaryViolation, "delete-on-close"):
                                self.guard._guard_file_open((path, *arguments))
                            self.assertTrue(self.guard._VIOLATED)
                            self.guard._VIOLATED = False

    def test_ordinary_write_bits_remain_pending_only(self):
        root = self.tmp_root / "classification-only"
        approved = root / "public.txt"
        pending = root / "output/run-record.pending"
        with mock.patch.multiple(self.guard, _WORKSPACE_ROOT=root, _OUTPUT_ROOT=root / "output",
                                 _ALLOWED_PUBLIC_FILES=frozenset({approved})):
            for flag in (os.O_WRONLY, os.O_RDWR, os.O_CREAT, os.O_TRUNC, os.O_APPEND):
                for arguments in ((None, flag), (flag,)):
                    with self.subTest(flag=flag, arguments=arguments):
                        with self.assertRaises(self.guard.BoundaryViolation):
                            self.guard._guard_file_open((approved, *arguments))
                        self.guard._VIOLATED = False
                        self.guard._guard_file_open((pending, *arguments))
                        self.assertFalse(self.guard._VIOLATED)

    def test_none_mode_readonly_flag_combinations(self):
        masks = [getattr(os, name, 0) for name in ("O_BINARY", "O_CLOEXEC", "O_NOFOLLOW")]
        for bits in range(8):
            flags = os.O_RDONLY
            for index, mask in enumerate(masks):
                if bits & (1 << index):
                    flags |= mask
            with self.subTest(flags=flags, combination=bits):
                self.assertFalse(self.guard._write_requested(("public.txt", None, flags)))

    def test_none_mode_each_write_flag(self):
        for name in ("O_WRONLY", "O_RDWR", "O_CREAT", "O_TRUNC", "O_APPEND"):
            with self.subTest(flag=name):
                self.assertTrue(self.guard._write_requested(("public.txt", None, getattr(os, name))))

    def test_none_mode_rejects_missing_bool_noninteger_negative(self):
        for flags in ((), (False,), (True,), ("0",), (None,), (0.0,), (-1,)):
            with self.subTest(flags=flags):
                with self.assertRaises(self.guard.BoundaryViolation):
                    self.guard._write_requested(("public.txt", None, *flags))
                self.assertTrue(self.guard._VIOLATED)
                self.guard._VIOLATED = False

    def test_valid_string_and_legacy_integer_modes(self):
        for mode, expected in (("r", False), ("rb", False), ("r+", True), ("w", True),
                               ("wb", True), ("a", True), ("x", True), (os.O_RDONLY, False),
                               (os.O_WRONLY, True), (os.O_RDWR, True), (os.O_CREAT, True),
                               (os.O_TRUNC, True), (os.O_APPEND, True)):
            with self.subTest(mode=mode):
                self.assertEqual(self.guard._write_requested(("public.txt", mode, 0)), expected)

    def test_third_flags_are_used_only_for_none_mode(self):
        self.assertFalse(self.guard._write_requested(("public.txt", "r", os.O_WRONLY)))
        self.assertTrue(self.guard._write_requested(("public.txt", "w", os.O_RDONLY)))
        self.assertFalse(self.guard._write_requested(("public.txt", os.O_RDONLY, os.O_WRONLY)))

    def test_write_flags_do_not_bypass_public_allowlist(self):
        root = self.tmp_root / "classification-only"
        approved = root / "public.txt"
        with mock.patch.multiple(self.guard, _WORKSPACE_ROOT=root, _OUTPUT_ROOT=root / "output",
                                 _ALLOWED_PUBLIC_FILES=frozenset({approved})):
            for flag in (os.O_WRONLY, os.O_RDWR, os.O_CREAT, os.O_TRUNC, os.O_APPEND):
                with self.subTest(flag=flag):
                    with self.assertRaises(self.guard.BoundaryViolation):
                        self.guard._guard_file_open((approved, None, flag))
                    self.guard._VIOLATED = False

    def test_storage_safe_relative_paths_still_reject_escape(self):
        for path in ("../outside.txt", "/absolute.txt", "C:/outside.txt", "a\\b", "file:stream"):
            with self.subTest(path=path):
                with self.assertRaises(self.storage.StorageError):
                    self.storage._safe_relative(path)

    def test_storage_reparse_marker_still_detected(self):
        class FileInfo:
            st_file_attributes = 0x400
        self.assertTrue(self.storage._is_reparse(FileInfo()))
        FileInfo.st_file_attributes = 0
        self.assertFalse(self.storage._is_reparse(FileInfo()))


class RecordedResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cases = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.cases.append({"test": test.id(), "outcome": "pass"})

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.cases.append({"test": test.id(), "outcome": "failure", "detail": self._exc_info_to_string(err, test)})

    def addError(self, test, err):
        super().addError(test, err)
        self.cases.append({"test": test.id(), "outcome": "error", "detail": self._exc_info_to_string(err, test)})

    def addSubTest(self, test, subtest, err):
        super().addSubTest(test, subtest, err)
        self.cases.append({"test": subtest.id(), "outcome": "pass" if err is None else "failure",
                           "kind": "subtest"})


def run_all():
    started = time.monotonic()
    assert Path(sys.executable).resolve() == PYTHON.resolve()
    assert sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
    before = authenticate()
    historical = json.loads((CANDIDATE / "verification/delete-on-close-diagnostic.json").read_text(encoding="utf-8"))
    import_candidate()
    streams = load_exact("a01_test_stream_inventory", Path(__file__).with_name("test_stream_inventory.py"))
    suite = unittest.TestSuite((unittest.defaultTestLoader.loadTestsFromTestCase(RuntimeGuardTests),
                               unittest.defaultTestLoader.loadTestsFromModule(streams)))
    output = io.StringIO()
    result = unittest.TextTestRunner(stream=output, verbosity=2, resultclass=RecordedResult,
                                    failfast=True).run(suite)
    after = authenticate()
    imported = {}
    for name in PINS:
        module_name = name.removesuffix(".py").replace("/__init__", "").replace("/", ".")
        actual = Path(sys.modules[module_name].__file__).resolve()
        assert actual == (IMPLEMENTATION / name).resolve()
        imported[module_name] = str(actual)
    scratch = CANDIDATE / "verification/tmp"
    scratch_remaining_count = sum(1 for _ in scratch.iterdir())
    assert scratch_remaining_count == 0
    verification = CANDIDATE / "verification"
    stdout_path = verification / "test-stdout.txt"
    stdout_path.write_text(output.getvalue(), encoding="utf-8", newline="\n")
    records = {
        "candidate": "a01-public-boundaries-v0.2", "role": "TEST/VERIFICATION",
        "result": "BOUNDED-UNIT-REGRESSION-PASS" if result.wasSuccessful() else "BOUNDED-UNIT-REGRESSION-FAIL",
        "command": [str(PYTHON), "-I", "-S", "-B", str(Path(__file__).resolve())],
        "interpreter": {"executable": sys.executable, "version": sys.version,
                        "isolated": sys.flags.isolated, "no_site": sys.flags.no_site,
                        "dont_write_bytecode": sys.dont_write_bytecode},
        "tests_run": result.testsRun, "failures": len(result.failures), "errors": len(result.errors),
        "skips": list(result.skipped), "cases": result.cases,
        "before": before, "after": after, "imported_candidate_modules": imported,
        "historical_delete_on_close_diagnostic": {"sha256": DIAGNOSTIC_PINS["verification/delete-on-close-diagnostic.json"], "result": historical["result"], "cases": historical["cases"]},
        "child_observations": OBSERVATIONS, "stream_observations": streams.OBSERVATIONS,
        "test_sha256": {str(Path(__file__).resolve()): digest(Path(__file__)),
                        str(Path(streams.__file__).resolve()): digest(Path(streams.__file__))},
        "stdout_sha256": digest(stdout_path), "scratch_remaining_count": scratch_remaining_count,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "unverified": ["Hostile interpreter, standard-library or import-closure security",
                       "Controller or native publication lifecycle; actual ADS exploitation",
                       "ACL/root identity/privileged replacement/TOCTOU and OS isolation",
                       "Arbitrary hostile same-process fields, descriptor authority, introspection, races or concurrency",
                       "Exhaustive future flags and all-platform compatibility; trusted evidence producer",
                       "S0/E0 execution, models/providers, integration and operational safety"],
    }
    (verification / "test-results.json").write_text(json.dumps(records, indent=2, sort_keys=True) + "\n",
                                                     encoding="utf-8", newline="\n")
    print(output.getvalue(), end="")
    print(records["result"])
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(run_all())

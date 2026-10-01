"""Bounded public unit diagnostics for the complete A08 source integration.

No live Win32 backend, dependency preloader, S0/E0 run, or provider is invoked.
The old authority paths and diagnostic implementation pin are not rebound.
"""

from __future__ import annotations

import ast
import hashlib
import importlib
import importlib.util
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tempfile
import time
import unittest
from unittest import mock

CANDIDATE = Path(__file__).resolve().parents[1]
REPOSITORY = CANDIDATE.parents[2]
IMPLEMENTATION = CANDIDATE / "implementation"
SCRATCH = CANDIDATE / "verification/scratch"
BASE = "s0-lab/assembly-rehearsal/public-end-to-end-v0.1"
A01 = "s0-lab/audit-remediation/a01-public-boundaries-v0.2"
PYTHON = Path("C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe")
PYTHON_PIN = "4d6f5f81a4bca11191c4c7c6b43632694d0a4ce74e068619d8fdc161d469859a"
AGENTS_PIN = "393984b6d83639d0c4365d0ca6066907d3d281384656b860a4853d3d6d46ac9e"
REPLACEMENTS = {
    "s0_public_assembly_candidate/runtime_guard.py": "811f1df27a44d70948f3e37fedcba976189fd5b58ff61a6e029c14d74c768f7a",
    "s0_public_assembly_verifier/win32.py": "dd250e352431390885adfb4a95244d96622bc9546bd003f585b1afb579143f68",
}
MANIFESTS = (
    (BASE + "/verification/implementation-files.sha256", "0cc96816404094dec313dbab4bb108744383afb2ca5272834b589235364a9623", "", 32),
    ("s0-lab/public-practice/v0.1/bundle-files.sha256", "e41ee6c71169df646e3c8c0b0e8f3d77e7871d939f651b86a52ea5696feeb637", "s0-lab/public-practice/v0.1", 90),
    ("s0-lab/i0/verification/implementation-files.sha256", "f57514f96a2c30366cdf1f1414524711da20c9410186b3017e3dbf902bb612ae", "s0-lab/i0", 15),
    ("s0-lab/i1/verification/implementation-files.sha256", "668d3549ef6f7146ac7200e7be1f362967eca4c2cf66119a1f727bebd245332c", "s0-lab/i1", 26),
    ("s0-lab/i2/verification/implementation-files.sha256", "18ccfbcbe73b1170e07bd000376b079528dcf135b806e3f6c77b10efae736bd6", "", 16),
    ("s0-lab/i3/verification/implementation-files.sha256", "e07c9754d61b143bca9747bbcccb58b0861b14f60031422e1e4fd88a0fb93648", "", 17),
    ("s0-lab/control/assembly-rehearsal/public-end-to-end-v0.5/design-package-files.sha256", "6292e322549c79f539b57c1087fd722c5cca96318c45d89fac5343247c429802", "", 5),
)
REVIEW_HASH_ONLY = "s0-lab/reviews/assembly-rehearsal/public-end-to-end-v0.5/public-end-to-end-assembly-rehearsal-design-v0.5-independent-rereview-v0.1.md"
DIRECT_PINS = {
    "AGENTS.md": AGENTS_PIN,
    REVIEW_HASH_ONLY: "7c629c9c4aed5c2e36598e4ad08e4819fa06b73f3f77bf9e7d19714f61b35137",
    "s0-lab/control/sm0/answer.schema.json": "e21100f06d2715f42cd1fda812e17d22340a64327bfb48c03112a0f83d33ac6b",
}
TEST_NAMES = ("test_candidate", "test_harness", "test_verifier", "test_runtime_guard", "test_stream_inventory")
SOURCE_PINS = {}
ADMITTED = {}
IMPORTED = {}
PROCESS_OBSERVATIONS = []


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest(relative, expected, row_base, count):
    path = REPOSITORY / relative
    raw = path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == expected, "manifest pin mismatch"
    assert raw.endswith(b"\n") and b"\r" not in raw
    rows = {}
    for line in raw[:-1].split(b"\n"):
        match = re.fullmatch(rb"([0-9a-f]{64})  ([A-Za-z0-9._/-]+)", line)
        assert match is not None, "manifest syntax mismatch"
        sha, name = (part.decode("ascii") for part in match.groups())
        pure = PurePosixPath(name)
        assert not pure.is_absolute() and ".." not in pure.parts
        name = f"{row_base}/{name}" if row_base else name
        assert name not in rows, "duplicate manifest row"
        rows[name] = sha
    assert len(rows) == count, "manifest count mismatch"
    return rows


def exact_inventory():
    observed = set()
    for root, directories, files in os.walk(IMPLEMENTATION, followlinks=False):
        for name in directories + files:
            path = Path(root) / name
            assert not (getattr(path.lstat(), "st_file_attributes", 0) & 0x400), "implementation reparse entry"
        observed.update((Path(root) / name).relative_to(IMPLEMENTATION).as_posix() for name in files)
    assert observed == set(SOURCE_PINS), "implementation inventory mismatch (names suppressed)"
    return len(observed)


def authenticate():
    global SOURCE_PINS, ADMITTED
    entries = dict(DIRECT_PINS)
    for relative, sha, row_base, count in MANIFESTS:
        entries[relative] = sha
        entries.update(manifest(relative, sha, row_base, count))
    a01_manifest = A01 + "/artifact-files.sha256"
    a01_sha = "c26f8a02c4dc306e9639dfefd26ee8e41793ffb45998b84c7c2841490772f972"
    a01_rows = manifest(a01_manifest, a01_sha, A01, 18)
    entries[a01_manifest] = a01_sha
    # A01 result packets and old diagnostic execution are not inputs.
    for name, sha in a01_rows.items():
        if name.startswith(A01 + "/implementation/") or name in {
            A01 + "/tests/test_runtime_guard.py", A01 + "/tests/test_stream_inventory.py"
        }:
            entries[name] = sha
    original_prefix = BASE + "/implementation/"
    SOURCE_PINS = {name.removeprefix(original_prefix): sha for name, sha in entries.items()
                   if name.startswith(original_prefix)}
    assert len(SOURCE_PINS) == 27
    SOURCE_PINS.update(REPLACEMENTS)
    candidate_prefix = IMPLEMENTATION.relative_to(REPOSITORY).as_posix() + "/"
    entries.update({candidate_prefix + name: sha for name, sha in SOURCE_PINS.items()})
    actual = {name: digest(REPOSITORY / name) for name in entries}
    assert actual == entries, "admitted input pin mismatch (names suppressed)"
    assert digest(PYTHON) == PYTHON_PIN, "interpreter pin mismatch"
    identity = {}
    for label, arguments, expected in (
        ("branch", ["branch", "--show-current"], "codex/windows-build-toolchain-environment-v0.1"),
        ("head", ["rev-parse", "HEAD"], "cc76d7e82aeb51dfdc7baba3da0f7993ab2da61a"),
        ("tree", ["rev-parse", "HEAD^{tree}"], "82c02f37fd13ecfc8c7b888bb66127989b6d4f34"),
    ):
        result = subprocess.run(["git", "-C", str(REPOSITORY), *arguments], capture_output=True, timeout=10)
        assert result.returncode == 0, "identity query failed"
        identity[label] = result.stdout.decode().strip()
        assert identity[label] == expected, "Git identity mismatch"
    ADMITTED = entries
    return {"input_sha256": actual, "python_sha256": PYTHON_PIN,
            "implementation_count": exact_inventory(), **identity}


def load_exact(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    assert Path(module.__file__).resolve() == path.resolve()
    return module


class IntegrationTests(unittest.TestCase):
    def test_exact_27_source_inventory_25_original_plus_two_a01(self):
        self.assertEqual(exact_inventory(), 27)
        changed = [name for name in SOURCE_PINS if digest(IMPLEMENTATION / name) != digest(REPOSITORY / BASE / "implementation" / name)]
        self.assertEqual(set(changed), set(REPLACEMENTS))

    def test_full_initializers_exports_and_consumer_bindings(self):
        candidate = importlib.import_module("s0_public_assembly_candidate")
        verifier = importlib.import_module("s0_public_assembly_verifier")
        consumer = importlib.import_module("s0_public_assembly_verifier.consumer")
        observer = importlib.import_module("s0_public_assembly_verifier.observer")
        win32 = importlib.import_module("s0_public_assembly_verifier.win32")
        self.assertEqual(candidate.__version__, "0.1.0")
        self.assertEqual(candidate.__all__, [])
        self.assertEqual(verifier.__all__, ["ExternalPins", "LiveConsumer", "PublicationObserver"])
        self.assertIs(verifier.LiveConsumer, consumer.LiveConsumer)
        self.assertIs(verifier.PublicationObserver, observer.PublicationObserver)
        self.assertIs(consumer.PublicationObserver, observer.PublicationObserver)
        self.assertIs(consumer._is_authenticated_win32_backend, win32._is_authenticated_win32_backend)

    def test_complete_import_origins_and_source_compile(self):
        for name in SOURCE_PINS:
            path = IMPLEMENTATION / name
            with self.subTest(source=name):
                compile(path.read_bytes(), str(path), "exec", dont_inherit=True)
                if name in {"s0_public_assembly_candidate/child.py", "s0_public_assembly_candidate/__main__.py"}:
                    # These intentionally install process-global sentinels at import.
                    continue
                module_name = name.removesuffix(".py").replace("/__init__", "").replace("/", ".")
                module = importlib.import_module(module_name)
                self.assertEqual(Path(module.__file__).resolve(), path.resolve())
                IMPORTED[module_name] = str(path.resolve())

    def test_runtime_roots_and_authority_pins_are_not_rebound_by_relocation(self):
        harness = importlib.import_module("s0_public_assembly_verifier.harness")
        bootstrap = importlib.import_module("s0_public_assembly_child_bootstrap")
        self.assertEqual(harness.ASSEMBLY_ROOT, BASE)
        self.assertEqual(bootstrap._CANDIDATE_ROOT, BASE + "/implementation/s0_public_assembly_candidate")
        self.assertNotEqual(harness.CANDIDATE_ROOT, (IMPLEMENTATION / "s0_public_assembly_candidate").relative_to(REPOSITORY).as_posix())
        with self.assertRaisesRegex(bootstrap._BootstrapFailure, "runtime profile"):
            bootstrap._require_exact_preinstalled_jsonschema()
        value = {key: "0" * 64 for key in bootstrap._CONFIG_KEYS}
        value.update(schema_id=bootstrap._CONFIG_SCHEMA,
                     candidate_root=(IMPLEMENTATION / "s0_public_assembly_candidate").relative_to(REPOSITORY).as_posix())
        raw = (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()
        with mock.patch.object(sys, "stdin", type("UnitInput", (), {"buffer": io.BytesIO(raw)})()):
            with self.assertRaisesRegex(bootstrap._BootstrapFailure, "candidate root"):
                bootstrap._canonical_config()


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
        entry = {"test": subtest.id(), "outcome": "pass" if err is None else "failure", "kind": "subtest"}
        if err is not None:
            entry["detail"] = self._exc_info_to_string(err, test)
        self.cases.append(entry)


def run_all():
    start = time.monotonic()
    assert Path(sys.executable).resolve() == PYTHON.resolve()
    assert sys.version_info[:3] == (3, 12, 10)
    assert sys.flags.isolated and sys.flags.no_site and sys.flags.utf8_mode and sys.dont_write_bytecode
    before = authenticate()
    SCRATCH.mkdir(parents=True, exist_ok=True)
    for path in (SCRATCH, *SCRATCH.parents):
        assert not (getattr(path.lstat(), "st_file_attributes", 0) & 0x400)
    index = 1
    while (SCRATCH / f"attempt-{index:03d}").exists():
        index += 1
    evidence = SCRATCH / f"attempt-{index:03d}"
    evidence.mkdir()
    # All inherited TemporaryDirectory calls remain inside owned scratch.
    tempfile.tempdir = str(SCRATCH)
    sys.path.insert(0, str(IMPLEMENTATION))
    modules = [load_exact(name, Path(__file__).with_name(name + ".py")) for name in TEST_NAMES]
    suites = [unittest.defaultTestLoader.loadTestsFromModule(module) for module in modules]
    counts = {name: suite.countTestCases() for name, suite in zip(TEST_NAMES, suites)}
    assert sum(counts[name] for name in TEST_NAMES[:3]) == 47
    suites.append(unittest.defaultTestLoader.loadTestsFromTestCase(IntegrationTests))
    output = io.StringIO()
    original_run = subprocess.run

    def record_process(*args, **kwargs):
        result = original_run(*args, **kwargs)
        def printable(value):
            return value.decode("utf-8", errors="replace") if isinstance(value, bytes) else value
        PROCESS_OBSERVATIONS.append({"command": list(result.args), "returncode": result.returncode,
                                     "stdout": printable(result.stdout), "stderr": printable(result.stderr),
                                     "timeout_seconds": kwargs.get("timeout")})
        return result

    with mock.patch.object(subprocess, "run", side_effect=record_process):
        result = unittest.TextTestRunner(stream=output, verbosity=2, resultclass=RecordedResult).run(unittest.TestSuite(suites))
    after = authenticate()
    assert after == before, "pre/post admitted inputs changed"
    remaining = [path for path in SCRATCH.iterdir() if not path.name.startswith("attempt-")]
    assert not remaining, "owned temporary directory residue (names suppressed)"
    records = {
        "candidate": CANDIDATE.name, "role": "TEST/VERIFICATION", "attempt": index,
        "result": "BOUNDED-PUBLIC-UNIT-INTEGRATION-PASS" if result.wasSuccessful() else "BOUNDED-PUBLIC-UNIT-INTEGRATION-FAIL",
        "command": [str(PYTHON), "-I", "-S", "-B", "-X", "utf8", str(Path(__file__).resolve())],
        "expected_process_exit": 0 if result.wasSuccessful() else 1,
        "interpreter": {"executable": sys.executable, "version": sys.version, "isolated": sys.flags.isolated,
                        "no_site": sys.flags.no_site, "utf8_mode": sys.flags.utf8_mode,
                        "dont_write_bytecode": sys.dont_write_bytecode},
        "tests_run": result.testsRun, "original_test_purposes": 47, "module_test_counts": counts,
        "integration_tests": 4, "subtests": sum(case.get("kind") == "subtest" for case in result.cases),
        "failures": len(result.failures), "errors": len(result.errors), "skips": list(result.skipped),
        "cases": result.cases, "before": before, "after": after, "imported_modules": IMPORTED,
        "child_observations": modules[3].OBSERVATIONS, "stream_observations": modules[4].OBSERVATIONS,
        "process_observations": PROCESS_OBSERVATIONS, "scratch_temporary_residue_count": len(remaining),
        "test_sha256": {path.name: digest(path) for path in [Path(__file__).with_name(name + ".py") for name in TEST_NAMES] + [Path(__file__)]},
        "stdout_sha256": hashlib.sha256(output.getvalue().encode("utf-8")).hexdigest(),
        "elapsed_seconds": round(time.monotonic() - start, 3),
        "scope": ["Original 47 unit purposes retained; FakeBackend, API doubles, and tiny temporary unit parameters only",
                  "IMPLEMENTATION_PIN='a'*64 remains diagnostic-only; original authority and runtime roots unchanged",
                  "Existing public practice inputs reused without new S0 fixture/oracle creation",
                  "Review authority content used only as a hash input; no verdict content inspection",
                  "No real jsonschema/runtime preload or Win32PublicationBackend construction"],
        "unverified": ["Live Win32 rehearsal, native publication lifecycle, actual ADS exploitation",
                       "Hostile interpreter/stdlib/native/import closure and historical runtime identity",
                       "Hostile same-process globals, introspection, arbitrary caller minting, races and concurrency",
                       "ACL/root volume/reparse/rename/retained handles/repository exclusion/TOCTOU beyond owned scratch checks",
                       "Future flags, exhaustive platform compatibility, and trusted evidence-producer security",
                       "S0/E0 execution or scoring, providers/models, operational safety and economic value"],
    }
    raw = json.dumps(records, indent=2, sort_keys=True) + "\n"
    for root in [evidence] + ([CANDIDATE / "verification"] if result.wasSuccessful() and not (CANDIDATE / "verification/test-results.json").exists() else []):
        with (root / "test-stdout.txt").open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(output.getvalue())
        with (root / "test-results.json").open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(raw)
    print(output.getvalue(), end="")
    print(records["result"], "tests=", result.testsRun, "subtests=", records["subtests"], "attempt=", index)
    return records["expected_process_exit"]


if __name__ == "__main__":
    raise SystemExit(run_all())

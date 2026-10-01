"""Bounded source/unit regressions; no native execution or S0 inputs."""

from __future__ import annotations

import difflib
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import unittest


ROOT = Path("C:/Users/SSAFY/Documents/ai-development-tradition")
CANDIDATE = ROOT / "s0-lab/audit-remediation/a02-native-source-corrections-v0.1"
ORIGINAL = ROOT / "docs/maintenance/audit-2026-09-09/source-snapshot-2026-09-16"
IMPLEMENTATION = CANDIDATE / "implementation"
PACKAGE = IMPLEMENTATION / "s0_public_runtime_preloader"
PYTHON = Path("C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe")
IDENTITY = {
    "branch": "codex/windows-build-toolchain-environment-v0.1",
    "head": "cc76d7e82aeb51dfdc7baba3da0f7993ab2da61a",
    "tree": "82c02f37fd13ecfc8c7b888bb66127989b6d4f34",
}
PINS = {
    ROOT / "AGENTS.md": (30777, "4aac0c255dea03b85f6fb98b0b89f5b3c3f348e42c4dcaaf423411b818e3a065"),
    ORIGINAL / "s0_neutral_preloader_v0_5.cpp": (81162, "6230ef69d5b4b175968f7576b43aeb5ae15fa3646c59778f84b5c3877c0ef9ec"),
    ORIGINAL / "canonical.py": (5835, "f73112b1bf55708d68d1e3823d768f1e9083f44760945ca7d2eb3d4fdf75aad4"),
    ORIGINAL / "source_audit.py": (24041, "c5cc9edb2e290f9ec0be74e944bf515b0c398f9bd08e379a701a8582951aac99"),
    IMPLEMENTATION / "native/s0_neutral_preloader_v0_5.cpp": (81191, "88e2a05bbb643c18247844b9aa38b0b327215730f8cf0fd44925e077df5c6e53"),
    PACKAGE / "canonical.py": (5980, "14b30ef5688f3340b78215632fba4f0f4360b2d394ca56730979ac5e6f5c1ff0"),
    PACKAGE / "source_audit.py": (24115, "7b65cfec819544a258ecb0cb9f25346b0c9c6606c52f12448d0a8d6954f57e6c"),
    PACKAGE / "errors.py": (643, "20940829a8c905028bee90d3188f019ac0b30720016a5aaf327ce71feca77c86"),
    PACKAGE / "__init__.py": (64, "57adf310b3589dadfc4c69369def09c3185d99983e7a42a5772c431c60bb250a"),
}
EXPECTED_FILES = {p.relative_to(IMPLEMENTATION).as_posix() for p in PINS if p.is_relative_to(IMPLEMENTATION)}
EXPECTED_DIRECTORIES = {"native", "s0_public_runtime_preloader"}
SEVEN_FILES = (
    "runtime-files.sha256", "runtime-profile-package-files-v0.5.sha256",
    "runtime-profile-v0.1.json", "runtime-profile-v0.2.json",
    "runtime-profile-v0.3.json", "runtime-profile-v0.4.json", "runtime-profile-v0.5.json",
)
DOT_ALIASES = (".", "./a", "a/./b", "a/.")
INVALID_PATHS = DOT_ALIASES + (
    "../a", "a/../b", "", "/abs", "C:/a", "a:b", "a\\b", "a//b", "a/",
    "a\x00b", "a" * 256, "/".join(["a" * 205] * 5), "a.", "a ",
)
MOVE_CALLS = ("MoveFile", "MoveFileA", "MoveFileW", "MoveFileExA", "MoveFileExW", "MoveFileWithProgressA", "MoveFileWithProgressW", "MoveFileTransactedA", "MoveFileTransactedW")
COMMAND = f'& "{PYTHON.as_posix()}" -I -S -B "{(CANDIDATE / "tests/test_source_corrections.py").as_posix()}"'
CAPTURED: dict[Path, bytes] = {}
IMPORTS: list[dict[str, str]] = []


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def authenticate():
    files, directories = set(), set()
    for root, dirs, names in os.walk(IMPLEMENTATION, followlinks=False):
        base = Path(root)
        for name in dirs:
            directories.add((base / name).relative_to(IMPLEMENTATION).as_posix())
        for name in names:
            files.add((base / name).relative_to(IMPLEMENTATION).as_posix())
    if files != EXPECTED_FILES or directories != EXPECTED_DIRECTORIES:
        raise RuntimeError("candidate inventory missing, extra, or shadow entries")
    records = {}
    for path, (size, expected) in PINS.items():
        raw = path.read_bytes()
        actual = digest(raw)
        if len(raw) != size or actual != expected:
            raise RuntimeError("frozen input size/hash mismatch")
        CAPTURED[path] = raw
        records[path.relative_to(ROOT).as_posix()] = {"bytes": len(raw), "sha256": actual}
    identity = {}
    for label, args in (("branch", ["branch", "--show-current"]), ("head", ["rev-parse", "HEAD"]), ("tree", ["rev-parse", "HEAD^{tree}"])):
        process = subprocess.run(["git", *args], cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=False)
        if process.returncode:
            raise RuntimeError(f"git identity query failed: {label}, exit {process.returncode}")
        identity[label] = process.stdout.decode("ascii").strip()
    if identity != IDENTITY:
        raise RuntimeError("frozen branch/head/tree differs")
    if (CANDIDATE / "verification/tmp").exists():
        raise RuntimeError("owned scratch unexpectedly present; no cleanup attempted")
    return {"pins": records, "identity": identity, "implementation_file_count": len(files), "missing": 0, "extra_or_shadow": 0, "scratch_used": False, "scratch_absent": True}


def load_exact(name, path, package=False):
    if name in sys.modules:
        raise RuntimeError("test module name already loaded")
    spec = importlib.util.spec_from_file_location(name, path, submodule_search_locations=[] if package else None)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    # Execute only the authenticated byte buffer, without another source read.
    exec(compile(CAPTURED[path], str(path), "exec"), module.__dict__)
    if Path(module.__file__) != path or Path(module.__spec__.origin) != path:
        raise RuntimeError("explicit import origin differs")
    IMPORTS.append({"module": name, "path": path.as_posix(), "sha256": digest(CAPTURED[path])})
    return module


def package_modules(prefix, baseline=False):
    load_exact(prefix, PACKAGE / "__init__.py", package=True)
    error = load_exact(prefix + ".errors", PACKAGE / "errors.py").RuntimeProfileError
    location = ORIGINAL if baseline else PACKAGE
    canonical = load_exact(prefix + ".canonical", location / "canonical.py")
    audit = load_exact(prefix + ".source_audit", location / "source_audit.py")
    return canonical, audit, error


def cpp_scope(raw, function, next_function):
    text = raw.decode("utf-8")
    start = text.index(function + "(")
    return text[start:text.index(next_function + "(", start)]


def package_list(scope):
    matches = re.findall(r"\bexpected_package_files\s*=\s*\{([^}]+)\};", scope)
    if len(matches) != 1:
        raise ValueError("physical list declaration not unique")
    return tuple(re.findall(r'"([^"\n]+)"', matches[0]))


def exact_seven(sequence):
    if tuple(sorted(sequence)) != SEVEN_FILES or len(set(sequence)) != 7:
        raise ValueError("physical package inventory differs")


def benign_source(audit, role):
    row = audit.NATIVE_API_INVENTORY[role]
    calls = sorted(set(row["decision_semantic_calls"]) | set(row["supporting_calls"]))
    return ("void benign() {\n" + "\n".join(name + "();" for name in calls) + "\n}\n").encode(), tuple(calls)


class SourceCorrections(unittest.TestCase):
    def test_environment_and_pinned_imports(self):
        self.assertEqual(sys.version_info[:3], (3, 12, 10))
        self.assertEqual(Path(sys.executable), PYTHON)
        self.assertTrue(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode)
        self.assertEqual(len(IMPORTS), 8)
        for item in IMPORTS:
            with self.subTest(module=item["module"]):
                self.assertEqual(item["sha256"], PINS[Path(item["path"])][1])

    def test_f01_both_physical_lists_exact_seven(self):
        for scope in (INITIAL, REVERIFY):
            with self.subTest(scope=scope.split("(", 1)[0]):
                exact_seven(package_list(scope))
                self.assertEqual(package_list(scope).count("runtime-profile-v0.5.json"), 1)

    def test_f01_lists_consumed_by_comparison_and_directory_check(self):
        for scope in (INITIAL, REVERIFY):
            with self.subTest(scope=scope.split("(", 1)[0]):
                self.assertRegex(scope, r'EnumerateFiles\(package_root, L"", package_files\)')
                self.assertIn("std::sort(package_files.begin(), package_files.end());", scope)
                self.assertRegex(scope, r'if \(package_files != expected_package_files\) Fail\(')
                self.assertIn("RequireExactDirectorySet(package_root, expected_package_files);", scope)

    def test_f01_baseline_discriminates_missing_p5(self):
        exact_seven(package_list(BASE_INITIAL))
        self.assertEqual(package_list(BASE_REVERIFY), SEVEN_FILES[:-1])
        with self.assertRaises(ValueError):
            exact_seven(package_list(BASE_REVERIFY))

    def test_f01_cpp_diff_exactly_one_added_list_entry(self):
        old = CAPTURED[ORIGINAL / "s0_neutral_preloader_v0_5.cpp"]
        before = b'"runtime-profile-v0.3.json", "runtime-profile-v0.4.json"\n'
        after = b'"runtime-profile-v0.3.json", "runtime-profile-v0.4.json", "runtime-profile-v0.5.json"\n'
        self.assertEqual(old.count(before), 1)
        self.assertEqual(old.replace(before, after), CAPTURED[IMPLEMENTATION / "native/s0_neutral_preloader_v0_5.cpp"])

    def test_f01_in_memory_missing_duplicate_extra_mutants(self):
        for i in range(7):
            with self.subTest(missing=i), self.assertRaises(ValueError):
                exact_seven(SEVEN_FILES[:i] + SEVEN_FILES[i + 1:])
            with self.subTest(duplicate=i), self.assertRaises(ValueError):
                exact_seven(SEVEN_FILES + (SEVEN_FILES[i],))
        with self.subTest(extra=True), self.assertRaises(ValueError):
            exact_seven(SEVEN_FILES + ("unexpected.txt",))

    def test_f08_normal_relative_paths(self):
        for value in ("a", "a/b", "data.json", "a-b_c/file.sha256", "v0.5/data", "a" * 255):
            with self.subTest(path=value):
                self.assertEqual(canonical.safe_virtual_path(value), value)

    def test_f08_invalid_paths_rejected(self):
        for i, value in enumerate(INVALID_PATHS):
            with self.subTest(case=i), self.assertRaises(Error):
                canonical.safe_virtual_path(value)

    def test_f08_exact_type_rejected(self):
        for value in (None, b"a", 1, ["a"]):
            with self.subTest(value=repr(value)), self.assertRaises(Error):
                canonical.safe_virtual_path(value)

    def test_f08_baseline_dot_alias_acceptance_discriminated(self):
        for path in DOT_ALIASES:
            with self.subTest(path=path):
                self.assertEqual(base_canonical.safe_virtual_path(path), path)
                with self.assertRaises(Error):
                    canonical.safe_virtual_path(path)

    def test_f08_traversal_remains_rejected(self):
        for module, error in ((canonical, Error), (base_canonical, BaseError)):
            for path in ("../a", "a/../b"):
                with self.subTest(module=module.__name__, path=path), self.assertRaises(error):
                    module.safe_virtual_path(path)

    def test_f08_manifest_aliases_rejected(self):
        for path in DOT_ALIASES:
            row = (digest(b"benign") + "  " + path + "\n").encode()
            with self.subTest(path=path):
                self.assertEqual(dict(base_canonical.parse_manifest(row)), {path: digest(b"benign")})
                self.assertEqual(dict(base_canonical.verify_manifest_material(row, {path: b"benign"}, expected_rows=1)), {path: digest(b"benign")})
                with self.assertRaises(Error):
                    canonical.parse_manifest(row, expected_rows=1)
                with self.assertRaises(Error):
                    canonical.verify_manifest_material(row, {path: b"benign"}, expected_rows=1)

    def test_f08_manifest_material_key_aliases_rejected(self):
        row = (digest(b"benign") + "  a\n").encode()
        for path in DOT_ALIASES:
            with self.subTest(path=path), self.assertRaises(Error):
                canonical.verify_manifest_material(row, {path: b"benign"}, expected_rows=1)

    def test_f08_normal_manifest_and_material(self):
        targets = {"a": b"benign-a", "b/c": b"benign-b"}
        row = "".join(digest(raw) + "  " + path + "\n" for path, raw in targets.items()).encode()
        expected = {path: digest(raw) for path, raw in targets.items()}
        self.assertEqual(dict(canonical.parse_manifest(row, expected_rows=2)), expected)
        self.assertEqual(dict(canonical.verify_manifest_material(row, targets, expected_rows=2)), expected)

    def test_api_role_sources_accepted(self):
        for role in audit.NATIVE_API_INVENTORY:
            raw, calls = benign_source(audit, role)
            with self.subTest(role=role):
                self.assertEqual(audit.inspect_native_source(role, raw), calls)
                self.assertEqual(base_audit.inspect_native_source(role, raw), calls)

    def test_api_movefile_family_rejected(self):
        for role in audit.NATIVE_API_INVENTORY:
            raw, _ = benign_source(audit, role)
            for name in MOVE_CALLS:
                with self.subTest(role=role, call=name), self.assertRaisesRegex(Error, "unclassified Windows API"):
                    audit.inspect_native_source(role, raw + (name + "();\n").encode())

    def test_api_baseline_movefilew_discriminated(self):
        for role in audit.NATIVE_API_INVENTORY:
            raw, calls = benign_source(audit, role)
            mutated = raw + b"MoveFileW();\n"
            with self.subTest(role=role):
                self.assertEqual(base_audit.inspect_native_source(role, mutated), calls)
                with self.assertRaisesRegex(Error, "unclassified Windows API"):
                    audit.inspect_native_source(role, mutated)

    def test_api_gettemppathw_rejection_retained(self):
        for role in audit.NATIVE_API_INVENTORY:
            raw, _ = benign_source(audit, role)
            for module, error in ((audit, Error), (base_audit, BaseError)):
                with self.subTest(role=role, module=module.__name__), self.assertRaisesRegex(error, "unclassified Windows API"):
                    module.inspect_native_source(role, raw + b"GetTempPathW();\n")

    def test_api_comments_and_strings_are_not_calls(self):
        comments = b'// MoveFileW(); GetTempPathW();\n/* MoveFileExW(); */\nconst char* label = "MoveFileW(); GetTempPathW();";\n'
        for role in audit.NATIVE_API_INVENTORY:
            raw, calls = benign_source(audit, role)
            with self.subTest(role=role):
                self.assertEqual(audit.inspect_native_source(role, raw + comments), calls)

    def test_api_unknown_role_and_inventory_mismatch_rejected(self):
        with self.assertRaisesRegex(Error, "role is not exact"):
            audit.inspect_native_source("unknown", b"void benign() {}\n")
        for role in audit.NATIVE_API_INVENTORY:
            raw, calls = benign_source(audit, role)
            with self.subTest(role=role), self.assertRaisesRegex(Error, "API set differs"):
                audit.inspect_native_source(role, raw.replace((calls[0] + "();").encode(), b"", 1))

    def test_minimal_python_diffs(self):
        base = CAPTURED[ORIGINAL / "canonical.py"]
        anchor = b"    pure = PurePosixPath(value)\n"
        addition = b'    if any(part in {"", ".", ".."} for part in value.split("/")):\n        raise RuntimeProfileError("virtual path escapes its public namespace")\n'
        self.assertEqual(base.count(anchor), 1)
        self.assertEqual(base.replace(anchor, addition + anchor), CAPTURED[PACKAGE / "canonical.py"])
        base = CAPTURED[ORIGINAL / "source_audit.py"]
        old_comment = b"    # Locally defined wrappers are not foreign APIs. Unknown Windows-family\n    # names require rejection rather than silently disappearing from inventory.\n"
        new_comment = b"    # Locally defined wrappers are not foreign APIs. This bounded diagnostic\n    # rejects unclassified calls only in the name families listed below,\n    # including MoveFile; it is not a complete Windows API classifier.\n"
        self.assertEqual(base.count(old_comment), 1)
        self.assertEqual(base.count(b"Interlocked|FlushFile|DeviceIoControl|"), 1)
        self.assertEqual(base.replace(old_comment, new_comment).replace(b"Interlocked|FlushFile|DeviceIoControl|", b"Interlocked|FlushFile|MoveFile|DeviceIoControl|"), CAPTURED[PACKAGE / "source_audit.py"])


class CountingResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.subtest_count = 0

    def addSubTest(self, test, subtest, err):
        self.subtest_count += 1
        super().addSubTest(test, subtest, err)


if __name__ == "__main__":
    started = time.monotonic()
    pre = authenticate()
    canonical, audit, Error = package_modules("_a02_candidate")
    base_canonical, base_audit, BaseError = package_modules("_a02_baseline", baseline=True)
    cpp = CAPTURED[IMPLEMENTATION / "native/s0_neutral_preloader_v0_5.cpp"]
    base_cpp = CAPTURED[ORIGINAL / "s0_neutral_preloader_v0_5.cpp"]
    INITIAL = cpp_scope(cpp, "VerifyEffectivePackage", "RuntimeRow")
    REVERIFY = cpp_scope(cpp, "ReverifyPackage", "FileIdentity")
    BASE_INITIAL = cpp_scope(base_cpp, "VerifyEffectivePackage", "RuntimeRow")
    BASE_REVERIFY = cpp_scope(base_cpp, "ReverifyPackage", "FileIdentity")
    stream = io.StringIO()
    result = unittest.TextTestRunner(stream=stream, verbosity=2, resultclass=CountingResult).run(unittest.defaultTestLoader.loadTestsFromTestCase(SourceCorrections))
    post = authenticate()
    if pre != post:
        raise RuntimeError("pre/post integrity or identity changed")
    report = {
        "candidate": "a02-native-source-corrections-v0.1", "role": "TEST/VERIFICATION",
        "outcome": "pass" if result.wasSuccessful() else "fail",
        "tests": result.testsRun, "subtests": result.subtest_count,
        "failures": len(result.failures), "errors": len(result.errors), "skips": len(result.skipped),
        "command": COMMAND, "working_directory": ROOT.as_posix(),
        "interpreter": {"path": sys.executable, "version": sys.version, "sha256": digest(PYTHON.read_bytes()), "flags": ["-I", "-S", "-B"]},
        "imports": IMPORTS, "pre": pre, "post": post, "pre_post_equal": pre == post,
        "test_file_sha256": digest(Path(__file__).read_bytes()),
        "elapsed_seconds": round(time.monotonic() - started, 6),
        "discrimination": {"F01": "baseline initial 7 / reverify 6; candidate both exact 7", "F08": "baseline accepts four dot aliases; candidate rejects direct and manifest aliases", "API": "baseline accepts MoveFileW text; candidate rejects; GetTempPathW rejection retained"},
        "minimal_diff": {"cpp": "one P5 physical-list entry", "canonical": "raw-segment rejection before PurePosixPath", "source_audit": "MoveFile family plus bounded-diagnostic comment"},
        "limits": [
            "Source/unit/static verification only; not a native runnable candidate, compilation, native call, object, or PE check.",
            "In-memory benign unit strings only; no S0/E0 fixture, execution, scoring, hidden oracle, F0 content, provider call, or network.",
            "Lexical paths only; OS containment, ACL, volume/root identity, symlink/junction/reparse, rename/replacement, retained handles, repository exclusion, and TOCTOU remain unverified.",
            "API checks cover only the bounded name families; not all APIs or capability/sandbox acceptance authority.",
            "CPython, standard library, OS, Git identity tool, and output root trusted; hostile import/native closure, introspection, fields, concurrency, and secure evidence production unverified.",
            "Source snapshot originals are recovery inputs, not newly validated native execution material; no operational safety or economic/model-transfer claim.",
        ],
    }
    output = CANDIDATE / "verification"
    output.mkdir(exist_ok=True)
    stdout = "Command: " + COMMAND + "\n\n" + stream.getvalue()
    (output / "test-stdout.txt").write_bytes(stdout.encode("utf-8"))
    report["stdout_sha256"] = digest(stdout.encode("utf-8"))
    (output / "test-results.json").write_bytes((json.dumps(report, indent=2, sort_keys=True) + "\n").encode("utf-8"))
    print(stdout, end="")
    print(json.dumps({"outcome": report["outcome"], "tests": report["tests"], "subtests": report["subtests"], "failures": report["failures"], "errors": report["errors"], "skips": report["skips"], "pre_post_equal": report["pre_post_equal"]}))
    sys.exit(0 if result.wasSuccessful() else 1)

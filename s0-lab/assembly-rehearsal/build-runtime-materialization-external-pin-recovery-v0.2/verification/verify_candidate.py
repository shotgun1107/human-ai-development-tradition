from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import secrets
import stat
import subprocess
import sys
import sysconfig
import tempfile


V02_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
PACKAGE_PREFIX = "s0_public_external_pin_recovery"

EXPECTED_HASHES = {
    "implementation/s0_public_external_pin_recovery/__init__.py": "56b43e5091371afa2ac2b96ac0220744537e5bc1b6bf0274da822a1ee9c18ccb",
    "implementation/s0_public_external_pin_recovery/errors.py": "bdb75b464b3e381d53acd44d477c8f837c170ccbe7844b019969c451ed6168d2",
    "implementation/s0_public_external_pin_recovery/pins.py": "8ec74ae91a452a6c4367977364462ce273d6ff6307a0b8b43f517f54c224576d",
    "implementation/s0_public_external_pin_recovery/canonical.py": "bafea3f6e2b4f19e98edbbea0a70a05750e9f2fa12b57c84f963269e6ed7a461",
    "implementation/s0_public_external_pin_recovery/candidate.py": "23365c09e2369024adce3faa5bba83bcb6ab71cd0d6c7e0f9506e022cf762d43",
    "implementation/s0_public_external_pin_recovery/win32_secure.py": "b9c64a30cdf3e15c1334b4078ee4572cabf696c1ba4dada1e67abb43af013149",
    "implementation/s0_public_external_pin_recovery/acquisition.py": "3b8790b981dbf372e2147866c3fed11affb34dc92a4ccd3b78a8c84cebebc9f6",
    "implementation/s0_public_external_pin_recovery/materialize.py": "b5cd48c1a0a714f164c71ff30df430a27b0eb2e4452795e30c8dbad1cb37f5a5",
    "tests/test_foundation_acquisition.py": "79fe011b09d28fe52313b26daf8a283d557466e4740a5d2bee401b0b1f9943bb",
    "tests/test_materialization_security.py": "4c24b9df3c5571916968ed763700d7c05a151350d3456c08e48c3ba7e34b8cf4",
}
EXPECTED_TESTS = (
    ("tests/test_foundation_acquisition.py", 11),
    ("tests/test_materialization_security.py", 8),
)
EXPECTED_PIN_ROWS = {
    "cpython-3.12.10-embed-amd64": {
        "expected_sha256": "4acbed6dd1c744b0376e3b1cf57ce906f9dc9e95e68824584c8099a63025a3c3",
        "expected_size": None,
        "filename": "python-3.12.10-embed-amd64.zip",
        "max_size": 24 * 1024 * 1024 * 1024,
        "url": "https://www.python.org/ftp/python/3.12.10/python-3.12.10-embed-amd64.zip",
    },
    "jsonschema-4.26.0-py3-none-any": {
        "expected_sha256": "d489f15263b8d200f8387e64b4c3a75f06629559fb73deb8fdfb525f2dab50ce",
        "expected_size": 90630,
        "filename": "jsonschema-4.26.0-py3-none-any.whl",
        "max_size": 90630,
        "url": None,
    },
    "vs-build-tools-17.14.39-17.14.37614.0": {
        "expected_sha256": None,
        "expected_size": None,
        "filename": "vs_BuildTools.exe",
        "max_size": 24 * 1024 * 1024 * 1024,
        "url": "https://download.visualstudio.microsoft.com/download/pr/"
        "fa619120-9c0e-47e6-bfe0-3ee96fb671b2/"
        "236367b68ba9a51708263ab10a1c85546cc4a8eca78b365168811d19c4fb2f29/"
        "vs_BuildTools.exe",
    },
}
EXPECTED_DIRECTORIES = {
    "implementation",
    "implementation/s0_public_external_pin_recovery",
    "tests",
}
REPARSE_ATTRIBUTE = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)


class VerificationFailure(RuntimeError):
    pass


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _is_reparse(status: os.stat_result) -> bool:
    return bool(getattr(status, "st_file_attributes", 0) & REPARSE_ATTRIBUTE)


def _scan_inventory(root: Path) -> None:
    observed_files: set[str] = set()
    observed_directories: set[str] = set()

    def visit(directory: Path, relative: str) -> None:
        status = os.stat(directory, follow_symlinks=False)
        if _is_reparse(status) or stat.S_ISLNK(status.st_mode) or not stat.S_ISDIR(status.st_mode):
            raise VerificationFailure(f"directory is reparse, symlink, or non-directory: {relative}")
        observed_directories.add(relative)
        with os.scandir(directory) as entries:
            for entry in entries:
                child_relative = f"{relative}/{entry.name}" if relative else entry.name
                child_status = entry.stat(follow_symlinks=False)
                if entry.is_symlink() or _is_reparse(child_status):
                    raise VerificationFailure(f"reparse or symlink inventory entry: {child_relative}")
                if stat.S_ISDIR(child_status.st_mode):
                    visit(Path(entry.path), child_relative)
                elif stat.S_ISREG(child_status.st_mode):
                    observed_files.add(child_relative)
                else:
                    raise VerificationFailure(f"non-regular inventory entry: {child_relative}")

    visit(root / "implementation", "implementation")
    visit(root / "tests", "tests")
    if observed_directories != EXPECTED_DIRECTORIES or observed_files != set(EXPECTED_HASHES):
        raise VerificationFailure(
            "complete executable/importable inventory mismatch: "
            + json.dumps(
                {
                    "extra_directories": sorted(observed_directories - EXPECTED_DIRECTORIES),
                    "extra_files": sorted(observed_files - set(EXPECTED_HASHES)),
                    "missing_directories": sorted(EXPECTED_DIRECTORIES - observed_directories),
                    "missing_files": sorted(set(EXPECTED_HASHES) - observed_files),
                },
                sort_keys=True,
            )
        )


def _read_bound_file(path: Path) -> bytes:
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0)
    descriptor = os.open(path, flags)
    try:
        before = os.fstat(descriptor)
        named = os.stat(path, follow_symlinks=False)
        if (
            _is_reparse(before)
            or _is_reparse(named)
            or not stat.S_ISREG(before.st_mode)
            or (before.st_dev, before.st_ino, before.st_size) != (named.st_dev, named.st_ino, named.st_size)
        ):
            raise VerificationFailure(f"input handle/name binding changed: {path.name}")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(descriptor)
        if (before.st_dev, before.st_ino, before.st_size) != (after.st_dev, after.st_ino, after.st_size):
            raise VerificationFailure(f"input handle changed while reading: {path.name}")
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def _observe_interpreter() -> dict[str, object]:
    path = Path(sys.executable).resolve(strict=True)
    data = _read_bound_file(path)
    status = os.stat(path, follow_symlinks=False)
    return {
        "device": status.st_dev,
        "inode": status.st_ino,
        "path": str(path),
        "sha256": _sha256(data),
        "size": status.st_size,
    }


def _observe_loaded_stdlib_modules() -> list[dict[str, object]]:
    names = (
        "base64",
        "hashlib",
        "json",
        "os",
        "pathlib",
        "platform",
        "stat",
        "subprocess",
        "sysconfig",
        "tempfile",
    )
    observations: list[dict[str, object]] = []
    for name in names:
        module = sys.modules.get(name)
        origin = getattr(module, "__file__", None)
        entry: dict[str, object] = {"module": name, "origin": origin}
        if type(origin) is str and Path(origin).is_file():
            try:
                data = _read_bound_file(Path(origin).resolve(strict=True))
                entry["observed_sha256"] = _sha256(data)
                entry["observed_size"] = len(data)
            except VerificationFailure as exc:
                entry["observation_error"] = str(exc)
        observations.append(entry)
    return observations


def _host_runtime_prerequisite(
    interpreter_pre: dict[str, object], interpreter_post: dict[str, object]
) -> dict[str, object]:
    if interpreter_pre != interpreter_post:
        raise VerificationFailure("launched interpreter identity or bytes changed")
    return {
        "authority": "UNAUTHENTICATED/TRUSTED-PREREQUISITE",
        "blocker_ids": ["RUNTIME-PROFILE"],
        "claim_scope": (
            "Authenticated candidate/test byte binding only; interpreter, stdlib, site, "
            "platform, and OS-DLL execution prerequisites remain unverified."
        ),
        "executable_import_closure_authenticated": False,
        "interpreter": {"post": interpreter_post, "pre": interpreter_pre, "stable": True},
        "os_dll_execution_closure_authenticated": False,
        "platform": {
            "implementation": sys.implementation.name,
            "platform": platform.platform(),
            "python_build": list(platform.python_build()),
            "python_version": platform.python_version(),
            "sys_version": sys.version,
            "sysconfig_platform": sysconfig.get_platform(),
        },
        "site_enabled": not bool(sys.flags.no_site),
        "stdlib": {
            "loaded_module_observations": _observe_loaded_stdlib_modules(),
            "path": sysconfig.get_path("stdlib"),
            "stdlib_import_closure_authenticated": False,
        },
    }


RESULT_MARKER = "__S0_BOUND_RESULT__="


def _validate_child_result(
    output: str,
    *,
    nonce: str,
    test_relative: str,
    expected_count: int,
    interpreter: dict[str, object],
) -> dict[str, object]:
    matches = re.findall(
        rf"^{re.escape(RESULT_MARKER)}([^\r\n]+)$", output, flags=re.MULTILINE
    )
    if len(matches) != 1:
        raise VerificationFailure("missing or duplicate structured child result")
    try:
        record = json.loads(matches[0])
    except json.JSONDecodeError as exc:
        raise VerificationFailure("structured child result is not JSON") from exc
    expected = {
        "challenge": nonce,
        "errors": 0,
        "expected_count": expected_count,
        "expected_failures": 0,
        "failures": 0,
        "observed_count": expected_count,
        "skips": 0,
        "successful": True,
        "test_relative": test_relative,
        "unexpected_successes": 0,
    }
    if type(record) is not dict or any(record.get(key) != value for key, value in expected.items()):
        raise VerificationFailure("structured child result fields or challenge mismatch")
    runtime = record.get("runtime_observation")
    if (
        type(runtime) is not dict
        or runtime.get("interpreter_path") != interpreter["path"]
        or runtime.get("interpreter_sha256") != interpreter["sha256"]
        or runtime.get("interpreter_size") != interpreter["size"]
        or runtime.get("isolated") is not True
        or runtime.get("no_site") is not True
        or runtime.get("dont_write_bytecode") is not True
    ):
        raise VerificationFailure("structured child runtime observation mismatch")
    return record


def _authenticate_once(root: Path) -> tuple[dict[str, bytes], dict[str, str]]:
    _scan_inventory(root)
    values = {relative: _read_bound_file(root / relative) for relative in EXPECTED_HASHES}
    observed = {relative: _sha256(values[relative]) for relative in sorted(values)}
    expected = {relative: EXPECTED_HASHES[relative] for relative in sorted(EXPECTED_HASHES)}
    if observed != expected:
        raise VerificationFailure("path-bound source/test hash mismatch")
    return values, observed


def _write_fixture(root: Path, values: dict[str, bytes]) -> None:
    for relative, data in values.items():
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("xb") as output:
            output.write(data)


def _expect_rejection(root: Path) -> bool:
    executed = False
    try:
        _authenticate_once(root)
        executed = True
    except VerificationFailure:
        pass
    if executed:
        raise VerificationFailure("sentinel reached execution after rejected filesystem input")
    return True


def _run_filesystem_sentinels(baseline: dict[str, bytes]) -> dict[str, bool]:
    results: dict[str, bool] = {}
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary) / "shadow-pyd"
        _write_fixture(root, baseline)
        (root / "implementation" / "shadow_native.pyd").write_bytes(b"not-loadable")
        results["shadow_pyd_rejected_before_execution"] = _expect_rejection(root)
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary) / "shadow-pyc"
        _write_fixture(root, baseline)
        cache = root / "tests" / "__pycache__"
        cache.mkdir()
        (cache / "shadow.cpython-312.pyc").write_bytes(b"not-bytecode")
        results["shadow_pyc_rejected_before_execution"] = _expect_rejection(root)
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary) / "path-swap"
        _write_fixture(root, baseline)
        first = root / "tests/test_foundation_acquisition.py"
        second = root / "tests/test_materialization_security.py"
        first_bytes, second_bytes = first.read_bytes(), second.read_bytes()
        first.write_bytes(second_bytes)
        second.write_bytes(first_bytes)
        results["path_byte_swap_rejected_before_execution"] = _expect_rejection(root)
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary) / "mutation"
        _write_fixture(root, baseline)
        target = root / "implementation/s0_public_external_pin_recovery/canonical.py"
        data = target.read_bytes()
        target.write_bytes(bytes([data[0] ^ 1]) + data[1:])
        results["filesystem_mutation_rejected_before_execution"] = _expect_rejection(root)
    fake_interpreter = {"path": "C:\\bound-python.exe", "sha256": "1" * 64, "size": 1}
    forged = {
        "challenge": "attacker-challenge",
        "errors": 0,
        "expected_count": 11,
        "expected_failures": 0,
        "failures": 0,
        "observed_count": 11,
        "runtime_observation": {
            "dont_write_bytecode": True,
            "interpreter_path": fake_interpreter["path"],
            "interpreter_sha256": fake_interpreter["sha256"],
            "interpreter_size": fake_interpreter["size"],
            "isolated": True,
            "no_site": True,
        },
        "skips": 0,
        "successful": True,
        "test_relative": "tests/test_foundation_acquisition.py",
        "unexpected_successes": 0,
    }
    forged_output = RESULT_MARKER + json.dumps(forged, sort_keys=True, separators=(",", ":"))
    try:
        _validate_child_result(
            forged_output,
            nonce="real-unpredictable-challenge",
            test_relative="tests/test_foundation_acquisition.py",
            expected_count=11,
            interpreter=fake_interpreter,
        )
    except VerificationFailure:
        results["forged_structured_child_result_rejected"] = True
    else:
        raise VerificationFailure("forged structured child result was accepted")
    return results


BOOTSTRAP = r'''
import base64
import hashlib
import importlib.abc
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
import types
import unittest

payload = json.loads(sys.stdin.read())
challenge = payload["challenge"]
expected = payload["expected_hashes"]
files = {name: base64.b64decode(value) for name, value in payload["files"].items()}
if set(files) != set(expected):
    raise SystemExit("bootstrap path set mismatch")
for name, data in files.items():
    if hashlib.sha256(data).hexdigest() != expected[name]:
        raise SystemExit("bootstrap byte hash mismatch: " + name)

package_prefix = "s0_public_external_pin_recovery"
module_sources = {}
module_paths = {}
for relative, data in files.items():
    if not relative.startswith("implementation/"):
        continue
    stem = Path(relative).stem
    module_name = package_prefix if stem == "__init__" else package_prefix + "." + stem
    module_sources[module_name] = data
    module_paths[module_name] = relative

class MemoryFinder(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def __init__(self, support_root):
        self.support_root = support_root
    def find_spec(self, fullname, path=None, target=None):
        if fullname in module_sources:
            return importlib.util.spec_from_loader(
                fullname, self, is_package=(fullname == package_prefix)
            )
        if fullname.startswith(package_prefix + "."):
            raise ImportError("unexpected candidate module: " + fullname)
        return None
    def create_module(self, spec):
        return None
    def exec_module(self, module):
        relative = module_paths[module.__name__]
        filename = str(self.support_root / relative)
        module.__file__ = filename
        if module.__name__ == package_prefix:
            module.__path__ = [str(Path(filename).parent)]
            module.__package__ = package_prefix
        else:
            module.__package__ = module.__name__.rpartition(".")[0]
        exec(compile(module_sources[module.__name__], filename, "exec"), module.__dict__)

def verify_support(root):
    observed = set()
    for directory, directories, filenames in os.walk(root, followlinks=False):
        for dirname in directories:
            status = os.stat(Path(directory) / dirname, follow_symlinks=False)
            if getattr(status, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400):
                raise RuntimeError("support reparse directory")
        for filename in filenames:
            path = Path(directory) / filename
            status = os.stat(path, follow_symlinks=False)
            if getattr(status, "st_file_attributes", 0) & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400):
                raise RuntimeError("support reparse file")
            relative = path.relative_to(root).as_posix()
            observed.add(relative)
            if relative not in expected or hashlib.sha256(path.read_bytes()).hexdigest() != expected[relative]:
                raise RuntimeError("support bytes changed: " + relative)
    if observed != set(expected):
        raise RuntimeError("support inventory changed")

with tempfile.TemporaryDirectory() as temporary:
    repository = Path(temporary)
    v02 = repository / "s0-lab/assembly-rehearsal/build-runtime-materialization-external-pin-recovery-v0.2"
    for relative, data in files.items():
        destination = v02 / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("xb") as output:
            output.write(data)
    verify_support(v02)
    finder = MemoryFinder(v02)
    sys.meta_path.insert(0, finder)
    test_relative = payload["test_relative"]
    test_bytes = files[test_relative]
    test_path = str(v02 / test_relative)
    module_name = "_s0_bound_test_" + hashlib.sha256(test_relative.encode("utf-8")).hexdigest()
    test_module = types.ModuleType(module_name)
    test_module.__file__ = test_path
    test_module.__package__ = None
    sys.modules[module_name] = test_module
    try:
        exec(compile(test_bytes, test_path, "exec"), test_module.__dict__)
        suite = unittest.defaultTestLoader.loadTestsFromModule(test_module)
        result = unittest.TextTestRunner(stream=sys.stderr, verbosity=2).run(suite)
        interpreter_path = Path(sys.executable).resolve(strict=True)
        interpreter_bytes = interpreter_path.read_bytes()
        record = {
            "challenge": challenge,
            "errors": len(result.errors),
            "expected_count": payload["expected_count"],
            "expected_failures": len(result.expectedFailures),
            "failures": len(result.failures),
            "observed_count": result.testsRun,
            "runtime_observation": {
                "dont_write_bytecode": bool(sys.flags.dont_write_bytecode),
                "interpreter_path": str(interpreter_path),
                "interpreter_sha256": hashlib.sha256(interpreter_bytes).hexdigest(),
                "interpreter_size": len(interpreter_bytes),
                "isolated": bool(sys.flags.isolated),
                "no_site": bool(sys.flags.no_site),
            },
            "skips": len(result.skipped),
            "successful": result.wasSuccessful(),
            "test_relative": test_relative,
            "unexpected_successes": len(result.unexpectedSuccesses),
        }
        print("__S0_BOUND_RESULT__=" + json.dumps(record, sort_keys=True, separators=(",", ":")))
        exit_code = 0 if result.wasSuccessful() else 1
    finally:
        verify_support(v02)
        sys.meta_path.remove(finder)
        sys.modules.pop(module_name, None)
    raise SystemExit(exit_code)
'''


def _run_test_from_bound_bytes(
    baseline: dict[str, bytes],
    relative: str,
    expected_count: int,
    interpreter: dict[str, object],
) -> dict[str, object]:
    nonce = secrets.token_hex(32)
    payload = {
        "challenge": nonce,
        "expected_hashes": EXPECTED_HASHES,
        "expected_count": expected_count,
        "files": {
            name: base64.b64encode(data).decode("ascii") for name, data in baseline.items()
        },
        "test_relative": relative,
    }
    command = [str(interpreter["path"]), "-I", "-S", "-B", "-c", BOOTSTRAP]
    with tempfile.TemporaryDirectory() as isolated_cwd:
        completed = subprocess.run(
            command,
            cwd=isolated_cwd,
            input=json.dumps(payload, sort_keys=True, separators=(",", ":")),
            text=True,
            capture_output=True,
            timeout=180,
            check=False,
        )
    output = completed.stdout + completed.stderr
    if completed.returncode != 0:
        raise VerificationFailure(
            f"bound-byte isolated test failed for {relative}: return={completed.returncode}\n{output}"
        )
    structured = _validate_child_result(
        output,
        nonce=nonce,
        test_relative=relative,
        expected_count=expected_count,
        interpreter=interpreter,
    )
    return {
        "challenge_sha256": _sha256(nonce.encode("ascii")),
        "child_runtime_observation": structured["runtime_observation"],
        "execution_binding": "authenticated-candidate-test-bytes-via-stdin-memory-loader",
        "expected_count": expected_count,
        "observed_count": structured["observed_count"],
        "returncode": completed.returncode,
        "failures": 0,
        "errors": 0,
        "skips": 0,
        "expected_failures": 0,
        "test_relative": relative,
    }


def _write_evidence(path: Path, evidence: dict[str, object]) -> str:
    encoded = json.dumps(
        evidence, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    digest = _sha256(encoded)
    if path.exists() or not path.parent.is_dir():
        raise VerificationFailure("verifier evidence output must be fresh under existing parent")
    with path.open("xb") as output:
        output.write(encoded)
    with Path(str(path) + ".sha256").open("xb") as output:
        output.write((digest + "\n").encode("ascii"))
    return digest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--evidence-out", required=True)
    args = parser.parse_args()
    evidence_path = Path(args.evidence_out).resolve(strict=False)
    if not (sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode):
        raise VerificationFailure("verifier must run with python -I -S -B")

    interpreter_pre = _observe_interpreter()
    baseline, pre_hashes = _authenticate_once(V02_ROOT)
    sentinels = _run_filesystem_sentinels(baseline)
    tests: list[dict[str, object]] = []
    for relative, count in EXPECTED_TESTS:
        if _observe_interpreter() != interpreter_pre:
            raise VerificationFailure("interpreter changed before child launch")
        tests.append(
            _run_test_from_bound_bytes(
                baseline, relative, count, interpreter_pre
            )
        )
        if _observe_interpreter() != interpreter_pre:
            raise VerificationFailure("interpreter changed after child launch")
    _post_values, post_hashes = _authenticate_once(V02_ROOT)
    if post_hashes != pre_hashes:
        raise VerificationFailure("source/test paths changed during bound-byte execution")
    interpreter_post = _observe_interpreter()
    runtime_prerequisite = _host_runtime_prerequisite(
        interpreter_pre, interpreter_post
    )
    evidence = {
        "candidate": "build-runtime-materialization-external-pin-recovery-v0.2",
        "claim_scope": (
            "Authenticated candidate/test byte binding only under an unverified "
            "host-runtime trusted prerequisite."
        ),
        "execution_binding": "authenticated-candidate-test-bytes-via-stdin-memory-loader",
        "host_runtime_prerequisite": runtime_prerequisite,
        "input_count": len(EXPECTED_HASHES),
        "pin_rows": EXPECTED_PIN_ROWS,
        "post_hashes": post_hashes,
        "pre_hashes": pre_hashes,
        "sentinels": sentinels,
        "status": "verified-candidate-test-bytes-under-unverified-host-runtime",
        "tests": tests,
    }
    digest = _write_evidence(evidence_path, evidence)
    print("VERIFICATION_EVIDENCE_PATH=" + str(evidence_path))
    print("VERIFICATION_EVIDENCE_SHA256=" + digest)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except VerificationFailure as exc:
        print(f"VERIFICATION_FAILED={exc}", file=sys.stderr)
        raise SystemExit(1)

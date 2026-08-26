from __future__ import annotations

import argparse
import atexit
import hashlib
import importlib.abc
import importlib.util
import json
import os
from pathlib import Path
import platform
import stat
import subprocess
import sys
import sysconfig
import tempfile
import urllib.request


V02_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
IMPLEMENTATION_ROOT = V02_ROOT / "implementation"
CANDIDATE_PREFIX = "s0_public_external_pin_recovery"
CANDIDATE_ID = "build-runtime-materialization-external-pin-recovery-v0.2"


EXPECTED_INPUT_HASHES = {
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
EXPECTED_PIN_ROWS = {
    "vs-build-tools-17.14.39-17.14.37614.0": (
        "vs_BuildTools.exe",
        "https://download.visualstudio.microsoft.com/download/pr/"
        "fa619120-9c0e-47e6-bfe0-3ee96fb671b2/"
        "236367b68ba9a51708263ab10a1c85546cc4a8eca78b365168811d19c4fb2f29/"
        "vs_BuildTools.exe",
        None,
        None,
        24 * 1024 * 1024 * 1024,
    ),
    "cpython-3.12.10-embed-amd64": (
        "python-3.12.10-embed-amd64.zip",
        "https://www.python.org/ftp/python/3.12.10/python-3.12.10-embed-amd64.zip",
        "4acbed6dd1c744b0376e3b1cf57ce906f9dc9e95e68824584c8099a63025a3c3",
        None,
        24 * 1024 * 1024 * 1024,
    ),
    "jsonschema-4.26.0-py3-none-any": (
        "jsonschema-4.26.0-py3-none-any.whl",
        None,
        "d489f15263b8d200f8387e64b4c3a75f06629559fb73deb8fdfb525f2dab50ce",
        90630,
        90630,
    ),
}
CHUNK_SIZE = 1024 * 1024
EXPECTED_DIRECTORIES = {
    "implementation",
    "implementation/s0_public_external_pin_recovery",
    "tests",
}
REPARSE_ATTRIBUTE = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)


class LiveFailure(RuntimeError):
    pass


class RejectRedirects(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise LiveFailure(f"redirect_not_permitted: status={code}")


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_json_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        allow_nan=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def _is_reparse(status: os.stat_result) -> bool:
    return bool(getattr(status, "st_file_attributes", 0) & REPARSE_ATTRIBUTE)


def _scan_inventory(root: Path) -> None:
    observed_files: set[str] = set()
    observed_directories: set[str] = set()

    def visit(directory: Path, relative: str) -> None:
        status = os.stat(directory, follow_symlinks=False)
        if _is_reparse(status) or stat.S_ISLNK(status.st_mode) or not stat.S_ISDIR(status.st_mode):
            raise LiveFailure(f"directory inventory binding invalid: {relative}")
        observed_directories.add(relative)
        with os.scandir(directory) as entries:
            for entry in entries:
                child_relative = f"{relative}/{entry.name}" if relative else entry.name
                child_status = entry.stat(follow_symlinks=False)
                if entry.is_symlink() or _is_reparse(child_status):
                    raise LiveFailure(f"reparse/symlink inventory entry: {child_relative}")
                if stat.S_ISDIR(child_status.st_mode):
                    visit(Path(entry.path), child_relative)
                elif stat.S_ISREG(child_status.st_mode):
                    observed_files.add(child_relative)
                else:
                    raise LiveFailure(f"non-regular inventory entry: {child_relative}")

    visit(root / "implementation", "implementation")
    visit(root / "tests", "tests")
    if observed_directories != EXPECTED_DIRECTORIES or observed_files != set(EXPECTED_INPUT_HASHES):
        raise LiveFailure("complete source/test inventory mismatch before candidate import")


def _read_bound_file(path: Path) -> bytes:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_BINARY", 0))
    try:
        before = os.fstat(descriptor)
        named = os.stat(path, follow_symlinks=False)
        if (
            _is_reparse(before)
            or _is_reparse(named)
            or not stat.S_ISREG(before.st_mode)
            or (before.st_dev, before.st_ino, before.st_size)
            != (named.st_dev, named.st_ino, named.st_size)
        ):
            raise LiveFailure(f"input handle/name binding changed: {path.name}")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(descriptor)
        if (before.st_dev, before.st_ino, before.st_size) != (
            after.st_dev,
            after.st_ino,
            after.st_size,
        ):
            raise LiveFailure(f"input changed while reading: {path.name}")
        return b"".join(chunks)
    finally:
        os.close(descriptor)


def _authenticate_inputs(root: Path) -> tuple[dict[str, bytes], dict[str, str]]:
    _scan_inventory(root)
    values = {
        relative: _read_bound_file(root / relative) for relative in EXPECTED_INPUT_HASHES
    }
    observed = {relative: _sha256(values[relative]) for relative in sorted(values)}
    expected = {
        relative: EXPECTED_INPUT_HASHES[relative] for relative in sorted(EXPECTED_INPUT_HASHES)
    }
    if observed != expected:
        raise LiveFailure("source/test hash mismatch before candidate import")
    return values, observed


def _assert_candidate_not_loaded() -> None:
    loaded = sorted(
        name
        for name in sys.modules
        if name == CANDIDATE_PREFIX or name.startswith(CANDIDATE_PREFIX + ".")
    )
    if loaded:
        raise LiveFailure("candidate module loaded before authenticated-byte activation")


class CandidateMemoryFinder(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def __init__(self, values: dict[str, bytes]) -> None:
        self.sources: dict[str, tuple[str, bytes]] = {}
        for relative, data in values.items():
            if not relative.startswith("implementation/"):
                continue
            stem = Path(relative).stem
            name = CANDIDATE_PREFIX if stem == "__init__" else CANDIDATE_PREFIX + "." + stem
            self.sources[name] = (relative, data)

    def find_spec(self, fullname, path=None, target=None):
        if fullname in self.sources:
            return importlib.util.spec_from_loader(
                fullname, self, is_package=(fullname == CANDIDATE_PREFIX)
            )
        if fullname.startswith(CANDIDATE_PREFIX + "."):
            raise ImportError("unexpected candidate module: " + fullname)
        return None

    def create_module(self, spec):
        return None

    def exec_module(self, module) -> None:
        relative, data = self.sources[module.__name__]
        filename = "<authenticated-memory>/" + relative
        module.__file__ = filename
        if module.__name__ == CANDIDATE_PREFIX:
            module.__path__ = ["<authenticated-memory>/implementation/" + CANDIDATE_PREFIX]
            module.__package__ = CANDIDATE_PREFIX
        else:
            module.__package__ = module.__name__.rpartition(".")[0]
        exec(compile(data, filename, "exec"), module.__dict__)


def _activate_candidate(values: dict[str, bytes]) -> CandidateMemoryFinder:
    global acquisition, candidate, materialize, pins, win32_secure
    _assert_candidate_not_loaded()
    finder = CandidateMemoryFinder(values)
    sys.meta_path.insert(0, finder)
    try:
        importlib.import_module(CANDIDATE_PREFIX)
        acquisition = importlib.import_module(CANDIDATE_PREFIX + ".acquisition")
        candidate = importlib.import_module(CANDIDATE_PREFIX + ".candidate")
        materialize = importlib.import_module(CANDIDATE_PREFIX + ".materialize")
        pins = importlib.import_module(CANDIDATE_PREFIX + ".pins")
        win32_secure = importlib.import_module(CANDIDATE_PREFIX + ".win32_secure")
    except Exception:
        sys.meta_path.remove(finder)
        for name in tuple(sys.modules):
            if name == CANDIDATE_PREFIX or name.startswith(CANDIDATE_PREFIX + "."):
                sys.modules.pop(name, None)
        raise
    return finder


def _observe_file(path: Path) -> dict[str, object]:
    path = path.resolve(strict=True)
    data = _read_bound_file(path)
    status = os.stat(path, follow_symlinks=False)
    return {
        "device": status.st_dev,
        "inode": status.st_ino,
        "path": str(path),
        "sha256": _sha256(data),
        "size": status.st_size,
    }


def _live_producer_prerequisite() -> dict[str, object]:
    return {
        "authority": "UNAUTHENTICATED/TRUSTED-PREREQUISITE",
        "blocker_ids": ["ACQUISITION-PRODUCER", "RUNTIME-PROFILE"],
        "candidate_load_binding": (
            "Authenticated source bytes loaded by in-memory finder with no mutable "
            "repository-path fallback."
        ),
        "claim_scope": (
            "Live evidence is produced under an unverified harness, interpreter, stdlib, "
            "platform, OS-DLL, and network-stack prerequisite."
        ),
        "host_runtime": {
            "interpreter": _observe_file(Path(sys.executable)),
            "platform": platform.platform(),
            "python_version": platform.python_version(),
            "stdlib_path": sysconfig.get_path("stdlib"),
        },
        "live_harness": _observe_file(Path(__file__)),
        "producer_authenticated": False,
        "runtime_authenticated": False,
    }


def _pin_mapping(pin: pins.ArtifactPin) -> dict[str, object]:
    return {
        "expected_sha256": pin.expected_sha256,
        "expected_size": pin.expected_size,
        "filename": pin.filename,
        "max_size": pin.max_size,
        "pin_id": pin.pin_id,
        "url": pin.url,
    }


def _verify_pins() -> dict[str, dict[str, object]]:
    if set(pins.APPROVED_PINS) != set(EXPECTED_PIN_ROWS):
        raise LiveFailure("closed pin ID set changed")
    result: dict[str, dict[str, object]] = {}
    for pin_id, expected in EXPECTED_PIN_ROWS.items():
        pin = pins.resolve_approved_pin(pin_id)
        observed = (pin.filename, pin.url, pin.expected_sha256, pin.expected_size, pin.max_size)
        if observed != expected:
            raise LiveFailure(f"closed pin row changed: {pin_id}")
        result[pin_id] = _pin_mapping(pin)
    return result


def _expected_verifier_pin_rows() -> dict[str, dict[str, object]]:
    return {
        pin_id: {
            "expected_sha256": row[2],
            "expected_size": row[3],
            "filename": row[0],
            "max_size": row[4],
            "url": row[1],
        }
        for pin_id, row in EXPECTED_PIN_ROWS.items()
    }


def _read_verifier_record(path: Path) -> tuple[dict[str, object], str]:
    if not path.is_absolute():
        raise LiveFailure("verification evidence path must be absolute")
    path = path.resolve(strict=True)
    repository = REPOSITORY_ROOT.resolve(strict=True)
    if _is_within(path, repository):
        raise LiveFailure("verification evidence must be out of repository")
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_BINARY", 0))
    try:
        before = os.fstat(descriptor)
        named = os.stat(path, follow_symlinks=False)
        reparse = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
        if (
            getattr(before, "st_file_attributes", 0) & reparse
            or getattr(named, "st_file_attributes", 0) & reparse
            or not stat.S_ISREG(before.st_mode)
            or (before.st_dev, before.st_ino, before.st_size)
            != (named.st_dev, named.st_ino, named.st_size)
        ):
            raise LiveFailure("verification evidence handle/name binding is invalid")
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(descriptor)
        if (before.st_dev, before.st_ino, before.st_size) != (
            after.st_dev,
            after.st_ino,
            after.st_size,
        ):
            raise LiveFailure("verification evidence changed while reading")
    finally:
        os.close(descriptor)
    encoded = b"".join(chunks)
    try:
        record = json.loads(encoded.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise LiveFailure("verification evidence is not strict UTF-8 JSON") from exc
    if type(record) is not dict or _canonical_json_bytes(record) != encoded:
        raise LiveFailure("verification evidence is not canonical JSON")
    expected_hashes = {
        relative: EXPECTED_INPUT_HASHES[relative] for relative in sorted(EXPECTED_INPUT_HASHES)
    }
    expected_sentinels = {
        "filesystem_mutation_rejected_before_execution": True,
        "forged_structured_child_result_rejected": True,
        "path_byte_swap_rejected_before_execution": True,
        "shadow_pyc_rejected_before_execution": True,
        "shadow_pyd_rejected_before_execution": True,
    }
    prerequisite = record.get("host_runtime_prerequisite")
    prerequisite_valid = False
    if type(prerequisite) is dict:
        interpreter = prerequisite.get("interpreter")
        stdlib = prerequisite.get("stdlib")
        prerequisite_valid = bool(
            prerequisite.get("authority") == "UNAUTHENTICATED/TRUSTED-PREREQUISITE"
            and prerequisite.get("blocker_ids") == ["RUNTIME-PROFILE"]
            and prerequisite.get("executable_import_closure_authenticated") is False
            and prerequisite.get("os_dll_execution_closure_authenticated") is False
            and prerequisite.get("site_enabled") is False
            and type(interpreter) is dict
            and interpreter.get("stable") is True
            and interpreter.get("pre") == interpreter.get("post")
            and type(stdlib) is dict
            and stdlib.get("stdlib_import_closure_authenticated") is False
        )
    tests = record.get("tests")
    tests_valid = type(tests) is list and len(tests) == 2
    expected_test_rows = (
        ("tests/test_foundation_acquisition.py", 11),
        ("tests/test_materialization_security.py", 8),
    )
    if tests_valid and prerequisite_valid:
        interpreter_pre = prerequisite["interpreter"]["pre"]
        for test, (relative, expected_count) in zip(tests, expected_test_rows, strict=True):
            challenge_sha256 = test.get("challenge_sha256") if type(test) is dict else None
            child_runtime = test.get("child_runtime_observation") if type(test) is dict else None
            tests_valid = bool(
                tests_valid
                and type(test) is dict
                and test.get("execution_binding")
                == "authenticated-candidate-test-bytes-via-stdin-memory-loader"
                and test.get("test_relative") == relative
                and test.get("expected_count") == expected_count
                and test.get("observed_count") == expected_count
                and test.get("returncode") == 0
                and test.get("failures") == 0
                and test.get("errors") == 0
                and test.get("skips") == 0
                and test.get("expected_failures") == 0
                and type(challenge_sha256) is str
                and len(challenge_sha256) == 64
                and all(character in "0123456789abcdef" for character in challenge_sha256)
                and type(child_runtime) is dict
                and child_runtime.get("interpreter_path") == interpreter_pre.get("path")
                and child_runtime.get("interpreter_sha256") == interpreter_pre.get("sha256")
                and child_runtime.get("interpreter_size") == interpreter_pre.get("size")
                and child_runtime.get("isolated") is True
                and child_runtime.get("no_site") is True
                and child_runtime.get("dont_write_bytecode") is True
            )
    else:
        tests_valid = False
    if (
        record.get("candidate") != CANDIDATE_ID
        or record.get("status")
        != "verified-candidate-test-bytes-under-unverified-host-runtime"
        or record.get("claim_scope")
        != "Authenticated candidate/test byte binding only under an unverified host-runtime trusted prerequisite."
        or record.get("execution_binding")
        != "authenticated-candidate-test-bytes-via-stdin-memory-loader"
        or record.get("input_count") != len(EXPECTED_INPUT_HASHES)
        or record.get("pre_hashes") != expected_hashes
        or record.get("post_hashes") != expected_hashes
        or record.get("pin_rows") != _expected_verifier_pin_rows()
        or record.get("sentinels") != expected_sentinels
        or not prerequisite_valid
        or not tests_valid
    ):
        raise LiveFailure("verification evidence success fields, pins, or results mismatch")
    return record, _sha256(encoded)


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _validate_external_root_path(raw: str) -> Path:
    root = Path(raw)
    if not root.is_absolute():
        raise LiveFailure("external root must be absolute")
    root = root.resolve(strict=False)
    repository = REPOSITORY_ROOT.resolve(strict=True)
    if _is_within(root, repository) or _is_within(repository, root):
        raise LiveFailure("external root must be disjoint from repository")
    lowered_parts = tuple(part.casefold() for part in root.parts)
    if any("v0.1" in part or "v01" in part for part in lowered_parts):
        raise LiveFailure("v0.1 root reuse is forbidden")
    if not root.name.casefold().startswith("s0-v0.2-live-"):
        raise LiveFailure("external root name must start with s0-v0.2-live-")
    if root.exists() or not root.parent.is_dir():
        raise LiveFailure("external root must be fresh under an existing parent")
    return root


def _response_chunks(response):
    while True:
        chunk = response.read(CHUNK_SIZE)
        if not chunk:
            return
        yield chunk


def _download(pin: pins.ArtifactPin, destination: Path) -> tuple[acquisition.AcquisitionEvidence, dict[str, object]]:
    if pin.url is None:
        raise LiveFailure(f"source unavailable for {pin.pin_id}")
    request = urllib.request.Request(
        pin.url,
        headers={"Accept-Encoding": "identity", "User-Agent": "s0-v0.2-verification/1"},
        method="GET",
    )
    opener = urllib.request.build_opener(RejectRedirects)
    with opener.open(request, timeout=120) as response:
        status = getattr(response, "status", None)
        final_url = response.geturl()
        if status != 200 or final_url != pin.url:
            raise LiveFailure(f"source response mismatch for {pin.pin_id}: status={status}, url={final_url}")
        if response.headers.get("Content-Encoding", "identity").casefold() not in {"", "identity"}:
            raise LiveFailure(f"encoded transport not permitted for {pin.pin_id}")
        length_text = response.headers.get("Content-Length")
        if length_text is None or not length_text.isdigit() or int(length_text) <= 0:
            raise LiveFailure(f"exact transport size unavailable for {pin.pin_id}")
        content_length = int(length_text)
        if content_length > pin.max_size:
            raise LiveFailure(f"transport size exceeds pin bound for {pin.pin_id}")
        evidence = acquisition.acquire_pinned_artifact(
            pin,
            chunks=_response_chunks(response),
            observed_uri=final_url,
            redirect_count=0,
            destination=destination,
            repository_root=REPOSITORY_ROOT,
        )
    if evidence.observed_size != content_length:
        raise LiveFailure(f"transport/acquired size mismatch for {pin.pin_id}")
    return evidence, {
        "content_length": content_length,
        "final_url": final_url,
        "redirect_count": 0,
        "status": status,
    }


def _identity_mapping(identity: win32_secure.WindowsFileIdentity) -> dict[str, object]:
    return {"file_id": identity.file_id, "volume_serial": identity.volume_serial}


def _materialization_mapping(value: materialize.MaterializationEvidence) -> dict[str, object]:
    return {
        "acquisition_evidence_sha256": value.acquisition_evidence_sha256,
        "archive_final_identity": _identity_mapping(value.archive_final_identity),
        "archive_initial_identity": _identity_mapping(value.archive_initial_identity),
        "archive_path": value.archive_path,
        "archive_post_sha256": value.archive_post_sha256,
        "archive_pre_sha256": value.archive_pre_sha256,
        "archive_sha256": value.archive_sha256,
        "destination_path": value.destination_path,
        "directory_count": value.directory_count,
        "file_count": value.file_count,
        "files": [
            {"relative_path": item.relative_path, "sha256": item.sha256, "size": item.size}
            for item in value.files
        ],
        "final_reauthentication_passed": value.final_reauthentication_passed,
        "process_authority_granted": value.process_authority_granted,
        "root_final_identity": _identity_mapping(value.root_final_identity),
        "root_initial_identity": _identity_mapping(value.root_initial_identity),
        "target_set_sha256": value.target_set_sha256,
        "total_size": value.total_size,
    }


def _checkpoint_identity(evidence: acquisition.AcquisitionEvidence) -> win32_secure.WindowsFileIdentity:
    checkpoint = evidence.checkpoints[0]
    return win32_secure.WindowsFileIdentity(checkpoint.volume_serial, checkpoint.file_id)


def _final_reauthenticate(
    path: Path,
    *,
    expected_size: int,
    expected_sha256: str,
    expected_identity: win32_secure.WindowsFileIdentity | None = None,
) -> dict[str, object]:
    retained = win32_secure.secure_open_existing_file(
        repository_root=REPOSITORY_ROOT,
        path=path,
        expected_identity=expected_identity,
    )
    try:
        before = retained.revalidate()
        digest = retained.readback_sha256(expected_size, CHUNK_SIZE)
        after = retained.revalidate()
    finally:
        retained.close()
    if before != after or before.length != expected_size or digest != expected_sha256:
        raise LiveFailure(f"final retained-handle reauthentication failed: {path.name}")
    return {
        "identity": _identity_mapping(before.identity),
        "path": str(path),
        "sha256": digest,
        "size": before.length,
    }


def _write_root_file(
    root: win32_secure.SecureDirectoryRoot, filename: str, data: bytes
) -> tuple[Path, win32_secure.WindowsFileIdentity]:
    root.revalidate()
    output = root.create_file((), filename)
    try:
        output.write_all(data)
        output.flush()
        snapshot = output.snapshot("evidence_file_invalid")
        digest = output.readback_sha256(len(data), CHUNK_SIZE)
        final = output.final_reauthenticate(len(data))
        if (
            snapshot != final
            or snapshot.identity != output.identity
            or digest != _sha256(data)
        ):
            raise LiveFailure(f"retained evidence write failed final reauthentication: {filename}")
        path = Path(output.destination)
        identity = output.identity
    finally:
        output.close()
    root.revalidate()
    return path, identity


def _write_evidence(
    root: win32_secure.SecureDirectoryRoot, evidence: dict[str, object]
) -> tuple[Path, str]:
    encoded = _canonical_json_bytes(evidence)
    digest = _sha256(encoded)
    root.revalidate()
    evidence_path, _evidence_identity = _write_root_file(
        root, "evidence.json", encoded
    )
    _sidecar_path, _sidecar_identity = _write_root_file(
        root, "evidence.sha256", (digest + "\n").encode("ascii")
    )
    root.revalidate()
    return evidence_path, digest


def _write_fixture(root: Path, values: dict[str, bytes]) -> None:
    for relative, data in values.items():
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("xb") as output:
            output.write(data)


def _create_junction(link: Path, target: Path) -> None:
    completed = subprocess.run(
        ["cmd.exe", "/d", "/c", "mklink", "/J", str(link), str(target)],
        text=True,
        capture_output=True,
        timeout=30,
        check=False,
    )
    if completed.returncode != 0 or not link.exists():
        raise LiveFailure(
            "junction adversarial prerequisite unavailable: "
            + (completed.stderr or completed.stdout).strip()
        )


def _run_offline_binding_check(
    baseline: dict[str, bytes], verifier_record: dict[str, object]
) -> dict[str, object]:
    _assert_candidate_not_loaded()
    results: dict[str, object] = {
        "candidate_absent_before_authentication": True,
    }
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary) / "path-swap"
        _write_fixture(root, baseline)
        first = root / "implementation/s0_public_external_pin_recovery/pins.py"
        second = root / "implementation/s0_public_external_pin_recovery/acquisition.py"
        first_bytes, second_bytes = first.read_bytes(), second.read_bytes()
        first.write_bytes(second_bytes)
        second.write_bytes(first_bytes)
        try:
            _authenticate_inputs(root)
        except LiveFailure:
            results["preauth_path_byte_swap_rejected"] = True
        else:
            raise LiveFailure("pre-auth candidate path/byte swap was accepted")
        _assert_candidate_not_loaded()
        results["candidate_absent_after_rejected_swap"] = True

    mutated_record = json.loads(json.dumps(verifier_record))
    mutated_record["host_runtime_prerequisite"]["authority"] = "AUTHENTICATED"
    with tempfile.TemporaryDirectory() as temporary:
        path = Path(temporary) / "forged-prerequisite.json"
        path.write_bytes(_canonical_json_bytes(mutated_record))
        try:
            _read_verifier_record(path)
        except LiveFailure:
            results["forged_runtime_prerequisite_rejected"] = True
        else:
            raise LiveFailure("forged runtime prerequisite schema was accepted")

    finder = _activate_candidate(baseline)
    origins = {
        name: getattr(module, "__file__", None)
        for name, module in sys.modules.items()
        if name == CANDIDATE_PREFIX or name.startswith(CANDIDATE_PREFIX + ".")
    }
    if not origins or any(
        type(origin) is not str or not origin.startswith("<authenticated-memory>/")
        for origin in origins.values()
    ):
        raise LiveFailure("candidate module origin escaped authenticated memory loader")
    if str(IMPLEMENTATION_ROOT) in sys.path:
        raise LiveFailure("mutable repository implementation path entered sys.path")
    results["authenticated_memory_load_no_repo_fallback"] = True
    results["loaded_candidate_modules"] = sorted(origins)
    results["pin_rows_authenticated_after_memory_load"] = bool(_verify_pins())
    if finder not in sys.meta_path:
        raise LiveFailure("candidate memory finder was not retained")

    repository_target = REPOSITORY_ROOT / "s0-v0.2-live-cycle4-must-not-create"
    if repository_target.exists():
        raise LiveFailure("repository-target sentinel path unexpectedly exists")
    try:
        _validate_external_root_path(str(repository_target))
    except LiveFailure:
        results["repository_target_rejected_without_write"] = not repository_target.exists()
    else:
        raise LiveFailure("repository-target external root was accepted")

    with tempfile.TemporaryDirectory() as temporary:
        parent = Path(temporary)
        junction = parent / "s0-v0.2-live-cycle4-junction"
        _create_junction(junction, REPOSITORY_ROOT)
        try:
            try:
                _validate_external_root_path(str(junction))
            except LiveFailure:
                pass
            else:
                raise LiveFailure("preexisting repository-target junction was accepted")
            try:
                win32_secure.secure_create_directory_root(
                    repository_root=REPOSITORY_ROOT, destination=junction
                )
            except Exception as exc:
                if type(exc).__name__ != "AcquisitionError":
                    raise
                results["reparse_junction_repository_target_rejected"] = True
            else:
                raise LiveFailure("secure root creation accepted a preexisting junction")
        finally:
            os.rmdir(junction)

        root_path = parent / "s0-v0.2-live-cycle4-retained-root"
        _validate_external_root_path(str(root_path))
        retained = win32_secure.secure_create_directory_root(
            repository_root=REPOSITORY_ROOT, destination=root_path
        )
        initial_identity = retained.identity
        try:
            retained.create_directory(("acquisitions",))
            retained.revalidate()
            renamed = parent / "renamed-root"
            try:
                os.rename(root_path, renamed)
            except OSError:
                results["retained_root_rename_rejected"] = True
            else:
                raise LiveFailure("retained external root rename unexpectedly succeeded")
            attacker = parent / "attacker-replacement"
            os.mkdir(attacker)
            try:
                os.replace(attacker, root_path)
            except OSError:
                results["retained_root_replacement_rejected"] = True
            else:
                raise LiveFailure("retained external root replacement unexpectedly succeeded")
            replacement_junction = subprocess.run(
                [
                    "cmd.exe",
                    "/d",
                    "/c",
                    "mklink",
                    "/J",
                    str(root_path),
                    str(REPOSITORY_ROOT),
                ],
                text=True,
                capture_output=True,
                timeout=30,
                check=False,
            )
            if replacement_junction.returncode == 0:
                raise LiveFailure("junction replacement at retained root unexpectedly succeeded")
            results["retained_root_reparse_replacement_rejected"] = True
            retained.revalidate()
            offline_evidence = {
                "external_root_identity": _identity_mapping(initial_identity),
                "offline_cycle4": True,
                "retained_handle_relative_evidence_write": True,
            }
            evidence_path, evidence_digest = _write_evidence(
                retained, offline_evidence
            )
            retained.revalidate()
            if retained.identity != initial_identity:
                raise LiveFailure("retained root identity changed during offline evidence write")
            results["handle_relative_evidence_write_sha256"] = evidence_digest
            results["handle_relative_evidence_path"] = str(evidence_path)
            results["retained_root_identity_stable"] = True
        finally:
            retained.close()
        results["fresh_root_preserved_after_close_no_delete"] = root_path.is_dir()
        results["repository_unchanged_by_root_adversary"] = not repository_target.exists()
    return results


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--external-root")
    parser.add_argument("--verification-evidence", required=True)
    parser.add_argument("--offline-binding-check", action="store_true")
    args = parser.parse_args()
    if not (sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode):
        raise LiveFailure("live harness must run with python -I -S -B")
    _assert_candidate_not_loaded()

    verifier_record, verifier_digest = _read_verifier_record(
        Path(args.verification_evidence)
    )
    baseline, pre_hashes = _authenticate_inputs(V02_ROOT)
    live_prerequisite = _live_producer_prerequisite()
    if args.offline_binding_check:
        results = _run_offline_binding_check(baseline, verifier_record)
        _post_values, post_hashes = _authenticate_inputs(V02_ROOT)
        if post_hashes != pre_hashes:
            raise LiveFailure("source/test inputs changed during offline binding check")
        print(
            "OFFLINE_BINDING_RESULT="
            + _canonical_json_bytes(
                {
                    "candidate_binding_claim": (
                        "Authenticated source-byte in-memory load under an unverified "
                        "live-harness/host-runtime prerequisite."
                    ),
                    "live_producer_prerequisite": live_prerequisite,
                    "results": results,
                    "verification_evidence_sha256": verifier_digest,
                }
            ).decode("utf-8")
        )
        return 0
    if args.external_root is None:
        raise LiveFailure("--external-root is required for live acquisition")
    root_path = _validate_external_root_path(args.external_root)
    _activate_candidate(baseline)
    pin_rows = _verify_pins()
    root = win32_secure.secure_create_directory_root(
        repository_root=REPOSITORY_ROOT,
        destination=root_path,
    )
    root_close_registration = atexit.register(root.close)
    root_initial_identity = root.identity
    blockers = list(candidate.CandidateDecision().blocker_ids)
    blockers.extend(
        [
            "CPYTHON-EXPECTED-SIZE-UNPINNED",
            "VS-BUILD-TOOLS-UNAUTHENTICATED-PIN",
            "VS-BUILD-TOOLS-EXPECTED-SIZE-UNPINNED",
            "JSONSCHEMA-SOURCE-UNAVAILABLE",
        ]
    )
    nonclaims = {
        "build_claimed": False,
        "build_validated": False,
        "e0_claimed": False,
        "e0_validated": False,
        "install_claimed": False,
        "install_validated": False,
        "process_authority_granted": False,
        "process_executed": False,
        "rehearsal_claimed": False,
        "rehearsal_validated": False,
        "runtime_claimed": False,
        "runtime_validated": False,
        "s0_claimed": False,
        "s0_validated": False,
    }
    evidence: dict[str, object] = {
        "acquisitions": {},
        "blockers": sorted(set(blockers)),
        "candidate": CANDIDATE_ID,
        "candidate_load_binding": (
            "Authenticated source bytes loaded by in-memory finder with no mutable "
            "repository-path fallback."
        ),
        "external_root": root.destination,
        "external_root_binding": {
            "evidence_writes_handle_relative": True,
            "expected_final_identity": _identity_mapping(root_initial_identity),
            "fresh_exclusive_create": True,
            "initial_identity": _identity_mapping(root_initial_identity),
            "no_path_creation_fallback": True,
            "retained_entire_live_lifecycle": True,
        },
        "input_hashes_pre": pre_hashes,
        "jsonschema_acquired": False,
        "nonclaims": nonclaims,
        "pin_rows": pin_rows,
        "live_producer_prerequisite": live_prerequisite,
        "status": "running",
        "verification_evidence": {"record": verifier_record},
    }
    exit_code = 1
    evidence_path: Path | None = None
    evidence_sha256: str | None = None
    try:
        root.create_directory(("acquisitions",))
        root.revalidate()
        cpython_pin = pins.resolve_approved_pin(pins.CPYTHON_PIN_ID)
        build_tools_pin = pins.resolve_approved_pin(pins.VS_BUILD_TOOLS_PIN_ID)
        if pins.JSONSCHEMA_PIN.url is not None:
            raise LiveFailure("jsonschema source authority unexpectedly became available")

        cpython_evidence, cpython_transport = _download(
            cpython_pin, Path(root.destination) / "acquisitions" / cpython_pin.filename
        )
        root.revalidate()
        if not cpython_evidence.authenticated or cpython_evidence.process_authority:
            raise LiveFailure("CPython acquisition did not remain authenticated and inert")
        evidence["acquisitions"]["cpython"] = {
            "evidence": cpython_evidence.to_mapping(),
            "evidence_sha256": cpython_evidence.evidence_sha256(),
            "transport": cpython_transport,
        }

        materialized = materialize.materialize_authenticated_zip(
            cpython_pin,
            cpython_evidence,
            Path(root.destination) / "materialized-cpython",
            repository_root=REPOSITORY_ROOT,
        )
        root.revalidate()
        if not materialized.final_reauthentication_passed or materialized.process_authority_granted:
            raise LiveFailure("CPython materialization did not remain final-reauthenticated and inert")
        evidence["materialization"] = _materialization_mapping(materialized)

        build_tools_evidence, build_tools_transport = _download(
            build_tools_pin,
            Path(root.destination) / "acquisitions" / build_tools_pin.filename,
        )
        root.revalidate()
        if build_tools_evidence.authenticated or build_tools_evidence.process_authority:
            raise LiveFailure("Build Tools bootstrapper gained unauthoritative trust or process authority")
        evidence["acquisitions"]["build_tools"] = {
            "evidence": build_tools_evidence.to_mapping(),
            "evidence_sha256": build_tools_evidence.evidence_sha256(),
            "transport": build_tools_transport,
        }

        final_files = {
            "cpython_archive": _final_reauthenticate(
                Path(cpython_evidence.destination),
                expected_size=cpython_evidence.observed_size,
                expected_sha256=cpython_evidence.observed_sha256,
                expected_identity=_checkpoint_identity(cpython_evidence),
            ),
            "build_tools_bootstrapper": _final_reauthenticate(
                Path(build_tools_evidence.destination),
                expected_size=build_tools_evidence.observed_size,
                expected_sha256=build_tools_evidence.observed_sha256,
                expected_identity=_checkpoint_identity(build_tools_evidence),
            ),
        }
        final_files["materialized_outputs"] = [
            _final_reauthenticate(
                Path(materialized.destination_path) / Path(*item.relative_path.split("/")),
                expected_size=item.size,
                expected_sha256=item.sha256,
            )
            for item in materialized.files
        ]
        evidence["final_reauthentication"] = final_files
        root.revalidate()
        evidence["status"] = "completed-blocked-nonexecuting"
        exit_code = 0
    except Exception as exc:
        evidence["status"] = "failed-closed"
        evidence["live_failure"] = f"{type(exc).__name__}: {exc}"
        evidence["blockers"] = sorted(set([*evidence["blockers"], "LIVE-ACQUISITION-OR-MATERIALIZATION-FAILURE"]))

    _post_values, post_hashes = _authenticate_inputs(V02_ROOT)
    if post_hashes != pre_hashes:
        raise LiveFailure("source/test inputs changed during live operation")
    verifier_record_post, verifier_digest_post = _read_verifier_record(
        Path(args.verification_evidence)
    )
    if verifier_digest_post != verifier_digest or verifier_record_post != verifier_record:
        raise LiveFailure("canonical verifier evidence changed during live operation")
    evidence["input_hashes_post"] = post_hashes
    evidence["verification_evidence"].update(
        {
            "measurement": (
                "Exact canonical verifier-record bytes from the supplied path were "
                "handle-bound, parsed, and hashed before candidate activation, then "
                "reread, reparsed, and rehashed after live operations and immediately "
                "before evidence creation."
            ),
            "pre_post_digest_equal": True,
            "pre_post_record_equal": True,
            "post_sha256": verifier_digest_post,
            "pre_sha256": verifier_digest,
        }
    )
    root.revalidate()
    if root.identity != root_initial_identity:
        raise LiveFailure("external root identity changed before evidence creation")
    evidence_path, evidence_sha256 = _write_evidence(root, evidence)
    root.revalidate()
    if root.identity != root_initial_identity:
        raise LiveFailure("external root identity changed after evidence creation")
    root.close()
    atexit.unregister(root_close_registration)
    if evidence_path is None or evidence_sha256 is None:
        raise LiveFailure("live evidence was not created")
    print("EXTERNAL_ROOT=" + str(root_path))
    print("EVIDENCE_PATH=" + str(evidence_path))
    print("EVIDENCE_SHA256=" + evidence_sha256)
    print("LIVE_STATUS=" + str(evidence["status"]))
    return exit_code


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except LiveFailure as exc:
        print(f"LIVE_FAILED={exc}", file=sys.stderr)
        raise SystemExit(1)

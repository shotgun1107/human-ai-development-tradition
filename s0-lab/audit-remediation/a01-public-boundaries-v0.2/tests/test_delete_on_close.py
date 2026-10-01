"""Bounded, disposable-file Windows delete-on-close discriminator and regression."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sys

CANDIDATE = Path(__file__).resolve().parents[1]
REPOSITORY = CANDIDATE.parents[2]
OLD = REPOSITORY / "s0-lab/audit-remediation/a01-public-boundaries-v0.1"
PYTHON = Path("C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe")
MANIFEST_PIN = "d583db794052e751a03200bee65a278fa06c2dc943011482e58d9c34f48e654a"
AGENTS_PIN = "4aac0c255dea03b85f6fb98b0b89f5b3c3f348e42c4dcaaf423411b818e3a065"
BENIGN = b"Disposable A01 Windows delete-on-close diagnostic.\n"
SOURCE_NAMES = frozenset({
    "implementation/s0_public_assembly_candidate/__init__.py",
    "implementation/s0_public_assembly_candidate/constants.py",
    "implementation/s0_public_assembly_candidate/errors.py",
    "implementation/s0_public_assembly_candidate/runtime_guard.py",
    "implementation/s0_public_assembly_candidate/storage.py",
    "implementation/s0_public_assembly_verifier/__init__.py",
    "implementation/s0_public_assembly_verifier/errors.py",
    "implementation/s0_public_assembly_verifier/models.py",
    "implementation/s0_public_assembly_verifier/win32.py",
})


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def authenticate_old():
    assert digest(REPOSITORY / "AGENTS.md") == AGENTS_PIN
    manifest = OLD / "artifact-files.sha256"
    assert digest(manifest) == MANIFEST_PIN
    pins = {name: pin for pin, name in
            (line.split("  ", 1) for line in manifest.read_text(encoding="utf-8").splitlines())
            if name in SOURCE_NAMES}
    assert set(pins) == SOURCE_NAMES
    observed = {name: digest(OLD / name) for name in pins}
    assert observed == pins
    return observed


def checked_owned(path):
    root = CANDIDATE / "verification/tmp"
    assert path.is_absolute()
    path.relative_to(root)
    for current in (path, *path.parents):
        if current.exists():
            assert not (getattr(current.lstat(), "st_file_attributes", 0) & 0x400)
    return path


def child_main():
    variant, action, scratch_text = sys.argv[2:]
    authenticate_old()
    implementation = (OLD if variant == "old" else CANDIDATE) / "implementation"
    sys.path.insert(0, str(implementation))
    from s0_public_assembly_candidate import runtime_guard as guard
    scratch = checked_owned(Path(scratch_text))
    approved = scratch / "approved.txt"
    pending = scratch / "output/run-record.pending"
    forbidden = scratch / "forbidden.txt"
    path = forbidden if action == "temporary_forbidden" else pending if action == "temporary_pending" else approved
    flags = os.O_RDONLY | (os.O_TEMPORARY if action.startswith("temporary") else 0)
    imports = {name: str(Path(module.__file__).resolve()) for name, module in sys.modules.items()
               if name.startswith("s0_public_assembly_candidate")}
    for name, actual in imports.items():
        relative = name.replace(".", "/") + ("/__init__.py" if "." not in name else ".py")
        assert Path(actual) == (implementation / relative).resolve()
    events = []
    def observe(event, args):
        if event == "open":
            events.append([str(args[0]), args[1], args[2]])
    sys.addaudithook(observe)
    guard.install_runtime_sentinels(workspace_root=scratch, output_root=scratch / "output",
                                   allowed_public_files=frozenset({approved}), bundle_root=scratch)
    result = {"variant": variant, "action": action, "path": str(path), "flags": flags,
              "O_TEMPORARY": os.O_TEMPORARY, "imports": imports}
    try:
        fd = os.open(path, flags)
        try:
            raw = os.read(fd, 4096)
        finally:
            os.close(fd)
        assert raw == BENIGN
        guard.require_runtime_sentinels_healthy()
        result.update(status="allowed", read_sha256=hashlib.sha256(raw).hexdigest())
    except guard.BoundaryViolation as exc:
        result.update(status="denied", diagnostic=str(exc))
        try:
            guard.require_runtime_sentinels_healthy()
        except guard.BoundaryViolation:
            result["latched"] = True
        else:
            raise AssertionError("denial did not latch")
    except OSError as exc:
        result.update(status="native_error", errno=exc.errno, winerror=getattr(exc, "winerror", None))
    result["audit_open_events"] = events
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__" and len(sys.argv) > 1 and sys.argv[1] == "--child":
    child_main()
    raise SystemExit(0)

import subprocess
import tempfile
import time


def run_case(action, variant="old"):
    root = CANDIDATE / "verification/tmp"
    checked_owned(root)
    root.mkdir(parents=True, exist_ok=True)
    scratch = checked_owned(Path(tempfile.mkdtemp(prefix="delete-on-close-", dir=root)))
    output = checked_owned(scratch / "output")
    output.mkdir()
    paths = [scratch / "approved.txt", scratch / "forbidden.txt", output / "run-record.pending"]
    try:
        for path in paths:
            checked_owned(path).write_bytes(BENIGN)
        before = {str(path): {"exists": True, "hex": path.read_bytes().hex(), "sha256": digest(path)} for path in paths}
        command = [str(PYTHON), "-I", "-S", "-B", str(Path(__file__).resolve()), "--child", variant, action, str(scratch)]
        child = subprocess.run(command, capture_output=True, text=True, timeout=15)
        assert child.returncode == 0, child.stderr
        assert child.stderr == ""
        value = json.loads(child.stdout)
        after = {str(path): {"exists": path.exists(), "hex": path.read_bytes().hex() if path.exists() else None,
                             "sha256": digest(path) if path.exists() else None} for path in paths}
        return {"command": command, "child": value, "before": before, "after": after}
    finally:
        for path in paths:
            checked_owned(path)
            if path.exists():
                path.unlink()
        checked_owned(output).rmdir()
        checked_owned(scratch).rmdir()


def run_diagnostic():
    started = time.monotonic()
    assert os.name == "nt" and hasattr(os, "O_TEMPORARY")
    assert Path(sys.executable).resolve() == PYTHON.resolve()
    assert sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode
    before = authenticate_old()
    cases = [run_case(action) for action in ("ordinary_approved", "temporary_approved", "temporary_pending", "temporary_forbidden")]
    for case in cases:
        status = case["child"]["status"]
        target = case["child"]["path"]
        action = case["child"]["action"]
        expected_status = "denied" if action == "temporary_forbidden" else "allowed"
        assert status == expected_status, (action, status)
        expected_exists = action in {"ordinary_approved", "temporary_forbidden"}
        assert case["after"][target]["exists"] == expected_exists
        for path, state in case["after"].items():
            if state["exists"]:
                assert state == case["before"][path]
    after = authenticate_old()
    text = "\n".join(f"{case['child']['action']}: {case['child']['status']}; target_exists_after={case['after'][case['child']['path']]['exists']}" for case in cases) + "\n"
    stdout = CANDIDATE / "verification/diagnostic-stdout.txt"
    stdout.write_text(text, encoding="utf-8", newline="\n")
    record = {"role": "TEST/VERIFICATION", "candidate": "a01-public-boundaries-v0.2",
              "subject": "Frozen v0.1 discriminator before CODE", "result": "DEFECT-REPRODUCED",
              "interpreter": {"executable": sys.executable, "version": sys.version, "os_name": os.name,
                              "isolated": sys.flags.isolated, "no_site": sys.flags.no_site,
                              "dont_write_bytecode": sys.dont_write_bytecode, "O_TEMPORARY": os.O_TEMPORARY},
              "command": [str(PYTHON), "-I", "-S", "-B", str(Path(__file__).resolve()), "--diagnostic"],
              "before": before, "after": after, "cases": cases, "test_sha256": digest(Path(__file__)),
              "stdout_sha256": digest(stdout), "elapsed_seconds": round(time.monotonic()-started, 3),
              "scratch_remaining_count": sum(1 for _ in (CANDIDATE / "verification/tmp").iterdir()),
              "limits": ["Disposable newly created benign files only", "Host runtime, stdlib, native closure and evidence producer trusted",
                         "No hostile concurrency, ACL/root/reparse replacement or TOCTOU security claim", "No native publication, S0/E0, model or provider execution"]}
    (CANDIDATE / "verification/delete-on-close-diagnostic.json").write_text(json.dumps(record, indent=2, sort_keys=True)+"\n", encoding="utf-8", newline="\n")
    print(text, end="")
    print(record["result"])


if __name__ == "__main__":
    assert sys.argv[1:] == ["--diagnostic"]
    run_diagnostic()

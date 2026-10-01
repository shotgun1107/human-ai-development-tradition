"""One offline verification of the three authenticated A04 public CLI commands.

Run from the repository root with the pinned base Python and -I -S -B -X utf8.
The two result files are created exclusively; an existing result is never replaced.
This checks ordinary public CLI readiness, not S0 or project-native execution.
"""

from __future__ import annotations

import ast
import copy
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import time
from datetime import datetime, timezone
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parents[4]
A4 = ROOT / "s0-lab/audit-remediation/a04-i0-cli-authentication-v0.1"
A7 = ROOT / "s0-lab/audit-remediation/a07-public-cli-readiness-v0.1"
SOURCE = A4 / "implementation/s0_i0"
BUNDLE = ROOT / "s0-lab/public-practice/v0.1"
ENV = ROOT / ".venv-public"
BASE = Path("C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe")
PYTHON = ENV / "Scripts/python.exe"
RESULT = A7 / "verification/test-results.json"
TRANSCRIPT = A7 / "verification/test-stdout.txt"
BRANCH = "codex/windows-build-toolchain-environment-v0.1"
HEAD = "cc76d7e82aeb51dfdc7baba3da0f7993ab2da61a"
TREE = "82c02f37fd13ecfc8c7b888bb66127989b6d4f34"
SOURCE_NAMES = {
    "__init__.py", "answer_validation.py", "authentication.py", "cli.py",
    "error_reporting.py", "integrity.py", "json_validation.py", "paths.py",
    "schema_suite.py", "transform.py", "verification.py",
}
PINS = {
    ROOT / "AGENTS.md": "393984b6d83639d0c4365d0ca6066907d3d281384656b860a4853d3d6d46ac9e",
    ROOT / ".gitignore": "93b0ba1fee168778488b7839f3094b9f2c137399aafea117a3dc417a6ddd718a",
    A7 / "requirements.lock.txt": "58a76393ebeb1d098c09bd74713704673d4b2c768162bb903145e7d2acbd9c71",
    PYTHON: "0b471133e110cfb53a061cad528ce8e517d7b9ac41a0a396c39ad795a487fc14",
    ENV / "pyvenv.cfg": "6d7ac85012ab1132ed60a62b8ead1d23b2a29f658e90b443babbe9e6464feb68",
    ENV / "install-report.json": "3df056b8d8c3ba50349cd3b8fe8d379f60280af55e6c408153a930607458767c",
    BASE: "4d6f5f81a4bca11191c4c7c6b43632694d0a4ce74e068619d8fdc161d469859a",
    A4 / "artifact-files.sha256": "3188bfb5d5745b83a0f07f8134e2021d63285c8591db1698eca02e6086fc3f68",
    A4 / "requirements.txt": "d0bc9baee84543883a0a966d477620161876536b552742ab6409d1da50251405",
    BUNDLE / "bundle-files.sha256": "e41ee6c71169df646e3c8c0b0e8f3d77e7871d939f651b86a52ea5696feeb637",
}
TAG = "A07_OBSERVATION="
CHECKS: list[dict] = []
COMMANDS: list[dict] = []

# The child adds only the authenticated A04 implementation directory, calls the
# real main() once, then reports observations on stderr. No handler is replaced.
# -I retains the venv's site-packages; -B prevents project/package pycache writes.
CHILD = r'''
import importlib.metadata as metadata
import json
from pathlib import Path
import platform
import sys
root = Path(sys.argv[1])
implementation = root / "s0-lab/audit-remediation/a04-i0-cli-authentication-v0.1/implementation"
env = root / ".venv-public"
sys.path.insert(0, str(implementation))
import s0_i0.cli as cli
import jsonschema
rc = cli.main([sys.argv[2]])
project_modules = {}
unexpected_repo_module_count = 0
dependency_modules = {}
for name, module in tuple(sys.modules.items()):
    raw = getattr(module, "__file__", None)
    if not raw:
        continue
    path = Path(raw).resolve()
    if path.is_relative_to(implementation):
        project_modules[name] = {
            "file": str(path),
            "spec_origin": getattr(getattr(module, "__spec__", None), "origin", None),
        }
    elif path.is_relative_to(env):
        dependency_modules[name] = str(path)
    elif path.is_relative_to(root):
        unexpected_repo_module_count += 1
distributions = []
for dist in metadata.distributions(path=[str(env / "Lib/site-packages")]):
    distributions.append({
        "name": dist.metadata["Name"], "version": dist.version,
        "location": str(Path(dist.locate_file("")).resolve()),
        "requires": dist.requires or [],
    })
observation = {
    "python": platform.python_version(), "executable": sys.executable,
    "prefix": sys.prefix, "base_prefix": sys.base_prefix,
    "flags": {"isolated": sys.flags.isolated, "utf8_mode": sys.flags.utf8_mode,
              "dont_write_bytecode": sys.dont_write_bytecode},
    "sys_path": sys.path, "project_modules": project_modules,
    "unexpected_repo_module_count": unexpected_repo_module_count,
    "dependency_modules": dependency_modules,
    "jsonschema_version": metadata.version("jsonschema"),
    "jsonschema_file": str(Path(jsonschema.__file__).resolve()) if Path(jsonschema.__file__).resolve().is_relative_to(env) else "OUTSIDE_APPROVED_ENV",
    "distributions": sorted(distributions, key=lambda row: row["name"].lower()),
    "cli_main_return": rc,
}
print("A07_OBSERVATION=" + json.dumps(observation, sort_keys=True), file=sys.stderr)
raise SystemExit(rc)
'''


def check(name: str, condition: bool, **detail: object) -> None:
    CHECKS.append({"name": name, "status": "pass" if condition else "fail", **detail})
    if not condition:
        raise AssertionError(name)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def path_key(path: Path) -> str:
    return path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path)


def reparse_chain(path: Path) -> int:
    return sum(bool(p.lstat().st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT)
               for p in (path, *path.parents) if p.exists())


def manifest(path: Path) -> dict[str, str]:
    rows = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"([0-9a-f]{64})  ([^\r\n]+)", line)
        if not match:
            raise AssertionError("manifest syntax")
        sha, relative = match.groups()
        pure = PurePosixPath(relative)
        if (pure.is_absolute() or ".." in pure.parts or "\\" in relative
                or ":" in relative or relative in rows):
            raise AssertionError("manifest path contract")
        rows[relative] = sha
    return rows


def inventory(root: Path, expected_files: set[str]) -> dict:
    # Enumerate only these approved roots. Unexpected names remain internal;
    # do not follow reparse entries or enumerate an unexpected directory.
    expected_dirs = {str(parent) for name in expected_files
                     for parent in PurePosixPath(name).parents if str(parent) != "."}
    files, dirs = set(), set()
    extras = reparses = 0
    pending = [root]
    while pending:
        current = pending.pop()
        for entry in os.scandir(current):
            info = entry.stat(follow_symlinks=False)
            rel = Path(entry.path).relative_to(root).as_posix()
            if info.st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT:
                reparses += 1
            elif entry.is_dir(follow_symlinks=False):
                if rel in expected_dirs:
                    dirs.add(rel)
                    pending.append(Path(entry.path))
                else:
                    extras += 1
            elif rel in expected_files:
                files.add(rel)
            else:
                extras += 1
    return {"files": len(files), "directories": len(dirs), "extra_entries": extras,
            "missing_files": len(expected_files - files), "reparse_entries": reparses,
            "root_chain_reparse_entries": reparse_chain(root)}


def authenticate(pins: dict[Path, str], phase: str) -> dict:
    observations = {}
    for path, expected in pins.items():
        check(phase + ": path has no observed reparse components: " + path_key(path),
              reparse_chain(path) == 0)
        actual = digest(path)
        check(phase + ": SHA256: " + path_key(path), actual == expected)
        info = path.stat()
        observations[path_key(path)] = {"sha256": actual, "bytes": info.st_size}
    return observations


def run(name: str, argv: list[str], timeout: int = 45, git: bool = False) -> dict:
    started = time.monotonic()
    try:
        proc = subprocess.run(argv, cwd=ROOT, capture_output=True, text=True,
                              encoding="utf-8", errors="strict", timeout=timeout)
        row = {"name": name, "argv": argv, "cwd": str(ROOT), "timeout_seconds": timeout,
               "exit_code": proc.returncode, "stdout": proc.stdout,
               "stderr": "suppressed at Git boundary" if git and proc.stderr else proc.stderr,
               "timed_out": False}
    except subprocess.TimeoutExpired as exc:
        row = {"name": name, "argv": argv, "cwd": str(ROOT), "timeout_seconds": timeout,
               "exit_code": None, "stdout": (exc.stdout or b"").decode("utf-8", "replace"),
               "stderr": "suppressed at Git boundary" if git else (exc.stderr or b"").decode("utf-8", "replace"),
               "timed_out": True}
    row["elapsed_seconds"] = round(time.monotonic() - started, 6)
    COMMANDS.append(row)
    check(name + ": successful exit", row["exit_code"] == 0 and not row["timed_out"],
          exit_code=row["exit_code"])
    return row


def norm(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def receipt_matches(lock: dict, receipt: dict) -> bool:
    rows = receipt["install"]
    if len(rows) != len(lock) or {norm(r["metadata"]["name"]) for r in rows} != set(lock):
        return False
    for row in rows:
        expected = lock[norm(row["metadata"]["name"])]
        url = urlsplit(row["download_info"]["url"])
        if (row["metadata"]["version"] != expected["version"]
                or row["download_info"]["archive_info"]["hashes"]["sha256"] != expected["sha256"]
                or url.scheme != "https" or url.hostname != "files.pythonhosted.org"
                or not url.path.endswith(".whl") or url.username or url.password):
            return False
    return True


def main() -> int:
    if RESULT.exists() or TRANSCRIPT.exists():
        print("Refusing to overwrite existing verification outputs.")
        return 2
    RESULT.parent.mkdir(parents=True, exist_ok=True)
    result = {
        "candidate": "a07-public-cli-readiness-v0.1", "role": "TEST/VERIFICATION",
        "started_at": datetime.now(timezone.utc).isoformat(),
        "producer_argv": [str(BASE), "-I", "-S", "-B", "-X", "utf8", str(Path(__file__).resolve())],
        "producer_sha256": digest(Path(__file__)), "producer_cwd": str(Path.cwd()),
        "checks": CHECKS, "commands": COMMANDS, "status": "fail",
        "wrapper": "Fresh venv child: prepend exact A04 implementation, import real cli, call main once, tagged stderr observations after main; CLI stdout remains unmodified.",
        "network": "No network command requested; pip check and the three local CLI commands only. No OS-enforced network isolation claim.",
        "nonclaims": [
            "No S0/E0 run, oracle, scoring, provider/model call or new fixture.",
            "No historical 36-test rerun, project-native preloader or Win32 runtime rehearsal.",
            "No central system, Project Brain, operational safety, economic value or model-transfer validation.",
            "Receipt and installed metadata are trusted setup evidence, not independent supply-chain or publisher-signature proof.",
            "Interpreter/stdlib/native import closure, ACL/volume authority, hostile concurrency, retained handles, rename/rebinding and TOCTOU defenses remain unverified.",
            "Ordinary venv dependency execution includes rpds; it is not project-native runtime validation.",
            "Output producer and local path observations are not a secure attestation or enforced role isolation.",
        ],
    }
    all_pins = dict(PINS)
    try:
        check("parent cwd and pinned interpreter", Path.cwd() == ROOT and Path(sys.executable) == BASE)
        check("parent flags", bool(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.utf8_mode))
        authenticate(PINS, "initial")
        for name, args, expected in (
            ("branch", ["branch", "--show-current"], BRANCH),
            ("HEAD", ["rev-parse", "HEAD"], HEAD),
            ("tree", ["rev-parse", "HEAD^{tree}"], TREE),
        ):
            row = run("git " + name, ["git", *args], git=True)
            check("frozen " + name, row["stdout"].strip() == expected)
        head_ignore = run("git original ignore", ["git", "show", "HEAD:.gitignore"], git=True)["stdout"]
        check("only appended local environment ignore entry",
              (ROOT / ".gitignore").read_text(encoding="utf-8") == head_ignore + ".venv-public/\n")
        ignored = run("git environment ignored", ["git", "check-ignore", "--", ".venv-public/pyvenv.cfg"], git=True)
        check("exact ignored public environment path", ignored["stdout"].strip() == ".venv-public/pyvenv.cfg")

        a4_manifest = manifest(A4 / "artifact-files.sha256")
        source_pins = {A4 / name: sha for name, sha in a4_manifest.items()
                       if name.startswith("implementation/s0_i0/")}
        check("exact eleven source entries", {p.name for p in source_pins} == SOURCE_NAMES and len(source_pins) == 11)
        authenticate(source_pins, "source-admission")
        parsed = ast.parse((SOURCE / "schema_suite.py").read_text(encoding="utf-8"))
        schemas = next(ast.literal_eval(n.value) for n in parsed.body if isinstance(n, ast.Assign)
                       and any(isinstance(t, ast.Name) and t.id == "FROZEN_SCHEMA_HASHES" for t in n.targets))
        check("eleven frozen schema entries", len(schemas) == 11)
        schema_pins = {ROOT / "s0-lab/control" / rel: sha for rel, sha in schemas.items()}
        public = manifest(BUNDLE / "bundle-files.sha256")
        check("ninety bundle entries", len(public) == 90)
        all_pins.update(source_pins)
        all_pins.update(schema_pins)
        all_pins.update({BUNDLE / rel: sha for rel, sha in public.items()})
        expected_bundle = set(public) | {"bundle-files.sha256"}
        result["inventory_before"] = {
            "source": inventory(SOURCE, SOURCE_NAMES), "public_bundle": inventory(BUNDLE, expected_bundle)}
        for name, observed in result["inventory_before"].items():
            check("preflight exact " + name + " inventory", all(observed[key] == 0 for key in
                  ("extra_entries", "missing_files", "reparse_entries", "root_chain_reparse_entries")), **observed)
        result["inputs_before"] = authenticate(all_pins, "pre-execution")
        result["path_observations"] = {}
        for name, path in (("workspace", ROOT), ("environment", ENV), ("source", SOURCE),
                           ("public_bundle", BUNDLE), ("output_parent", RESULT.parent)):
            info = path.stat()
            check("no observed reparse chain: " + name, reparse_chain(path) == 0)
            result["path_observations"][name] = {"path": str(path), "device": info.st_dev,
                                                "inode": info.st_ino, "attributes": info.st_file_attributes}
        refs = []
        def collect_refs(value: object) -> None:
            if isinstance(value, dict):
                refs.extend(v for k, v in value.items() if k in ("$ref", "$dynamicRef") and isinstance(v, str) and not v.startswith("#"))
                for child in value.values():
                    collect_refs(child)
            elif isinstance(value, list):
                for child in value:
                    collect_refs(child)
        for path in schema_pins:
            collect_refs(json.loads(path.read_bytes()))
        check("schemas need no external reference retrieval", len(refs) == 0, external_reference_count=len(refs))

        lock = {}
        for line in (A7 / "requirements.lock.txt").read_text(encoding="utf-8").splitlines():
            match = re.fullmatch(r"([A-Za-z0-9_.-]+)(\[format\])?==([^ ]+) --hash=sha256:([a-f0-9]{64})", line)
            check("lock row syntax", match is not None)
            name, extra, version, sha = match.groups()
            check("unique normalized lock name", norm(name) not in lock)
            lock[norm(name)] = {"version": version, "sha256": sha, "extra": extra}
        check("eighteen exact locked packages and format extra", len(lock) == 18 and lock["jsonschema"]["extra"] == "[format]")
        check("original top-level requirement preserved", (A4 / "requirements.txt").read_text().strip() == "jsonschema[format]==4.26.0")
        receipt = json.loads((ENV / "install-report.json").read_bytes())
        check("installer receipt matches all locked wheel hashes versions and HTTPS host", receipt_matches(lock, receipt))
        check("receipt requested jsonschema format", next(r for r in receipt["install"] if norm(r["metadata"]["name"]) == "jsonschema")["requested_extras"] == ["format"])
        result["locked_packages"] = lock
        result["install_receipt_rows"] = [{"name": r["metadata"]["name"], "version": r["metadata"]["version"],
                                           "url": r["download_info"]["url"], "hashes": r["download_info"]["archive_info"]["hashes"]}
                                          for r in receipt["install"]]
        for field in ("sha256", "version"):
            changed = copy.deepcopy(lock)
            changed["jsonschema"][field] = "0" * 64 if field == "sha256" else "0.0.0"
            check("in-memory mismatched " + field + " rejected", not receipt_matches(changed, receipt))
        pip = run("pip check", [str(PYTHON), "-I", "-B", "-X", "utf8", "-m", "pip", "--isolated", "check"])
        check("pip dependency consistency", pip["stdout"].strip() == "No broken requirements found." and pip["stderr"] == "")

        expected_modules = {"s0_i0" if name == "__init__.py" else "s0_i0." + name[:-3]: SOURCE / name for name in SOURCE_NAMES}
        expected_versions = {name: row["version"] for name, row in lock.items()} | {"pip": receipt["pip_version"]}
        result["cli"] = {}
        for command in ("integrity", "schema-check", "verify"):
            row = run("CLI " + command, [str(PYTHON), "-I", "-B", "-X", "utf8", "-c", CHILD, str(ROOT), command])
            payload = json.loads(row["stdout"])
            lines = row["stderr"].splitlines()
            check(command + ": sole stderr observation", len(lines) == 1 and lines[0].startswith(TAG))
            observed = json.loads(lines[0][len(TAG):])
            result["cli"][command] = {"result": payload, "observation": observed}
            check(command + ": Python and venv identities", observed["python"] == "3.12.10" and Path(observed["executable"]) == PYTHON
                  and Path(observed["prefix"]) == ENV and Path(observed["base_prefix"]) == BASE.parent)
            check(command + ": isolated no-bytecode UTF8 flags", observed["flags"] == {"isolated": 1, "utf8_mode": 1, "dont_write_bytecode": True})
            check(command + ": exact real A04 module origins", set(observed["project_modules"]) == set(expected_modules)
                  and all(Path(v["file"]) == expected_modules[k] and Path(v["spec_origin"]) == expected_modules[k]
                          for k, v in observed["project_modules"].items()) and observed["unexpected_repo_module_count"] == 0)
            check(command + ": real env jsonschema", observed["jsonschema_version"] == "4.26.0"
                  and Path(observed["jsonschema_file"]) == ENV / "Lib/site-packages/jsonschema/__init__.py")
            installed = {norm(d["name"]): d["version"] for d in observed["distributions"]}
            check(command + ": exact installed distribution versions", installed == expected_versions and len(observed["distributions"]) == 19
                  and all(Path(d["location"]) == ENV / "Lib/site-packages" for d in observed["distributions"]), distribution_count=len(installed))
            check(command + ": handler returned zero", observed["cli_main_return"] == 0)
            if command == "integrity":
                check("integrity: ninety entries and eight existing packages", payload["manifest_entries"] == 90 and len(payload["packages"]) == 8)
            else:
                schema_result = payload if command == "schema-check" else payload["schema_summary"]
                impact = payload["broader_upstream_impact"]
                check(command + ": eleven schema checks zero errors", schema_result["schema_count"] == 11 and schema_result["error_count"] == 0
                      and len(schema_result["results"]) == 11 and all(not r["errors"] for r in schema_result["results"]))
                check(command + ": broader impact zero errors", all(impact[k] == 0 for k in ("related_error_count", "designated_error_count", "additional_error_count")))
            if command == "verify":
                check("verify: public-only pass record", payload["status"] == "pass" and payload["not_an_s0_run"] is True
                      and payload["record_kind"] == "i0-public-technical-verification" and payload["errors"] == [])
                packages = {"s0-lab/public-practice/v0.1/" + rel: sha for rel, sha in public.items() if re.fullmatch(r"packages/[^/]+/input\.json", rel)}
                outputs = {o["path"]: o for o in payload["outputs"]}
                check("verify: eight in-memory generated packages match pinned bytes", len(outputs) == 8 and set(outputs) == set(packages)
                      and all(o["sha256"] == packages[name] and o["bytes"] == (ROOT / name).stat().st_size for name, o in outputs.items()))
                check("verify: runtime versions", payload["runtime"] == {"python": "3.12.10", "jsonschema": "4.26.0"})
        result["status"] = "pass"
    except Exception as exc:
        result["failure"] = {"type": type(exc).__name__, "message": str(exc) if isinstance(exc, AssertionError) else "Verification error; no potentially unclassified path details emitted."}
    finally:
        try:
            result["inputs_after"] = authenticate(all_pins, "post-execution")
            if "inputs_before" in result:
                check("all admitted input hashes and sizes unchanged", result["inputs_after"] == result["inputs_before"], authenticated_input_count=len(all_pins))
            if "inventory_before" in result:
                result["inventory_after"] = {"source": inventory(SOURCE, SOURCE_NAMES), "public_bundle": inventory(BUNDLE, expected_bundle)}
                check("source and public inventories unchanged; no fixture or pycache added", result["inventory_after"] == result["inventory_before"])
        except Exception as exc:
            result["status"] = "fail"
            result["postcheck_failure"] = {"type": type(exc).__name__, "message": str(exc) if isinstance(exc, AssertionError) else "Postcheck error; path details withheld."}
        result["ended_at"] = datetime.now(timezone.utc).isoformat()
        result["check_count"] = len(CHECKS)
        result["failed_check_count"] = sum(row["status"] == "fail" for row in CHECKS)
        result["producer_exit_code"] = 0 if result["status"] == "pass" else 1
        with RESULT.open("x", encoding="utf-8", newline="\n") as handle:
            json.dump(result, handle, ensure_ascii=False, sort_keys=True, indent=2)
            handle.write("\n")
        with TRANSCRIPT.open("x", encoding="utf-8", newline="\n") as handle:
            for row in COMMANDS:
                handle.write(json.dumps({k: v for k, v in row.items() if k not in {"stdout", "stderr"}}, sort_keys=True) + "\n")
                handle.write("STDOUT\n" + row["stdout"] + "STDERR\n" + row["stderr"] + "\n")
            handle.write(json.dumps({"status": result["status"], "checks": len(CHECKS), "failed": result["failed_check_count"], "producer_exit_code": result["producer_exit_code"]}) + "\n")
        print(json.dumps({"status": result["status"], "checks": len(CHECKS), "failed": result["failed_check_count"], "results": str(RESULT), "transcript": str(TRANSCRIPT)}))
    return result["producer_exit_code"]


if __name__ == "__main__":
    raise SystemExit(main())

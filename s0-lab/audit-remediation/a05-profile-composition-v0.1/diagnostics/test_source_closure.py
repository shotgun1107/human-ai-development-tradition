"""Read-only source-closure diagnostic; originals are parsed as data only."""

import ast
import hashlib
import json
from pathlib import Path
import sys
from types import ModuleType


ROOT = Path("C:/Users/SSAFY/Documents/ai-development-tradition")
CANDIDATE_REL = "s0-lab/audit-remediation/a05-profile-composition-v0.1"
CANDIDATE = ROOT / CANDIDATE_REL
ORIGINAL = ROOT / "docs/maintenance/audit-2026-09-09/f03-source-recovery-2026-09-16/implementation/s0_public_runtime_preloader"
SOURCE_REL = "implementation/s0_public_runtime_preloader"
NAMES = (
    "__init__.py", "canonical.py", "errors.py", "evidence.py",
    "integration.py", "preloader.py", "profile.py", "schema.py",
    "semantic.py", "source_audit.py",
)
EXPECTED_MANIFEST = "b2505ce58732de16185f434f9e4ece1c8c2345aba80bc165f3a2df43cc217802"
EXPECTED_AGENTS = "393984b6d83639d0c4365d0ca6066907d3d281384656b860a4853d3d6d46ac9e"
EXPECTED_PYTHON = "4d6f5f81a4bca11191c4c7c6b43632694d0a4ce74e068619d8fdc161d469859a"
ORIGINAL_OVERRIDES = {
    "profile.py": "c5c1f6c6c937e45b9da246b24783134570a48923501757ab4683173a5367fe89",
    "preloader.py": "b6f343c7a0a0c3ebe075eed386ff53d08abda507116ca19d1e7b7985aabd1c59",
}


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def authenticated_read(path, expected):
    raw = path.read_bytes()
    if digest(raw) != expected:
        raise AssertionError("pinned input mismatch: " + str(path))
    return raw


def snapshot(pins):
    return {
        str(path): digest(authenticated_read(path, expected))
        for path, expected in pins.items()
    }


def import_set(raw):
    imports = set()
    for node in ast.walk(ast.parse(raw.decode("utf-8", errors="strict"))):
        if isinstance(node, ast.Import):
            imports.update(("import", 0, "", alias.name, alias.asname) for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.update(
                ("from", node.level, node.module or "", alias.name, alias.asname)
                for alias in node.names
            )
    return imports


def main():
    if sys.version_info[:3] != (3, 12, 10):
        raise AssertionError("interpreter version mismatch")
    if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode and sys.flags.utf8_mode):
        raise AssertionError("required isolated interpreter flags absent")
    result_path = CANDIDATE / "diagnostics/source-closure-results.json"
    stdout_path = CANDIDATE / "diagnostics/source-closure-stdout.txt"
    if result_path.exists() or stdout_path.exists():
        raise AssertionError("diagnostic outputs already exist; no overwrite permitted")
    manifest_path = CANDIDATE / "candidate-files.sha256"
    manifest_raw = authenticated_read(manifest_path, EXPECTED_MANIFEST)
    entries = {}
    for line in manifest_raw.decode("utf-8", errors="strict").splitlines():
        if not line:
            continue
        expected, relative = line.split("  ", 1)
        if len(expected) != 64 or any(c not in "0123456789abcdef" for c in expected):
            raise AssertionError("invalid digest in pinned manifest")
        if not relative.startswith(CANDIDATE_REL + "/") or ".." in Path(relative).parts:
            raise AssertionError("manifest target outside frozen candidate")
        if relative in entries:
            raise AssertionError("duplicate manifest entry")
        entries[relative] = expected
    if len(entries) != 17:
        raise AssertionError("frozen manifest entry count mismatch")
    pins = {ROOT / relative: expected for relative, expected in entries.items()}
    pins.update({
        manifest_path: EXPECTED_MANIFEST,
        ROOT / "AGENTS.md": EXPECTED_AGENTS,
        Path(sys.executable): EXPECTED_PYTHON,
    })
    for name in NAMES:
        relative = CANDIDATE_REL + "/" + SOURCE_REL + "/" + name
        pins[ORIGINAL / name] = ORIGINAL_OVERRIDES.get(name, entries[relative])
    before = snapshot(pins)
    script_path = Path(__file__)
    script_hash = digest(script_path.read_bytes())
    candidate_sources = {
        name: authenticated_read(CANDIDATE / SOURCE_REL / name, pins[CANDIDATE / SOURCE_REL / name])
        for name in NAMES
    }
    original_sources = {
        name: authenticated_read(ORIGINAL / name, pins[ORIGINAL / name])
        for name in NAMES
    }

    # Execute only exact authenticated candidate errors/source_audit bytes.
    # The namespace package prevents __init__ or other source imports.
    package_name = "a05_source_closure_diagnostic"
    package = ModuleType(package_name)
    package.__path__ = []
    sys.modules[package_name] = package
    loaded = {}
    for name in ("errors", "source_audit"):
        module_name = package_name + "." + name
        module = ModuleType(module_name)
        module.__package__ = package_name
        sys.modules[module_name] = module
        exec(compile(candidate_sources[name + ".py"], str(CANDIDATE / SOURCE_REL / (name + ".py")), "exec"), module.__dict__)
        loaded[name] = module
    audit = loaded["source_audit"]
    error_type = loaded["errors"].RuntimeProfileError

    variants = [
        ("all_originals", dict(original_sources)),
        ("all_candidate", dict(candidate_sources)),
        ("originals_except_candidate_profile", {**original_sources, "profile.py": candidate_sources["profile.py"]}),
        ("originals_except_candidate_preloader", {**original_sources, "preloader.py": candidate_sources["preloader.py"]}),
    ]
    matrix = []
    for label, sources in variants:
        row = {"case": label, "source_hashes": {name: digest(raw) for name, raw in sources.items()}}
        try:
            row["returned_inventory"] = list(audit.inspect_source_structure(sources))
            row.update(status="pass", error_type=None, error=None)
        except error_type as exc:
            row.update(status="reject", error_type=type(exc).__name__, error=str(exc))
        matrix.append(row)

    differences = {}
    for name in ("profile.py", "preloader.py"):
        added = sorted(import_set(candidate_sources[name]) - import_set(original_sources[name]))
        removed = sorted(import_set(original_sources[name]) - import_set(candidate_sources[name]))
        added_details = []
        for kind, level, module, symbol, alias in added:
            allowed = (
                audit._ALLOWED_RELATIVE_FROM.get(module, set()) if level == 1
                else audit._ALLOWED_ABSOLUTE_FROM.get(module, set()) if level == 0 and kind == "from"
                else set()
            )
            added_details.append({
                "kind": kind, "level": level, "module": module, "symbol": symbol,
                "alias": alias, "symbol_in_unchanged_allowlist": symbol in allowed,
                "unchanged_allowlist": sorted(allowed),
            })
        differences[name] = {"added": added_details, "removed": removed}

    after = snapshot(pins)
    if before != after or script_hash != digest(script_path.read_bytes()):
        raise AssertionError("input or diagnostic harness changed during execution")
    result = {
        "diagnostic": "a05-profile-composition-v0.1-source-closure",
        "command": '& "C:/Users/SSAFY/AppData/Local/Python/pythoncore-3.12-64/python.exe" -I -S -B -X utf8 "C:/Users/SSAFY/Documents/ai-development-tradition/s0-lab/audit-remediation/a05-profile-composition-v0.1/diagnostics/test_source_closure.py"',
        "interpreter_version": sys.version,
        "diagnostic_script_sha256": script_hash,
        "executed_candidate_modules": ["errors.py", "source_audit.py"],
        "matrix": matrix,
        "ast_import_set_differences": differences,
        "frozen_manifest_entries": 17,
        "original_source_entries": 10,
        "pre_input_sha256": before,
        "post_input_sha256": after,
        "all_pinned_inputs_unchanged": before == after,
        "limitations": [
            "Source-unit diagnostic only; no original source executed.",
            "No implementation, existing test, manifest, or policy modified.",
            "No S0/E0 execution, native/P4 validation, or provider call.",
            "Full interpreter, installed standard-library, and native closure remain unverified.",
        ],
    }
    result_raw = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    with result_path.open("xb") as output:
        output.write(result_raw)
    lines = ["a05 source-closure diagnostic"]
    for row in matrix:
        lines.append(row["case"] + ": " + row["status"] + (" | " + row["error"] if row["error"] else ""))
    for name, change in differences.items():
        for added in change["added"]:
            lines.append(name + " added import: " + "." * added["level"] + added["module"] + "." + added["symbol"] + "; admitted=" + str(added["symbol_in_unchanged_allowlist"]))
    lines.extend([
        "Frozen manifest: 17/17 unchanged; original sources: 10/10 unchanged.",
        "All 30 pinned inputs match before and after execution.",
        "Diagnostic script SHA256: " + script_hash,
        "Result JSON SHA256: " + digest(result_raw),
    ])
    stdout = "\n".join(lines) + "\n"
    with stdout_path.open("x", encoding="utf-8", newline="\n") as output:
        output.write(stdout)
    print(stdout, end="")


if __name__ == "__main__":
    main()

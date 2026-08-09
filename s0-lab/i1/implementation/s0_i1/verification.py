"""Deterministic public I1 construction verification; never an S0 run."""

from __future__ import annotations

import ast
import platform
from importlib.metadata import version
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .auth import (
    ManifestAnchor,
    authenticate_manifest_file_set,
    load_authenticated_manifest,
)
from .errors import safe_exception_message
from .json_bytes import parse_strict_json_bytes
from .topology import (
    FROZEN_PUBLIC_SPEC_MANIFEST_SHA256,
    PUBLIC_SPEC_MANIFEST_PATH,
    audit_topology,
    load_public_runtime_spec,
)


_FORBIDDEN_RUNTIME_IMPORTS = {
    "aiohttp",
    "asyncio",
    "ftplib",
    "http",
    "requests",
    "socket",
    "subprocess",
    "urllib",
    "webbrowser",
}


def _implementation_import_audit(workspace_root: Path) -> dict[str, Any]:
    implementation = workspace_root / "s0-lab" / "i1" / "implementation" / "s0_i1"
    files: list[dict[str, Any]] = []
    violations: list[dict[str, str]] = []
    for path in sorted(implementation.glob("*.py")):
        raw = path.read_bytes()
        tree = ast.parse(raw.decode("utf-8", errors="strict"))
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".")[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".")[0])
        forbidden = sorted(imported & _FORBIDDEN_RUNTIME_IMPORTS)
        relative = path.relative_to(workspace_root).as_posix()
        files.append({"path": relative, "imports": sorted(imported)})
        for module in forbidden:
            violations.append({"path": relative, "module": module})
    return {"files": files, "forbidden_imports": violations}


def build_public_verification_record(workspace_root: Path) -> dict[str, Any]:
    """Build a stable fact/test/proposal-separated verification record."""

    errors: list[dict[str, str]] = []
    facts: dict[str, Any] | None = None
    tests: dict[str, Any] | None = None
    closed_boundaries: list[str] = []
    try:
        spec = load_public_runtime_spec(workspace_root)
        anchor = ManifestAnchor(
            PUBLIC_SPEC_MANIFEST_PATH,
            FROZEN_PUBLIC_SPEC_MANIFEST_SHA256,
            "s0-lab/i1/spec/",
        )
        manifest = load_authenticated_manifest(workspace_root, anchor)
        files = authenticate_manifest_file_set(workspace_root, manifest)
        schema_results: list[dict[str, Any]] = []
        for relative, authenticated in sorted(files.items()):
            if not relative.endswith(".schema.json"):
                continue
            schema = parse_strict_json_bytes(authenticated.raw, require_object=True)
            Draft202012Validator.check_schema(schema)
            schema_results.append({"path": relative, "sha256": authenticated.sha256})
        topology_issues = [issue.as_dict() for issue in audit_topology(spec)]
        source_audit = _implementation_import_audit(workspace_root)
        if topology_issues:
            errors.append({"category": "topology", "message": "public topology audit failed"})
        if source_audit["forbidden_imports"]:
            errors.append({"category": "source-boundary", "message": "forbidden runtime import found"})
        facts = {
            "spec_manifest_sha256": manifest.manifest.sha256,
            "authenticated_spec_files": len(files),
            "counts": spec["counts"],
            "source_sha256": spec["source_sha256"],
        }
        tests = {
            "schema_definitions_checked": len(schema_results),
            "schema_results": schema_results,
            "topology_issue_count": len(topology_issues),
            "topology_issues": topology_issues,
            "source_boundary": source_audit,
        }
        closed_boundaries = list(spec["closed_boundaries"])
    except Exception as exc:
        errors.append(
            {"category": type(exc).__name__, "message": safe_exception_message(exc)}
        )
    return {
        "record_kind": "i1-public-structural-verification",
        "not_an_s0_run": True,
        "status": "pass" if not errors else "fail",
        "runtime": {
            "python": platform.python_version(),
            "jsonschema": version("jsonschema"),
        },
        "authenticated_facts": facts,
        "construction_tests": tests,
        "closed_proposals_and_boundaries": closed_boundaries,
        "errors": errors,
    }

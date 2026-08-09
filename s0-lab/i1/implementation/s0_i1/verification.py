"""Deterministic public I1 construction verification; never an S0 run."""

from __future__ import annotations

import ast
import platform
from importlib.metadata import version
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from .auth import (
    authenticate_manifest_file_set,
    bind_external_manifest_grant,
    load_authenticated_manifest,
)
from .errors import safe_exception_message
from .json_bytes import parse_strict_json_bytes
from .topology import (
    FROZEN_PUBLIC_SPEC_MANIFEST_SHA256,
    PUBLIC_SPEC_ALLOWED_PATHS,
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


def _schema_instance_checks(
    schemas: dict[str, dict[str, Any]], spec: dict[str, Any]
) -> dict[str, Any]:
    """Exercise accepted and rejected instances, not only metaschemas."""

    digest = "0" * 64
    signature = "0" * 128
    receipt_schema = schemas["evidence-receipt.schema.json"]
    bundle_schema = schemas["evidence-bundle-structure.schema.json"]
    status_schema = schemas["status-record.schema.json"]
    signed_schema = schemas["signed-envelope-structure.schema.json"]
    result_schema = schemas["one-shot-result.schema.json"]
    topology_schema = schemas["public-runtime-topology.schema.json"]

    positive: list[tuple[str, dict[str, Any], dict[str, Any]]] = []
    negative: list[tuple[str, dict[str, Any], dict[str, Any]]] = []
    for row in spec["status"]["receipts"]:
        for entry in row["entries"]:
            positive.append(
                (
                    "evidence-receipt",
                    receipt_schema,
                    {
                        "edge": row["edge"],
                        "producer_role": entry["producer_role"],
                        "artifact_kind": entry["artifact_kind"],
                        "artifact_sha256": digest,
                        "required_check_result": "accepted",
                    },
                )
            )
    negative.extend(
        (
            (
                "receipt-invalid-edge",
                receipt_schema,
                {
                    "edge": "E99",
                    "producer_role": "content-intake",
                    "artifact_kind": "content-digest",
                    "artifact_sha256": digest,
                    "required_check_result": "accepted",
                },
            ),
            (
                "receipt-invalid-role-kind",
                receipt_schema,
                {
                    "edge": "E05",
                    "producer_role": "simulation-builder",
                    "artifact_kind": "content-digest",
                    "artifact_sha256": digest,
                    "required_check_result": "accepted",
                },
            ),
        )
    )
    positive.extend(
        (
            (
                "bundle-root",
                bundle_schema,
                {
                    "edge": "ROOT",
                    "entry_count": 0,
                    "control_integration_manifest_sha256": digest,
                    "envelope_sha256": [],
                },
            ),
            (
                "bundle-e02",
                bundle_schema,
                {"edge": "E02", "entry_count": 3, "envelope_sha256": [digest] * 3},
            ),
            (
                "bundle-e25",
                bundle_schema,
                {"edge": "E25", "entry_count": 2, "envelope_sha256": [digest] * 2},
            ),
            (
                "bundle-single",
                bundle_schema,
                {"edge": "E56", "entry_count": 1, "envelope_sha256": [digest]},
            ),
        )
    )
    negative.extend(
        (
            ("bundle-root-missing-manifest", bundle_schema, {"edge": "ROOT", "entry_count": 0, "envelope_sha256": []}),
            ("bundle-root-with-entry", bundle_schema, {"edge": "ROOT", "entry_count": 1, "control_integration_manifest_sha256": digest, "envelope_sha256": [digest]}),
            ("bundle-e25-count-array", bundle_schema, {"edge": "E25", "entry_count": 2, "envelope_sha256": [digest]}),
            ("bundle-nonroot-manifest", bundle_schema, {"edge": "E05", "entry_count": 1, "control_integration_manifest_sha256": digest, "envelope_sha256": [digest]}),
        )
    )
    for sequence, state in enumerate(spec["status"]["states"]):
        positive.append(
            (
                "status-record",
                status_schema,
                {
                    "sequence": sequence,
                    "previous_record_sha256": digest,
                    "event_edge": "ROOT" if sequence == 0 else spec["status"]["edge_order"][sequence - 1],
                    "event_commitment_sha256": digest,
                    "evidence_mask": state[2:],
                    "status_code": state,
                    "monotonic_timestamp_ns": sequence,
                },
            )
        )
    negative.extend(
        (
            ("status-invalid-edge", status_schema, {"sequence": 1, "previous_record_sha256": digest, "event_edge": "E99", "event_commitment_sha256": digest, "evidence_mask": "0001", "status_code": "A-0001", "monotonic_timestamp_ns": 1}),
            ("status-invalid-relation", status_schema, {"sequence": 2, "previous_record_sha256": digest, "event_edge": "E02", "event_commitment_sha256": digest, "evidence_mask": "0001", "status_code": "A-0001", "monotonic_timestamp_ns": 2}),
            ("status-invalid-root-previous", status_schema, {"sequence": 0, "previous_record_sha256": "1" * 64, "event_edge": "ROOT", "event_commitment_sha256": digest, "evidence_mask": "0000", "status_code": "A-0000", "monotonic_timestamp_ns": 0}),
        )
    )
    positive.extend(
        (
            ("signed-envelope", signed_schema, {"signer_role": "content-intake", "signer_key_sha256": digest, "record_length": 1, "record_sha256": digest, "signature_algorithm": "Ed25519", "signature_hex": signature}),
            ("one-shot-result", result_schema, {"record_kind": "i1-public-one-shot-structural-result", "not_an_s0_run": True, "run_id": "RUN.PUBLIC", "request_sha256": digest, "response_sha256": digest, "response_bytes": 1, "parsed_type": "object"}),
            ("public-topology", topology_schema, spec),
        )
    )
    bad_topology = dict(spec)
    bad_topology["spec_schema"] = "INVALID"
    negative.extend(
        (
            ("signed-envelope-role", signed_schema, {"signer_role": "forged-role", "signer_key_sha256": digest, "record_length": 1, "record_sha256": digest, "signature_algorithm": "Ed25519", "signature_hex": signature}),
            ("one-shot-zero-bytes", result_schema, {"record_kind": "i1-public-one-shot-structural-result", "not_an_s0_run": True, "run_id": "RUN.PUBLIC", "request_sha256": digest, "response_sha256": digest, "response_bytes": 0, "parsed_type": "object"}),
            ("public-topology-identity", topology_schema, bad_topology),
        )
    )

    positive_failures = [
        label
        for label, schema, instance in positive
        if not Draft202012Validator(schema).is_valid(instance)
    ]
    negative_failures = [
        label
        for label, schema, instance in negative
        if Draft202012Validator(schema).is_valid(instance)
    ]
    return {
        "positive_instances": len(positive),
        "negative_instances": len(negative),
        "positive_failures": positive_failures,
        "negative_failures": negative_failures,
        "runtime_only_relations": [
            "ASCII/LF field order and exact byte framing",
            "record length, SHA-256 scope, role/key binding, and injected signature decision",
            "bundle envelope extraction and immutable topology receipt order",
            "status previous hash, event commitment, and timestamp increase",
            "E43/E45 source-envelope extraction, common byte equality, and named digest scope",
            "E54/E55 decision byte equality and E56 full-envelope digest binding",
        ],
    }


def build_public_verification_record(workspace_root: Path) -> dict[str, Any]:
    """Build a stable fact/test/proposal-separated verification record."""

    errors: list[dict[str, str]] = []
    facts: dict[str, Any] | None = None
    tests: dict[str, Any] | None = None
    closed_boundaries: list[str] = []
    try:
        topology = load_public_runtime_spec(workspace_root)
        spec = topology.to_plain_dict()
        grant = bind_external_manifest_grant(
            expected_manifest_path=PUBLIC_SPEC_MANIFEST_PATH,
            expected_manifest_sha256=FROZEN_PUBLIC_SPEC_MANIFEST_SHA256,
            expected_entry_prefix="s0-lab/i1/spec/",
            expected_allowed_paths=PUBLIC_SPEC_ALLOWED_PATHS,
            purpose="i1-public-topology",
        )
        manifest = load_authenticated_manifest(workspace_root, grant)
        files = authenticate_manifest_file_set(workspace_root, manifest)
        schema_results: list[dict[str, Any]] = []
        schemas: dict[str, dict[str, Any]] = {}
        for relative, authenticated in sorted(files.items()):
            if not relative.endswith(".schema.json"):
                continue
            schema = parse_strict_json_bytes(authenticated.raw, require_object=True)
            Draft202012Validator.check_schema(schema)
            schemas[Path(relative).name] = schema
            schema_results.append({"path": relative, "sha256": authenticated.sha256})
        instance_results = _schema_instance_checks(schemas, spec)
        topology_issues = [issue.as_dict() for issue in audit_topology(spec)]
        source_audit = _implementation_import_audit(workspace_root)
        if topology_issues:
            errors.append({"category": "topology", "message": "public topology audit failed"})
        if source_audit["forbidden_imports"]:
            errors.append({"category": "source-boundary", "message": "forbidden runtime import found"})
        if instance_results["positive_failures"] or instance_results["negative_failures"]:
            errors.append({"category": "schema-instances", "message": "schema positive/negative instance checks failed"})
        facts = {
            "spec_manifest_sha256": manifest.manifest.sha256,
            "authenticated_spec_files": len(files),
            "counts": spec["counts"],
            "source_sha256": spec["source_sha256"],
        }
        tests = {
            "schema_definitions_checked": len(schema_results),
            "schema_results": schema_results,
            "schema_instances": instance_results,
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

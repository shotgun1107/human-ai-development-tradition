"""Frozen-schema verification for the eleven designated public instances."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .integrity import (
    BUNDLE_RELATIVE,
    SCHEMA_INSTANCE_MAP,
    SCHEMA_RELATIVE,
    sha256_bytes,
    verify_public_bundle,
)
from .json_validation import load_json, validate_instance


FROZEN_SCHEMA_HASHES = {
    "sm0/answer.schema.json": "e21100f06d2715f42cd1fda812e17d22340a64327bfb48c03112a0f83d33ac6b",
    "sm0/common-manifest.schema.json": "a539022d937672a99c605c12980f10d89a956a40c1e8523cb02f774d280ccc8a",
    "sm0/condition-overlay-manifest.schema.json": "a239c1ffa7e4b9ae3c963e7ddbf55c4cabf1f05353032cd11d9d35b842086e7a",
    "sm0/fixture-manifest.schema.json": "846071f069b1cbc040ef89e176caa1698dfb13fce6c6848505a60523fd8f9c80",
    "sm1/question-options.schema.json": "5bd4c1970662b1254f73b828e7f9e6e110d9d683621e8bc6c7bd73fe4def42e0",
    "sm1/transformation-manifest.schema.json": "8e233cbd678c8319da1b192ddec80ac0907444d7c05802a7c110b6bf35a9d346",
    "sm1/neutral-answer-validation.schema.json": "675222967cebc312e8fe79bc45763254bd232e3f2325df6d1a4463e7d1d0066c",
    "sm1/access-manifest.schema.json": "3e27d1bcdb253a9065443d1d9244889dfad753c63512d89178c7ca93dee3ef4b",
    "sm1/run-manifest.schema.json": "ef773dcc5bc17e6924aafc6c6ab01f080e8793a6ab91c5cbf44654105e5e9f84",
    "sm1/scoring.schema.json": "2d4e3464c01ca9c220df7344cfdf76bb05021d9d4eec484007c2e21c80af082e",
    "sm1/pre-review-record.schema.json": "b936fcd86a270f57d81b959682cd72a40e22a35e49013a5ee2f6a3b4c89fa23e",
}


def validate_public_schema_instances(workspace_root: Path) -> dict[str, Any]:
    # Authenticate the complete frozen public file set before any designated
    # instance is parsed.  This makes this function safe when called standalone.
    verify_public_bundle(workspace_root)
    results: list[dict[str, Any]] = []
    total_errors = 0
    for schema_rel, instance_rel in SCHEMA_INSTANCE_MAP:
        schema_path = workspace_root / SCHEMA_RELATIVE / schema_rel
        instance_path = workspace_root / BUNDLE_RELATIVE / instance_rel
        schema, schema_raw = load_json(schema_path)
        expected = FROZEN_SCHEMA_HASHES[schema_rel]
        actual = sha256_bytes(schema_raw)
        if actual != expected:
            errors = [{
                "category": "frozen-hash",
                "instance_path": "$",
                "schema_path": "$",
                "message": f"frozen schema hash mismatch: {schema_rel}",
            }]
        else:
            instance, _ = load_json(instance_path)
            errors = [error.as_dict() for error in validate_instance(instance, schema)]
        total_errors += len(errors)
        results.append({
            "schema": schema_rel,
            "instance": instance_rel,
            "schema_sha256": actual,
            "errors": errors,
        })
    return {"schema_count": len(results), "error_count": total_errors, "results": results}


def audit_broader_upstream_id_impact(workspace_root: Path) -> dict[str, Any]:
    """Report related B2 ID/path violations outside the designated eleven map."""

    verify_public_bundle(workspace_root)
    mappings = (
        ("sm1/run-manifest.schema.json", "manifests/run-manifest.json", "designated"),
        (
            "sm0/fixture-manifest.schema.json",
            "blocks/BLK-PRACTICE0002/fixture-manifest.json",
            "additional-impact",
        ),
        (
            "sm1/transformation-manifest.schema.json",
            "blocks/BLK-PRACTICE0002/transformation-manifest.json",
            "additional-impact",
        ),
    )
    results: list[dict[str, Any]] = []
    total = 0
    for schema_rel, instance_rel, classification in mappings:
        schema, schema_raw = load_json(workspace_root / SCHEMA_RELATIVE / schema_rel)
        if sha256_bytes(schema_raw) != FROZEN_SCHEMA_HASHES[schema_rel]:
            errors = [{
                "category": "frozen-hash",
                "instance_path": "$",
                "schema_path": "$",
                "message": f"frozen schema hash mismatch: {schema_rel}",
            }]
        else:
            instance, _ = load_json(workspace_root / BUNDLE_RELATIVE / instance_rel)
            errors = [error.as_dict() for error in validate_instance(instance, schema)]
        total += len(errors)
        results.append(
            {
                "classification": classification,
                "schema": schema_rel,
                "instance": instance_rel,
                "error_count": len(errors),
                "errors": errors,
            }
        )
    return {
        "related_error_count": total,
        "designated_error_count": results[0]["error_count"],
        "additional_error_count": sum(item["error_count"] for item in results[1:]),
        "results": results,
    }

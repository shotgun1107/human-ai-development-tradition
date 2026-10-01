"""Integrity checks for the frozen, fictional F0-PUBLIC practice bundle."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path, PurePosixPath
from typing import Any

from .json_validation import load_json


MANIFEST_LINE = re.compile(r"^([a-f0-9]{64})  ([^\r\n]+)$")
BUNDLE_RELATIVE = Path("s0-lab/public-practice/v0.1")
SCHEMA_RELATIVE = Path("s0-lab/control")

SCHEMA_INSTANCE_MAP = (
    ("sm0/answer.schema.json", "examples/answer.json"),
    ("sm0/common-manifest.schema.json", "manifests/common-manifest.json"),
    ("sm0/condition-overlay-manifest.schema.json", "manifests/overlay-P01.json"),
    ("sm0/fixture-manifest.schema.json", "blocks/BLK-PRACTICE0001/fixture-manifest.json"),
    ("sm1/question-options.schema.json", "blocks/BLK-PRACTICE0001/question-options.json"),
    ("sm1/transformation-manifest.schema.json", "blocks/BLK-PRACTICE0001/transformation-manifest.json"),
    ("sm1/neutral-answer-validation.schema.json", "manifests/neutral-answer-validation.json"),
    ("sm1/access-manifest.schema.json", "manifests/access-manifest.json"),
    ("sm1/run-manifest.schema.json", "manifests/run-manifest.json"),
    ("sm1/scoring.schema.json", "blocks/BLK-PRACTICE0001/public-scoring.json"),
    ("sm1/pre-review-record.schema.json", "manifests/pre-review-record.json"),
)


class IntegrityError(ValueError):
    """A frozen public-bundle invariant failed."""


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def aggregate_facts(facts: list[dict[str, Any]]) -> tuple[str, str]:
    fact_ids = sorted(fact["fact_id"] for fact in facts)
    fact_set = sha256_bytes("\n".join(fact_ids).encode("utf-8"))
    record_lines = []
    for fact in facts:
        text_hash = sha256_bytes(fact["text"].encode("utf-8"))
        record_lines.append(f'{fact["record_id"]}\t{text_hash}')
    record_set = sha256_bytes("\n".join(sorted(record_lines)).encode("utf-8"))
    return fact_set, record_set


def parse_bundle_manifest(bundle_root: Path) -> dict[str, str]:
    manifest_path = bundle_root / "bundle-files.sha256"
    try:
        lines = manifest_path.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError as exc:
        raise IntegrityError("bundle manifest is not UTF-8") from exc

    result: dict[str, str] = {}
    for line in lines:
        match = MANIFEST_LINE.fullmatch(line)
        if not match:
            raise IntegrityError("invalid bundle manifest line")
        digest, relative = match.groups()
        pure = PurePosixPath(relative)
        if pure.is_absolute() or ".." in pure.parts or "\\" in relative:
            raise IntegrityError(f"unsafe manifest path: {relative}")
        if relative == "bundle-files.sha256":
            raise IntegrityError("bundle manifest must exclude itself")
        if relative in result:
            raise IntegrityError(f"duplicate manifest path: {relative}")
        result[relative] = digest
    if len(result) != 90:
        raise IntegrityError(f"expected 90 manifest entries, found {len(result)}")
    return result


def _verify_fact_manifest(bundle_root: Path, block_dir: str) -> dict[str, str]:
    canonical, _ = load_json(bundle_root / "blocks" / block_dir / "canonical-input.json")
    manifest, _ = load_json(bundle_root / "blocks" / block_dir / "fact-manifest.json")
    computed_fact, computed_record = aggregate_facts(canonical["facts"])
    if computed_fact != manifest["fact_set_sha256"]:
        raise IntegrityError(f"fact-set aggregate mismatch: {block_dir}")
    if computed_record != manifest["record_content_set_sha256"]:
        raise IntegrityError(f"record-content aggregate mismatch: {block_dir}")
    listed = {
        item["fact_id"]: (item["record_id"], item["normalized_text_sha256"])
        for item in manifest["facts"]
    }
    computed = {
        fact["fact_id"]: (fact["record_id"], sha256_bytes(fact["text"].encode("utf-8")))
        for fact in canonical["facts"]
    }
    if listed != computed:
        raise IntegrityError(f"fact manifest content mismatch: {block_dir}")
    return {"fact_set_sha256": computed_fact, "record_content_set_sha256": computed_record}


def verify_public_bundle(workspace_root: Path) -> dict[str, Any]:
    bundle_root = (workspace_root / BUNDLE_RELATIVE).resolve(strict=True)
    manifest = parse_bundle_manifest(bundle_root)

    discovered = list(bundle_root.rglob("*"))
    symlinks = sorted(path.relative_to(bundle_root).as_posix() for path in discovered if path.is_symlink())
    if symlinks:
        raise IntegrityError(f"bundle must not contain symbolic links: {symlinks}")
    disk = {
        path.relative_to(bundle_root).as_posix()
        for path in discovered
        if path.is_file() and path.name != "bundle-files.sha256"
    }
    if disk != set(manifest):
        missing = sorted(set(manifest) - disk)
        extra = sorted(disk - set(manifest))
        raise IntegrityError(f"bundle file-set mismatch; missing={missing}; extra={extra}")

    json_count = 0
    for relative, expected in sorted(manifest.items()):
        path = bundle_root / PurePosixPath(relative)
        raw = path.read_bytes()
        if sha256_bytes(raw) != expected:
            raise IntegrityError(f"bundle hash mismatch: {relative}")
        if relative.endswith(".json"):
            load_json(path)
            json_count += 1

    aggregates = {
        block: _verify_fact_manifest(bundle_root, block)
        for block in ("BLK-PRACTICE0001", "BLK-PRACTICE0002")
    }

    package_results: dict[str, dict[str, Any]] = {}
    max_ratios: dict[str, float] = {}
    for block in ("BLK-PRACTICE0001", "BLK-PRACTICE0002"):
        canonical, _ = load_json(bundle_root / "blocks" / block / "canonical-input.json")
        transform_manifest, _ = load_json(
            bundle_root / "blocks" / block / "transformation-manifest.json"
        )
        sizes: list[int] = []
        for output in transform_manifest["outputs"]:
            relative = output["runner_path"]
            raw = (bundle_root / PurePosixPath(relative)).read_bytes()
            package, _ = load_json(bundle_root / PurePosixPath(relative))
            if package.get("block_id") != block or package.get("facts") != canonical["facts"]:
                raise IntegrityError(f"package fact/project/timestamp/text mismatch: {relative}")
            if len(raw) != output["byte_count"]:
                raise IntegrityError(f"package byte count mismatch: {relative}")
            if sha256_bytes(raw) != output["input_sha256"]:
                raise IntegrityError(f"package output hash mismatch: {relative}")
            fact_hash, record_hash = aggregate_facts(package["facts"])
            if fact_hash != output["fact_set_sha256"] or record_hash != output["record_content_set_sha256"]:
                raise IntegrityError(f"package aggregate mismatch: {relative}")
            package_results[relative] = {"sha256": sha256_bytes(raw), "bytes": len(raw)}
            sizes.append(len(raw))
        ratio = (max(sizes) - min(sizes)) / min(sizes)
        if ratio > 0.15:
            raise IntegrityError(f"package byte ceiling exceeded: {block}")
        max_ratios[block] = ratio

    return {
        "manifest_entries": len(manifest),
        "json_files": json_count,
        "aggregates": aggregates,
        "packages": package_results,
        "max_byte_ratios": max_ratios,
    }

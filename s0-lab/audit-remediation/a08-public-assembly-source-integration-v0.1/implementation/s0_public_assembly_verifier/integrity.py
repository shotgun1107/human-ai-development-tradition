"""Exact public manifest and design-authority authentication."""

from __future__ import annotations

import hashlib
import re
from pathlib import Path, PurePosixPath
from types import MappingProxyType
from typing import Mapping

from .errors import auth_failure
from .pins import (
    DESIGN_INDEPENDENT_REVIEW_SHA256,
    DESIGN_PACKAGE_MANIFEST_SHA256,
    I0_IMPLEMENTATION_MANIFEST_SHA256,
    I1_IMPLEMENTATION_MANIFEST_SHA256,
    I2_IMPLEMENTATION_MANIFEST_SHA256,
    I3_IMPLEMENTATION_MANIFEST_SHA256,
)


_ROW = re.compile(rb"^([0-9a-f]{64})  ([A-Za-z0-9._/-]+)$")

COMPONENT_MANIFESTS = (
    (
        "s0-lab/i0/verification/implementation-files.sha256",
        I0_IMPLEMENTATION_MANIFEST_SHA256,
        "s0-lab/i0",
        False,
    ),
    (
        "s0-lab/i1/verification/implementation-files.sha256",
        I1_IMPLEMENTATION_MANIFEST_SHA256,
        "s0-lab/i1",
        False,
    ),
    (
        "s0-lab/i2/verification/implementation-files.sha256",
        I2_IMPLEMENTATION_MANIFEST_SHA256,
        ".",
        True,
    ),
    (
        "s0-lab/i3/verification/implementation-files.sha256",
        I3_IMPLEMENTATION_MANIFEST_SHA256,
        ".",
        True,
    ),
)

DESIGN_MANIFEST_PATH = (
    "s0-lab/control/assembly-rehearsal/public-end-to-end-v0.5/"
    "design-package-files.sha256"
)
DESIGN_REVIEW_PATH = (
    "s0-lab/reviews/assembly-rehearsal/public-end-to-end-v0.5/"
    "public-end-to-end-assembly-rehearsal-design-v0.5-independent-rereview-v0.1.md"
)
INTERFACE_MAP_PATH = (
    "s0-lab/control/assembly-rehearsal/public-end-to-end-v0.5/"
    "assembly-rehearsal-interface-map-v0.5.json"
)


def sha256_bytes(raw: bytes) -> str:
    if type(raw) is not bytes:
        raise TypeError("hash input must be exact bytes")
    return hashlib.sha256(raw).hexdigest()


def _workspace_file(workspace_root: Path, relative: str) -> Path:
    if type(relative) is not str or not relative or "\\" in relative or "\x00" in relative:
        raise auth_failure("manifest path is not canonical POSIX-relative text")
    pure = PurePosixPath(relative)
    if pure.is_absolute() or any(part in {"", ".", ".."} or ":" in part for part in pure.parts):
        raise auth_failure("manifest path escapes its public workspace authority")
    root = workspace_root.resolve(strict=True)
    candidate = root.joinpath(*pure.parts)
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root)
    except (OSError, ValueError) as exc:
        raise auth_failure("authenticated public input is missing or escapes the workspace") from exc
    if resolved != candidate or not candidate.is_file() or candidate.is_symlink():
        raise auth_failure("authenticated public input is not an exact regular path")
    return candidate


def read_exact_public_file(workspace_root: Path, relative: str, expected_sha256: str) -> bytes:
    raw = _workspace_file(workspace_root, relative).read_bytes()
    if sha256_bytes(raw) != expected_sha256:
        raise auth_failure("authenticated public input SHA-256 mismatch")
    return raw


def parse_manifest(raw: bytes) -> Mapping[str, str]:
    if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw or not raw.endswith(b"\n"):
        raise auth_failure("manifest text form is noncanonical")
    entries: dict[str, str] = {}
    for line in raw[:-1].split(b"\n"):
        match = _ROW.fullmatch(line)
        if match is None:
            raise auth_failure("manifest contains a noncanonical row")
        digest = match.group(1).decode("ascii")
        relative = match.group(2).decode("ascii")
        pure = PurePosixPath(relative)
        if pure.is_absolute() or any(part in {"", ".", ".."} or ":" in part for part in pure.parts):
            raise auth_failure("manifest row escapes its public authority")
        if relative in entries:
            raise auth_failure("manifest contains a duplicate path")
        entries[relative] = digest
    if not entries:
        raise auth_failure("manifest must contain at least one row")
    return MappingProxyType(dict(entries))


def verify_manifest_rows(
    workspace_root: Path,
    *,
    manifest_path: str,
    manifest_sha256: str,
    row_base: str,
    rows_are_repo_relative: bool,
) -> Mapping[str, str]:
    raw = read_exact_public_file(workspace_root, manifest_path, manifest_sha256)
    entries = parse_manifest(raw)
    for relative, digest in entries.items():
        if rows_are_repo_relative:
            target = relative
        elif row_base == ".":
            target = relative
        else:
            target = f"{row_base}/{relative}"
        read_exact_public_file(workspace_root, target, digest)
    return entries


def verify_component_implementations(workspace_root: Path) -> dict[str, int]:
    counts: dict[str, int] = {}
    for index, (path, digest, base, repo_relative) in enumerate(COMPONENT_MANIFESTS):
        entries = verify_manifest_rows(
            workspace_root,
            manifest_path=path,
            manifest_sha256=digest,
            row_base=base,
            rows_are_repo_relative=repo_relative,
        )
        counts[f"i{index}"] = len(entries)
    return counts


def verify_v0_5_design_authority(workspace_root: Path) -> Mapping[str, str]:
    entries = verify_manifest_rows(
        workspace_root,
        manifest_path=DESIGN_MANIFEST_PATH,
        manifest_sha256=DESIGN_PACKAGE_MANIFEST_SHA256,
        row_base=".",
        rows_are_repo_relative=True,
    )
    if len(entries) != 5 or INTERFACE_MAP_PATH not in entries:
        raise auth_failure("v0.5 design-package manifest inventory mismatch")
    read_exact_public_file(
        workspace_root,
        DESIGN_REVIEW_PATH,
        DESIGN_INDEPENDENT_REVIEW_SHA256,
    )
    return entries

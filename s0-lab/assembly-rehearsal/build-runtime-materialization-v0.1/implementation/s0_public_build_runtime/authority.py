"""Exact public design-manifest authentication with caller-supplied bytes only."""

from __future__ import annotations

import re
from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from .canonical import freeze_exact_mapping, require_sha256, sha256_hex
from .errors import AuthenticationError, CanonicalError

_MANIFEST_ROW = re.compile(rb"^([0-9a-f]{64})  ([A-Za-z0-9._/-]+)$")
_DESIGN_MANIFESTS = (
    (
        "s0-lab/control/assembly-rehearsal/build-runtime-materialization-v0.1/design-package-files.sha256",
        "bdf3cd280c65adcb4a1a4c965a3e2512e460eb2c03f498274bddfe5879ba5e1c",
        6,
    ),
    (
        "s0-lab/control/assembly-rehearsal/build-runtime-materialization-v0.2/design-package-files.sha256",
        "47b956ca352f0e8ac969cdd36b801234c1436cefe50308c1e4d7c2b4e9bf1304",
        7,
    ),
    (
        "s0-lab/control/assembly-rehearsal/build-runtime-materialization-v0.3/design-package-files.sha256",
        "1d3ddfa20c6e0413b7d0420c17e35e3c2251bba77ee6421cc40d92b40e9c5277",
        9,
    ),
    (
        "s0-lab/control/assembly-rehearsal/build-runtime-materialization-v0.4/design-package-files.sha256",
        "7af9c640f90f4cf42b85b77bb4851af6f33b71890b64355b62e449d58e528884",
        9,
    ),
    (
        "s0-lab/control/assembly-rehearsal/build-runtime-materialization-v0.5/design-package-files.sha256",
        "ca52a47378c9cbd46eae5d94fec8466562c40d702dfdc8d2e1f63c61e4b3f98c",
        7,
    ),
)
_REVIEW_SHA256 = "5353431dfa8bc36b7d86c0ece1eabf88bad0cb598f1a8f73092cdebf2c95e2f9"
_CONTROL_DECISION_SHA256 = "d4fc2bc7ea6a6f606efd9395be230e8aec408cf07a48c246825409cfac7f3eaf"
_AUTHENTICATED = object()


@dataclass(frozen=True)
class ManifestBundle:
    logical_path: str
    raw: bytes
    targets: Mapping[str, bytes]


@dataclass(frozen=True)
class DesignClosure:
    manifests: tuple[ManifestBundle, ...]
    approving_review_raw: bytes
    control_decision_raw: bytes


@dataclass(frozen=True)
class AuthenticatedDesign:
    files: Mapping[str, bytes]
    manifest_hashes: tuple[str, ...]
    marker: object

    def require_authenticated(self) -> None:
        if self.marker is not _AUTHENTICATED or type(self.files) is not type(MappingProxyType({})):
            raise AuthenticationError("design authority is not authenticated")


def manifest_contract() -> tuple[tuple[str, str, int], ...]:
    return _DESIGN_MANIFESTS


def _authenticate_manifest(bundle: ManifestBundle, expected: tuple[str, str, int]) -> dict[str, bytes]:
    path, expected_sha256, expected_rows = expected
    if type(bundle) is not ManifestBundle or bundle.logical_path != path:
        raise AuthenticationError("design manifest path or order differs")
    if type(bundle.raw) is not bytes or sha256_hex(bundle.raw) != expected_sha256:
        raise AuthenticationError("design manifest differs from its external pin")
    if not bundle.raw.endswith(b"\n") or bundle.raw.startswith(b"\xef\xbb\xbf") or b"\r" in bundle.raw:
        raise AuthenticationError("design manifest byte grammar is invalid")
    try:
        snapshot = freeze_exact_mapping(bundle.targets)
    except CanonicalError as error:
        raise AuthenticationError(str(error)) from error
    rows = bundle.raw[:-1].split(b"\n")
    if len(rows) != expected_rows:
        raise AuthenticationError("design manifest row count differs")
    parsed_paths: list[str] = []
    for row in rows:
        match = _MANIFEST_ROW.fullmatch(row)
        if match is None:
            raise AuthenticationError("design manifest row is malformed")
        digest = match.group(1).decode("ascii")
        target = match.group(2).decode("ascii")
        require_sha256(digest)
        raw = snapshot.get(target)
        if raw is None or sha256_hex(raw) != digest:
            raise AuthenticationError("design target differs from its manifest")
        parsed_paths.append(target)
    if len(set(parsed_paths)) != len(parsed_paths):
        raise AuthenticationError("design manifest paths are not unique")
    if set(snapshot) != set(parsed_paths):
        raise AuthenticationError("design target closure is not exact")
    return {path: bundle.raw, **snapshot}


def authenticate_design_closure(closure: DesignClosure) -> AuthenticatedDesign:
    if type(closure) is not DesignClosure or type(closure.manifests) is not tuple:
        raise AuthenticationError("design closure type is not exact")
    if len(closure.manifests) != len(_DESIGN_MANIFESTS):
        raise AuthenticationError("design manifest inventory is not exact")
    if type(closure.approving_review_raw) is not bytes or sha256_hex(closure.approving_review_raw) != _REVIEW_SHA256:
        raise AuthenticationError("approving review differs from its external pin")
    if type(closure.control_decision_raw) is not bytes or sha256_hex(closure.control_decision_raw) != _CONTROL_DECISION_SHA256:
        raise AuthenticationError("CONTROL decision differs from its external pin")
    files: dict[str, bytes] = {}
    hashes: list[str] = []
    for bundle, expected in zip(closure.manifests, _DESIGN_MANIFESTS, strict=True):
        authenticated = _authenticate_manifest(bundle, expected)
        for path, raw in authenticated.items():
            prior = files.get(path)
            if prior is not None and prior != raw:
                raise AuthenticationError("authenticated public path collision")
            files[path] = raw
        hashes.append(expected[1])
    files[
        "s0-lab/reviews/assembly-rehearsal/build-runtime-materialization-v0.5/public-assembly-build-runtime-materialization-design-v0.5-independent-review-v0.1.md"
    ] = closure.approving_review_raw
    files[
        "s0-lab/control/assembly-rehearsal/build-runtime-materialization-v0.5-control-integration/control-integration-decision-v0.1.md"
    ] = closure.control_decision_raw
    return AuthenticatedDesign(MappingProxyType(files), tuple(hashes), _AUTHENTICATED)

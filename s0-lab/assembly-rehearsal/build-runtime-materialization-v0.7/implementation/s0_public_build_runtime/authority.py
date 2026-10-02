"""Exact v0.6 design and external-pin authority activation."""

from __future__ import annotations

import hashlib
import threading
import weakref
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from .canonical import jcs_lf, parse_hash_manifest, read_exact, require_sha256, sha256_hex, strict_json
from .errors import AuthenticationError, CanonicalError

_MANIFESTS = (
    ("s0-lab/control/assembly-rehearsal/build-runtime-materialization-v0.1/design-package-files.sha256", "bdf3cd280c65adcb4a1a4c965a3e2512e460eb2c03f498274bddfe5879ba5e1c", 6),
    ("s0-lab/control/assembly-rehearsal/build-runtime-materialization-v0.2/design-package-files.sha256", "47b956ca352f0e8ac969cdd36b801234c1436cefe50308c1e4d7c2b4e9bf1304", 7),
    ("s0-lab/control/assembly-rehearsal/build-runtime-materialization-v0.3/design-package-files.sha256", "1d3ddfa20c6e0413b7d0420c17e35e3c2251bba77ee6421cc40d92b40e9c5277", 9),
    ("s0-lab/control/assembly-rehearsal/build-runtime-materialization-v0.4/design-package-files.sha256", "7af9c640f90f4cf42b85b77bb4851af6f33b71890b64355b62e449d58e528884", 9),
    ("s0-lab/control/assembly-rehearsal/build-runtime-materialization-v0.5/design-package-files.sha256", "ca52a47378c9cbd46eae5d94fec8466562c40d702dfdc8d2e1f63c61e4b3f98c", 7),
)
_REVIEW = ("s0-lab/reviews/assembly-rehearsal/build-runtime-materialization-v0.5/public-assembly-build-runtime-materialization-design-v0.5-independent-review-v0.1.md", "5353431dfa8bc36b7d86c0ece1eabf88bad0cb598f1a8f73092cdebf2c95e2f9")
_DECISION = ("s0-lab/control/assembly-rehearsal/build-runtime-materialization-v0.5-control-integration/control-integration-decision-v0.1.md", "d4fc2bc7ea6a6f606efd9395be230e8aec408cf07a48c246825409cfac7f3eaf")
_EVIDENCE_PATH = "s0-lab/assembly-rehearsal/build-runtime-materialization-external-artifact-authority-acquisition-v0.1/evidence-manifest.json"
_EVIDENCE_SIZE = 37_688
_EVIDENCE_SHA256 = "b7896b00ba187aa431ff8f81840259f91f58f4dff7c33f5589d9ea1b33b6f084"
_RELATION_SHA256 = "5af2b472f4abf96c446ae56fa90f02d54fa87cdebe4e6129fcc4c3c1de1610db"
_TOKEN = object()


@dataclass(frozen=True, slots=True)
class ArtifactPin:
    pin_id: str
    project: str
    version: str
    filename: str
    size: int
    sha256: str
    url: str
    tag: str
    dist_info_dir: str

    def __post_init__(self) -> None:
        if any(type(value) is not str or not value for value in (self.pin_id, self.project, self.version, self.filename, self.url, self.tag)) or type(self.dist_info_dir) is not str:
            raise AuthenticationError("artifact pin string field differs")
        if type(self.size) is not int or type(self.size) is bool or self.size <= 0:
            raise AuthenticationError("artifact pin size differs")
        require_sha256(self.sha256)
        if "/" in self.filename or "\\" in self.filename or "\x00" in self.filename:
            raise AuthenticationError("artifact filename differs")
        if not self.url.startswith("https://") or "@" in self.url.split("/", 3)[2]:
            raise AuthenticationError("artifact URL is not credential-free HTTPS")


_EXPECTED_PINS = (
    ArtifactPin("cpython-3.12.10-embed-amd64", "cpython", "3.12.10", "python-3.12.10-embed-amd64.zip", 11133606, "4acbed6dd1c744b0376e3b1cf57ce906f9dc9e95e68824584c8099a63025a3c3", "https://www.python.org/ftp/python/3.12.10/python-3.12.10-embed-amd64.zip", "cp312-win_amd64", ""),
    ArtifactPin("jsonschema-4.26.0-py3-none-any", "jsonschema", "4.26.0", "jsonschema-4.26.0-py3-none-any.whl", 90630, "d489f15263b8d200f8387e64b4c3a75f06629559fb73deb8fdfb525f2dab50ce", "https://files.pythonhosted.org/packages/69/90/f63fb5873511e014207a475e2bb4e8b2e570d655b00ac19a9a0ca0a385ee/jsonschema-4.26.0-py3-none-any.whl", "py3-none-any", "jsonschema-4.26.0.dist-info"),
    ArtifactPin("attrs-26.1.0-py3-none-any", "attrs", "26.1.0", "attrs-26.1.0-py3-none-any.whl", 67548, "c647aa4a12dfbad9333ca4e71fe62ddc36f4e63b2d260a37a8b83d2f043ac309", "https://files.pythonhosted.org/packages/64/b4/17d4b0b2a2dc85a6df63d1157e028ed19f90d4cd97c36717afef2bc2f395/attrs-26.1.0-py3-none-any.whl", "py3-none-any", "attrs-26.1.0.dist-info"),
    ArtifactPin("jsonschema-specifications-2025.9.1-py3-none-any", "jsonschema-specifications", "2025.9.1", "jsonschema_specifications-2025.9.1-py3-none-any.whl", 18437, "98802fee3a11ee76ecaca44429fda8a41bff98b00a0f2838151b113f210cc6fe", "https://files.pythonhosted.org/packages/41/45/1a4ed80516f02155c51f51e8cedb3c1902296743db0bbc66608a0db2814f/jsonschema_specifications-2025.9.1-py3-none-any.whl", "py3-none-any", "jsonschema_specifications-2025.9.1.dist-info"),
    ArtifactPin("referencing-0.37.0-py3-none-any", "referencing", "0.37.0", "referencing-0.37.0-py3-none-any.whl", 26766, "381329a9f99628c9069361716891d34ad94af76e461dcb0335825aecc7692231", "https://files.pythonhosted.org/packages/2c/58/ca301544e1fa93ed4f80d724bf5b194f6e4b945841c5bfd555878eea9fcb/referencing-0.37.0-py3-none-any.whl", "py3-none-any", "referencing-0.37.0.dist-info"),
    ArtifactPin("rpds-py-2026.6.3-cp312-cp312-win_amd64", "rpds-py", "2026.6.3", "rpds_py-2026.6.3-cp312-cp312-win_amd64.whl", 220394, "2c958bf94822e9290a40aaf2a822d4bc5c88099093e3948ad6c571eca9272e5f", "https://files.pythonhosted.org/packages/04/3a/f0ee4d4dde9d3b69dedf1b5f74e7a40017046d55052d173e418c6a94f960/rpds_py-2026.6.3-cp312-cp312-win_amd64.whl", "cp312-cp312-win_amd64", "rpds_py-2026.6.3.dist-info"),
    ArtifactPin("typing-extensions-4.16.0-py3-none-any", "typing-extensions", "4.16.0", "typing_extensions-4.16.0-py3-none-any.whl", 45571, "481caa481374e813c1b176ada14e97f1f67a4539ce9cfeb3f350d78d6370c2e8", "https://files.pythonhosted.org/packages/49/d3/b8441a820a491ddfc024b0b0cf0393375b75ea13866d9c66727e54c2fc80/typing_extensions-4.16.0-py3-none-any.whl", "py3-none-any", "typing_extensions-4.16.0.dist-info"),
)


class _ActivatedAuthority:
    __slots__ = (
        "_design_snapshot",
        "_design_snapshot_sha256",
        "_evidence_snapshot",
        "_pin_snapshot",
        "design_rows",
        "design_manifest_hashes",
        "evidence_raw",
        "pins",
        "__weakref__",
    )

    def __init__(self, *args: object, **kwargs: object) -> None:
        del args, kwargs
        raise AuthenticationError("authority construction is repository-activation-only")

    def require_authenticated(self) -> None:
        _validate_issued_authority(self)


def _repo_file(root: Path, logical_path: str) -> Path:
    if type(logical_path) is not str:
        raise AuthenticationError("logical path type differs")
    pure = PurePosixPath(logical_path)
    if pure.is_absolute() or ".." in pure.parts or "\\" in logical_path or ":" in logical_path:
        raise AuthenticationError("logical path escapes the authenticated repository")
    return root.joinpath(*pure.parts)


def _design_snapshot_sha256(snapshot: tuple[tuple[str, bytes], ...]) -> str:
    digest = hashlib.sha256()
    digest.update(b"S0-PUBLIC-BRM-V0.7-DESIGN-SNAPSHOT-1\n")
    for path, raw in snapshot:
        encoded = path.encode("ascii", "strict")
        digest.update(len(encoded).to_bytes(4, "big"))
        digest.update(encoded)
        digest.update(len(raw).to_bytes(8, "big"))
        digest.update(raw)
    return digest.hexdigest()


def _validate_design_snapshot(snapshot: object) -> str:
    if type(snapshot) is not tuple or len(snapshot) != 45:
        raise AuthenticationError("design closure snapshot inventory differs")
    if any(type(row) is not tuple or len(row) != 2 or type(row[0]) is not str or type(row[1]) is not bytes for row in snapshot):
        raise AuthenticationError("design closure snapshot row type differs")
    paths = tuple(row[0] for row in snapshot)
    if paths != tuple(sorted(paths)) or len(paths) != len(set(paths)):
        raise AuthenticationError("design closure snapshot paths differ")
    files = dict(snapshot)
    expected_paths: set[str] = set()
    for manifest_path, expected_hash, expected_rows in _MANIFESTS:
        raw = files.get(manifest_path)
        if type(raw) is not bytes or sha256_hex(raw) != expected_hash:
            raise AuthenticationError("design manifest differs in the immutable snapshot")
        try:
            rows = parse_hash_manifest(raw, expected_rows=expected_rows)
        except CanonicalError as error:
            raise AuthenticationError(str(error)) from error
        expected_paths.add(manifest_path)
        for digest, target in rows:
            target_raw = files.get(target)
            if type(target_raw) is not bytes or sha256_hex(target_raw) != digest:
                raise AuthenticationError("design target differs in the immutable snapshot")
            expected_paths.add(target)
    for path, digest in (_REVIEW, _DECISION):
        raw = files.get(path)
        if type(raw) is not bytes or sha256_hex(raw) != digest:
            raise AuthenticationError("review or CONTROL decision differs in the immutable snapshot")
        expected_paths.add(path)
    if set(files) != expected_paths:
        raise AuthenticationError("design closure snapshot contains an extra or missing path")
    return _design_snapshot_sha256(snapshot)


def _authenticate_design(root: Path) -> tuple[tuple[str, bytes], ...]:
    files: dict[str, bytes] = {}
    for manifest_path, expected_hash, expected_rows in _MANIFESTS:
        raw = read_exact(_repo_file(root, manifest_path), maximum_bytes=1024 * 1024)
        if sha256_hex(raw) != expected_hash:
            raise AuthenticationError("design manifest differs from its v0.6 pin")
        try:
            rows = parse_hash_manifest(raw, expected_rows=expected_rows)
        except CanonicalError as error:
            raise AuthenticationError(str(error)) from error
        files[manifest_path] = raw
        for digest, target in rows:
            target_raw = read_exact(_repo_file(root, target), maximum_bytes=32 * 1024 * 1024)
            if sha256_hex(target_raw) != digest:
                raise AuthenticationError("design target differs from its authenticated manifest")
            prior = files.get(target)
            if prior is not None and prior != target_raw:
                raise AuthenticationError("authenticated design path collision")
            files[target] = target_raw
    for path, digest in (_REVIEW, _DECISION):
        raw = read_exact(_repo_file(root, path), maximum_bytes=4 * 1024 * 1024)
        if sha256_hex(raw) != digest:
            raise AuthenticationError("review or CONTROL decision differs from its v0.6 pin")
        files[path] = raw
    snapshot = tuple(sorted(files.items()))
    _validate_design_snapshot(snapshot)
    return snapshot


def _mapping(value: object, label: str) -> dict[str, object]:
    if type(value) is not dict:
        raise AuthenticationError(f"{label} is not an exact object")
    return value


def _pin_from_row(row: object) -> ArtifactPin:
    value = _mapping(row, "pin row")
    return ArtifactPin(
        value.get("pin_id"), value.get("project"), value.get("version"),
        value.get("filename"), value.get("size"), value.get("sha256"),
        value.get("url"), value.get("tag"), value.get("dist_info_dir"),
    )


def _authenticate_evidence_raw(raw: object) -> tuple[ArtifactPin, ...]:
    if type(raw) is not bytes:
        raise AuthenticationError("external evidence snapshot type differs")
    if len(raw) != _EVIDENCE_SIZE or sha256_hex(raw) != _EVIDENCE_SHA256:
        raise AuthenticationError("external evidence manifest differs from its frozen size/hash")
    try:
        value = strict_json(raw)
        if jcs_lf(value) != raw:
            raise AuthenticationError("external evidence manifest is not canonical JCS+LF")
    except CanonicalError as error:
        raise AuthenticationError(str(error)) from error
    root_value = _mapping(value, "evidence manifest")
    if root_value.get("schema_id") != "S0-EXTERNAL-ARTIFACT-AUTHORITY-ACQUISITION-V0.1-EVIDENCE-MANIFEST-1":
        raise AuthenticationError("external evidence schema differs")
    pin_authority = _mapping(root_value.get("pin_authority"), "pin authority")
    artifact_rows = pin_authority.get("artifact_pins")
    wheel_rows = pin_authority.get("wheel_pins")
    if type(artifact_rows) is not list or len(artifact_rows) != 2 or type(wheel_rows) is not list or len(wheel_rows) != 6:
        raise AuthenticationError("external pin inventory differs")
    cpython_row = _mapping(artifact_rows[0], "CPython pin")
    cpython = ArtifactPin(
        cpython_row.get("artifact_id"), "cpython", "3.12.10",
        cpython_row.get("filename"), cpython_row.get("size"), cpython_row.get("sha256"),
        cpython_row.get("url"), "cp312-win_amd64", "",
    )
    if cpython_row.get("authority_state") != "PINNED-SOURCE-INPUT":
        raise AuthenticationError("CPython pin authority state differs")
    second = _mapping(artifact_rows[1], "non-runtime artifact pin")
    if second.get("artifact_id") != "vs-build-tools-17.14.39-17.14.37614.0" or second.get("authority_state") != "EXPECTED-PROPOSAL-ONLY":
        raise AuthenticationError("external artifact inventory order differs")
    pins = (cpython, *(_pin_from_row(row) for row in wheel_rows))
    if pins != _EXPECTED_PINS:
        raise AuthenticationError("runtime pin fields or order differ")
    closure = _mapping(root_value.get("dependency_closure"), "dependency closure")
    graph = closure.get("graph")
    graph_order = (
        "jsonschema-4.26.0-py3-none-any",
        "jsonschema-specifications-2025.9.1-py3-none-any",
        "referencing-0.37.0-py3-none-any",
        "attrs-26.1.0-py3-none-any",
        "rpds-py-2026.6.3-cp312-cp312-win_amd64",
        "typing-extensions-4.16.0-py3-none-any",
    )
    if closure.get("extras_selected") is not False or type(graph) is not list or tuple(_mapping(row, "dependency graph row").get("pin_id") for row in graph) != graph_order:
        raise AuthenticationError("six-project dependency closure differs")
    if pins[5].tag != "cp312-cp312-win_amd64":
        raise AuthenticationError("rpds wheel ABI/platform tag differs")
    return pins


def _authenticate_evidence(root: Path) -> tuple[bytes, tuple[ArtifactPin, ...]]:
    raw = read_exact(_repo_file(root, _EVIDENCE_PATH), maximum_bytes=_EVIDENCE_SIZE)
    return raw, _authenticate_evidence_raw(raw)


def _authority_lifecycle() -> tuple[object, object]:
    authority_type = _ActivatedAuthority
    pin_type = ArtifactPin
    expected_pins = _EXPECTED_PINS
    expected_manifest_hashes = tuple(row[1] for row in _MANIFESTS)
    issued: weakref.WeakKeyDictionary[object, tuple[object, ...]] = weakref.WeakKeyDictionary()
    lock = threading.RLock()

    def validate(authority: object) -> None:
        if type(authority) is not authority_type:
            raise AuthenticationError("authority exact type differs")
        with lock:
            registration = issued.get(authority)
        if registration is None:
            raise AuthenticationError("authority was not issued by repository activation")
        design_snapshot, design_digest, evidence_snapshot, pin_snapshot, rows, manifest_hashes = registration
        try:
            private_design = object.__getattribute__(authority, "_design_snapshot")
            private_digest = object.__getattribute__(authority, "_design_snapshot_sha256")
            private_evidence = object.__getattribute__(authority, "_evidence_snapshot")
            private_pins = object.__getattribute__(authority, "_pin_snapshot")
            public_rows = object.__getattribute__(authority, "design_rows")
            public_hashes = object.__getattribute__(authority, "design_manifest_hashes")
            public_evidence = object.__getattribute__(authority, "evidence_raw")
            public_pins = object.__getattribute__(authority, "pins")
        except (AttributeError, TypeError) as error:
            raise AuthenticationError("authority snapshot fields are incomplete") from error
        if (
            private_design is not design_snapshot
            or private_digest is not design_digest
            or private_evidence is not evidence_snapshot
            or private_pins is not pin_snapshot
            or public_rows is not rows
            or public_hashes is not manifest_hashes
            or public_evidence is not evidence_snapshot
            or public_pins is not pin_snapshot
        ):
            raise AuthenticationError("authority snapshot identity was rebound")
        if _validate_design_snapshot(private_design) != private_digest:
            raise AuthenticationError("authority design snapshot digest differs")
        derived_pins = _authenticate_evidence_raw(private_evidence)
        if (
            type(private_pins) is not tuple
            or private_pins != expected_pins
            or derived_pins != private_pins
            or any(type(pin) is not pin_type for pin in private_pins)
            or type(public_rows) is not tuple
            or public_rows != tuple((path, len(raw), sha256_hex(raw)) for path, raw in private_design)
            or type(public_hashes) is not tuple
            or public_hashes != expected_manifest_hashes
        ):
            raise AuthenticationError("authority public/private closure differs")

    def issue(design_snapshot: object, evidence_snapshot: object, pins: object) -> _ActivatedAuthority:
        design_digest = _validate_design_snapshot(design_snapshot)
        derived_pins = _authenticate_evidence_raw(evidence_snapshot)
        if type(pins) is not tuple or pins != expected_pins or derived_pins != pins or any(type(pin) is not pin_type for pin in pins):
            raise AuthenticationError("authority issuance pins differ")
        rows = tuple((path, len(raw), sha256_hex(raw)) for path, raw in design_snapshot)
        authority = object.__new__(authority_type)
        object.__setattr__(authority, "_design_snapshot", design_snapshot)
        object.__setattr__(authority, "_design_snapshot_sha256", design_digest)
        object.__setattr__(authority, "_evidence_snapshot", evidence_snapshot)
        object.__setattr__(authority, "_pin_snapshot", pins)
        object.__setattr__(authority, "design_rows", rows)
        object.__setattr__(authority, "design_manifest_hashes", expected_manifest_hashes)
        object.__setattr__(authority, "evidence_raw", evidence_snapshot)
        object.__setattr__(authority, "pins", pins)
        with lock:
            issued[authority] = (design_snapshot, design_digest, evidence_snapshot, pins, rows, expected_manifest_hashes)
        validate(authority)
        return authority

    return issue, validate


_issue_authority, _validate_issued_authority = _authority_lifecycle()


def activate_repository_authority(repository_root: str) -> _ActivatedAuthority:
    """Authenticate every input before any output, cache, or network action."""

    if type(repository_root) is not str or not repository_root:
        raise AuthenticationError("repository root must be exact nonempty text")
    root = Path(repository_root).resolve(strict=True)
    if not root.is_dir():
        raise AuthenticationError("repository root is not a directory")
    design_rows = _authenticate_design(root)
    evidence_raw, pins = _authenticate_evidence(root)
    return _issue_authority(design_rows, evidence_raw, pins)


def authority_record(authority: object) -> dict[str, object]:
    _validate_issued_authority(authority)
    return {
        "design_file_count": len(authority.design_rows),
        "design_manifest_sha256": list(authority.design_manifest_hashes),
        "effective_mutation_row_count": 115,
        "effective_relations_sha256": _RELATION_SHA256,
        "external_evidence_manifest_sha256": _EVIDENCE_SHA256,
        "external_evidence_manifest_size": _EVIDENCE_SIZE,
        "runtime_pin_count": len(authority.pins),
        "publication_policy_authority": {
            "active_policy_id": "python-os-rename-windows-no-replace-v0.7",
            "caller_selected": False,
            "historical_special_api_policy_active": False,
            "scope": "build-runtime-materialization-v0.7-only",
            "supersession_authority": "explicit-user-proceed-plus-CONTROL-v0.7-supersession",
        },
        "runtime_pins": [
            {
                "filename": pin.filename,
                "pin_id": pin.pin_id,
                "sha256": pin.sha256,
                "size": pin.size,
                "url": pin.url,
            }
            for pin in authority.pins
        ],
    }

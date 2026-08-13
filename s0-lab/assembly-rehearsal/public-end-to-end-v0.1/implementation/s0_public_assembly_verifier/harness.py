"""Authenticated parent/child harness for the bounded public candidate.

The diagnostic entry point can exercise the process and publication predicates
with a test backend, but its return type is deliberately not live acceptance.
Only :func:`run_live_public_candidate` constructs the exact Win32 backend and
can return ``LiveDecision``.  Neither entry point is an S0 runner.
"""

from __future__ import annotations

import hashlib
import json
import os
import queue
import stat
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import BinaryIO, Callable, Mapping

from .consumer import (
    DiagnosticPredicateDecision,
    LiveDecision,
    _exercise_consumer_predicates_for_tests,
)
from .errors import auth_failure
from .integrity import (
    COMPONENT_MANIFESTS,
    DESIGN_REVIEW_PATH,
    parse_manifest,
    read_exact_public_file,
    verify_v0_5_design_authority,
)
from .observer import PublicationBackend, PublicationObserver
from .pins import ExternalPins
from .source_audit import audit_candidate_source, audit_win32_source


ASSEMBLY_ROOT = "s0-lab/assembly-rehearsal/public-end-to-end-v0.1"
IMPLEMENTATION_MANIFEST_PATH = f"{ASSEMBLY_ROOT}/verification/implementation-files.sha256"
IMPLEMENTATION_ROOT = f"{ASSEMBLY_ROOT}/implementation"
CANDIDATE_ROOT = f"{IMPLEMENTATION_ROOT}/s0_public_assembly_candidate"
VERIFIER_ROOT = f"{IMPLEMENTATION_ROOT}/s0_public_assembly_verifier"
BOOTSTRAP_PATH = f"{IMPLEMENTATION_ROOT}/s0_public_assembly_child_bootstrap.py"

PUBLIC_BUNDLE_MANIFEST_PATH = "s0-lab/public-practice/v0.1/bundle-files.sha256"
PUBLIC_BUNDLE_MANIFEST_SHA256 = (
    "e41ee6c71169df646e3c8c0b0e8f3d77e7871d939f651b86a52ea5696feeb637"
)
PUBLIC_BUNDLE_ROOT = "s0-lab/public-practice/v0.1"
PUBLIC_BUNDLE_ENTRY_COUNT = 90

# Frozen child import closures.  The parent reviews the full component
# manifests, but the child may open only these exact source modules.
_COMPONENT_CHILD_CLOSURES = (
    (
        "s0-lab/i0/implementation/s0_i0/__init__.py",
        "s0-lab/i0/implementation/s0_i0/answer_validation.py",
        "s0-lab/i0/implementation/s0_i0/authentication.py",
        "s0-lab/i0/implementation/s0_i0/integrity.py",
        "s0-lab/i0/implementation/s0_i0/json_validation.py",
        "s0-lab/i0/implementation/s0_i0/paths.py",
        "s0-lab/i0/implementation/s0_i0/transform.py",
    ),
    (
        "s0-lab/i1/implementation/s0_i1/__init__.py",
        "s0-lab/i1/implementation/s0_i1/auth.py",
        "s0-lab/i1/implementation/s0_i1/canonical.py",
        "s0-lab/i1/implementation/s0_i1/errors.py",
        "s0-lab/i1/implementation/s0_i1/json_bytes.py",
        "s0-lab/i1/implementation/s0_i1/runner.py",
        "s0-lab/i1/implementation/s0_i1/topology.py",
    ),
    (
        "s0-lab/i2/implementation/s0_i2/__init__.py",
        "s0-lab/i2/implementation/s0_i2/canonical.py",
        "s0-lab/i2/implementation/s0_i2/contract.py",
        "s0-lab/i2/implementation/s0_i2/errors.py",
        "s0-lab/i2/implementation/s0_i2/records.py",
        "s0-lab/i2/implementation/s0_i2/vectors.py",
        "s0-lab/i2/implementation/s0_i2/lifecycle.py",
    ),
    (
        "s0-lab/i3/implementation/s0_i3/__init__.py",
        "s0-lab/i3/implementation/s0_i3/boundaries.py",
        "s0-lab/i3/implementation/s0_i3/classifier.py",
        "s0-lab/i3/implementation/s0_i3/contract.py",
        "s0-lab/i3/implementation/s0_i3/errors.py",
        "s0-lab/i3/implementation/s0_i3/models.py",
        "s0-lab/i3/implementation/s0_i3/records.py",
        "s0-lab/i3/implementation/s0_i3/finalizer.py",
    ),
)

_FIXED_CHILD_INPUTS = (
    (
        f"{ASSEMBLY_ROOT}/request-files.sha256",
        "872f2bca8d2d56c9b664e37ad6092a4dd4d8750d40eb8ba99dfbad7f7c94c9f7",
    ),
    (
        f"{ASSEMBLY_ROOT}/inputs/request.json",
        "990f12bd98b0f2c7ce64e683a8165c6e67384d6dbc6b4f1f4ec62b19f28b75e2",
    ),
    (
        "s0-lab/control/sm0/answer.schema.json",
        "e21100f06d2715f42cd1fda812e17d22340a64327bfb48c03112a0f83d33ac6b",
    ),
    (
        "s0-lab/i2/spec/trust-root-role-isolation-contract-v0.4.json",
        "713fc6b44c84126387dc492b93e22d928ba894e18bdc8705049a2ea5cb8cc7da",
    ),
    (
        "s0-lab/i3/spec/import-decision-contract-v0.1.json",
        "ae834becfc393e4f525265aff473ae32d12f349713fb48b2e0bb60ea39fc7ac8",
    ),
)

_PUBLISH_RECORD = b"PUBLISH_RECORD\n"
_PUBLISH_RECEIPT = b"PUBLISH_RECEIPT\n"
_PUBLISH_OK = b"OK\n"
_MAX_FRAME = max(len(_PUBLISH_RECORD), len(_PUBLISH_RECEIPT)) + 1
_MAX_CONFIG = 1_048_576
_DIAGNOSTIC_KEYS = {
    "cause_label",
    "cleanup_status",
    "failed_operation",
    "observed_transport_calls",
    "offline_status",
    "output_root_status",
    "primary_class",
    "rehearsal_pass",
    "schema_id",
    "state_at_failure",
}


class HarnessFailure(RuntimeError):
    """Stable parent-harness failure without child stderr disclosure."""

    def __init__(self, label: str, *, quarantined: bool) -> None:
        super().__init__(label)
        self.label = label
        self.quarantined = quarantined


@dataclass(frozen=True)
class AuthenticatedLaunch:
    """Read-only evidence produced before child launch or output mutation."""

    workspace_root: Path
    bootstrap_path: Path
    candidate_root: Path
    external_pins: ExternalPins
    implementation_entry_count: int
    design_entry_count: int
    component_entry_counts: tuple[int, int, int, int]
    public_bundle_entry_count: int
    allowed_read_paths: tuple[str, ...]


@dataclass(frozen=True)
class _CompletedPublication:
    observer: PublicationObserver
    witness: object
    child_identity: object
    parent_pipe_identity: object


def _safe_repo_relative(value: str) -> str:
    if type(value) is not str or not value or "\\" in value or "\x00" in value:
        raise auth_failure("public path is not canonical POSIX-relative text")
    pure = PurePosixPath(value)
    if pure.is_absolute() or any(part in {"", ".", ".."} or ":" in part for part in pure.parts):
        raise auth_failure("public path escapes its authenticated namespace")
    return value


def _workspace_path(workspace_root: Path, relative: str) -> Path:
    relative = _safe_repo_relative(relative)
    root = workspace_root.resolve(strict=True)
    candidate = root.joinpath(*PurePosixPath(relative).parts)
    try:
        resolved = candidate.resolve(strict=True)
        resolved.relative_to(root)
    except (OSError, ValueError) as exc:
        raise auth_failure("required public implementation path is unavailable") from exc
    if resolved != candidate or not candidate.is_file() or candidate.is_symlink():
        raise auth_failure("required public implementation path is not an exact file")
    return candidate


def _authenticate_scoped_manifest(
    workspace_root: Path,
    *,
    manifest_path: str,
    manifest_sha256: str,
    allowed_prefix: str,
) -> Mapping[str, str]:
    """Authenticate a repo-relative manifest without following out-of-scope rows."""

    raw = read_exact_public_file(workspace_root, manifest_path, manifest_sha256)
    entries = parse_manifest(raw)
    prefix = _safe_repo_relative(allowed_prefix).rstrip("/") + "/"
    for relative in entries:
        if not relative.startswith(prefix):
            raise auth_failure("manifest row is outside its public implementation namespace")
    for relative, digest in entries.items():
        read_exact_public_file(workspace_root, relative, digest)
    return entries


def _relative_source_inventory(workspace_root: Path, source_root: Path) -> tuple[str, ...]:
    root = workspace_root.resolve(strict=True)
    inventory: list[str] = []
    for path in sorted(source_root.rglob("*.py")):
        if not path.is_file() or path.is_symlink():
            raise auth_failure("implementation source inventory contains an invalid path")
        try:
            relative = path.resolve(strict=True).relative_to(root).as_posix()
        except (OSError, ValueError) as exc:
            raise auth_failure("implementation source escapes the public workspace") from exc
        inventory.append(relative)
    if not inventory:
        raise auth_failure("implementation source inventory is empty")
    return tuple(inventory)


def _authenticate_component_rows(workspace_root: Path) -> tuple[tuple[int, int, int, int], set[str]]:
    counts: list[int] = []
    child_allowed: set[str] = set()
    for index, (manifest_path, digest, row_base, rows_are_repo_relative) in enumerate(
        COMPONENT_MANIFESTS
    ):
        raw = read_exact_public_file(workspace_root, manifest_path, digest)
        entries = parse_manifest(raw)
        component_prefix = f"s0-lab/i{index}/"
        targets: list[tuple[str, str]] = []
        for relative, row_digest in entries.items():
            target = relative if rows_are_repo_relative else f"{row_base}/{relative}"
            if not target.startswith(component_prefix):
                raise auth_failure("component manifest row escapes its public component")
            targets.append((target, row_digest))
        for target, row_digest in targets:
            read_exact_public_file(workspace_root, target, row_digest)
        closure = set(_COMPONENT_CHILD_CLOSURES[index])
        if not closure.issubset(dict(targets)):
            raise auth_failure("child component closure is not authenticated by its manifest")
        child_allowed.update(closure)
        child_allowed.add(manifest_path)
        counts.append(len(entries))
    if len(counts) != 4:
        raise auth_failure("component implementation inventory is incomplete")
    return (counts[0], counts[1], counts[2], counts[3]), child_allowed


def _authenticate_public_bundle(workspace_root: Path) -> set[str]:
    raw = read_exact_public_file(
        workspace_root,
        PUBLIC_BUNDLE_MANIFEST_PATH,
        PUBLIC_BUNDLE_MANIFEST_SHA256,
    )
    entries = parse_manifest(raw)
    if len(entries) != PUBLIC_BUNDLE_ENTRY_COUNT:
        raise auth_failure("public bundle manifest entry count mismatch")
    targets: list[tuple[str, str]] = []
    for relative, digest in entries.items():
        relative = _safe_repo_relative(relative)
        target = f"{PUBLIC_BUNDLE_ROOT}/{relative}"
        if not target.startswith(PUBLIC_BUNDLE_ROOT + "/"):
            raise auth_failure("public bundle row escapes its fixed bundle root")
        targets.append((target, digest))
    for target, digest in targets:
        read_exact_public_file(workspace_root, target, digest)
    return {PUBLIC_BUNDLE_MANIFEST_PATH, *(target for target, _ in targets)}


def authenticate_public_launch(
    *,
    workspace_root: Path,
    implementation_manifest_sha256: str,
) -> AuthenticatedLaunch:
    """Complete all parent authentication and source audits before launch."""

    if not isinstance(workspace_root, Path):
        raise auth_failure("workspace root must be pathlib.Path")
    try:
        root = workspace_root.resolve(strict=True)
    except OSError as exc:
        raise auth_failure("workspace root is unavailable") from exc
    if root != workspace_root.absolute() or not root.is_dir() or root.is_symlink():
        raise auth_failure("workspace root is not one exact public directory")

    external_pins = ExternalPins(
        assembly_implementation_manifest_sha256=implementation_manifest_sha256,
        design_package_manifest_sha256=(
            "6292e322549c79f539b57c1087fd722c5cca96318c45d89fac5343247c429802"
        ),
        design_independent_review_sha256=(
            "7c629c9c4aed5c2e36598e4ad08e4819fa06b73f3f77bf9e7d19714f61b35137"
        ),
    )

    implementation_entries = _authenticate_scoped_manifest(
        root,
        manifest_path=IMPLEMENTATION_MANIFEST_PATH,
        manifest_sha256=implementation_manifest_sha256,
        allowed_prefix=ASSEMBLY_ROOT,
    )

    # These reads authenticate the frozen v0.5 design package and independent
    # rereview before any candidate module is imported or output is touched.
    design_entries = verify_v0_5_design_authority(root)
    read_exact_public_file(
        root,
        DESIGN_REVIEW_PATH,
        external_pins.design_independent_review_sha256,
    )
    component_counts, component_allowed = _authenticate_component_rows(root)
    bundle_allowed = _authenticate_public_bundle(root)

    candidate_root = root.joinpath(*PurePosixPath(CANDIDATE_ROOT).parts)
    verifier_root = root.joinpath(*PurePosixPath(VERIFIER_ROOT).parts)
    bootstrap_path = _workspace_path(root, BOOTSTRAP_PATH)
    candidate_sources = _relative_source_inventory(root, candidate_root)
    verifier_sources = _relative_source_inventory(root, verifier_root)
    required_implementation = set(candidate_sources) | set(verifier_sources) | {BOOTSTRAP_PATH}
    if not required_implementation.issubset(implementation_entries):
        raise auth_failure("implementation manifest omits a required authenticated source")

    # Static authority split and exact Win32 ABI are audited while the
    # candidate is still merely authenticated text.
    audit_candidate_source(candidate_root)
    audit_win32_source(verifier_root / "win32.py")

    allowed: set[str] = set(candidate_sources)
    allowed.update(component_allowed)
    allowed.update(bundle_allowed)
    for relative, digest in _FIXED_CHILD_INPUTS:
        read_exact_public_file(root, relative, digest)
        allowed.add(relative)

    return AuthenticatedLaunch(
        workspace_root=root,
        bootstrap_path=bootstrap_path,
        candidate_root=candidate_root,
        external_pins=external_pins,
        implementation_entry_count=len(implementation_entries),
        design_entry_count=len(design_entries),
        component_entry_counts=component_counts,
        public_bundle_entry_count=PUBLIC_BUNDLE_ENTRY_COUNT,
        allowed_read_paths=tuple(sorted(allowed)),
    )


def _create_fresh_output_root(output_root: Path) -> Path:
    """Create and own one previously absent leaf directory, exactly once."""

    if not isinstance(output_root, Path) or not output_root.is_absolute():
        raise auth_failure("output root must be one absolute pathlib.Path")
    if output_root.exists() or output_root.is_symlink():
        raise auth_failure("output root must be absent before parent reservation")
    parent = output_root.parent
    try:
        parent_info = os.lstat(parent)
        resolved_parent = parent.resolve(strict=True)
    except OSError as exc:
        raise auth_failure("output-root parent is unavailable") from exc
    reparse = bool(
        getattr(parent_info, "st_file_attributes", 0)
        & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    )
    if (
        resolved_parent != parent.absolute()
        or not stat.S_ISDIR(parent_info.st_mode)
        or stat.S_ISLNK(parent_info.st_mode)
        or reparse
    ):
        raise auth_failure("output-root parent is not one regular non-reparse directory")
    try:
        os.mkdir(output_root, 0o700)
    except OSError as exc:
        raise auth_failure("exclusive output-root creation failed") from exc
    root = output_root.resolve(strict=True)
    if root != output_root.absolute() or root.is_symlink():
        raise auth_failure("created output root is not exact")
    return root


def _canonical_child_config(
    launch: AuthenticatedLaunch,
    output_root: Path,
) -> bytes:
    value: dict[str, object] = {
        "allowed_read_paths": list(launch.allowed_read_paths),
        "assembly_implementation_manifest_sha256": (
            launch.external_pins.assembly_implementation_manifest_sha256
        ),
        "candidate_root": CANDIDATE_ROOT,
        "design_independent_review_sha256": (
            launch.external_pins.design_independent_review_sha256
        ),
        "design_package_manifest_sha256": (
            launch.external_pins.design_package_manifest_sha256
        ),
        "output_root": str(output_root),
        "schema_id": "S0-PUBLIC-ASSEMBLY-CHILD-CONFIG-1",
        "workspace_root": str(launch.workspace_root),
    }
    raw = (
        json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("ascii")
    if len(raw) > _MAX_CONFIG:
        raise auth_failure("canonical child configuration exceeds its fixed bound")
    return raw


def _child_command(python_executable: Path, bootstrap_path: Path) -> tuple[str, ...]:
    try:
        executable = python_executable.resolve(strict=True)
    except OSError as exc:
        raise auth_failure("child Python executable is unavailable") from exc
    if not executable.is_file():
        raise auth_failure("child Python executable is not a regular file")
    return (str(executable), "-I", "-S", "-B", str(bootstrap_path))


def _minimal_child_environment() -> dict[str, str]:
    allowed = ("SYSTEMROOT", "WINDIR", "SYSTEMDRIVE", "TEMP", "TMP")
    return {name: os.environ[name] for name in allowed if name in os.environ}


def _remaining(deadline: float) -> float:
    value = deadline - time.monotonic()
    if value <= 0:
        raise TimeoutError("child process deadline expired")
    return value


def _readline_bounded(stream: BinaryIO, *, deadline: float) -> bytes:
    result: queue.Queue[object] = queue.Queue(maxsize=1)

    def read() -> None:
        try:
            result.put(stream.readline(_MAX_FRAME))
        except BaseException as exc:  # passed back to the controlling thread
            result.put(exc)

    thread = threading.Thread(target=read, name="s0-public-child-stdout", daemon=True)
    thread.start()
    try:
        value = result.get(timeout=_remaining(deadline))
    except queue.Empty as exc:
        raise TimeoutError("child publication request timed out") from exc
    if isinstance(value, BaseException):
        raise value
    if type(value) is not bytes or not value or not value.endswith(b"\n"):
        raise HarnessFailure("child-publication-frame-partial-or-absent", quarantined=True)
    if len(value) >= _MAX_FRAME:
        raise HarnessFailure("child-publication-frame-exceeds-fixed-bound", quarantined=True)
    return value


def _write_exact(stream: BinaryIO, raw: bytes) -> None:
    written = stream.write(raw)
    if type(written) is not int or written != len(raw):
        raise HarnessFailure("parent-publication-reply-write-was-not-exact", quarantined=True)
    stream.flush()


def _abort_child(process: subprocess.Popen[bytes]) -> None:
    try:
        if process.poll() is None:
            process.kill()
    except OSError:
        pass
    try:
        process.communicate(timeout=2.0)
    except (OSError, subprocess.TimeoutExpired, ValueError):
        pass


def _finish_child(process: subprocess.Popen[bytes], *, deadline: float) -> tuple[bytes, bytes, int]:
    if process.stdin is None:
        raise HarnessFailure("child-stdin-endpoint-is-unavailable", quarantined=True)
    process.stdin.close()
    # Avoid communicate() attempting to flush a stream that was deliberately
    # closed only after the second exact reply.
    process.stdin = None
    try:
        extra_stdout, stderr = process.communicate(timeout=_remaining(deadline))
    except subprocess.TimeoutExpired as exc:
        raise TimeoutError("child did not terminate after the second reply") from exc
    return extra_stdout, stderr, int(process.returncode)


def _parse_child_failure(stderr: bytes) -> tuple[str, int]:
    if type(stderr) is not bytes or not stderr.endswith(b"\n") or len(stderr) > 8192:
        raise HarnessFailure("child-failure-diagnostic-is-not-bounded", quarantined=True)
    try:
        value = json.loads(stderr)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise HarnessFailure("child-failure-diagnostic-is-not-strict-json", quarantined=True) from exc
    if type(value) is not dict or set(value) != _DIAGNOSTIC_KEYS:
        raise HarnessFailure("child-failure-diagnostic-field-set-is-not-exact", quarantined=True)
    canonical = (
        json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("ascii")
    if (
        canonical != stderr
        or value.get("schema_id") != "S0-PUBLIC-ASSEMBLY-FAILURE-DIAGNOSTIC-1"
        or value.get("offline_status") != "offline-not-success-diagnostic-only"
        or value.get("rehearsal_pass") is not False
    ):
        raise HarnessFailure("child-failure-diagnostic-is-not-canonical", quarantined=True)
    failure_class = value.get("primary_class")
    calls = value.get("observed_transport_calls")
    if failure_class not in {
        "AR-BOUNDARY", "AR-AUTH", "AR-TRANSFORM", "AR-RESERVE", "AR-INVOKE",
        "AR-RESPONSE", "AR-ANSWER", "AR-RECORD", "AR-DETERMINISM",
    } or type(calls) is not int or calls not in {0, 1}:
        raise HarnessFailure("child-failure-class-or-call-count-is-invalid", quarantined=True)
    return failure_class, calls


def _classify_child_termination(stderr: bytes, returncode: int) -> None:
    if returncode == 0:
        if stderr:
            raise HarnessFailure("successful-child-stderr-was-not-empty", quarantined=True)
        return
    failure_class, calls = _parse_child_failure(stderr)
    raise HarnessFailure(
        f"authenticated-child-failure:{failure_class}/{calls}",
        quarantined=True,
    )


def _execute_authenticated(
    *,
    launch: AuthenticatedLaunch,
    output_root: Path,
    observer_factory: Callable[[object, object], PublicationObserver],
    python_executable: Path,
    timeout_seconds: float,
) -> _CompletedPublication:
    if type(timeout_seconds) not in {int, float} or timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be positive")
    config = _canonical_child_config(launch, output_root)
    command = _child_command(python_executable, launch.bootstrap_path)
    process = subprocess.Popen(
        command,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=str(launch.workspace_root),
        env=_minimal_child_environment(),
        shell=False,
        close_fds=True,
        bufsize=0,
    )
    pipe_identity = object()
    deadline = time.monotonic() + float(timeout_seconds)
    try:
        if process.stdin is None or process.stdout is None or process.stderr is None:
            raise HarnessFailure("child-pipe-construction-failed", quarantined=True)
        observer = observer_factory(process, pipe_identity)
        _write_exact(process.stdin, config)

        first = _readline_bounded(process.stdout, deadline=deadline)
        if first != _PUBLISH_RECORD:
            raise HarnessFailure("child-first-publication-request-is-not-exact", quarantined=True)
        reply, first_witness = observer.observe_message(
            first,
            child_identity=process,
            parent_pipe_identity=pipe_identity,
        )
        if reply != _PUBLISH_OK or first_witness is not None:
            raise HarnessFailure("record-publication-observer-result-is-invalid", quarantined=True)
        _write_exact(process.stdin, reply)

        second = _readline_bounded(process.stdout, deadline=deadline)
        if second != _PUBLISH_RECEIPT:
            raise HarnessFailure("child-second-publication-request-is-not-exact", quarantined=True)
        reply, witness = observer.observe_message(
            second,
            child_identity=process,
            parent_pipe_identity=pipe_identity,
        )
        if reply != _PUBLISH_OK or witness is None:
            raise HarnessFailure("receipt-publication-observer-result-is-invalid", quarantined=True)
        _write_exact(process.stdin, reply)

        extra_stdout, stderr, returncode = _finish_child(process, deadline=deadline)
        if extra_stdout != b"":
            raise HarnessFailure("child-stdout-contained-an-extra-frame", quarantined=True)
        _classify_child_termination(stderr, returncode)
        return _CompletedPublication(observer, witness, process, pipe_identity)
    except BaseException:
        _abort_child(process)
        raise


def run_diagnostic_public_candidate(
    *,
    workspace_root: Path,
    output_root: Path,
    implementation_manifest_sha256: str,
    backend: PublicationBackend,
    python_executable: Path | None = None,
    timeout_seconds: float = 30.0,
) -> DiagnosticPredicateDecision:
    """Run bounded process predicates with a fake backend; never return PASS."""

    launch = authenticate_public_launch(
        workspace_root=workspace_root,
        implementation_manifest_sha256=implementation_manifest_sha256,
    )
    root = _create_fresh_output_root(output_root)
    if backend.output_root != root:
        raise auth_failure("diagnostic backend is not bound to the exact output root")

    completed = _execute_authenticated(
        launch=launch,
        output_root=root,
        observer_factory=lambda child, pipe: PublicationObserver(
            backend=backend,
            child_identity=child,
            parent_pipe_identity=pipe,
        ),
        python_executable=python_executable or Path(sys.executable),
        timeout_seconds=timeout_seconds,
    )
    return _exercise_consumer_predicates_for_tests(
        workspace_root=launch.workspace_root,
        observer=completed.observer,
        witness=completed.witness,
        child_identity=completed.child_identity,
        parent_pipe_identity=completed.parent_pipe_identity,
        external_pins=launch.external_pins,
        quarantined=False,
    )


def run_live_public_candidate(
    *,
    workspace_root: Path,
    output_root: Path,
    implementation_manifest_sha256: str,
    python_executable: Path | None = None,
    runtime_profile_manifest_sha256: str | None = None,
    timeout_seconds: float = 30.0,
) -> LiveDecision:
    """Run the exact Win32 path; this API is intentionally not used by tests."""

    # v0.5 freezes neither CPython/stdlib bytes nor jsonschema's transitive
    # runtime closure.  Live authority therefore remains fail-closed until a
    # separately reviewed external runtime-profile manifest is admitted.
    if runtime_profile_manifest_sha256 is None:
        raise auth_failure("live runtime profile is not externally authenticated")
    raise auth_failure("no live runtime-profile schema is admitted by the v0.5 design")
    launch = authenticate_public_launch(  # pragma: no cover - future gate only
        workspace_root=workspace_root,
        implementation_manifest_sha256=implementation_manifest_sha256,
    )


def implementation_manifest_sha256(workspace_root: Path) -> str:
    """Hash the public manifest for an external caller; do not self-authorize."""

    path = _workspace_path(workspace_root, IMPLEMENTATION_MANIFEST_PATH)
    return hashlib.sha256(path.read_bytes()).hexdigest()

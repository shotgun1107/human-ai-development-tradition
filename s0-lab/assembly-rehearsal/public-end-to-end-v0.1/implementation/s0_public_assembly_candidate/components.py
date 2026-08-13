"""Delayed loading of the four authenticated public component APIs."""

from __future__ import annotations

import importlib
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from .constants import COMPONENT_MANIFESTS
from .errors import BoundaryViolation
from .storage import StorageError, read_workspace_file, workspace_path


class ComponentError(RuntimeError):
    """A pinned component manifest or required API is unavailable."""


_MANIFEST_LINE = re.compile(rb"^([a-f0-9]{64})  ([^\r\n]+)$")

_REQUIRED_COMPONENT_SOURCE_ROWS = {
    "i0": (
        "implementation/s0_i0/__init__.py",
        "implementation/s0_i0/answer_validation.py",
        "implementation/s0_i0/authentication.py",
        "implementation/s0_i0/integrity.py",
        "implementation/s0_i0/json_validation.py",
        "implementation/s0_i0/paths.py",
        "implementation/s0_i0/transform.py",
    ),
    "i1": (
        "implementation/s0_i1/__init__.py",
        "implementation/s0_i1/auth.py",
        "implementation/s0_i1/canonical.py",
        "implementation/s0_i1/errors.py",
        "implementation/s0_i1/json_bytes.py",
        "implementation/s0_i1/runner.py",
        "implementation/s0_i1/topology.py",
    ),
    "i2": (
        "s0-lab/i2/implementation/s0_i2/__init__.py",
        "s0-lab/i2/implementation/s0_i2/canonical.py",
        "s0-lab/i2/implementation/s0_i2/contract.py",
        "s0-lab/i2/implementation/s0_i2/errors.py",
        "s0-lab/i2/implementation/s0_i2/lifecycle.py",
        "s0-lab/i2/implementation/s0_i2/records.py",
        "s0-lab/i2/implementation/s0_i2/vectors.py",
    ),
    "i3": (
        "s0-lab/i3/implementation/s0_i3/__init__.py",
        "s0-lab/i3/implementation/s0_i3/boundaries.py",
        "s0-lab/i3/implementation/s0_i3/classifier.py",
        "s0-lab/i3/implementation/s0_i3/contract.py",
        "s0-lab/i3/implementation/s0_i3/errors.py",
        "s0-lab/i3/implementation/s0_i3/finalizer.py",
        "s0-lab/i3/implementation/s0_i3/models.py",
        "s0-lab/i3/implementation/s0_i3/records.py",
    ),
}


@dataclass(frozen=True)
class ComponentApis:
    i0_verify_public_bundle: Callable
    i0_transform_canonical: Callable
    i0_validate_answer_candidate_bytes: Callable
    i1_bind_external_manifest_grant: Callable
    i1_load_authenticated_manifest: Callable
    i1_authenticate_manifest_entry: Callable
    i1_run_one_shot: Callable
    i1_response_frame_type: type
    i2_verify_contract_file: Callable
    i3_verify_contract_file: Callable


def authenticate_component_manifests(workspace_root: Path) -> None:
    for component, (relative, digest) in sorted(COMPONENT_MANIFESTS.items()):
        raw = read_workspace_file(
            workspace_root,
            relative,
            expected_sha256=digest,
        )
        if raw.startswith(b"\xef\xbb\xbf") or b"\r" in raw or not raw.endswith(b"\n"):
            raise ComponentError("component manifest text form is noncanonical")
        rows: dict[str, str] = {}
        for line in raw[:-1].split(b"\n"):
            match = _MANIFEST_LINE.fullmatch(line)
            if match is None:
                raise ComponentError("component manifest row is noncanonical")
            try:
                row_digest = match.group(1).decode("ascii")
                row_path = match.group(2).decode("ascii")
            except UnicodeDecodeError as exc:
                raise ComponentError("component manifest row is not ASCII") from exc
            if row_path in rows:
                raise ComponentError("component manifest path is duplicated")
            rows[row_path] = row_digest
        required_rows = _REQUIRED_COMPONENT_SOURCE_ROWS.get(component)
        if required_rows is None or any(row not in rows for row in required_rows):
            raise ComponentError("component manifest omits a required API source")
        for row_path in required_rows:
            row_digest = rows[row_path]
            if component in {"i0", "i1"}:
                source_path = f"s0-lab/{component}/{row_path}"
            else:
                source_path = row_path
            read_workspace_file(
                workspace_root,
                source_path,
                expected_sha256=row_digest,
            )


def _required_callable(module: object, name: str) -> Callable:
    value = getattr(module, name, None)
    if not callable(value):
        raise ComponentError("required public component API is unavailable")
    return value


def _required_type(module: object, name: str) -> type:
    value = getattr(module, name, None)
    if type(value) is not type:
        raise ComponentError("required public component type is unavailable")
    return value


def load_component_apis(workspace_root: Path) -> ComponentApis:
    """Authenticate manifest anchors, then import only the required public APIs."""

    try:
        authenticate_component_manifests(workspace_root)
        implementation_roots = [
            workspace_path(workspace_root, f"s0-lab/{name}/implementation")
            for name in ("i0", "i1", "i2", "i3")
        ]
    except StorageError as exc:
        raise ComponentError("component manifest authentication failed") from exc

    for root in reversed(implementation_roots):
        value = str(root)
        if value not in sys.path:
            sys.path.insert(0, value)
    for name in ("s0_i0", "s0_i1", "s0_i2", "s0_i3"):
        if name in sys.modules or any(key.startswith(name + ".") for key in sys.modules):
            raise ComponentError("public component module was preloaded before authentication")
    try:
        i0 = importlib.import_module("s0_i0")
        i1_auth = importlib.import_module("s0_i1.auth")
        i1_runner = importlib.import_module("s0_i1.runner")
        i2_contract = importlib.import_module("s0_i2.contract")
        i3_contract = importlib.import_module("s0_i3.contract")
    except BoundaryViolation:
        raise
    except Exception as exc:
        raise ComponentError("public component import failed") from exc

    return ComponentApis(
        i0_verify_public_bundle=_required_callable(i0, "verify_public_bundle"),
        i0_transform_canonical=_required_callable(i0, "transform_canonical"),
        i0_validate_answer_candidate_bytes=_required_callable(
            i0, "validate_answer_candidate_bytes"
        ),
        i1_bind_external_manifest_grant=_required_callable(
            i1_auth, "bind_external_manifest_grant"
        ),
        i1_load_authenticated_manifest=_required_callable(
            i1_auth, "load_authenticated_manifest"
        ),
        i1_authenticate_manifest_entry=_required_callable(
            i1_auth, "authenticate_manifest_entry"
        ),
        i1_run_one_shot=_required_callable(i1_runner, "run_one_shot"),
        i1_response_frame_type=_required_type(i1_runner, "ResponseFrame"),
        i2_verify_contract_file=_required_callable(i2_contract, "verify_contract_file"),
        i3_verify_contract_file=_required_callable(i3_contract, "verify_contract_file"),
    )

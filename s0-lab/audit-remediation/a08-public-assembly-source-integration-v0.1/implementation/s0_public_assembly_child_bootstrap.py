"""Standalone isolated child bootstrap for the bounded public candidate.

Only Python's standard library is imported before the single canonical config
frame is received.  Candidate and component modules are then loaded from the
parent-authenticated, exact source allowlist through a source-only loader.
"""

from __future__ import annotations

# Preload the fixed standard-library surface before the candidate open sentinel
# is installed.  The child is launched with -I -S -B, so none of these imports
# are selected from the workspace or ambient site packages.
import ast
import copy
import hashlib
import importlib
import importlib.abc
import importlib.metadata
import importlib.util
import json
import math
import os
import platform
import re
import stat
import sys
import unicodedata
from collections.abc import Callable, Iterator, Mapping, Sequence
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path, PurePath, PurePosixPath
from types import MappingProxyType
from typing import Any, BinaryIO, Iterable, NoReturn, Protocol


_CONFIG_SCHEMA = "S0-PUBLIC-ASSEMBLY-CHILD-CONFIG-1"
_MAX_CONFIG = 1_048_576
_CANDIDATE_ROOT = (
    "s0-lab/assembly-rehearsal/public-end-to-end-v0.1/implementation/"
    "s0_public_assembly_candidate"
)
_CONFIG_KEYS = {
    "allowed_read_paths",
    "assembly_implementation_manifest_sha256",
    "candidate_root",
    "design_independent_review_sha256",
    "design_package_manifest_sha256",
    "output_root",
    "schema_id",
    "workspace_root",
}
_LOWER_SHA256 = re.compile(r"^[0-9a-f]{64}$")


class _BootstrapFailure(RuntimeError):
    pass


def _object_no_duplicates(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise _BootstrapFailure("duplicate config key")
        result[key] = value
    return result


def _canonical_config() -> dict[str, object]:
    raw = sys.stdin.buffer.readline(_MAX_CONFIG + 1)
    if not raw or len(raw) > _MAX_CONFIG or not raw.endswith(b"\n"):
        raise _BootstrapFailure("config frame is partial, absent, or oversized")
    try:
        value = json.loads(raw, object_pairs_hook=_object_no_duplicates)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise _BootstrapFailure("config frame is not strict JSON") from exc
    if type(value) is not dict or set(value) != _CONFIG_KEYS:
        raise _BootstrapFailure("config field set is not exact")
    canonical = (
        json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
        + "\n"
    ).encode("ascii")
    if canonical != raw:
        raise _BootstrapFailure("config frame is not canonical ASCII JSON")
    if value["schema_id"] != _CONFIG_SCHEMA or value["candidate_root"] != _CANDIDATE_ROOT:
        raise _BootstrapFailure("config schema or candidate root is not exact")
    for key in (
        "assembly_implementation_manifest_sha256",
        "design_independent_review_sha256",
        "design_package_manifest_sha256",
    ):
        digest = value[key]
        if type(digest) is not str or _LOWER_SHA256.fullmatch(digest) is None:
            raise _BootstrapFailure("config contains a malformed external pin")
    return value


def _absolute_directory(value: object, label: str) -> Path:
    if type(value) is not str or not value or "\x00" in value:
        raise _BootstrapFailure(f"{label} is not one path string")
    path = Path(value)
    if not path.is_absolute():
        raise _BootstrapFailure(f"{label} is not absolute")
    try:
        resolved = path.resolve(strict=True)
    except OSError as exc:
        raise _BootstrapFailure(f"{label} is unavailable") from exc
    if resolved != path.absolute() or not resolved.is_dir() or resolved.is_symlink():
        raise _BootstrapFailure(f"{label} is not one exact directory")
    return resolved


def _safe_relative(value: object) -> str:
    if type(value) is not str or not value or "\\" in value or "\x00" in value:
        raise _BootstrapFailure("allowlist path is not canonical POSIX text")
    pure = PurePosixPath(value)
    if pure.is_absolute() or any(part in {"", ".", ".."} or ":" in part for part in pure.parts):
        raise _BootstrapFailure("allowlist path escapes the workspace")
    return value


def _authenticated_paths(
    workspace_root: Path,
    values: object,
) -> tuple[tuple[str, ...], frozenset[Path]]:
    if type(values) is not list or not values:
        raise _BootstrapFailure("allowlist is not one nonempty array")
    relative = tuple(_safe_relative(value) for value in values)
    if list(relative) != sorted(set(relative)):
        raise _BootstrapFailure("allowlist is not sorted and unique")
    absolute: set[Path] = set()
    for item in relative:
        lexical = workspace_root.joinpath(*PurePosixPath(item).parts)
        try:
            resolved = lexical.resolve(strict=True)
            resolved.relative_to(workspace_root)
        except (OSError, ValueError) as exc:
            raise _BootstrapFailure("allowlisted file is unavailable or escaping") from exc
        if resolved != lexical or not lexical.is_file() or lexical.is_symlink():
            raise _BootstrapFailure("allowlisted path is not one exact file")
        absolute.add(lexical)
    return relative, frozenset(absolute)


class _ExactSourceLoader(importlib.abc.Loader):
    """Compile only one already allowlisted source; never consult bytecode."""

    def __init__(self, path: Path, is_package: bool) -> None:
        self._path = path
        self._is_package = is_package

    def create_module(self, spec: object) -> None:
        del spec
        return None

    def exec_module(self, module: object) -> None:
        raw = self._path.read_bytes()
        code = compile(raw, str(self._path), "exec", dont_inherit=True)
        namespace = module.__dict__
        namespace["__file__"] = str(self._path)
        namespace["__cached__"] = None
        exec(code, namespace, namespace)


class _ExactSourceFinder(importlib.abc.MetaPathFinder):
    def __init__(self, sources: dict[str, tuple[Path, bool]]) -> None:
        self._sources = dict(sources)

    def find_spec(
        self,
        fullname: str,
        path: object = None,
        target: object = None,
    ) -> object:
        del path, target
        entry = self._sources.get(fullname)
        if entry is None:
            return None
        source, is_package = entry
        loader = _ExactSourceLoader(source, is_package)
        spec = importlib.util.spec_from_loader(
            fullname,
            loader,
            origin=str(source),
            is_package=is_package,
        )
        if spec is None:
            raise _BootstrapFailure("source-only module spec could not be constructed")
        if is_package:
            spec.submodule_search_locations = [str(source.parent)]
        return spec


def _module_name(relative: str) -> tuple[str, bool] | None:
    pure = PurePosixPath(relative)
    if pure.suffix != ".py":
        return None
    parts = pure.parts
    start: int | None = None
    for index, part in enumerate(parts):
        if part == "s0_public_assembly_candidate" or re.fullmatch(r"s0_i[0-3]", part):
            start = index
            break
    if start is None:
        return None
    module_parts = list(parts[start:])
    filename = module_parts[-1]
    is_package = filename == "__init__.py"
    if is_package:
        module_parts.pop()
    else:
        module_parts[-1] = filename[:-3]
    if not module_parts:
        raise _BootstrapFailure("allowlisted Python source has no module name")
    return ".".join(module_parts), is_package


def _install_source_only_finder(
    workspace_root: Path,
    relative_paths: tuple[str, ...],
) -> None:
    sources: dict[str, tuple[Path, bool]] = {}
    for relative in relative_paths:
        module = _module_name(relative)
        if module is None:
            continue
        name, is_package = module
        path = workspace_root.joinpath(*PurePosixPath(relative).parts)
        if name in sources:
            raise _BootstrapFailure("source allowlist contains a duplicate module")
        sources[name] = (path, is_package)
    required = {
        "s0_public_assembly_candidate",
        "s0_public_assembly_candidate.errors",
        "s0_public_assembly_candidate.runtime_guard",
    }
    if not required.issubset(sources):
        raise _BootstrapFailure("source allowlist omits a bootstrap-critical module")
    sys.meta_path.insert(0, _ExactSourceFinder(sources))


def _require_exact_preinstalled_jsonschema() -> None:
    """Accept only a module already established by the diagnostic host.

    ``-S`` deliberately disables ambient site discovery.  The current v0.5
    design has no dependency manifest, so this bootstrap never searches or
    imports an unpinned dependency tree by path.
    """

    try:
        jsonschema = sys.modules["jsonschema"]
        installed = importlib.metadata.version("jsonschema")
    except (KeyError, importlib.metadata.PackageNotFoundError) as exc:
        raise _BootstrapFailure("authenticated jsonschema runtime profile is unavailable") from exc
    if installed != "4.26.0" or getattr(jsonschema, "__version__", installed) != installed:
        raise _BootstrapFailure("jsonschema runtime profile is not exact")


def _run(config: dict[str, object]) -> int:
    workspace_root = _absolute_directory(config["workspace_root"], "workspace root")
    output_root = _absolute_directory(config["output_root"], "output root")
    relative_paths, absolute_paths = _authenticated_paths(
        workspace_root,
        config["allowed_read_paths"],
    )
    candidate_root = workspace_root.joinpath(*PurePosixPath(_CANDIDATE_ROOT).parts)
    if candidate_root.resolve(strict=True) != candidate_root or not candidate_root.is_dir():
        raise _BootstrapFailure("candidate source root is not exact")

    # Under the current v0.5 gate this deliberately fails closed.  A future
    # runtime-profile gate may preload an authenticated dependency closure.
    _require_exact_preinstalled_jsonschema()
    _install_source_only_finder(workspace_root, relative_paths)
    implementation_root = candidate_root.parent
    sys.path.insert(0, str(implementation_root))

    # The package initializer is inert.  Loading the guard also loads only its
    # private exception class; all controller/component imports follow install.
    from s0_public_assembly_candidate.runtime_guard import install_runtime_sentinels

    install_runtime_sentinels(
        workspace_root=workspace_root,
        output_root=output_root,
        allowed_public_files=absolute_paths,
        bundle_root=workspace_root / "s0-lab" / "public-practice" / "v0.1",
    )

    from s0_public_assembly_candidate.canonical import canonical_json_bytes
    from s0_public_assembly_candidate.channel import FixedAsciiPipeChannel
    from s0_public_assembly_candidate.controller import AssemblyController
    from s0_public_assembly_candidate.errors import AssemblyRunFailed
    from s0_public_assembly_candidate.records import ExternalPins

    pins = ExternalPins(
        assembly_implementation_manifest_sha256=(
            config["assembly_implementation_manifest_sha256"]
        ),
        design_package_manifest_sha256=config["design_package_manifest_sha256"],
        design_independent_review_sha256=config["design_independent_review_sha256"],
    )
    channel = FixedAsciiPipeChannel(
        request_writer=sys.stdout.buffer,
        reply_reader=sys.stdin.buffer,
    )
    controller = AssemblyController(
        workspace_root=workspace_root,
        output_root=output_root,
        external_pins=pins,
        publication_channel=channel,
    )
    try:
        controller.run()
    except AssemblyRunFailed as exc:
        sys.stderr.buffer.write(canonical_json_bytes(exc.diagnostic.as_dict()))
        sys.stderr.buffer.flush()
        return 1
    return 0


def main() -> int:
    try:
        config = _canonical_config()
        return _run(config)
    except BaseException:
        # No exception text, path, environment value, or child input content is
        # allowed to cross this bootstrap-failure boundary.
        try:
            sys.stderr.buffer.write(b"BOOTSTRAP_FAILURE\n")
            sys.stderr.buffer.flush()
        except BaseException:
            pass
        return 2


if __name__ == "__main__":
    raise SystemExit(main())

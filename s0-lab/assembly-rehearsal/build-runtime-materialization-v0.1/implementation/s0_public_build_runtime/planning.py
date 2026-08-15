"""Non-executing build and runtime-tree planning primitives."""

from __future__ import annotations

from dataclasses import dataclass
from types import MappingProxyType
from typing import Iterable, Mapping

from .canonical import canonical_virtual_path, require_sha256, sha256_hex
from .errors import CanonicalError, PlanningError

_DENIED_REPOSITORY_PREFIXES = (
    "s0-lab/control/f0-sealed/",
    "s0-lab/f0-sealed-staging/",
    "s0-lab/reviews/f0-sealed/",
)


def windows_directory_identity_key(directory: str) -> str:
    try:
        canonical_virtual_path(directory)
    except (CanonicalError, UnicodeError) as error:
        raise PlanningError(str(error)) from error
    return "".join(chr(ord(value) + 32) if "A" <= value <= "Z" else value for value in directory)


def directory_identity_sha256(directory: str) -> str:
    key = windows_directory_identity_key(directory)
    return sha256_hex(f"windows_directory_identity_key={key}\n".encode("ascii"))


@dataclass(frozen=True)
class DllRow:
    name: str
    path: str
    sha256: str

    def __post_init__(self) -> None:
        if type(self.name) is not str or not self.name or self.name != self.name.lower() or not self.name.endswith(".dll"):
            raise PlanningError("DLL name is not exact lowercase .dll text")
        canonical_virtual_path(self.path)
        require_sha256(self.sha256, nonzero=True)


@dataclass(frozen=True)
class DllDirectory:
    index: int
    path: str
    identity_key: str
    identity_sha256: str


def derive_dll_directories(application_path: str, dll_rows: Iterable[DllRow]) -> tuple[DllDirectory, ...]:
    canonical_virtual_path(application_path)
    if "/" not in application_path:
        raise PlanningError("application path has no parent directory")
    application_directory = application_path.rsplit("/", 1)[0]
    application_key = windows_directory_identity_key(application_directory)
    exact_rows = tuple(dll_rows)
    names = tuple(row.name for row in exact_rows)
    if len(names) != len(set(names)):
        raise PlanningError("DLL names are not unique")
    parents: dict[str, str] = {application_key: application_directory}
    for row in exact_rows:
        if "/" not in row.path:
            raise PlanningError("DLL path has no parent directory")
        parent = row.path.rsplit("/", 1)[0]
        key = windows_directory_identity_key(parent)
        prior = parents.get(key)
        if prior is not None and prior != parent:
            raise PlanningError("Windows directory identity alias is present")
        parents[key] = parent
    other_keys = sorted((key for key in parents if key != application_key), key=lambda value: value.encode("ascii"))
    ordered = (application_key, *other_keys)
    return tuple(
        DllDirectory(index, parents[key], key, directory_identity_sha256(parents[key]))
        for index, key in enumerate(ordered)
    )


@dataclass(frozen=True)
class RuntimeRow:
    path: str
    role: str
    byte_length: int
    sha256: str
    classification: str
    phase: str

    def __post_init__(self) -> None:
        canonical_virtual_path(self.path)
        if any(self.path.startswith(prefix) for prefix in _DENIED_REPOSITORY_PREFIXES):
            raise PlanningError("runtime row references a denied repository class")
        if type(self.role) is not str or not self.role or type(self.classification) is not str or not self.classification:
            raise PlanningError("runtime row role or classification is invalid")
        if type(self.phase) is not str or not self.phase:
            raise PlanningError("runtime row phase is invalid")
        if type(self.byte_length) is not int or type(self.byte_length) is bool or self.byte_length < 0:
            raise PlanningError("runtime row byte length is invalid")
        require_sha256(self.sha256)


@dataclass(frozen=True)
class RuntimeMaterializationPlan:
    rows: tuple[RuntimeRow, ...]
    total_bytes: int
    file_count: int
    path_index: Mapping[str, RuntimeRow]
    execution_authorized: bool = False


def plan_runtime_tree(
    rows: Iterable[RuntimeRow], *, maximum_files: int = 20_000, maximum_bytes: int = 2_147_483_648
) -> RuntimeMaterializationPlan:
    exact = tuple(rows)
    if not exact or len(exact) > maximum_files:
        raise PlanningError("runtime row count is outside the public bound")
    paths = tuple(row.path for row in exact)
    if paths != tuple(sorted(paths, key=lambda value: value.encode("ascii"))) or len(paths) != len(set(paths)):
        raise PlanningError("runtime paths are not unique unsigned-ASCII order")
    keys = tuple(windows_directory_identity_key(path) for path in paths)
    if len(keys) != len(set(keys)):
        raise PlanningError("runtime paths contain a Windows case alias")
    roles = tuple(row.role for row in exact)
    if len(roles) != len(set(roles)):
        raise PlanningError("runtime semantic roles are not unique")
    total = sum(row.byte_length for row in exact)
    if total > maximum_bytes:
        raise PlanningError("runtime bytes exceed the public bound")
    return RuntimeMaterializationPlan(exact, total, len(exact), MappingProxyType(dict(zip(paths, exact, strict=True))))

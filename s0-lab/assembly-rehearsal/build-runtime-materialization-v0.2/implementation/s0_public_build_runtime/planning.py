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
_MAXIMUM_RUNTIME_FILES = 20_000
_MAXIMUM_RUNTIME_BYTES = 2_147_483_648


def _ascii_lower(value: str) -> str:
    return "".join(chr(ord(character) + 32) if "A" <= character <= "Z" else character for character in value)


def windows_directory_identity_key(directory: str) -> str:
    try:
        canonical_virtual_path(directory)
    except (CanonicalError, UnicodeError) as error:
        raise PlanningError(str(error)) from error
    return _ascii_lower(directory)


def directory_identity_sha256(directory: str) -> str:
    key = windows_directory_identity_key(directory)
    return sha256_hex(f"windows_directory_identity_key={key}\n".encode("ascii"))


@dataclass(frozen=True, slots=True)
class DllRow:
    name: str
    path: str
    sha256: str

    def __post_init__(self) -> None:
        if type(self.name) is not str or not self.name or self.name != self.name.lower() or not self.name.endswith(".dll"):
            raise PlanningError("DLL name is not exact lowercase .dll text")
        canonical_virtual_path(self.path)
        require_sha256(self.sha256, nonzero=True)


@dataclass(frozen=True, slots=True)
class DllDirectory:
    index: int
    path: str
    identity_key: str
    identity_sha256: str

    def __post_init__(self) -> None:
        if type(self.index) is not int or type(self.index) is bool or self.index < 0:
            raise PlanningError("DLL directory index is invalid")
        if self.identity_key != windows_directory_identity_key(self.path):
            raise PlanningError("DLL directory identity key differs")
        if self.identity_sha256 != directory_identity_sha256(self.path):
            raise PlanningError("DLL directory identity digest differs")


def derive_dll_directories(application_path: str, dll_rows: Iterable[DllRow]) -> tuple[DllDirectory, ...]:
    canonical_virtual_path(application_path)
    if "/" not in application_path:
        raise PlanningError("application path has no parent directory")
    application_directory = application_path.rsplit("/", 1)[0]
    application_key = windows_directory_identity_key(application_directory)
    exact_rows = tuple(dll_rows)
    if any(type(row) is not DllRow for row in exact_rows):
        raise PlanningError("DLL row type is not exact")
    names = tuple(row.name for row in exact_rows)
    paths = tuple(row.path for row in exact_rows)
    path_keys = tuple(windows_directory_identity_key(path) for path in paths)
    if len(names) != len(set(names)) or len(paths) != len(set(paths)) or len(path_keys) != len(set(path_keys)):
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


@dataclass(frozen=True, slots=True)
class DllResolutionRow:
    name: str
    path: str
    sha256: str
    parent_directory: str
    directory_identity_key: str
    directory_identity_sha256: str
    directory_index: int

    def __post_init__(self) -> None:
        source = DllRow(self.name, self.path, self.sha256)
        parent = source.path.rsplit("/", 1)[0]
        if source.path.rsplit("/", 1)[1] != source.name or self.parent_directory != parent:
            raise PlanningError("DLL name/path/parent binding differs")
        if self.directory_identity_key != windows_directory_identity_key(parent):
            raise PlanningError("DLL resolution identity key differs")
        if self.directory_identity_sha256 != directory_identity_sha256(parent):
            raise PlanningError("DLL resolution identity digest differs")
        if type(self.directory_index) is not int or type(self.directory_index) is bool or self.directory_index < 0:
            raise PlanningError("DLL resolution directory index differs")


@dataclass(frozen=True, slots=True)
class DllResolutionPlan:
    application_path: str
    directories: tuple[DllDirectory, ...]
    rows: tuple[DllResolutionRow, ...]

    def __post_init__(self) -> None:
        canonical_virtual_path(self.application_path)
        if "/" not in self.application_path:
            raise PlanningError("application path has no parent directory")
        if type(self.directories) is not tuple or any(type(row) is not DllDirectory for row in self.directories):
            raise PlanningError("DLL directory inventory type differs")
        if type(self.rows) is not tuple or any(type(row) is not DllResolutionRow for row in self.rows):
            raise PlanningError("DLL resolution row inventory type differs")
        if tuple(directory.index for directory in self.directories) != tuple(range(len(self.directories))):
            raise PlanningError("DLL directory indices are not contiguous")
        directory_by_key = {directory.identity_key: directory for directory in self.directories}
        if len(directory_by_key) != len(self.directories):
            raise PlanningError("DLL directory identities are not unique")
        application_parent = self.application_path.rsplit("/", 1)[0]
        application_key = windows_directory_identity_key(application_parent)
        parent_by_key = {application_key: application_parent}
        for row in self.rows:
            directory = directory_by_key.get(row.directory_identity_key)
            if directory is None or directory.index != row.directory_index or directory.path != row.parent_directory:
                raise PlanningError("DLL row does not bind one directory inventory entry")
            prior = parent_by_key.get(row.directory_identity_key)
            if prior is not None and prior != row.parent_directory:
                raise PlanningError("DLL plan contains a Windows directory alias")
            parent_by_key[row.directory_identity_key] = row.parent_directory
        expected_keys = (application_key, *sorted((key for key in parent_by_key if key != application_key), key=lambda value: value.encode("ascii")))
        if tuple(directory.identity_key for directory in self.directories) != expected_keys:
            raise PlanningError("DLL directory inventory has an extra, missing, or reordered entry")
        names = tuple(row.name for row in self.rows)
        paths = tuple(row.path for row in self.rows)
        if len(names) != len(set(names)) or len(paths) != len(set(paths)):
            raise PlanningError("DLL resolution rows are not bijective")


def plan_dll_resolution(application_path: str, dll_rows: Iterable[DllRow]) -> DllResolutionPlan:
    exact_rows = tuple(dll_rows)
    if any(type(row) is not DllRow for row in exact_rows):
        raise PlanningError("DLL row type is not exact")
    directories = derive_dll_directories(application_path, exact_rows)
    by_key = {directory.identity_key: directory for directory in directories}
    resolved: list[DllResolutionRow] = []
    for row in exact_rows:
        if "/" not in row.path or row.path.rsplit("/", 1)[1] != row.name:
            raise PlanningError("DLL basename does not equal its exact name")
        parent = row.path.rsplit("/", 1)[0]
        key = windows_directory_identity_key(parent)
        directory = by_key[key]
        resolved.append(
            DllResolutionRow(
                row.name,
                row.path,
                row.sha256,
                parent,
                key,
                directory.identity_sha256,
                directory.index,
            )
        )
    return DllResolutionPlan(application_path, directories, tuple(resolved))


@dataclass(frozen=True, slots=True)
class RuntimeRow:
    path: str
    role: str
    byte_length: int
    sha256: str
    classification: str
    phase: str

    def __post_init__(self) -> None:
        canonical_virtual_path(self.path)
        identity_path = windows_directory_identity_key(self.path)
        if any(identity_path.startswith(_ascii_lower(prefix)) for prefix in _DENIED_REPOSITORY_PREFIXES):
            raise PlanningError("runtime row references a denied repository class")
        if type(self.role) is not str or not self.role or type(self.classification) is not str or not self.classification:
            raise PlanningError("runtime row role or classification is invalid")
        if type(self.phase) is not str or not self.phase:
            raise PlanningError("runtime row phase is invalid")
        if type(self.byte_length) is not int or type(self.byte_length) is bool or self.byte_length < 0:
            raise PlanningError("runtime row byte length is invalid")
        require_sha256(self.sha256)


@dataclass(frozen=True, slots=True)
class RuntimeMaterializationPlan:
    rows: tuple[RuntimeRow, ...]
    total_bytes: int
    file_count: int
    path_index: Mapping[str, RuntimeRow]

    def __post_init__(self) -> None:
        if type(self.rows) is not tuple or not self.rows or any(type(row) is not RuntimeRow for row in self.rows):
            raise PlanningError("runtime plan rows are not exact RuntimeRow values")
        paths = tuple(row.path for row in self.rows)
        if paths != tuple(sorted(paths, key=lambda value: value.encode("ascii"))) or len(paths) != len(set(paths)):
            raise PlanningError("runtime plan paths are not unique unsigned-ASCII order")
        keys = tuple(windows_directory_identity_key(path) for path in paths)
        if len(keys) != len(set(keys)):
            raise PlanningError("runtime plan paths contain a Windows case alias")
        for index, path in enumerate(keys):
            if any(other.startswith(path + "/") for other in keys[index + 1 :]):
                raise PlanningError("runtime plan file path is also a directory prefix")
        roles = tuple(row.role for row in self.rows)
        if len(roles) != len(set(roles)):
            raise PlanningError("runtime plan roles are not unique")
        if len(self.rows) > _MAXIMUM_RUNTIME_FILES:
            raise PlanningError("runtime plan file count exceeds the fixed public ceiling")
        expected_total = sum(row.byte_length for row in self.rows)
        if expected_total > _MAXIMUM_RUNTIME_BYTES:
            raise PlanningError("runtime plan bytes exceed the fixed public ceiling")
        if self.total_bytes != expected_total or self.file_count != len(self.rows):
            raise PlanningError("runtime plan aggregate fields differ")
        if type(self.path_index) is not type(MappingProxyType({})):
            raise PlanningError("runtime plan path index is not immutable")
        expected_index = {row.path: row for row in self.rows}
        if dict(self.path_index) != expected_index:
            raise PlanningError("runtime plan path index differs from rows")

    @property
    def execution_authorized(self) -> bool:
        return False


def plan_runtime_tree(
    rows: Iterable[RuntimeRow], *, maximum_files: int = 20_000, maximum_bytes: int = 2_147_483_648
) -> RuntimeMaterializationPlan:
    exact = tuple(rows)
    if any(type(row) is not RuntimeRow for row in exact):
        raise PlanningError("runtime row type is not exact")
    if (
        type(maximum_files) is not int
        or type(maximum_files) is bool
        or maximum_files <= 0
        or maximum_files > _MAXIMUM_RUNTIME_FILES
        or type(maximum_bytes) is not int
        or type(maximum_bytes) is bool
        or maximum_bytes <= 0
        or maximum_bytes > _MAXIMUM_RUNTIME_BYTES
    ):
        raise PlanningError("caller bound exceeds the fixed public resource ceiling")
    if not exact or len(exact) > maximum_files:
        raise PlanningError("runtime row count is outside the public bound")
    paths = tuple(row.path for row in exact)
    if paths != tuple(sorted(paths, key=lambda value: value.encode("ascii"))) or len(paths) != len(set(paths)):
        raise PlanningError("runtime paths are not unique unsigned-ASCII order")
    keys = tuple(windows_directory_identity_key(path) for path in paths)
    if len(keys) != len(set(keys)):
        raise PlanningError("runtime paths contain a Windows case alias")
    for index, path in enumerate(keys):
        if any(other.startswith(path + "/") for other in keys[index + 1 :]):
            raise PlanningError("runtime file path is also a directory prefix")
    roles = tuple(row.role for row in exact)
    if len(roles) != len(set(roles)):
        raise PlanningError("runtime semantic roles are not unique")
    total = sum(row.byte_length for row in exact)
    if total > maximum_bytes:
        raise PlanningError("runtime bytes exceed the public bound")
    return RuntimeMaterializationPlan(exact, total, len(exact), MappingProxyType(dict(zip(paths, exact, strict=True))))

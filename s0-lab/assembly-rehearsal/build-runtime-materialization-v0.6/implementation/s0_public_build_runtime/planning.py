"""Non-executing, non-authoritative runtime structure diagnostics."""

from __future__ import annotations

import re
from dataclasses import dataclass
from types import MappingProxyType
from typing import Iterable, Mapping

from .canonical import canonical_virtual_path, require_sha256, sha256_hex
from .errors import CanonicalError, PlanningError

_DENIED_REPOSITORY_ROOTS = (
    "s0-lab/control/f0-sealed",
    "s0-lab/f0-sealed-staging",
    "s0-lab/reviews/f0-sealed",
)
_MAXIMUM_RUNTIME_FILES = 20_000
_MAXIMUM_RUNTIME_BYTES = 2_147_483_648
_CLASSIFICATIONS = frozenset(
    {
        "native-executable",
        "native-library",
        "python-source",
        "python-runtime",
        "python-dependency",
        "profile",
        "manifest",
        "public-input",
    }
)
_SEMANTIC_ROLE = re.compile(r"^[a-z0-9][a-z0-9.-]{0,127}$")
_LOAD_OR_READ_PHASE = re.compile(r"^[A-Z][A-Z0-9-]{0,63}$")
_DLL_NAME = re.compile(r"^[A-Za-z0-9_.-]+\.dll$")
_BLOCKED = "BLOCKED-MISSING-EXTERNAL-PIN"


def _ascii_lower(value: str) -> str:
    return "".join(chr(ord(character) + 32) if "A" <= character <= "Z" else character for character in value)


def windows_directory_identity_key(directory: str) -> str:
    try:
        canonical_virtual_path(directory)
    except (CanonicalError, UnicodeError) as error:
        raise PlanningError(str(error)) from error
    return _ascii_lower(directory)


def _is_denied_path(path: str) -> bool:
    identity = windows_directory_identity_key(path)
    return any(identity == root or identity.startswith(root + "/") for root in _DENIED_REPOSITORY_ROOTS)


def directory_identity_sha256(directory: str) -> str:
    identity = windows_directory_identity_key(directory)
    return sha256_hex(f"windows_directory_identity_key={identity}\n".encode("ascii"))


@dataclass(frozen=True, slots=True)
class RuntimeRow:
    """Exact eight-field public runtime-row codec; never execution authority."""

    virtual_path: str
    semantic_role: str
    provenance_manifest_sha256: str
    provenance_path: str
    byte_length: int
    sha256: str
    classification: str
    load_or_read_phase: str

    def __post_init__(self) -> None:
        try:
            canonical_virtual_path(self.virtual_path)
            canonical_virtual_path(self.provenance_path)
            require_sha256(self.provenance_manifest_sha256)
            require_sha256(self.sha256)
        except (CanonicalError, UnicodeError) as error:
            raise PlanningError(str(error)) from error
        if _is_denied_path(self.virtual_path) or _is_denied_path(self.provenance_path):
            raise PlanningError("runtime row references an exact or descendant denied repository identity")
        if type(self.semantic_role) is not str or _SEMANTIC_ROLE.fullmatch(self.semantic_role) is None:
            raise PlanningError("runtime semantic role grammar differs")
        if (
            type(self.byte_length) is not int
            or type(self.byte_length) is bool
            or not 1 <= self.byte_length <= _MAXIMUM_RUNTIME_BYTES
        ):
            raise PlanningError("runtime row byte length is outside the closed public range")
        if type(self.classification) is not str or self.classification not in _CLASSIFICATIONS:
            raise PlanningError("runtime row classification is outside the closed enum")
        if type(self.load_or_read_phase) is not str or _LOAD_OR_READ_PHASE.fullmatch(self.load_or_read_phase) is None:
            raise PlanningError("runtime row load/read phase grammar differs")

    @property
    def path(self) -> str:
        return self.virtual_path

    @property
    def role(self) -> str:
        return self.semantic_role


def _validate_runtime_rows(
    rows: tuple[RuntimeRow, ...], *, maximum_files: int, maximum_bytes: int
) -> tuple[tuple[RuntimeRow, ...], int, Mapping[str, RuntimeRow]]:
    if type(rows) is not tuple or not rows or any(type(row) is not RuntimeRow for row in rows):
        raise PlanningError("runtime rows are not a nonempty exact RuntimeRow tuple")
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
        raise PlanningError("caller diagnostic bound exceeds the fixed public resource ceiling")
    if len(rows) > maximum_files:
        raise PlanningError("runtime row count is outside the selected diagnostic bound")
    rebuilt_rows = tuple(
        RuntimeRow(
            row.virtual_path,
            row.semantic_role,
            row.provenance_manifest_sha256,
            row.provenance_path,
            row.byte_length,
            row.sha256,
            row.classification,
            row.load_or_read_phase,
        )
        for row in rows
    )
    paths = tuple(row.virtual_path for row in rebuilt_rows)
    if paths != tuple(sorted(paths, key=lambda value: value.encode("ascii"))) or len(paths) != len(set(paths)):
        raise PlanningError("runtime paths are not unique unsigned-ASCII order")
    identities = tuple(windows_directory_identity_key(path) for path in paths)
    if len(identities) != len(set(identities)):
        raise PlanningError("runtime paths contain a Windows case alias")
    sorted_identities = tuple(sorted(identities, key=lambda value: value.encode("ascii")))
    for current, following in zip(sorted_identities, sorted_identities[1:]):
        if following.startswith(current + "/"):
            raise PlanningError("runtime file path is also a Windows directory prefix")
    roles = tuple(row.semantic_role for row in rebuilt_rows)
    if len(roles) != len(set(roles)):
        raise PlanningError("runtime semantic roles are not unique")
    total = sum(row.byte_length for row in rebuilt_rows)
    if total > maximum_bytes:
        raise PlanningError("runtime bytes exceed the selected diagnostic bound")
    return rebuilt_rows, total, MappingProxyType({row.virtual_path: row for row in rebuilt_rows})


@dataclass(frozen=True, slots=True)
class RuntimeTreeStructureDiagnostic:
    rows: tuple[RuntimeRow, ...]
    total_bytes: int
    file_count: int

    def __post_init__(self) -> None:
        if type(self.rows) is not tuple:
            raise PlanningError("runtime diagnostic rows are not an exact tuple")
        received_rows = tuple(self.rows)
        copied_rows, total, _ = _validate_runtime_rows(
            received_rows,
            maximum_files=_MAXIMUM_RUNTIME_FILES,
            maximum_bytes=_MAXIMUM_RUNTIME_BYTES,
        )
        if (
            type(self.total_bytes) is not int
            or type(self.file_count) is not int
            or self.total_bytes != total
            or self.file_count != len(copied_rows)
        ):
            raise PlanningError("runtime structure diagnostic aggregate fields differ")
        object.__setattr__(self, "rows", copied_rows)

    @property
    def path_index(self) -> Mapping[str, RuntimeRow]:
        return MappingProxyType({row.virtual_path: row for row in self.rows})

    @property
    def authority_status(self) -> str:
        return _BLOCKED

    @property
    def execution_authorized(self) -> bool:
        return False


def inspect_runtime_tree_structure(
    rows: Iterable[RuntimeRow],
    *,
    maximum_files: int = _MAXIMUM_RUNTIME_FILES,
    maximum_bytes: int = _MAXIMUM_RUNTIME_BYTES,
) -> RuntimeTreeStructureDiagnostic:
    exact = tuple(rows)
    copied_rows, total, _ = _validate_runtime_rows(
        exact, maximum_files=maximum_files, maximum_bytes=maximum_bytes
    )
    return RuntimeTreeStructureDiagnostic(copied_rows, total, len(copied_rows))


def plan_runtime_tree(*args: object, **kwargs: object) -> None:
    del args, kwargs
    raise PlanningError("runtime materialization planning is BLOCKED-MISSING-EXTERNAL-PIN")


@dataclass(frozen=True, slots=True)
class DllRow:
    """Exact three-field DLL-map row codec; caller order is not authority."""

    name: str
    path: str
    sha256: str

    def __post_init__(self) -> None:
        if type(self.name) is not str or _DLL_NAME.fullmatch(self.name) is None:
            raise PlanningError("DLL name grammar differs")
        try:
            canonical_virtual_path(self.path)
            require_sha256(self.sha256)
        except (CanonicalError, UnicodeError) as error:
            raise PlanningError(str(error)) from error
        if _is_denied_path(self.path):
            raise PlanningError("DLL row references an exact or descendant denied repository identity")
        if "/" not in self.path or _ascii_lower(self.path.rsplit("/", 1)[1]) != _ascii_lower(self.name):
            raise PlanningError("DLL basename does not equal its exact case-folded name")


@dataclass(frozen=True, slots=True)
class DllDirectoryDiagnostic:
    index: int
    path: str
    identity_key: str
    identity_sha256: str

    def __post_init__(self) -> None:
        if type(self.index) is not int or type(self.index) is bool or self.index < 0:
            raise PlanningError("DLL directory index is invalid")
        if _is_denied_path(self.path):
            raise PlanningError("DLL directory references an exact or descendant denied repository identity")
        if type(self.identity_key) is not str or self.identity_key != windows_directory_identity_key(self.path):
            raise PlanningError("DLL directory identity key differs")
        try:
            require_sha256(self.identity_sha256)
        except CanonicalError as error:
            raise PlanningError(str(error)) from error
        if self.identity_sha256 != directory_identity_sha256(self.path):
            raise PlanningError("DLL directory identity digest differs")


@dataclass(frozen=True, slots=True)
class DllResolutionRowDiagnostic:
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
        if type(self.parent_directory) is not str or self.parent_directory != parent:
            raise PlanningError("DLL parent binding differs")
        if (
            type(self.directory_identity_key) is not str
            or self.directory_identity_key != windows_directory_identity_key(parent)
        ):
            raise PlanningError("DLL resolution identity key differs")
        try:
            require_sha256(self.directory_identity_sha256)
        except CanonicalError as error:
            raise PlanningError(str(error)) from error
        if self.directory_identity_sha256 != directory_identity_sha256(parent):
            raise PlanningError("DLL resolution identity digest differs")
        if type(self.directory_index) is not int or type(self.directory_index) is bool or self.directory_index < 0:
            raise PlanningError("DLL resolution directory index differs")


@dataclass(frozen=True, slots=True)
class DllResolutionStructureDiagnostic:
    application_path: str
    directories: tuple[DllDirectoryDiagnostic, ...]
    rows: tuple[DllResolutionRowDiagnostic, ...]

    def __post_init__(self) -> None:
        canonical_virtual_path(self.application_path)
        if _is_denied_path(self.application_path) or "/" not in self.application_path:
            raise PlanningError("application path is denied or has no parent")
        if type(self.directories) is not tuple or type(self.rows) is not tuple:
            raise PlanningError("DLL aggregate containers are not exact tuples")
        copied_directories = tuple(self.directories)
        copied_rows = tuple(self.rows)
        if not copied_directories or not copied_rows:
            raise PlanningError("DLL aggregate is empty")
        if any(type(row) is not DllDirectoryDiagnostic for row in copied_directories):
            raise PlanningError("DLL directory diagnostic type differs")
        if any(type(row) is not DllResolutionRowDiagnostic for row in copied_rows):
            raise PlanningError("DLL resolution diagnostic type differs")
        copied_directories = tuple(
            DllDirectoryDiagnostic(row.index, row.path, row.identity_key, row.identity_sha256)
            for row in copied_directories
        )
        copied_rows = tuple(
            DllResolutionRowDiagnostic(
                row.name,
                row.path,
                row.sha256,
                row.parent_directory,
                row.directory_identity_key,
                row.directory_identity_sha256,
                row.directory_index,
            )
            for row in copied_rows
        )
        if tuple(row.index for row in copied_directories) != tuple(range(len(copied_directories))):
            raise PlanningError("DLL directory indices are not contiguous")
        directory_by_key = {row.identity_key: row for row in copied_directories}
        if len(directory_by_key) != len(copied_directories):
            raise PlanningError("DLL directory identities are not unique")
        application_directory = self.application_path.rsplit("/", 1)[0]
        application_key = windows_directory_identity_key(application_directory)
        if (
            copied_directories[0].path != application_directory
            or copied_directories[0].identity_key != application_key
        ):
            raise PlanningError("DLL directory zero is not the application parent")
        actual_keys = tuple(row.identity_key for row in copied_directories)
        expected_keys = (
            application_key,
            *sorted(
                (key for key in actual_keys if key != application_key),
                key=lambda value: value.encode("ascii"),
            ),
        )
        if actual_keys != expected_keys:
            raise PlanningError("DLL directories are not in effective identity-key order")
        names = tuple(_ascii_lower(row.name) for row in copied_rows)
        paths = tuple(row.path for row in copied_rows)
        path_keys = tuple(windows_directory_identity_key(path) for path in paths)
        if len(names) != len(set(names)) or len(paths) != len(set(paths)) or len(path_keys) != len(set(path_keys)):
            raise PlanningError("DLL aggregate names or paths are not unique")
        used_directory_keys = {application_key}
        for row in copied_rows:
            directory = directory_by_key.get(row.directory_identity_key)
            if directory is None or directory.index != row.directory_index or directory.path != row.parent_directory:
                raise PlanningError("DLL row does not bind one directory diagnostic")
            used_directory_keys.add(row.directory_identity_key)
        if set(directory_by_key) != used_directory_keys:
            raise PlanningError("DLL aggregate contains an unused directory")
        object.__setattr__(self, "directories", copied_directories)
        object.__setattr__(self, "rows", copied_rows)

    @property
    def authority_status(self) -> str:
        return _BLOCKED

    @property
    def execution_authorized(self) -> bool:
        return False


def inspect_dll_resolution_structure(
    application_path: str, dll_rows: Iterable[DllRow]
) -> DllResolutionStructureDiagnostic:
    canonical_virtual_path(application_path)
    if _is_denied_path(application_path) or "/" not in application_path:
        raise PlanningError("application path is denied or has no parent")
    exact_rows = tuple(dll_rows)
    if not exact_rows or any(type(row) is not DllRow for row in exact_rows):
        raise PlanningError("DLL rows are not a nonempty exact DllRow tuple")
    exact_rows = tuple(DllRow(row.name, row.path, row.sha256) for row in exact_rows)
    names = tuple(_ascii_lower(row.name) for row in exact_rows)
    paths = tuple(row.path for row in exact_rows)
    path_keys = tuple(windows_directory_identity_key(path) for path in paths)
    if len(names) != len(set(names)) or len(paths) != len(set(paths)) or len(path_keys) != len(set(path_keys)):
        raise PlanningError("DLL names or paths are not unique under the closed identity rules")

    application_directory = application_path.rsplit("/", 1)[0]
    application_key = windows_directory_identity_key(application_directory)
    parent_by_identity: dict[str, str] = {application_key: application_directory}
    for row in exact_rows:
        parent = row.path.rsplit("/", 1)[0]
        key = windows_directory_identity_key(parent)
        prior = parent_by_identity.get(key)
        if prior is not None and prior != parent:
            raise PlanningError("DLL parent directories contain a Windows case alias")
        parent_by_identity[key] = parent

    other_paths = tuple(
        parent_by_identity[key]
        for key in sorted(
            (key for key in parent_by_identity if key != application_key),
            key=lambda value: value.encode("ascii"),
        )
    )
    ordered_paths = (application_directory, *other_paths)
    directories = tuple(
        DllDirectoryDiagnostic(index, path, windows_directory_identity_key(path), directory_identity_sha256(path))
        for index, path in enumerate(ordered_paths)
    )
    index_by_path = {row.path: row.index for row in directories}
    resolution_rows = tuple(
        DllResolutionRowDiagnostic(
            row.name,
            row.path,
            row.sha256,
            row.path.rsplit("/", 1)[0],
            windows_directory_identity_key(row.path.rsplit("/", 1)[0]),
            directory_identity_sha256(row.path.rsplit("/", 1)[0]),
            index_by_path[row.path.rsplit("/", 1)[0]],
        )
        for row in exact_rows
    )
    return DllResolutionStructureDiagnostic(application_path, directories, resolution_rows)


def derive_dll_directories(*args: object, **kwargs: object) -> None:
    del args, kwargs
    raise PlanningError("design-bound DLL directory derivation is BLOCKED-MISSING-EXTERNAL-PIN")


def plan_dll_resolution(*args: object, **kwargs: object) -> None:
    del args, kwargs
    raise PlanningError("design-bound DLL resolution planning is BLOCKED-MISSING-EXTERNAL-PIN")

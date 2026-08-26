"""Inert, hash-authenticated ZIP materialization.

This module only copies regular-file bytes from an authenticated ZIP archive
to a new directory.  It deliberately provides no process, import, install, or
build authority.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import hmac
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import shutil
import stat
from typing import BinaryIO, Final
import zipfile

from .canonical import canonical_sha256
from .errors import MaterializationError


_COPY_CHUNK_SIZE: Final = 1024 * 1024
_SHA256_RE: Final = re.compile(r"[0-9a-f]{64}\Z")
_WINDOWS_RESERVED: Final = frozenset(
    {"CON", "PRN", "AUX", "NUL", "CLOCK$"}
    | {f"COM{number}" for number in range(1, 10)}
    | {f"LPT{number}" for number in range(1, 10)}
)
_SUPPORTED_COMPRESSION: Final = frozenset(
    {
        zipfile.ZIP_STORED,
        zipfile.ZIP_DEFLATED,
        zipfile.ZIP_BZIP2,
        zipfile.ZIP_LZMA,
    }
)
_REPARSE_ATTRIBUTE: Final = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)


@dataclass(frozen=True, slots=True)
class MaterializationLimits:
    """Hard limits applied to the declared uncompressed ZIP inventory."""

    max_entries: int = 4096
    max_files: int = 4096
    max_file_size: int = 64 * 1024 * 1024
    max_total_size: int = 512 * 1024 * 1024
    max_path_length: int = 240

    def __post_init__(self) -> None:
        for name in (
            "max_entries",
            "max_files",
            "max_file_size",
            "max_total_size",
            "max_path_length",
        ):
            if getattr(self, name) <= 0:
                raise ValueError(f"{name} must be positive")


DEFAULT_LIMITS: Final = MaterializationLimits()


@dataclass(frozen=True, slots=True)
class MaterializedFile:
    relative_path: str
    size: int
    sha256: str


@dataclass(frozen=True, slots=True)
class MaterializationEvidence:
    archive_path: str
    archive_sha256: str
    destination_path: str
    file_count: int
    directory_count: int
    total_size: int
    target_set_sha256: str
    files: tuple[MaterializedFile, ...]
    process_authority_granted: bool = field(default=False, init=False)
    installed: bool = field(default=False, init=False)
    executed: bool = field(default=False, init=False)
    imported: bool = field(default=False, init=False)


@dataclass(frozen=True, slots=True)
class WheelMaterializationState:
    evidence: MaterializationEvidence
    inert_only: bool = field(default=True, init=False)
    installed: bool = field(default=False, init=False)
    executed: bool = field(default=False, init=False)
    process_authority_granted: bool = field(default=False, init=False)


@dataclass(frozen=True, slots=True)
class BuildToolsMaterializationState:
    evidence: MaterializationEvidence
    inert_only: bool = field(default=True, init=False)
    installed: bool = field(default=False, init=False)
    built: bool = field(default=False, init=False)
    executed: bool = field(default=False, init=False)
    process_authority_granted: bool = field(default=False, init=False)


@dataclass(frozen=True, slots=True)
class _PlannedFile:
    relative_path: str
    info: zipfile.ZipInfo


@dataclass(frozen=True, slots=True)
class _Inventory:
    files: tuple[_PlannedFile, ...]
    directories: tuple[str, ...]
    total_size: int


def _fail(message: str) -> MaterializationError:
    return MaterializationError(message)


def _is_reparse_or_symlink(path: Path) -> bool:
    if path.is_symlink():
        return True
    try:
        attributes = getattr(os.lstat(path), "st_file_attributes", 0)
    except OSError as exc:
        raise _fail(f"cannot inspect path component: {path}") from exc
    return bool(attributes & _REPARSE_ATTRIBUTE)


def _require_plain_existing_directory(path: Path, label: str) -> None:
    if not os.path.lexists(path):
        raise _fail(f"{label} does not exist: {path}")
    if _is_reparse_or_symlink(path):
        raise _fail(f"{label} is a symlink or reparse point: {path}")
    if not path.is_dir():
        raise _fail(f"{label} is not a directory: {path}")


def _check_parent_chain(path: Path) -> None:
    current = path
    while True:
        _require_plain_existing_directory(current, "destination parent")
        if current.parent == current:
            return
        current = current.parent


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _prepare_paths(
    archive_path: os.PathLike[str] | str,
    destination: os.PathLike[str] | str,
    repository_root: os.PathLike[str] | str,
) -> tuple[Path, Path, Path]:
    archive = Path(archive_path)
    target = Path(destination)
    repository = Path(repository_root)

    if not target.is_absolute():
        raise _fail("destination must be an absolute path")
    if not repository.is_absolute():
        raise _fail("repository_root must be an absolute path")
    if os.path.lexists(target):
        if _is_reparse_or_symlink(target):
            raise _fail("destination is a symlink or reparse point")
        raise _fail("destination must be fresh and must not already exist")

    _require_plain_existing_directory(repository, "repository_root")
    _check_parent_chain(target.parent)
    repository_resolved = repository.resolve(strict=True)
    target_resolved = target.resolve(strict=False)
    if _is_within(target_resolved, repository_resolved):
        raise _fail("destination must be outside the repository")

    if not os.path.lexists(archive):
        raise _fail("archive does not exist")
    if _is_reparse_or_symlink(archive):
        raise _fail("archive must not be a symlink or reparse point")
    archive_resolved = archive.resolve(strict=True)
    if not archive_resolved.is_file():
        raise _fail("archive must be a regular file")
    return archive_resolved, target_resolved, repository_resolved


def _validated_digest(expected_sha256: str) -> str:
    if not isinstance(expected_sha256, str):
        raise _fail("expected_sha256 must be a lowercase hexadecimal string")
    if _SHA256_RE.fullmatch(expected_sha256) is None:
        raise _fail("expected_sha256 must be exactly 64 lowercase hexadecimal characters")
    return expected_sha256


def _hash_open_file(source: BinaryIO) -> str:
    digest = hashlib.sha256()
    while True:
        chunk = source.read(_COPY_CHUNK_SIZE)
        if not chunk:
            break
        digest.update(chunk)
    source.seek(0)
    return digest.hexdigest()


def _validate_component(component: str) -> None:
    if component in {"", ".", ".."}:
        raise _fail("ZIP member contains an empty, dot, or traversal component")
    if component.endswith((".", " ")):
        raise _fail("ZIP member component has a trailing dot or space")
    if ":" in component:
        raise _fail("ZIP member contains a colon or alternate-data-stream syntax")
    if any(ord(character) < 32 or ord(character) == 127 for character in component):
        raise _fail("ZIP member contains a control character")
    device_stem = component.split(".", 1)[0].rstrip(" .").upper()
    if device_stem in _WINDOWS_RESERVED:
        raise _fail("ZIP member contains a Windows reserved device name")


def _safe_member_path(info: zipfile.ZipInfo, limits: MaterializationLimits) -> str:
    raw_name = getattr(info, "orig_filename", info.filename)
    if not isinstance(raw_name, str) or raw_name == "":
        raise _fail("ZIP member has an empty path")
    if "\x00" in raw_name:
        raise _fail("ZIP member path contains NUL")
    if "\\" in raw_name:
        raise _fail("ZIP member path contains a backslash")
    if raw_name.startswith("/") or PureWindowsPath(raw_name).drive:
        raise _fail("ZIP member path is absolute, drive-qualified, or UNC-qualified")

    is_directory = info.is_dir()
    path_text = raw_name[:-1] if is_directory and raw_name.endswith("/") else raw_name
    if path_text == "" or path_text.endswith("/"):
        raise _fail("ZIP member has an empty path component")
    parts = path_text.split("/")
    for component in parts:
        _validate_component(component)

    normalized = PurePosixPath(*parts).as_posix()
    if normalized != path_text:
        raise _fail("ZIP member path is not canonical")
    if len(normalized) > limits.max_path_length:
        raise _fail("ZIP member path exceeds the configured path-length limit")
    return normalized


def _validate_entry_type(info: zipfile.ZipInfo) -> None:
    if info.flag_bits & 0x1:
        raise _fail("encrypted ZIP members are not permitted")
    if info.compress_type not in _SUPPORTED_COMPRESSION:
        raise _fail("ZIP member uses an unsupported compression method")

    unix_mode = info.external_attr >> 16
    if info.create_system == 3 and unix_mode:
        file_type = stat.S_IFMT(unix_mode)
        expected = stat.S_IFDIR if info.is_dir() else stat.S_IFREG
        if file_type not in {0, expected}:
            raise _fail("ZIP member is a symlink or another non-regular entry")

    dos_attributes = info.external_attr & 0xFFFF
    if dos_attributes & _REPARSE_ATTRIBUTE:
        raise _fail("ZIP member carries a reparse-point attribute")
    if info.is_dir() and info.file_size != 0:
        raise _fail("ZIP directory member declares nonzero file data")


def _preflight_inventory(
    archive: zipfile.ZipFile,
    destination: Path,
    limits: MaterializationLimits,
) -> _Inventory:
    infos = archive.infolist()
    if len(infos) > limits.max_entries:
        raise _fail("ZIP entry count exceeds the configured limit")

    explicit_names: set[str] = set()
    explicit_casefold: dict[str, str] = {}
    node_casefold: dict[str, str] = {}
    files: dict[str, zipfile.ZipInfo] = {}
    directories: set[str] = set()
    total_size = 0

    for info in infos:
        _validate_entry_type(info)
        relative_path = _safe_member_path(info, limits)
        folded = relative_path.casefold()
        if relative_path in explicit_names:
            raise _fail("ZIP contains a duplicate target path")
        prior_explicit = explicit_casefold.get(folded)
        if prior_explicit is not None and prior_explicit != relative_path:
            raise _fail("ZIP contains a case-folding target collision")
        explicit_names.add(relative_path)
        explicit_casefold[folded] = relative_path

        parts = relative_path.split("/")
        prefixes = ["/".join(parts[:index]) for index in range(1, len(parts) + 1)]
        for prefix in prefixes:
            folded_prefix = prefix.casefold()
            prior_node = node_casefold.get(folded_prefix)
            if prior_node is not None and prior_node != prefix:
                raise _fail("ZIP contains a case-folding directory collision")
            node_casefold[folded_prefix] = prefix

        for index in range(1, len(parts)):
            parent = "/".join(parts[:index])
            if parent in files:
                raise _fail("ZIP file path is an ancestor of another target")
            directories.add(parent)

        if info.is_dir():
            if relative_path in files:
                raise _fail("ZIP target is both a file and a directory")
            directories.add(relative_path)
        else:
            if relative_path in directories:
                raise _fail("ZIP target is both a file and a directory")
            if info.file_size < 0 or info.file_size > limits.max_file_size:
                raise _fail("ZIP member exceeds the configured per-file size limit")
            total_size += info.file_size
            if total_size > limits.max_total_size:
                raise _fail("ZIP aggregate size exceeds the configured limit")
            files[relative_path] = info

    if len(files) > limits.max_files:
        raise _fail("ZIP file count exceeds the configured limit")
    if not files:
        raise _fail("ZIP archive contains no regular files")
    if files.keys() & directories:
        raise _fail("ZIP has a file/directory topology collision")
    for file_path in files:
        parts = file_path.split("/")
        if any("/".join(parts[:index]) in files for index in range(1, len(parts))):
            raise _fail("ZIP file path is an ancestor of another target")

    for relative_path in (*directories, *files):
        resolved_target = (destination / Path(*relative_path.split("/"))).resolve(strict=False)
        if not _is_within(resolved_target, destination):
            raise _fail("ZIP target resolves outside the destination")

    planned_files = tuple(
        _PlannedFile(relative_path=path, info=files[path])
        for path in sorted(files, key=lambda value: (value.casefold(), value))
    )
    planned_directories = tuple(
        sorted(
            directories,
            key=lambda value: (len(value.split("/")), value.casefold(), value),
        )
    )
    return _Inventory(
        files=planned_files,
        directories=planned_directories,
        total_size=total_size,
    )


def _destination_child(destination: Path, relative_path: str) -> Path:
    child = destination / Path(*relative_path.split("/"))
    resolved = child.resolve(strict=False)
    if not _is_within(resolved, destination):
        raise _fail("materialization target escaped the destination")
    return child


def _copy_member_exclusively(
    archive: zipfile.ZipFile,
    planned: _PlannedFile,
    destination: Path,
) -> MaterializedFile:
    target = _destination_child(destination, planned.relative_path)
    digest = hashlib.sha256()
    observed_size = 0
    try:
        with archive.open(planned.info, mode="r") as source, target.open(mode="xb") as output:
            while True:
                chunk = source.read(_COPY_CHUNK_SIZE)
                if not chunk:
                    break
                observed_size += len(chunk)
                if observed_size > planned.info.file_size:
                    raise _fail("ZIP member produced more bytes than declared")
                output.write(chunk)
                digest.update(chunk)
    except FileExistsError as exc:
        raise _fail("exclusive target creation failed") from exc
    if observed_size != planned.info.file_size:
        raise _fail("ZIP member produced a size different from its declaration")
    return MaterializedFile(
        relative_path=planned.relative_path,
        size=observed_size,
        sha256=digest.hexdigest(),
    )


def materialize_authenticated_zip(
    archive_path: os.PathLike[str] | str,
    expected_sha256: str,
    destination: os.PathLike[str] | str,
    *,
    repository_root: os.PathLike[str] | str,
    limits: MaterializationLimits = DEFAULT_LIMITS,
) -> MaterializationEvidence:
    """Copy authenticated regular files into a fresh out-of-repository path."""

    expected_digest = _validated_digest(expected_sha256)
    archive_path_resolved, destination_resolved, _ = _prepare_paths(
        archive_path,
        destination,
        repository_root,
    )
    created_destination = False
    open_flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)

    try:
        descriptor = os.open(archive_path_resolved, open_flags)
        with os.fdopen(descriptor, mode="rb") as source:
            if not stat.S_ISREG(os.fstat(source.fileno()).st_mode):
                raise _fail("archive must remain a regular file when opened")
            actual_digest = _hash_open_file(source)
            if not hmac.compare_digest(actual_digest, expected_digest):
                raise _fail("archive SHA-256 does not match the authenticated pin")

            with zipfile.ZipFile(source, mode="r") as archive:
                inventory = _preflight_inventory(archive, destination_resolved, limits)
                _check_parent_chain(destination_resolved.parent)
                destination_resolved.mkdir(mode=0o700, exist_ok=False)
                created_destination = True
                if _is_reparse_or_symlink(destination_resolved):
                    raise _fail("created destination became a symlink or reparse point")

                for relative_path in inventory.directories:
                    directory = _destination_child(destination_resolved, relative_path)
                    directory.mkdir(mode=0o700, exist_ok=False)
                    if _is_reparse_or_symlink(directory):
                        raise _fail("created directory became a symlink or reparse point")

                materialized = tuple(
                    _copy_member_exclusively(archive, planned, destination_resolved)
                    for planned in inventory.files
                )
    except MaterializationError:
        if created_destination:
            shutil.rmtree(destination_resolved)
        raise
    except (
        OSError,
        ValueError,
        RuntimeError,
        zipfile.BadZipFile,
        zipfile.LargeZipFile,
    ) as exc:
        if created_destination:
            shutil.rmtree(destination_resolved)
        raise _fail("authenticated ZIP materialization failed") from exc

    target_set = [
        {
            "path": item.relative_path,
            "sha256": item.sha256,
            "size": item.size,
        }
        for item in materialized
    ]
    return MaterializationEvidence(
        archive_path=str(archive_path_resolved),
        archive_sha256=actual_digest,
        destination_path=str(destination_resolved),
        file_count=len(materialized),
        directory_count=len(inventory.directories),
        total_size=sum(item.size for item in materialized),
        target_set_sha256=canonical_sha256({"files": target_set}),
        files=materialized,
    )


def materialize_wheel_archive(
    archive_path: os.PathLike[str] | str,
    expected_sha256: str,
    destination: os.PathLike[str] | str,
    *,
    repository_root: os.PathLike[str] | str,
    limits: MaterializationLimits = DEFAULT_LIMITS,
) -> WheelMaterializationState:
    """Materialize wheel bytes without installing or importing them."""

    evidence = materialize_authenticated_zip(
        archive_path,
        expected_sha256,
        destination,
        repository_root=repository_root,
        limits=limits,
    )
    return WheelMaterializationState(evidence=evidence)


def materialize_build_tools_archive(
    archive_path: os.PathLike[str] | str,
    expected_sha256: str,
    destination: os.PathLike[str] | str,
    *,
    repository_root: os.PathLike[str] | str,
    limits: MaterializationLimits = DEFAULT_LIMITS,
) -> BuildToolsMaterializationState:
    """Materialize build-tool bytes without installing, building, or running."""

    evidence = materialize_authenticated_zip(
        archive_path,
        expected_sha256,
        destination,
        repository_root=repository_root,
        limits=limits,
    )
    return BuildToolsMaterializationState(evidence=evidence)


stage_zip_archive = materialize_authenticated_zip

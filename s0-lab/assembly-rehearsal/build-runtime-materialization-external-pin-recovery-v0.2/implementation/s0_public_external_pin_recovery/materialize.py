"""Inert, handle-bound materialization of the authenticated CPython ZIP."""

from __future__ import annotations

from dataclasses import dataclass, field
import hashlib
import hmac
import os
from pathlib import Path, PurePosixPath, PureWindowsPath
import re
import stat
import sys
from typing import Callable, Final, NamedTuple
import zipfile

from .acquisition import AcquisitionCheckpoint, AcquisitionEvidence
from .canonical import canonical_sha256
from .errors import MaterializationError
from .pins import ArtifactPin, PinSnapshot, _resolve_approved_pin_snapshot
from .win32_secure import (
    SecureCreatedFile,
    SecureDirectoryRoot,
    SecureExistingFile,
    WindowsFileIdentity,
    secure_create_directory_root,
    secure_open_existing_file,
)


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
_CHECKPOINT_LABELS: Final = (
    "post_write",
    "post_flush",
    "post_readback",
    "final_binding",
)


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
            if type(getattr(self, name)) is not int or getattr(self, name) <= 0:
                raise ValueError(f"{name} must be a positive exact integer")


DEFAULT_LIMITS: Final = MaterializationLimits()


@dataclass(frozen=True, slots=True)
class MaterializedFile:
    relative_path: str
    size: int
    sha256: str


@dataclass(frozen=True, slots=True)
class MaterializationEvidence:
    pin_id: str
    acquisition_evidence_sha256: str
    archive_path: str
    archive_sha256: str
    archive_initial_identity: WindowsFileIdentity
    archive_final_identity: WindowsFileIdentity
    archive_pre_sha256: str
    archive_post_sha256: str
    destination_path: str
    root_initial_identity: WindowsFileIdentity
    root_final_identity: WindowsFileIdentity
    file_count: int
    directory_count: int
    total_size: int
    target_set_sha256: str
    files: tuple[MaterializedFile, ...]
    final_reauthentication_passed: bool
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


@dataclass(frozen=True, slots=True)
class _CreatedOutput:
    relative_path: str
    size: int
    streamed_sha256: str
    identity: WindowsFileIdentity


class _TrustedPin(NamedTuple):
    """One immutable pin value copied from closure-held primitive authority."""

    pin_id: str
    filename: str
    url: str | None
    expected_sha256: str | None
    expected_size: int | None
    max_size: int


def _fail(message: str) -> MaterializationError:
    return MaterializationError(message)


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _destination_preview(destination: os.PathLike[str] | str) -> Path:
    try:
        raw = os.fspath(destination)
    except (TypeError, ValueError, OSError) as exc:
        raise _fail("destination is invalid") from exc
    if type(raw) is not str or not raw or "\x00" in raw:
        raise _fail("destination must be an absolute string path")
    target = Path(raw)
    if not target.is_absolute():
        raise _fail("destination must be an absolute path")
    return target.resolve(strict=False)


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
        resolved_target = (
            destination / Path(*relative_path.split("/"))
        ).resolve(strict=False)
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


def _require_sha256(value: object, error_message: str) -> str:
    if type(value) is not str or _SHA256_RE.fullmatch(value) is None:
        raise _fail(error_message)
    return value


def _freeze_cpython_resolver(
    snapshot_resolver: Callable[[ArtifactPin | str], PinSnapshot],
) -> Callable[[ArtifactPin | str], _TrustedPin]:
    resolver = snapshot_resolver
    trusted_type = _TrustedPin
    try:
        cpython_snapshot = resolver("cpython-3.12.10-embed-amd64")
    except Exception as exc:
        raise RuntimeError("canonical CPython authority is unavailable") from exc
    if (
        type(cpython_snapshot) is not tuple
        or len(cpython_snapshot) != 6
        or cpython_snapshot[0] != "cpython-3.12.10-embed-amd64"
        or type(cpython_snapshot[3]) is not str
    ):
        raise RuntimeError("canonical CPython authority is invalid")

    def resolve_cpython_pin(pin_or_id: ArtifactPin | str) -> _TrustedPin:
        try:
            snapshot = resolver(pin_or_id)
        except Exception as exc:
            raise _fail("external-artifact pin is not approved") from exc
        if type(snapshot) is not tuple or snapshot != cpython_snapshot:
            raise _fail("only the canonical authenticated CPython pin may be materialized")
        return trusted_type(*cpython_snapshot)

    return resolve_cpython_pin


_resolve_cpython_pin = _freeze_cpython_resolver(_resolve_approved_pin_snapshot)
del _freeze_cpython_resolver
del _resolve_approved_pin_snapshot


def _checkpoint_mapping(checkpoint: AcquisitionCheckpoint) -> dict[str, object]:
    return {
        "file_id": checkpoint.file_id,
        "label": checkpoint.label,
        "sha256": checkpoint.sha256,
        "size": checkpoint.size,
        "volume_serial": checkpoint.volume_serial,
    }


def _acquisition_mapping(evidence: AcquisitionEvidence) -> dict[str, object]:
    return {
        "artifact_name": evidence.artifact_name,
        "authenticated": evidence.authenticated,
        "checkpoints": [_checkpoint_mapping(item) for item in evidence.checkpoints],
        "destination": evidence.destination,
        "expected_sha256": evidence.expected_sha256,
        "expected_size": evidence.expected_size,
        "filename": evidence.filename,
        "max_size": evidence.max_size,
        "observed_sha256": evidence.observed_sha256,
        "observed_size": evidence.observed_size,
        "pin_id": evidence.pin_id,
        "process_authority": evidence.process_authority,
        "redirect_count": evidence.redirect_count,
        "reuse_authority": evidence.reuse_authority,
        "source_uri": evidence.source_uri,
        "status": evidence.status,
    }


def _validate_acquisition_evidence(
    pin: _TrustedPin, evidence: AcquisitionEvidence
) -> tuple[WindowsFileIdentity, str]:
    if type(evidence) is not AcquisitionEvidence:
        raise _fail("acquisition_evidence must be an exact v0.2 AcquisitionEvidence")
    expected_digest = _require_sha256(
        pin.expected_sha256, "the canonical CPython digest is invalid"
    )
    if (
        evidence.pin_id != pin.pin_id
        or evidence.artifact_name != pin.filename
        or evidence.filename != pin.filename
        or evidence.source_uri != pin.url
        or type(evidence.redirect_count) is not int
        or evidence.redirect_count != 0
        or evidence.expected_size != pin.expected_size
        or evidence.expected_sha256 != expected_digest
        or evidence.max_size != pin.max_size
        or type(evidence.observed_size) is not int
        or evidence.observed_size <= 0
        or evidence.observed_size > pin.max_size
        or evidence.observed_sha256 != expected_digest
        or type(evidence.destination) is not str
        or not evidence.destination
        or type(evidence.authenticated) is not bool
        or evidence.authenticated is not True
        or type(evidence.process_authority) is not bool
        or evidence.process_authority is not False
        or type(evidence.reuse_authority) is not bool
        or evidence.reuse_authority is not False
        or evidence.status != "acquired-authenticated"
    ):
        raise _fail("acquisition evidence does not exactly authenticate the CPython pin")
    if pin.expected_size is not None and evidence.observed_size != pin.expected_size:
        raise _fail("acquisition evidence size does not match the CPython pin")

    checkpoints = evidence.checkpoints
    if type(checkpoints) is not tuple or len(checkpoints) != len(_CHECKPOINT_LABELS):
        raise _fail("acquisition evidence checkpoints are incomplete")
    reference: tuple[int, str, int, str] | None = None
    for expected_label, checkpoint in zip(_CHECKPOINT_LABELS, checkpoints, strict=True):
        if type(checkpoint) is not AcquisitionCheckpoint:
            raise _fail("acquisition checkpoint has a non-canonical type")
        if (
            type(checkpoint.label) is not str
            or checkpoint.label != expected_label
            or type(checkpoint.volume_serial) is not int
            or checkpoint.volume_serial < 0
            or type(checkpoint.file_id) is not str
            or len(checkpoint.file_id) != 32
            or checkpoint.file_id != checkpoint.file_id.lower()
            or any(character not in "0123456789abcdef" for character in checkpoint.file_id)
            or type(checkpoint.size) is not int
            or checkpoint.size != evidence.observed_size
            or checkpoint.sha256 != expected_digest
        ):
            raise _fail("acquisition checkpoint does not authenticate stable bytes")
        current = (
            checkpoint.volume_serial,
            checkpoint.file_id,
            checkpoint.size,
            checkpoint.sha256,
        )
        if reference is None:
            reference = current
        elif current != reference:
            raise _fail("acquisition checkpoint identity or bytes changed")
    if reference is None:
        raise _fail("acquisition evidence identity is unavailable")
    identity = WindowsFileIdentity(
        volume_serial=reference[0],
        file_id=reference[1],
    )
    try:
        evidence_sha256 = canonical_sha256(_acquisition_mapping(evidence))
    except (TypeError, ValueError) as exc:
        raise _fail("acquisition evidence is not canonical JSON data") from exc
    return identity, evidence_sha256


def _write_member(
    archive: zipfile.ZipFile,
    planned: _PlannedFile,
    output: SecureCreatedFile,
) -> _CreatedOutput:
    digest = hashlib.sha256()
    observed_size = 0
    with archive.open(planned.info, mode="r") as source:
        while True:
            chunk = source.read(_COPY_CHUNK_SIZE)
            if not chunk:
                break
            observed_size += len(chunk)
            if observed_size > planned.info.file_size:
                raise _fail("ZIP member produced more bytes than declared")
            output.write_all(chunk)
            digest.update(chunk)
    if observed_size != planned.info.file_size:
        raise _fail("ZIP member produced a size different from its declaration")
    output.flush()
    snapshot = output.snapshot("materialized_file_invalid")
    if snapshot.length != observed_size or snapshot.identity != output.identity:
        raise _fail("materialized file changed before final verification")
    return _CreatedOutput(
        relative_path=planned.relative_path,
        size=observed_size,
        streamed_sha256=digest.hexdigest(),
        identity=output.identity,
    )


def _close_retained(handle: object) -> BaseException | None:
    try:
        handle.close()  # type: ignore[attr-defined]
    except BaseException as exc:
        return exc
    return None


def _materialize_authenticated_zip_impl(
    pin_or_id: ArtifactPin | str,
    acquisition_evidence: AcquisitionEvidence,
    destination: os.PathLike[str] | str,
    *,
    repository_root: os.PathLike[str] | str,
    limits: MaterializationLimits = DEFAULT_LIMITS,
    resolve_cpython_pin: Callable[[ArtifactPin | str], _TrustedPin],
) -> MaterializationEvidence:
    """Copy authenticated CPython files without process, import, or install authority."""

    if type(limits) is not MaterializationLimits:
        raise _fail("limits must be an exact MaterializationLimits value")
    pin = resolve_cpython_pin(pin_or_id)
    expected_identity, acquisition_evidence_sha256 = _validate_acquisition_evidence(
        pin, acquisition_evidence
    )
    expected_digest = _require_sha256(
        pin.expected_sha256, "the canonical CPython digest is invalid"
    )
    destination_path = _destination_preview(destination)

    archive_file: SecureExistingFile | None = None
    root: SecureDirectoryRoot | None = None
    created_handles: list[SecureCreatedFile] = []
    verified_handles: list[SecureExistingFile] = []
    primary_error: BaseException | None = None
    close_error: BaseException | None = None
    try:
        archive_file = secure_open_existing_file(
            repository_root=repository_root,
            path=acquisition_evidence.destination,
            expected_identity=expected_identity,
        )
        archive_initial = archive_file.revalidate()
        if (
            archive_initial.identity != expected_identity
            or archive_initial.length != acquisition_evidence.observed_size
            or archive_file.initial_length != acquisition_evidence.observed_size
        ):
            raise _fail("retained archive identity or size differs from acquisition evidence")
        archive_pre_sha256 = archive_file.readback_sha256(
            archive_initial.length, _COPY_CHUNK_SIZE
        )
        if not hmac.compare_digest(archive_pre_sha256, expected_digest):
            raise _fail("retained archive SHA-256 does not match the canonical pin")
        archive_file.seek(0)

        created_outputs: list[_CreatedOutput] = []
        with zipfile.ZipFile(archive_file, mode="r") as archive:
            inventory = _preflight_inventory(archive, destination_path, limits)
            root = secure_create_directory_root(
                repository_root=repository_root,
                destination=destination,
            )
            root_initial_identity = root.identity
            for relative_path in inventory.directories:
                root.create_directory(tuple(relative_path.split("/")))
            for planned in inventory.files:
                components = tuple(planned.relative_path.split("/"))
                output = root.create_file(components[:-1], components[-1])
                created_handles.append(output)
                created_outputs.append(_write_member(archive, planned, output))
            root.revalidate()

        archive_post_open = archive_file.revalidate()
        if archive_post_open != archive_initial:
            raise _fail("archive identity or size changed during extraction")
        archive_post_sha256 = archive_file.readback_sha256(
            archive_initial.length, _COPY_CHUNK_SIZE
        )
        archive_final = archive_file.revalidate()
        if (
            archive_final != archive_initial
            or not hmac.compare_digest(archive_post_sha256, archive_pre_sha256)
            or not hmac.compare_digest(archive_post_sha256, expected_digest)
        ):
            raise _fail("archive failed post-extraction reauthentication")

        for output in reversed(created_handles):
            output.close()
        if root is None:
            raise _fail("secure destination root is unavailable")
        root.revalidate()

        materialized: list[MaterializedFile] = []
        for created in created_outputs:
            components = tuple(created.relative_path.split("/"))
            verified = root.open_file(
                components[:-1],
                components[-1],
                expected_identity=created.identity,
            )
            verified_handles.append(verified)
            if verified.initial_length != created.size:
                raise _fail("materialized file size changed before final readback")
            final_sha256 = verified.readback_sha256(created.size, _COPY_CHUNK_SIZE)
            final_snapshot = verified.revalidate()
            if (
                final_snapshot.identity != created.identity
                or final_snapshot.length != created.size
                or not hmac.compare_digest(final_sha256, created.streamed_sha256)
            ):
                raise _fail("materialized file failed final retained-handle verification")
            materialized.append(
                MaterializedFile(
                    relative_path=created.relative_path,
                    size=created.size,
                    sha256=final_sha256,
                )
            )

        root.revalidate()
        root_final_identity = root.identity
        if root_final_identity != root_initial_identity:
            raise _fail("destination root identity changed before evidence creation")
        if sum(item.size for item in materialized) != inventory.total_size:
            raise _fail("final verified size differs from the preflight inventory")
        target_set = [
            {"path": item.relative_path, "sha256": item.sha256, "size": item.size}
            for item in materialized
        ]
        return MaterializationEvidence(
            pin_id=pin.pin_id,
            acquisition_evidence_sha256=acquisition_evidence_sha256,
            archive_path=archive_file.path,
            archive_sha256=archive_post_sha256,
            archive_initial_identity=archive_initial.identity,
            archive_final_identity=archive_final.identity,
            archive_pre_sha256=archive_pre_sha256,
            archive_post_sha256=archive_post_sha256,
            destination_path=root.destination,
            root_initial_identity=root_initial_identity,
            root_final_identity=root_final_identity,
            file_count=len(materialized),
            directory_count=len(inventory.directories),
            total_size=sum(item.size for item in materialized),
            target_set_sha256=canonical_sha256({"files": target_set}),
            files=tuple(materialized),
            final_reauthentication_passed=True,
        )
    except MaterializationError as exc:
        primary_error = exc
        raise
    except BaseException as exc:
        primary_error = exc
        if isinstance(exc, (KeyboardInterrupt, SystemExit, GeneratorExit)):
            raise
        raise _fail("authenticated ZIP materialization failed") from exc
    finally:
        for handle in reversed(verified_handles):
            error = _close_retained(handle)
            if close_error is None and error is not None:
                close_error = error
        for handle in reversed(created_handles):
            error = _close_retained(handle)
            if close_error is None and error is not None:
                close_error = error
        if root is not None:
            error = _close_retained(root)
            if close_error is None and error is not None:
                close_error = error
        if archive_file is not None:
            error = _close_retained(archive_file)
            if close_error is None and error is not None:
                close_error = error
        if primary_error is None and close_error is not None and sys.exc_info()[0] is None:
            raise _fail("retained handle close failed") from close_error


def _freeze_materializer(
    resolve_cpython_pin: Callable[[ArtifactPin | str], _TrustedPin],
):
    implementation = _materialize_authenticated_zip_impl

    def materialize_authenticated_zip(
        pin_or_id: ArtifactPin | str,
        acquisition_evidence: AcquisitionEvidence,
        destination: os.PathLike[str] | str,
        *,
        repository_root: os.PathLike[str] | str,
        limits: MaterializationLimits = DEFAULT_LIMITS,
    ) -> MaterializationEvidence:
        return implementation(
            pin_or_id,
            acquisition_evidence,
            destination,
            repository_root=repository_root,
            limits=limits,
            resolve_cpython_pin=resolve_cpython_pin,
        )

    return materialize_authenticated_zip


materialize_authenticated_zip = _freeze_materializer(_resolve_cpython_pin)
del _freeze_materializer
del _materialize_authenticated_zip_impl
del _resolve_cpython_pin


def materialize_wheel_archive(
    pin_or_id: ArtifactPin | str,
    acquisition_evidence: AcquisitionEvidence,
    destination: os.PathLike[str] | str,
    *,
    repository_root: os.PathLike[str] | str,
    limits: MaterializationLimits = DEFAULT_LIMITS,
) -> WheelMaterializationState:
    """Materialize only the approved CPython ZIP, retaining inert wheel state."""

    evidence = materialize_authenticated_zip(
        pin_or_id,
        acquisition_evidence,
        destination,
        repository_root=repository_root,
        limits=limits,
    )
    return WheelMaterializationState(evidence=evidence)


def materialize_build_tools_archive(
    pin_or_id: ArtifactPin | str,
    acquisition_evidence: AcquisitionEvidence,
    destination: os.PathLike[str] | str,
    *,
    repository_root: os.PathLike[str] | str,
    limits: MaterializationLimits = DEFAULT_LIMITS,
) -> BuildToolsMaterializationState:
    """Materialize only the approved CPython ZIP, retaining inert build-tool state."""

    evidence = materialize_authenticated_zip(
        pin_or_id,
        acquisition_evidence,
        destination,
        repository_root=repository_root,
        limits=limits,
    )
    return BuildToolsMaterializationState(evidence=evidence)


stage_zip_archive = materialize_authenticated_zip


__all__ = [
    "BuildToolsMaterializationState",
    "DEFAULT_LIMITS",
    "MaterializationEvidence",
    "MaterializationLimits",
    "MaterializedFile",
    "WheelMaterializationState",
    "materialize_authenticated_zip",
    "materialize_build_tools_archive",
    "materialize_wheel_archive",
    "stage_zip_archive",
]

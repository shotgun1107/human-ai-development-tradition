"""Windows-only acquisition, extraction, publication, readback, and import probe."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import stat
import subprocess
import tempfile
import time
import urllib.parse
import urllib.request
import uuid
import zipfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from .authority import ArtifactPin, activate_repository_authority, authority_record
from .canonical import hash_file_object, jcs_lf, sha256_hex, sidecar_bytes, strict_json
from .errors import AcquisitionError, ArchiveError, PathSafetyError, ProbeError, PublicationError

_MAX_ARCHIVES = 7
_MAX_DOWNLOAD_BYTES = 16 * 1024 * 1024
_MAX_ENTRIES = 20_000
_MAX_ENTRY_BYTES = 128 * 1024 * 1024
_MAX_ARCHIVE_BYTES = 768 * 1024 * 1024
_MAX_RUNTIME_BYTES = 1024 * 1024 * 1024
_MAX_RATIO = 200
_PROCESS_TIMEOUT = 30
_PUBLICATION_POLICY_ID = "python-os-rename-windows-no-replace-v0.7"
_PUBLICATION_PRIMITIVE_ID = "python.os.rename"
_PUBLICATION_LINEARIZATION_POINT = "successful-os.rename-call"
_REPARSE = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
_RESERVED = {"con", "prn", "aux", "nul", *(f"com{i}" for i in range(1, 10)), *(f"lpt{i}" for i in range(1, 10))}


@dataclass(frozen=True, slots=True)
class MaterializationResult:
    final_root: str
    payload_manifest_sha256: str
    runtime_record_sha256: str
    status: str


def _identity(path: Path) -> tuple[int, int]:
    value = path.stat(follow_symlinks=False)
    return (value.st_dev, value.st_ino)


def _is_reparse(path: Path) -> bool:
    value = path.lstat()
    return path.is_symlink() or bool(getattr(value, "st_file_attributes", 0) & _REPARSE)


def _require_directory_identity(path: Path, expected: tuple[int, int]) -> None:
    try:
        value = path.lstat()
    except OSError as error:
        raise PathSafetyError("bound directory identity is no longer reachable") from error
    if _is_reparse(path) or not stat.S_ISDIR(value.st_mode) or _identity(path) != expected:
        raise PathSafetyError("bound directory was replaced or became reparse-backed")


def _check_existing_ancestors(path: Path) -> None:
    absolute = Path(os.path.abspath(path))
    existing: list[Path] = []
    cursor = absolute
    while not cursor.exists():
        parent = cursor.parent
        if parent == cursor:
            raise PathSafetyError("path has no existing ancestor")
        cursor = parent
    while True:
        existing.append(cursor)
        if cursor.parent == cursor:
            break
        cursor = cursor.parent
    for item in reversed(existing):
        if _is_reparse(item):
            raise PathSafetyError("an existing path ancestor is a reparse point")


def _under(path: Path, root: Path) -> bool:
    try:
        return os.path.commonpath((str(path), str(root))).casefold() == str(root).casefold()
    except ValueError:
        return False


def _safe_external_root(value: str, repository: Path, *, must_exist: bool) -> Path:
    if type(value) is not str or not value:
        raise PathSafetyError("external path must be exact nonempty text")
    path = Path(os.path.abspath(value))
    _check_existing_ancestors(path)
    if _under(path, repository):
        raise PathSafetyError("runtime/cache path must be outside the repository")
    if must_exist:
        resolved = path.resolve(strict=True)
        if not resolved.is_dir() or _is_reparse(path):
            raise PathSafetyError("required external directory is absent or reparse-backed")
        return resolved
    parent = path.parent.resolve(strict=True)
    if not parent.is_dir() or path.exists():
        raise PathSafetyError("final root parent must exist and final root must be absent")
    aliases = [entry.name for entry in os.scandir(parent) if entry.name.casefold() == path.name.casefold()]
    if aliases:
        raise PathSafetyError("final root has an existing Windows case alias")
    return parent / path.name


class _Redirects(urllib.request.HTTPRedirectHandler):
    def __init__(self, expected_host: str) -> None:
        self.expected_host = expected_host
        self.urls: list[str] = []

    def redirect_request(self, req: object, fp: object, code: int, msg: str, headers: object, newurl: str) -> object:
        parsed = urllib.parse.urlsplit(newurl)
        if len(self.urls) >= 3 or parsed.scheme != "https" or parsed.hostname != self.expected_host or parsed.username is not None:
            raise AcquisitionError("redirect exceeds the closed HTTPS same-host policy")
        self.urls.append(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _download(pin: ArtifactPin, cache: Path) -> tuple[Path, dict[str, object]]:
    target = cache / pin.filename
    if target.exists():
        if _is_reparse(target) or not target.is_file():
            raise AcquisitionError("cache entry is not an exact regular file")
        with target.open("rb") as handle:
            size, digest = hash_file_object(handle, maximum_bytes=pin.size)
        if (size, digest) != (pin.size, pin.sha256):
            raise AcquisitionError("cache entry differs from its frozen pin")
        return target, {"final_url": pin.url, "redirects": [], "source": "authenticated-cache"}
    part = cache / f".{pin.filename}.{uuid.uuid4().hex}.part"
    parsed = urllib.parse.urlsplit(pin.url)
    if parsed.scheme != "https" or parsed.hostname is None or parsed.username is not None:
        raise AcquisitionError("pin URL is not credential-free HTTPS")
    redirects = _Redirects(parsed.hostname)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), redirects, urllib.request.HTTPSHandler())
    request = urllib.request.Request(pin.url, headers={"Accept-Encoding": "identity", "User-Agent": "s0-public-brm-v0.7"})
    try:
        with part.open("xb") as output, opener.open(request, timeout=30) as response:
            if response.status != 200 or response.headers.get("Content-Encoding", "identity").lower() not in {"", "identity"}:
                raise AcquisitionError("HTTP response status or content encoding differs")
            final_url = response.geturl()
            final = urllib.parse.urlsplit(final_url)
            if final.scheme != "https" or final.hostname != parsed.hostname or final.username is not None:
                raise AcquisitionError("final response URL differs from the closed host policy")
            declared = response.headers.get("Content-Length")
            if declared is not None and (not declared.isascii() or not declared.isdecimal() or int(declared) != pin.size):
                raise AcquisitionError("HTTP Content-Length differs from the pin")
            digest = hashlib.sha256()
            total = 0
            while True:
                chunk = response.read(min(1024 * 1024, pin.size - total + 1))
                if not chunk:
                    break
                total += len(chunk)
                if total > pin.size or total > _MAX_DOWNLOAD_BYTES:
                    raise AcquisitionError("download exceeds its exact size or global cap")
                digest.update(chunk)
                output.write(chunk)
            output.flush()
            os.fsync(output.fileno())
        if total != pin.size or digest.hexdigest() != pin.sha256:
            raise AcquisitionError("download size or SHA-256 differs from the pin")
        os.link(part, target)
        part.unlink()
        return target, {"final_url": final_url, "redirects": list(redirects.urls), "source": "https-download"}
    except Exception:
        if part.exists() and not _is_reparse(part):
            part.unlink()
        raise


def _member_path(name: str) -> tuple[str, bool]:
    if type(name) is not str or not name or "\x00" in name or "\\" in name or name.startswith("/") or ":" in name:
        raise ArchiveError("archive member path grammar differs")
    directory = name.endswith("/")
    core = name[:-1] if directory else name
    try:
        core.encode("ascii", "strict")
    except UnicodeEncodeError as error:
        raise ArchiveError("archive member path is not bounded ASCII") from error
    parts = core.split("/")
    if not core or any(not part or part in {".", ".."} or part.endswith((".", " ")) or part.split(".", 1)[0].casefold() in _RESERVED for part in parts):
        raise ArchiveError("archive member contains an unsafe Windows segment")
    return "/".join(parts), directory


def _inspect_archive(handle: object) -> tuple[zipfile.ZipFile, tuple[tuple[zipfile.ZipInfo, str, bool], ...], int]:
    try:
        archive = zipfile.ZipFile(handle, "r")
        infos = archive.infolist()
    except (OSError, zipfile.BadZipFile) as error:
        raise ArchiveError("archive parsing failed") from error
    if not infos or len(infos) > _MAX_ENTRIES:
        archive.close()
        raise ArchiveError("archive entry count is outside the bound")
    rows: list[tuple[zipfile.ZipInfo, str, bool]] = []
    seen: set[str] = set()
    total = 0
    for info in infos:
        if info.external_attr & _REPARSE:
            archive.close()
            raise ArchiveError("archive member carries the Windows reparse attribute")
        if "\x00" in info.orig_filename or info.flag_bits & 1 or info.compress_type not in {zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED}:
            archive.close()
            raise ArchiveError("archive member flags or compression differ")
        path, directory = _member_path(info.filename)
        key = path.casefold()
        if key in seen:
            archive.close()
            raise ArchiveError("archive contains a duplicate or case-alias member")
        seen.add(key)
        mode = (info.external_attr >> 16) & 0xFFFF
        kind = stat.S_IFMT(mode)
        if kind not in {0, stat.S_IFREG, stat.S_IFDIR} or (directory and kind == stat.S_IFREG) or (not directory and kind == stat.S_IFDIR):
            archive.close()
            raise ArchiveError("archive contains a link or special member")
        if info.file_size < 0 or info.file_size > _MAX_ENTRY_BYTES or info.compress_size < 0 or (info.file_size and info.file_size > max(1, info.compress_size) * _MAX_RATIO):
            archive.close()
            raise ArchiveError("archive member exceeds a resource bound")
        total += info.file_size
        if total > _MAX_ARCHIVE_BYTES:
            archive.close()
            raise ArchiveError("archive expansion exceeds its bound")
        rows.append((info, path, directory))
    files = {path.casefold() for _, path, directory in rows if not directory}
    for _, path, _ in rows:
        parents = PurePosixPath(path).parents
        if any(str(parent).casefold() in files for parent in parents if str(parent) != "."):
            archive.close()
            raise ArchiveError("archive contains a file/directory-prefix collision")
    return archive, tuple(rows), total


def _extract(handle: object, destination: Path, prefix: str, provenance: str, claimed: set[str], sources: dict[str, str]) -> tuple[int, int]:
    archive, rows, total = _inspect_archive(handle)
    try:
        for info, member, directory in rows:
            relative = f"{prefix}/{member}" if prefix else member
            key = relative.casefold()
            parents = tuple(str(parent).casefold() for parent in PurePosixPath(relative).parents if str(parent) != ".")
            if key in claimed or any(parent in claimed for parent in parents) or any(existing.startswith(key + "/") for existing in claimed):
                raise ArchiveError("runtime archives contain a cross-archive shadow collision")
            target = destination.joinpath(*PurePosixPath(relative).parts)
            if directory:
                target.mkdir(parents=True, exist_ok=True)
                continue
            if prefix and member.casefold().endswith(".pth"):
                raise ArchiveError("wheel contains an executable .pth surface")
            target.parent.mkdir(parents=True, exist_ok=True)
            with archive.open(info, "r") as source, target.open("xb") as output:
                copied = 0
                while True:
                    chunk = source.read(1024 * 1024)
                    if not chunk:
                        break
                    copied += len(chunk)
                    if copied > info.file_size:
                        raise ArchiveError("archive member expanded beyond its declared size")
                    output.write(chunk)
                output.flush()
                os.fsync(output.fileno())
            if copied != info.file_size:
                raise ArchiveError("archive member ended before its declared size")
            claimed.add(key)
            sources[relative] = provenance
        return sum(not directory for _, _, directory in rows), total
    finally:
        archive.close()


def _inventory(root: Path, sources: dict[str, str]) -> tuple[list[dict[str, object]], int]:
    rows: list[dict[str, object]] = []
    total = 0
    for current, directories, files in os.walk(root, topdown=True, followlinks=False):
        current_path = Path(current)
        directories[:] = sorted((name for name in directories if not (current_path == root and name == "evidence")), key=str.casefold)
        for name in directories:
            if _is_reparse(current_path / name):
                raise PublicationError("runtime directory is reparse-backed")
        for name in sorted(files, key=str.casefold):
            path = current_path / name
            if _is_reparse(path) or not path.is_file():
                raise PublicationError("runtime payload contains a non-regular file")
            relative = path.relative_to(root).as_posix()
            with path.open("rb") as handle:
                size, digest = hash_file_object(handle, maximum_bytes=_MAX_ENTRY_BYTES)
            total += size
            if total > _MAX_RUNTIME_BYTES or len(rows) >= _MAX_ENTRIES:
                raise PublicationError("runtime payload exceeds a resource bound")
            rows.append({"path": relative, "provenance_pin_id": sources.get(relative, "materializer-v0.7"), "sha256": digest, "size": size})
    rows.sort(key=lambda row: str(row["path"]).encode("ascii"))
    keys = [str(row["path"]).casefold() for row in rows]
    if len(keys) != len(set(keys)):
        raise PublicationError("runtime payload contains a Windows case alias")
    return rows, total


def _write_pair(directory: Path, filename: str, value: dict[str, object]) -> str:
    raw = jcs_lf(value)
    digest = sha256_hex(raw)
    path = directory / filename
    sidecar = directory / f"{filename}.sha256"
    with path.open("xb") as handle:
        handle.write(raw)
        handle.flush()
        os.fsync(handle.fileno())
    with sidecar.open("xb") as handle:
        handle.write(sidecar_bytes(filename, digest))
        handle.flush()
        os.fsync(handle.fileno())
    if path.read_bytes() != raw or sidecar.read_bytes() != sidecar_bytes(filename, digest) or strict_json(raw) != value:
        raise PublicationError("canonical evidence pair readback differs")
    return digest


def _record_package(body: dict[str, object], body_field_order: tuple[str, ...]) -> dict[str, object]:
    if type(body) is not dict or type(body_field_order) is not tuple or set(body) != set(body_field_order) or len(body) != len(body_field_order):
        raise PublicationError("publication record body field inventory differs")
    body_digest = sha256_hex(jcs_lf(body))
    return {
        "body": body,
        "body_canonical_sha256": body_digest,
        "body_closed_file_sha256": body_digest,
        "body_field_order": list(body_field_order),
        "body_hashes_equal": True,
        "body_readback_sha256": body_digest,
        "record_package_codec": "rfc8785-jcs-utf8-no-bom-plus-single-final-lf",
        "schema_id": "S0-PUBLIC-BRM-V0.7-OS-RENAME-PREPUBLICATION-RECORD-1",
        "version": "0.7.0",
    }


def _publication_policy() -> tuple[dict[str, object], str]:
    policy = {
        "authority": "explicit-user-proceed-plus-CONTROL-v0.7-supersession",
        "destination_overwrite_allowed": False,
        "fallback_allowed": False,
        "invocation_count": 1,
        "policy_id": "python-os-rename-windows-no-replace-v0.7",
        "primitive": "python.os.rename",
        "retry_allowed": False,
        "same_volume_required": True,
        "scope": "build-runtime-materialization-v0.7-only",
        "supersedes": "historical-v0.4-v0.5-special-publication-transaction-for-v0.7-only",
        "windows_destination_exists_result": "FileExistsError",
    }
    return policy, sha256_hex(jcs_lf(policy))


def _path_identity_sha256(path: Path) -> str:
    device, file_id = _identity(path)
    return sha256_hex(jcs_lf({
        "device_hex": format(device, "x"),
        "file_id_hex": format(file_id, "x"),
        "path": os.path.normcase(os.path.abspath(path)),
        "reparse_point": _is_reparse(path),
        "schema_id": "S0-PUBLIC-BRM-V0.7-PATH-IDENTITY-1",
    }))


def _destination_absence(final: Path, parent_identity: tuple[int, int]) -> tuple[dict[str, object], str]:
    if _identity(final.parent) != parent_identity or _is_reparse(final.parent):
        raise PathSafetyError("destination parent identity changed before absence observation")
    try:
        final.lstat()
    except FileNotFoundError:
        pass
    else:
        raise FileExistsError(f"destination already exists: {final.name}")
    record = {
        "destination_absent_observed": True,
        "intended_final_name": final.name,
        "parent_identity_sha256": _path_identity_sha256(final.parent),
        "policy_id": _PUBLICATION_POLICY_ID,
    }
    return record, sha256_hex(jcs_lf(record))


def _require_unpublished_state(staging: Path, staging_identity: tuple[int, int], final: Path, parent_identity: tuple[int, int]) -> None:
    _require_directory_identity(staging, staging_identity)
    if _identity(final.parent) != parent_identity or _is_reparse(final.parent):
        raise PathSafetyError("destination parent identity changed during materialization")
    if staging.lstat().st_dev != final.parent.lstat().st_dev:
        raise PathSafetyError("staging and destination are no longer on one volume")
    if not os.access(staging, os.W_OK) or not os.access(final.parent, os.W_OK):
        raise PathSafetyError("effective Windows ACL does not admit required publication access")
    try:
        final.lstat()
    except FileNotFoundError:
        return
    raise FileExistsError(f"destination already exists: {final.name}")


def _target_set(rows: list[dict[str, object]]) -> tuple[list[dict[str, object]], str]:
    targets = [
        {"path": row["path"], "target_byte_length": row["size"], "target_sha256": row["sha256"]}
        for row in rows
    ]
    lines = [
        "schema_id=S0-BRM-TARGET-SET-PREIMAGE-1",
        f"target_count={len(targets)}",
        f"total_target_bytes={sum(int(row['target_byte_length']) for row in targets)}",
    ]
    for row in targets:
        path = str(row["path"])
        lines.extend((f"path_byte_length={len(path.encode('ascii'))}", f"path={path}", f"target_byte_length={row['target_byte_length']}", f"target_sha256={row['target_sha256']}"))
    return targets, sha256_hex(("\n".join(lines) + "\n").encode("ascii"))


_PROBE = r'''import hashlib,importlib,importlib.metadata,json,os,sys
expected=sys.argv[1]
with open(sys.executable,"rb") as f: actual=hashlib.sha256(f.read()).hexdigest()
if actual != expected: raise SystemExit("executable-hash-mismatch")
names=("jsonschema","attrs","jsonschema_specifications","referencing","rpds","typing_extensions","rpds.rpds")
origins={}
for name in names:
 m=importlib.import_module(name); origins[name]=os.path.realpath(m.__file__)
print(json.dumps({"executable":os.path.realpath(sys.executable),"prefix":os.path.realpath(sys.prefix),"path":[os.path.realpath(p) for p in sys.path],"origins":origins,"versions":{p:importlib.metadata.version(p) for p in ("jsonschema","attrs","jsonschema-specifications","referencing","rpds-py","typing-extensions")}},sort_keys=True,separators=(",",":")))
'''


def _probe(final: Path, rows: list[dict[str, object]]) -> dict[str, object]:
    by_path = {row["path"]: row for row in rows}
    executable = final / "python.exe"
    expected = by_path.get("python.exe")
    if expected is None:
        raise ProbeError("payload has no exact python.exe row")
    with executable.open("rb") as handle:
        size, digest = hash_file_object(handle, maximum_bytes=_MAX_ENTRY_BYTES)
    if (size, digest) != (expected["size"], expected["sha256"]):
        raise ProbeError("final python.exe differs immediately before launch")
    environment = {"PYTHONNOUSERSITE": "1", "PYTHONDONTWRITEBYTECODE": "1", "PYTHONPATH": "", "PYTHONUTF8": "1"}
    for key in ("SystemRoot", "WINDIR"):
        if key in os.environ:
            environment[key] = os.environ[key]
    try:
        result = subprocess.run([str(executable), "-I", "-B", "-c", _PROBE, digest], cwd=final / "evidence", env=environment, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=_PROCESS_TIMEOUT, check=False)
    except (OSError, subprocess.SubprocessError) as error:
        raise ProbeError("isolated runtime process could not complete") from error
    if result.returncode != 0 or len(result.stdout) > 1024 * 1024 or len(result.stderr) > 1024 * 1024:
        raise ProbeError("isolated runtime process rejected the final payload")
    try:
        value = json.loads(result.stdout.decode("utf-8", "strict"))
    except (ValueError, UnicodeError) as error:
        raise ProbeError("runtime probe output is not strict JSON") from error
    site = final / "Lib" / "site-packages"
    if type(value) is not dict or Path(value.get("executable", "")).resolve() != executable.resolve() or Path(value.get("prefix", "")).resolve() != final.resolve():
        raise ProbeError("runtime executable or prefix rebound")
    expected_path = [str((final / "python312.zip").resolve()), str(final.resolve()), str(site.resolve())]
    if value.get("path") != expected_path:
        raise ProbeError("isolated sys.path differs from the fixed ._pth closure")
    origins = value.get("origins")
    if type(origins) is not dict or set(origins) != {"jsonschema", "attrs", "jsonschema_specifications", "referencing", "rpds", "typing_extensions", "rpds.rpds"}:
        raise ProbeError("six-project import inventory differs")
    if any(type(origin) is not str for origin in origins.values()) or any(not _under(Path(origin).resolve(), site.resolve()) for origin in origins.values()):
        raise ProbeError("an imported project originated outside final site-packages")
    if value.get("versions") != {"jsonschema": "4.26.0", "attrs": "26.1.0", "jsonschema-specifications": "2025.9.1", "referencing": "0.37.0", "rpds-py": "2026.6.3", "typing-extensions": "4.16.0"}:
        raise ProbeError("imported project versions differ from the frozen pins")
    extension = Path(origins["rpds.rpds"])
    if extension.suffix.casefold() != ".pyd":
        raise ProbeError("rpds imported extension is not the pinned native payload")
    relative = extension.resolve().relative_to(final.resolve()).as_posix()
    extension_row = by_path.get(relative)
    if extension_row is None or sha256_hex(extension.read_bytes()) != extension_row["sha256"]:
        raise ProbeError("rpds extension identity differs")
    return value


def materialize(repository_root: str, cache_root: str, final_root: str) -> MaterializationResult:
    """Activate exact authority, materialize seven archives, publish, and probe."""
    if os.name != "nt":
        raise PathSafetyError("v0.7 materialization is Windows-only")
    authority = activate_repository_authority(repository_root)
    authority.require_authenticated()
    repository = Path(repository_root).resolve(strict=True)
    cache = _safe_external_root(cache_root, repository, must_exist=True)
    final = _safe_external_root(final_root, repository, must_exist=False)
    if len(authority.pins) != _MAX_ARCHIVES or sum(pin.size for pin in authority.pins) > _MAX_DOWNLOAD_BYTES:
        raise AcquisitionError("runtime archive inventory exceeds the fixed aggregate cap")
    parent_identity = _identity(final.parent)
    lock = final.parent / f".{final.name}.s0-brm-v0.7.lock"
    token = uuid.uuid4().hex
    staging: Path | None = None
    published = False
    lock_handle = None
    prepublication_digest: str | None = None
    observations: list[dict[str, object]] = []
    handles: list[tuple[ArtifactPin, object, tuple[int, int]]] = []
    started = time.monotonic()
    try:
        lock_handle = lock.open("x+b")
        lock_handle.write(token.encode("ascii"))
        lock_handle.flush()
        os.fsync(lock_handle.fileno())
        staging = Path(tempfile.mkdtemp(prefix=f".{final.name}.staging-", dir=final.parent))
        if _is_reparse(staging) or not stat.S_ISDIR(staging.lstat().st_mode):
            raise PathSafetyError("fresh staging root is reparse-backed or not a directory")
        staging_identity = _identity(staging)
        if staging.lstat().st_dev != final.parent.stat().st_dev:
            raise PathSafetyError("fresh staging root is not on the publication volume")
        _require_directory_identity(staging, staging_identity)
        _require_unpublished_state(staging, staging_identity, final, parent_identity)
        evidence = staging / "evidence"
        evidence.mkdir()
        marker = evidence / ".s0-brm-v0.7-owner"
        marker.write_text(token, encoding="ascii", newline="\n")
        _require_directory_identity(staging, staging_identity)
        if _identity(final.parent) != parent_identity:
            raise PathSafetyError("parent identity or staging volume changed")
        for pin in authority.pins:
            _require_directory_identity(staging, staging_identity)
            _require_unpublished_state(staging, staging_identity, final, parent_identity)
            path, network = _download(pin, cache)
            handle = path.open("rb")
            before = _identity(path)
            size, digest = hash_file_object(handle, maximum_bytes=pin.size)
            if (size, digest) != (pin.size, pin.sha256):
                handle.close()
                raise AcquisitionError("retained archive handle differs from its pin")
            handles.append((pin, handle, before))
            observations.append({"pin_id": pin.pin_id, "pre_sha256": digest, "pre_size": size, **network})
        claimed: set[str] = set()
        sources: dict[str, str] = {}
        extracted_files = 0
        extracted_bytes = 0
        for index, (pin, handle, before) in enumerate(handles):
            _require_directory_identity(staging, staging_identity)
            _require_unpublished_state(staging, staging_identity, final, parent_identity)
            count, expanded = _extract(handle, staging, "" if index == 0 else "Lib/site-packages", pin.pin_id, claimed, sources)
            _require_directory_identity(staging, staging_identity)
            _require_unpublished_state(staging, staging_identity, final, parent_identity)
            extracted_files += count
            extracted_bytes += expanded
            if extracted_files > _MAX_ENTRIES or extracted_bytes > _MAX_RUNTIME_BYTES:
                raise ArchiveError("aggregate runtime extraction exceeds a resource bound")
            size, digest = hash_file_object(handle, maximum_bytes=pin.size)
            if _identity(Path(handle.name)) != before or (size, digest) != (pin.size, pin.sha256):
                raise AcquisitionError("archive identity changed across extraction")
            observations[index].update({"post_sha256": digest, "post_size": size})
        _require_directory_identity(staging, staging_identity)
        pth = staging / "python312._pth"
        if not pth.is_file() or _is_reparse(pth):
            raise ArchiveError("CPython embeddable python312._pth is absent")
        pth.write_bytes(b"python312.zip\n.\nLib/site-packages\nimport site\n")
        sources["python312._pth"] = "materializer-fixed-pth-v0.7"
        stdlib = staging / "python312.zip"
        with stdlib.open("rb") as handle:
            nested, nested_rows, nested_bytes = _inspect_archive(handle)
            nested.close()
        payload_rows, payload_bytes = _inventory(staging, sources)
        payload_manifest = {
            "file_count": len(payload_rows), "files": payload_rows,
            "python_stdlib_zip": {"entry_count": len(nested_rows), "uncompressed_bytes": nested_bytes},
            "schema_id": "S0-PUBLIC-BRM-V0.7-PAYLOAD-MANIFEST-1", "total_bytes": payload_bytes,
        }
        payload_digest = _write_pair(evidence, "payload-manifest.json", payload_manifest)
        _require_unpublished_state(staging, staging_identity, final, parent_identity)
        authority_value = authority_record(authority)
        authority_digest = sha256_hex(jcs_lf(authority_value))
        publication_policy, publication_policy_sha256 = _publication_policy()
        staging_identity_sha256 = _path_identity_sha256(staging)
        parent_identity_sha256 = _path_identity_sha256(final.parent)
        transaction_id = sha256_hex(jcs_lf({
            "authority_pin_closure_sha256": authority_digest,
            "intended_final_name": final.name,
            "payload_manifest_sha256": payload_digest,
            "policy_id": _PUBLICATION_POLICY_ID,
            "staging_identity_sha256": staging_identity_sha256,
            "transaction_nonce_sha256": sha256_hex(token.encode("ascii")),
        }))
        initial_absence, initial_absence_digest = _destination_absence(final, parent_identity)
        prepublication_order = (
            "authority_supersession",
            "transaction_id",
            "authority_pin_closure_sha256",
            "staging_identity_sha256",
            "destination_parent_identity_sha256",
            "payload_manifest_sha256",
            "intended_final_name",
            "destination_absent_observation_sha256",
            "destination_absent_observed",
            "same_volume_verified",
            "effective_acl_access_verified",
            "publication_policy",
            "publication_policy_sha256",
            "publication_primitive_id",
            "publication_invocation_limit",
            "fallback_allowed",
            "retry_allowed",
            "prepublication_state",
        )
        prepublication_body = {
            "authority_supersession": "explicit-user-proceed-plus-CONTROL-v0.7-only",
            "transaction_id": transaction_id,
            "authority_pin_closure_sha256": authority_digest,
            "staging_identity_sha256": staging_identity_sha256,
            "destination_parent_identity_sha256": parent_identity_sha256,
            "payload_manifest_sha256": payload_digest,
            "intended_final_name": final.name,
            "destination_absent_observation_sha256": initial_absence_digest,
            "destination_absent_observed": initial_absence["destination_absent_observed"],
            "same_volume_verified": True,
            "effective_acl_access_verified": True,
            "publication_policy": publication_policy,
            "publication_policy_sha256": publication_policy_sha256,
            "publication_primitive_id": _PUBLICATION_PRIMITIVE_ID,
            "publication_invocation_limit": 1,
            "fallback_allowed": False,
            "retry_allowed": False,
            "prepublication_state": "PREPUBLICATION-RECORD-BODY-FROZEN",
        }
        prepublication_digest = _write_pair(
            evidence,
            "prepublication-record.json",
            _record_package(prepublication_body, prepublication_order),
        )
        _require_unpublished_state(staging, staging_identity, final, parent_identity)
        destination_recheck, destination_recheck_digest = _destination_absence(final, parent_identity)
        os.rename(staging, final)
        published = True
        staging = None
        (final / "evidence" / ".s0-brm-v0.7-owner").unlink()
        _require_directory_identity(final, staging_identity)
        if _identity(final.parent) != parent_identity:
            raise PublicationError("published root identity differs")
        final_rows, final_bytes = _inventory(final, sources)
        if final_rows != payload_rows or final_bytes != payload_bytes:
            raise PublicationError("post-publication payload readback differs")
        probe = _probe(final, final_rows)
        final_rows_again, final_bytes_again = _inventory(final, sources)
        if final_rows_again != payload_rows or final_bytes_again != payload_bytes:
            raise PublicationError("payload changed across the isolated probe")
        native = [row for row in final_rows if Path(str(row["path"])).suffix.casefold() in {".exe", ".dll", ".pyd"}]
        target_rows, target_set_sha256 = _target_set(final_rows)
        final_publication = {
            "authority_supersession": "explicit-user-proceed-plus-CONTROL-v0.7-only",
            "destination_absent_recheck_observation_sha256": destination_recheck_digest,
            "destination_absent_recheck_observed": destination_recheck["destination_absent_observed"],
            "destination_parent_identity_sha256": parent_identity_sha256,
            "fallback_allowed": False,
            "final_destination_identity_sha256": _path_identity_sha256(final),
            "intended_final_name": final.name,
            "no_overwrite_rename_result": "success",
            "postpublication_identity_verified": True,
            "prepublication_record_package_sha256": prepublication_digest,
            "publication_invocation_count": 1,
            "publication_linearization_point": _PUBLICATION_LINEARIZATION_POINT,
            "publication_policy_id": _PUBLICATION_POLICY_ID,
            "publication_policy_sha256": publication_policy_sha256,
            "publication_primitive_id": _PUBLICATION_PRIMITIVE_ID,
            "reopened_exact_file_count": len(target_rows),
            "reopened_runtime_manifest_sha256": payload_digest,
            "reopened_target_rows": target_rows,
            "reopened_target_set_sha256": target_set_sha256,
            "reopened_total_bytes": final_bytes,
            "retry_allowed": False,
            "staging_prepublication_identity_sha256": staging_identity_sha256,
            "transaction_id": transaction_id,
        }
        record = {
            "artifact_observations": observations,
            "authority": authority_value,
            "claims": {"build_runtime_materialized": True, "central_system_complete": False, "model_to_model_transfer_validated": False, "operational_safety_validated": False, "project_brain_integrated": False, "rehearsal_complete": False, "s0_complete": False},
            "duration_milliseconds": int((time.monotonic() - started) * 1000),
            "executed_python_sha256": next(row["sha256"] for row in final_rows if row["path"] == "python.exe"),
            "final_root": str(final),
            "native_payload": native,
            "nonclaims": ["network-producer-and-supplier-assurance", "same-user-or-local-admin-parent-write-adversary", "all-Windows-versions-and-filesystems-no-overwrite-semantics", "OS-DLL-and-runtime-loader-closure"],
            "payload_manifest_sha256": payload_digest,
            "prepublication_record_sha256": prepublication_digest,
            "probe": probe,
            "publication_policy": publication_policy,
            "publication_transaction": final_publication,
            "schema_id": "S0-PUBLIC-BRM-V0.7-RUNTIME-RECORD-1",
            "status": "COMPLETE-RUNTIME-MATERIALIZATION-ONLY",
        }
        record_digest = _write_pair(final / "evidence", "runtime-record.json", record)
        _require_directory_identity(final, staging_identity)
        _write_pair(final / "evidence", "status.json", {
            "prepublication_record_sha256": prepublication_digest,
            "publication_policy_id": _PUBLICATION_POLICY_ID,
            "publication_policy_sha256": publication_policy_sha256,
            "publication_primitive_id": _PUBLICATION_PRIMITIVE_ID,
            "runtime_record_sha256": record_digest,
            "schema_id": "S0-PUBLIC-BRM-V0.7-STATUS-1",
            "status": "COMPLETE-RUNTIME-MATERIALIZATION-ONLY",
            "transaction_id": transaction_id,
        })
        _require_directory_identity(final, staging_identity)
        return MaterializationResult(str(final), payload_digest, record_digest, "COMPLETE-RUNTIME-MATERIALIZATION-ONLY")
    except Exception as error:
        if published:
            try:
                _write_pair(final / "evidence", "failure-status.json", {
                    "error_type": type(error).__name__,
                    "prepublication_record_sha256": prepublication_digest,
                    "publication_policy_id": _PUBLICATION_POLICY_ID,
                    "publication_primitive_id": _PUBLICATION_PRIMITIVE_ID,
                    "schema_id": "S0-PUBLIC-BRM-V0.7-FAILURE-STATUS-1",
                    "status": "FAILED-AFTER-PUBLICATION-NOT-READY",
                })
            except Exception:
                pass
        raise
    finally:
        for _, handle, _ in handles:
            handle.close()
        if staging is not None and staging.exists():
            marker = staging / "evidence" / ".s0-brm-v0.7-owner"
            if not _is_reparse(staging) and marker.is_file() and marker.read_text(encoding="ascii") == token:
                shutil.rmtree(staging)
        if lock_handle is not None:
            lock_handle.close()
        if lock.exists() and not _is_reparse(lock) and lock.read_bytes() == token.encode("ascii"):
            lock.unlink()

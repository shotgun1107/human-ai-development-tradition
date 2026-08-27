"""In-memory wheel and jsonschema dependency-closure validation."""

from __future__ import annotations

import csv
from dataclasses import dataclass, field, replace
from email import policy
from email.parser import BytesParser
import io
import stat
import unicodedata
import zipfile

from ._issuance import make_bounded_issuance_registry
from .canonical import decode_base64url_nopad, sha256_hex
from .errors import AuthorityError
from .metadata import (
    PyPIMetadataEvidence,
    _consume_issued_metadata_evidence,
    _release_issued_metadata_evidence,
    validate_pypi_metadata,
)
from .pins import (
    JSONSCHEMA_DEPENDENCY_GRAPH,
    MAX_WHEEL_AGGREGATE_BYTES,
    PYPI_JSON_REQUIRES_DIST_INVENTORY,
    WHEEL_METADATA_REQUIRES_DIST_INVENTORY,
    WHEEL_PIN_IDS,
    WheelPin,
    WheelSnapshot,
    resolve_wheel_snapshot,
)


MAX_WHEEL_ENTRIES = 4096
MAX_WHEEL_UNCOMPRESSED_BYTES = 64 * 1024 * 1024
MAX_COMPRESSION_RATIO = 200


@dataclass(frozen=True, slots=True)
class WheelEvidence:
    pin_id: str
    raw_sha256: str
    raw_size: int
    entry_count: int
    uncompressed_size: int
    inventory_sha256: str
    project: str
    version: str
    requires_python: str
    requires_dist: tuple[str, ...]
    wheel_requires_dist: tuple[str, ...]
    tag: str
    record_validated: bool
    imported: bool = False
    installed: bool = False
    raw: bytes = field(repr=False, default=b"")


@dataclass(frozen=True, slots=True, weakref_slot=True)
class JsonschemaClosureEvidence:
    wheel_pin_ids: tuple[str, ...]
    dependency_graph: tuple[tuple[str, tuple[str, ...]], ...]
    pypi_json_requires_dist_inventory: tuple[tuple[str, tuple[str, ...]], ...]
    wheel_metadata_requires_dist_inventory: tuple[tuple[str, tuple[str, ...]], ...]
    metadata_aggregate_size: int
    wheel_aggregate_size: int
    extras_selected: bool = False
    imported: bool = False
    installed: bool = False
    runtime_authority: bool = False


def _zip64_extra_present(extra: bytes, *, error_type) -> bool:
    if type(extra) is not bytes:
        raise error_type("wheel_zip_extra_type_invalid")
    cursor = 0
    while cursor < len(extra):
        if len(extra) - cursor < 4:
            raise error_type("wheel_zip_extra_truncated")
        identifier = int.from_bytes(extra[cursor : cursor + 2], "little")
        length = int.from_bytes(extra[cursor + 2 : cursor + 4], "little")
        cursor += 4
        if cursor + length > len(extra):
            raise error_type("wheel_zip_extra_truncated")
        if identifier == 0x0001:
            return True
        cursor += length
    return False


def _safe_member_name(name: object, *, error_type) -> str:
    if type(name) is not str or not name or len(name) > 4096:
        raise error_type("wheel_member_name_invalid")
    if (
        name.startswith(("/", "\\"))
        or "\\" in name
        or ":" in name
        or "\x00" in name
        or name.endswith("/")
    ):
        raise error_type("wheel_member_path_invalid")
    parts = name.split("/")
    if any(not part or part in {".", ".."} for part in parts):
        raise error_type("wheel_member_traversal_invalid")
    return name


def _headers(raw: bytes, *, label: str, parser_type, parser_policy, error_type):
    if type(raw) is not bytes or not raw or raw.startswith(b"\xef\xbb\xbf") or b"\x00" in raw:
        raise error_type(f"{label}_header_bytes_invalid")
    try:
        message = parser_type(policy=parser_policy).parsebytes(raw, headersonly=True)
    except (TypeError, ValueError) as exc:
        raise error_type(f"{label}_header_parse_failed") from exc
    if message.defects:
        raise error_type(f"{label}_header_defect")
    return message


def _single_header(message, name: str, *, label: str, error_type) -> str:
    values = message.get_all(name, [])
    if len(values) != 1 or type(values[0]) is not str or not values[0]:
        raise error_type(f"{label}_{name.lower()}_cardinality_invalid")
    return values[0]


def _canonical_project(value: str) -> str:
    return value.lower().replace("_", "-").replace(".", "-")


def _validate_wheel_impl(
    pin_or_id: str | WheelPin,
    raw_wheel: bytes,
    *,
    resolve_pin,
    evidence_type,
    error_type,
    hash_bytes,
    zip_file_type,
    bytes_io,
    zip_bad_error,
    zip_stored,
    zip_deflated,
    safe_member_name,
    unicode_normalize,
    stat_ifmt,
    stat_ifreg,
    zip64_extra_present,
    max_entries,
    max_uncompressed_bytes,
    max_compression_ratio,
    headers_parser,
    single_header,
    canonical_project,
    email_parser_type,
    email_parser_policy,
    csv_reader,
    string_io,
    csv_error,
    decode_record_hash,
) -> WheelEvidence:
    pin: WheelSnapshot = resolve_pin(pin_or_id)
    if type(raw_wheel) is not bytes:
        raise error_type("wheel_raw_not_exact_bytes")
    if len(raw_wheel) != pin[6]:
        raise error_type("wheel_raw_size_mismatch")
    if hash_bytes(raw_wheel) != pin[5]:
        raise error_type("wheel_raw_sha256_mismatch")
    try:
        archive = zip_file_type(bytes_io(raw_wheel), "r")
    except (OSError, ValueError, zip_bad_error) as exc:
        raise error_type("wheel_zip_invalid") from exc
    with archive:
        infos = archive.infolist()
        if not infos or len(infos) > max_entries:
            raise error_type("wheel_entry_count_bound_invalid")
        names: dict[str, zipfile.ZipInfo] = {}
        collision_keys: set[str] = set()
        total_size = 0
        for info in infos:
            name = safe_member_name(info.filename, error_type=error_type)
            collision = unicode_normalize("NFC", name).casefold()
            if name in names or collision in collision_keys:
                raise error_type("wheel_duplicate_or_unicode_case_collision")
            names[name] = info
            collision_keys.add(collision)
            if info.is_dir() or info.flag_bits & 0x1:
                raise error_type("wheel_directory_or_encryption_forbidden")
            mode = (info.external_attr >> 16) & 0xFFFF
            if mode and stat_ifmt(mode) not in {0, stat_ifreg}:
                raise error_type("wheel_nonregular_member_forbidden")
            if info.compress_type not in {zip_stored, zip_deflated}:
                raise error_type("wheel_compression_method_forbidden")
            if zip64_extra_present(info.extra, error_type=error_type) or info.extract_version >= 45:
                raise error_type("wheel_zip64_forbidden")
            if info.file_size < 0 or info.compress_size < 0:
                raise error_type("wheel_member_size_invalid")
            if info.file_size and info.file_size > max(1, info.compress_size) * max_compression_ratio:
                raise error_type("wheel_compression_ratio_exceeded")
            total_size += info.file_size
            if total_size > max_uncompressed_bytes:
                raise error_type("wheel_uncompressed_bound_exceeded")

        dist_info_roots = {
            name.split("/", 1)[0]
            for name in names
            if ".dist-info/" in name
        }
        if dist_info_roots != {pin[10]}:
            raise error_type("wheel_dist_info_inventory_mismatch")
        metadata_name = f"{pin[10]}/METADATA"
        wheel_name = f"{pin[10]}/WHEEL"
        record_name = f"{pin[10]}/RECORD"
        if any(name not in names for name in (metadata_name, wheel_name, record_name)):
            raise error_type("wheel_required_dist_info_missing")
        try:
            payloads = {name: archive.read(info) for name, info in names.items()}
        except (OSError, RuntimeError, zip_bad_error) as exc:
            raise error_type("wheel_member_read_failed") from exc

    metadata_headers = headers_parser(
        payloads[metadata_name],
        label="wheel_metadata",
        parser_type=email_parser_type,
        parser_policy=email_parser_policy,
        error_type=error_type,
    )
    if canonical_project(single_header(metadata_headers, "Name", label="wheel_metadata", error_type=error_type)) != pin[1]:
        raise error_type("wheel_metadata_name_mismatch")
    if single_header(metadata_headers, "Version", label="wheel_metadata", error_type=error_type) != pin[2]:
        raise error_type("wheel_metadata_version_mismatch")
    if single_header(metadata_headers, "Requires-Python", label="wheel_metadata", error_type=error_type) != pin[8]:
        raise error_type("wheel_metadata_requires_python_mismatch")
    dependencies = tuple(metadata_headers.get_all("Requires-Dist", []))
    if dependencies != pin[12] or any(type(item) is not str for item in dependencies):
        raise error_type("wheel_metadata_requires_dist_inventory_mismatch")

    wheel_headers = headers_parser(
        payloads[wheel_name],
        label="wheel_contract",
        parser_type=email_parser_type,
        parser_policy=email_parser_policy,
        error_type=error_type,
    )
    if single_header(wheel_headers, "Wheel-Version", label="wheel_contract", error_type=error_type) != "1.0":
        raise error_type("wheel_contract_version_mismatch")
    purelib = single_header(wheel_headers, "Root-Is-Purelib", label="wheel_contract", error_type=error_type)
    if purelib != ("true" if pin[13] else "false"):
        raise error_type("wheel_contract_purelib_mismatch")
    tags = tuple(wheel_headers.get_all("Tag", []))
    if tags != (pin[9],):
        raise error_type("wheel_contract_tag_mismatch")

    record_raw = payloads[record_name]
    if record_raw.startswith(b"\xef\xbb\xbf") or b"\x00" in record_raw:
        raise error_type("wheel_record_bytes_invalid")
    try:
        record_text = record_raw.decode("utf-8", "strict")
        rows = list(csv_reader(string_io(record_text, newline=""), strict=True))
    except (UnicodeDecodeError, csv_error) as exc:
        raise error_type("wheel_record_parse_failed") from exc
    record_paths: set[str] = set()
    for row in rows:
        if len(row) != 3:
            raise error_type("wheel_record_row_shape_invalid")
        path, hash_field, size_field = row
        if path in record_paths or path not in payloads:
            raise error_type("wheel_record_path_inventory_invalid")
        record_paths.add(path)
        if path == record_name:
            if hash_field or size_field:
                raise error_type("wheel_record_self_row_invalid")
            continue
        if not hash_field.startswith("sha256="):
            raise error_type("wheel_record_hash_algorithm_invalid")
        digest = decode_record_hash(
            hash_field[7:], label="wheel_record_hash", expected_size=32
        )
        if digest.hex() != hash_bytes(payloads[path]):
            raise error_type("wheel_record_hash_mismatch")
        if size_field != str(len(payloads[path])):
            raise error_type("wheel_record_size_mismatch")
    if record_paths != set(payloads):
        raise error_type("wheel_record_closure_incomplete")
    inventory = "".join(f"{name}\0{hash_bytes(payloads[name])}\n" for name in sorted(payloads)).encode("utf-8")
    return evidence_type(
        pin[0],
        pin[5],
        pin[6],
        len(payloads),
        total_size,
        hash_bytes(inventory),
        pin[1],
        pin[2],
        pin[8],
        pin[11],
        pin[12],
        pin[9],
        True,
        raw=raw_wheel,
    )


def _freeze_wheel_validator(resolver):
    """Bind the primitive pin resolver before public module rebinding is possible."""

    implementation = _validate_wheel_impl
    frozen_resolver = resolver
    frozen_evidence_type = WheelEvidence
    frozen_error_type = AuthorityError
    frozen_hash_bytes = sha256_hex
    frozen_zip_file_type = zipfile.ZipFile
    frozen_bytes_io = io.BytesIO
    frozen_zip_bad_error = zipfile.BadZipFile
    frozen_zip_stored = zipfile.ZIP_STORED
    frozen_zip_deflated = zipfile.ZIP_DEFLATED
    frozen_safe_member_name = _safe_member_name
    frozen_unicode_normalize = unicodedata.normalize
    frozen_stat_ifmt = stat.S_IFMT
    frozen_stat_ifreg = stat.S_IFREG
    frozen_zip64_extra_present = _zip64_extra_present
    frozen_max_entries = MAX_WHEEL_ENTRIES
    frozen_max_uncompressed_bytes = MAX_WHEEL_UNCOMPRESSED_BYTES
    frozen_max_compression_ratio = MAX_COMPRESSION_RATIO
    frozen_headers_parser = _headers
    frozen_single_header = _single_header
    frozen_canonical_project = _canonical_project
    frozen_email_parser_type = BytesParser
    frozen_email_parser_policy = policy.compat32
    frozen_csv_reader = csv.reader
    frozen_string_io = io.StringIO
    frozen_csv_error = csv.Error
    frozen_decode_record_hash = decode_base64url_nopad

    def validate_wheel(pin_or_id: str | WheelPin, raw_wheel: bytes) -> WheelEvidence:
        return implementation(
            pin_or_id,
            raw_wheel,
            resolve_pin=frozen_resolver,
            evidence_type=frozen_evidence_type,
            error_type=frozen_error_type,
            hash_bytes=frozen_hash_bytes,
            zip_file_type=frozen_zip_file_type,
            bytes_io=frozen_bytes_io,
            zip_bad_error=frozen_zip_bad_error,
            zip_stored=frozen_zip_stored,
            zip_deflated=frozen_zip_deflated,
            safe_member_name=frozen_safe_member_name,
            unicode_normalize=frozen_unicode_normalize,
            stat_ifmt=frozen_stat_ifmt,
            stat_ifreg=frozen_stat_ifreg,
            zip64_extra_present=frozen_zip64_extra_present,
            max_entries=frozen_max_entries,
            max_uncompressed_bytes=frozen_max_uncompressed_bytes,
            max_compression_ratio=frozen_max_compression_ratio,
            headers_parser=frozen_headers_parser,
            single_header=frozen_single_header,
            canonical_project=frozen_canonical_project,
            email_parser_type=frozen_email_parser_type,
            email_parser_policy=frozen_email_parser_policy,
            csv_reader=frozen_csv_reader,
            string_io=frozen_string_io,
            csv_error=frozen_csv_error,
            decode_record_hash=frozen_decode_record_hash,
        )

    return validate_wheel


validate_wheel = _freeze_wheel_validator(resolve_wheel_snapshot)


def _validate_jsonschema_closure_impl(
    metadata_evidence_by_id: dict[str, PyPIMetadataEvidence],
    wheel_evidence_by_id: dict[str, WheelEvidence],
    *,
    pin_ids,
    dependency_graph,
    pypi_json_requires_dist_inventory,
    wheel_metadata_requires_dist_inventory,
    metadata_validator,
    metadata_consumer,
    metadata_releaser,
    wheel_validator,
    metadata_evidence_type,
    wheel_evidence_type,
    closure_evidence_type,
    error_type,
    aggregate_bound,
) -> JsonschemaClosureEvidence:
    if type(metadata_evidence_by_id) is not dict or type(wheel_evidence_by_id) is not dict:
        raise error_type("jsonschema_closure_mapping_type_invalid")
    expected = set(pin_ids)
    if set(metadata_evidence_by_id) != expected or set(wheel_evidence_by_id) != expected:
        raise error_type("jsonschema_closure_pin_inventory_mismatch")
    metadata_total = 0
    wheel_total = 0
    for pin_id in pin_ids:
        metadata = metadata_evidence_by_id[pin_id]
        wheel = wheel_evidence_by_id[pin_id]
        if type(metadata) is not metadata_evidence_type or type(wheel) is not wheel_evidence_type:
            raise error_type("jsonschema_closure_evidence_type_invalid")
        metadata_consumer(metadata, "pypi")
        authenticated_metadata = None
        try:
            authenticated_metadata = metadata_validator(pin_id, metadata.raw)
            authenticated_wheel = wheel_validator(pin_id, wheel.raw)
            if authenticated_metadata != metadata or authenticated_wheel != wheel:
                raise error_type("jsonschema_closure_evidence_rebinding_detected")
            metadata_total += authenticated_metadata.raw_size
            wheel_total += authenticated_wheel.raw_size
        finally:
            if authenticated_metadata is not None:
                metadata_releaser(authenticated_metadata, "pypi")
    if metadata_total > aggregate_bound or wheel_total > aggregate_bound:
        raise error_type("jsonschema_closure_aggregate_bound_exceeded")
    return closure_evidence_type(
        pin_ids,
        dependency_graph,
        pypi_json_requires_dist_inventory,
        wheel_metadata_requires_dist_inventory,
        metadata_total,
        wheel_total,
    )


def _freeze_closure_validator(
    metadata_validator,
    metadata_consumer,
    metadata_releaser,
    wheel_validator,
):
    """Bind both validators so exported-name rebinding cannot redirect closure."""

    implementation = _validate_jsonschema_closure_impl
    frozen_metadata_validator = metadata_validator
    frozen_metadata_consumer = metadata_consumer
    frozen_metadata_releaser = metadata_releaser
    frozen_wheel_validator = wheel_validator
    frozen_pin_ids = WHEEL_PIN_IDS
    frozen_dependency_graph = JSONSCHEMA_DEPENDENCY_GRAPH
    frozen_pypi_json_requires_dist_inventory = PYPI_JSON_REQUIRES_DIST_INVENTORY
    frozen_wheel_metadata_requires_dist_inventory = (
        WHEEL_METADATA_REQUIRES_DIST_INVENTORY
    )
    frozen_metadata_type = PyPIMetadataEvidence
    frozen_wheel_type = WheelEvidence
    frozen_closure_type = JsonschemaClosureEvidence
    frozen_error_type = AuthorityError
    frozen_aggregate_bound = MAX_WHEEL_AGGREGATE_BYTES
    frozen_materialize = replace
    frozen_type = type
    frozen_getattribute = object.__getattribute__

    def snapshot(value: object) -> tuple[object, ...]:
        if frozen_type(value) is not frozen_closure_type:
            raise frozen_error_type("jsonschema_closure_evidence_type_not_issued")
        return (
            frozen_getattribute(value, "wheel_pin_ids"),
            frozen_getattribute(value, "dependency_graph"),
            frozen_getattribute(
                value, "pypi_json_requires_dist_inventory"
            ),
            frozen_getattribute(
                value, "wheel_metadata_requires_dist_inventory"
            ),
            frozen_getattribute(value, "metadata_aggregate_size"),
            frozen_getattribute(value, "wheel_aggregate_size"),
            frozen_getattribute(value, "extras_selected"),
            frozen_getattribute(value, "imported"),
            frozen_getattribute(value, "installed"),
            frozen_getattribute(value, "runtime_authority"),
        )

    issue, require_issued, consume_issued, release_issued = (
        make_bounded_issuance_registry(
            limits={"closure": 1},
            snapshot=snapshot,
            materialize=frozen_materialize,
            error_type=frozen_error_type,
            capacity_error="jsonschema_closure_registry_capacity_exceeded",
            invalid_kind_error="jsonschema_closure_registry_kind_invalid",
            not_issued_error="jsonschema_closure_evidence_not_issued_or_changed",
        )
    )

    def validate_jsonschema_closure(
        metadata_evidence_by_id: dict[str, PyPIMetadataEvidence],
        wheel_evidence_by_id: dict[str, WheelEvidence],
    ) -> JsonschemaClosureEvidence:
        supplied_metadata = (
            tuple(metadata_evidence_by_id.get(pin_id) for pin_id in frozen_pin_ids)
            if type(metadata_evidence_by_id) is dict
            else ()
        )
        try:
            result = implementation(
                metadata_evidence_by_id,
                wheel_evidence_by_id,
                pin_ids=frozen_pin_ids,
                dependency_graph=frozen_dependency_graph,
                pypi_json_requires_dist_inventory=(
                    frozen_pypi_json_requires_dist_inventory
                ),
                wheel_metadata_requires_dist_inventory=(
                    frozen_wheel_metadata_requires_dist_inventory
                ),
                metadata_validator=frozen_metadata_validator,
                metadata_consumer=frozen_metadata_consumer,
                metadata_releaser=frozen_metadata_releaser,
                wheel_validator=frozen_wheel_validator,
                metadata_evidence_type=frozen_metadata_type,
                wheel_evidence_type=frozen_wheel_type,
                closure_evidence_type=frozen_closure_type,
                error_type=frozen_error_type,
                aggregate_bound=frozen_aggregate_bound,
            )
            return issue(result, "closure")
        finally:
            for metadata in supplied_metadata:
                frozen_metadata_releaser(metadata, "pypi")

    def require_issued_jsonschema_closure(value: object) -> JsonschemaClosureEvidence:
        return require_issued(value, "closure")

    def consume_issued_jsonschema_closure(value: object) -> JsonschemaClosureEvidence:
        return consume_issued(value, "closure")

    def release_issued_jsonschema_closure(value: object) -> bool:
        return release_issued(value, "closure")

    return (
        validate_jsonschema_closure,
        require_issued_jsonschema_closure,
        consume_issued_jsonschema_closure,
        release_issued_jsonschema_closure,
    )


(
    validate_jsonschema_closure,
    _require_issued_jsonschema_closure,
    _consume_issued_jsonschema_closure,
    _release_issued_jsonschema_closure,
) = _freeze_closure_validator(
    validate_pypi_metadata,
    _consume_issued_metadata_evidence,
    _release_issued_metadata_evidence,
    validate_wheel,
)


__all__ = [
    "JsonschemaClosureEvidence",
    "WheelEvidence",
    "validate_jsonschema_closure",
    "validate_wheel",
]

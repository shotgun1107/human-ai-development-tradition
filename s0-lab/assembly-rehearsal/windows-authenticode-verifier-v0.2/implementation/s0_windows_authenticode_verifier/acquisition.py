"""Authenticate one externally pinned acquisition record before native use."""

from __future__ import annotations

from dataclasses import dataclass
import re

from .canonical import (
    VerificationError,
    canonical_json_lf,
    exact_bool,
    exact_int,
    exact_keys,
    require_sha256,
    sha256_hex,
    strict_json_object,
)
from .contract import (
    ACQUISITION_HANDLE_CONTRACT,
    ACQUISITION_SCHEMA_ID,
    FIXED_BOOTSTRAPPER_URL,
    MAX_CANDIDATE_BYTES,
)


_VOLUME = re.compile(r"^[0-9a-f]{16}$")
_FILE_ID = re.compile(r"^[0-9a-f]{32}$")
_HANDLE = re.compile(r"^[0-9a-f]{16}$")
_FILETIME = re.compile(r"^[0-9a-f]{16}$")


@dataclass(frozen=True)
class AcquisitionEvidence:
    raw: bytes
    record_sha256: str
    authority_manifest_sha256: str

    def record(self) -> dict[str, object]:
        return strict_json_object(self.raw)


def _file_identity(value: object) -> dict[str, object]:
    identity = exact_keys(
        value,
        ("volume_serial_hex", "file_id_hex", "reparse_point", "byte_length"),
        name="acquisition file identity",
    )
    if type(identity["volume_serial_hex"]) is not str or _VOLUME.fullmatch(
        identity["volume_serial_hex"]
    ) is None:
        raise VerificationError("acquisition volume serial differs")
    if type(identity["file_id_hex"]) is not str or _FILE_ID.fullmatch(
        identity["file_id_hex"]
    ) is None:
        raise VerificationError("acquisition file ID differs")
    if exact_bool(identity["reparse_point"], name="acquisition reparse point") is not False:
        raise VerificationError("acquisition record allows a reparse point")
    length = exact_int(identity["byte_length"], name="acquisition byte length", minimum=1)
    if length > MAX_CANDIDATE_BYTES:
        raise VerificationError("acquisition byte length exceeds the public bound")
    return identity


def authenticate_acquisition_record(
    raw: bytes,
    *,
    expected_record_sha256: str,
    expected_authority_manifest_sha256: str,
    retained_handle: int,
    current_process_id: int,
) -> AcquisitionEvidence:
    """Bind a CONTROL-pinned transfer record to this process and handle."""

    if type(raw) is not bytes:
        raise VerificationError("acquisition record must be exact bytes")
    expected_record = require_sha256(expected_record_sha256, name="acquisition record")
    expected_authority = require_sha256(
        expected_authority_manifest_sha256,
        name="acquisition authority manifest",
    )
    if sha256_hex(raw) != expected_record:
        raise VerificationError("acquisition record pin differs")
    record = strict_json_object(raw)
    exact_keys(
        record,
        (
            "schema_id",
            "authority_manifest_sha256",
            "sequence_id",
            "producer_process_id",
            "created_filetime_hex",
            "requested_uri",
            "final_uri",
            "redirect_count",
            "transfer_complete",
            "retained_handle_hex",
            "handle_contract",
            "file_identity",
            "byte_sha256",
        ),
        name="acquisition record",
    )
    if canonical_json_lf(record) != raw or record["schema_id"] != ACQUISITION_SCHEMA_ID:
        raise VerificationError("acquisition record is not canonical v0.2 bytes")
    if record["authority_manifest_sha256"] != expected_authority:
        raise VerificationError("acquisition producer authority differs")
    require_sha256(record["sequence_id"], name="acquisition sequence")
    if exact_int(record["producer_process_id"], name="producer process", minimum=1) != current_process_id:
        raise VerificationError("acquisition process binding differs")
    created = record["created_filetime_hex"]
    if type(created) is not str or _FILETIME.fullmatch(created) is None or int(created, 16) <= 0:
        raise VerificationError("acquisition creation FILETIME differs")
    if (
        record["requested_uri"] != FIXED_BOOTSTRAPPER_URL
        or record["final_uri"] != FIXED_BOOTSTRAPPER_URL
        or exact_int(record["redirect_count"], name="acquisition redirects", minimum=0) != 0
        or exact_bool(record["transfer_complete"], name="transfer complete") is not True
    ):
        raise VerificationError("acquisition URL or completion binding differs")
    handle_hex = record["retained_handle_hex"]
    if type(handle_hex) is not str or _HANDLE.fullmatch(handle_hex) is None:
        raise VerificationError("acquisition handle grammar differs")
    if type(retained_handle) is not int or retained_handle <= 0 or retained_handle > 0xFFFFFFFFFFFFFFFF:
        raise VerificationError("retained handle is outside the exact runtime range")
    if handle_hex != f"{retained_handle:016x}":
        raise VerificationError("acquisition handle binding differs")
    handle_contract = exact_keys(
        record["handle_contract"],
        tuple(ACQUISITION_HANDLE_CONTRACT),
        name="acquisition handle contract",
    )
    if handle_contract != ACQUISITION_HANDLE_CONTRACT:
        raise VerificationError("acquisition handle contract differs")
    _file_identity(record["file_identity"])
    require_sha256(record["byte_sha256"], name="acquisition bytes")
    return AcquisitionEvidence(raw, expected_record, expected_authority)

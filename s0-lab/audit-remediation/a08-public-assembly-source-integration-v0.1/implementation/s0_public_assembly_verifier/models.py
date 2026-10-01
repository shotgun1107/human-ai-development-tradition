"""Immutable observer and publication value objects."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FileIdentity:
    volume_serial_number: int
    file_index_high: int
    file_index_low: int


@dataclass(frozen=True)
class FileSnapshot:
    identity: FileIdentity
    byte_length: int
    sha256: str


@dataclass(frozen=True)
class MoveResult:
    ffi_return_signed_int32: int
    last_error_uint32: int


@dataclass(frozen=True)
class MoveEvent:
    observer_instance_identity: int
    run_capability_identity: int
    ordinal: int
    output_root_identity: FileIdentity
    source_path: str
    destination_path: str
    pre_volume_serial_number: int
    pre_file_index_high: int
    pre_file_index_low: int
    pre_byte_length: int
    pre_sha256: str
    destination_absent_before_call: bool
    abi_profile_id: str
    flags_numeric: int
    ffi_return_signed_int32: int
    last_error_uint32: int
    source_absent_after_success: bool
    post_volume_serial_number: int
    post_file_index_high: int
    post_file_index_low: int
    post_byte_length: int
    post_sha256: str
    terminal_status: str

    def field_count(self) -> int:
        return len(self.__dataclass_fields__)

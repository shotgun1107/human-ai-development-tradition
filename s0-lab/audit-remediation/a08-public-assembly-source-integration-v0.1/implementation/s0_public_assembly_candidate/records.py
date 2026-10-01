"""Exact run-record-v3 and externally pinned receipt-v2 builders."""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Mapping

from .canonical import canonical_json_bytes
from .constants import (
    DESIGN_INDEPENDENT_REVIEW_SHA256,
    DESIGN_PACKAGE_MANIFEST_SHA256,
    EXPECTED_RUN_RECORD,
    RECEIPT_BYTES,
    RECEIPT_FIXED_VALUES,
    REQUIRED_STUB_COUNTERS,
    RUN_RECORD_BYTES,
    RUN_RECORD_SHA256,
)
from .stub import StubCounters


_LOWER_HEX_64 = re.compile(r"^[a-f0-9]{64}$")


class PinError(ValueError):
    """An external receipt authority pin is inadmissible."""


class DeterminismError(ValueError):
    """A semantic run-record fact differs from the frozen exact object."""


class RecordEncodingError(ValueError):
    """Canonical record or receipt bytes differ from the frozen encoding."""


@dataclass(frozen=True)
class ExternalPins:
    assembly_implementation_manifest_sha256: str
    design_package_manifest_sha256: str
    design_independent_review_sha256: str


@dataclass(frozen=True)
class RunObservation:
    actual_response_sha256: str
    answer_validation_error_count: int
    denied_input_access_count: int
    retry_count: int
    response_frames: int
    final_frames: int
    transport_calls: int
    stub_script_frame_count: int
    stub_yielded_frame_count: int
    stub_unconsumed_frame_count_on_close: int


@dataclass(frozen=True)
class ReceiptMaterial:
    value: dict[str, object]
    raw: bytes
    sha256: str


def validate_external_pins(pins: ExternalPins) -> None:
    if type(pins) is not ExternalPins:
        raise PinError("external pins must use the exact ExternalPins type")
    values = (
        pins.assembly_implementation_manifest_sha256,
        pins.design_package_manifest_sha256,
        pins.design_independent_review_sha256,
    )
    if any(type(value) is not str or not _LOWER_HEX_64.fullmatch(value) for value in values):
        raise PinError("all receipt authority pins must be lowercase SHA-256")
    if pins.assembly_implementation_manifest_sha256 == "0" * 64:
        raise PinError("implementation manifest pin must not be a zero placeholder")
    if pins.design_package_manifest_sha256 != DESIGN_PACKAGE_MANIFEST_SHA256:
        raise PinError("design package manifest pin is not the current v0.5 authority")
    if pins.design_independent_review_sha256 != DESIGN_INDEPENDENT_REVIEW_SHA256:
        raise PinError("design independent-review pin is not the current authority")


def _type_exact_equal(actual: object, expected: object) -> bool:
    return type(actual) is type(expected) and actual == expected


def build_run_record_v3(observation: RunObservation) -> dict[str, object]:
    if type(observation) is not RunObservation:
        raise DeterminismError("run observation type mismatch")
    record = dict(EXPECTED_RUN_RECORD)
    record.update(
        {
            "actual_response_sha256": observation.actual_response_sha256,
            "answer_validation_error_count": observation.answer_validation_error_count,
            "denied_input_access_count": observation.denied_input_access_count,
            "retry_count": observation.retry_count,
            "response_frames": observation.response_frames,
            "final_frames": observation.final_frames,
            "transport_calls": observation.transport_calls,
            "stub_script_frame_count": observation.stub_script_frame_count,
            "stub_yielded_frame_count": observation.stub_yielded_frame_count,
            "stub_unconsumed_frame_count_on_close": (
                observation.stub_unconsumed_frame_count_on_close
            ),
        }
    )
    audit_run_record_v3(record)
    return record


def audit_run_record_v3(record: Mapping[str, object]) -> None:
    if type(record) is not dict:
        raise DeterminismError("run record must be an exact dict")
    expected = dict(EXPECTED_RUN_RECORD)
    if len(record) != 38 or set(record) != set(expected):
        raise DeterminismError("run record field set mismatch")
    for key, expected_value in expected.items():
        if not _type_exact_equal(record[key], expected_value):
            raise DeterminismError(f"run record semantic mismatch: {key}")


def serialize_run_record_v3(record: Mapping[str, object]) -> bytes:
    audit_run_record_v3(record)
    raw = canonical_json_bytes(record)
    if len(raw) != RUN_RECORD_BYTES:
        raise RecordEncodingError("run-record-v3 canonical byte length mismatch")
    if hashlib.sha256(raw).hexdigest() != RUN_RECORD_SHA256:
        raise RecordEncodingError("run-record-v3 canonical hash mismatch")
    return raw


def build_receipt_v2(pins: ExternalPins, counters: StubCounters) -> ReceiptMaterial:
    validate_external_pins(pins)
    if type(counters) is not StubCounters:
        raise RecordEncodingError("receipt counters must use the exact StubCounters type")
    observed_counters = counters.five_counter_dict()
    if set(observed_counters) != set(REQUIRED_STUB_COUNTERS) or any(
        type(observed_counters[name]) is not int
        or observed_counters[name] != expected
        for name, expected in REQUIRED_STUB_COUNTERS.items()
    ):
        raise RecordEncodingError("receipt stub counters mismatch")
    value: dict[str, object] = dict(RECEIPT_FIXED_VALUES)
    value.update(
        {
            "assembly_implementation_manifest_sha256": (
                pins.assembly_implementation_manifest_sha256
            ),
            "design_package_manifest_sha256": pins.design_package_manifest_sha256,
            "design_independent_review_sha256": (
                pins.design_independent_review_sha256
            ),
        }
    )
    if len(value) != 21:
        raise RecordEncodingError("receipt-v2 field count mismatch")
    raw = canonical_json_bytes(value)
    if len(raw) != RECEIPT_BYTES:
        raise RecordEncodingError("receipt-v2 canonical byte length mismatch")
    return ReceiptMaterial(value=value, raw=raw, sha256=hashlib.sha256(raw).hexdigest())

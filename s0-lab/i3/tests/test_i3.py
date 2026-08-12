from __future__ import annotations

import ast
import hashlib
import itertools
import json
import sys
import unittest
from dataclasses import replace
from pathlib import Path


I3_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = I3_ROOT.parents[1]
sys.path[:0] = [
    str(I3_ROOT / "implementation"),
    str(REPO_ROOT / "s0-lab" / "i2" / "implementation"),
]

import s0_i2  # noqa: E402
import s0_i3  # noqa: E402
from s0_i2.canonical import ZERO64  # noqa: E402
from s0_i2.records import (  # noqa: E402
    EVENT_FIELD_ORDER,
    FROZEN_REGISTRY_ROLE_ORDER,
    I1_PUBLIC_RUNTIME_MANIFEST_SHA256,
    IMPORT_ROUTE_STATES,
)
from s0_i3.classifier import END_OBSERVATIONS, EVIDENCE_STATUSES, PHASES, STATUS_FIELDS  # noqa: E402
from s0_i3.contract import CONTRACT_SHA256  # noqa: E402
from s0_i3.errors import (  # noqa: E402
    I3Error,
    I3BindingError,
    I3ByteError,
    I3FieldError,
    I3HashError,
    I3InputError,
    I3RouteError,
    I3TupleError,
    I3UnsupportedBoundaryError,
    I3ValueError,
)
from s0_i3.records import (  # noqa: E402
    ADMISSION_FIELD_ORDER,
    OUTCOME_FIELD_ORDER,
    OUTCOME_SCHEMA_PREFIX,
)


def hex64(character: str) -> str:
    return character * 64


def signer_context() -> s0_i2.SignerRegistryContext:
    return s0_i2.bind_public_i1_signer_context(
        manifest_sha256=I1_PUBLIC_RUNTIME_MANIFEST_SHA256,
        registry_role_order=FROZEN_REGISTRY_ROLE_ORDER,
    )


def encode_values(values: dict[str, str], order: tuple[str, ...]) -> bytes:
    return ("\n".join(f"{name}={values[name]}" for name in order) + "\n").encode(
        "ascii"
    )


def synthetic_generator_self_test() -> tuple[int, int, str]:
    """Check the public generator's exact order/LF/hash primitives independently."""

    probe = {"alpha": "1", "beta": "2"}
    raw = encode_values(probe, ("alpha", "beta"))
    if raw != b"alpha=1\nbeta=2\n":
        raise AssertionError("synthetic encoder order/LF self-test failed")
    if hashlib.sha256(raw).hexdigest() != "5d4f0c6a7441ec3302dfd4b081759ea6bc0dbfaa02edd450b962b8b302e2d5fb":
        raise AssertionError("synthetic encoder hash self-test failed")
    if len(ADMISSION_FIELD_ORDER) != 21 or len(OUTCOME_FIELD_ORDER) != 26:
        raise AssertionError("synthetic schema-count self-test failed")
    return (21, 26, hashlib.sha256(raw).hexdigest())


def admission_values(
    route_class: str = "preactivation-context-v1",
    *,
    campaign: str = "5",
) -> dict[str, str]:
    source, destination = IMPORT_ROUTE_STATES[route_class]
    return {
        "import_admission_schema": "S0-SIGNER-IMPORT-ADMISSION-2",
        "authority_id": "control-host-preflight",
        "campaign_id": hex64(campaign),
        "ceremony_id": hex64("6"),
        "signer_id": "analysis",
        "import_class": route_class,
        "from_state": source,
        "to_state": destination,
        "package_sha256": hex64("9"),
        "package_object_id": hex64("a"),
        "attachment_capability_id": hex64("7"),
        "result_media_kind": "import-outcome-v1",
        "result_media_id": hex64("b"),
        "reserved_media_event_id": hex64("1"),
        "admission_frozen_media_event_id": hex64("2"),
        "pending_media_event_id": hex64("3"),
        "completion_media_event_id": hex64("4"),
        "outcome_schema": "S0-SIGNER-IMPORT-OUTCOME-1",
        "outcome_max_bytes": "2048",
        "admission_event_id": hex64("2"),
        "decision": "approved",
    }


def admission_case(
    route_class: str = "preactivation-context-v1",
) -> tuple[s0_i2.SignerRegistryContext, bytes, s0_i3.ImportAdmission, s0_i2.ImportRouteContext]:
    signers = signer_context()
    raw = s0_i3.serialize_import_admission(
        admission_values(route_class), signer_context=signers
    )
    admission = s0_i3.parse_import_admission(raw, signer_context=signers)
    context = s0_i2.bind_import_route_context(
        signer_context=signers,
        campaign_id=admission["campaign_id"],
        ceremony_id=admission["ceremony_id"],
        signer_id=admission["signer_id"],
        route_class=admission["import_class"],
        attachment_capability_id=admission["attachment_capability_id"],
        admission_record_sha256=admission.admission_record_sha256,
        media_object_sha256=admission["package_sha256"],
        media_object_id=admission["package_object_id"],
        result_media_id=admission["result_media_id"],
        reserved_media_event_id=admission["reserved_media_event_id"],
        admission_frozen_media_event_id=admission[
            "admission_frozen_media_event_id"
        ],
        pending_media_event_id=admission["pending_media_event_id"],
        completion_media_event_id=admission["completion_media_event_id"],
    )
    return signers, raw, admission, context


def outcome_values(
    admission: s0_i3.ImportAdmission,
    outcome_class: str = "accepted",
) -> dict[str, str]:
    source = admission["from_state"]
    destination = admission["to_state"]
    tuples = {
        "accepted": ("accepted", "none", destination, hex64("e")),
        "parse-rejected": ("rejected", "parse-rejected", source, hex64("d")),
        "validation-rejected": (
            "rejected",
            "validation-rejected",
            source,
            hex64("d"),
        ),
        "state-commit-failed": (
            "rejected",
            "state-commit-failed",
            "indeterminate",
            ZERO64,
        ),
    }
    decision, reason, after_state, after_configuration = tuples[outcome_class]
    values = {
        "import_outcome_schema": "S0-SIGNER-IMPORT-OUTCOME-1",
        "tcb_service_id": "S0-IMPORT-TRANSITION-TCB-1",
        "campaign_id": admission["campaign_id"],
        "ceremony_id": admission["ceremony_id"],
        "signer_id": admission["signer_id"],
        "import_class": admission["import_class"],
        "from_state": source,
        "to_state": destination,
        "package_sha256": admission["package_sha256"],
        "package_object_id": admission["package_object_id"],
        "attachment_capability_id": admission["attachment_capability_id"],
        "admission_event_id": admission["admission_event_id"],
        "admission_record_sha256": admission.admission_record_sha256,
        "result_media_kind": admission["result_media_kind"],
        "result_media_id": admission["result_media_id"],
        "reserved_media_event_id": admission["reserved_media_event_id"],
        "admission_frozen_media_event_id": admission[
            "admission_frozen_media_event_id"
        ],
        "pending_media_event_id": admission["pending_media_event_id"],
        "completion_media_event_id": admission["completion_media_event_id"],
        "before_state": source,
        "after_state": after_state,
        "before_configuration_state_sha256": hex64("d"),
        "after_configuration_state_sha256": after_configuration,
        "decision": decision,
        "reason": reason,
        "outcome_body_sha256": ZERO64,
    }
    body = encode_values(values, OUTCOME_FIELD_ORDER[:25])
    values["outcome_body_sha256"] = hashlib.sha256(body).hexdigest()
    return values


def outcome_case(
    outcome_class: str = "accepted",
    route_class: str = "preactivation-context-v1",
) -> tuple[
    s0_i2.SignerRegistryContext,
    bytes,
    s0_i3.ImportAdmission,
    s0_i2.ImportRouteContext,
    bytes,
    bytes,
]:
    signers, admission_raw, admission, context = admission_case(route_class)
    frame = s0_i3.serialize_import_outcome(
        outcome_values(admission, outcome_class), signer_context=signers
    )
    medium = frame + bytes(2048 - len(frame))
    return signers, admission_raw, admission, context, frame, medium


def facts(
    media: tuple[bytes, ...] | list[bytes],
    *,
    phase: str = "pending",
    end: str = "normal",
    status: str = "exact",
    overrides: dict[str, str] | None = None,
) -> s0_i3.ClassificationFactSet:
    statuses = {name: status for name in STATUS_FIELDS}
    statuses.update(overrides or {})
    return s0_i3.bind_classification_fact_set(
        last_durable_phase=phase,
        end_observation=end,
        outcome_media_observations=media,
        **statuses,
    )


def classify(
    admission_raw: bytes | None,
    media: tuple[bytes, ...] | list[bytes],
    context: s0_i2.ImportRouteContext,
    **kwargs: object,
) -> s0_i3.ImportClassification:
    return s0_i3.classify_import_attempt(
        admission_raw,
        facts(media, **kwargs),
        route_context=context,
    )


def event_values(
    classification: s0_i3.ImportClassification,
    context: s0_i2.ImportRouteContext,
) -> dict[str, str]:
    phase = classification.last_durable_phase
    pending = phase == "pending"
    direct_reserved = phase == "reserved"
    source, _destination = IMPORT_ROUTE_STATES[context.route_class]
    admission_bound = {
        "admission_event_id": context.admission_frozen_media_event_id,
        "admission_record_sha256": context.admission_record_sha256,
        "media_object_sha256": context.media_object_sha256,
        "media_object_id": context.media_object_id,
    }
    values = {
        "signer_media_event_schema": "S0-SIGNER-MEDIA-LEDGER-IMPORT-EVENT-1",
        "namespace": "signer-media",
        "sequence": "3" if pending else ("1" if direct_reserved else "2"),
        "previous_event_sha256": hex64("f"),
        "event_id": context.completion_media_event_id,
        "prior_route_event_id": (
            context.pending_media_event_id
            if pending
            else (
                context.reserved_media_event_id
                if direct_reserved
                else context.admission_frozen_media_event_id
            )
        ),
        "campaign_id": context.campaign_id,
        "ceremony_id": context.ceremony_id,
        "signer_id": context.signer_id,
        "route_kind": "import",
        "route_class": context.route_class,
        "request_id": ZERO64,
        "attachment_capability_id": context.attachment_capability_id,
        "admission_event_id": ZERO64 if direct_reserved else admission_bound["admission_event_id"],
        "admission_record_sha256": ZERO64 if direct_reserved else admission_bound["admission_record_sha256"],
        "media_object_sha256": ZERO64 if direct_reserved else admission_bound["media_object_sha256"],
        "media_object_id": ZERO64 if direct_reserved else admission_bound["media_object_id"],
        "result_media_id": context.result_media_id,
        "result_media_kind": "import-outcome-v1",
        "reserved_media_event_id": context.reserved_media_event_id,
        "admission_frozen_media_event_id": context.admission_frozen_media_event_id,
        "pending_media_event_id": context.pending_media_event_id,
        "completion_media_event_id": context.completion_media_event_id,
        "outcome_schema": "S0-SIGNER-IMPORT-OUTCOME-1",
        "outcome_frame_sha256": classification.outcome_frame_sha256,
        "outcome_class": classification.outcome_class,
        "before_appliance_state": classification.before_appliance_state,
        "after_appliance_state": classification.after_appliance_state,
        "state": "terminal",
        "terminal_from": phase,
        "decision": "rejected",
    }
    if classification.outcome_class == "accepted":
        values.update(state="consumed", terminal_from="none", decision="accepted")
    if classification.outcome_class == "none":
        values["terminal_from"] = phase
    if not pending:
        values["outcome_frame_sha256"] = ZERO64
        values["outcome_class"] = "none"
        values["before_appliance_state"] = "none"
        values["after_appliance_state"] = "none"
    return values


def event_bytes(
    classification: s0_i3.ImportClassification,
    context: s0_i2.ImportRouteContext,
) -> bytes:
    return s0_i2.serialize_import_event(
        event_values(classification, context), signer_context=context.signer_context
    )


class ContractTests(unittest.TestCase):
    def test_synthetic_generator_self_test(self) -> None:
        self.assertEqual(synthetic_generator_self_test()[:2], (21, 26))

    def test_exact_contract_and_mapping(self) -> None:
        path = I3_ROOT / "spec" / "import-decision-contract-v0.1.json"
        raw = path.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), CONTRACT_SHA256)
        document = s0_i3.verify_contract_file(path)
        self.assertEqual(document["records"]["import_admission"]["line_count"], 21)
        self.assertEqual(document["records"]["import_outcome"]["line_count"], 26)
        self.assertEqual(document["records"]["import_event"]["line_count"], 31)

    def test_contract_mutation_and_duplicate_key_fail(self) -> None:
        raw = (I3_ROOT / "spec" / "import-decision-contract-v0.1.json").read_bytes()
        with self.assertRaises(I3BindingError):
            s0_i3.verify_contract_bytes(raw.replace(b'"version": "0.1.0"', b'"version": "0.1.1"'))
        duplicate = raw.replace(b"{\n", b'{\n  "version": "0.1.0",\n', 1)
        with self.assertRaises(I3BindingError):
            s0_i3.verify_contract_bytes(duplicate)


class AdmissionCodecTests(unittest.TestCase):
    def test_all_routes_round_trip_and_hash(self) -> None:
        for route_class in IMPORT_ROUTE_STATES:
            with self.subTest(route_class=route_class):
                signers, raw, admission, _context = admission_case(route_class)
                self.assertEqual(len(admission.fields), 21)
                self.assertEqual(
                    s0_i3.serialize_import_admission(admission, signer_context=signers),
                    raw,
                )
                self.assertEqual(
                    s0_i3.hash_import_admission(raw, signer_context=signers),
                    hashlib.sha256(raw).hexdigest(),
                )

    def test_byte_defects_are_stable(self) -> None:
        signers, raw, _admission, _context = admission_case()
        first_lf = raw.index(b"\n")
        mutations = (
            b"\xef\xbb\xbf" + raw,
            raw.replace(b"\n", b"\r\n", 1),
            raw[:first_lf] + b"\x00" + raw[first_lf:],
            raw[:-1],
            raw[:first_lf] + b" " + raw[first_lf:],
            raw[: first_lf + 1] + b"\n" + raw[first_lf + 1 :],
            raw[:first_lf] + b"\x80" + raw[first_lf:],
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation[:8]), self.assertRaises(I3ByteError):
                s0_i3.parse_import_admission(mutation, signer_context=signers)

    def test_every_field_presence_order_and_name_is_exact(self) -> None:
        signers, raw, _admission, _context = admission_case()
        lines = raw.splitlines(keepends=True)
        for index in range(len(lines)):
            with self.subTest(kind="missing", index=index), self.assertRaises(I3FieldError):
                s0_i3.parse_import_admission(
                    b"".join(lines[:index] + lines[index + 1 :]),
                    signer_context=signers,
                )
            with self.subTest(kind="duplicate", index=index), self.assertRaises(I3FieldError):
                s0_i3.parse_import_admission(
                    b"".join(lines[:index] + [lines[index]] + lines[index:]),
                    signer_context=signers,
                )
        for index in range(len(lines) - 1):
            changed = list(lines)
            changed[index], changed[index + 1] = changed[index + 1], changed[index]
            with self.subTest(kind="reorder", index=index), self.assertRaises(I3FieldError):
                s0_i3.parse_import_admission(b"".join(changed), signer_context=signers)

    def test_route_signer_and_identifier_failures(self) -> None:
        signers = signer_context()
        base = admission_values()
        for name, value, error in (
            ("signer_id", "control-root-authority", I3ValueError),
            ("signer_id", "Analysis", I3ValueError),
            ("from_state", "active", I3RouteError),
            ("admission_event_id", hex64("4"), I3BindingError),
            ("result_media_id", ZERO64, I3ValueError),
        ):
            changed = dict(base)
            changed[name] = value
            with self.subTest(name=name, value=value), self.assertRaises(error):
                s0_i3.serialize_import_admission(changed, signer_context=signers)

    def test_every_admission_field_value_is_validated(self) -> None:
        signers = signer_context()
        base = admission_values()
        mutations = {
            "import_admission_schema": "wrong",
            "authority_id": "wrong",
            "campaign_id": "g" * 64,
            "ceremony_id": "g" * 64,
            "signer_id": "control-root-authority",
            "import_class": "wrong",
            "from_state": "wrong",
            "to_state": "wrong",
            "package_sha256": "g" * 64,
            "package_object_id": "g" * 64,
            "attachment_capability_id": "g" * 64,
            "result_media_kind": "wrong",
            "result_media_id": ZERO64,
            "reserved_media_event_id": ZERO64,
            "admission_frozen_media_event_id": ZERO64,
            "pending_media_event_id": ZERO64,
            "completion_media_event_id": ZERO64,
            "outcome_schema": "wrong",
            "outcome_max_bytes": "2049",
            "admission_event_id": hex64("f"),
            "decision": "rejected",
        }
        self.assertEqual(set(mutations), set(ADMISSION_FIELD_ORDER))
        for name, value in mutations.items():
            changed = dict(base)
            changed[name] = value
            with self.subTest(name=name), self.assertRaises(I3Error):
                s0_i3.serialize_import_admission(changed, signer_context=signers)
        for left, right in itertools.combinations(
            (
                "result_media_id",
                "reserved_media_event_id",
                "admission_frozen_media_event_id",
                "pending_media_event_id",
                "completion_media_event_id",
            ),
            2,
        ):
            changed = dict(base)
            changed[right] = changed[left]
            if right == "admission_frozen_media_event_id":
                changed["admission_event_id"] = changed[right]
            with self.subTest(left=left, right=right), self.assertRaises(I3BindingError):
                s0_i3.serialize_import_admission(changed, signer_context=signers)


class OutcomeCodecTests(unittest.TestCase):
    def test_four_tuples_round_trip_body_and_frame_hash(self) -> None:
        for route_class, outcome_class in itertools.product(
            IMPORT_ROUTE_STATES,
            (
                "accepted",
                "parse-rejected",
                "validation-rejected",
                "state-commit-failed",
            ),
        ):
            with self.subTest(route=route_class, outcome=outcome_class):
                signers, _raw, admission, _context = admission_case(route_class)
                frame = s0_i3.serialize_import_outcome(
                    outcome_values(admission, outcome_class), signer_context=signers
                )
                outcome = s0_i3.parse_import_outcome_frame(
                    frame, signer_context=signers
                )
                self.assertEqual(outcome.outcome_class, outcome_class)
                self.assertEqual(len(outcome.fields), 26)
                self.assertEqual(outcome.outcome_body_sha256, hashlib.sha256(b"".join(frame.splitlines(keepends=True)[:25])).hexdigest())
                self.assertEqual(outcome.outcome_frame_sha256, hashlib.sha256(frame).hexdigest())
                self.assertEqual(s0_i3.serialize_import_outcome(outcome, signer_context=signers), frame)

    def test_every_outcome_field_presence_order_and_name_is_exact(self) -> None:
        signers, _raw, _admission, _context, frame, _medium = outcome_case()
        lines = frame.splitlines(keepends=True)
        for index in range(len(lines)):
            with self.subTest(kind="missing", index=index), self.assertRaises(I3FieldError):
                s0_i3.parse_import_outcome_frame(
                    b"".join(lines[:index] + lines[index + 1 :]),
                    signer_context=signers,
                )
            with self.subTest(kind="duplicate", index=index), self.assertRaises(I3FieldError):
                s0_i3.parse_import_outcome_frame(
                    b"".join(lines[:index] + [lines[index]] + lines[index:]),
                    signer_context=signers,
                )
        for index in range(len(lines) - 1):
            changed = list(lines)
            changed[index], changed[index + 1] = changed[index + 1], changed[index]
            with self.subTest(kind="reorder", index=index), self.assertRaises(I3FieldError):
                s0_i3.parse_import_outcome_frame(
                    b"".join(changed), signer_context=signers
                )

    def test_outcome_byte_defects_are_stable(self) -> None:
        signers, _raw, _admission, _context, frame, _medium = outcome_case()
        first_lf = frame.index(b"\n")
        mutations = (
            b"\xef\xbb\xbf" + frame,
            frame.replace(b"\n", b"\r\n", 1),
            frame[:first_lf] + b"\x00" + frame[first_lf:],
            frame[:-1],
            frame[:first_lf] + b" " + frame[first_lf:],
            frame[: first_lf + 1] + b"\n" + frame[first_lf + 1 :],
            frame[:first_lf] + b"\x80" + frame[first_lf:],
        )
        for mutation in mutations:
            with self.subTest(mutation=mutation[:8]), self.assertRaises(I3ByteError):
                s0_i3.parse_import_outcome_frame(mutation, signer_context=signers)

    def test_hash_tuple_and_route_failures_are_distinct(self) -> None:
        signers, _raw, admission, _context = admission_case()
        bad_hash = outcome_values(admission)
        bad_hash["outcome_body_sha256"] = ZERO64
        with self.assertRaises(I3HashError):
            s0_i3.serialize_import_outcome(bad_hash, signer_context=signers)
        bad_tuple = outcome_values(admission)
        bad_tuple["after_state"] = admission["from_state"]
        bad_tuple["outcome_body_sha256"] = hashlib.sha256(
            encode_values(bad_tuple, OUTCOME_FIELD_ORDER[:25])
        ).hexdigest()
        with self.assertRaises(I3TupleError):
            s0_i3.serialize_import_outcome(bad_tuple, signer_context=signers)
        bad_route = outcome_values(admission)
        bad_route["from_state"] = "active"
        bad_route["before_state"] = "active"
        bad_route["outcome_body_sha256"] = hashlib.sha256(
            encode_values(bad_route, OUTCOME_FIELD_ORDER[:25])
        ).hexdigest()
        with self.assertRaises(I3RouteError):
            s0_i3.serialize_import_outcome(bad_route, signer_context=signers)

    def test_cross_record_binding_each_field(self) -> None:
        signers, _raw, admission, _context, frame, _medium = outcome_case()
        outcome = s0_i3.parse_import_outcome_frame(frame, signer_context=signers)
        s0_i3.validate_outcome_binding(outcome, admission, signer_context=signers)
        for name in (
            "campaign_id",
            "ceremony_id",
            "package_sha256",
            "package_object_id",
            "attachment_capability_id",
            "result_media_id",
            "reserved_media_event_id",
            "admission_frozen_media_event_id",
            "pending_media_event_id",
            "completion_media_event_id",
        ):
            changed = outcome_values(admission)
            changed[name] = hex64("f")
            if name == "admission_frozen_media_event_id":
                changed["admission_event_id"] = hex64("f")
            changed["outcome_body_sha256"] = hashlib.sha256(
                encode_values(changed, OUTCOME_FIELD_ORDER[:25])
            ).hexdigest()
            other = s0_i3.parse_import_outcome_frame(
                encode_values(changed, OUTCOME_FIELD_ORDER), signer_context=signers
            )
            with self.subTest(name=name), self.assertRaises(I3BindingError):
                s0_i3.validate_outcome_binding(other, admission, signer_context=signers)

    def test_every_outcome_field_value_is_validated(self) -> None:
        signers, _raw, admission, _context = admission_case()
        base = outcome_values(admission)
        mutations = {
            "import_outcome_schema": "wrong",
            "tcb_service_id": "wrong",
            "campaign_id": "g" * 64,
            "ceremony_id": "g" * 64,
            "signer_id": "control-root-authority",
            "import_class": "wrong",
            "from_state": "wrong",
            "to_state": "wrong",
            "package_sha256": "g" * 64,
            "package_object_id": "g" * 64,
            "attachment_capability_id": "g" * 64,
            "admission_event_id": "g" * 64,
            "admission_record_sha256": "g" * 64,
            "result_media_kind": "wrong",
            "result_media_id": ZERO64,
            "reserved_media_event_id": ZERO64,
            "admission_frozen_media_event_id": ZERO64,
            "pending_media_event_id": ZERO64,
            "completion_media_event_id": ZERO64,
            "before_state": "wrong",
            "after_state": "wrong",
            "before_configuration_state_sha256": ZERO64,
            "after_configuration_state_sha256": hex64("d"),
            "decision": "rejected",
            "reason": "wrong",
            "outcome_body_sha256": ZERO64,
        }
        self.assertEqual(set(mutations), set(OUTCOME_FIELD_ORDER))
        for name, value in mutations.items():
            changed = dict(base)
            changed[name] = value
            if name != "outcome_body_sha256":
                changed["outcome_body_sha256"] = hashlib.sha256(
                    encode_values(changed, OUTCOME_FIELD_ORDER[:25])
                ).hexdigest()
            with self.subTest(name=name), self.assertRaises(I3Error):
                s0_i3.serialize_import_outcome(changed, signer_context=signers)


class ClassificationTests(unittest.TestCase):
    def test_every_named_row(self) -> None:
        signers, admission_raw, admission, context, frame, medium = outcome_case()
        cases: list[tuple[str, s0_i3.ImportClassification]] = []
        cases.append(("PRE-R", classify(admission_raw, (medium,), context, phase="reserved")))
        cases.append(("PRE-A", classify(admission_raw, (medium,), context, phase="admission-frozen")))
        cases.append(("P-CRASH", classify(admission_raw, (medium,), context, end="abnormal")))
        cases.append(("P-MISSING", classify(admission_raw, (bytes(2048),), context)))
        cases.append(("P-DUPLICATE", classify(admission_raw, (medium, medium), context)))
        cases.append(("P-DISAGREE-H", classify(admission_raw, (medium,), context, end="unknown")))
        cases.append(("P-DISAGREE-Z", classify(admission_raw, (), context)))
        for outcome_class, row in (
            ("parse-rejected", "P-PARSE-REJECTED"),
            ("validation-rejected", "P-VALIDATION-REJECTED"),
            ("state-commit-failed", "P-STATE-COMMIT-FAILED"),
            ("accepted", "P-ACCEPTED"),
        ):
            _s, a_raw, _a, route, _f, route_medium = outcome_case(outcome_class)
            cases.append((row, classify(a_raw, (route_medium,), route)))
        self.assertEqual([expected for expected, _ in cases], [result.selected_row for _, result in cases])
        self.assertTrue(all(result.destination_authority == "unavailable" for _, result in cases))
        self.assertEqual(signers.registry_role_order, signer_context().registry_role_order)
        self.assertLess(len(frame), 2048)

    def test_missing_duplicate_and_malformed_boundaries(self) -> None:
        _signers, admission_raw, _admission, context, frame, medium = outcome_case()
        partial = (b"partial=x\n" * 12) + bytes(2048 - len(b"partial=x\n" * 12))
        self.assertEqual(classify(admission_raw, (partial,), context).outcome_class, "missing")
        nonzero_tail = frame + b"\x01" + bytes(2048 - len(frame) - 1)
        self.assertEqual(classify(admission_raw, (nonzero_tail,), context).outcome_class, "duplicate")
        two_prefixes = (
            frame
            + OUTCOME_SCHEMA_PREFIX
            + bytes(2048 - len(frame) - len(OUTCOME_SCHEMA_PREFIX))
        )
        self.assertEqual(classify(admission_raw, (two_prefixes,), context).outcome_class, "duplicate")
        bad_hash_frame = frame[:-2] + (b"0" if frame[-2:-1] != b"0" else b"1") + b"\n"
        bad_hash_medium = bad_hash_frame + bytes(2048 - len(bad_hash_frame))
        self.assertEqual(classify(admission_raw, (bad_hash_medium,), context).selected_row, "P-DISAGREE-Z")
        offset = b"x" + frame + bytes(2048 - len(frame) - 1)
        self.assertEqual(classify(admission_raw, (offset,), context).selected_row, "P-DISAGREE-Z")
        self.assertEqual(classify(admission_raw, (medium[:-1],), context).selected_row, "P-DISAGREE-Z")

    def test_b01_end_cross_and_statuses_preserve_h(self) -> None:
        for outcome_class in (
            "accepted",
            "parse-rejected",
            "validation-rejected",
            "state-commit-failed",
        ):
            _s, admission_raw, _a, context, _frame, medium = outcome_case(outcome_class)
            exact = classify(admission_raw, (medium,), context)
            for end, expected_class, expected_hash in (
                ("normal", outcome_class, exact.outcome_frame_sha256),
                ("unknown", "disagreement", exact.outcome_frame_sha256),
                ("not-started", "disagreement", exact.outcome_frame_sha256),
                ("abnormal", "crash", ZERO64),
            ):
                result = classify(admission_raw, (medium,), context, end=end)
                with self.subTest(outcome=outcome_class, end=end):
                    self.assertEqual(result.outcome_class, expected_class)
                    self.assertEqual(result.outcome_frame_sha256, expected_hash)
            for name, value in itertools.product(STATUS_FIELDS, ("conflict", "unavailable")):
                result = classify(
                    admission_raw,
                    (medium,),
                    context,
                    overrides={name: value},
                )
                with self.subTest(outcome=outcome_class, status=name, value=value):
                    self.assertEqual(result.selected_row, "P-DISAGREE-H")
                    self.assertEqual(result.outcome_frame_sha256, exact.outcome_frame_sha256)

    def test_cross_route_canonical_frame_uses_expected_route_source(self) -> None:
        signers, admission_raw, _admission, context = admission_case(
            "preactivation-context-v1"
        )
        _other_signers, _other_raw, other_admission, _other_context = admission_case(
            "registry-binding-v1"
        )
        values = outcome_values(other_admission, "accepted")
        values["campaign_id"] = context.campaign_id
        values["ceremony_id"] = context.ceremony_id
        values["signer_id"] = context.signer_id
        values["package_sha256"] = context.media_object_sha256
        values["package_object_id"] = context.media_object_id
        values["attachment_capability_id"] = context.attachment_capability_id
        values["admission_event_id"] = context.admission_frozen_media_event_id
        values["admission_record_sha256"] = context.admission_record_sha256
        values["result_media_id"] = context.result_media_id
        values["reserved_media_event_id"] = context.reserved_media_event_id
        values["admission_frozen_media_event_id"] = context.admission_frozen_media_event_id
        values["pending_media_event_id"] = context.pending_media_event_id
        values["completion_media_event_id"] = context.completion_media_event_id
        values["outcome_body_sha256"] = hashlib.sha256(
            encode_values(values, OUTCOME_FIELD_ORDER[:25])
        ).hexdigest()
        frame = s0_i3.serialize_import_outcome(values, signer_context=signers)
        medium = frame + bytes(2048 - len(frame))
        result = classify(admission_raw, (medium,), context)
        self.assertEqual(result.selected_row, "P-DISAGREE-H")
        self.assertEqual(result.before_appliance_state, "key-generated")
        self.assertEqual(result.after_appliance_state, "indeterminate")

    def test_media_sequence_type_and_count_are_single_source(self) -> None:
        _s, admission_raw, _a, context, _frame, medium = outcome_case()
        self.assertEqual(classify(admission_raw, [], context).selected_row, "P-DISAGREE-Z")
        self.assertEqual(classify(admission_raw, [bytes(2048)], context).selected_row, "P-MISSING")
        self.assertEqual(classify(admission_raw, [medium, medium], context).selected_row, "P-DUPLICATE")
        for outer in (medium, iter([medium]), {medium}):
            with self.subTest(outer=type(outer).__name__), self.assertRaises(I3InputError):
                facts(outer)  # type: ignore[arg-type]
        with self.assertRaises(I3InputError):
            facts((bytearray(medium),))  # type: ignore[list-item]
        with self.assertRaises(I3InputError):
            s0_i3.bind_classification_fact_set(
                end_observation="normal",
                outcome_media_observations=(medium,),
                **{name: "exact" for name in STATUS_FIELDS},
            )
        with self.assertRaises(I3InputError):
            s0_i3.bind_classification_fact_set(
                last_durable_phase="pending",
                end_observation="normal",
                outcome_media_observations=(medium,),
                outcome_media_count=1,
                **{name: "exact" for name in STATUS_FIELDS},
            )
        with self.assertRaises(I3InputError):
            s0_i3.classify_import_attempt(
                admission_raw,
                facts((medium,)),
                route_context=context,
                outcome_media_count=1,
            )

    def test_all_closed_enum_cartesian_inputs_are_total(self) -> None:
        _s, admission_raw, _a, context, _frame, _medium = outcome_case()
        media = (bytes(2048),)
        count = 0
        for phase, end, status_values in itertools.product(
            sorted(PHASES),
            sorted(END_OBSERVATIONS),
            itertools.product(sorted(EVIDENCE_STATUSES), repeat=len(STATUS_FIELDS)),
        ):
            overrides = dict(zip(STATUS_FIELDS, status_values, strict=True))
            result = classify(
                admission_raw,
                media,
                context,
                phase=phase,
                end=end,
                overrides=overrides,
            )
            self.assertIn(
                result.outcome_class,
                {
                    "none",
                    "crash",
                    "missing",
                    "disagreement",
                },
            )
            count += 1
        self.assertEqual(count, 3 * 4 * (3**8))

    def test_input_errors_do_not_leak_runtime_exceptions(self) -> None:
        _s, admission_raw, _a, context, _frame, medium = outcome_case()
        for kwargs in (
            {"last_durable_phase": "bad"},
            {"end_observation": "bad"},
            {"launch_admission_status": "bad"},
        ):
            base: dict[str, object] = {
                "last_durable_phase": "pending",
                "end_observation": "normal",
                "outcome_media_observations": (medium,),
                **{name: "exact" for name in STATUS_FIELDS},
            }
            base.update(kwargs)
            with self.subTest(kwargs=kwargs), self.assertRaises(I3InputError):
                s0_i3.bind_classification_fact_set(**base)  # type: ignore[arg-type]
        good = facts((medium,))
        forged = replace(good, _provenance=object())
        with self.assertRaises(I3InputError):
            s0_i3.classify_import_attempt(admission_raw, forged, route_context=context)
        with self.assertRaises(I3InputError):
            s0_i3.classify_import_attempt("not-bytes", good, route_context=context)  # type: ignore[arg-type]


class FinalizationTests(unittest.TestCase):
    def test_every_class_exact_persisted_event(self) -> None:
        cases: list[tuple[s0_i3.ImportClassification, s0_i2.ImportRouteContext]] = []
        _s, a_raw, _a, context, _frame, medium = outcome_case()
        cases.extend(
            (
                classify(a_raw, (medium,), context, phase="reserved"),
                context,
            )
            for _ in range(1)
        )
        cases.extend(
            (
                classify(a_raw, (medium,), context, phase="admission-frozen"),
                context,
            )
            for _ in range(1)
        )
        cases.append((classify(a_raw, (medium,), context, end="abnormal"), context))
        cases.append((classify(a_raw, (bytes(2048),), context), context))
        cases.append((classify(a_raw, (medium, medium), context), context))
        cases.append((classify(a_raw, (medium,), context, end="unknown"), context))
        cases.append((classify(a_raw, (), context), context))
        for outcome_class in (
            "accepted",
            "parse-rejected",
            "validation-rejected",
            "state-commit-failed",
        ):
            _s2, a2, _a2, c2, _f2, m2 = outcome_case(outcome_class)
            cases.append((classify(a2, (m2,), c2), c2))
        seen: set[str] = set()
        for classification, route in cases:
            decision = s0_i3.finalize_import_attempt(
                classification,
                event_bytes(classification, route),
                "persisted",
                signer_context=route.signer_context,
            )
            seen.add(classification.outcome_class)
            with self.subTest(outcome=classification.outcome_class, row=classification.selected_row):
                if classification.outcome_class == "accepted":
                    self.assertEqual(decision.disposition, "consumed-accepted")
                    self.assertEqual(decision.destination_authority, "available")
                    self.assertEqual(decision.destination_state, classification.after_appliance_state)
                else:
                    self.assertEqual(decision.disposition, "terminal-rejected")
                    self.assertEqual(decision.destination_authority, "unavailable")
        self.assertEqual(
            seen,
            {
                "none",
                "accepted",
                "parse-rejected",
                "validation-rejected",
                "state-commit-failed",
                "crash",
                "missing",
                "duplicate",
                "disagreement",
            },
        )

    def test_wrong_or_unpersisted_event_never_grants_authority(self) -> None:
        _s, a_raw, _a, context, _frame, medium = outcome_case()
        accepted = classify(a_raw, (medium,), context)
        exact_event = event_bytes(accepted, context)
        for append in ("conflict", "unavailable", "failed"):
            decision = s0_i3.finalize_import_attempt(
                accepted, exact_event, append, signer_context=context.signer_context
            )
            self.assertEqual(decision.disposition, "no-completion-claim")
        self.assertEqual(
            s0_i3.finalize_import_attempt(
                accepted, None, "persisted", signer_context=context.signer_context
            ).disposition,
            "no-completion-claim",
        )
        wrong = dict(event_values(accepted, context))
        wrong["outcome_frame_sha256"] = hex64("e")
        wrong_event = s0_i2.serialize_import_event(
            wrong, signer_context=context.signer_context
        )
        self.assertEqual(
            s0_i3.finalize_import_attempt(
                accepted,
                wrong_event,
                "persisted",
                signer_context=context.signer_context,
            ).disposition,
            "no-completion-claim",
        )
        with self.assertRaises(I3InputError):
            s0_i3.finalize_import_attempt(
                accepted, exact_event, "unknown", signer_context=context.signer_context
            )


class BoundaryAndSourceTests(unittest.TestCase):
    def test_closed_boundaries_are_named_and_not_executed(self) -> None:
        for operation in (
            s0_i3.validate_durable_ledger,
            s0_i3.validate_witness,
            s0_i3.enforce_platform_isolation,
            s0_i3.run_s0,
        ):
            with self.subTest(operation=operation.__name__), self.assertRaises(I3UnsupportedBoundaryError):
                operation()

    def test_implementation_has_no_operational_imports(self) -> None:
        forbidden = {
            "subprocess",
            "socket",
            "requests",
            "urllib",
            "http",
            "asyncio",
            "multiprocessing",
            "ctypes",
            "winreg",
        }
        imported: set[str] = set()
        for path in sorted((I3_ROOT / "implementation" / "s0_i3").glob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imported.update(alias.name.split(".")[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imported.add(node.module.split(".")[0])
        self.assertFalse(imported & forbidden)


if __name__ == "__main__":
    if sys.argv[1:] == ["--self-test-generator"]:
        counts = synthetic_generator_self_test()
        print(
            "SYNTHETIC_GENERATOR_SELFTEST=PASS "
            f"ADMISSION_FIELDS={counts[0]} OUTCOME_FIELDS={counts[1]}"
        )
    else:
        unittest.main()

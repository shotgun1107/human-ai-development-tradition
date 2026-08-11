from __future__ import annotations

import ast
import hashlib
import json
import sys
import unittest
from dataclasses import replace
from pathlib import Path


I2_ROOT = Path(__file__).resolve().parents[1]
IMPLEMENTATION_ROOT = I2_ROOT / "implementation"
sys.path.insert(0, str(IMPLEMENTATION_ROOT))

import s0_i2  # noqa: E402
from s0_i2.canonical import ZERO64  # noqa: E402
from s0_i2.contract import (  # noqa: E402
    CONTRACT_SHA256,
    I1_PUBLIC_RUNTIME_JSON_SHA256,
)
from s0_i2.errors import (  # noqa: E402
    BindingError,
    CanonicalRecordError,
    LifecycleError,
    UnsupportedBoundaryError,
    VectorBindingError,
)
from s0_i2.records import (  # noqa: E402
    EVENT_FIELD_ORDER,
    FROZEN_REGISTRY_ROLE_ORDER,
    I1_PUBLIC_RUNTIME_MANIFEST_SHA256,
    IMPORT_ROUTE_STATES,
    SignerRegistryContext,
)
from s0_i2.vectors import (  # noqa: E402
    TRI2_VEC_02_ARTIFACT_SHA256,
    TRI2_VEC_02_DECISION_SHA256,
    TRI2_VEC_02_DERIVATION_SHA256,
    TRI2_VEC_02_ROWS,
)


def hex64(character: str) -> str:
    return character * 64


def signer_context() -> s0_i2.SignerRegistryContext:
    return s0_i2.bind_public_i1_signer_context(
        manifest_sha256=I1_PUBLIC_RUNTIME_MANIFEST_SHA256,
        registry_role_order=FROZEN_REGISTRY_ROLE_ORDER,
    )


def route_context(
    *,
    route_class: str = "preactivation-context-v1",
    campaign_character: str = "5",
    event_characters: tuple[str, str, str, str] = ("1", "2", "3", "4"),
    result_media_character: str = "b",
) -> s0_i2.ImportRouteContext:
    return s0_i2.bind_import_route_context(
        signer_context=signer_context(),
        campaign_id=hex64(campaign_character),
        ceremony_id=hex64("6"),
        signer_id="analysis",
        route_class=route_class,
        attachment_capability_id=hex64("7"),
        admission_record_sha256=hex64("8"),
        media_object_sha256=hex64("9"),
        media_object_id=hex64("a"),
        result_media_id=hex64(result_media_character),
        reserved_media_event_id=hex64(event_characters[0]),
        admission_frozen_media_event_id=hex64(event_characters[1]),
        pending_media_event_id=hex64(event_characters[2]),
        completion_media_event_id=hex64(event_characters[3]),
    )


def event_values(
    context: s0_i2.ImportRouteContext,
    variant: str,
    *,
    sequence: str = "0",
    previous_event_sha256: str = ZERO64,
    disagreement_frame_sha256: str = ZERO64,
) -> dict[str, str]:
    values = {
        "signer_media_event_schema": "S0-SIGNER-MEDIA-LEDGER-IMPORT-EVENT-1",
        "namespace": "signer-media",
        "sequence": sequence,
        "previous_event_sha256": previous_event_sha256,
        "event_id": context.reserved_media_event_id,
        "prior_route_event_id": ZERO64,
        "campaign_id": context.campaign_id,
        "ceremony_id": context.ceremony_id,
        "signer_id": context.signer_id,
        "route_kind": "import",
        "route_class": context.route_class,
        "request_id": ZERO64,
        "attachment_capability_id": context.attachment_capability_id,
        "admission_event_id": ZERO64,
        "admission_record_sha256": ZERO64,
        "media_object_sha256": ZERO64,
        "media_object_id": ZERO64,
        "result_media_id": context.result_media_id,
        "result_media_kind": "import-outcome-v1",
        "reserved_media_event_id": context.reserved_media_event_id,
        "admission_frozen_media_event_id": context.admission_frozen_media_event_id,
        "pending_media_event_id": context.pending_media_event_id,
        "completion_media_event_id": context.completion_media_event_id,
        "outcome_schema": "S0-SIGNER-IMPORT-OUTCOME-1",
        "outcome_frame_sha256": ZERO64,
        "outcome_class": "none",
        "before_appliance_state": "none",
        "after_appliance_state": "none",
        "state": "reserved",
        "terminal_from": "none",
        "decision": "reserved",
    }
    admission_bound = {
        "admission_event_id": context.admission_frozen_media_event_id,
        "admission_record_sha256": context.admission_record_sha256,
        "media_object_sha256": context.media_object_sha256,
        "media_object_id": context.media_object_id,
    }
    source, destination = IMPORT_ROUTE_STATES[context.route_class]
    variants: dict[str, dict[str, str]] = {
        "reserved": {},
        "admission-frozen": {
            "event_id": context.admission_frozen_media_event_id,
            "prior_route_event_id": context.reserved_media_event_id,
            **admission_bound,
            "state": "admission-frozen",
            "decision": "approved",
        },
        "pending": {
            "event_id": context.pending_media_event_id,
            "prior_route_event_id": context.admission_frozen_media_event_id,
            **admission_bound,
            "before_appliance_state": source,
            "state": "pending",
            "decision": "executing",
        },
        "direct-terminal-reserved": {
            "event_id": context.completion_media_event_id,
            "prior_route_event_id": context.reserved_media_event_id,
            "state": "terminal",
            "terminal_from": "reserved",
            "decision": "rejected",
        },
        "direct-terminal-admission-frozen": {
            "event_id": context.completion_media_event_id,
            "prior_route_event_id": context.admission_frozen_media_event_id,
            **admission_bound,
            "state": "terminal",
            "terminal_from": "admission-frozen",
            "decision": "rejected",
        },
        "accepted": {
            "event_id": context.completion_media_event_id,
            "prior_route_event_id": context.pending_media_event_id,
            **admission_bound,
            "outcome_frame_sha256": hex64("c"),
            "outcome_class": "accepted",
            "before_appliance_state": source,
            "after_appliance_state": destination,
            "state": "consumed",
            "decision": "accepted",
        },
        "parse-rejected": {
            "event_id": context.completion_media_event_id,
            "prior_route_event_id": context.pending_media_event_id,
            **admission_bound,
            "outcome_frame_sha256": hex64("c"),
            "outcome_class": "parse-rejected",
            "before_appliance_state": source,
            "after_appliance_state": source,
            "state": "terminal",
            "terminal_from": "pending",
            "decision": "rejected",
        },
        "validation-rejected": {
            "event_id": context.completion_media_event_id,
            "prior_route_event_id": context.pending_media_event_id,
            **admission_bound,
            "outcome_frame_sha256": hex64("c"),
            "outcome_class": "validation-rejected",
            "before_appliance_state": source,
            "after_appliance_state": source,
            "state": "terminal",
            "terminal_from": "pending",
            "decision": "rejected",
        },
        "state-commit-failed": {
            "event_id": context.completion_media_event_id,
            "prior_route_event_id": context.pending_media_event_id,
            **admission_bound,
            "outcome_frame_sha256": hex64("c"),
            "outcome_class": "state-commit-failed",
            "before_appliance_state": source,
            "after_appliance_state": "indeterminate",
            "state": "terminal",
            "terminal_from": "pending",
            "decision": "rejected",
        },
        "crash": {
            "event_id": context.completion_media_event_id,
            "prior_route_event_id": context.pending_media_event_id,
            **admission_bound,
            "outcome_class": "crash",
            "before_appliance_state": source,
            "after_appliance_state": "indeterminate",
            "state": "terminal",
            "terminal_from": "pending",
            "decision": "rejected",
        },
        "missing": {
            "event_id": context.completion_media_event_id,
            "prior_route_event_id": context.pending_media_event_id,
            **admission_bound,
            "outcome_class": "missing",
            "before_appliance_state": source,
            "after_appliance_state": "indeterminate",
            "state": "terminal",
            "terminal_from": "pending",
            "decision": "rejected",
        },
        "duplicate": {
            "event_id": context.completion_media_event_id,
            "prior_route_event_id": context.pending_media_event_id,
            **admission_bound,
            "outcome_class": "duplicate",
            "before_appliance_state": source,
            "after_appliance_state": "indeterminate",
            "state": "terminal",
            "terminal_from": "pending",
            "decision": "rejected",
        },
        "disagreement": {
            "event_id": context.completion_media_event_id,
            "prior_route_event_id": context.pending_media_event_id,
            **admission_bound,
            "outcome_frame_sha256": disagreement_frame_sha256,
            "outcome_class": "disagreement",
            "before_appliance_state": source,
            "after_appliance_state": "indeterminate",
            "state": "terminal",
            "terminal_from": "pending",
            "decision": "rejected",
        },
    }
    values.update(variants[variant])
    return values


def parsed_event(
    context: s0_i2.ImportRouteContext,
    variant: str,
    *,
    sequence: str,
    previous_event_sha256: str,
    disagreement_frame_sha256: str = ZERO64,
) -> s0_i2.ImportLedgerEvent:
    raw = s0_i2.serialize_import_event(
        event_values(
            context,
            variant,
            sequence=sequence,
            previous_event_sha256=previous_event_sha256,
            disagreement_frame_sha256=disagreement_frame_sha256,
        ),
        signer_context=context.signer_context,
    )
    return s0_i2.parse_import_event(raw, signer_context=context.signer_context)


def parsed_route(
    completion_variant: str = "accepted",
    *,
    disagreement_frame_sha256: str = ZERO64,
    context: s0_i2.ImportRouteContext | None = None,
    route_class: str = "preactivation-context-v1",
) -> tuple[s0_i2.ImportRouteContext, tuple[s0_i2.ImportLedgerEvent, ...]]:
    context = context or route_context(route_class=route_class)
    variants = ("reserved", "admission-frozen", "pending", completion_variant)
    previous = ZERO64
    events: list[s0_i2.ImportLedgerEvent] = []
    for sequence, variant in enumerate(variants):
        event = parsed_event(
            context,
            variant,
            sequence=str(sequence),
            previous_event_sha256=previous,
            disagreement_frame_sha256=disagreement_frame_sha256,
        )
        events.append(event)
        previous = event.event_sha256
    return context, tuple(events)


def parsed_early_route(
    context: s0_i2.ImportRouteContext, *, after_admission: bool
) -> tuple[s0_i2.ImportLedgerEvent, ...]:
    reserved = parsed_event(
        context, "reserved", sequence="0", previous_event_sha256=ZERO64
    )
    if not after_admission:
        terminal = parsed_event(
            context,
            "direct-terminal-reserved",
            sequence="1",
            previous_event_sha256=reserved.event_sha256,
        )
        return (reserved, terminal)
    admission = parsed_event(
        context,
        "admission-frozen",
        sequence="1",
        previous_event_sha256=reserved.event_sha256,
    )
    terminal = parsed_event(
        context,
        "direct-terminal-admission-frozen",
        sequence="2",
        previous_event_sha256=admission.event_sha256,
    )
    return (reserved, admission, terminal)


class SignerContextTests(unittest.TestCase):
    def test_exact_i1_manifest_and_role_order_bind(self) -> None:
        context = signer_context()
        self.assertEqual(context.manifest_sha256, I1_PUBLIC_RUNTIME_MANIFEST_SHA256)
        self.assertEqual(len(context.registry_role_order), 22)
        self.assertEqual(len(context.non_root_signer_role_order), 21)
        self.assertNotIn("control-root-authority", context.non_root_signer_role_order)

    def test_wrong_manifest_or_role_order_fails(self) -> None:
        with self.assertRaises(BindingError):
            s0_i2.bind_public_i1_signer_context(
                manifest_sha256=hex64("0"),
                registry_role_order=FROZEN_REGISTRY_ROLE_ORDER,
            )
        with self.assertRaises(BindingError):
            s0_i2.bind_public_i1_signer_context(
                manifest_sha256=I1_PUBLIC_RUNTIME_MANIFEST_SHA256,
                registry_role_order=tuple(reversed(FROZEN_REGISTRY_ROLE_ORDER)),
            )

    def test_forged_context_is_rejected(self) -> None:
        forged = SignerRegistryContext(
            I1_PUBLIC_RUNTIME_MANIFEST_SHA256,
            FROZEN_REGISTRY_ROLE_ORDER,
            tuple(role for role in FROZEN_REGISTRY_ROLE_ORDER if role != "control-root-authority"),
            object(),
        )
        values = event_values(route_context(), "reserved")
        with self.assertRaises(BindingError):
            s0_i2.serialize_import_event(values, signer_context=forged)


class CanonicalEventTests(unittest.TestCase):
    def setUp(self) -> None:
        self.context = route_context()

    def test_round_trip_exact_31_lines_and_hash(self) -> None:
        values = event_values(self.context, "reserved")
        raw = s0_i2.serialize_import_event(
            values, signer_context=self.context.signer_context
        )
        event = s0_i2.parse_import_event(
            raw, signer_context=self.context.signer_context
        )
        self.assertEqual(raw.count(b"\n"), 31)
        self.assertTrue(raw.endswith(b"\n"))
        self.assertEqual(tuple(dict(event.fields)), EVENT_FIELD_ORDER)
        self.assertEqual(event.event_sha256, hashlib.sha256(raw).hexdigest())
        self.assertEqual(
            s0_i2.import_event_sha256(raw, signer_context=self.context.signer_context),
            event.event_sha256,
        )

    def test_arbitrary_length_canonical_decimal_has_no_application_ceiling(self) -> None:
        values = event_values(
            self.context,
            "reserved",
            sequence="1" + ("0" * 5000),
            previous_event_sha256=hex64("d"),
        )
        raw = s0_i2.serialize_import_event(
            values, signer_context=self.context.signer_context
        )
        event = s0_i2.parse_import_event(
            raw, signer_context=self.context.signer_context
        )
        self.assertEqual(event.sequence, "1" + ("0" * 5000))

    def test_noncanonical_decimal_and_zero_predecessor_rule_fail(self) -> None:
        for sequence, previous in (("01", hex64("d")), ("0", hex64("d")), ("1", ZERO64)):
            with self.subTest(sequence=sequence, previous=previous):
                values = event_values(
                    self.context,
                    "reserved",
                    sequence=sequence,
                    previous_event_sha256=previous,
                )
                with self.assertRaises(CanonicalRecordError):
                    s0_i2.serialize_import_event(
                        values, signer_context=self.context.signer_context
                    )

    def test_byte_format_failures_are_independent(self) -> None:
        raw = s0_i2.serialize_import_event(
            event_values(self.context, "reserved"),
            signer_context=self.context.signer_context,
        )
        lines = raw[:-1].split(b"\n")
        duplicate = list(lines)
        duplicate[1] = duplicate[0]
        missing = list(lines[:-1])
        unknown = list(lines)
        unknown[5] = b"unknown_field=" + unknown[5].split(b"=", 1)[1]
        blank = list(lines)
        blank[10] = b""
        nul = list(lines)
        nul[8] += b"\x00"
        trailing = list(lines)
        trailing[10] += b" "
        wrong_schema = list(lines)
        wrong_schema[0] = b"signer_media_event_schema=UNKNOWN-1"
        additive = list(lines)
        additive.insert(12, b"future_field=forbidden")
        cases = {
            "missing-final-lf": raw[:-1],
            "crlf": raw.replace(b"\n", b"\r\n", 1),
            "bom": b"\xef\xbb\xbf" + raw,
            "wrong-order": b"\n".join(lines[:2][::-1] + lines[2:]) + b"\n",
            "non-ascii": raw.replace(b"analysis", b"anal\xffsis"),
            "duplicate-field": b"\n".join(duplicate) + b"\n",
            "missing-field": b"\n".join(missing) + b"\n",
            "unknown-field": b"\n".join(unknown) + b"\n",
            "extra-field": b"\n".join(lines + [b"extra=1"]) + b"\n",
            "blank-line": b"\n".join(blank) + b"\n",
            "nul": b"\n".join(nul) + b"\n",
            "trailing-whitespace": b"\n".join(trailing) + b"\n",
            "wrong-schema": b"\n".join(wrong_schema) + b"\n",
            "additive-field": b"\n".join(additive) + b"\n",
        }
        for label, malformed in cases.items():
            with self.subTest(label=label), self.assertRaises(CanonicalRecordError):
                s0_i2.parse_import_event(
                    malformed, signer_context=self.context.signer_context
                )

    def test_non_ascii_serialization_is_canonical_error(self) -> None:
        values = event_values(self.context, "reserved")
        values["signer_id"] = "analys\N{LATIN SMALL LETTER I WITH ACUTE}s"
        with self.assertRaises(CanonicalRecordError):
            s0_i2.serialize_import_event(
                values, signer_context=self.context.signer_context
            )

    def test_root_signer_is_not_an_event_signer(self) -> None:
        values = event_values(self.context, "reserved")
        values["signer_id"] = "control-root-authority"
        with self.assertRaises(CanonicalRecordError):
            s0_i2.serialize_import_event(
                values, signer_context=self.context.signer_context
            )

    def test_result_media_id_must_not_collide_with_event_ids(self) -> None:
        values = event_values(self.context, "reserved")
        values["result_media_id"] = self.context.reserved_media_event_id
        with self.assertRaises(CanonicalRecordError):
            s0_i2.serialize_import_event(
                values, signer_context=self.context.signer_context
            )
        with self.assertRaises(BindingError):
            route_context(result_media_character="1")


class LifecycleTests(unittest.TestCase):
    def assert_structural_variant_rejected(
        self,
        context: s0_i2.ImportRouteContext,
        values: dict[str, str],
    ) -> None:
        event = s0_i2.parse_import_event(
            s0_i2.serialize_import_event(
                values, signer_context=context.signer_context
            ),
            signer_context=context.signer_context,
        )
        with self.assertRaises(LifecycleError):
            s0_i2.classify_event_variant(event, context)

    def test_full_accepted_route_and_global_chain(self) -> None:
        context, events = parsed_route("accepted")
        self.assertEqual(
            tuple(s0_i2.classify_event_variant(event, context) for event in events),
            ("reserved", "admission-frozen", "pending", "accepted"),
        )
        self.assertEqual(s0_i2.validate_import_route(events, context), events)
        self.assertEqual(
            s0_i2.validate_event_global_chain(
                events,
                expected_start_sequence="0",
                expected_previous_event_sha256=ZERO64,
            ),
            events,
        )

    def test_early_terminal_paths(self) -> None:
        for route_class in IMPORT_ROUTE_STATES:
            with self.subTest(route_class=route_class):
                context = route_context(route_class=route_class)
                reserved = parsed_event(
                    context, "reserved", sequence="0", previous_event_sha256=ZERO64
                )
                direct_r = parsed_event(
                    context,
                    "direct-terminal-reserved",
                    sequence="1",
                    previous_event_sha256=reserved.event_sha256,
                )
                self.assertEqual(
                    s0_i2.validate_import_route((reserved, direct_r), context),
                    (reserved, direct_r),
                )

                admission = parsed_event(
                    context,
                    "admission-frozen",
                    sequence="1",
                    previous_event_sha256=reserved.event_sha256,
                )
                direct_a = parsed_event(
                    context,
                    "direct-terminal-admission-frozen",
                    sequence="2",
                    previous_event_sha256=admission.event_sha256,
                )
                self.assertEqual(
                    s0_i2.validate_import_route(
                        (reserved, admission, direct_a), context
                    ),
                    (reserved, admission, direct_a),
                )

    def test_early_terminal_paths_reject_tuple_or_appliance_claims(self) -> None:
        for route_class, (source, destination) in IMPORT_ROUTE_STATES.items():
            context = route_context(route_class=route_class)
            for variant in (
                "direct-terminal-reserved",
                "direct-terminal-admission-frozen",
            ):
                base = event_values(context, variant)
                tuple_field = (
                    "admission_event_id"
                    if variant == "direct-terminal-reserved"
                    else "admission_record_sha256"
                )
                tuple_value = (
                    context.admission_frozen_media_event_id
                    if variant == "direct-terminal-reserved"
                    else hex64("f")
                )
                hostile_changes = {
                    "admission-tuple": (tuple_field, tuple_value),
                    "before-appliance-claim": (
                        "before_appliance_state",
                        source,
                    ),
                    "after-appliance-claim": (
                        "after_appliance_state",
                        destination,
                    ),
                }
                for label, (field_name, value) in hostile_changes.items():
                    with self.subTest(
                        route_class=route_class,
                        variant=variant,
                        label=label,
                    ):
                        values = dict(base)
                        values[field_name] = value
                        self.assert_structural_variant_rejected(context, values)

    def test_pending_rejects_noncanonical_structural_claims(self) -> None:
        source_order = ("key-generated", "pop-issued", "registry-bound")
        for route_class, (source, destination) in IMPORT_ROUTE_STATES.items():
            context = route_context(route_class=route_class)
            wrong_source = source_order[(source_order.index(source) + 1) % len(source_order)]
            base = event_values(context, "pending")
            hostile_changes = {
                "wrong-source": ("before_appliance_state", wrong_source),
                "known-after-state": ("after_appliance_state", destination),
                "non-none-outcome": ("outcome_class", "accepted"),
                "nonzero-frame": ("outcome_frame_sha256", hex64("c")),
            }
            for label, (field_name, value) in hostile_changes.items():
                with self.subTest(route_class=route_class, label=label):
                    values = dict(base)
                    values[field_name] = value
                    self.assert_structural_variant_rejected(context, values)

    def test_parse_and_validation_rejections_require_source_to_source(self) -> None:
        source_order = ("key-generated", "pop-issued", "registry-bound")
        for route_class, (source, destination) in IMPORT_ROUTE_STATES.items():
            context = route_context(route_class=route_class)
            wrong_source = source_order[(source_order.index(source) + 1) % len(source_order)]
            for variant in ("parse-rejected", "validation-rejected"):
                base = event_values(context, variant)
                for label, (field_name, value) in {
                    "wrong-before-source": (
                        "before_appliance_state",
                        wrong_source,
                    ),
                    "wrong-after-source": (
                        "after_appliance_state",
                        destination,
                    ),
                }.items():
                    with self.subTest(
                        route_class=route_class,
                        variant=variant,
                        label=label,
                    ):
                        values = dict(base)
                        values[field_name] = value
                        self.assert_structural_variant_rejected(context, values)

    def test_state_commit_failure_requires_source_to_indeterminate(self) -> None:
        source_order = ("key-generated", "pop-issued", "registry-bound")
        for route_class, (source, destination) in IMPORT_ROUTE_STATES.items():
            context = route_context(route_class=route_class)
            wrong_source = source_order[(source_order.index(source) + 1) % len(source_order)]
            base = event_values(context, "state-commit-failed")
            for label, (field_name, value) in {
                "wrong-before-source": (
                    "before_appliance_state",
                    wrong_source,
                ),
                "wrong-after-indeterminate": (
                    "after_appliance_state",
                    destination,
                ),
            }.items():
                with self.subTest(route_class=route_class, label=label):
                    values = dict(base)
                    values[field_name] = value
                    self.assert_structural_variant_rejected(context, values)

    def test_all_completion_classes_have_structural_variants(self) -> None:
        for route_class in IMPORT_ROUTE_STATES:
            for outcome_class in (
                "accepted",
                "parse-rejected",
                "validation-rejected",
                "state-commit-failed",
                "crash",
                "missing",
                "duplicate",
                "disagreement",
            ):
                with self.subTest(
                    route_class=route_class, outcome_class=outcome_class
                ):
                    context, events = parsed_route(
                        outcome_class, route_class=route_class
                    )
                    self.assertEqual(
                        s0_i2.classify_event_variant(events[-1], context),
                        outcome_class,
                    )
                    self.assertEqual(
                        s0_i2.validate_import_route(events, context), events
                    )
                    source, destination = IMPORT_ROUTE_STATES[route_class]
                    self.assertEqual(events[2]["before_appliance_state"], source)
                    if outcome_class == "accepted":
                        self.assertEqual(
                            events[-1]["after_appliance_state"], destination
                        )

    def test_disagreement_accepts_zero_or_bound_frame_hash_structurally(self) -> None:
        for frame_hash in (ZERO64, hex64("c")):
            context, events = parsed_route(
                "disagreement", disagreement_frame_sha256=frame_hash
            )
            self.assertEqual(
                s0_i2.classify_event_variant(events[-1], context), "disagreement"
            )

    def test_completion_frame_hash_sentinels(self) -> None:
        context, events = parsed_route("accepted")
        invalid = event_values(
            context,
            "accepted",
            sequence="3",
            previous_event_sha256=events[-2].event_sha256,
        )
        invalid["outcome_frame_sha256"] = ZERO64
        event = s0_i2.parse_import_event(
            s0_i2.serialize_import_event(
                invalid, signer_context=context.signer_context
            ),
            signer_context=context.signer_context,
        )
        with self.assertRaises(LifecycleError):
            s0_i2.classify_event_variant(event, context)

        invalid = event_values(
            context,
            "crash",
            sequence="3",
            previous_event_sha256=events[-2].event_sha256,
        )
        invalid["outcome_frame_sha256"] = hex64("c")
        event = s0_i2.parse_import_event(
            s0_i2.serialize_import_event(
                invalid, signer_context=context.signer_context
            ),
            signer_context=context.signer_context,
        )
        with self.assertRaises(LifecycleError):
            s0_i2.classify_event_variant(event, context)

    def test_route_binding_predecessor_and_duplicate_fail(self) -> None:
        context, events = parsed_route("accepted")
        wrong_context = s0_i2.bind_import_route_context(
            signer_context=context.signer_context,
            campaign_id=hex64("f"),
            ceremony_id=context.ceremony_id,
            signer_id=context.signer_id,
            route_class=context.route_class,
            attachment_capability_id=context.attachment_capability_id,
            admission_record_sha256=context.admission_record_sha256,
            media_object_sha256=context.media_object_sha256,
            media_object_id=context.media_object_id,
            result_media_id=context.result_media_id,
            reserved_media_event_id=context.reserved_media_event_id,
            admission_frozen_media_event_id=context.admission_frozen_media_event_id,
            pending_media_event_id=context.pending_media_event_id,
            completion_media_event_id=context.completion_media_event_id,
        )
        with self.assertRaises(LifecycleError):
            s0_i2.validate_import_route(events, wrong_context)
        with self.assertRaises(LifecycleError):
            s0_i2.validate_import_route((events[0], events[0]), context)

        wrong_prior_values = event_values(
            context,
            "admission-frozen",
            sequence="1",
            previous_event_sha256=events[0].event_sha256,
        )
        wrong_prior_values["prior_route_event_id"] = ZERO64
        wrong_prior = s0_i2.parse_import_event(
            s0_i2.serialize_import_event(
                wrong_prior_values, signer_context=context.signer_context
            ),
            signer_context=context.signer_context,
        )
        with self.assertRaises(LifecycleError):
            s0_i2.validate_import_route((events[0], wrong_prior), context)

    def test_global_link_and_arbitrary_length_successor(self) -> None:
        context = route_context()
        start = "9" * 5000
        first = parsed_event(
            context,
            "reserved",
            sequence=start,
            previous_event_sha256=hex64("d"),
        )
        second_values = event_values(
            context,
            "reserved",
            sequence="1" + ("0" * 5000),
            previous_event_sha256=first.event_sha256,
        )
        second_values["event_id"] = context.admission_frozen_media_event_id
        second = s0_i2.parse_import_event(
            s0_i2.serialize_import_event(
                second_values, signer_context=context.signer_context
            ),
            signer_context=context.signer_context,
        )
        self.assertEqual(
            s0_i2.validate_event_global_chain(
                (first, second),
                expected_start_sequence=start,
                expected_previous_event_sha256=hex64("d"),
            ),
            (first, second),
        )
        with self.assertRaises(LifecycleError):
            s0_i2.validate_event_global_link(
                second,
                expected_sequence=second.sequence,
                expected_previous_event_sha256=hex64("e"),
            )

    def test_wrong_lifecycle_tuple_components_fail(self) -> None:
        context, events = parsed_route("accepted")
        base = event_values(
            context,
            "accepted",
            sequence="3",
            previous_event_sha256=events[-2].event_sha256,
        )
        hostile_changes = {
            "wrong-admission-tuple": ("admission_record_sha256", hex64("f")),
            "wrong-source": ("before_appliance_state", "pop-issued"),
            "wrong-destination": ("after_appliance_state", "registry-bound"),
            "wrong-state": ("state", "terminal"),
            "wrong-terminal-from": ("terminal_from", "pending"),
        }
        for label, (field_name, value) in hostile_changes.items():
            with self.subTest(label=label):
                values = dict(base)
                values[field_name] = value
                event = s0_i2.parse_import_event(
                    s0_i2.serialize_import_event(
                        values, signer_context=context.signer_context
                    ),
                    signer_context=context.signer_context,
                )
                with self.assertRaises(LifecycleError):
                    s0_i2.classify_event_variant(event, context)

    def test_forged_and_corrupt_event_handles_are_stable_lifecycle_errors(self) -> None:
        context, events = parsed_route("accepted")
        valid = events[0]
        forged_route_context = replace(context, _provenance=object())
        with self.assertRaises(LifecycleError):
            s0_i2.validate_import_route(events, forged_route_context)
        with self.assertRaises(LifecycleError):
            s0_i2.classify_event_variant(valid, forged_route_context)
        wrong_provenance = type(valid)(
            b"",
            (),
            ZERO64,
            "0",
            context.signer_context,
            object(),
        )
        forged_context = SignerRegistryContext(
            I1_PUBLIC_RUNTIME_MANIFEST_SHA256,
            FROZEN_REGISTRY_ROLE_ORDER,
            tuple(
                role
                for role in FROZEN_REGISTRY_ROLE_ORDER
                if role != "control-root-authority"
            ),
            object(),
        )
        corrupt_handles = (
            wrong_provenance,
            replace(valid, raw=valid.raw[:-1]),
            replace(valid, fields=()),
            replace(valid, event_sha256=hex64("f")),
            replace(valid, sequence="1"),
            replace(valid, _signer_context=forged_context),
        )
        for index, event in enumerate(corrupt_handles):
            with self.subTest(index=index, api="route"):
                with self.assertRaises(LifecycleError):
                    s0_i2.validate_import_route((event,), context)
            with self.subTest(index=index, api="variant"):
                with self.assertRaises(LifecycleError):
                    s0_i2.classify_event_variant(event, context)

    def test_wrong_global_sequence_and_duplicate_emitted_event_id_fail(self) -> None:
        context, events = parsed_route("accepted")
        with self.assertRaises(LifecycleError):
            s0_i2.validate_event_global_link(
                events[0],
                expected_sequence="1",
                expected_previous_event_sha256=ZERO64,
            )

        first_values = event_values(
            context,
            "reserved",
            sequence="1",
            previous_event_sha256=hex64("d"),
        )
        first_values["event_id"] = hex64("f")
        first = s0_i2.parse_import_event(
            s0_i2.serialize_import_event(
                first_values, signer_context=context.signer_context
            ),
            signer_context=context.signer_context,
        )
        second_values = event_values(
            context,
            "reserved",
            sequence="2",
            previous_event_sha256=first.event_sha256,
        )
        second_values["event_id"] = hex64("f")
        second = s0_i2.parse_import_event(
            s0_i2.serialize_import_event(
                second_values, signer_context=context.signer_context
            ),
            signer_context=context.signer_context,
        )
        with self.assertRaises(LifecycleError):
            s0_i2.validate_event_global_chain(
                (first, second),
                expected_start_sequence="1",
                expected_previous_event_sha256=hex64("d"),
            )


class SuppliedRouteSetTests(unittest.TestCase):
    def assert_route_set_rejected(
        self,
        *groups: tuple[
            s0_i2.ImportRouteContext,
            tuple[s0_i2.ImportLedgerEvent, ...],
        ],
    ) -> None:
        with self.assertRaises(LifecycleError):
            s0_i2.validate_supplied_route_set(groups)

    def test_disjoint_routes_are_accepted(self) -> None:
        first_context, first_events = parsed_route("accepted")
        second_context = route_context(
            route_class="registry-binding-v1",
            campaign_character="0",
            event_characters=("c", "d", "e", "f"),
            result_media_character="a",
        )
        _, second_events = parsed_route("missing", context=second_context)
        validated = s0_i2.validate_supplied_route_set(
            ((first_context, first_events), (second_context, second_events))
        )
        self.assertEqual(len(validated), 2)

    def test_repeated_route_identity_and_contradictory_histories_are_rejected(
        self,
    ) -> None:
        context, accepted = parsed_route("accepted")
        _, missing = parsed_route("missing", context=context)
        early_reserved = parsed_early_route(context, after_admission=False)
        early_admission = parsed_early_route(context, after_admission=True)
        cases = (
            (accepted, accepted),
            (accepted, missing),
            (missing, accepted),
            (accepted, early_reserved),
            (early_reserved, accepted),
            (accepted, early_admission),
            (early_admission, accepted),
            (early_reserved, early_reserved),
            (early_admission, early_admission),
        )
        for first, second in cases:
            with self.subTest(first=len(first), second=len(second)):
                self.assert_route_set_rejected(
                    (context, first),
                    (context, second),
                )

    def test_distinct_route_preallocated_overlap_is_rejected(self) -> None:
        first_context, first_events = parsed_route("accepted")
        overlapping_context = route_context(
            route_class="activation-binding-v1",
            campaign_character="0",
            event_characters=("4", "c", "d", "e"),
        )
        _, overlapping_events = parsed_route(
            "crash", context=overlapping_context
        )
        self.assert_route_set_rejected(
            (first_context, first_events),
            (overlapping_context, overlapping_events),
        )

    def test_cross_route_result_media_to_event_id_collision_is_rejected(self) -> None:
        first_context = route_context(result_media_character="c")
        _, first_full = parsed_route("accepted", context=first_context)
        first_early = parsed_early_route(first_context, after_admission=False)
        second_context = route_context(
            route_class="registry-binding-v1",
            campaign_character="0",
            event_characters=("c", "d", "e", "f"),
            result_media_character="a",
        )
        _, second_full = parsed_route("missing", context=second_context)
        second_early = parsed_early_route(second_context, after_admission=True)
        cases = (
            ((first_context, first_full), (second_context, second_full)),
            ((second_context, second_full), (first_context, first_full)),
            ((first_context, first_early), (second_context, second_full)),
            ((second_context, second_early), (first_context, first_full)),
        )
        for first, second in cases:
            with self.subTest(first=first[0].route_class, second=second[0].route_class):
                self.assert_route_set_rejected(first, second)

    def test_cross_route_result_media_id_reuse_is_rejected(self) -> None:
        first_context = route_context(result_media_character="b")
        _, first_full = parsed_route("accepted", context=first_context)
        first_early = parsed_early_route(first_context, after_admission=True)
        second_context = route_context(
            route_class="registry-binding-v1",
            campaign_character="0",
            event_characters=("c", "d", "e", "f"),
            result_media_character="b",
        )
        _, second_full = parsed_route("crash", context=second_context)
        second_early = parsed_early_route(second_context, after_admission=False)
        cases = (
            ((first_context, first_full), (second_context, second_full)),
            ((second_context, second_full), (first_context, first_full)),
            ((first_context, first_early), (second_context, second_full)),
            ((second_context, second_early), (first_context, first_full)),
        )
        for first, second in cases:
            with self.subTest(first=first[0].route_class, second=second[0].route_class):
                self.assert_route_set_rejected(first, second)

    def test_early_terminal_unused_preallocated_id_overlap_is_rejected(self) -> None:
        first_context = route_context()
        first_events = parsed_early_route(first_context, after_admission=False)
        self.assertNotIn(
            first_context.pending_media_event_id,
            tuple(event["event_id"] for event in first_events),
        )
        overlapping_context = route_context(
            route_class="registry-binding-v1",
            campaign_character="0",
            event_characters=("3", "c", "d", "e"),
        )
        _, overlapping_events = parsed_route(
            "validation-rejected", context=overlapping_context
        )
        self.assert_route_set_rejected(
            (first_context, first_events),
            (overlapping_context, overlapping_events),
        )


class UnsupportedBoundaryTests(unittest.TestCase):
    def assert_blocked(self, function: object, *args: object, **kwargs: object) -> None:
        with self.assertRaisesRegex(UnsupportedBoundaryError, "^BLOCKED:"):
            function(*args, **kwargs)  # type: ignore[operator]

    def test_unauthenticated_record_grammars_are_blocked(self) -> None:
        self.assert_blocked(s0_i2.parse_import_admission, b"not-a-record")
        self.assert_blocked(s0_i2.serialize_import_admission, {})
        self.assert_blocked(s0_i2.parse_import_outcome, b"not-a-frame")
        self.assert_blocked(s0_i2.serialize_import_outcome, {})
        self.assert_blocked(s0_i2.validate_outcome_binding, object(), object())

    def test_complete_classification_ledger_and_witness_are_blocked(self) -> None:
        self.assert_blocked(s0_i2.classify_outcome_medium, b"non-final-lf")
        self.assert_blocked(s0_i2.validate_complete_import)
        self.assert_blocked(s0_i2.validate_durable_ledger)
        self.assert_blocked(s0_i2.validate_witness)


class ContractAndVectorTests(unittest.TestCase):
    def test_exact_contract_and_signer_context(self) -> None:
        path = I2_ROOT / "spec" / "trust-root-role-isolation-contract-v0.3.json"
        raw = path.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), CONTRACT_SHA256)
        document = s0_i2.verify_contract_bytes(raw)
        self.assertEqual(set(document["records"]), {"import_ledger_event"})
        self.assertEqual(document["complete_validation_status"], "BLOCKED")
        ownership = document["supplied_route_set_identifier_ownership"]
        self.assertEqual(ownership["route_identity_occurrences"], "exactly one")
        self.assertEqual(ownership["identifiers_per_route"], 5)
        self.assertEqual(ownership["project_lifetime_uniqueness"], "BLOCKED")
        context = s0_i2.signer_context_from_contract_file(path)
        self.assertEqual(context.registry_role_order, FROZEN_REGISTRY_ROLE_ORDER)

    def test_contract_byte_change_fails_before_semantic_use(self) -> None:
        path = I2_ROOT / "spec" / "trust-root-role-isolation-contract-v0.3.json"
        raw = path.read_bytes()
        with self.assertRaises(BindingError):
            s0_i2.verify_contract_bytes(raw + b"\n")

    def test_exact_i1_snapshot_signer_roles_match_contract_inventory(self) -> None:
        manifest_path = I2_ROOT.parent / "i1" / "spec" / "public-runtime-files.sha256"
        runtime_path = I2_ROOT.parent / "i1" / "spec" / "public-runtime-v0.14.json"
        manifest_raw = manifest_path.read_bytes()
        runtime_raw = runtime_path.read_bytes()
        self.assertEqual(
            hashlib.sha256(manifest_raw).hexdigest(),
            I1_PUBLIC_RUNTIME_MANIFEST_SHA256,
        )
        self.assertEqual(
            hashlib.sha256(runtime_raw).hexdigest(),
            I1_PUBLIC_RUNTIME_JSON_SHA256,
        )
        self.assertIn(
            (
                I1_PUBLIC_RUNTIME_JSON_SHA256
                + "  s0-lab/i1/spec/public-runtime-v0.14.json"
            ),
            manifest_raw.decode("ascii").splitlines(),
        )

        def reject_duplicate_pairs(
            pairs: list[tuple[str, object]],
        ) -> dict[str, object]:
            result: dict[str, object] = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError(f"duplicate JSON key: {key}")
                result[key] = value
            return result

        runtime = json.loads(runtime_raw, object_pairs_hook=reject_duplicate_pairs)
        roles = tuple(runtime["signer_roles"])
        self.assertEqual(roles, FROZEN_REGISTRY_ROLE_ORDER)
        self.assertEqual(runtime["counts"]["signer_roles"], 22)
        self.assertEqual(len(roles), 22)
        self.assertEqual(len(set(roles)), 22)
        self.assertEqual(
            len(tuple(role for role in roles if role != "control-root-authority")),
            21,
        )

    def test_exact_vector_package_and_mutation(self) -> None:
        package = s0_i2.bind_frozen_tri2_vec_02(
            artifact_id="TRI2-VEC-02",
            artifact_sha256=TRI2_VEC_02_ARTIFACT_SHA256,
            derivation_sha256=TRI2_VEC_02_DERIVATION_SHA256,
            decision_sha256=TRI2_VEC_02_DECISION_SHA256,
            rows=TRI2_VEC_02_ROWS,
        )
        self.assertEqual(package.rows, TRI2_VEC_02_ROWS)
        changed = list(TRI2_VEC_02_ROWS)
        changed[0] = (changed[0][0], hex64("f"))
        with self.assertRaises(VectorBindingError):
            s0_i2.bind_frozen_tri2_vec_02(
                artifact_id="TRI2-VEC-02",
                artifact_sha256=TRI2_VEC_02_ARTIFACT_SHA256,
                derivation_sha256=TRI2_VEC_02_DERIVATION_SHA256,
                decision_sha256=TRI2_VEC_02_DECISION_SHA256,
                rows=changed,
            )


class CapabilityBoundaryTests(unittest.TestCase):
    def test_implementation_has_no_forbidden_imports(self) -> None:
        forbidden_roots = {
            "asyncio",
            "cryptography",
            "ecdsa",
            "http",
            "nacl",
            "requests",
            "socket",
            "ssl",
            "subprocess",
            "urllib",
        }
        for path in sorted((IMPLEMENTATION_ROOT / "s0_i2").glob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            imported: set[str] = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imported.update(alias.name.split(".", 1)[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imported.add(node.module.split(".", 1)[0])
            self.assertFalse(
                imported & forbidden_roots,
                f"forbidden import in {path.name}: {sorted(imported & forbidden_roots)}",
            )


if __name__ == "__main__":
    unittest.main()

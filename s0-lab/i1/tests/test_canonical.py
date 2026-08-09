from __future__ import annotations

import hashlib
import sys
import unittest
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[3]
IMPLEMENTATION = WORKSPACE / "s0-lab" / "i1" / "implementation"
sys.path.insert(0, str(IMPLEMENTATION))

from s0_i1.auth import sha256_bytes  # noqa: E402
from s0_i1.canonical import (  # noqa: E402
    assemble_signed_envelope,
    bind_external_signer_authority,
    parse_comparison_record,
    parse_evidence_bundle,
    parse_publication_record,
    parse_signed_envelope,
    parse_status_record,
    serialize_comparison_record,
    serialize_evidence_bundle,
    serialize_evidence_receipt,
    serialize_publication_record,
    serialize_root_bundle,
    serialize_status_record,
    signature_preimage,
    signer_assignment_binding_sha256,
    validate_status_chain,
    verify_comparison_delivery,
    verify_e56_publication_receipt,
    verify_publication_delivery,
)
from s0_i1.errors import CanonicalRecordError, TopologyError  # noqa: E402
from s0_i1.topology import EXPECTED_SIGNER_ROLES, load_public_runtime_spec  # noqa: E402


SIGNATURE_SENTINEL = "ab" * 64
MANIFEST_SENTINEL = "cd" * 32


def key_id(role: str) -> str:
    return hashlib.sha256(("non-key-sentinel:" + role).encode("ascii")).hexdigest()


class SentinelVerifier:
    def __init__(self, decision=True):
        self.decision = decision
        self.calls = []

    def verify(self, **values):
        self.calls.append(values)
        if values["signature_hex"] != SIGNATURE_SENTINEL:
            return False
        return self.decision


class CanonicalRecordTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.topology = load_public_runtime_spec(WORKSPACE)
        cls.assignments = tuple((role, key_id(role)) for role in EXPECTED_SIGNER_ROLES)
        binding = signer_assignment_binding_sha256(cls.topology, cls.assignments)
        cls.authority = bind_external_signer_authority(
            cls.topology,
            cls.assignments,
            expected_binding_sha256=binding,
        )
        cls.keys = dict(cls.assignments)

    def _envelope(self, record: bytes, role: str, signature: str = SIGNATURE_SENTINEL) -> bytes:
        return assemble_signed_envelope(
            signature_preimage(record, role, self.keys[role]), signature
        )

    def _receipt_envelope(
        self, edge: str, role: str, kind: str, byte: str
    ) -> bytes:
        record = serialize_evidence_receipt(
            self.topology, edge, role, kind, byte * 64
        )
        return self._envelope(record, role)

    def _two_pair_chain(self):
        root_bundle = serialize_root_bundle(MANIFEST_SENTINEL)
        root_record = serialize_status_record(
            0, "0" * 64, "ROOT", sha256_bytes(root_bundle), "0000", 100
        )
        root_envelope = self._envelope(root_record, "control-registrar")
        receipt_envelopes = [
            self._receipt_envelope(
                "E02", "simulation-builder", "benchmark-summary", "1"
            ),
            self._receipt_envelope(
                "E02", "simulation-builder", "audit-summary", "2"
            ),
            self._receipt_envelope(
                "E02", "simulation-builder", "power-summary", "3"
            ),
        ]
        e02_bundle = serialize_evidence_bundle(
            self.topology, "E02", receipt_envelopes
        )
        e02_record = serialize_status_record(
            1,
            sha256_bytes(root_record),
            "E02",
            sha256_bytes(e02_bundle),
            "0001",
            101,
        )
        e02_envelope = self._envelope(e02_record, "control-registrar")
        return (root_envelope, root_bundle), (e02_envelope, e02_bundle), root_record

    def _comparison_delivery(self, edge: str, record: bytes = b"table_schema=public-sentinel\nvalue=1\n"):
        if edge == "E43":
            left_role, right_role, custodian = (
                "semantic-judge-1",
                "semantic-judge-2",
                "judgment-comparison",
            )
        else:
            left_role, right_role, custodian = (
                "comparator-operator-1",
                "comparator-operator-2",
                "adjudication-comparison",
            )
        left = self._envelope(record, left_role)
        right = self._envelope(record, right_role)
        comparison_record = serialize_comparison_record(
            edge, left, right, self.authority, SentinelVerifier()
        )
        comparison_envelope = self._envelope(comparison_record, custodian)
        return [
            left,
            right,
            comparison_envelope,
            sha256_bytes(comparison_record),
            record,
        ]

    def test_signed_envelope_requires_immutable_authority_and_exact_true_decision(self):
        record = serialize_evidence_receipt(
            self.topology,
            "E05",
            "content-intake",
            "content-digest",
            "1" * 64,
        )
        raw = self._envelope(record, "content-intake")
        verifier = SentinelVerifier()
        parsed = parse_signed_envelope(
            raw, self.authority, verifier, required_role="content-intake"
        )
        self.assertEqual(parsed.record_bytes, record)
        self.assertEqual(len(verifier.calls), 1)
        with self.assertRaisesRegex(CanonicalRecordError, "authority"):
            parse_signed_envelope(raw, dict(self.assignments), SentinelVerifier())
        for decision in (False, "accepted", 1):
            with self.subTest(decision=decision):
                with self.assertRaisesRegex(CanonicalRecordError, "injected"):
                    parse_signed_envelope(
                        raw, self.authority, SentinelVerifier(decision)
                    )

    def test_self_authored_second_signer_binding_does_not_replace_required_authority(self):
        altered = list(self.assignments)
        altered[0] = (altered[0][0], "f" * 64)
        binding = signer_assignment_binding_sha256(self.topology, altered)
        other = bind_external_signer_authority(
            self.topology, altered, expected_binding_sha256=binding
        )
        record = b"record_schema=sentinel\n"
        raw = self._envelope(record, "adjudication-comparison")
        with self.assertRaisesRegex(CanonicalRecordError, "role/key"):
            parse_signed_envelope(raw, other, SentinelVerifier())

        original = self.authority.binding_sha256
        try:
            object.__setattr__(self.authority, "binding_sha256", "0" * 64)
            with self.assertRaisesRegex(CanonicalRecordError, "digest"):
                parse_signed_envelope(raw, self.authority, SentinelVerifier())
        finally:
            object.__setattr__(self.authority, "binding_sha256", original)

    def test_envelope_field_order_algorithm_hash_and_resource_bounds(self):
        record = serialize_evidence_receipt(
            self.topology,
            "E05",
            "content-intake",
            "content-digest",
            "1" * 64,
        )
        raw = self._envelope(record, "content-intake")
        length = f"record_length={len(record)}".encode("ascii")
        digest = f"record_sha256={sha256_bytes(record)}".encode("ascii")
        signature_line = f"signature_hex={SIGNATURE_SENTINEL}\n".encode("ascii")
        algorithm_line = b"signature_algorithm=Ed25519\n"
        attacks = (
            raw.replace(
                b"signature_algorithm=Ed25519", b"signature_algorithm=ed25519"
            ),
            raw.replace(b"record_sha256=", b"record_digest="),
            raw.replace(length, b"record_length=" + b"9" * 10000),
            raw.replace(digest, b"record_sha256=" + b"0" * 64),
            raw.replace(
                algorithm_line + signature_line, signature_line + algorithm_line
            ),
            raw + b"extra=1\n",
        )
        for attack in attacks:
            with self.subTest(attack=attack[-20:]):
                with self.assertRaises(CanonicalRecordError):
                    parse_signed_envelope(attack, self.authority, SentinelVerifier())

    def test_e25_bundle_requires_two_fixed_roles_in_fixed_order(self):
        first = self._receipt_envelope(
            "E25",
            "comparator-builder-1",
            "implementation-mutation-table-digest",
            "1",
        )
        second = self._receipt_envelope(
            "E25",
            "comparator-builder-2",
            "implementation-mutation-table-digest",
            "2",
        )
        valid = serialize_evidence_bundle(self.topology, "E25", [first, second])
        parsed = parse_evidence_bundle(
            valid,
            self.topology,
            self.authority,
            SentinelVerifier(),
            expected_control_integration_manifest_sha256=MANIFEST_SENTINEL,
        )
        self.assertEqual(
            [receipt.producer_role for receipt in parsed.receipts],
            ["comparator-builder-1", "comparator-builder-2"],
        )
        reversed_bundle = serialize_evidence_bundle(
            self.topology, "E25", [second, first]
        )
        with self.assertRaises(CanonicalRecordError):
            parse_evidence_bundle(
                reversed_bundle,
                self.topology,
                self.authority,
                SentinelVerifier(),
                expected_control_integration_manifest_sha256=MANIFEST_SENTINEL,
            )
        with self.assertRaisesRegex(CanonicalRecordError, "count"):
            serialize_evidence_bundle(self.topology, "E25", [first])

    def test_receipt_result_identity_and_mutated_topology_mapping_reject(self):
        valid = serialize_evidence_receipt(
            self.topology,
            "E05",
            "content-intake",
            "content-digest",
            "4" * 64,
        )
        for record in (
            valid.replace(b"accepted\n", b"rejected\n"),
            valid.replace(b"content-intake", b"simulation-builder"),
        ):
            envelope = self._envelope(record, "content-intake")
            bundle = (
                b"evidence_bundle_schema=URC-0.14-STATUS-BUNDLE-1\n"
                b"edge=E05\nentry_count=1\n"
                + f"entry_1_envelope_length={len(envelope)}\n".encode("ascii")
                + envelope
            )
            with self.assertRaises(CanonicalRecordError):
                parse_evidence_bundle(
                    bundle,
                    self.topology,
                    self.authority,
                    SentinelVerifier(),
                    expected_control_integration_manifest_sha256=MANIFEST_SENTINEL,
                )
        mutated = self.topology.to_plain_dict()
        mutated["status"]["receipts"][1]["entries"][0][
            "producer_role"
        ] = "simulation-builder"
        with self.assertRaises((TopologyError, CanonicalRecordError)):
            serialize_evidence_receipt(
                mutated,
                "E05",
                "simulation-builder",
                "content-digest",
                "4" * 64,
            )

    def test_status_root_binding_relations_and_two_pairs(self):
        root_pair, e02_pair, _ = self._two_pair_chain()
        parsed = validate_status_chain(
            [root_pair, e02_pair],
            self.topology,
            self.authority,
            SentinelVerifier(),
            expected_control_integration_manifest_sha256=MANIFEST_SENTINEL,
        )
        self.assertEqual(
            [pair.record.status_code for pair in parsed], ["A-0000", "A-0001"]
        )
        with self.assertRaisesRegex(CanonicalRecordError, "ROOT manifest"):
            validate_status_chain(
                [root_pair],
                self.topology,
                self.authority,
                SentinelVerifier(),
                expected_control_integration_manifest_sha256="0" * 64,
            )

    def test_status_serializer_parser_reject_every_expressible_relation_and_bool(self):
        with self.assertRaisesRegex(CanonicalRecordError, "exact integer"):
            serialize_status_record(
                True, "0" * 64, "ROOT", "1" * 64, "0000", 1
            )
        with self.assertRaisesRegex(CanonicalRecordError, "exact integer"):
            serialize_status_record(
                0, "0" * 64, "ROOT", "1" * 64, "0000", True
            )
        for values in (
            (0, "0" * 64, "E02", "0000"),
            (1, "0" * 64, "E05", "0001"),
            (1, "0" * 64, "E02", "0002"),
            (0, "1" * 64, "ROOT", "0000"),
        ):
            sequence, previous, edge, mask = values
            with self.subTest(values=values):
                with self.assertRaises(CanonicalRecordError):
                    serialize_status_record(
                        sequence, previous, edge, "1" * 64, mask, 1
                    )
        valid = serialize_status_record(
            0, "0" * 64, "ROOT", "1" * 64, "0000", 1
        )
        attacks = (
            valid.replace(b"event_edge=ROOT", b"event_edge=E99"),
            valid.replace(b"sequence=0", b"sequence=1"),
            valid.replace(b"evidence_mask=0000", b"evidence_mask=0001"),
            valid.replace(b"status_code=A-0000", b"status_code=A-0001"),
            valid.replace(b"sequence=0", b"sequence=" + b"9" * 10000),
        )
        for attack in attacks:
            with self.assertRaises(CanonicalRecordError):
                parse_status_record(attack)

    def test_status_chain_hash_commitment_time_and_final_e56_order(self):
        root_pair, e02_pair, root_record = self._two_pair_chain()
        e02_bundle = e02_pair[1]
        valid = parse_signed_envelope(
            e02_pair[0], self.authority, SentinelVerifier()
        ).record_bytes
        cases = (
            valid.replace(
                f"previous_record_sha256={sha256_bytes(root_record)}".encode(),
                b"previous_record_sha256=" + b"0" * 64,
            ),
            valid.replace(
                f"event_commitment_sha256={sha256_bytes(e02_bundle)}".encode(),
                b"event_commitment_sha256=" + b"0" * 64,
            ),
            valid.replace(b"monotonic_timestamp_ns=101", b"monotonic_timestamp_ns=100"),
        )
        for record in cases:
            pair = (self._envelope(record, "control-registrar"), e02_bundle)
            with self.assertRaises(CanonicalRecordError):
                validate_status_chain(
                    [root_pair, pair],
                    self.topology,
                    self.authority,
                    SentinelVerifier(),
                    expected_control_integration_manifest_sha256=MANIFEST_SENTINEL,
                )

        publication_digest_receipt = self._receipt_envelope(
            "E56",
            "public-record-publisher",
            "publication-receipt-envelope-digest",
            "5",
        )
        e56_bundle = serialize_evidence_bundle(
            self.topology, "E56", [publication_digest_receipt]
        )
        premature = serialize_status_record(
            1,
            sha256_bytes(root_record),
            "E02",
            sha256_bytes(e56_bundle),
            "0001",
            101,
        ).replace(b"event_edge=E02", b"event_edge=E56")
        with self.assertRaisesRegex(CanonicalRecordError, "relation"):
            validate_status_chain(
                [
                    root_pair,
                    (self._envelope(premature, "control-registrar"), e56_bundle),
                ],
                self.topology,
                self.authority,
                SentinelVerifier(),
                expected_control_integration_manifest_sha256=MANIFEST_SENTINEL,
            )

    def test_complete_root_through_e56_chain(self):
        root_bundle = serialize_root_bundle(MANIFEST_SENTINEL)
        previous_record = serialize_status_record(
            0, "0" * 64, "ROOT", sha256_bytes(root_bundle), "0000", 1000
        )
        pairs = [(self._envelope(previous_record, "control-registrar"), root_bundle)]
        for sequence, row in enumerate(self.topology["status"]["receipts"], 1):
            envelopes = []
            for entry_index, entry in enumerate(row["entries"], 1):
                digest = hashlib.sha256(
                    f"{row['edge']}:{entry_index}".encode("ascii")
                ).hexdigest()
                receipt = serialize_evidence_receipt(
                    self.topology,
                    row["edge"],
                    entry["producer_role"],
                    entry["artifact_kind"],
                    digest,
                )
                envelopes.append(self._envelope(receipt, entry["producer_role"]))
            bundle = serialize_evidence_bundle(
                self.topology, row["edge"], envelopes
            )
            mask = f"{((1 << sequence) - 1):04x}"
            record = serialize_status_record(
                sequence,
                sha256_bytes(previous_record),
                row["edge"],
                sha256_bytes(bundle),
                mask,
                1000 + sequence,
            )
            pairs.append((self._envelope(record, "control-registrar"), bundle))
            previous_record = record
        parsed = validate_status_chain(
            pairs,
            self.topology,
            self.authority,
            SentinelVerifier(),
            expected_control_integration_manifest_sha256=MANIFEST_SENTINEL,
        )
        self.assertEqual(len(parsed), 15)
        self.assertEqual(parsed[-1].record.event_edge, "E56")
        self.assertEqual(parsed[-1].record.status_code, "A-3fff")

    def test_e43_and_e45_recipient_recomputation_positive(self):
        for edge in ("E43", "E45"):
            with self.subTest(edge=edge):
                delivery = self._comparison_delivery(edge)
                verified = verify_comparison_delivery(
                    edge, delivery, self.authority, SentinelVerifier()
                )
                self.assertEqual(verified.comparison_record.edge, edge)
                self.assertEqual(
                    verified.comparison_digest,
                    sha256_bytes(verified.comparison_record.raw),
                )

    def test_comparison_swaps_bad_signatures_wrong_custodian_and_digest_domain_reject(self):
        delivery = self._comparison_delivery("E43")
        swapped = [delivery[1], delivery[0], *delivery[2:]]
        with self.assertRaises(CanonicalRecordError):
            verify_comparison_delivery(
                "E43", swapped, self.authority, SentinelVerifier()
            )

        bad_left = delivery[0].replace(
            f"signature_hex={SIGNATURE_SENTINEL}".encode(),
            b"signature_hex=" + b"cd" * 64,
        )
        with self.assertRaisesRegex(CanonicalRecordError, "injected"):
            verify_comparison_delivery(
                "E43", [bad_left, *delivery[1:]], self.authority, SentinelVerifier()
            )

        record = parse_signed_envelope(
            delivery[2], self.authority, SentinelVerifier()
        ).record_bytes
        wrong_custodian = self._envelope(record, "adjudication-comparison")
        with self.assertRaisesRegex(CanonicalRecordError, "role"):
            verify_comparison_delivery(
                "E43",
                [delivery[0], delivery[1], wrong_custodian, delivery[3], delivery[4]],
                self.authority,
                SentinelVerifier(),
            )

        wrong_named_digest = sha256_bytes(delivery[2])
        with self.assertRaisesRegex(CanonicalRecordError, "record bytes"):
            verify_comparison_delivery(
                "E43",
                [delivery[0], delivery[1], delivery[2], wrong_named_digest, delivery[4]],
                self.authority,
                SentinelVerifier(),
            )

    def test_generic_envelope_does_not_accept_inconsistent_comparison_binding(self):
        delivery = self._comparison_delivery("E43")
        parsed = parse_signed_envelope(
            delivery[2], self.authority, SentinelVerifier()
        )
        inconsistent = parsed.record_bytes.replace(
            f"left_envelope_sha256={sha256_bytes(delivery[0])}".encode(),
            f"left_envelope_sha256={sha256_bytes(delivery[4])}".encode(),
        )
        inconsistent_envelope = self._envelope(
            inconsistent, "judgment-comparison"
        )
        parse_signed_envelope(
            inconsistent_envelope, self.authority, SentinelVerifier()
        )
        with self.assertRaisesRegex(CanonicalRecordError, "binding"):
            verify_comparison_delivery(
                "E43",
                [
                    delivery[0],
                    delivery[1],
                    inconsistent_envelope,
                    sha256_bytes(inconsistent),
                    delivery[4],
                ],
                self.authority,
                SentinelVerifier(),
            )

    def test_every_comparison_hash_scope_and_agreed_bytes_mutation_rejects(self):
        delivery = self._comparison_delivery("E43")
        record = parse_signed_envelope(
            delivery[2], self.authority, SentinelVerifier()
        ).record_bytes
        replacements = {
            b"left_envelope_sha256=" + sha256_bytes(delivery[0]).encode():
                b"left_envelope_sha256="
                + sha256_bytes(
                    parse_signed_envelope(
                        delivery[0], self.authority, SentinelVerifier()
                    ).preimage
                ).encode(),
            b"left_record_sha256=" + sha256_bytes(delivery[4]).encode():
                b"left_record_sha256=" + b"0" * 64,
            b"right_envelope_sha256=" + sha256_bytes(delivery[1]).encode():
                b"right_envelope_sha256=" + b"0" * 64,
            b"right_record_sha256=" + sha256_bytes(delivery[4]).encode():
                b"right_record_sha256=" + b"0" * 64,
            b"agreed_record_sha256=" + sha256_bytes(delivery[4]).encode():
                b"agreed_record_sha256=" + b"0" * 64,
        }
        for index, (source, replacement) in enumerate(replacements.items()):
            with self.subTest(index=index):
                mutated = record.replace(source, replacement)
                envelope = self._envelope(mutated, "judgment-comparison")
                with self.assertRaises(CanonicalRecordError):
                    verify_comparison_delivery(
                        "E43",
                        [
                            delivery[0],
                            delivery[1],
                            envelope,
                            sha256_bytes(mutated),
                            delivery[4],
                        ],
                        self.authority,
                        SentinelVerifier(),
                    )
        with self.assertRaisesRegex(CanonicalRecordError, "byte-identical"):
            verify_comparison_delivery(
                "E43",
                [
                    delivery[0],
                    delivery[1],
                    delivery[2],
                    delivery[3],
                    delivery[4].replace(b"value=1", b"value=2"),
                ],
                self.authority,
                SentinelVerifier(),
            )

    def test_comparison_unequal_records_agreed_hash_and_byte_canonical_attacks_reject(self):
        left_record = b"table_schema=public-sentinel\nvalue=1\n"
        right_record = b"table_schema=public-sentinel\nvalue=2\n"
        left = self._envelope(left_record, "semantic-judge-1")
        right = self._envelope(right_record, "semantic-judge-2")
        with self.assertRaisesRegex(CanonicalRecordError, "byte-identical"):
            serialize_comparison_record(
                "E43", left, right, self.authority, SentinelVerifier()
            )

        delivery = self._comparison_delivery("E43")
        record = parse_signed_envelope(
            delivery[2], self.authority, SentinelVerifier()
        ).record_bytes
        agreed_line = b"agreed_record_sha256=" + sha256_bytes(delivery[4]).encode()
        attacks = (
            record.replace(agreed_line, b"agreed_record_sha256=" + b"0" * 64),
            b"\xef\xbb\xbf" + record,
            record.replace(b"\n", b"\r\n", 1),
            record[:-1],
            record.replace(
                b"edge=E43\nleft_role=semantic-judge-1\n",
                b"left_role=semantic-judge-1\nedge=E43\n",
            ),
            record.replace(agreed_line, b"agreed_record_sha256=" + b"A" * 64),
        )
        for attack in attacks:
            with self.assertRaises(CanonicalRecordError):
                parse_comparison_record(attack)

    def test_publication_record_and_recipient_recomputation(self):
        decision = b"decision_schema=public-sentinel\nvalue=accepted\n"
        record = serialize_publication_record(decision, decision, 123)
        envelope = self._envelope(record, "public-record-publisher")
        verified = verify_publication_delivery(
            [decision, decision, envelope], self.authority, SentinelVerifier()
        )
        self.assertEqual(verified.published_record_bytes, decision)
        self.assertEqual(
            verified.publication_record.source_record_sha256,
            sha256_bytes(decision),
        )
        with self.assertRaisesRegex(CanonicalRecordError, "byte-identical"):
            serialize_publication_record(decision, decision + b"changed", 123)
        with self.assertRaisesRegex(CanonicalRecordError, "differ"):
            verify_publication_delivery(
                [decision, decision + b"changed", envelope],
                self.authority,
                SentinelVerifier(),
            )

    def test_publication_hash_role_and_decimal_attacks_reject(self):
        decision = b"decision_schema=public-sentinel\nvalue=accepted\n"
        record = serialize_publication_record(decision, decision, 9)
        source_line = b"source_record_sha256=" + sha256_bytes(decision).encode()
        attacks = (
            record.replace(
                b"published_record_sha256=" + sha256_bytes(decision).encode(),
                b"published_record_sha256=" + b"0" * 64,
            ),
            record.replace(b"monotonic_timestamp_ns=9", b"monotonic_timestamp_ns=01"),
            record.replace(b"monotonic_timestamp_ns=9", b"monotonic_timestamp_ns=-1"),
            record.replace(b"monotonic_timestamp_ns=9", b"monotonic_timestamp_ns=+1"),
            record.replace(source_line, b"source_record_sha256=" + b"A" * 64),
        )
        for attack in attacks:
            with self.assertRaises(CanonicalRecordError):
                parse_publication_record(attack)
        with self.assertRaisesRegex(CanonicalRecordError, "exact integer"):
            serialize_publication_record(decision, decision, True)
        wrong = self._envelope(record, "judgment-comparison")
        with self.assertRaisesRegex(CanonicalRecordError, "role"):
            verify_publication_delivery(
                [decision, decision, wrong], self.authority, SentinelVerifier()
            )

    def test_e56_binds_full_publication_envelope_without_double_hash(self):
        decision = b"decision_schema=public-sentinel\nvalue=accepted\n"
        publication_record = serialize_publication_record(decision, decision, 9)
        publication_envelope = self._envelope(
            publication_record, "public-record-publisher"
        )
        receipt = serialize_evidence_receipt(
            self.topology,
            "E56",
            "public-record-publisher",
            "publication-receipt-envelope-digest",
            sha256_bytes(publication_envelope),
        )
        receipt_envelope = self._envelope(receipt, "public-record-publisher")
        parsed = verify_e56_publication_receipt(
            publication_envelope,
            receipt_envelope,
            self.topology,
            self.authority,
            SentinelVerifier(),
        )
        self.assertEqual(parsed.artifact_sha256, sha256_bytes(publication_envelope))

        double_hash = sha256_bytes(
            sha256_bytes(publication_envelope).encode("ascii")
        )
        wrong_receipt = serialize_evidence_receipt(
            self.topology,
            "E56",
            "public-record-publisher",
            "publication-receipt-envelope-digest",
            double_hash,
        )
        with self.assertRaisesRegex(CanonicalRecordError, "binding"):
            verify_e56_publication_receipt(
                publication_envelope,
                self._envelope(wrong_receipt, "public-record-publisher"),
                self.topology,
                self.authority,
                SentinelVerifier(),
            )

        for label, wrong_record in (
            ("edge", receipt.replace(b"edge=E56", b"edge=E50")),
            (
                "role",
                receipt.replace(
                    b"producer_role=public-record-publisher",
                    b"producer_role=content-intake",
                ),
            ),
            (
                "kind",
                receipt.replace(
                    b"artifact_kind=publication-receipt-envelope-digest",
                    b"artifact_kind=decision-record-digest",
                ),
            ),
        ):
            with self.subTest(label=label):
                with self.assertRaises(CanonicalRecordError):
                    verify_e56_publication_receipt(
                        publication_envelope,
                        self._envelope(wrong_record, "public-record-publisher"),
                        self.topology,
                        self.authority,
                        SentinelVerifier(),
                    )
        with self.assertRaisesRegex(CanonicalRecordError, "role"):
            verify_e56_publication_receipt(
                publication_envelope,
                self._envelope(receipt, "content-intake"),
                self.topology,
                self.authority,
                SentinelVerifier(),
            )


if __name__ == "__main__":
    unittest.main()

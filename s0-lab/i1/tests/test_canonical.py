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
    parse_evidence_bundle,
    parse_signed_envelope,
    parse_status_record,
    serialize_evidence_bundle,
    serialize_evidence_receipt,
    serialize_root_bundle,
    serialize_status_record,
    signature_preimage,
    validate_status_chain,
)
from s0_i1.errors import CanonicalRecordError  # noqa: E402
from s0_i1.topology import load_public_runtime_spec  # noqa: E402


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
        cls.spec = load_public_runtime_spec(WORKSPACE)
        cls.keys = {role: key_id(role) for role in cls.spec["signer_roles"]}

    def _envelope(self, record: bytes, role: str) -> bytes:
        return assemble_signed_envelope(
            signature_preimage(record, role, self.keys[role]),
            SIGNATURE_SENTINEL,
        )

    def _receipt_envelope(self, edge: str, role: str, kind: str, byte: str) -> bytes:
        record = serialize_evidence_receipt(edge, role, kind, byte * 64)
        return self._envelope(record, role)

    def _two_pair_chain(self):
        root_bundle = serialize_root_bundle(MANIFEST_SENTINEL)
        root_record = serialize_status_record(
            0,
            "0" * 64,
            "ROOT",
            sha256_bytes(root_bundle),
            "0000",
            100,
        )
        root_envelope = self._envelope(root_record, "control-registrar")

        receipt_envelopes = [
            self._receipt_envelope("E02", "simulation-builder", "benchmark-summary", "1"),
            self._receipt_envelope("E02", "simulation-builder", "audit-summary", "2"),
            self._receipt_envelope("E02", "simulation-builder", "power-summary", "3"),
        ]
        e02_bundle = serialize_evidence_bundle("E02", receipt_envelopes)
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

    def test_signed_envelope_structure_uses_injected_verifier_once(self):
        record = serialize_evidence_receipt(
            "E05", "content-intake", "content-digest", "1" * 64
        )
        raw = self._envelope(record, "content-intake")
        verifier = SentinelVerifier()
        parsed = parse_signed_envelope(raw, self.keys, verifier, required_role="content-intake")
        self.assertEqual(parsed.record_bytes, record)
        self.assertEqual(len(verifier.calls), 1)
        self.assertEqual(verifier.calls[0]["preimage"], signature_preimage(record, "content-intake", self.keys["content-intake"]))

    def test_envelope_field_order_algorithm_hash_and_injected_rejection(self):
        record = serialize_evidence_receipt(
            "E05", "content-intake", "content-digest", "1" * 64
        )
        raw = self._envelope(record, "content-intake")
        length = f"record_length={len(record)}".encode("ascii")
        digest = f"record_sha256={sha256_bytes(record)}".encode("ascii")
        signature_line = f"signature_hex={SIGNATURE_SENTINEL}\n".encode("ascii")
        algorithm_line = b"signature_algorithm=Ed25519\n"
        attacks = (
            raw.replace(b"signature_algorithm=Ed25519", b"signature_algorithm=ed25519"),
            raw.replace(b"record_sha256=", b"record_digest="),
            raw.replace(length, f"record_length={len(record) + 1}".encode("ascii")),
            raw.replace(digest, b"record_sha256=" + b"0" * 64),
            raw.replace(algorithm_line + signature_line, signature_line + algorithm_line),
            raw + b"extra=1\n",
        )
        for attack in attacks:
            with self.subTest(attack=attack[-20:]):
                with self.assertRaises(CanonicalRecordError):
                    parse_signed_envelope(attack, self.keys, SentinelVerifier())
        with self.assertRaisesRegex(CanonicalRecordError, "injected"):
            parse_signed_envelope(raw, self.keys, SentinelVerifier(False))
        with self.assertRaisesRegex(CanonicalRecordError, "injected"):
            parse_signed_envelope(raw, self.keys, SentinelVerifier("rejected"))
        wrong_keys = dict(self.keys)
        wrong_keys["content-intake"] = "0" * 64
        with self.assertRaisesRegex(CanonicalRecordError, "role/key"):
            parse_signed_envelope(raw, wrong_keys, SentinelVerifier())

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
        valid = serialize_evidence_bundle("E25", [first, second])
        parsed = parse_evidence_bundle(
            valid,
            self.spec,
            self.keys,
            SentinelVerifier(),
            expected_control_integration_manifest_sha256=MANIFEST_SENTINEL,
        )
        self.assertEqual([receipt.producer_role for receipt in parsed.receipts], ["comparator-builder-1", "comparator-builder-2"])
        reversed_bundle = serialize_evidence_bundle("E25", [second, first])
        with self.assertRaises(CanonicalRecordError):
            parse_evidence_bundle(
                reversed_bundle,
                self.spec,
                self.keys,
                SentinelVerifier(),
                expected_control_integration_manifest_sha256=MANIFEST_SENTINEL,
            )
        missing = serialize_evidence_bundle("E25", [first])
        with self.assertRaisesRegex(CanonicalRecordError, "count"):
            parse_evidence_bundle(
                missing,
                self.spec,
                self.keys,
                SentinelVerifier(),
                expected_control_integration_manifest_sha256=MANIFEST_SENTINEL,
            )

    def test_receipt_result_and_identity_mutations_reject(self):
        valid = serialize_evidence_receipt(
            "E05", "content-intake", "content-digest", "4" * 64
        )
        mutated_result = valid.replace(b"accepted\n", b"rejected\n")
        mutated_identity = valid.replace(b"content-intake", b"simulation-builder")
        for record in (mutated_result, mutated_identity):
            envelope = self._envelope(record, "content-intake")
            bundle = serialize_evidence_bundle("E05", [envelope])
            with self.assertRaises(CanonicalRecordError):
                parse_evidence_bundle(
                    bundle,
                    self.spec,
                    self.keys,
                    SentinelVerifier(),
                    expected_control_integration_manifest_sha256=MANIFEST_SENTINEL,
                )

    def test_root_manifest_anchor_and_two_status_pairs_validate(self):
        root_pair, e02_pair, _ = self._two_pair_chain()
        verifier = SentinelVerifier()
        parsed = validate_status_chain(
            [root_pair, e02_pair],
            self.spec,
            self.keys,
            verifier,
            expected_control_integration_manifest_sha256=MANIFEST_SENTINEL,
        )
        self.assertEqual([pair.record.status_code for pair in parsed], ["A-0000", "A-0001"])
        with self.assertRaisesRegex(CanonicalRecordError, "ROOT manifest anchor mismatch"):
            validate_status_chain(
                [root_pair],
                self.spec,
                self.keys,
                SentinelVerifier(),
                expected_control_integration_manifest_sha256="0" * 64,
            )

    def test_status_mask_previous_hash_commitment_and_time_mutations_reject(self):
        root_pair, e02_pair, root_record = self._two_pair_chain()
        e02_bundle = e02_pair[1]
        cases = (
            serialize_status_record(2, sha256_bytes(root_record), "E02", sha256_bytes(e02_bundle), "0001", 101),
            serialize_status_record(1, sha256_bytes(root_record), "E02", sha256_bytes(e02_bundle), "0002", 101),
            serialize_status_record(1, "0" * 64, "E02", sha256_bytes(e02_bundle), "0001", 101),
            serialize_status_record(1, sha256_bytes(root_record), "E02", "0" * 64, "0001", 101),
            serialize_status_record(1, sha256_bytes(root_record), "E02", sha256_bytes(e02_bundle), "0001", 100),
        )
        for record in cases:
            pair = (self._envelope(record, "control-registrar"), e02_bundle)
            with self.assertRaises(CanonicalRecordError):
                validate_status_chain(
                    [root_pair, pair],
                    self.spec,
                    self.keys,
                    SentinelVerifier(),
                    expected_control_integration_manifest_sha256=MANIFEST_SENTINEL,
                )

    def test_status_serializer_and_parser_reject_invalid_event_syntax(self):
        for event in ("NOT-AN-EDGE", "E99"):
            with self.subTest(event=event):
                with self.assertRaisesRegex(CanonicalRecordError, "event edge"):
                    serialize_status_record(0, "0" * 64, event, "1" * 64, "0000", 1)
        valid = serialize_status_record(0, "0" * 64, "ROOT", "1" * 64, "0000", 1)
        for event in (b"NOT-AN-EDGE", b"E99"):
            with self.subTest(parsed_event=event):
                invalid = valid.replace(b"event_edge=ROOT", b"event_edge=" + event)
                with self.assertRaises(CanonicalRecordError):
                    parse_status_record(invalid)

    def test_complete_root_plus_fourteen_status_pair_chain(self):
        root_bundle = serialize_root_bundle(MANIFEST_SENTINEL)
        previous_record = serialize_status_record(
            0, "0" * 64, "ROOT", sha256_bytes(root_bundle), "0000", 1000
        )
        pairs = [(self._envelope(previous_record, "control-registrar"), root_bundle)]
        for sequence, row in enumerate(self.spec["status"]["receipts"], 1):
            envelopes = []
            for entry_index, entry in enumerate(row["entries"], 1):
                digest = hashlib.sha256(
                    f"{row['edge']}:{entry_index}".encode("ascii")
                ).hexdigest()
                receipt = serialize_evidence_receipt(
                    row["edge"],
                    entry["producer_role"],
                    entry["artifact_kind"],
                    digest,
                )
                envelopes.append(self._envelope(receipt, entry["producer_role"]))
            bundle = serialize_evidence_bundle(row["edge"], envelopes)
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
            self.spec,
            self.keys,
            SentinelVerifier(),
            expected_control_integration_manifest_sha256=MANIFEST_SENTINEL,
        )
        self.assertEqual(len(parsed), 15)
        self.assertEqual(parsed[-1].record.status_code, "A-3fff")
        self.assertEqual(self.spec["counts"]["e51_pairs"], len(parsed))


if __name__ == "__main__":
    unittest.main()

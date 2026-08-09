from __future__ import annotations

import sys
import unittest
from pathlib import Path
from types import MappingProxyType


WORKSPACE = Path(__file__).resolve().parents[3]
IMPLEMENTATION = WORKSPACE / "s0-lab" / "i1" / "implementation"
sys.path.insert(0, str(IMPLEMENTATION))

from s0_i1.errors import TopologyError  # noqa: E402
from s0_i1.topology import (  # noqa: E402
    EXPECTED_PAYLOAD_RECEIPT_SPLIT_EDGES,
    EXPECTED_ROLE_LABELS,
    EXPECTED_SOURCE_SHA256,
    EXPECTED_SIGNER_ROLES,
    STATUS_EDGE_ORDER,
    FrozenTopology,
    audit_topology,
    expected_edge_ids,
    expected_states,
    load_public_runtime_spec,
    require_frozen_topology,
    require_store_read,
    store_read_scope,
)


class TopologyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.topology = load_public_runtime_spec(WORKSPACE)

    def test_frozen_counts_and_closed_inventories(self):
        topology = require_frozen_topology(self.topology)
        self.assertIsInstance(topology, FrozenTopology)
        self.assertEqual(audit_topology(topology), [])
        self.assertEqual(topology["counts"]["role_rows"], 32)
        self.assertEqual(topology["counts"]["role_positions"], 40)
        self.assertEqual(topology["counts"]["paired_role_rows"], 8)
        self.assertEqual(topology["counts"]["stores"], 27)
        self.assertEqual(dict(topology["source_sha256"]), EXPECTED_SOURCE_SHA256)
        self.assertEqual(
            tuple(row["label"] for row in topology["role_rows"]),
            EXPECTED_ROLE_LABELS,
        )
        self.assertEqual(
            tuple(edge["id"] for edge in topology["edges"]), expected_edge_ids()
        )
        self.assertEqual(
            tuple(topology["payload_receipt_split_edges"]),
            EXPECTED_PAYLOAD_RECEIPT_SPLIT_EDGES,
        )
        self.assertEqual(tuple(topology["signer_roles"]), EXPECTED_SIGNER_ROLES)
        self.assertEqual(
            tuple(topology["status"]["edge_order"]), STATUS_EDGE_ORDER
        )
        self.assertEqual(tuple(topology["status"]["states"]), expected_states())

    def test_32_rows_are_not_recast_as_a_40_role_registry(self):
        positions = sum(len(row["positions"]) for row in self.topology["role_rows"])
        self.assertEqual(len(self.topology["role_rows"]), 32)
        self.assertEqual(positions, 40)
        self.assertEqual(len(self.topology["signer_roles"]), 22)
        self.assertNotEqual(positions, len(self.topology["signer_roles"]))

    def test_topology_is_deeply_immutable_and_detached_copies_have_no_authority(self):
        with self.assertRaises(TypeError):
            self.topology["status"]["receipts"][1]["entries"][0][
                "producer_role"
            ] = "simulation-builder"
        detached = self.topology.to_plain_dict()
        detached["status"]["receipts"][1]["entries"][0][
            "producer_role"
        ] = "simulation-builder"
        detached["stores"][23]["readers"].append(
            {
                "role": "public-executor",
                "position": "single",
                "edges": ["E39"],
                "scope": "full",
            }
        )
        self.assertTrue(audit_topology(detached))
        with self.assertRaises(TopologyError):
            require_store_read(
                detached, "public-executor", "single", "raw-output-vault"
            )
        with self.assertRaises(TopologyError):
            require_frozen_topology(detached)

    def test_digest_tampering_rejects_at_policy_boundary(self):
        original = self.topology.snapshot_sha256
        try:
            object.__setattr__(self.topology, "snapshot_sha256", "0" * 64)
            with self.assertRaisesRegex(TopologyError, "digest"):
                require_store_read(
                    self.topology,
                    "comparator-operators",
                    "1",
                    "comparator-vault-1",
                )
        finally:
            object.__setattr__(self.topology, "snapshot_sha256", original)
        require_frozen_topology(self.topology)

    def test_top_level_proxy_with_mutable_nested_containers_rejects(self):
        original = self.topology._snapshot
        forged_plain = self.topology.to_plain_dict()
        try:
            object.__setattr__(
                self.topology, "_snapshot", MappingProxyType(forged_plain)
            )
            with self.assertRaisesRegex(TopologyError, "deeply immutable"):
                require_frozen_topology(self.topology)
            forged_plain["status"]["states"][1] = "A-0002"
            with self.assertRaisesRegex(TopologyError, "deeply immutable"):
                require_store_read(
                    self.topology,
                    "comparator-operators",
                    "1",
                    "comparator-vault-1",
                )
        finally:
            object.__setattr__(self.topology, "_snapshot", original)
        require_frozen_topology(self.topology)

    def test_role_store_access_is_omission_denied_and_position_specific(self):
        self.assertEqual(
            store_read_scope(
                self.topology,
                "comparator-operators",
                "1",
                "comparator-vault-1",
            ),
            "full",
        )
        require_store_read(
            self.topology,
            "comparator-operators",
            "1",
            "comparator-vault-1",
        )
        with self.assertRaisesRegex(TopologyError, "cross-role"):
            require_store_read(
                self.topology,
                "comparator-operators",
                "1",
                "comparator-vault-2",
            )
        with self.assertRaises(TopologyError):
            require_store_read(
                self.topology, "registrar", "single", "condition-map-vault"
            )
        with self.assertRaises(TopologyError):
            require_store_read(
                self.topology, "public-executor", "single", "raw-output-vault"
            )

    def test_broader_cross_index_audit_reports_independent_failures(self):
        mutated = self.topology.to_plain_dict()
        mutated["role_rows"][0]["outbound_edges"].append("E99")
        mutated["stores"][13]["readers"][0]["position"] = "A"
        mutated["status"]["states"][1] = "A-0002"
        mutated["counts"]["stores"] = 26
        categories = {issue.category for issue in audit_topology(mutated)}
        self.assertIn("role-edge", categories)
        self.assertIn("store-position", categories)
        self.assertIn("status-state-order", categories)
        self.assertIn("declared-counts", categories)

    def test_receipt_position_store_and_signer_mutations_are_diagnostic_only(self):
        mutated = self.topology.to_plain_dict()
        mutated["status"]["receipts"][6]["entries"].pop()
        mutated["role_rows"][7]["positions"] = ["single"]
        mutated["stores"][0]["writer"]["role"] = "simulation-builder"
        mutated["signer_roles"][0] = "forged-role"
        categories = {issue.category for issue in audit_topology(mutated)}
        self.assertIn("receipt-count", categories)
        self.assertIn("receipt-total", categories)
        self.assertIn("role-position-count", categories)
        self.assertIn("signer-inventory", categories)


if __name__ == "__main__":
    unittest.main()

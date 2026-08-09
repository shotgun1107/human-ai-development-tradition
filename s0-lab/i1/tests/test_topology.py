from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path


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
    audit_topology,
    expected_edge_ids,
    expected_states,
    load_public_runtime_spec,
    require_store_read,
    store_read_scope,
)


class TopologyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = load_public_runtime_spec(WORKSPACE)

    def test_frozen_counts_and_closed_inventories(self):
        self.assertEqual(audit_topology(self.spec), [])
        self.assertEqual(self.spec["counts"]["role_rows"], 32)
        self.assertEqual(self.spec["counts"]["role_positions"], 40)
        self.assertEqual(self.spec["counts"]["paired_role_rows"], 8)
        self.assertEqual(self.spec["counts"]["stores"], 27)
        self.assertEqual(self.spec["source_sha256"], EXPECTED_SOURCE_SHA256)
        self.assertEqual(tuple(row["label"] for row in self.spec["role_rows"]), EXPECTED_ROLE_LABELS)
        self.assertEqual(tuple(edge["id"] for edge in self.spec["edges"]), expected_edge_ids())
        self.assertEqual(tuple(self.spec["payload_receipt_split_edges"]), EXPECTED_PAYLOAD_RECEIPT_SPLIT_EDGES)
        self.assertEqual(tuple(self.spec["signer_roles"]), EXPECTED_SIGNER_ROLES)
        self.assertEqual(tuple(self.spec["status"]["edge_order"]), STATUS_EDGE_ORDER)
        self.assertEqual(tuple(self.spec["status"]["states"]), expected_states())

    def test_32_rows_are_not_recast_as_a_40_role_registry(self):
        positions = sum(len(row["positions"]) for row in self.spec["role_rows"])
        self.assertEqual(len(self.spec["role_rows"]), 32)
        self.assertEqual(positions, 40)
        self.assertEqual(len(self.spec["signer_roles"]), 22)
        self.assertNotEqual(positions, len(self.spec["signer_roles"]))

    def test_role_store_access_is_omission_denied_and_position_specific(self):
        self.assertEqual(
            store_read_scope(self.spec, "comparator-operators", "1", "comparator-vault-1"),
            "full",
        )
        require_store_read(self.spec, "comparator-operators", "1", "comparator-vault-1")
        with self.assertRaisesRegex(TopologyError, "cross-role"):
            require_store_read(self.spec, "comparator-operators", "1", "comparator-vault-2")
        with self.assertRaises(TopologyError):
            require_store_read(self.spec, "registrar", "single", "condition-map-vault")
        with self.assertRaises(TopologyError):
            require_store_read(self.spec, "public-executor", "single", "raw-output-vault")

    def test_broader_cross_index_audit_reports_independent_failures(self):
        mutated = copy.deepcopy(self.spec)
        mutated["role_rows"][0]["outbound_edges"].append("E99")
        mutated["stores"][13]["readers"][0]["position"] = "A"
        mutated["status"]["states"][1] = "A-0002"
        mutated["counts"]["stores"] = 26
        categories = {issue.category for issue in audit_topology(mutated)}
        self.assertIn("role-edge", categories)
        self.assertIn("store-position", categories)
        self.assertIn("status-state-order", categories)
        self.assertIn("declared-counts", categories)

    def test_status_receipt_inventory_mutation_fails(self):
        mutated = copy.deepcopy(self.spec)
        mutated["status"]["receipts"][6]["entries"].pop()
        categories = {issue.category for issue in audit_topology(mutated)}
        self.assertIn("receipt-count", categories)
        self.assertIn("receipt-total", categories)


if __name__ == "__main__":
    unittest.main()

"""F06 frozen accounting identities only; no production calculator exists.

Decimal values are invented arithmetic unit examples, not observed costs,
financial rates, or S0/E0 synthetic fixtures. This checks the CONTROL-frozen
correction contract; a later reviewer must compare the erratum to the contract.
No staffing, time, call, token, execution, safety, or economic claim is tested.
"""

from collections import Counter
from decimal import Decimal
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import unittest


D = Decimal
BUCKETS = ("R", "H", "R_reserve", "H_reserve")
CATEGORIES = ("AI", "human", "replacement", "tools_storage", "other_approved")
DIRECT = tuple(f"C_{category}_{bucket}_max"
               for bucket in BUCKETS for category in CATEGORIES)
FIXED = tuple(f"C_{category}_fixed_max" for category in CATEGORIES)
AI_RESTART = "C_AI_Q_restart_fixed_max"  # Excluded from base AI fixed.
Q_MEMO = "C_human_Q_restart_fixed_max"  # Included subset of human fixed.
CASH_TERMS = DIRECT + FIXED + (AI_RESTART,)
REQUIRED = frozenset(CASH_TERMS + (Q_MEMO,))


def checked_rows(rows):
    """Test-only classification guard; unknown costs require STOP/DEFER."""
    if set(rows) != REQUIRED:
        raise ValueError("STOP/DEFER: missing or unclassified cost row")
    if any(not isinstance(value, D) or not value.is_finite() or value < 0
           for value in rows.values()):
        raise ValueError("STOP/DEFER: invalid cost value")
    if rows[Q_MEMO] > rows["C_human_fixed_max"]:
        raise ValueError("STOP/DEFER: Q memo exceeds containing human fixed")
    return rows


def cash_identity(rows):
    rows = checked_rows(rows)
    return sum((rows[term] for term in CASH_TERMS), D(0))


def attributed_human_identity(rows, allocation):
    rows = checked_rows(rows)
    if set(allocation) != set(BUCKETS):
        raise ValueError("STOP/DEFER: missing or unknown allocation bucket")
    if any(not isinstance(value, D) or not value.is_finite() or value < 0
           for value in allocation.values()) or sum(allocation.values()) != 1:
        raise ValueError("STOP/DEFER: invalid fixed allocation")
    return {bucket: rows[f"C_human_{bucket}_max"]
            + allocation[bucket] * rows["C_human_fixed_max"]
            for bucket in BUCKETS}


class CostDefinitionTests(unittest.TestCase):
    def rows(self, **updates):
        return dict.fromkeys(REQUIRED, D(0)) | updates

    def allocation(self):
        return dict(zip(BUCKETS, map(D, ("0.1", "0.2", "0.3", "0.4"))))

    def test_symbolic_map_has_each_physical_term_once_and_memo_zero(self):
        counts = Counter(CASH_TERMS)
        self.assertEqual(len(counts), 26)
        self.assertTrue(all(count == 1 for count in counts.values()))
        self.assertEqual(counts[Q_MEMO], 0)
        self.assertEqual(set(counts), set(DIRECT) | set(FIXED) | {AI_RESTART})

    def test_each_physical_row_has_unit_coefficient(self):
        for term in CASH_TERMS:
            with self.subTest(term=term):
                self.assertEqual(cash_identity(self.rows(**{term: D("1.25")})),
                                 D("1.25"))

    def test_primary_q_zero_nonzero_and_entire_fixed_subset(self):
        for base, q in (("11", "0"), ("11", "7"), ("0", "7")):
            with self.subTest(base=base, q=q):
                rows = self.rows(C_human_fixed_max=D(base) + D(q),
                                 **{Q_MEMO: D(q)})
                corrected = cash_identity(rows)
                self.assertEqual(corrected, D(base) + D(q))
                historical_extra_term = corrected + rows[Q_MEMO]
                self.assertEqual(historical_extra_term - corrected, D(q))
                if D(q):
                    self.assertNotEqual(historical_extra_term, D(base) + D(q))

    def test_q_memo_is_informational_when_fixed_is_unchanged(self):
        rows = self.rows(C_human_fixed_max=D("18"))
        self.assertEqual(cash_identity(rows),
                         cash_identity(rows | {Q_MEMO: D("7")}))

    def test_replacement_and_ai_restart_are_separate_once(self):
        rows = self.rows(C_human_fixed_max=D("18"),
                         C_replacement_fixed_max=D("3"),
                         C_AI_fixed_max=D("5"),
                         **{Q_MEMO: D("7"), AI_RESTART: D("2")})
        # Human base 11 + primary Q 7 + replacement 3 + AI base 5 + restart 2.
        self.assertEqual(cash_identity(rows), D("28"))
        self.assertEqual(cash_identity(rows | {"C_replacement_fixed_max": D(0)}),
                         D("25"))
        self.assertEqual(cash_identity(rows | {AI_RESTART: D(0)}), D("26"))

    def test_four_bucket_human_conservation_and_two_distinct_views(self):
        rows = self.rows(C_human_fixed_max=D("10"), **{Q_MEMO: D("4")})
        rows.update({f"C_human_{bucket}_max": D(index)
                     for index, bucket in enumerate(BUCKETS, 1)})
        attributed = attributed_human_identity(rows, self.allocation())
        self.assertEqual(tuple(attributed.values()), tuple(map(D, (2, 4, 6, 8))))
        physical = rows["C_human_fixed_max"] + sum(
            rows[f"C_human_{bucket}_max"] for bucket in BUCKETS)
        self.assertEqual(physical, D("20"))
        self.assertEqual(sum(attributed.values()), physical)
        self.assertEqual(cash_identity(rows), physical)
        self.assertNotEqual(physical + sum(attributed.values()), physical)
        with self.assertRaises(ValueError):
            cash_identity(rows | {"C_human_R_attributed_max": attributed["R"]})

    def test_zero_and_single_bucket_allocations_conserve(self):
        for fixed in (D(0), D("12")):
            for bucket in BUCKETS:
                with self.subTest(fixed=fixed, bucket=bucket):
                    rows = self.rows(C_human_fixed_max=fixed, **{Q_MEMO: fixed})
                    allocation = dict.fromkeys(BUCKETS, D(0)) | {bucket: D(1)}
                    result = attributed_human_identity(rows, allocation)
                    self.assertEqual(sum(result.values()), fixed)
                    self.assertEqual(result[bucket], fixed)

    def test_missing_unknown_and_negative_costs_stop(self):
        for term in REQUIRED:
            with self.subTest(term=term):
                missing = self.rows()
                del missing[term]
                with self.assertRaises(ValueError):
                    cash_identity(missing)
                with self.assertRaises(ValueError):
                    cash_identity(self.rows(**{term: D("-1")}))
        with self.assertRaises(ValueError):
            cash_identity(self.rows(unclassified_cost=D(0)))

    def test_invalid_q_subset_and_nonfinite_values_stop(self):
        with self.assertRaises(ValueError):
            cash_identity(self.rows(C_human_fixed_max=D(1), **{Q_MEMO: D(2)}))
        for value in (D("NaN"), D("Infinity"), "1", None):
            with self.subTest(value=str(value)):
                with self.assertRaises(ValueError):
                    cash_identity(self.rows(C_human_fixed_max=value))

    def test_invalid_or_incomplete_allocation_stops(self):
        valid = self.allocation()
        bad = [valid | {"R": D("-0.1")}, valid | {"R": D("0.2")},
               valid | {"unknown": D(0)}, valid | {"R": D("NaN")},
               valid | {"R": "0.1"}]
        bad.extend({key: value for key, value in valid.items() if key != bucket}
                   for bucket in BUCKETS)
        for allocation in bad:
            with self.subTest(allocation=str(allocation)):
                with self.assertRaises(ValueError):
                    attributed_human_identity(self.rows(), allocation)


def record_evidence():
    """Owned runner writes only the two explicitly authorized raw outputs."""
    root = Path(__file__).resolve().parents[4]
    source = "docs/tradition/e0-effect-test/e0-operating-cost-and-gates-v0.4.md"
    pins = {"AGENTS.md": "4aac0c255dea03b85f6fb98b0b89f5b3c3f348e42c4dcaaf423411b818e3a065",
            source: "9124990ebfd328a8628728317cbce62385a2a059e888e30c300eb55627409057"}
    expected_git = {"branch": "codex/windows-build-toolchain-environment-v0.1",
                    "head": "cc76d7e82aeb51dfdc7baba3da0f7993ab2da61a",
                    "tree": "82c02f37fd13ecfc8c7b888bb66127989b6d4f34"}

    def authenticate():
        hashes = {name: hashlib.sha256((root / name).read_bytes()).hexdigest()
                  for name in pins}
        identity = {}
        for key, args in (("branch", ["branch", "--show-current"]),
                          ("head", ["rev-parse", "HEAD"]),
                          ("tree", ["rev-parse", "HEAD^{tree}"])):
            result = subprocess.run(["git", "-C", str(root), *args],
                                    stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                                    text=True, check=False)
            if result.returncode:
                raise RuntimeError(f"Git {key} query failed: {result.returncode}")
            identity[key] = result.stdout.strip()
        if hashes != pins or identity != expected_git:
            raise RuntimeError("Pinned policy, source, or Git identity mismatch")
        return {"sha256": hashes, "git": identity}

    before = authenticate()
    stream = io.StringIO()
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(CostDefinitionTests)
    result = unittest.TextTestRunner(stream=stream, verbosity=2).run(suite)
    after = authenticate()
    output = Path(__file__).resolve().parents[1] / "verification"
    output.mkdir(exist_ok=True)
    raw = stream.getvalue()
    (output / "test-stdout.txt").write_text(raw, encoding="utf-8", newline="\n")
    evidence = {"candidate": "a03-cost-definition-v0.1", "role": "TEST/VERIFICATION",
                "scope": "Frozen symbolic identities and invented Decimal arithmetic only",
                "not_tested": ["production implementation (none exists)",
                               "later erratum wording", "real costs or financial rates",
                               "S0/E0 execution or scoring", "economic or safety value",
                               "staffing feasibility", "hostile host/import/TOCTOU/ACL isolation"],
                "python": sys.version, "executable": sys.executable,
                "flags": {"isolated": sys.flags.isolated, "no_site": sys.flags.no_site,
                          "dont_write_bytecode": sys.dont_write_bytecode},
                "reproduce": [sys.executable, "-I", "-S", "-B", str(Path(__file__).resolve()),
                              "--record"], "before": before, "after": after,
                "test_file_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "stdout_sha256": hashlib.sha256(raw.encode("utf-8")).hexdigest(),
                "tests_run": result.testsRun, "failures": len(result.failures),
                "errors": len(result.errors), "skipped": len(result.skipped),
                "successful": result.wasSuccessful()}
    (output / "test-results.json").write_text(
        json.dumps(evidence, indent=2, ensure_ascii=True) + "\n", encoding="utf-8", newline="\n")
    print(raw, end="")
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    if sys.argv[1:] == ["--record"]:
        raise SystemExit(record_evidence())
    unittest.main(verbosity=2)

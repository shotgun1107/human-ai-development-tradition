from __future__ import annotations

from dataclasses import replace
import gc
import hashlib
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
import weakref


CANDIDATE_ROOT = Path(__file__).resolve().parents[1]
IMPLEMENTATION_ROOT = CANDIDATE_ROOT / "implementation"
AUTHENTICODE_ROOT = (
    CANDIDATE_ROOT.parent
    / "windows-authenticode-verifier-v0.4"
    / "implementation"
)
sys.path.insert(0, str(AUTHENTICODE_ROOT))
sys.path.insert(0, str(IMPLEMENTATION_ROOT))

from s0_external_artifact_authority_acquisition import buildtools
from s0_external_artifact_authority_acquisition.errors import AuthorityError
from s0_windows_authenticode_verifier import verifier as authenticode_verifier
from s0_windows_authenticode_verifier.model import VerificationResult


BLOCKER = "BUILD-TOOLS-AUTHENTICODE-TRANSITIVE-CLOSURE-UNVERIFIED"


def _arguments() -> dict[str, object]:
    return {
        "release_history_raw": b"bounded-test-release-history",
        "verifier_full_path": "C:\\bounded\\vs_BuildTools.exe",
        "file_handle": 7,
        "sequence_id": "1" * 64,
        "producer_process_id": 11,
        "created_filetime_hex": "0000000000000001",
        "acquired_path": (
            "\\\\?\\Volume{01234567-89AB-CDEF-0123-456789ABCDEF}\\"
            "bounded\\vs_BuildTools.exe"
        ),
        "volume_serial_hex": "2" * 16,
        "file_id_hex": "3" * 32,
    }


def _verification_result() -> VerificationResult:
    trace_raw = b'{"test":"private-trace"}\n'
    decision_raw = b'{"test":"private-decision"}\n'
    return VerificationResult(
        observation_sha256="a" * 64,
        trace_raw=trace_raw,
        trace_sha256=hashlib.sha256(trace_raw).hexdigest(),
        decision_raw=decision_raw,
        decision_sha256=hashlib.sha256(decision_raw).hexdigest(),
        trust_policy_pass=True,
        failure_relations=(),
    )


def _private_adapter():
    original = buildtools.validate_microsoft_release_metadata
    try:
        buildtools.validate_microsoft_release_metadata = lambda _raw: object()
        return buildtools._freeze_buildtools_adapter(
            lambda **_kwargs: _verification_result(),
            include_issuance_checker=True,
        )
    finally:
        buildtools.validate_microsoft_release_metadata = original


class EntrypointIsolationTests(unittest.TestCase):
    def test_public_blocker_precedes_authentic_historical_verifier_and_checker(self) -> None:
        self.assertEqual(
            authenticode_verifier.verify_open_file_trusted_host.__module__,
            "s0_windows_authenticode_verifier.verifier",
        )
        with self.assertRaisesRegex(AuthorityError, f"^{BLOCKER}$"):
            buildtools.verify_buildtools_and_propose_pin(**_arguments())
        with self.assertRaisesRegex(AuthorityError, f"^{BLOCKER}$"):
            buildtools._require_issued_buildtools_proposal(object())

    def test_public_blocker_precedes_every_reachable_rebound_verifier_global(self) -> None:
        calls: list[str] = []

        def tracker(name: str):
            def tracked(*_args, **_kwargs):
                calls.append(name)
                raise AssertionError(f"rebound v0.4 global invoked: {name}")

            return tracked

        callable_cases = {
            "authenticate_installed_implementation": tracker("authority"),
            "authenticate_acquisition_record": tracker("acquisition"),
            "os": SimpleNamespace(getpid=tracker("getpid")),
            "collect_observation": tracker("collector"),
            "canonical_json_lf": tracker("exception_encoder"),
            "evaluate_observation": tracker("semantic"),
        }
        value_cases = {
            "NativeVerificationError": RuntimeError,
            "VerificationError": LookupError,
            "OSError": ArithmeticError,
            "OverflowError": MemoryError,
            "ValueError": KeyError,
            "OBSERVATION_SCHEMA_ID": "ATTACKER-REBOUND-SCHEMA",
        }
        missing = object()
        for name, replacement in {**callable_cases, **value_cases}.items():
            original = getattr(authenticode_verifier, name, missing)
            try:
                setattr(authenticode_verifier, name, replacement)
                with self.subTest(rebound=name), self.assertRaisesRegex(
                    AuthorityError, f"^{BLOCKER}$"
                ):
                    buildtools.verify_buildtools_and_propose_pin(**_arguments())
            finally:
                if original is missing:
                    delattr(authenticode_verifier, name)
                else:
                    setattr(authenticode_verifier, name, original)
        self.assertEqual(calls, [])

    def test_private_seam_is_bounded_separate_and_recovers_after_drop(self) -> None:
        adapter, checker = _private_adapter()
        first = adapter(**_arguments())
        first_raw = first.acquisition_record_raw
        self.assertIs(checker(first), first)
        with self.assertRaisesRegex(
            AuthorityError, "buildtools_proposal_registry_capacity_exceeded"
        ):
            adapter(**_arguments())
        with self.assertRaisesRegex(
            AuthorityError, "buildtools_proposal_not_issued_or_changed"
        ):
            checker(replace(first))
        original_size = first.size
        try:
            object.__setattr__(first, "size", original_size + 1)
            with self.assertRaisesRegex(
                AuthorityError, "buildtools_proposal_not_issued_or_changed"
            ):
                checker(first)
        finally:
            object.__setattr__(first, "size", original_size)
        try:
            object.__setattr__(
                first,
                "acquisition_record_raw",
                bytes(bytearray(first.acquisition_record_raw)),
            )
            with self.assertRaisesRegex(
                AuthorityError, "buildtools_proposal_not_issued_or_changed"
            ):
                checker(first)
        finally:
            object.__setattr__(first, "acquisition_record_raw", first_raw)
        self.assertIs(checker(first), first)
        with self.assertRaisesRegex(AuthorityError, f"^{BLOCKER}$"):
            buildtools._require_issued_buildtools_proposal(first)

        dropped = weakref.ref(first)
        del first
        gc.collect()
        self.assertIsNone(dropped())
        recovered = adapter(**_arguments())
        self.assertIs(checker(recovered), recovered)

    def test_path_roles_remain_distinct_in_private_test_seam(self) -> None:
        calls: list[dict[str, object]] = []

        def verifier(**kwargs):
            calls.append(dict(kwargs))
            return _verification_result()

        original = buildtools.validate_microsoft_release_metadata
        try:
            buildtools.validate_microsoft_release_metadata = lambda _raw: object()
            adapter = buildtools._freeze_buildtools_adapter(verifier)
        finally:
            buildtools.validate_microsoft_release_metadata = original

        arguments = _arguments()
        proposal = adapter(**arguments)
        self.assertEqual(proposal.acquired_path, arguments["acquired_path"])
        self.assertEqual(proposal.verifier_full_path, arguments["verifier_full_path"])
        record = proposal.acquisition_record_raw.decode("utf-8")
        self.assertIn(str(arguments["acquired_path"]).replace("\\", "\\\\"), record)
        self.assertNotIn("verifier_full_path", record)
        self.assertEqual(calls[0]["full_path"], arguments["verifier_full_path"])


if __name__ == "__main__":
    unittest.main(verbosity=2)

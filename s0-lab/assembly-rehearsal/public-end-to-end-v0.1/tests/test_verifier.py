from __future__ import annotations

import copy
import hashlib
import importlib.util
import os
import pickle
import shutil
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path


HERE = Path(__file__).resolve()
WORKSPACE = next(parent for parent in HERE.parents if (parent / "AGENTS.md").is_file())
IMPLEMENTATION = HERE.parents[1] / "implementation"
sys.path.insert(0, str(IMPLEMENTATION))

from s0_public_assembly_verifier.authority import (  # noqa: E402
    _authority_copy_negative_matrix,
    _is_witness,
)
from s0_public_assembly_verifier.canonical import (  # noqa: E402
    RUN_RECORD_SHA256,
    canonical_json_bytes,
    expected_receipt_bytes,
    expected_run_record_bytes,
)
from s0_public_assembly_verifier.consumer import (  # noqa: E402
    LiveDecision,
    LiveConsumer,
    _exercise_consumer_predicates_for_tests,
)
from s0_public_assembly_verifier.errors import AssemblyFailure  # noqa: E402
from s0_public_assembly_verifier.integrity import (  # noqa: E402
    verify_component_implementations,
    verify_v0_5_design_authority,
)
from s0_public_assembly_verifier.models import (  # noqa: E402
    FileIdentity,
    FileSnapshot,
    MoveResult,
)
from s0_public_assembly_verifier.observer import PublicationObserver  # noqa: E402
from s0_public_assembly_verifier.pins import (  # noqa: E402
    DESIGN_INDEPENDENT_REVIEW_SHA256,
    DESIGN_PACKAGE_MANIFEST_SHA256,
    ExternalPins,
)
from s0_public_assembly_verifier.source_audit import (  # noqa: E402
    audit_candidate_source,
    audit_win32_source,
    audit_win32_source_text,
)
from s0_public_assembly_verifier.win32 import (  # noqa: E402
    MoveFileExBinding,
    Win32PublicationBackend,
    _configure_move_file_ex,
    _is_authenticated_win32_backend,
)


IMPLEMENTATION_PIN = "a" * 64


def pins() -> ExternalPins:
    return ExternalPins(
        IMPLEMENTATION_PIN,
        DESIGN_PACKAGE_MANIFEST_SHA256,
        DESIGN_INDEPENDENT_REVIEW_SHA256,
    )


class _Callable:
    argtypes = None
    restype = None

    def __call__(self, *args: object) -> int:
        raise AssertionError("synthetic no-call binding invoked the function")


class FakeBackend:
    def __init__(self, root: Path) -> None:
        self.output_root = root
        self.root_identity = FileIdentity(11, 22, 33)
        self._identities: dict[str, FileIdentity] = {
            "run-record.pending": FileIdentity(11, 1, 1),
            "publication-receipt.pending": FileIdentity(11, 2, 2),
        }

    def canonical_event_path(self, path: Path) -> str:
        return str((self.output_root / path).resolve())

    def path_absent(self, path: Path) -> bool:
        return not (self.output_root / path).exists()

    def inspect_file(self, path: Path) -> FileSnapshot:
        target = self.output_root / path
        raw = target.read_bytes()
        identity = self._identities.get(path.name)
        if identity is None:
            raise AssertionError(f"identity is missing for {path.name}")
        return FileSnapshot(identity, len(raw), hashlib.sha256(raw).hexdigest())

    def move_no_replace(self, source: Path, destination: Path) -> MoveResult:
        source_path = self.output_root / source
        destination_path = self.output_root / destination
        if destination_path.exists():
            return MoveResult(0, 80)
        os.rename(source_path, destination_path)
        self._identities[destination.name] = self._identities.pop(source.name)
        return MoveResult(1, 0)


class ContractTests(unittest.TestCase):
    def test_public_authorities_authenticate(self) -> None:
        self.assertEqual(len(verify_v0_5_design_authority(WORKSPACE)), 5)
        self.assertEqual(verify_component_implementations(WORKSPACE), {"i0": 15, "i1": 26, "i2": 16, "i3": 17})

    def test_exact_record_and_receipt(self) -> None:
        record = expected_run_record_bytes(WORKSPACE)
        receipt = expected_receipt_bytes(WORKSPACE, pins().receipt_fields())
        self.assertEqual(len(record), 2224)
        self.assertEqual(hashlib.sha256(record).hexdigest(), RUN_RECORD_SHA256)
        self.assertEqual(len(receipt), 1173)

    def test_every_record_field_mutation_changes_bytes(self) -> None:
        import json

        original = json.loads(expected_run_record_bytes(WORKSPACE))
        baseline = canonical_json_bytes(original)
        for key in original:
            changed = dict(original)
            value = changed[key]
            changed[key] = (not value) if type(value) is bool else value + 1 if type(value) is int else value + "-mutated"
            self.assertNotEqual(canonical_json_bytes(changed), baseline, key)

    def test_every_receipt_field_mutation_changes_bytes(self) -> None:
        import json

        original = json.loads(expected_receipt_bytes(WORKSPACE, pins().receipt_fields()))
        baseline = canonical_json_bytes(original)
        for key in original:
            changed = dict(original)
            value = changed[key]
            changed[key] = value + 1 if type(value) is int else value + "-mutated"
            self.assertNotEqual(canonical_json_bytes(changed), baseline, key)

    def test_pin_forms_and_stale_pins_reject(self) -> None:
        invalid = ("", "A" * 64, "g" * 64, "0" * 63, "0" * 65)
        for value in invalid:
            with self.assertRaises(ValueError):
                ExternalPins(value, DESIGN_PACKAGE_MANIFEST_SHA256, DESIGN_INDEPENDENT_REVIEW_SHA256)
        with self.assertRaises(ValueError):
            ExternalPins(IMPLEMENTATION_PIN, "b" * 64, DESIGN_INDEPENDENT_REVIEW_SHA256)
        with self.assertRaises(ValueError):
            ExternalPins(IMPLEMENTATION_PIN, DESIGN_PACKAGE_MANIFEST_SHA256, "b" * 64)

    def test_source_audits_and_synthetic_binding(self) -> None:
        verifier_root = IMPLEMENTATION / "s0_public_assembly_verifier"
        audit_win32_source(verifier_root / "win32.py")
        candidate_root = IMPLEMENTATION / "s0_public_assembly_candidate"
        if candidate_root.is_dir():
            audit_candidate_source(candidate_root)
        function = _Callable()
        self.assertIs(MoveFileExBinding.synthetic_no_call_binding(function), function)
        import ctypes

        self.assertEqual(function.argtypes, [ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32])
        self.assertIs(function.restype, ctypes.c_int32)

    def test_source_mutations_reject(self) -> None:
        text = (IMPLEMENTATION / "s0_public_assembly_verifier" / "win32.py").read_text(encoding="utf-8")
        mutations = {
            "loader": text.replace('ctypes.WinDLL("kernel32", use_last_error=True)', 'ctypes.CDLL("kernel32")', 1),
            "argtype": text.replace("ctypes.c_wchar_p", "ctypes.c_char_p", 1),
            "flagtype": text.replace("ctypes.c_uint32", "ctypes.c_int32", 1),
            "error-reset": text.replace("ctypes.set_last_error(0)", "pass", 1),
            "error-read": text.replace("ctypes.get_last_error()", "0", 1),
            "flags": text.replace("flags != 0", "flags != 1", 1),
            "export": text.replace("kernel32.MoveFileExW", "kernel32.MoveFileW", 1),
            "other-dll": text.replace('ctypes.WinDLL("kernel32", use_last_error=True)', 'ctypes.WinDLL("user32", use_last_error=True)', 1),
            "extra-loader": text + '\nctypes.WinDLL("kernel32", use_last_error=True)\n',
            "extra-call": text.replace(
                "return self._move.call(source_text, destination_text, 0)",
                "self._move.call(source_text, destination_text, 0)\n        return self._move.call(source_text, destination_text, 0)",
                1,
            ),
            "fallback": text + '\nCopyFileW = None\n',
            "delayed-error": text.replace(
                "last_error = ctypes.get_last_error()",
                "marker = 0\n            last_error = ctypes.get_last_error()",
                1,
            ),
            "success-read": text.replace("last_error = 0", "last_error = ctypes.get_last_error()", 1),
        }
        for label, mutation in mutations.items():
            with self.subTest(label=label):
                with self.assertRaises(AssemblyFailure):
                    audit_win32_source_text(mutation)

        candidate_root = IMPLEMENTATION / "s0_public_assembly_candidate"
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for label, source in {
                "ffi-import": "import ctypes\n",
                "network-import": "import socket\n",
                "direct-rename": "import os\nos.rename('a', 'b')\n",
                "observer-reference": "PublicationObserver()\n",
            }.items():
                path = root / f"{label}.py"
                path.write_text(source, encoding="utf-8")
                with self.subTest(label=label):
                    with self.assertRaises(AssemblyFailure):
                        audit_candidate_source(root)
                path.unlink()
        audit_candidate_source(candidate_root)

    def test_live_authority_types_cannot_be_fabricated(self) -> None:
        with self.assertRaises(TypeError):
            LiveDecision()
        with self.assertRaises(TypeError):
            LiveDecision(True)
        fabricated_decision = object.__new__(LiveDecision)
        with self.assertRaises(TypeError):
            _ = fabricated_decision.accepted
        with self.assertRaises(TypeError):
            copy.copy(fabricated_decision)
        with self.assertRaises(TypeError):
            copy.deepcopy(fabricated_decision)
        with self.assertRaises(TypeError):
            pickle.dumps(fabricated_decision)
        forged = object.__new__(Win32PublicationBackend)
        forged.output_root = WORKSPACE
        forged._sealed = True
        self.assertFalse(_is_authenticated_win32_backend(forged))


class AuthorityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "run-record.pending").write_bytes(expected_run_record_bytes(WORKSPACE))
        (self.root / "publication-receipt.pending").write_bytes(
            expected_receipt_bytes(WORKSPACE, pins().receipt_fields())
        )
        self.backend = FakeBackend(self.root)
        self.child = object()
        self.pipe = object()
        self.observer = PublicationObserver(
            backend=self.backend,
            child_identity=self.child,
            parent_pipe_identity=self.pipe,
        )

    def tearDown(self) -> None:
        self.temp.cleanup()

    def publish(self) -> object:
        reply1, witness1 = self.observer.observe_message(
            b"PUBLISH_RECORD\n",
            child_identity=self.child,
            parent_pipe_identity=self.pipe,
        )
        self.assertEqual(reply1, b"OK\n")
        self.assertIsNone(witness1)
        reply2, witness2 = self.observer.observe_message(
            b"PUBLISH_RECEIPT\n",
            child_identity=self.child,
            parent_pipe_identity=self.pipe,
        )
        self.assertEqual(reply2, b"OK\n")
        self.assertTrue(_is_witness(witness2))
        return witness2

    def consume(self, witness: object, **overrides: object) -> bool:
        arguments = {
            "workspace_root": WORKSPACE,
            "observer": self.observer,
            "witness": witness,
            "child_identity": self.child,
            "parent_pipe_identity": self.pipe,
            "external_pins": pins(),
            "quarantined": False,
        }
        arguments.update(overrides)
        return _exercise_consumer_predicates_for_tests(**arguments).predicates_satisfied

    def test_positive_and_one_use(self) -> None:
        witness = self.publish()
        self.assertEqual(tuple(event.ordinal for event in self.observer.trace), (1, 2))
        self.assertTrue(all(event.field_count() == 23 for event in self.observer.trace))
        self.assertTrue(self.consume(witness))
        with self.assertRaises(AssemblyFailure):
            self.consume(witness)

    def test_fake_backend_never_returns_live_acceptance(self) -> None:
        witness = self.publish()
        with self.assertRaises(AssemblyFailure):
            LiveConsumer().consume(
                workspace_root=WORKSPACE,
                observer=self.observer,
                witness=witness,
                child_identity=self.child,
                parent_pipe_identity=self.pipe,
                external_pins=pins(),
                quarantined=False,
            )

    def test_authority_copy_pickle_and_foreign_object_reject(self) -> None:
        witness = self.publish()
        self.assertEqual(_authority_copy_negative_matrix(witness), (True, True))
        with self.assertRaises(TypeError):
            pickle.dumps(witness)
        with self.assertRaises(AssemblyFailure):
            self.consume(object())

    def test_reordered_duplicate_extra_nonascii_and_wrong_binding_reject(self) -> None:
        cases = (
            b"PUBLISH_RECEIPT\n",
            b"PUBLISH_RECORD\nEXTRA",
            b"PUBLISH_RECORD",
            b"\xff\n",
        )
        for message in cases:
            with self.subTest(message=message):
                self.tearDown()
                self.setUp()
                with self.assertRaises(AssemblyFailure):
                    self.observer.observe_message(message, child_identity=self.child, parent_pipe_identity=self.pipe)
        self.tearDown()
        self.setUp()
        with self.assertRaises(AssemblyFailure):
            self.observer.observe_message(b"PUBLISH_RECORD\n", child_identity=object(), parent_pipe_identity=self.pipe)

    def test_copied_pair_without_witness_rejects(self) -> None:
        shutil.copyfile(self.root / "run-record.pending", self.root / "run-record.json")
        shutil.copyfile(self.root / "publication-receipt.pending", self.root / "publication-receipt.json")
        (self.root / "run-record.pending").unlink()
        (self.root / "publication-receipt.pending").unlink()
        self.backend._identities["run-record.json"] = FileIdentity(11, 9, 9)
        self.backend._identities["publication-receipt.json"] = FileIdentity(11, 10, 10)
        with self.assertRaises(AssemblyFailure):
            self.consume(object())

    def test_post_witness_exact_copy_replacement_rejects(self) -> None:
        witness = self.publish()
        record = self.root / "run-record.json"
        raw = record.read_bytes()
        record.unlink()
        record.write_bytes(raw)
        self.backend._identities["run-record.json"] = FileIdentity(11, 99, 99)
        with self.assertRaises(AssemblyFailure):
            self.consume(witness)

    def test_pending_quarantine_wrong_child_and_missing_consumer_reject(self) -> None:
        witness = self.publish()
        (self.root / "run-record.pending").write_bytes(b"residue")
        self.backend._identities["run-record.pending"] = FileIdentity(11, 77, 77)
        with self.assertRaises(AssemblyFailure):
            self.consume(witness)
        (self.root / "run-record.pending").unlink()
        # The first terminal attempt spent the witness before rejecting the
        # residue; repairing the file set cannot authorize a retry.
        with self.assertRaises(AssemblyFailure):
            self.consume(witness)

        self.tearDown()
        self.setUp()
        witness = self.publish()
        with self.assertRaises(AssemblyFailure):
            self.consume(witness, quarantined=True)

        self.tearDown()
        self.setUp()
        witness = self.publish()
        with self.assertRaises(AssemblyFailure):
            self.consume(witness, child_identity=object())

    def test_trace_mutation_and_foreign_observer_reject(self) -> None:
        witness = self.publish()
        self.observer._events[0] = replace(self.observer._events[0], last_error_uint32=1)
        with self.assertRaises(AssemblyFailure):
            self.consume(witness)

    def test_shared_trace_and_capability_mutations_reject(self) -> None:
        witness = self.publish()
        mutated = replace(witness.events[0], flags_numeric=1)
        witness.events = (mutated, witness.events[1])
        self.observer._events[0] = mutated
        with self.assertRaises(AssemblyFailure):
            self.consume(witness)

        self.tearDown()
        self.setUp()
        witness = self.publish()
        witness.capability.terminal = False
        with self.assertRaises(AssemblyFailure):
            self.consume(witness)


if __name__ == "__main__":
    unittest.main()

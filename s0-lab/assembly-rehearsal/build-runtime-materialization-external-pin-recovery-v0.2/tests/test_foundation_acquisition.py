from __future__ import annotations

import ast
from dataclasses import fields, replace
import hashlib
from pathlib import Path
import sys
import tempfile
import unittest
from unittest import mock


TEST_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
IMPLEMENTATION_ROOT = TEST_ROOT / "implementation"
sys.path.insert(0, str(IMPLEMENTATION_ROOT))

from s0_public_external_pin_recovery import acquisition, candidate, canonical, pins
from s0_public_external_pin_recovery import win32_secure
from s0_public_external_pin_recovery.errors import AcquisitionError, AuthorityError


class _MemorySecureFile:
    def __init__(self, destination: Path) -> None:
        self.destination = str(destination)
        self.identity = win32_secure.WindowsFileIdentity(7, "12" * 16)
        self.data = bytearray()
        self.closed = False

    def write_all(self, data: bytes) -> None:
        self.data.extend(data)

    def flush(self) -> None:
        pass

    def snapshot(self, _error_code: str = "unused") -> win32_secure.WindowsFileSnapshot:
        return win32_secure.WindowsFileSnapshot(self.identity, len(self.data))

    def readback_sha256(self, expected_size: int, _block_size: int) -> str:
        if expected_size != len(self.data):
            raise AcquisitionError("fake_size_mismatch")
        return hashlib.sha256(self.data).hexdigest()

    def final_reauthenticate(self, expected_size: int) -> win32_secure.WindowsFileSnapshot:
        if expected_size != len(self.data):
            raise AcquisitionError("fake_revalidation_failure")
        return self.snapshot()

    def close(self) -> None:
        self.closed = True


class FoundationTests(unittest.TestCase):
    def test_exact_seven_source_hashes(self) -> None:
        expected_hashes = {
            "__init__.py": "56b43e5091371afa2ac2b96ac0220744537e5bc1b6bf0274da822a1ee9c18ccb",
            "errors.py": "bdb75b464b3e381d53acd44d477c8f837c170ccbe7844b019969c451ed6168d2",
            "pins.py": "8ec74ae91a452a6c4367977364462ce273d6ff6307a0b8b43f517f54c224576d",
            "canonical.py": "bafea3f6e2b4f19e98edbbea0a70a05750e9f2fa12b57c84f963269e6ed7a461",
            "candidate.py": "23365c09e2369024adce3faa5bba83bcb6ab71cd0d6c7e0f9506e022cf762d43",
            "win32_secure.py": "b9c64a30cdf3e15c1334b4078ee4572cabf696c1ba4dada1e67abb43af013149",
            "acquisition.py": "3b8790b981dbf372e2147866c3fed11affb34dc92a4ccd3b78a8c84cebebc9f6",
        }
        self.assertEqual(7, len(expected_hashes))
        source_root = IMPLEMENTATION_ROOT / "s0_public_external_pin_recovery"
        for filename, expected in expected_hashes.items():
            with self.subTest(filename=filename):
                payload = (source_root / filename).read_bytes()
                self.assertEqual(expected, canonical.sha256_hex(payload))
        with self.assertRaises(TypeError):
            canonical.sha256_hex(bytearray(b"abc"))  # type: ignore[arg-type]

    def test_strict_canonical_json(self) -> None:
        value = {"z": [True, None, 2], "a": "한"}
        expected = '{"a":"한","z":[true,null,2]}'.encode("utf-8")
        self.assertEqual(expected, canonical.canonical_json_bytes(value))
        self.assertEqual(hashlib.sha256(expected).hexdigest(), canonical.canonical_sha256(value))

        class IntSubclass(int):
            pass

        class StrSubclass(str):
            pass

        class ListSubclass(list):
            pass

        rejected = (
            1.0,
            float("nan"),
            b"bytes",
            (1, 2),
            IntSubclass(1),
            StrSubclass("x"),
            ListSubclass(),
        )
        for item in rejected:
            with self.subTest(rejected_type=type(item).__name__):
                with self.assertRaises((TypeError, ValueError)):
                    canonical.canonical_json_bytes(item)

        with self.assertRaises(TypeError):
            canonical.canonical_json_bytes({StrSubclass("key"): 1})
        cycle: list[object] = []
        cycle.append(cycle)
        with self.assertRaises(ValueError):
            canonical.canonical_json_bytes(cycle)
        shared: list[object] = []
        with self.assertRaises(ValueError):
            canonical.canonical_json_bytes([shared, shared])

    def test_closed_pin_ids_exact_rows_and_hostile_inputs(self) -> None:
        expected_rows = {
            "vs-build-tools-17.14.39-17.14.37614.0": (
                "vs_BuildTools.exe",
                "https://download.visualstudio.microsoft.com/download/pr/"
                "fa619120-9c0e-47e6-bfe0-3ee96fb671b2/"
                "236367b68ba9a51708263ab10a1c85546cc4a8eca78b365168811d19c4fb2f29/"
                "vs_BuildTools.exe",
                None,
                None,
                24 * 1024 * 1024 * 1024,
            ),
            "cpython-3.12.10-embed-amd64": (
                "python-3.12.10-embed-amd64.zip",
                "https://www.python.org/ftp/python/3.12.10/"
                "python-3.12.10-embed-amd64.zip",
                "4acbed6dd1c744b0376e3b1cf57ce906f9dc9e95e68824584c8099a63025a3c3",
                None,
                24 * 1024 * 1024 * 1024,
            ),
            "jsonschema-4.26.0-py3-none-any": (
                "jsonschema-4.26.0-py3-none-any.whl",
                None,
                "d489f15263b8d200f8387e64b4c3a75f06629559fb73deb8fdfb525f2dab50ce",
                90630,
                90630,
            ),
        }
        self.assertEqual(set(expected_rows), set(pins.APPROVED_PINS))
        for pin_id, expected in expected_rows.items():
            resolved = pins.resolve_approved_pin(pin_id)
            self.assertIsNot(resolved, pins.APPROVED_PINS[pin_id])
            self.assertEqual(
                (resolved.filename, resolved.url, resolved.expected_sha256,
                 resolved.expected_size, resolved.max_size),
                expected,
            )
            clone_resolution = pins.resolve_approved_pin(replace(resolved))
            self.assertEqual(resolved, clone_resolution)
            self.assertIsNot(resolved, clone_resolution)
        self.assertEqual(
            "ba66b457e169106bc830d68e10d72bcfe0fe3248e83515ee330d94457b34e77c",
            pins.VERIFIER_MANIFEST_SHA256,
        )
        with self.assertRaises(TypeError):
            pins.APPROVED_PINS["new"] = pins.CPYTHON_PIN  # type: ignore[index]

        class PinSubclass(pins.ArtifactPin):
            pass

        subclass = PinSubclass(
            pins.CPYTHON_PIN.pin_id,
            pins.CPYTHON_PIN.filename,
            pins.CPYTHON_PIN.url,
            pins.CPYTHON_PIN.expected_sha256,
            pins.CPYTHON_PIN.expected_size,
            pins.CPYTHON_PIN.max_size,
        )

        class MutablePropertyPin:
            reads = 0

            @property
            def pin_id(self) -> str:
                self.reads += 1
                return pins.CPYTHON_PIN_ID

        mutable = MutablePropertyPin()
        rejected = (
            "unknown-pin",
            subclass,
            object(),
            replace(pins.CPYTHON_PIN, filename="altered.zip"),
            mutable,
        )
        for item in rejected:
            with self.subTest(rejected=type(item).__name__):
                with self.assertRaises(AuthorityError):
                    pins.resolve_approved_pin(item)  # type: ignore[arg-type]
        self.assertEqual(0, mutable.reads)

    def test_exported_pin_views_are_non_authoritative_under_low_level_mutation(self) -> None:
        canonical_ids = (
            pins.VS_BUILD_TOOLS_PIN_ID,
            pins.CPYTHON_PIN_ID,
            pins.JSONSCHEMA_PIN_ID,
        )
        targets = (
            pins.VS_BUILD_TOOLS_PIN,
            pins.CPYTHON_PIN,
            pins.JSONSCHEMA_PIN,
            *(pins.APPROVED_PINS[pin_id] for pin_id in canonical_ids),
        )
        mutations = {
            "pin_id": "attacker-pin",
            "filename": "attacker.bin",
            "url": "https://attacker.invalid/artifact",
            "expected_sha256": "0" * 64,
            "expected_size": 1,
            "max_size": 1,
        }
        for target in targets:
            canonical_id = target.pin_id
            canonical = pins.resolve_approved_pin(canonical_id)
            canonical_row = tuple(getattr(canonical, name) for name in mutations)
            for field_name, malicious in mutations.items():
                original = getattr(target, field_name)
                object.__setattr__(target, field_name, malicious)
                try:
                    with self.subTest(pin_id=canonical_id, field=field_name):
                        with self.assertRaises(AuthorityError):
                            pins.resolve_approved_pin(target)
                        resolved = pins.resolve_approved_pin(canonical_id)
                        self.assertEqual(
                            canonical_row,
                            tuple(getattr(resolved, name) for name in mutations),
                        )
                        self.assertIsNot(resolved, target)
                finally:
                    object.__setattr__(target, field_name, original)

        malicious_view = replace(pins.CPYTHON_PIN, filename="attacker.zip")
        with mock.patch.object(pins, "CPYTHON_PIN", malicious_view), mock.patch.object(
            pins, "APPROVED_PINS", {pins.CPYTHON_PIN_ID: malicious_view}
        ), mock.patch.object(
            pins, "_resolve_approved_pin_snapshot", side_effect=AssertionError("rebound")
        ):
            resolved = pins.resolve_approved_pin(pins.CPYTHON_PIN_ID)
            self.assertEqual("python-3.12.10-embed-amd64.zip", resolved.filename)
            self.assertEqual(pins.CPYTHON_SHA256, resolved.expected_sha256)

    def test_acquisition_uses_captured_primitive_snapshot_before_and_during_stream(self) -> None:
        canonical = pins.resolve_approved_pin(pins.VS_BUILD_TOOLS_PIN_ID)
        expected_url = canonical.url
        expected_filename = canonical.filename
        mutable_clone = replace(canonical)
        retained = _MemorySecureFile(Path(tempfile.gettempdir()) / expected_filename)

        def chunks():
            yield b"before-mutation"
            object.__setattr__(mutable_clone, "url", "https://attacker.invalid/changed")
            object.__setattr__(mutable_clone, "filename", "attacker.exe")
            object.__setattr__(pins.VS_BUILD_TOOLS_PIN, "max_size", 1)
            yield b"after-mutation"

        original_export_max = pins.FALLBACK_MAX_SIZE
        malicious_view = replace(canonical, filename="attacker.exe")
        try:
            with mock.patch.object(acquisition, "secure_create_file", return_value=retained), mock.patch.object(
                pins, "VS_BUILD_TOOLS_PIN", malicious_view
            ), mock.patch.object(pins, "resolve_approved_pin", side_effect=AssertionError("rebound")):
                evidence = acquisition.acquire_pinned_artifact(
                    mutable_clone,
                    chunks=chunks(),
                    observed_uri=expected_url,
                    redirect_count=0,
                    destination=Path(retained.destination),
                    repository_root=REPOSITORY_ROOT,
                )
        finally:
            object.__setattr__(pins.VS_BUILD_TOOLS_PIN, "max_size", original_export_max)
        self.assertEqual(expected_url, evidence.source_uri)
        self.assertEqual(expected_filename, evidence.filename)
        self.assertEqual(pins.FALLBACK_MAX_SIZE, evidence.max_size)
        self.assertEqual(len(b"before-mutationafter-mutation"), evidence.observed_size)
        self.assertFalse(evidence.authenticated)
        self.assertFalse(evidence.process_authority)

    def test_candidate_is_fixed_blocked_with_all_nonclaims(self) -> None:
        expected_ids = (
            "IR-001", "IR-002", "IR-003", "SUPPLIER-ASSURANCE",
            "EFFECTIVE-TRUST-SNAPSHOT", "ACQUISITION-PRODUCER",
            "SEMANTIC-VALIDATOR", "FRESHNESS-PROVENANCE",
            "JSONSCHEMA-TRANSITIVE-CLOSURE", "NATIVE-SOURCE",
            "MATERIALIZER-SOURCE", "OFFLINE-TOOLCHAIN-LAYOUT", "RUNTIME-PROFILE",
            "BRM-EPRI01-IR-001", "BRM-EPRI01-IR-002", "BRM-EPRI01-IR-003",
            "BRM-EPRI01-IR-004",
        )
        decision = candidate.evaluate_candidate(
            {"eligible": True, "waive_all": True}, s0_validated=True, executed=True
        )
        self.assertEqual(candidate.CANDIDATE_ID, decision.candidate_id)
        self.assertEqual(expected_ids, decision.blocker_ids)
        self.assertEqual(candidate.REQUIRED_BLOCKERS, decision.blockers)
        self.assertTrue(decision.blocked)
        false_fields = (
            "eligible", "process_executed", "process_authority_granted",
            "installation_claimed", "install_validated", "build_claimed",
            "build_validated", "runtime_claimed", "runtime_validated",
            "rehearsal_claimed", "rehearsal_validated", "s0_claimed", "s0_validated",
            "e0_claimed", "e0_validated", "self_assertions_considered_evidence",
        )
        self.assertTrue(all(getattr(decision, name) is False for name in false_fields))
        init_fields = {item.name: item.init for item in fields(candidate.CandidateDecision)}
        self.assertTrue(all(init_fields[name] is False for name in false_fields))
        with self.assertRaises(TypeError):
            candidate.CandidateDecision(eligible=True)  # type: ignore[call-arg]


class WindowsAndAcquisitionTests(unittest.TestCase):
    def test_actual_secure_fresh_write_revalidate_reuse_and_inside_rejection(self) -> None:
        payload = b"retained Windows handle\n"
        with tempfile.TemporaryDirectory() as outside:
            destination = Path(outside) / "native.bin"
            secured = win32_secure.secure_create_file(
                repository_root=REPOSITORY_ROOT,
                destination=destination,
                expected_filename="native.bin",
            )
            identity = secured.identity
            secured.write_all(payload)
            secured.flush()
            self.assertEqual(len(payload), secured.snapshot().length)
            self.assertEqual(hashlib.sha256(payload).hexdigest(), secured.readback_sha256(len(payload), 7))
            self.assertEqual(identity, secured.final_reauthenticate(len(payload)).identity)
            secured.close()
            with self.assertRaisesRegex(AcquisitionError, "destination_not_fresh"):
                win32_secure.secure_create_file(
                    repository_root=REPOSITORY_ROOT,
                    destination=destination,
                    expected_filename="native.bin",
                )

        with tempfile.TemporaryDirectory(dir=REPOSITORY_ROOT) as inside:
            with self.assertRaisesRegex(AcquisitionError, "destination_inside_repository"):
                win32_secure.secure_create_file(
                    repository_root=REPOSITORY_ROOT,
                    destination=Path(inside) / "inside.bin",
                    expected_filename="inside.bin",
                )

    def test_deterministic_native_and_revalidation_failures(self) -> None:
        with tempfile.TemporaryDirectory() as outside:
            destination = Path(outside) / "native-fail.bin"
            with mock.patch.object(
                win32_secure,
                "_open_volume_root",
                side_effect=AcquisitionError("forced_native_failure"),
            ):
                with self.assertRaisesRegex(AcquisitionError, "forced_native_failure"):
                    win32_secure.secure_create_file(
                        repository_root=REPOSITORY_ROOT,
                        destination=destination,
                        expected_filename="native-fail.bin",
                    )

        identity = win32_secure.WindowsFileIdentity(1, "34" * 16)
        handle = mock.Mock(value=91)
        chain = win32_secure._DirectoryChain(
            win32_secure._CapturedPath("C:\\", "\\\\?\\C:\\", ()),
            (handle,),
            (identity,),
        )
        with mock.patch.object(
            win32_secure,
            "_query_directory",
            side_effect=AcquisitionError("forced_revalidation_failure"),
        ):
            with self.assertRaisesRegex(AcquisitionError, "forced_revalidation_failure"):
                chain.revalidate("forced_revalidation_failure")

    def test_injected_build_tools_is_unauthenticated_and_never_process_authority(self) -> None:
        payload = b"injected bytes only"
        with tempfile.TemporaryDirectory() as outside:
            destination = Path(outside) / pins.VS_BUILD_TOOLS_ARTIFACT
            retained = _MemorySecureFile(destination)
            with mock.patch.object(
                acquisition,
                "secure_create_file",
                side_effect=[retained, AcquisitionError("destination_not_fresh")],
            ):
                evidence = acquisition.acquire_pinned_artifact(
                    pins.VS_BUILD_TOOLS_PIN_ID,
                    chunks=[payload],
                    observed_uri=pins.VS_BUILD_TOOLS_URL,
                    redirect_count=0,
                    destination=destination,
                    repository_root=REPOSITORY_ROOT,
                )
                with self.assertRaisesRegex(AcquisitionError, "destination_not_fresh"):
                    acquisition.acquire_pinned_artifact(
                        pins.VS_BUILD_TOOLS_PIN_ID,
                        chunks=[payload], observed_uri=pins.VS_BUILD_TOOLS_URL,
                        redirect_count=0, destination=destination,
                        repository_root=REPOSITORY_ROOT,
                    )
            self.assertTrue(retained.closed)
            self.assertEqual(hashlib.sha256(payload).hexdigest(), evidence.observed_sha256)
            self.assertEqual(len(payload), evidence.observed_size)
            self.assertFalse(evidence.authenticated)
            self.assertFalse(evidence.process_authority)
            self.assertFalse(evidence.reuse_authority)
            self.assertEqual("acquired-unauthenticated", evidence.status)
            self.assertEqual(
                ("post_write", "post_flush", "post_readback", "final_binding"),
                tuple(item.label for item in evidence.checkpoints),
            )
            self.assertEqual(1, len({
                (item.volume_serial, item.file_id, item.size, item.sha256)
                for item in evidence.checkpoints
            }))

    def test_uri_redirect_size_and_mutable_pin_rejections(self) -> None:
        class MutablePin:
            pin_id = pins.VS_BUILD_TOOLS_PIN_ID

        with tempfile.TemporaryDirectory() as outside:
            base = Path(outside)
            cases = (
                ({"pin_or_id": pins.VS_BUILD_TOOLS_PIN_ID,
                  "observed_uri": pins.VS_BUILD_TOOLS_URL + "?changed=1", "redirect_count": 0,
                  "destination": base / "uri.exe"}, "source_uri_mismatch"),
                ({"pin_or_id": pins.VS_BUILD_TOOLS_PIN_ID,
                  "observed_uri": pins.VS_BUILD_TOOLS_URL, "redirect_count": 1,
                  "destination": base / "redirect.exe"}, "redirect_not_permitted"),
                ({"pin_or_id": MutablePin(),
                  "observed_uri": pins.VS_BUILD_TOOLS_URL, "redirect_count": 0,
                  "destination": base / "mutable.exe"}, "pin_not_approved"),
            )
            for arguments, code in cases:
                with self.subTest(code=code):
                    with self.assertRaisesRegex(AcquisitionError, code):
                        acquisition.acquire_pinned_artifact(
                            arguments["pin_or_id"], chunks=[b"x"],
                            observed_uri=arguments["observed_uri"],
                            redirect_count=arguments["redirect_count"],
                            destination=arguments["destination"],
                            repository_root=REPOSITORY_ROOT,
                        )
            with self.assertRaisesRegex(AcquisitionError, "chunk_size_bound_exceeded"):
                with mock.patch.object(
                    acquisition,
                    "secure_create_file",
                    return_value=_MemorySecureFile(base / pins.VS_BUILD_TOOLS_ARTIFACT),
                ):
                    acquisition.acquire_pinned_artifact(
                        pins.VS_BUILD_TOOLS_PIN_ID, chunks=[b"xx"],
                        observed_uri=pins.VS_BUILD_TOOLS_URL, redirect_count=0,
                        destination=base / pins.VS_BUILD_TOOLS_ARTIFACT,
                        repository_root=REPOSITORY_ROOT, max_chunk_size=1,
                    )

    def test_static_no_process_shell_dynamic_execution_or_path_fallback(self) -> None:
        disallowed_imports = {"subprocess", "shutil", "requests", "urllib"}
        disallowed_names = {"open", "eval", "exec", "compile", "__import__"}
        disallowed_attributes = {
            "system", "popen", "startfile", "spawnl", "spawnle", "spawnlp",
            "spawnlpe", "spawnv", "spawnve", "spawnvp", "spawnvpe",
        }
        source_names = (
            "__init__.py", "errors.py", "pins.py", "canonical.py",
            "candidate.py", "win32_secure.py", "acquisition.py",
        )
        for source_name in source_names:
            source = (IMPLEMENTATION_ROOT / "s0_public_external_pin_recovery" / source_name).read_text(
                encoding="utf-8"
            )
            tree = ast.parse(source, filename=source_name)
            imported = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imported.update(alias.name.split(".", 1)[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imported.add(node.module.split(".", 1)[0])
                elif isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        self.assertNotIn(node.func.id, disallowed_names, source_name)
                    elif isinstance(node.func, ast.Attribute):
                        self.assertNotIn(node.func.attr, disallowed_attributes, source_name)
                        if node.func.attr == "open":
                            self.fail(f"path-open fallback in {source_name}")
                    self.assertFalse(
                        any(keyword.arg == "shell" for keyword in node.keywords), source_name
                    )
            self.assertTrue(imported.isdisjoint(disallowed_imports), source_name)


if __name__ == "__main__":
    unittest.main(verbosity=2)

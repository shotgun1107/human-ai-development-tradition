from __future__ import annotations

import ast
from dataclasses import dataclass, fields, replace
import hashlib
from pathlib import Path
import stat
import sys
import tempfile
import unittest
from unittest import mock
import zipfile


TEST_ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = Path(__file__).resolve().parents[4]
IMPLEMENTATION_ROOT = TEST_ROOT / "implementation"
PACKAGE_ROOT = IMPLEMENTATION_ROOT / "s0_public_external_pin_recovery"
sys.path.insert(0, str(IMPLEMENTATION_ROOT))

from s0_public_external_pin_recovery import acquisition, materialize, pins, win32_secure
from s0_public_external_pin_recovery.errors import AcquisitionError, MaterializationError


@dataclass(frozen=True)
class _Case:
    archive: Path
    destination: Path
    pin: pins.ArtifactPin
    evidence: acquisition.AcquisitionEvidence
    archive_identity: win32_secure.WindowsFileIdentity
    archive_bytes: bytes


def _make_case(directory: Path) -> _Case:
    archive = directory / "test-cpython.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_STORED) as output:
        output.writestr("python.exe", b"inert-runtime-placeholder")
        output.writestr("Lib/site.py", b"INERT_ONLY = True\n")
    archive_bytes = archive.read_bytes()
    digest = hashlib.sha256(archive_bytes).hexdigest()
    size = len(archive_bytes)
    pin = pins.ArtifactPin(
        pin_id="test-cpython-v02",
        filename=archive.name,
        url="https://example.invalid/test-cpython.zip",
        expected_sha256=digest,
        expected_size=size,
        max_size=size,
    )
    retained = win32_secure.secure_open_existing_file(
        repository_root=REPOSITORY_ROOT, path=archive
    )
    try:
        snapshot = retained.revalidate()
    finally:
        retained.close()
    checkpoints = tuple(
        acquisition.AcquisitionCheckpoint(
            label=label,
            volume_serial=snapshot.identity.volume_serial,
            file_id=snapshot.identity.file_id,
            size=size,
            sha256=digest,
        )
        for label in ("post_write", "post_flush", "post_readback", "final_binding")
    )
    evidence = acquisition.AcquisitionEvidence(
        pin_id=pin.pin_id,
        artifact_name=pin.filename,
        filename=pin.filename,
        source_uri=pin.url,
        redirect_count=0,
        destination=str(archive),
        expected_size=pin.expected_size,
        expected_sha256=pin.expected_sha256,
        max_size=pin.max_size,
        observed_size=size,
        observed_sha256=digest,
        authenticated=True,
        process_authority=False,
        reuse_authority=False,
        status="acquired-authenticated",
        checkpoints=checkpoints,
    )
    return _Case(
        archive=archive,
        destination=directory / "materialized",
        pin=pin,
        evidence=evidence,
        archive_identity=snapshot.identity,
        archive_bytes=archive_bytes,
    )


def _closure_function(function, name: str):
    for cell in function.__closure__ or ():
        value = cell.cell_contents
        if callable(value) and getattr(value, "__name__", None) == name:
            return value
    raise AssertionError(f"missing closure function: {name}")


def _run(
    case: _Case,
    *,
    evidence: acquisition.AcquisitionEvidence | None = None,
    destination: Path | None = None,
) -> materialize.MaterializationEvidence:
    implementation = _closure_function(
        materialize.materialize_authenticated_zip, "_materialize_authenticated_zip_impl"
    )
    trusted = materialize._TrustedPin(
        case.pin.pin_id,
        case.pin.filename,
        case.pin.url,
        case.pin.expected_sha256,
        case.pin.expected_size,
        case.pin.max_size,
    )
    return implementation(
        case.pin,
        case.evidence if evidence is None else evidence,
        case.destination if destination is None else destination,
        repository_root=REPOSITORY_ROOT,
        resolve_cpython_pin=lambda _pin: trusted,
    )


class MaterializationSecurityTests(unittest.TestCase):
    def test_positive_windows_lifecycle_and_evidence_binding(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            case = _make_case(Path(temporary))
            evidence = _run(case)
            expected_paths = ("Lib/site.py", "python.exe")
            self.assertEqual(case.pin.pin_id, evidence.pin_id)
            self.assertEqual(case.evidence.evidence_sha256(), evidence.acquisition_evidence_sha256)
            self.assertEqual(case.archive_identity, evidence.archive_initial_identity)
            self.assertEqual(case.archive_identity, evidence.archive_final_identity)
            self.assertEqual(case.pin.expected_sha256, evidence.archive_sha256)
            self.assertEqual(evidence.archive_pre_sha256, evidence.archive_post_sha256)
            self.assertEqual(evidence.root_initial_identity, evidence.root_final_identity)
            self.assertEqual(expected_paths, tuple(item.relative_path for item in evidence.files))
            self.assertEqual(2, evidence.file_count)
            self.assertEqual(1, evidence.directory_count)
            self.assertEqual(sum(item.size for item in evidence.files), evidence.total_size)
            self.assertTrue(evidence.final_reauthentication_passed)
            self.assertFalse(evidence.process_authority_granted)
            self.assertFalse(evidence.installed)
            self.assertFalse(evidence.executed)
            self.assertFalse(evidence.imported)
            self.assertEqual(b"inert-runtime-placeholder", (case.destination / "python.exe").read_bytes())
            self.assertEqual(b"INERT_ONLY = True\n", (case.destination / "Lib/site.py").read_bytes())

    def test_hostile_zip_paths_and_inventory_are_rejected(self) -> None:
        class InventoryArchive:
            def __init__(self, infos: list[zipfile.ZipInfo]) -> None:
                self._infos = infos

            def infolist(self) -> list[zipfile.ZipInfo]:
                return self._infos

        def info(name: str) -> zipfile.ZipInfo:
            item = zipfile.ZipInfo(name)
            item.file_size = 1
            return item

        symlink = info("link")
        symlink.create_system = 3
        symlink.external_attr = (stat.S_IFLNK | 0o777) << 16
        reparse = info("reparse")
        reparse.external_attr = 0x400
        encrypted = info("encrypted")
        encrypted.flag_bits = 0x1
        unsupported = info("unsupported")
        unsupported.compress_type = 99
        cases = {
            "traversal": [info("../escape")],
            "absolute": [info("/escape")],
            "drive": [info("C:/escape")],
            "backslash": [info("a\\b")],
            "reserved": [info("CON")],
            "duplicate": [info("same"), info("same")],
            "case_collision": [info("Name"), info("name")],
            "file_ancestor": [info("a"), info("a/b")],
            "symlink": [symlink],
            "reparse": [reparse],
            "encrypted": [encrypted],
            "unsupported": [unsupported],
        }
        destination = Path(r"C:\materialization-preview-v02")
        for label, infos in cases.items():
            with self.subTest(label=label):
                with self.assertRaises(MaterializationError):
                    materialize._preflight_inventory(
                        InventoryArchive(infos), destination, materialize.DEFAULT_LIMITS
                    )

    def test_closed_pin_and_evidence_authority(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            case = _make_case(Path(temporary))
            with self.assertRaises(MaterializationError):
                materialize.materialize_authenticated_zip(
                    pins.JSONSCHEMA_PIN_ID,
                    case.evidence,
                    case.destination,
                    repository_root=REPOSITORY_ROOT,
                )
            with self.assertRaises(MaterializationError):
                materialize.materialize_authenticated_zip(
                    replace(pins.CPYTHON_PIN, filename="altered.zip"),
                    case.evidence,
                    case.destination,
                    repository_root=REPOSITORY_ROOT,
                )

            class EvidenceSubclass(acquisition.AcquisitionEvidence):
                pass

            subclass = EvidenceSubclass(
                **{item.name: getattr(case.evidence, item.name) for item in fields(case.evidence)}
            )
            altered = (
                subclass,
                replace(case.evidence, authenticated=False),
                replace(case.evidence, process_authority=True),
                replace(case.evidence, reuse_authority=True),
                replace(case.evidence, status="caller-claimed"),
                replace(case.evidence, checkpoints=list(case.evidence.checkpoints)),
            )
            for evidence in altered:
                with self.subTest(evidence_type=type(evidence).__name__):
                    with self.assertRaises(MaterializationError):
                        _run(case, evidence=evidence)  # type: ignore[arg-type]
            self.assertFalse(case.destination.exists())

    def test_identity_binding_rejects_inconsistent_and_wrong_file_ids(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            case = _make_case(base)
            changed = replace(case.evidence.checkpoints[1], file_id="ab" * 16)
            inconsistent = replace(
                case.evidence,
                checkpoints=(case.evidence.checkpoints[0], changed, *case.evidence.checkpoints[2:]),
            )
            wrong_checkpoints = tuple(
                replace(item, file_id="cd" * 16) for item in case.evidence.checkpoints
            )
            stable_but_wrong = replace(case.evidence, checkpoints=wrong_checkpoints)
            for label, evidence in (
                ("inconsistent", inconsistent),
                ("stable_wrong", stable_but_wrong),
            ):
                with self.subTest(label=label):
                    with self.assertRaises(MaterializationError):
                        _run(case, evidence=evidence, destination=base / f"output-{label}")

    def test_public_materializer_uses_closure_snapshot_before_and_after_export_mutation(self) -> None:
        canonical = pins.resolve_approved_pin(pins.CPYTHON_PIN_ID)
        canonical_tuple = (
            canonical.pin_id,
            canonical.filename,
            canonical.url,
            canonical.expected_sha256,
            canonical.expected_size,
            canonical.max_size,
        )
        export = pins.CPYTHON_PIN
        mapping_view = pins.APPROVED_PINS[pins.CPYTHON_PIN_ID]
        originals = {
            (id(target), field_name): getattr(target, field_name)
            for target in (export, mapping_view)
            for field_name in ("pin_id", "filename", "url", "expected_sha256", "expected_size", "max_size")
        }
        malicious = {
            "pin_id": "attacker-pin",
            "filename": "attacker.zip",
            "url": "https://attacker.invalid/archive",
            "expected_sha256": "0" * 64,
            "expected_size": 1,
            "max_size": 1,
        }
        captured: list[tuple[object, ...]] = []

        def stop_after_capture(trusted, _evidence):
            captured.append(tuple(trusted))
            for target in (export, mapping_view):
                for field_name, value in malicious.items():
                    object.__setattr__(target, field_name, value)
            self.assertEqual(canonical_tuple, tuple(trusted))
            raise MaterializationError("stop_after_authority_capture")

        try:
            for target in (export, mapping_view):
                for field_name, value in malicious.items():
                    object.__setattr__(target, field_name, value)
            clone = pins.ArtifactPin(*canonical_tuple)
            rebound = replace(canonical, filename="rebound.zip")
            with mock.patch.object(
                materialize, "_validate_acquisition_evidence", new=stop_after_capture
            ), mock.patch.object(pins, "CPYTHON_PIN", rebound), mock.patch.object(
                pins, "APPROVED_PINS", {pins.CPYTHON_PIN_ID: rebound}
            ), mock.patch.object(
                pins, "_resolve_approved_pin_snapshot", side_effect=AssertionError("rebound")
            ):
                for authority_input in (pins.CPYTHON_PIN_ID, clone):
                    with self.assertRaisesRegex(MaterializationError, "stop_after_authority_capture"):
                        materialize.materialize_authenticated_zip(
                            authority_input,
                            object(),  # type: ignore[arg-type]
                            Path(r"C:\never-created-v02"),
                            repository_root=REPOSITORY_ROOT,
                        )
        finally:
            for target in (export, mapping_view):
                for field_name in malicious:
                    object.__setattr__(target, field_name, originals[(id(target), field_name)])
        self.assertEqual([canonical_tuple, canonical_tuple], captured)

        class PinSubclass(pins.ArtifactPin):
            pass

        subclass = PinSubclass(*canonical_tuple)
        proxy = type("PinProxy", (), {"pin_id": pins.CPYTHON_PIN_ID})()
        mutated = pins.ArtifactPin(*canonical_tuple)
        object.__setattr__(mutated, "url", "https://attacker.invalid/archive")
        for authority_input in (subclass, proxy, mutated):
            with self.assertRaises(MaterializationError):
                materialize.materialize_authenticated_zip(
                    authority_input,  # type: ignore[arg-type]
                    object(),  # type: ignore[arg-type]
                    Path(r"C:\never-created-v02"),
                    repository_root=REPOSITORY_ROOT,
                )

    def test_archive_identity_toctou_and_final_hash_reauthentication_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            case = _make_case(base)
            original_revalidate = win32_secure.SecureExistingFile.revalidate
            calls = 0

            def changed_identity(retained: win32_secure.SecureExistingFile):
                nonlocal calls
                snapshot = original_revalidate(retained)
                if Path(retained.path) == case.archive:
                    calls += 1
                    if calls == 2:
                        identity = win32_secure.WindowsFileIdentity(
                            snapshot.identity.volume_serial, "ef" * 16
                        )
                        return win32_secure.WindowsFileSnapshot(identity, snapshot.length)
                return snapshot

            with mock.patch.object(
                win32_secure.SecureExistingFile, "revalidate", new=changed_identity
            ), self.assertRaisesRegex(MaterializationError, "archive identity or size changed"):
                _run(case)

        with tempfile.TemporaryDirectory() as temporary:
            case = _make_case(Path(temporary))
            original_readback = win32_secure.SecureExistingFile.readback_sha256
            reads = 0

            def changed_archive_hash(
                retained: win32_secure.SecureExistingFile, expected_size: int, block_size: int
            ) -> str:
                nonlocal reads
                digest = original_readback(retained, expected_size, block_size)
                if Path(retained.path) == case.archive:
                    reads += 1
                    if reads == 2:
                        return "0" * 64
                return digest

            with mock.patch.object(
                win32_secure.SecureExistingFile, "readback_sha256", new=changed_archive_hash
            ), self.assertRaisesRegex(MaterializationError, "post-extraction reauthentication"):
                _run(case)

    def test_output_final_reauthentication_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            case = _make_case(Path(temporary))
            original_readback = win32_secure.SecureExistingFile.readback_sha256

            def changed_output_hash(
                retained: win32_secure.SecureExistingFile, expected_size: int, block_size: int
            ) -> str:
                digest = original_readback(retained, expected_size, block_size)
                return "0" * 64 if Path(retained.path) != case.archive else digest

            with mock.patch.object(
                win32_secure.SecureExistingFile, "readback_sha256", new=changed_output_hash
            ), self.assertRaisesRegex(MaterializationError, "final retained-handle verification"):
                _run(case)

    def test_source_hash_and_static_no_execution_or_path_fallback(self) -> None:
        source_path = PACKAGE_ROOT / "materialize.py"
        source_bytes = source_path.read_bytes()
        self.assertEqual(
            "b5cd48c1a0a714f164c71ff30df430a27b0eb2e4452795e30c8dbad1cb37f5a5",
            hashlib.sha256(source_bytes).hexdigest(),
        )
        tree = ast.parse(source_bytes, filename="materialize.py")
        forbidden_imports = {"subprocess", "runpy", "importlib", "shutil"}
        forbidden_names = {"open", "eval", "exec", "compile", "__import__"}
        forbidden_attributes = {
            "system", "popen", "startfile", "extract", "extractall", "read_bytes",
            "write_bytes", "unlink", "remove", "rename", "replace",
        }
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported.update(alias.name.split(".", 1)[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imported.add(node.module.split(".", 1)[0])
            elif isinstance(node, ast.Call):
                if isinstance(node.func, ast.Name):
                    self.assertNotIn(node.func.id, forbidden_names)
                elif isinstance(node.func, ast.Attribute):
                    self.assertNotIn(node.func.attr, forbidden_attributes)
                self.assertFalse(any(keyword.arg == "shell" for keyword in node.keywords))
        self.assertTrue(imported.isdisjoint(forbidden_imports))


if __name__ == "__main__":
    unittest.main(verbosity=2)

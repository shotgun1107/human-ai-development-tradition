from __future__ import annotations

import hashlib
import os
from pathlib import Path
import stat
import sys
import tempfile
import unittest
from unittest import mock
import warnings
import zipfile


IMPLEMENTATION_ROOT = Path(__file__).resolve().parents[1] / "implementation"
sys.path.insert(0, str(IMPLEMENTATION_ROOT))

from s0_public_external_pin_recovery import canonical  # noqa: E402
from s0_public_external_pin_recovery import pins  # noqa: E402
from s0_public_external_pin_recovery import acquisition  # noqa: E402
from s0_public_external_pin_recovery import candidate  # noqa: E402
from s0_public_external_pin_recovery import materialize  # noqa: E402
from s0_public_external_pin_recovery.errors import (  # noqa: E402
    AcquisitionError,
    MaterializationError,
)


class StringSubclass(str):
    pass


class IntSubclass(int):
    pass


class ListSubclass(list):
    pass


class DictSubclass(dict):
    pass


class CanonicalTests(unittest.TestCase):
    def test_valid_tree_is_exact_deterministic_utf8(self) -> None:
        first = {"z": [None, True, -4], "a": {"é": "snowman ☃"}}
        second = {"a": {"é": "snowman ☃"}, "z": [None, True, -4]}
        expected = '{"a":{"é":"snowman ☃"},"z":[null,true,-4]}'.encode()

        self.assertEqual(canonical.canonical_json_bytes(first), expected)
        self.assertEqual(canonical.canonical_json_bytes(second), expected)
        self.assertEqual(
            canonical.canonical_sha256(first), hashlib.sha256(expected).hexdigest()
        )
        self.assertEqual(canonical.sha256_hex(expected), hashlib.sha256(expected).hexdigest())

    def test_float_nonstring_key_and_supported_subclasses_are_rejected(self) -> None:
        invalid = (
            0.0,
            {1: "value"},
            StringSubclass("text"),
            IntSubclass(3),
            ListSubclass(),
            DictSubclass(),
        )
        for value in invalid:
            with self.subTest(value=type(value).__name__):
                with self.assertRaises((TypeError, ValueError)):
                    canonical.canonical_json_bytes(value)

    def test_alias_cycle_and_nonexact_digest_input_are_rejected(self) -> None:
        shared: list[object] = []
        cyclic: list[object] = []
        cyclic.append(cyclic)
        for value in ([shared, shared], cyclic):
            with self.subTest(kind="alias-or-cycle"):
                with self.assertRaises(ValueError):
                    canonical.validate_json_value(value)
        with self.assertRaises(TypeError):
            canonical.sha256_hex(bytearray(b"not exact bytes"))  # type: ignore[arg-type]


class PinTests(unittest.TestCase):
    def test_frozen_external_pins_are_exact(self) -> None:
        expected_vs_url = (
            "https://download.visualstudio.microsoft.com/download/pr/"
            "fa619120-9c0e-47e6-bfe0-3ee96fb671b2/"
            "236367b68ba9a51708263ab10a1c85546cc4a8eca78b365168811d19c4fb2f29/"
            "vs_BuildTools.exe"
        )
        expected_python_url = (
            "https://www.python.org/ftp/python/3.12.10/"
            "python-3.12.10-embed-amd64.zip"
        )
        self.assertEqual(pins.VS_BUILD_TOOLS_RELEASE, "17.14.39")
        self.assertEqual(pins.VS_BUILD_TOOLS_BUILD, "17.14.37614.0")
        self.assertEqual(pins.VS_BUILD_TOOLS_URL, expected_vs_url)
        self.assertEqual(pins.VS_BUILD_TOOLS_SHA256, None)
        self.assertEqual(pins.VS_BUILD_TOOLS_SIZE, None)
        self.assertFalse(pins.VS_BUILD_TOOLS_AUTHENTICATED)
        self.assertEqual(
            pins.VS_BUILD_TOOLS_COMPONENTS,
            (
                "Microsoft.VisualStudio.Component.VC.Tools.x86.x64",
                "Microsoft.VisualStudio.Component.Windows11SDK.26100",
            ),
        )
        self.assertEqual(pins.CPYTHON_URL, expected_python_url)
        self.assertEqual(
            pins.CPYTHON_SHA256,
            "4acbed6dd1c744b0376e3b1cf57ce906f9dc9e95e68824584c8099a63025a3c3",
        )
        self.assertIsNone(pins.CPYTHON_SIZE)
        self.assertTrue(pins.CPYTHON_AUTHENTICATED)
        self.assertIsNone(pins.JSONSCHEMA_URL)
        self.assertEqual(pins.JSONSCHEMA_SIZE, 90630)
        self.assertEqual(
            pins.JSONSCHEMA_SHA256,
            "d489f15263b8d200f8387e64b4c3a75f06629559fb73deb8fdfb525f2dab50ce",
        )
        self.assertEqual(
            pins.VERIFIER_MANIFEST_SHA256,
            "ba66b457e169106bc830d68e10d72bcfe0fe3248e83515ee330d94457b34e77c",
        )
        self.assertEqual(
            pins.CPYTHON_PIN,
            pins.ArtifactPin(
                filename=pins.CPYTHON_ARTIFACT,
                url=expected_python_url,
                sha256=pins.CPYTHON_SHA256,
                size=None,
                authenticated=True,
            ),
        )


class CandidateTests(unittest.TestCase):
    def test_blockers_and_all_claim_bits_remain_fail_closed(self) -> None:
        expected_ids = (
            "IR-001",
            "IR-002",
            "IR-003",
            "SUPPLIER-ASSURANCE",
            "EFFECTIVE-TRUST-SNAPSHOT",
            "ACQUISITION-PRODUCER",
            "SEMANTIC-VALIDATOR",
            "FRESHNESS-PROVENANCE",
            "JSONSCHEMA-TRANSITIVE-CLOSURE",
            "NATIVE-SOURCE",
            "MATERIALIZER-SOURCE",
            "OFFLINE-TOOLCHAIN-LAYOUT",
            "RUNTIME-PROFILE",
        )
        assertions = {
            "blockers": (),
            "eligible": True,
            "process_authority_granted": True,
            "install_validated": True,
            "build_validated": True,
            "runtime_validated": True,
            "rehearsal_validated": True,
            "s0_validated": True,
            "e0_validated": True,
            "installation_claimed": True,
            "build_claimed": True,
            "runtime_claimed": True,
            "rehearsal_claimed": True,
            "s0_claimed": True,
            "e0_claimed": True,
            "self_assertions_considered_evidence": True,
        }
        decisions = (
            candidate.evaluate_candidate(assertions),
            candidate.evaluate_candidate(**assertions),
        )
        for decision in decisions:
            with self.subTest(form=decision):
                self.assertTrue(decision.blocked)
                self.assertFalse(decision.eligible)
                self.assertEqual(decision.blocker_ids, expected_ids)
                for name in assertions:
                    if name != "blockers":
                        self.assertIs(getattr(decision, name), False)

    def test_constructor_and_dataclass_replace_cannot_clear_fixed_state(self) -> None:
        with self.assertRaises(TypeError):
            candidate.CandidateDecision(eligible=True)  # type: ignore[call-arg]
        with self.assertRaises((TypeError, ValueError)):
            __import__("dataclasses").replace(
                candidate.CandidateDecision(), blockers=()
            )


class AcquisitionTests(unittest.TestCase):
    PAYLOAD = b"test-local inert CPython archive bytes"
    URL = "https://www.python.org/ftp/python/3.12.10/python-test-local.zip"
    FILENAME = "python-test-local.zip"

    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="external-pin-acquire-")
        self.root = Path(self.temporary.name)
        self.repository = self.root / "repository"
        self.destination_parent = self.root / "acquired"
        self.repository.mkdir()
        self.destination_parent.mkdir()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def pin(
        self,
        *,
        payload: bytes | None = None,
        size: int | None = None,
        digest: str | None = None,
        url: str | None = None,
    ) -> pins.ArtifactPin:
        data = self.PAYLOAD if payload is None else payload
        return pins.ArtifactPin(
            filename=self.FILENAME,
            url=self.URL if url is None else url,
            sha256=hashlib.sha256(data).hexdigest() if digest is None else digest,
            size=len(data) if size is None else size,
            authenticated=True,
        )

    def acquire(
        self,
        pin: pins.ArtifactPin,
        *,
        chunks: object | None = None,
        observed_uri: str | None = None,
        redirect_count: int = 0,
        destination: Path | None = None,
    ) -> acquisition.AcquisitionEvidence:
        return acquisition.acquire_pinned_artifact(
            pin,
            chunks=[self.PAYLOAD] if chunks is None else chunks,  # type: ignore[arg-type]
            observed_uri=pin.url if observed_uri is None else observed_uri,  # type: ignore[arg-type]
            redirect_count=redirect_count,
            destination=destination or self.destination_parent / pin.filename,
            repository_root=self.repository,
        )

    def assert_acquisition_error(self, code: str, function: object) -> None:
        with self.assertRaises(AcquisitionError) as raised:
            function()  # type: ignore[operator]
        self.assertEqual(str(raised.exception), code)

    def test_injected_cpython_bytes_succeed_without_process_or_reuse_authority(self) -> None:
        pin = self.pin()
        evidence = self.acquire(pin, chunks=[self.PAYLOAD[:7], self.PAYLOAD[7:]])

        self.assertEqual((self.destination_parent / self.FILENAME).read_bytes(), self.PAYLOAD)
        self.assertEqual(evidence.observed_size, len(self.PAYLOAD))
        self.assertEqual(evidence.observed_sha256, pin.sha256)
        self.assertTrue(evidence.authenticated)
        self.assertFalse(evidence.process_authority)
        self.assertFalse(evidence.reuse_authority)
        self.assertEqual(
            tuple(checkpoint.label for checkpoint in evidence.checkpoints),
            ("post_write", "post_sync", "post_hash", "path_binding"),
        )
        self.assertEqual(evidence.canonical_bytes(), evidence.canonical_bytes())
        self.assertEqual(
            evidence.evidence_sha256(),
            hashlib.sha256(evidence.canonical_bytes()).hexdigest(),
        )

    def test_hostile_or_changed_observed_uri_and_redirects_are_rejected(self) -> None:
        pin = self.pin()
        hostile = (
            "http://www.python.org/python-test-local.zip",
            self.URL + "#fragment",
            "https://attacker.invalid/python-test-local.zip",
            "file:///python-test-local.zip",
        )
        for observed in hostile:
            with self.subTest(observed=observed):
                self.assert_acquisition_error(
                    "source_uri_mismatch",
                    lambda observed=observed: self.acquire(pin, observed_uri=observed),
                )
        for redirect in (1, -1, True):
            with self.subTest(redirect=redirect):
                self.assert_acquisition_error(
                    "redirect_not_permitted",
                    lambda redirect=redirect: self.acquire(pin, redirect_count=redirect),
                )

    def test_inside_repository_existing_destination_and_reuse_are_rejected(self) -> None:
        pin = self.pin()
        inside = self.repository / pin.filename
        self.assert_acquisition_error(
            "destination_inside_repository",
            lambda: self.acquire(pin, destination=inside),
        )

        existing = self.destination_parent / pin.filename
        existing.write_bytes(b"preexisting")
        self.assert_acquisition_error(
            "destination_not_fresh",
            lambda: self.acquire(pin, destination=existing),
        )

    def test_hash_and_size_mismatch_fail_closed_and_leave_nonreusable_file(self) -> None:
        wrong_digest = "0" * 64
        self.assert_acquisition_error(
            "expected_sha256_mismatch",
            lambda: self.acquire(self.pin(digest=wrong_digest)),
        )
        self.assertEqual((self.destination_parent / self.FILENAME).read_bytes(), self.PAYLOAD)
        self.assert_acquisition_error(
            "destination_not_fresh",
            lambda: self.acquire(self.pin(digest=wrong_digest)),
        )

        other_destination = self.destination_parent / "other" / self.FILENAME
        other_destination.parent.mkdir()
        self.assert_acquisition_error(
            "expected_size_mismatch",
            lambda: self.acquire(
                self.pin(size=len(self.PAYLOAD) + 1), destination=other_destination
            ),
        )

    def test_partial_stream_failure_is_preserved_and_cannot_be_reused(self) -> None:
        def partial_stream() -> object:
            yield self.PAYLOAD[:8]
            raise RuntimeError("injected transport failure")

        destination = self.destination_parent / self.FILENAME
        self.assert_acquisition_error(
            "chunk_stream_failed",
            lambda: self.acquire(self.pin(), chunks=partial_stream()),
        )
        self.assertEqual(destination.read_bytes(), self.PAYLOAD[:8])
        self.assert_acquisition_error(
            "destination_not_fresh", lambda: self.acquire(self.pin())
        )

    def test_symlink_destination_and_symlink_parent_are_rejected(self) -> None:
        pin = self.pin()
        linked_destination = self.destination_parent / pin.filename
        fake_link = os.stat_result((stat.S_IFLNK | 0o777, 1, 1, 1, 0, 0, 0, 0, 0, 0))
        original_lstat = acquisition.os.lstat

        def destination_lstat(path: object) -> os.stat_result:
            if Path(path) == linked_destination:
                return fake_link
            return original_lstat(path)

        with mock.patch.object(acquisition.os, "lstat", side_effect=destination_lstat):
            self.assert_acquisition_error(
                "destination_not_fresh",
                lambda: self.acquire(pin, destination=linked_destination),
            )

        original_safe_lstat = acquisition._safe_lstat

        def parent_lstat(path: Path, error_code: str) -> os.stat_result:
            if Path(path) == self.destination_parent:
                return fake_link
            return original_safe_lstat(path, error_code)

        with mock.patch.object(acquisition, "_safe_lstat", side_effect=parent_lstat):
            self.assert_acquisition_error(
                "destination_parent_unsafe", lambda: self.acquire(pin)
            )

    @staticmethod
    def changed_identity(item: os.stat_result) -> os.stat_result:
        values = list(item)
        values[1] += 1
        return os.stat_result(values)

    def test_open_handle_identity_change_is_rejected(self) -> None:
        original = acquisition._checked_fstat

        def checked(descriptor: int, error_code: str) -> os.stat_result:
            item = original(descriptor, error_code)
            if error_code == "post_write_file_invalid":
                return self.changed_identity(item)
            return item

        with mock.patch.object(acquisition, "_checked_fstat", side_effect=checked):
            self.assert_acquisition_error(
                "destination_identity_changed", lambda: self.acquire(self.pin())
            )

    def test_final_path_binding_identity_change_is_rejected(self) -> None:
        original = acquisition._safe_lstat
        binding_calls = 0

        def lstat(path: Path, error_code: str) -> os.stat_result:
            nonlocal binding_calls
            item = original(path, error_code)
            if error_code == "destination_binding_unavailable":
                binding_calls += 1
                if binding_calls == 2:
                    return self.changed_identity(item)
            return item

        with mock.patch.object(acquisition, "_safe_lstat", side_effect=lstat):
            self.assert_acquisition_error(
                "destination_identity_changed", lambda: self.acquire(self.pin())
            )


class MaterializationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="external-pin-stage-")
        self.root = Path(self.temporary.name)
        self.repository = self.root / "repository"
        self.archives = self.root / "archives"
        self.staging = self.root / "staging"
        self.repository.mkdir()
        self.archives.mkdir()
        self.staging.mkdir()
        self.sequence = 0

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def archive(
        self,
        entries: list[tuple[str | zipfile.ZipInfo, bytes]],
    ) -> tuple[Path, str]:
        self.sequence += 1
        path = self.archives / f"archive-{self.sequence}.zip"
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", UserWarning)
            with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as output:
                for name, payload in entries:
                    output.writestr(name, payload)
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        return path, digest

    def destination(self) -> Path:
        self.sequence += 1
        return self.staging / f"destination-{self.sequence}"

    def rejected(
        self,
        entries: list[tuple[str | zipfile.ZipInfo, bytes]],
        *,
        limits: materialize.MaterializationLimits = materialize.DEFAULT_LIMITS,
    ) -> None:
        archive, digest = self.archive(entries)
        destination = self.destination()
        with self.assertRaises(MaterializationError):
            materialize.materialize_authenticated_zip(
                archive,
                digest,
                destination,
                repository_root=self.repository,
                limits=limits,
            )
        self.assertFalse(os.path.lexists(destination))

    def test_successful_inert_staging_is_deterministic_and_grants_no_authority(self) -> None:
        archive, digest = self.archive(
            [("pkg/z.txt", b"z"), ("pkg/a.bin", b"alpha")]
        )
        destination = self.destination()
        evidence = materialize.materialize_authenticated_zip(
            archive, digest, destination, repository_root=self.repository
        )

        self.assertEqual((destination / "pkg" / "z.txt").read_bytes(), b"z")
        self.assertEqual((destination / "pkg" / "a.bin").read_bytes(), b"alpha")
        self.assertEqual(
            tuple(item.relative_path for item in evidence.files),
            ("pkg/a.bin", "pkg/z.txt"),
        )
        self.assertEqual((evidence.file_count, evidence.directory_count), (2, 1))
        self.assertEqual(evidence.total_size, 6)
        self.assertFalse(evidence.process_authority_granted)
        self.assertFalse(evidence.installed)
        self.assertFalse(evidence.executed)
        self.assertFalse(evidence.imported)

    def test_wheel_and_build_tool_wrappers_remain_inert(self) -> None:
        for wrapper, state_flags in (
            (
                materialize.materialize_wheel_archive,
                ("inert_only", "installed", "executed", "process_authority_granted"),
            ),
            (
                materialize.materialize_build_tools_archive,
                (
                    "inert_only",
                    "installed",
                    "built",
                    "executed",
                    "process_authority_granted",
                ),
            ),
        ):
            with self.subTest(wrapper=wrapper.__name__):
                archive, digest = self.archive([("payload.bin", b"inert bytes")])
                state = wrapper(
                    archive,
                    digest,
                    self.destination(),
                    repository_root=self.repository,
                )
                self.assertTrue(state.inert_only)
                for flag in state_flags[1:]:
                    self.assertFalse(getattr(state, flag))

    def test_absolute_drive_unc_backslash_traversal_dot_and_empty_paths_rejected(self) -> None:
        unsafe = (
            "/absolute.txt",
            "C:/drive.txt",
            "//server/share.txt",
            "../escape.txt",
            "dir/../escape.txt",
            "dir/./dot.txt",
            "dir//empty.txt",
        )
        for name in unsafe:
            with self.subTest(name=name):
                self.rejected([(name, b"x")])

    def test_raw_zip_backslash_path_is_rejected(self) -> None:
        archive, _ = self.archive([("dir/backslash.txt", b"x")])
        original = archive.read_bytes()
        hostile = original.replace(b"dir/backslash.txt", b"dir\\backslash.txt")
        self.assertNotEqual(hostile, original)
        archive.write_bytes(hostile)
        digest = hashlib.sha256(hostile).hexdigest()
        destination = self.destination()
        with self.assertRaises(MaterializationError):
            materialize.materialize_authenticated_zip(
                archive,
                digest,
                destination,
                repository_root=self.repository,
            )
        self.assertFalse(destination.exists())

    def test_duplicate_casefold_and_file_directory_collisions_rejected(self) -> None:
        cases = (
            [("same.txt", b"a"), ("same.txt", b"b")],
            [("Alpha.txt", b"a"), ("alpha.txt", b"b")],
            [("A/one.txt", b"a"), ("a/two.txt", b"b")],
            [("node", b"file"), ("node/child", b"child")],
            [("node/", b""), ("node", b"file")],
        )
        for entries in cases:
            with self.subTest(entries=[str(item[0]) for item in entries]):
                self.rejected(list(entries))

    def test_zip_symlink_and_nonregular_members_are_rejected(self) -> None:
        symlink = zipfile.ZipInfo("link")
        symlink.create_system = 3
        symlink.external_attr = (stat.S_IFLNK | 0o777) << 16
        fifo = zipfile.ZipInfo("named-pipe")
        fifo.create_system = 3
        fifo.external_attr = (stat.S_IFIFO | 0o600) << 16
        for info in (symlink, fifo):
            with self.subTest(mode=info.external_attr >> 16):
                self.rejected([(info, b"target")])

    def test_windows_device_reserved_trailing_and_ads_names_are_rejected(self) -> None:
        unsafe = (
            "CON",
            "nul.txt",
            "COM1.bin",
            "LPT9",
            "CLOCK$",
            "trailing.",
            "trailing ",
            "file.txt:stream",
        )
        for name in unsafe:
            with self.subTest(name=name):
                self.rejected([(name, b"x")])

    def test_entry_file_per_file_and_aggregate_limits_are_enforced(self) -> None:
        cases = (
            (
                [("one", b"1"), ("two", b"2")],
                materialize.MaterializationLimits(max_entries=1),
            ),
            (
                [("one", b"1"), ("two", b"2")],
                materialize.MaterializationLimits(max_files=1),
            ),
            (
                [("large", b"123")],
                materialize.MaterializationLimits(max_file_size=2),
            ),
            (
                [("one", b"12"), ("two", b"34")],
                materialize.MaterializationLimits(max_total_size=3),
            ),
        )
        for entries, limits in cases:
            with self.subTest(limits=limits):
                self.rejected(list(entries), limits=limits)

    def test_hash_existing_destination_and_repository_escape_are_rejected(self) -> None:
        archive, digest = self.archive([("safe.txt", b"safe")])
        destination = self.destination()
        with self.assertRaises(MaterializationError):
            materialize.materialize_authenticated_zip(
                archive,
                "0" * 64,
                destination,
                repository_root=self.repository,
            )
        self.assertFalse(destination.exists())

        destination.mkdir()
        with self.assertRaises(MaterializationError):
            materialize.materialize_authenticated_zip(
                archive, digest, destination, repository_root=self.repository
            )

        inside_repository = self.repository / "escaped-staging"
        with self.assertRaises(MaterializationError):
            materialize.materialize_authenticated_zip(
                archive,
                digest,
                inside_repository,
                repository_root=self.repository,
            )
        self.assertFalse(inside_repository.exists())

    def test_symlink_archive_destination_and_parent_escape_are_rejected(self) -> None:
        archive, digest = self.archive([("safe.txt", b"safe")])
        destination_link = self.destination()
        destination_link.mkdir()
        parent_target = self.destination()

        cases = (
            (archive, self.destination(), archive),
            (archive, destination_link, destination_link),
            (archive, parent_target, parent_target.parent),
        )
        original = materialize._is_reparse_or_symlink
        for source, target, unsafe_path in cases:
            with self.subTest(source=source.name, target=target.name):
                def simulated(path: Path, unsafe_path: Path = unsafe_path) -> bool:
                    if Path(path) == unsafe_path:
                        return True
                    return original(path)

                with mock.patch.object(
                    materialize,
                    "_is_reparse_or_symlink",
                    side_effect=simulated,
                ):
                    with self.assertRaises(MaterializationError):
                        materialize.materialize_authenticated_zip(
                            source,
                            digest,
                            target,
                            repository_root=self.repository,
                        )


if __name__ == "__main__":
    unittest.main(verbosity=2)

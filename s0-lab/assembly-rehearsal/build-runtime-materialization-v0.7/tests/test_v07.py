"""Bounded adversarial verification for PUBLIC runtime materializer v0.7.

All synthetic writes are constrained to BRM07_TEST_RAW_ROOT.  Repository inputs
are authenticated before this module imports the candidate package.
"""

from __future__ import annotations

import contextlib
import hashlib
import importlib
import io
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import threading
import unittest
import warnings
import zipfile
from pathlib import Path
from unittest import mock


REPOSITORY = Path(os.environ["BRM07_REPOSITORY_ROOT"]).resolve(strict=True)
RAW_ROOT = Path(os.environ["BRM07_TEST_RAW_ROOT"]).resolve(strict=True)
FINAL_ROOT = Path(os.environ["BRM07_FINAL_ROOT"]).resolve(strict=True)
CACHE_ROOT = Path(os.environ["BRM07_CACHE_ROOT"]).resolve(strict=True)

from s0_public_build_runtime import authority as authority_module  # noqa: E402
from s0_public_build_runtime import canonical  # noqa: E402
from s0_public_build_runtime import ArtifactPin, activate_repository_authority  # noqa: E402
from s0_public_build_runtime import errors  # noqa: E402
materialize_module = importlib.import_module("s0_public_build_runtime.materialize")  # noqa: E402


EXPECTED_IMPLEMENTATION = {
    "__init__.py": "12ca47b823c8c8cbe1b8f2bb2de912a1695d3bb2550ea7c90947379e88e7b011",
    "__main__.py": "097f9fe6ecccda122f33f26e23ed8de5a5ac26c53d9a2b8bbb218731c3ab69f8",
    "authority.py": "985d64c7e9e65aaff97518729a32cde27062239b0a0de276c02871c88b3f12eb",
    "canonical.py": "17f02071c3514f5c99aae5c96d3d13d4b76d6a312a379bcfd7a06065ecf5fec5",
    "cli.py": "33bc72d474efe81dbb7c320ce54fd47dba1a0dfbf8e3ba6bb7131d63b70016da",
    "errors.py": "5e1235e362756224e6c494271a1d8532e2708767c29e01b462ddffe370600850",
    "materialize.py": "17c2cf9032998fe9653a5f6b8535eb76e4f15693e8b834ca60d10755bfa430f7",
}


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def assert_under_raw(path: Path) -> None:
    if os.path.commonpath((str(path.resolve()), str(RAW_ROOT))) != str(RAW_ROOT):
        raise AssertionError("test cleanup target escaped raw root")


@contextlib.contextmanager
def raw_temporary_directory(prefix: str):
    directory = Path(tempfile.mkdtemp(prefix=prefix, dir=RAW_ROOT))
    try:
        yield directory
    finally:
        assert_under_raw(directory)
        if directory.exists() and not directory.is_symlink():
            shutil.rmtree(directory)


def make_zip(entries: list[tuple[str, bytes, int | None]], *, compression: int = zipfile.ZIP_STORED) -> bytes:
    stream = io.BytesIO()
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", UserWarning)
        with zipfile.ZipFile(stream, "w", compression=compression) as archive:
            for name, data, external_attr in entries:
                info = zipfile.ZipInfo(name)
                info.compress_type = compression
                if external_attr is not None:
                    info.external_attr = external_attr
                archive.writestr(info, data)
    return stream.getvalue()


def inspect_zip(raw: bytes):
    return materialize_module._inspect_archive(io.BytesIO(raw))


class FakeResponse:
    def __init__(self, data: bytes, *, url: str, status: int = 200, content_length: str | None = None):
        self._data = io.BytesIO(data)
        self._url = url
        self.status = status
        self.headers = {"Content-Encoding": "identity"}
        if content_length is not None:
            self.headers["Content-Length"] = content_length

    def read(self, size: int = -1) -> bytes:
        return self._data.read(size)

    def geturl(self) -> str:
        return self._url

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


class FakeOpener:
    def __init__(self, response: FakeResponse):
        self.response = response

    def open(self, request, timeout):
        return self.response


class AuthenticationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.activated = activate_repository_authority(str(REPOSITORY))

    def test_implementation_hashes_are_exact_before_import(self):
        implementation = REPOSITORY / "s0-lab/assembly-rehearsal/build-runtime-materialization-v0.7/implementation/s0_public_build_runtime"
        self.assertEqual({name: digest(implementation / name) for name in EXPECTED_IMPLEMENTATION}, EXPECTED_IMPLEMENTATION)

    def test_authenticated_authority_and_pin_order(self):
        self.activated.require_authenticated()
        self.assertEqual(tuple(pin.pin_id for pin in self.activated.pins), tuple(pin.pin_id for pin in authority_module._EXPECTED_PINS))
        self.assertEqual(len(self.activated.pins), 7)
        record = authority_module.authority_record(self.activated)
        policy = record["publication_policy_authority"]
        self.assertEqual(policy["active_policy_id"], "python-os-rename-windows-no-replace-v0.7")
        self.assertFalse(policy["caller_selected"])
        self.assertFalse(policy["historical_special_api_policy_active"])
        with self.assertRaises(TypeError):
            activate_repository_authority(str(REPOSITORY), publication_policy="kernel32.dll!SetFileInformationByHandle:FileRenameInfoEx:22")

    def test_evidence_byte_mutation_rejected(self):
        mutated = bytearray(self.activated.evidence_raw)
        mutated[-2] ^= 1
        with raw_temporary_directory("evidence-change-") as root:
            target = root / authority_module._EVIDENCE_PATH
            target.parent.mkdir(parents=True)
            target.write_bytes(mutated)
            with self.assertRaises(errors.AuthenticationError):
                authority_module._authenticate_evidence(root)

    def test_forged_and_subclass_authority_rejected(self):
        forged = object.__new__(authority_module._ActivatedAuthority)
        with self.assertRaises(Exception):
            authority_module.authority_record(forged)

        class Subclass(authority_module._ActivatedAuthority):
            pass

        with self.assertRaises(errors.AuthenticationError):
            Subclass(
                authority_module._TOKEN,
                self.activated.design_rows,
                self.activated.evidence_raw,
                self.activated.pins,
            )

    def test_mutated_authority_rejected(self):
        changed = activate_repository_authority(str(REPOSITORY))
        changed.design_rows = ()
        with self.assertRaises(errors.AuthenticationError):
            changed.require_authenticated()

    def test_caller_cannot_mint_authority_with_module_token(self):
        fake_rows = tuple((f"fake-{index}", 0, "0" * 64) for index in range(40))
        with self.assertRaises(errors.AuthenticationError):
            authority_module._ActivatedAuthority(
                authority_module._TOKEN,
                fake_rows,
                self.activated.evidence_raw,
                self.activated.pins,
            )

    def test_pin_size_hash_and_order_mismatch_rejected(self):
        with self.assertRaises((errors.AuthenticationError, errors.CanonicalError)):
            ArtifactPin("x", "x", "1", "x.zip", True, "0" * 64, "https://example.com/x.zip", "x", "")
        with self.assertRaises((errors.AuthenticationError, errors.CanonicalError)):
            ArtifactPin("x", "x", "1", "x.zip", 1, "A" * 64, "https://example.com/x.zip", "x", "")
        with self.assertRaises(errors.AuthenticationError):
            authority_module._ActivatedAuthority(
                authority_module._TOKEN,
                self.activated.design_rows,
                self.activated.evidence_raw,
                tuple(reversed(self.activated.pins)),
            )


class DownloadTests(unittest.TestCase):
    def pin(self, data: bytes, *, expected: bytes | None = None) -> ArtifactPin:
        pinned = data if expected is None else expected
        return ArtifactPin("synthetic", "synthetic", "1", "synthetic.zip", len(pinned), hashlib.sha256(pinned).hexdigest(), "https://example.com/synthetic.zip", "test", "")

    def run_download(self, pin: ArtifactPin, response: FakeResponse, root: Path):
        with mock.patch.object(materialize_module.urllib.request, "build_opener", return_value=FakeOpener(response)):
            return materialize_module._download(pin, root)

    def test_exact_download_succeeds(self):
        data = b"exact"
        with raw_temporary_directory("download-good-") as root:
            path, observation = self.run_download(self.pin(data), FakeResponse(data, url="https://example.com/synthetic.zip", content_length=str(len(data))), root)
            self.assertEqual(path.read_bytes(), data)
            self.assertEqual(observation["source"], "https-download")

    def test_final_host_redirect_oversize_short_and_hash_mismatch_reject(self):
        cases = [
            (b"exact", b"exact", "https://evil.example/synthetic.zip", "5"),
            (b"longer", b"short", "https://example.com/synthetic.zip", None),
            (b"x", b"short", "https://example.com/synthetic.zip", None),
            (b"wrong", b"other", "https://example.com/synthetic.zip", None),
        ]
        for index, (actual, expected, url, length) in enumerate(cases):
            with self.subTest(index=index), raw_temporary_directory(f"download-bad-{index}-") as root:
                with self.assertRaises(errors.AcquisitionError):
                    self.run_download(self.pin(actual, expected=expected), FakeResponse(actual, url=url, content_length=length), root)
                self.assertEqual(list(root.iterdir()), [])

    def test_redirect_policy_rejects_cross_host_and_redirect_overflow(self):
        redirects = materialize_module._Redirects("example.com")
        with self.assertRaises(errors.AcquisitionError):
            redirects.redirect_request(None, None, 302, "", None, "https://evil.example/x")
        redirects.urls[:] = ["https://example.com/1", "https://example.com/2", "https://example.com/3"]
        with self.assertRaises(errors.AcquisitionError):
            redirects.redirect_request(None, None, 302, "", None, "https://example.com/4")

    def test_untrusted_cache_substitution_rejected(self):
        with raw_temporary_directory("cache-substitute-") as root:
            (root / "synthetic.zip").write_bytes(b"wrong")
            with self.assertRaises(errors.AcquisitionError):
                materialize_module._download(self.pin(b"exact"), root)


class ArchiveTests(unittest.TestCase):
    def reject(self, entries, *, compression=zipfile.ZIP_STORED):
        raw = make_zip(entries, compression=compression)
        with self.assertRaises(errors.ArchiveError):
            inspect_zip(raw)

    def test_member_path_matrix(self):
        for name in ("/absolute", "C:/drive", "back\\slash", "../escape", "a/../escape", "", "con.txt", "aux/file", "trail. /x", "trail /x"):
            with self.subTest(name=name), self.assertRaises(errors.ArchiveError):
                materialize_module._member_path(name)

    def test_duplicate_case_alias_prefix_and_symlink_reject(self):
        self.reject([("a", b"1", None), ("a", b"2", None)])
        self.reject([("A", b"1", None), ("a", b"2", None)])
        self.reject([("a", b"1", None), ("a/b", b"2", None)])
        self.reject([("link", b"target", (stat.S_IFLNK | 0o777) << 16)])

    def test_windows_reparse_like_attribute_rejected(self):
        self.reject([("reparse", b"target", materialize_module._REPARSE)])

    def test_unsupported_compression_rejected(self):
        raw = bytearray(make_zip([("x", b"x", None)]))
        local = raw.find(b"PK\x03\x04")
        central = raw.find(b"PK\x01\x02")
        self.assertGreaterEqual(local, 0)
        self.assertGreaterEqual(central, 0)
        raw[local + 8:local + 10] = (99).to_bytes(2, "little")
        raw[central + 10:central + 12] = (99).to_bytes(2, "little")
        with self.assertRaises(errors.ArchiveError):
            inspect_zip(bytes(raw))

    def test_count_size_and_ratio_boundaries(self):
        two = make_zip([("a", b"aa", None), ("b", b"bb", None)])
        three = make_zip([("a", b"aa", None), ("b", b"bb", None), ("c", b"x", None)])
        with mock.patch.object(materialize_module, "_MAX_ENTRIES", 2):
            archive, rows, total = inspect_zip(two)
            archive.close()
            self.assertEqual((len(rows), total), (2, 4))
            with self.assertRaises(errors.ArchiveError):
                inspect_zip(three)
        with mock.patch.object(materialize_module, "_MAX_ARCHIVE_BYTES", 4), mock.patch.object(materialize_module, "_MAX_ENTRY_BYTES", 4):
            archive, _, total = inspect_zip(two)
            archive.close()
            self.assertEqual(total, 4)
            with self.assertRaises(errors.ArchiveError):
                inspect_zip(three)
        compressed = make_zip([("ratio", b"A" * 4096, None)], compression=zipfile.ZIP_DEFLATED)
        with mock.patch.object(materialize_module, "_MAX_RATIO", 1000):
            archive, _, _ = inspect_zip(compressed)
            archive.close()
        with mock.patch.object(materialize_module, "_MAX_RATIO", 2):
            with self.assertRaises(errors.ArchiveError):
                inspect_zip(compressed)

    def test_wheel_pth_and_cross_archive_shadow_rejected(self):
        with raw_temporary_directory("extract-") as root:
            with self.assertRaises(errors.ArchiveError):
                materialize_module._extract(io.BytesIO(make_zip([("evil.pth", b"import evil", None)])), root, "Lib/site-packages", "wheel", set(), {})
            claimed = {"lib/site-packages/a"}
            with self.assertRaises(errors.ArchiveError):
                materialize_module._extract(io.BytesIO(make_zip([("a/b", b"x", None)])), root, "Lib/site-packages", "wheel", claimed, {})


class StandardPublicationTests(unittest.TestCase):
    def test_real_os_rename_once_same_volume_identity_and_no_fallback(self):
        with raw_temporary_directory("os-rename-success-") as parent:
            staging = parent / "staging"
            final = parent / "final"
            staging.mkdir()
            (staging / "sentinel").write_bytes(b"source")
            staging_identity = materialize_module._identity(staging)
            parent_identity = materialize_module._identity(parent)
            materialize_module._require_unpublished_state(staging, staging_identity, final, parent_identity)
            observation, _ = materialize_module._destination_absence(final, parent_identity)
            self.assertTrue(observation["destination_absent_observed"])
            self.assertEqual(staging.lstat().st_dev, parent.lstat().st_dev)
            real_rename = os.rename
            with mock.patch.object(materialize_module.os, "rename", wraps=real_rename) as rename, mock.patch.object(
                materialize_module.os, "replace", side_effect=AssertionError("os.replace fallback")
            ) as replace, mock.patch.object(materialize_module.shutil, "move", side_effect=AssertionError("shutil.move fallback")) as move:
                materialize_module.os.rename(staging, final)
            self.assertEqual(rename.call_count, 1)
            self.assertEqual(replace.call_count, 0)
            self.assertEqual(move.call_count, 0)
            self.assertFalse(staging.exists())
            self.assertEqual(materialize_module._identity(final), staging_identity)
            self.assertEqual((final / "sentinel").read_bytes(), b"source")
            policy, _ = materialize_module._publication_policy()
            self.assertEqual(policy["policy_id"], "python-os-rename-windows-no-replace-v0.7")
            self.assertEqual(policy["primitive"], "python.os.rename")
            self.assertEqual(policy["invocation_count"], 1)
            self.assertFalse(policy["fallback_allowed"])
            self.assertFalse(policy["retry_allowed"])
            source_text = Path(materialize_module.__file__).read_text(encoding="utf-8")
            self.assertNotIn("SetFileInformationByHandle", source_text)
            self.assertNotIn("MoveFileEx", source_text)
            self.assertFalse((Path(materialize_module.__file__).parent / "publication.py").exists())

    def test_real_os_rename_existing_destination_fileexists_preserves_both(self):
        with raw_temporary_directory("os-rename-existing-") as parent:
            staging = parent / "staging"
            final = parent / "final"
            staging.mkdir()
            final.mkdir()
            (staging / "source-sentinel").write_bytes(b"source")
            (final / "attacker-sentinel").write_bytes(b"attacker")
            real_rename = os.rename
            with mock.patch.object(materialize_module.os, "rename", wraps=real_rename) as rename:
                with self.assertRaises(FileExistsError):
                    materialize_module.os.rename(staging, final)
            self.assertEqual(rename.call_count, 1)
            self.assertEqual((staging / "source-sentinel").read_bytes(), b"source")
            self.assertEqual((final / "attacker-sentinel").read_bytes(), b"attacker")


class PathAndFailureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.authority = activate_repository_authority(str(REPOSITORY))

    def cleanup_assertions(self, parent: Path, final: Path, *, published: bool):
        lock = parent / f".{final.name}.s0-brm-v0.7.lock"
        self.assertFalse(lock.exists(), "owned lock leaked")
        self.assertEqual(list(parent.glob(f".{final.name}.staging-*")), [], "owned staging leaked")
        self.assertTrue((parent / "unrelated-sentinel").is_file(), "unrelated path was deleted")
        self.assertEqual(final.exists(), published)

    def make_roots(self, parent: Path):
        cache = parent / "cache"
        cache.mkdir()
        (parent / "unrelated-sentinel").write_text("preserve", encoding="ascii")
        return cache, parent / "final"

    def test_repository_and_denied_f0_descendants_rejected(self):
        inside = REPOSITORY / "s0-lab/assembly-rehearsal/build-runtime-materialization-v0.7/tests/not-a-runtime"
        denied = REPOSITORY / "s0-lab/control/f0-sealed/not-a-runtime"
        for path in (inside, denied):
            with self.subTest(kind=path.parent.name), self.assertRaises(errors.PathSafetyError):
                materialize_module._safe_external_root(str(path), REPOSITORY, must_exist=False)

    def test_existing_destination_rejected(self):
        with raw_temporary_directory("existing-final-") as parent:
            final = parent / "final"
            final.mkdir()
            (final / "attacker-sentinel").write_bytes(b"preserve-attacker")
            with self.assertRaises(errors.PathSafetyError):
                materialize_module._safe_external_root(str(final), REPOSITORY, must_exist=False)
            self.assertEqual((final / "attacker-sentinel").read_bytes(), b"preserve-attacker")

    def test_reparse_parent_rejected_when_synthesizable(self):
        with raw_temporary_directory("reparse-") as parent:
            target = parent / "target"
            target.mkdir()
            link = parent / "link"
            try:
                os.symlink(target, link, target_is_directory=True)
            except OSError as error:
                self.skipTest(f"directory symlink unavailable: {error.winerror}")
            with self.assertRaises(errors.PathSafetyError):
                materialize_module._safe_external_root(str(link / "final"), REPOSITORY, must_exist=False)
            link.unlink()

    def test_concurrent_second_materializer_fails_closed(self):
        with raw_temporary_directory("concurrent-") as parent:
            cache, final = self.make_roots(parent)
            entered = threading.Event()
            release = threading.Event()
            first_errors: list[BaseException] = []

            def blocked_download(pin, cache_root):
                entered.set()
                release.wait(10)
                raise errors.AcquisitionError("injected-download-stop")

            def first():
                try:
                    materialize_module.materialize(str(REPOSITORY), str(cache), str(final))
                except BaseException as error:
                    first_errors.append(error)

            with mock.patch.object(materialize_module, "_download", side_effect=blocked_download):
                thread = threading.Thread(target=first)
                thread.start()
                self.assertTrue(entered.wait(10))
                with self.assertRaises(FileExistsError):
                    materialize_module.materialize(str(REPOSITORY), str(cache), str(final))
                release.set()
                thread.join(10)
            self.assertFalse(thread.is_alive())
            self.assertEqual(len(first_errors), 1)
            self.assertIsInstance(first_errors[0], errors.AcquisitionError)
            self.cleanup_assertions(parent, final, published=False)

    def test_prepublication_failure_cleanup_matrix(self):
        cases = {
            "download": ("_download", errors.AcquisitionError("injected-download")),
            "extract": ("_extract", errors.ArchiveError("injected-extract")),
        }
        for name, (attribute, exception) in cases.items():
            with self.subTest(name=name), raw_temporary_directory(f"prepub-{name}-") as parent:
                cache, final = self.make_roots(parent)
                with mock.patch.object(materialize_module, attribute, side_effect=exception):
                    with self.assertRaises(type(exception)):
                        materialize_module.materialize(str(REPOSITORY), str(cache), str(final))
                self.cleanup_assertions(parent, final, published=False)

    def test_publish_rename_failure_cleans_staging(self):
        with raw_temporary_directory("publish-failure-") as parent:
            cache, final = self.make_roots(parent)
            for pin in self.authority.pins:
                shutil.copyfile(CACHE_ROOT / pin.filename, cache / pin.filename)
            with mock.patch.object(materialize_module.os, "rename", side_effect=FileExistsError("injected-publish-rename")) as rename:
                with self.assertRaises(FileExistsError):
                    materialize_module.materialize(str(REPOSITORY), str(cache), str(final))
            self.assertEqual(rename.call_count, 1)
            self.cleanup_assertions(parent, final, published=False)

    def test_staging_reparse_replacement_rejected_before_download(self):
        with raw_temporary_directory("staging-reparse-") as parent:
            cache, final = self.make_roots(parent)
            target = parent / "junction-target"
            target.mkdir()
            link = parent / "forced-staging"
            creation = subprocess.run(
                ["cmd.exe", "/d", "/c", "mklink", "/J", str(link), str(target)],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=10,
                check=False,
            )
            if creation.returncode != 0:
                self.skipTest(f"directory junction unavailable: exit {creation.returncode}")
            try:
                with mock.patch.object(materialize_module.tempfile, "mkdtemp", return_value=str(link)), mock.patch.object(
                    materialize_module, "_download", side_effect=errors.AcquisitionError("download-should-not-start")
                ):
                    with self.assertRaises(errors.PathSafetyError):
                        materialize_module.materialize(str(REPOSITORY), str(cache), str(final))
            finally:
                if link.exists():
                    link.rmdir()
            self.cleanup_assertions(parent, final, published=False)

    def test_intervening_destination_race_preserves_attacker_and_emits_no_complete(self):
        with raw_temporary_directory("destination-race-") as parent:
            cache, final = self.make_roots(parent)
            for pin in self.authority.pins:
                shutil.copyfile(CACHE_ROOT / pin.filename, cache / pin.filename)
            original_absence = materialize_module._destination_absence
            original_rename = os.rename
            absence_calls = 0
            injected = False

            def inject_immediately_before_rename(destination, parent_identity):
                nonlocal absence_calls, injected
                absence_calls += 1
                result = original_absence(destination, parent_identity)
                if absence_calls == 2:
                    self.assertFalse(injected)
                    final.mkdir()
                    (final / "attacker-sentinel").write_bytes(b"preserve-attacker")
                    injected = True
                return result

            with mock.patch.object(materialize_module, "_destination_absence", side_effect=inject_immediately_before_rename), mock.patch.object(
                materialize_module.os, "rename", wraps=original_rename
            ) as rename, mock.patch.object(materialize_module.os, "replace", side_effect=AssertionError("os.replace fallback")) as replace, mock.patch.object(
                materialize_module.shutil, "move", side_effect=AssertionError("shutil.move fallback")
            ) as move:
                with self.assertRaises(FileExistsError):
                    materialize_module.materialize(str(REPOSITORY), str(cache), str(final))
            self.assertTrue(injected)
            self.assertEqual(absence_calls, 2)
            self.assertEqual(rename.call_count, 1)
            self.assertEqual(replace.call_count, 0)
            self.assertEqual(move.call_count, 0)
            self.assertEqual((final / "attacker-sentinel").read_bytes(), b"preserve-attacker")
            self.assertEqual({path.name for path in final.iterdir()}, {"attacker-sentinel"})
            self.assertFalse((final / "evidence/runtime-record.json").exists())
            self.assertFalse((final / "evidence/status.json").exists())
            self.assertTrue((parent / "unrelated-sentinel").is_file())
            self.assertFalse((parent / f".{final.name}.s0-brm-v0.7.lock").exists())
            self.assertEqual(list(parent.glob(f".{final.name}.staging-*")), [])

    def _postpublish_failure(self, name: str, patcher):
        with raw_temporary_directory(f"postpub-{name}-") as parent:
            cache, final = self.make_roots(parent)
            for pin in self.authority.pins:
                shutil.copyfile(CACHE_ROOT / pin.filename, cache / pin.filename)
            with patcher:
                with self.assertRaises(errors.BuildRuntimeError):
                    materialize_module.materialize(str(REPOSITORY), str(cache), str(final))
            self.cleanup_assertions(parent, final, published=True)
            evidence = final / "evidence"
            self.assertTrue((evidence / "failure-status.json").is_file())
            failure = canonical.strict_json((evidence / "failure-status.json").read_bytes())
            self.assertEqual(failure["status"], "FAILED-AFTER-PUBLICATION-NOT-READY")
            self.assertFalse((evidence / "status.json").exists())

    def test_postpublication_readback_probe_and_record_failures_are_explicit(self):
        original_inventory = materialize_module._inventory
        calls = 0

        def fail_second_inventory(*args, **kwargs):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise errors.PublicationError("injected-readback")
            return original_inventory(*args, **kwargs)

        self._postpublish_failure("readback", mock.patch.object(materialize_module, "_inventory", side_effect=fail_second_inventory))
        self._postpublish_failure("probe", mock.patch.object(materialize_module, "_probe", side_effect=errors.ProbeError("injected-probe")))

        original_pair = materialize_module._write_pair

        def fail_record(directory, filename, value):
            if filename == "runtime-record.json":
                raise errors.PublicationError("injected-record")
            return original_pair(directory, filename, value)

        self._postpublish_failure("record", mock.patch.object(materialize_module, "_write_pair", side_effect=fail_record))


def read_canonical_pair(directory: Path, filename: str) -> tuple[dict[str, object], str]:
    raw = (directory / filename).read_bytes()
    value = canonical.strict_json(raw)
    if canonical.jcs_lf(value) != raw:
        raise AssertionError(f"{filename} is not canonical JCS+LF")
    value_digest = hashlib.sha256(raw).hexdigest()
    if (directory / f"{filename}.sha256").read_bytes() != canonical.sidecar_bytes(filename, value_digest):
        raise AssertionError(f"{filename} sidecar differs")
    return value, value_digest


def audit_live_runtime() -> dict[str, object]:
    activated = activate_repository_authority(str(REPOSITORY))
    cache_rows = []
    for pin in activated.pins:
        path = CACHE_ROOT / pin.filename
        cache_rows.append({"filename": pin.filename, "size": path.stat().st_size, "sha256": digest(path)})
        if (path.stat().st_size, digest(path)) != (pin.size, pin.sha256):
            raise AssertionError(f"cache pin mismatch: {pin.pin_id}")
    if {entry.name for entry in CACHE_ROOT.iterdir()} != {pin.filename for pin in activated.pins}:
        raise AssertionError("cache physical inventory differs")

    evidence = FINAL_ROOT / "evidence"
    payload, payload_hash = read_canonical_pair(evidence, "payload-manifest.json")
    prepublication_path = evidence / "prepublication-record.json"
    with prepublication_path.open("rb") as first_handle:
        prepublication_first = first_handle.read()
    first_closed = first_handle.closed
    with prepublication_path.open("rb") as second_handle:
        prepublication_second = second_handle.read()
    second_closed = second_handle.closed
    if not first_closed or not second_closed or prepublication_first != prepublication_second:
        raise AssertionError("prepublication record closed/reopened readback differs")
    prepublication, prepublication_hash = read_canonical_pair(evidence, "prepublication-record.json")
    record, record_hash = read_canonical_pair(evidence, "runtime-record.json")
    status, status_hash = read_canonical_pair(evidence, "status.json")
    rows = []
    for path in sorted((path for path in FINAL_ROOT.rglob("*") if path.is_file() and evidence not in path.parents), key=lambda p: p.relative_to(FINAL_ROOT).as_posix().encode("ascii")):
        rows.append({"path": path.relative_to(FINAL_ROOT).as_posix(), "size": path.stat().st_size, "sha256": digest(path)})
    expected_rows = [{"path": row["path"], "size": row["size"], "sha256": row["sha256"]} for row in payload["files"]]
    if rows != expected_rows:
        raise AssertionError("physical final payload differs from payload manifest")
    if payload_hash != record["payload_manifest_sha256"] or record_hash != status["runtime_record_sha256"]:
        raise AssertionError("evidence chain differs")
    body = prepublication["body"]
    body_hash = hashlib.sha256(canonical.jcs_lf(body)).hexdigest()
    if not prepublication["body_hashes_equal"] or {
        prepublication["body_canonical_sha256"],
        prepublication["body_closed_file_sha256"],
        prepublication["body_readback_sha256"],
    } != {body_hash}:
        raise AssertionError("prepublication canonical closed/reopened body hashes differ")
    publication = record["publication_transaction"]
    if not (
        prepublication_hash == record["prepublication_record_sha256"]
        == publication["prepublication_record_package_sha256"]
        == status["prepublication_record_sha256"]
    ):
        raise AssertionError("prepublication record is not bound into runtime and status records")
    if not (
        body["transaction_id"] == publication["transaction_id"] == status["transaction_id"]
        and body["publication_primitive_id"] == publication["publication_primitive_id"] == status["publication_primitive_id"]
        == "python.os.rename"
        and body["publication_policy"]["policy_id"] == publication["publication_policy_id"] == status["publication_policy_id"]
        == "python-os-rename-windows-no-replace-v0.7"
        and body["publication_policy_sha256"] == publication["publication_policy_sha256"] == status["publication_policy_sha256"]
    ):
        raise AssertionError("publication primitive fields are not bound across evidence records")
    if not (
        body["staging_identity_sha256"] == publication["staging_prepublication_identity_sha256"]
        and body["destination_parent_identity_sha256"] == publication["destination_parent_identity_sha256"]
        and body["destination_absent_observed"] is True
        and body["same_volume_verified"] is True
        and body["effective_acl_access_verified"] is True
        and body["publication_invocation_limit"] == 1
        and body["fallback_allowed"] is False
        and body["retry_allowed"] is False
        and publication["destination_absent_recheck_observed"] is True
        and publication["postpublication_identity_verified"] is True
        and publication["no_overwrite_rename_result"] == "success"
        and publication["publication_invocation_count"] == 1
        and publication["fallback_allowed"] is False
        and publication["retry_allowed"] is False
        and publication["publication_linearization_point"] == "successful-os.rename-call"
    ):
        raise AssertionError("publication identity, access, absence, or invocation evidence differs")
    if record["status"] != "COMPLETE-RUNTIME-MATERIALIZATION-ONLY" or status["status"] != "COMPLETE-RUNTIME-MATERIALIZATION-ONLY":
        raise AssertionError("successful publication lacks exact COMPLETE status binding")
    expected_claims = {
        "build_runtime_materialized": True,
        "central_system_complete": False,
        "model_to_model_transfer_validated": False,
        "operational_safety_validated": False,
        "project_brain_integrated": False,
        "rehearsal_complete": False,
        "s0_complete": False,
    }
    if record["claims"] != expected_claims or "OS-DLL-and-runtime-loader-closure" not in record["nonclaims"]:
        raise AssertionError("claims/nonclaims differ")

    with raw_temporary_directory("hostile-isolation-") as hostile:
        for module in ("jsonschema.py", "attrs.py", "jsonschema_specifications.py", "referencing.py", "rpds.py", "typing_extensions.py"):
            (hostile / module).write_text("raise RuntimeError('hostile-shadow-loaded')\n", encoding="ascii")
        probe = """import hashlib,importlib,importlib.metadata,json,os,sys
names=('jsonschema','attrs','jsonschema_specifications','referencing','rpds','typing_extensions','rpds.rpds')
origins={}; hashes={}
for name in names:
 m=importlib.import_module(name); p=os.path.realpath(m.__file__); origins[name]=p
 with open(p,'rb') as f: hashes[name]=hashlib.sha256(f.read()).hexdigest()
with open(sys.executable,'rb') as f: executable_sha256=hashlib.sha256(f.read()).hexdigest()
print(json.dumps({'executable':os.path.realpath(sys.executable),'executable_sha256':executable_sha256,'prefix':os.path.realpath(sys.prefix),'path':[os.path.realpath(p) for p in sys.path],'origins':origins,'origin_sha256':hashes,'versions':{p:importlib.metadata.version(p) for p in ('jsonschema','attrs','jsonschema-specifications','referencing','rpds-py','typing-extensions')}},sort_keys=True,separators=(',',':')))
"""
        environment = os.environ.copy()
        environment.update({"PYTHONPATH": str(hostile), "PYTHONHOME": str(hostile), "PYTHONUSERBASE": str(hostile), "PYTHONNOUSERSITE": "0", "PYTHONDONTWRITEBYTECODE": "1"})
        process = subprocess.run([str(FINAL_ROOT / "python.exe"), "-I", "-B", "-c", probe], cwd=hostile, env=environment, input=b"", stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30, check=False)
        if process.returncode != 0:
            raise AssertionError(f"hostile isolated probe rejected: {process.stderr.decode('utf-8', 'replace')}")
        isolation = json.loads(process.stdout.decode("utf-8", "strict"))
    site = (FINAL_ROOT / "Lib/site-packages").resolve()
    for name, origin in isolation["origins"].items():
        origin_path = Path(origin).resolve()
        if os.path.commonpath((str(origin_path), str(site))) != str(site):
            raise AssertionError(f"hostile shadow escaped final site-packages: {name}")
        if digest(origin_path) != isolation["origin_sha256"][name]:
            raise AssertionError(f"origin changed across hostile probe: {name}")
    expected_path = [str((FINAL_ROOT / "python312.zip").resolve()), str(FINAL_ROOT), str(site)]
    if isolation["path"] != expected_path or Path(isolation["executable"]).resolve() != (FINAL_ROOT / "python.exe").resolve() or Path(isolation["prefix"]).resolve() != FINAL_ROOT:
        raise AssertionError("isolated executable/prefix/path differs")
    expected_versions = {"jsonschema": "4.26.0", "attrs": "26.1.0", "jsonschema-specifications": "2025.9.1", "referencing": "0.37.0", "rpds-py": "2026.6.3", "typing-extensions": "4.16.0"}
    if isolation["versions"] != expected_versions:
        raise AssertionError("isolated versions differ")
    extension = Path(isolation["origins"]["rpds.rpds"])
    if extension.suffix.casefold() != ".pyd":
        raise AssertionError("rpds native origin is not .pyd")
    implementation = REPOSITORY / "s0-lab/assembly-rehearsal/build-runtime-materialization-v0.7/implementation"
    no_replace_environment = os.environ.copy()
    no_replace_environment.update({"PYTHONPATH": str(implementation), "PYTHONDONTWRITEBYTECODE": "1"})
    no_replace_started = __import__("time").monotonic()
    no_replace = subprocess.run(
        [
            sys.executable,
            "-B",
            "-m",
            "s0_public_build_runtime",
            "--repository-root",
            str(REPOSITORY),
            "--cache-root",
            str(CACHE_ROOT),
            "--final-root",
            str(FINAL_ROOT),
        ],
        cwd=REPOSITORY,
        env=no_replace_environment,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=30,
        check=False,
    )
    no_replace_elapsed = int((__import__("time").monotonic() - no_replace_started) * 1000)
    no_replace_stderr = no_replace.stderr.decode("utf-8", "strict")
    if no_replace.returncode != 2 or no_replace.stdout != b"" or json.loads(no_replace_stderr) != {"error_type": "PathSafetyError", "status": "REJECTED"}:
        raise AssertionError("exact no-replace rerun did not reject canonically")
    return {
        "cache": cache_rows,
        "claims": record["claims"],
        "evidence": {"payload_manifest_sha256": payload_hash, "prepublication_record_sha256": prepublication_hash, "runtime_record_sha256": record_hash, "status_sha256": status_hash},
        "final_file_count_excluding_evidence": len(rows),
        "final_total_bytes_excluding_evidence": sum(row["size"] for row in rows),
        "hostile_isolation_probe": isolation,
        "native_payload": record["native_payload"],
        "no_replace_rerun": {"elapsed_milliseconds": no_replace_elapsed, "exit_code": no_replace.returncode, "stderr": no_replace_stderr, "stdout": no_replace.stdout.decode("utf-8", "strict")},
        "nonclaims": record["nonclaims"],
        "physical_inventory": rows,
        "publication_transaction": publication,
    }


class LiveRuntimeTests(unittest.TestCase):
    def test_live_runtime_inventory_evidence_and_hostile_isolation(self):
        audit = audit_live_runtime()
        self.assertEqual(len(audit["cache"]), 7)
        self.assertGreater(audit["final_file_count_excluding_evidence"], 0)

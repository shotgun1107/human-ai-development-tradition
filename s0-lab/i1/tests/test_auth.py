from __future__ import annotations

import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


WORKSPACE = Path(__file__).resolve().parents[3]
IMPLEMENTATION = WORKSPACE / "s0-lab" / "i1" / "implementation"
sys.path.insert(0, str(IMPLEMENTATION))

from s0_i1.auth import (  # noqa: E402
    AuthenticatedManifest,
    ManifestGrant,
    _is_reparse,
    authenticate_manifest_entry,
    authenticate_manifest_file_set,
    bind_external_manifest_grant,
    load_authenticated_manifest,
    sha256_bytes,
)
from s0_i1.errors import AuthenticationError, UnsafePathError  # noqa: E402
from s0_i1.json_bytes import parse_strict_json_bytes  # noqa: E402


class AuthenticationTests(unittest.TestCase):
    def _workspace(self):
        return tempfile.TemporaryDirectory(dir=WORKSPACE / "s0-lab" / "i1" / "tests")

    def _make_manifest(
        self, root: Path, files: dict[str, bytes], *, purpose: str = "public-test-input"
    ) -> tuple[ManifestGrant, AuthenticatedManifest]:
        for relative, raw in files.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        lines = "".join(
            f"{sha256_bytes(raw)}  {relative}\n"
            for relative, raw in sorted(files.items())
        ).encode("ascii")
        manifest_path = root / "inputs" / "files.sha256"
        manifest_path.write_bytes(lines)
        grant = bind_external_manifest_grant(
            expected_manifest_path="inputs/files.sha256",
            expected_manifest_sha256=sha256_bytes(lines),
            expected_entry_prefix="inputs/",
            expected_allowed_paths=tuple(sorted(files)),
            purpose=purpose,
        )
        return grant, load_authenticated_manifest(root, grant)

    def test_same_authenticated_bytes_are_consumed_after_path_changes(self):
        with self._workspace() as temporary:
            root = Path(temporary)
            original = b'{"sentinel":"first"}\n'
            _grant, manifest = self._make_manifest(
                root, {"inputs/value.json": original}
            )
            authenticated = authenticate_manifest_entry(
                root, manifest, "inputs/value.json"
            )
            (root / "inputs" / "value.json").write_bytes(
                b'{"sentinel":"second"}\n'
            )
            self.assertEqual(authenticated.raw, original)
            self.assertEqual(
                parse_strict_json_bytes(authenticated.raw)["sentinel"], "first"
            )

    def test_caller_built_grant_manifest_and_plain_objects_cannot_fabricate_authority(self):
        with self.assertRaises(AuthenticationError):
            ManifestGrant(
                "inputs/files.sha256",
                "0" * 64,
                "inputs/",
                ("inputs/value.json",),
                "forged",
                "1" * 64,
                _provenance=object(),
            )
        with self.assertRaises(AuthenticationError):
            AuthenticatedManifest(
                SimpleNamespace(),
                SimpleNamespace(),
                {},
                "0" * 64,
                _provenance=object(),
            )
        with self._workspace() as temporary:
            with self.assertRaises(AuthenticationError):
                load_authenticated_manifest(Path(temporary), SimpleNamespace())

    def test_path_substitution_traversal_and_ungranted_path_are_rejected(self):
        with self._workspace() as temporary:
            root = Path(temporary)
            _grant, manifest = self._make_manifest(
                root,
                {
                    "inputs/allowed.json": b"{}\n",
                    "inputs/substitute.json": b"{}\n",
                },
            )
            with self.assertRaises(AuthenticationError):
                authenticate_manifest_entry(root, manifest, "inputs/missing.json")
            with self.assertRaises(UnsafePathError):
                authenticate_manifest_entry(
                    root, manifest, "inputs/../inputs/allowed.json"
                )
            with self.assertRaises(UnsafePathError):
                authenticate_manifest_entry(
                    root,
                    manifest,
                    str((root / "inputs" / "allowed.json").resolve()),
                )
            with self.assertRaises(UnsafePathError):
                authenticate_manifest_entry(
                    root, manifest, "inputs/allowed.json:stream"
                )

    def test_external_manifest_hash_mismatch_rejects_before_entry_use(self):
        with self._workspace() as temporary:
            root = Path(temporary)
            raw = b"{}\n"
            path = root / "inputs" / "value.json"
            path.parent.mkdir(parents=True)
            path.write_bytes(raw)
            manifest_raw = f"{sha256_bytes(raw)}  inputs/value.json\n".encode(
                "ascii"
            )
            (root / "inputs" / "files.sha256").write_bytes(manifest_raw)
            wrong = bind_external_manifest_grant(
                expected_manifest_path="inputs/files.sha256",
                expected_manifest_sha256="0" * 64,
                expected_entry_prefix="inputs/",
                expected_allowed_paths=("inputs/value.json",),
                purpose="public-test-input",
            )
            with self.assertRaisesRegex(AuthenticationError, "external trust hash"):
                load_authenticated_manifest(root, wrong)

    def test_complete_manifest_audit_rejects_extra_hidden_and_reparse_entries(self):
        with self._workspace() as temporary:
            root = Path(temporary)
            _grant, manifest = self._make_manifest(
                root, {"inputs/value.json": b"{}\n"}
            )
            (root / "inputs" / ".hidden.json").write_bytes(b"{}\n")
            with self.assertRaisesRegex(AuthenticationError, "initial file set"):
                authenticate_manifest_file_set(root, manifest)

        sentinel = SimpleNamespace(st_mode=stat.S_IFREG, st_file_attributes=0x400)
        self.assertTrue(_is_reparse(sentinel))

    def test_post_enumeration_extra_file_is_caught_by_stability_recheck(self):
        with self._workspace() as temporary:
            root = Path(temporary)
            _grant, manifest = self._make_manifest(
                root, {"inputs/value.json": b"{}\n"}
            )
            original = authenticate_manifest_entry
            injected = {"done": False}

            def inject(*args, **kwargs):
                result = original(*args, **kwargs)
                if not injected["done"]:
                    (root / "inputs" / "late.json").write_bytes(b"{}\n")
                    injected["done"] = True
                return result

            with patch("s0_i1.auth.authenticate_manifest_entry", side_effect=inject):
                with self.assertRaisesRegex(AuthenticationError, "changed after"):
                    authenticate_manifest_file_set(root, manifest)

    def test_post_read_content_change_is_caught_by_final_rehash(self):
        with self._workspace() as temporary:
            root = Path(temporary)
            _grant, manifest = self._make_manifest(
                root, {"inputs/value.json": b'{"v":1}\n'}
            )
            original = authenticate_manifest_entry
            injected = {"done": False}

            def inject(*args, **kwargs):
                result = original(*args, **kwargs)
                if not injected["done"]:
                    (root / "inputs" / "value.json").write_bytes(b'{"v":2}\n')
                    injected["done"] = True
                return result

            with patch("s0_i1.auth.authenticate_manifest_entry", side_effect=inject):
                with self.assertRaisesRegex(AuthenticationError, "content changed"):
                    authenticate_manifest_file_set(root, manifest)

    def test_change_during_final_manifest_revalidation_is_caught_by_last_enumeration(self):
        with self._workspace() as temporary:
            root = Path(temporary)
            _grant, manifest = self._make_manifest(
                root, {"inputs/value.json": b"{}\n"}
            )
            from s0_i1 import auth as auth_module

            original = auth_module._revalidate_manifest_file
            calls = {"count": 0}

            def inject(*args, **kwargs):
                calls["count"] += 1
                result = original(*args, **kwargs)
                if calls["count"] == 4:
                    (root / "inputs" / "final-race.json").write_bytes(b"{}\n")
                return result

            with patch(
                "s0_i1.auth._revalidate_manifest_file", side_effect=inject
            ):
                with self.assertRaisesRegex(AuthenticationError, "final stability"):
                    authenticate_manifest_file_set(root, manifest)

    def test_manifest_change_after_load_rejects_at_entry_boundary(self):
        with self._workspace() as temporary:
            root = Path(temporary)
            _grant, manifest = self._make_manifest(
                root, {"inputs/value.json": b"{}\n"}
            )
            (root / "inputs" / "files.sha256").write_bytes(
                b"0" * 64 + b"  inputs/value.json\n"
            )
            with self.assertRaisesRegex(AuthenticationError, "manifest changed"):
                authenticate_manifest_entry(root, manifest, "inputs/value.json")

    def test_exact_nonboolean_byte_ceiling_is_required(self):
        with self._workspace() as temporary:
            root = Path(temporary)
            _grant, manifest = self._make_manifest(
                root, {"inputs/value.json": b"{}\n"}
            )
            with self.assertRaisesRegex(AuthenticationError, "ceiling"):
                authenticate_manifest_entry(
                    root, manifest, "inputs/value.json", max_bytes=True
                )

    def test_reparse_detection_rejects_through_authenticated_path(self):
        with self._workspace() as temporary:
            root = Path(temporary)
            _grant, manifest = self._make_manifest(
                root, {"inputs/value.json": b"{}\n"}
            )
            with patch("s0_i1.auth._is_reparse", return_value=True):
                with self.assertRaisesRegex(UnsafePathError, "reparse-backed"):
                    authenticate_manifest_entry(root, manifest, "inputs/value.json")

    def test_symlink_input_is_rejected_when_host_permits_creation(self):
        with self._workspace() as temporary:
            root = Path(temporary)
            target = root / "target.json"
            target.write_bytes(b"{}\n")
            link = root / "inputs" / "link.json"
            link.parent.mkdir(parents=True)
            try:
                os.symlink(target, link)
            except OSError as exc:
                if isinstance(exc, PermissionError) or getattr(exc, "winerror", None) in {
                    5,
                    1314,
                }:
                    self.skipTest(
                        f"symlink privilege unavailable: {type(exc).__name__}"
                    )
                raise
            manifest_raw = (
                f"{sha256_bytes(target.read_bytes())}  inputs/link.json\n".encode(
                    "ascii"
                )
            )
            (root / "inputs" / "files.sha256").write_bytes(manifest_raw)
            grant = bind_external_manifest_grant(
                expected_manifest_path="inputs/files.sha256",
                expected_manifest_sha256=sha256_bytes(manifest_raw),
                expected_entry_prefix="inputs/",
                expected_allowed_paths=("inputs/link.json",),
                purpose="public-test-input",
            )
            manifest = load_authenticated_manifest(root, grant)
            with self.assertRaises(UnsafePathError):
                authenticate_manifest_entry(root, manifest, "inputs/link.json")


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import json
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
    ManifestAnchor,
    _is_reparse,
    authenticate_manifest_entry,
    authenticate_manifest_file_set,
    load_authenticated_manifest,
    sha256_bytes,
)
from s0_i1.errors import AuthenticationError, UnsafePathError  # noqa: E402
from s0_i1.json_bytes import parse_strict_json_bytes  # noqa: E402


class AuthenticationTests(unittest.TestCase):
    def _workspace(self):
        return tempfile.TemporaryDirectory(dir=WORKSPACE / "s0-lab" / "i1" / "tests")

    def _make_manifest(self, root: Path, files: dict[str, bytes]) -> ManifestAnchor:
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
        return ManifestAnchor("inputs/files.sha256", sha256_bytes(lines), "inputs/")

    def test_same_authenticated_bytes_are_consumed_after_path_changes(self):
        with self._workspace() as temporary:
            root = Path(temporary)
            original = b'{"sentinel":"first"}\n'
            anchor = self._make_manifest(root, {"inputs/value.json": original})
            manifest = load_authenticated_manifest(root, anchor)
            authenticated = authenticate_manifest_entry(root, manifest, "inputs/value.json")
            (root / "inputs" / "value.json").write_bytes(b'{"sentinel":"second"}\n')
            self.assertEqual(authenticated.raw, original)
            self.assertEqual(parse_strict_json_bytes(authenticated.raw)["sentinel"], "first")

    def test_path_substitution_and_traversal_are_rejected(self):
        with self._workspace() as temporary:
            root = Path(temporary)
            anchor = self._make_manifest(
                root,
                {
                    "inputs/allowed.json": b"{}\n",
                    "inputs/substitute.json": b"{}\n",
                },
            )
            manifest = load_authenticated_manifest(root, anchor)
            narrowed = type(manifest)(
                manifest.anchor,
                manifest.manifest,
                {"inputs/allowed.json": manifest.entries["inputs/allowed.json"]},
            )
            with self.assertRaises(AuthenticationError):
                authenticate_manifest_entry(root, narrowed, "inputs/substitute.json")
            with self.assertRaises(UnsafePathError):
                authenticate_manifest_entry(root, manifest, "inputs/../inputs/allowed.json")
            with self.assertRaises(UnsafePathError):
                authenticate_manifest_entry(root, manifest, str((root / "inputs" / "allowed.json").resolve()))
            with self.assertRaises(UnsafePathError):
                authenticate_manifest_entry(root, manifest, "inputs/allowed.json:stream")

    def test_manifest_anchor_mismatch_rejects_before_entry_use(self):
        with self._workspace() as temporary:
            root = Path(temporary)
            anchor = self._make_manifest(root, {"inputs/value.json": b"{}\n"})
            wrong = ManifestAnchor(anchor.manifest_path, "0" * 64, anchor.entry_prefix)
            with self.assertRaisesRegex(AuthenticationError, "anchor hash mismatch"):
                load_authenticated_manifest(root, wrong)

    def test_complete_manifest_audit_rejects_extra_file(self):
        with self._workspace() as temporary:
            root = Path(temporary)
            anchor = self._make_manifest(root, {"inputs/value.json": b"{}\n"})
            manifest = load_authenticated_manifest(root, anchor)
            (root / "inputs" / "extra.json").write_bytes(b"{}\n")
            with self.assertRaisesRegex(AuthenticationError, "file set mismatch"):
                authenticate_manifest_file_set(root, manifest)

    def test_reparse_attribute_sentinel_is_rejected_without_privilege(self):
        sentinel = SimpleNamespace(
            st_mode=stat.S_IFREG,
            st_file_attributes=0x400,
        )
        self.assertTrue(_is_reparse(sentinel))

    def test_reparse_detection_rejects_through_authenticated_path(self):
        with self._workspace() as temporary:
            root = Path(temporary)
            anchor = self._make_manifest(root, {"inputs/value.json": b"{}\n"})
            manifest = load_authenticated_manifest(root, anchor)
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
                if isinstance(exc, PermissionError) or getattr(exc, "winerror", None) in {5, 1314}:
                    self.skipTest(f"symlink privilege unavailable: {type(exc).__name__}")
                raise
            lines = f"{sha256_bytes(target.read_bytes())}  inputs/link.json\n".encode("ascii")
            manifest_path = root / "inputs" / "files.sha256"
            manifest_path.write_bytes(lines)
            anchor = ManifestAnchor("inputs/files.sha256", sha256_bytes(lines), "inputs/")
            manifest = load_authenticated_manifest(root, anchor)
            with self.assertRaises(UnsafePathError):
                authenticate_manifest_entry(root, manifest, "inputs/link.json")


if __name__ == "__main__":
    unittest.main()

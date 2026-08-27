from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import unittest


CANDIDATE_ROOT = Path(__file__).resolve().parents[1]
IMPLEMENTATION_ROOT = CANDIDATE_ROOT / "implementation"
sys.path.insert(0, str(IMPLEMENTATION_ROOT))

from s0_external_artifact_authority_acquisition import canonical, metadata, pins
from s0_external_artifact_authority_acquisition.errors import AuthorityError


EXPECTED_SOURCE_HASHES = {
    "__init__.py": "d96b293c7e93f319fb90547251b4c8044fb7c2f131061a7ab7c09befcfd28ced",
    "_issuance.py": "a93f9bb961715d61ca9c6545e30b3126b017e8edbf60246ab7a7c206ce7dcf32",
    "errors.py": "3792fd5467e39b18dcc58bb063e6075c422c8f6b2d7d061c1c537cd6ea6c1221",
    "canonical.py": "bc783bffc11a6394748468729066b1866f68eacfd19bbb0590363e0058b55fea",
    "pins.py": "63b205b3643b93f136bcc62a3b5e057baa8a3a4137b4c7810df86cde3b66e55d",
    "metadata.py": "d9c5276da4169d880f9388c515ce1f2bdd62670b1d7f6edce5973b000eb04221",
    "wheel.py": "c17676c51e17d5f369263bca0991d9ab5336fa7062a6ae599aedb6aa6ef4fc37",
    "buildtools.py": "4cd204b2b032929dfb9a7a524bfdee3f077d2aaa337768c00bcbad1b2d513fef",
    "candidate.py": "380471c778a43fded2037260bb5186e5df94a3a54e3f2b2a9551b165371e617d",
}


class AuthorityAcquisitionTests(unittest.TestCase):
    def test_exact_code_hashes(self) -> None:
        source_root = IMPLEMENTATION_ROOT / "s0_external_artifact_authority_acquisition"
        actual = {
            name: hashlib.sha256((source_root / name).read_bytes()).hexdigest()
            for name in EXPECTED_SOURCE_HASHES
        }
        self.assertEqual(actual, EXPECTED_SOURCE_HASHES)

    def test_strict_json_rejects_duplicate_bom_and_noncanonical_numbers(self) -> None:
        rejected = (
            b'{"a":1,"a":2}',
            b'\xef\xbb\xbf{"a":1}',
            b'{"a":1.0}',
            b'{"a":NaN}',
            b'{"a":9007199254740992}',
            b'\xff',
        )
        for raw in rejected:
            with self.subTest(raw=raw), self.assertRaises(AuthorityError):
                canonical.strict_json_object(raw, label="test", maximum_size=1024)

    def test_exported_pin_views_cannot_mint_changed_authority(self) -> None:
        cases = (
            (pins.SOURCE_PINS, pins.resolve_source_snapshot),
            (pins.ARTIFACT_PINS, pins.resolve_artifact_snapshot),
            (pins.WHEEL_PINS, pins.resolve_wheel_snapshot),
        )
        for views, resolver in cases:
            view = next(iter(views.values()))
            fields = tuple(view.__dataclass_fields__)
            originals = {field: getattr(view, field) for field in fields}
            for field in fields:
                value = originals[field]
                if type(value) is str:
                    replacement = value + "-attacker"
                elif type(value) is int:
                    replacement = value + 1
                elif type(value) is bool:
                    replacement = not value
                elif type(value) is tuple:
                    replacement = value + ("attacker",)
                else:
                    self.fail(f"unhandled frozen field type: {field}={type(value)!r}")
                try:
                    object.__setattr__(view, field, replacement)
                    with self.subTest(type=type(view).__name__, field=field):
                        with self.assertRaises(AuthorityError):
                            resolver(view)
                finally:
                    object.__setattr__(view, field, value)
            self.assertEqual(
                tuple(getattr(view, field) for field in fields),
                tuple(originals[field] for field in fields),
            )

    def test_clones_subclasses_proxies_and_exported_map_rebinding_do_not_mint_rows(self) -> None:
        view = next(iter(pins.SOURCE_PINS.values()))
        clone = pins.SourcePin(**{field: getattr(view, field) for field in view.__dataclass_fields__})
        self.assertEqual(pins.resolve_source_snapshot(clone), pins.resolve_source_snapshot(view))

        class SourcePinSubclass(pins.SourcePin):
            pass

        subclass = SourcePinSubclass(
            **{field: getattr(view, field) for field in view.__dataclass_fields__}
        )
        with self.assertRaises(AuthorityError):
            pins.resolve_source_snapshot(subclass)

        class Proxy:
            def __getattr__(self, name: str):
                return getattr(view, name)

        with self.assertRaises(AuthorityError):
            pins.resolve_source_snapshot(Proxy())

        original_export = pins.SOURCE_PINS
        try:
            pins.SOURCE_PINS = {"attacker": clone}
            with self.assertRaises(AuthorityError):
                pins.resolve_source_snapshot("attacker")
            self.assertEqual(pins.resolve_source_snapshot(view)[0], view.source_id)
        finally:
            pins.SOURCE_PINS = original_export

    def test_pypi_metadata_rejects_module_global_hash_rebinding(self) -> None:
        pin = pins.resolve_wheel_snapshot("attrs-26.1.0-py3-none-any")
        source = pins.resolve_source_snapshot(pin[7])
        document = {
            "info": {
                "name": pin[1],
                "requires_dist": list(pin[11]),
                "requires_python": pin[8],
                "version": pin[2],
            },
            "urls": [
                {
                    "digests": {"sha256": pin[5]},
                    "filename": pin[3],
                    "packagetype": "bdist_wheel",
                    "size": pin[6],
                    "url": pin[4],
                    "yanked": False,
                }
            ],
        }
        raw = json.dumps(document, separators=(",", ":")).encode("utf-8")
        self.assertLess(len(raw), source[3])
        raw += b" " * (source[3] - len(raw))
        self.assertNotEqual(hashlib.sha256(raw).hexdigest(), source[2])
        original = metadata.sha256_hex
        try:
            metadata.sha256_hex = lambda _raw: source[2]
            with self.assertRaises(AuthorityError):
                metadata.validate_pypi_metadata(pin[0], raw)
        finally:
            metadata.sha256_hex = original


if __name__ == "__main__":
    unittest.main(verbosity=2)

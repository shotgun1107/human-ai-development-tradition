from __future__ import annotations

import base64
import hashlib
import io
from pathlib import Path
import stat
import sys
import unittest
import zipfile


CANDIDATE_ROOT = Path(__file__).resolve().parents[1]
IMPLEMENTATION_ROOT = CANDIDATE_ROOT / "implementation"
sys.path.insert(0, str(IMPLEMENTATION_ROOT))

from s0_external_artifact_authority_acquisition.errors import AuthorityError
from s0_external_artifact_authority_acquisition import pins, wheel
from s0_external_artifact_authority_acquisition.canonical import canonical_json_lf


def _record_digest(raw: bytes) -> str:
    return base64.urlsafe_b64encode(hashlib.sha256(raw).digest()).decode("ascii").rstrip("=")


def _build_synthetic_wheel(
    *,
    project: str = "attacker",
    version: str = "1.0",
    requires_python: str = ">=3.12",
    dist_info: str = "attacker-1.0.dist-info",
    tag: str = "py3-none-any",
    requires_dist: tuple[str, ...] = (),
    purelib: bool = True,
    record_digest_override: str | None = None,
    target_size: int | None = None,
) -> bytes:
    payloads = {
        f"{project.replace('-', '_')}.py": b"VALUE = 1\n",
        "padding.bin": b"P" * 2048,
        f"{dist_info}/METADATA": (
            b"Metadata-Version: 2.1\n"
            + f"Name: {project}\n".encode("ascii")
            + f"Version: {version}\n".encode("ascii")
            + f"Requires-Python: {requires_python}\n".encode("ascii")
            + b"".join(
                f"Requires-Dist: {item}\n".encode("ascii")
                for item in requires_dist
            )
            + b"\n"
        ),
        f"{dist_info}/WHEEL": (
            b"Wheel-Version: 1.0\n"
            b"Generator: bounded-test\n"
            + f"Root-Is-Purelib: {'true' if purelib else 'false'}\n".encode("ascii")
            + f"Tag: {tag}\n\n".encode("ascii")
        ),
    }
    record_name = f"{dist_info}/RECORD"
    record_rows = [
        f"{name},sha256={record_digest_override or _record_digest(raw)},{len(raw)}\n"
        for name, raw in payloads.items()
    ]
    record_rows.append(f"{record_name},,\n")
    payloads[record_name] = "".join(record_rows).encode("utf-8")

    def render(comment: bytes) -> bytes:
        output = io.BytesIO()
        with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as archive:
            archive.comment = comment
            for name, raw in payloads.items():
                info = zipfile.ZipInfo(name, (2026, 1, 1, 0, 0, 0))
                info.create_system = 3
                info.compress_type = zipfile.ZIP_STORED
                info.external_attr = (stat.S_IFREG | 0o644) << 16
                archive.writestr(info, raw)
        return output.getvalue()

    rendered = render(b"")
    if target_size is None:
        return rendered
    comment_size = target_size - len(rendered)
    if not 0 <= comment_size <= 65535:
        raise AssertionError(
            f"synthetic wheel target cannot be reached: base={len(rendered)} target={target_size}"
        )
    rendered = render(b"C" * comment_size)
    if len(rendered) != target_size:
        raise AssertionError(f"synthetic wheel size mismatch: {len(rendered)} != {target_size}")
    return rendered


def _synthetic_wheel() -> bytes:
    return _build_synthetic_wheel()


class WheelAuthorityBindingTests(unittest.TestCase):
    def test_dual_inventory_canonical_hashes_are_exact(self) -> None:
        expected = {
            "jsonschema-4.26.0-py3-none-any": (
                "072c7bf9a4b395abd9a4f895549530b13a9e52b516458da517edcc2fdff3b249",
                "1cfb710b06ae7817c916f17462e9dad47918a9f54d7c15c54091fcb8c11170bc",
            ),
            "referencing-0.37.0-py3-none-any": (
                "9549d620e143164d5986d9721943efad38d9b9c5f941048da30854d35adbd768",
                "dc0e8b9496f3598aa78554d637314c9c7fb7eeeb6621a0cb0a638d7764f376fb",
            ),
        }
        for pin_id, hashes in expected.items():
            pin = pins.resolve_wheel_snapshot(pin_id)
            observed = (
                hashlib.sha256(canonical_json_lf(list(pin[11]))).hexdigest(),
                hashlib.sha256(canonical_json_lf(list(pin[12]))).hexdigest(),
            )
            with self.subTest(pin_id=pin_id):
                self.assertEqual(observed, hashes)

    def test_all_six_exact_wheel_inventories_accept(self) -> None:
        rows = {}
        raws = {}
        for pin_id in pins.WHEEL_PIN_IDS:
            pin = pins.resolve_wheel_snapshot(pin_id)
            raw = _build_synthetic_wheel(
                project=pin[1],
                version=pin[2],
                requires_python=pin[8],
                dist_info=pin[10],
                tag=pin[9],
                requires_dist=pin[12],
                purelib=pin[13],
            )
            row = list(pin)
            row[5] = hashlib.sha256(raw).hexdigest()
            row[6] = len(raw)
            rows[pin_id] = tuple(row)
            raws[pin_id] = raw

        validate = wheel._freeze_wheel_validator(lambda value: rows[value])
        for pin_id in pins.WHEEL_PIN_IDS:
            evidence = validate(pin_id, raws[pin_id])
            pin = pins.resolve_wheel_snapshot(pin_id)
            with self.subTest(pin_id=pin_id):
                self.assertEqual(evidence.requires_dist, pin[11])
                self.assertEqual(evidence.wheel_requires_dist, pin[12])
                self.assertIs(evidence.imported, False)
                self.assertIs(evidence.installed, False)

    def test_cross_representation_and_swapped_inventories_reject(self) -> None:
        jsonschema = pins.resolve_wheel_snapshot("jsonschema-4.26.0-py3-none-any")
        referencing = pins.resolve_wheel_snapshot("referencing-0.37.0-py3-none-any")
        cases = (
            (jsonschema, jsonschema[11], "jsonschema-cross-representation"),
            (referencing, referencing[11], "referencing-cross-representation"),
            (jsonschema, referencing[12], "jsonschema-swapped"),
            (referencing, jsonschema[12], "referencing-swapped"),
        )
        for pin, observed_inventory, label in cases:
            raw = _build_synthetic_wheel(
                project=pin[1],
                version=pin[2],
                requires_python=pin[8],
                dist_info=pin[10],
                tag=pin[9],
                requires_dist=observed_inventory,
                purelib=pin[13],
            )
            row = list(pin)
            row[5] = hashlib.sha256(raw).hexdigest()
            row[6] = len(raw)
            validate = wheel._freeze_wheel_validator(
                lambda _value, row=tuple(row): row
            )
            with self.subTest(case=label), self.assertRaisesRegex(
                AuthorityError, "wheel_metadata_requires_dist_inventory_mismatch"
            ):
                validate(pin[0], raw)

    def test_public_validator_rejects_module_global_resolver_rebinding(self) -> None:
        raw = _synthetic_wheel()
        attacker_row = (
            "attacker-1.0-py3-none-any",
            "attacker",
            "1.0",
            "attacker-1.0-py3-none-any.whl",
            "https://attacker.invalid/attacker-1.0-py3-none-any.whl",
            hashlib.sha256(raw).hexdigest(),
            len(raw),
            "attacker-metadata",
            ">=3.12",
            "py3-none-any",
            "attacker-1.0.dist-info",
            (),
            (),
            True,
        )
        original = wheel.resolve_wheel_snapshot
        try:
            wheel.resolve_wheel_snapshot = lambda _value: attacker_row
            with self.assertRaises(AuthorityError):
                wheel.validate_wheel("attacker-controlled-id", raw)
        finally:
            wheel.resolve_wheel_snapshot = original

    def test_public_validator_rejects_module_global_hash_rebinding(self) -> None:
        pinned_sha256 = "c647aa4a12dfbad9333ca4e71fe62ddc36f4e63b2d260a37a8b83d2f043ac309"
        raw = _build_synthetic_wheel(
            project="attrs",
            version="26.1.0",
            requires_python=">=3.9",
            dist_info="attrs-26.1.0.dist-info",
            tag="py3-none-any",
            record_digest_override=base64.urlsafe_b64encode(
                bytes.fromhex(pinned_sha256)
            ).decode("ascii").rstrip("="),
            target_size=67548,
        )
        self.assertNotEqual(hashlib.sha256(raw).hexdigest(), pinned_sha256)
        original = wheel.sha256_hex
        try:
            wheel.sha256_hex = lambda _raw: pinned_sha256
            with self.assertRaises(AuthorityError):
                wheel.validate_wheel("attrs-26.1.0-py3-none-any", raw)
        finally:
            wheel.sha256_hex = original


if __name__ == "__main__":
    unittest.main(verbosity=2)

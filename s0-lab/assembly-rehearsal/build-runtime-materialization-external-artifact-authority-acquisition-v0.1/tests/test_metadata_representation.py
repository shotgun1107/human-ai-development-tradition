from __future__ import annotations

import hashlib
from pathlib import Path
import sys
import unittest
import zlib


CANDIDATE_ROOT = Path(__file__).resolve().parents[1]
IMPLEMENTATION_ROOT = CANDIDATE_ROOT / "implementation"
sys.path.insert(0, str(IMPLEMENTATION_ROOT))

from s0_external_artifact_authority_acquisition import metadata, pins
from s0_external_artifact_authority_acquisition.errors import AuthorityError


DECODED_SHA256 = "6966370cecb61d5e29ed61264ffab8a0ebccaf77619e96e8646e112e5bdc5b61"
DECODED_SIZE = 48248
REPRESENTATION = "RAW-GZIP-TRANSFER-BYTES-TO-DECODED-ENTITY-BYTES"


def _gzip_member(raw: bytes) -> bytes:
    compressor = zlib.compressobj(level=9, wbits=16 + zlib.MAX_WBITS)
    return compressor.compress(raw) + compressor.flush()


def _decode(
    raw: bytes,
    *,
    maximum_size: int,
    expected_size: int,
    expected_sha256: str,
):
    return metadata._strict_gzip_decode(
        raw,
        decompressor_factory=zlib.decompressobj,
        gzip_wbits=16 + zlib.MAX_WBITS,
        decompression_error_type=zlib.error,
        hash_bytes=lambda value: hashlib.sha256(value).hexdigest(),
        maximum_size=maximum_size,
        expected_size=expected_size,
        expected_sha256=expected_sha256,
        error_type=AuthorityError,
    )


class MetadataRepresentationTests(unittest.TestCase):
    def test_frozen_representation_and_microsoft_source_pins(self) -> None:
        release = pins.resolve_source_snapshot("cpython-3.12.10-release-page")
        microsoft = pins.resolve_source_snapshot(
            "microsoft-vs-2022-release-history-17.14.39"
        )
        self.assertEqual(
            release,
            (
                "cpython-3.12.10-release-page",
                "https://www.python.org/downloads/release/python-31210/",
                "cc64f3159f7cbe565abe8b032439668b3cdbcd1768b1a08f7c7c79bcab881473",
                9943,
                1024 * 1024,
            ),
        )
        self.assertEqual(
            microsoft,
            (
                "microsoft-vs-2022-release-history-17.14.39",
                "https://learn.microsoft.com/en-us/visualstudio/releases/2022/release-history",
                "8ead78ae6b47e27b40beb10d387e038719703c2b8c194840ec7eeaad2b970401",
                287876,
                1024 * 1024,
            ),
        )
        self.assertNotEqual(microsoft[2], "973a3c4c1a75ddc11e2252a689eba1d964bbe9aa09b24fadabc73a5fb4074d6d")
        self.assertNotEqual(microsoft[3], 287499)

    def test_new_microsoft_snapshot_authenticates_and_old_snapshot_rejects(self) -> None:
        new_raw = b"N" * 287876
        new_snapshot = metadata._authenticate_source(
            "microsoft-vs-2022-release-history-17.14.39",
            new_raw,
            resolve_source=pins.resolve_source_snapshot,
            hash_bytes=lambda value: (
                "8ead78ae6b47e27b40beb10d387e038719703c2b8c194840ec7eeaad2b970401"
                if value is new_raw
                else hashlib.sha256(value).hexdigest()
            ),
            error_type=AuthorityError,
        )
        self.assertEqual(new_snapshot[2], "8ead78ae6b47e27b40beb10d387e038719703c2b8c194840ec7eeaad2b970401")
        self.assertEqual(new_snapshot[3], 287876)

        old_raw = b"O" * 287499
        with self.assertRaisesRegex(AuthorityError, "raw_size_mismatch"):
            metadata._authenticate_source(
                "microsoft-vs-2022-release-history-17.14.39",
                old_raw,
                resolve_source=pins.resolve_source_snapshot,
                hash_bytes=lambda _value: "973a3c4c1a75ddc11e2252a689eba1d964bbe9aa09b24fadabc73a5fb4074d6d",
                error_type=AuthorityError,
            )

    def test_strict_gzip_accepts_one_member_and_rejects_malformed_forms(self) -> None:
        decoded = (
            b"Python 3.12.10\n"
            b"python-3.12.10-embed-amd64.zip\n"
            b"https://www.python.org/ftp/python/3.12.10/python-3.12.10-embed-amd64.zip\n"
            b"https://www.python.org/ftp/python/3.12.10/python-3.12.10-embed-amd64.zip.sigstore\n"
            + b"D" * 4096
        )
        member = _gzip_member(decoded)
        digest = hashlib.sha256(decoded).hexdigest()
        self.assertEqual(
            _decode(
                member,
                maximum_size=1024 * 1024,
                expected_size=len(decoded),
                expected_sha256=digest,
            ),
            decoded,
        )

        with self.subTest(case="truncated"), self.assertRaisesRegex(
            AuthorityError, "gzip_not_eof|gzip_decode_failed"
        ):
            _decode(
                member[:-8],
                maximum_size=1024 * 1024,
                expected_size=len(decoded),
                expected_sha256=digest,
            )
        for label, malformed in (
            ("trailing", member + b"trailing"),
            ("concatenated", member + member),
        ):
            with self.subTest(case=label), self.assertRaisesRegex(
                AuthorityError, "trailing_or_concatenated_data"
            ):
                _decode(
                    malformed,
                    maximum_size=1024 * 1024,
                    expected_size=len(decoded),
                    expected_sha256=digest,
                )

        oversized = b"Z" * (1024 * 1024 + 1)
        with self.subTest(case="output_bound"), self.assertRaisesRegex(
            AuthorityError, "decoded_bound_exceeded"
        ):
            _decode(
                _gzip_member(oversized),
                maximum_size=1024 * 1024,
                expected_size=len(oversized),
                expected_sha256=hashlib.sha256(oversized).hexdigest(),
            )
        with self.subTest(case="wrong_size"), self.assertRaisesRegex(
            AuthorityError, "decoded_size_mismatch"
        ):
            _decode(
                member,
                maximum_size=1024 * 1024,
                expected_size=len(decoded) + 1,
                expected_sha256=digest,
            )
        with self.subTest(case="wrong_hash"), self.assertRaisesRegex(
            AuthorityError, "decoded_sha256_mismatch"
        ):
            _decode(
                member,
                maximum_size=1024 * 1024,
                expected_size=len(decoded),
                expected_sha256="0" * 64,
            )

    def test_frozen_decoder_and_hash_dependencies_resist_module_rebinding(self) -> None:
        literals = (
            b"Python 3.12.10\n"
            b"python-3.12.10-embed-amd64.zip\n"
            b"https://www.python.org/ftp/python/3.12.10/python-3.12.10-embed-amd64.zip\n"
            b"https://www.python.org/ftp/python/3.12.10/python-3.12.10-embed-amd64.zip.sigstore\n"
        )
        decoded = literals + b"P" * (DECODED_SIZE - len(literals))
        member = _gzip_member(decoded)

        def cpython_impl(
            release_page_raw: bytes,
            ftp_index_raw: bytes,
            sigstore_bundle_raw: bytes,
            **kwargs,
        ):
            decoded_entity = kwargs["decode_release_page"](release_page_raw)
            self.assertEqual(decoded_entity, decoded)
            evidence_type = kwargs["evidence_type"]
            return evidence_type(
                "cc64f3159f7cbe565abe8b032439668b3cdbcd1768b1a08f7c7c79bcab881473",
                9943,
                kwargs["release_representation"],
                kwargs["release_content_encoding"],
                kwargs["release_decoded_sha256"],
                kwargs["release_decoded_size"],
                "e6f937dbe22df020bcf8f2f3b251da05f0e4c9cdd4ceeea58b27cd528a562e58",
                8974,
                "8aa5b4e555fd8b73b3dfef2f04328739f52d30706655930dcdf6111603d015be",
                4915,
                "4acbed6dd1c744b0376e3b1cf57ce906f9dc9e95e68824584c8099a63025a3c3",
                11133606,
                "a60bd3cd635e7561d81b243fd1112091501fff894cffa400e2416eb2f7834eb3",
                717,
                72,
                1,
                pins.CPYTHON_SIGSTORE_POLICY_IDENTITY,
                pins.CPYTHON_SIGSTORE_OIDC_ISSUER,
                release_page_raw=release_page_raw,
                ftp_index_raw=ftp_index_raw,
                sigstore_bundle_raw=sigstore_bundle_raw,
            )

        originals = (
            metadata._validate_cpython_source_metadata_impl,
            metadata.sha256_hex,
        )
        try:
            metadata._validate_cpython_source_metadata_impl = cpython_impl
            metadata.sha256_hex = lambda value: (
                DECODED_SHA256 if value == decoded else hashlib.sha256(value).hexdigest()
            )
            (
                validate_cpython,
                _validate_microsoft,
                _validate_pypi,
                require_issued,
                _consume_issued,
                release_issued,
            ) = metadata._freeze_metadata_validators()
        finally:
            metadata._validate_cpython_source_metadata_impl, metadata.sha256_hex = originals

        original_decompressor = metadata.zlib.decompressobj
        original_hash = metadata.sha256_hex
        original_decoder = metadata._strict_gzip_decode
        try:
            metadata.zlib.decompressobj = lambda *_args, **_kwargs: (_ for _ in ()).throw(
                AssertionError("rebound decompressor used")
            )
            metadata.sha256_hex = lambda _value: "f" * 64
            metadata._strict_gzip_decode = lambda *_args, **_kwargs: (_ for _ in ()).throw(
                AssertionError("rebound decoder used")
            )
            evidence = validate_cpython(member, b"ftp", b"bundle")
        finally:
            metadata.zlib.decompressobj = original_decompressor
            metadata.sha256_hex = original_hash
            metadata._strict_gzip_decode = original_decoder

        self.assertIs(require_issued(evidence, "cpython"), evidence)
        self.assertEqual(evidence.release_page_representation, REPRESENTATION)
        self.assertEqual(evidence.release_page_content_encoding, "gzip")
        self.assertEqual(evidence.release_page_decoded_entity_size, DECODED_SIZE)
        self.assertEqual(evidence.release_page_decoded_entity_sha256, DECODED_SHA256)
        self.assertIs(evidence.release_page_decoder_authority_established, False)
        self.assertTrue(release_issued(evidence, "cpython"))


if __name__ == "__main__":
    unittest.main(verbosity=2)

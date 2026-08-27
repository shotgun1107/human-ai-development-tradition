"""Pinned source-metadata validation without network or cryptographic claims."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
import re
from typing import Mapping
import zlib

from ._issuance import make_bounded_issuance_registry
from .canonical import (
    canonical_json_lf,
    decode_base64,
    exact_list,
    exact_object,
    require_exact_bool,
    require_exact_int,
    require_exact_text,
    sha256_hex,
    strict_json_object,
)
from .errors import AuthorityError
from .pins import (
    CPYTHON_ARTIFACT_ID,
    CPYTHON_SIGSTORE_MEDIA_TYPE,
    CPYTHON_SIGSTORE_OIDC_ISSUER,
    CPYTHON_SIGSTORE_POLICY_IDENTITY,
    MAX_METADATA_BYTES,
    ArtifactSnapshot,
    SourceSnapshot,
    WheelPin,
    WheelSnapshot,
    resolve_artifact_snapshot,
    resolve_source_snapshot,
    resolve_wheel_snapshot,
)


_NORMALIZE_PROJECT = re.compile(r"[-_.]+")


@dataclass(frozen=True, slots=True, weakref_slot=True)
class CPythonSourceEvidence:
    release_page_sha256: str
    release_page_size: int
    release_page_representation: str
    release_page_content_encoding: str
    release_page_decoded_entity_sha256: str
    release_page_decoded_entity_size: int
    ftp_index_sha256: str
    ftp_index_size: int
    bundle_sha256: str
    bundle_size: int
    artifact_sha256: str
    artifact_size: int
    certificate_der_sha256: str
    certificate_der_size: int
    signature_size: int
    tlog_entry_count: int
    expected_identity: str
    expected_oidc_issuer: str
    release_page_decoder_authority_established: bool = False
    sigstore_cryptographic_verification: bool = False
    certificate_chain_verification: bool = False
    transparency_log_verification: bool = False
    signature_verification: bool = False
    release_page_raw: bytes = field(repr=False, default=b"")
    ftp_index_raw: bytes = field(repr=False, default=b"")
    sigstore_bundle_raw: bytes = field(repr=False, default=b"")

    def facts_raw(self) -> bytes:
        return canonical_json_lf(
            {
                "artifact_sha256": self.artifact_sha256,
                "artifact_size": self.artifact_size,
                "bundle_sha256": self.bundle_sha256,
                "bundle_size": self.bundle_size,
                "certificate_chain_verification": self.certificate_chain_verification,
                "certificate_der_sha256": self.certificate_der_sha256,
                "certificate_der_size": self.certificate_der_size,
                "expected_identity": self.expected_identity,
                "expected_oidc_issuer": self.expected_oidc_issuer,
                "ftp_index_sha256": self.ftp_index_sha256,
                "ftp_index_size": self.ftp_index_size,
                "release_page_sha256": self.release_page_sha256,
                "release_page_size": self.release_page_size,
                "release_page_representation": self.release_page_representation,
                "release_page_content_encoding": self.release_page_content_encoding,
                "release_page_decoded_entity_sha256": (
                    self.release_page_decoded_entity_sha256
                ),
                "release_page_decoded_entity_size": (
                    self.release_page_decoded_entity_size
                ),
                "release_page_decoder_authority_established": (
                    self.release_page_decoder_authority_established
                ),
                "signature_size": self.signature_size,
                "signature_verification": self.signature_verification,
                "sigstore_cryptographic_verification": self.sigstore_cryptographic_verification,
                "tlog_entry_count": self.tlog_entry_count,
                "transparency_log_verification": self.transparency_log_verification,
            }
        )


@dataclass(frozen=True, slots=True, weakref_slot=True)
class MicrosoftReleaseEvidence:
    source_id: str
    raw_sha256: str
    raw_size: int
    release: str
    build: str
    artifact_url: str
    artifact_sha256: str
    artifact_size: int
    authenticode_verified: bool = False
    raw: bytes = field(repr=False, default=b"")


@dataclass(frozen=True, slots=True, weakref_slot=True)
class PyPIMetadataEvidence:
    pin_id: str
    source_id: str
    raw_sha256: str
    raw_size: int
    project: str
    version: str
    requires_python: str
    requires_dist: tuple[str, ...]
    filename: str
    url: str
    wheel_sha256: str
    wheel_size: int
    yanked: bool
    raw: bytes = field(repr=False, default=b"")


def _authenticate_source(
    source_id: str,
    raw: bytes,
    *,
    resolve_source,
    hash_bytes,
    error_type,
) -> SourceSnapshot:
    row = resolve_source(source_id)
    if type(raw) is not bytes:
        raise error_type(f"{source_id}_raw_not_exact_bytes")
    if len(raw) > row[4]:
        raise error_type(f"{source_id}_raw_bound_exceeded")
    if len(raw) != row[3]:
        raise error_type(f"{source_id}_raw_size_mismatch")
    if hash_bytes(raw) != row[2]:
        raise error_type(f"{source_id}_raw_sha256_mismatch")
    return row


def _require_literals(
    raw: bytes,
    literals: tuple[str, ...],
    *,
    label: str,
    error_type,
) -> None:
    for index, literal in enumerate(literals):
        encoded = literal.encode("utf-8", "strict")
        if encoded not in raw:
            raise error_type(f"{label}_required_literal_{index}_missing")


def _strict_gzip_decode(
    raw: bytes,
    *,
    decompressor_factory,
    gzip_wbits: int,
    decompression_error_type,
    hash_bytes,
    maximum_size: int,
    expected_size: int,
    expected_sha256: str,
    error_type,
) -> bytes:
    if type(raw) is not bytes or not raw.startswith(b"\x1f\x8b\x08"):
        raise error_type("cpython_release_transfer_not_gzip")
    try:
        decompressor = decompressor_factory(gzip_wbits)
        decoded = decompressor.decompress(raw, maximum_size + 1)
        if len(decoded) > maximum_size or decompressor.unconsumed_tail:
            raise error_type("cpython_release_decoded_bound_exceeded")
        decoded += decompressor.flush(maximum_size - len(decoded) + 1)
    except error_type:
        raise
    except decompression_error_type as exc:
        raise error_type("cpython_release_gzip_decode_failed") from exc
    if len(decoded) > maximum_size:
        raise error_type("cpython_release_decoded_bound_exceeded")
    if not decompressor.eof:
        raise error_type("cpython_release_gzip_not_eof")
    if decompressor.unused_data or decompressor.unconsumed_tail:
        raise error_type("cpython_release_gzip_trailing_or_concatenated_data")
    if len(decoded) != expected_size:
        raise error_type("cpython_release_decoded_size_mismatch")
    if hash_bytes(decoded) != expected_sha256:
        raise error_type("cpython_release_decoded_sha256_mismatch")
    return decoded


def _validate_cpython_source_metadata_impl(
    release_page_raw: bytes,
    ftp_index_raw: bytes,
    sigstore_bundle_raw: bytes,
    *,
    authenticate_source,
    resolve_source,
    hash_bytes,
    error_type,
    resolve_artifact,
    artifact_id,
    require_literals,
    parse_json,
    exact_object_validator,
    decode_base64_value,
    exact_list_validator,
    max_metadata_bytes,
    sigstore_media_type,
    policy_identity,
    oidc_issuer,
    evidence_type,
    decode_release_page,
    release_representation,
    release_content_encoding,
    release_decoded_sha256,
    release_decoded_size,
) -> CPythonSourceEvidence:
    """Validate pinned page/index/bundle structure; do no Sigstore crypto."""

    release = authenticate_source(
        "cpython-3.12.10-release-page",
        release_page_raw,
        resolve_source=resolve_source,
        hash_bytes=hash_bytes,
        error_type=error_type,
    )
    index = authenticate_source(
        "cpython-3.12.10-ftp-index",
        ftp_index_raw,
        resolve_source=resolve_source,
        hash_bytes=hash_bytes,
        error_type=error_type,
    )
    bundle_pin = authenticate_source(
        "cpython-3.12.10-embed-amd64-sigstore-bundle",
        sigstore_bundle_raw,
        resolve_source=resolve_source,
        hash_bytes=hash_bytes,
        error_type=error_type,
    )
    release_entity = decode_release_page(release_page_raw)
    artifact: ArtifactSnapshot = resolve_artifact(artifact_id)
    require_literals(
        release_entity,
        (
            "Python 3.12.10",
            artifact[1],
            artifact[2],
            bundle_pin[1],
        ),
        label="cpython_release_page",
        error_type=error_type,
    )
    require_literals(
        ftp_index_raw,
        (artifact[1], str(artifact[4]), "python-3.12.10-embed-amd64.zip.sigstore", str(bundle_pin[3])),
        label="cpython_ftp_index",
        error_type=error_type,
    )
    bundle = parse_json(
        sigstore_bundle_raw,
        label="cpython_sigstore_bundle",
        maximum_size=max_metadata_bytes,
    )
    if bundle.get("mediaType") != sigstore_media_type:
        raise error_type("cpython_sigstore_media_type_mismatch")
    signature = exact_object_validator(bundle.get("messageSignature"), label="sigstore_message_signature")
    digest = exact_object_validator(signature.get("messageDigest"), label="sigstore_message_digest")
    if digest.get("algorithm") != "SHA2_256":
        raise error_type("cpython_sigstore_digest_algorithm_mismatch")
    digest_bytes = decode_base64_value(digest.get("digest"), label="sigstore_digest", maximum_size=32)
    if len(digest_bytes) != 32 or digest_bytes.hex() != artifact[3]:
        raise error_type("cpython_sigstore_artifact_digest_mismatch")
    signature_bytes = decode_base64_value(
        signature.get("signature"), label="sigstore_signature", maximum_size=72
    )
    if len(signature_bytes) != 72:
        raise error_type("cpython_sigstore_signature_size_mismatch")
    material = exact_object_validator(
        bundle.get("verificationMaterial"), label="sigstore_verification_material"
    )
    certificate = exact_object_validator(material.get("certificate"), label="sigstore_certificate")
    certificate_der = decode_base64_value(
        certificate.get("rawBytes"), label="sigstore_certificate_der", maximum_size=717
    )
    if len(certificate_der) != 717:
        raise error_type("cpython_sigstore_certificate_size_mismatch")
    certificate_sha = hash_bytes(certificate_der)
    if certificate_sha != "a60bd3cd635e7561d81b243fd1112091501fff894cffa400e2416eb2f7834eb3":
        raise error_type("cpython_sigstore_certificate_sha256_mismatch")
    tlog_entries = exact_list_validator(material.get("tlogEntries"), label="sigstore_tlog_entries")
    if len(tlog_entries) != 1 or type(tlog_entries[0]) is not dict:
        raise error_type("cpython_sigstore_tlog_entry_count_mismatch")
    return evidence_type(
        release[2],
        release[3],
        release_representation,
        release_content_encoding,
        release_decoded_sha256,
        release_decoded_size,
        index[2],
        index[3],
        bundle_pin[2],
        bundle_pin[3],
        artifact[3],
        artifact[4],
        certificate_sha,
        len(certificate_der),
        len(signature_bytes),
        1,
        policy_identity,
        oidc_issuer,
        release_page_raw=release_page_raw,
        ftp_index_raw=ftp_index_raw,
        sigstore_bundle_raw=sigstore_bundle_raw,
    )


def _validate_microsoft_release_metadata_impl(
    release_history_raw: bytes,
    *,
    authenticate_source,
    resolve_source,
    hash_bytes,
    error_type,
    resolve_artifact,
    require_literals,
    evidence_type,
) -> MicrosoftReleaseEvidence:
    source = authenticate_source(
        "microsoft-vs-2022-release-history-17.14.39",
        release_history_raw,
        resolve_source=resolve_source,
        hash_bytes=hash_bytes,
        error_type=error_type,
    )
    artifact = resolve_artifact("vs-build-tools-17.14.39-17.14.37614.0")
    require_literals(
        release_history_raw,
        ("17.14.39", "17.14.37614.0", "Build Tools", artifact[2]),
        label="microsoft_release_history",
        error_type=error_type,
    )
    return evidence_type(
        source[0],
        source[2],
        source[3],
        "17.14.39",
        "17.14.37614.0",
        artifact[2],
        artifact[3],
        artifact[4],
        raw=release_history_raw,
    )


def _canonical_project(value: object, *, label: str, require_text, normalizer) -> str:
    text = require_text(value, label=label, maximum_length=160)
    return normalizer.sub("-", text).lower()


def _validate_pypi_metadata_impl(
    pin_or_id: str | WheelPin,
    raw_json: bytes,
    *,
    resolve_wheel,
    authenticate_source,
    resolve_source,
    hash_bytes,
    error_type,
    parse_json,
    exact_object_validator,
    canonical_project,
    require_text,
    normalizer,
    exact_list_validator,
    require_int,
    require_bool,
    max_metadata_bytes,
    evidence_type,
) -> PyPIMetadataEvidence:
    pin: WheelSnapshot = resolve_wheel(pin_or_id)
    source = authenticate_source(
        pin[7],
        raw_json,
        resolve_source=resolve_source,
        hash_bytes=hash_bytes,
        error_type=error_type,
    )
    root = parse_json(raw_json, label="pypi_metadata", maximum_size=max_metadata_bytes)
    info = exact_object_validator(root.get("info"), label="pypi_info")
    if canonical_project(
        info.get("name"),
        label="pypi_name",
        require_text=require_text,
        normalizer=normalizer,
    ) != pin[1]:
        raise error_type("pypi_project_name_mismatch")
    if require_text(info.get("version"), label="pypi_version") != pin[2]:
        raise error_type("pypi_version_mismatch")
    if info.get("requires_python") != pin[8]:
        raise error_type("pypi_requires_python_mismatch")
    raw_dependencies = info.get("requires_dist")
    if raw_dependencies is None:
        dependencies: tuple[str, ...] = ()
    else:
        dependencies = tuple(
            require_text(item, label="pypi_requires_dist", maximum_length=1024)
            for item in exact_list_validator(raw_dependencies, label="pypi_requires_dist")
        )
    if dependencies != pin[11]:
        raise error_type("pypi_requires_dist_inventory_mismatch")
    candidates = []
    for entry in exact_list_validator(root.get("urls"), label="pypi_urls"):
        item = exact_object_validator(entry, label="pypi_url_entry")
        if item.get("filename") == pin[3]:
            candidates.append(item)
    if len(candidates) != 1:
        raise error_type("pypi_wheel_url_cardinality_mismatch")
    selected = candidates[0]
    digests = exact_object_validator(selected.get("digests"), label="pypi_wheel_digests")
    if (
        selected.get("url") != pin[4]
        or digests.get("sha256") != pin[5]
        or require_int(
            selected.get("size"), label="pypi_wheel_size", minimum=1, maximum=max_metadata_bytes
        )
        != pin[6]
        or selected.get("packagetype") != "bdist_wheel"
        or require_bool(selected.get("yanked"), label="pypi_yanked") is not False
    ):
        raise error_type("pypi_wheel_selected_fields_mismatch")
    return evidence_type(
        pin[0],
        source[0],
        source[2],
        source[3],
        pin[1],
        pin[2],
        pin[8],
        pin[11],
        pin[3],
        pin[4],
        pin[5],
        pin[6],
        False,
        raw=raw_json,
    )


def _freeze_metadata_validators():
    """Capture every authority-relevant helper before module-name rebinding."""

    cpython_impl = _validate_cpython_source_metadata_impl
    microsoft_impl = _validate_microsoft_release_metadata_impl
    pypi_impl = _validate_pypi_metadata_impl
    frozen_authenticate_source = _authenticate_source
    frozen_resolve_source = resolve_source_snapshot
    frozen_resolve_artifact = resolve_artifact_snapshot
    frozen_resolve_wheel = resolve_wheel_snapshot
    frozen_hash_bytes = sha256_hex
    frozen_error_type = AuthorityError
    frozen_require_literals = _require_literals
    frozen_parse_json = strict_json_object
    frozen_exact_object = exact_object
    frozen_decode_base64 = decode_base64
    frozen_exact_list = exact_list
    frozen_require_text = require_exact_text
    frozen_require_int = require_exact_int
    frozen_require_bool = require_exact_bool
    frozen_canonical_project = _canonical_project
    frozen_normalizer = _NORMALIZE_PROJECT
    frozen_max_metadata_bytes = MAX_METADATA_BYTES
    frozen_artifact_id = CPYTHON_ARTIFACT_ID
    frozen_sigstore_media_type = CPYTHON_SIGSTORE_MEDIA_TYPE
    frozen_policy_identity = CPYTHON_SIGSTORE_POLICY_IDENTITY
    frozen_oidc_issuer = CPYTHON_SIGSTORE_OIDC_ISSUER
    frozen_cpython_evidence_type = CPythonSourceEvidence
    frozen_microsoft_evidence_type = MicrosoftReleaseEvidence
    frozen_pypi_evidence_type = PyPIMetadataEvidence
    frozen_strict_gzip_decode = _strict_gzip_decode
    frozen_decompressor_factory = zlib.decompressobj
    frozen_gzip_wbits = 16 + zlib.MAX_WBITS
    frozen_decompression_error_type = zlib.error
    frozen_release_representation = (
        "RAW-GZIP-TRANSFER-BYTES-TO-DECODED-ENTITY-BYTES"
    )
    frozen_release_content_encoding = "gzip"
    frozen_release_decoded_sha256 = (
        "6966370cecb61d5e29ed61264ffab8a0ebccaf77619e96e8646e112e5bdc5b61"
    )
    frozen_release_decoded_size = 48248
    frozen_object_id = id
    frozen_materialize = replace
    frozen_type = type
    frozen_getattribute = object.__getattribute__

    def decode_release_page(raw: bytes) -> bytes:
        return frozen_strict_gzip_decode(
            raw,
            decompressor_factory=frozen_decompressor_factory,
            gzip_wbits=frozen_gzip_wbits,
            decompression_error_type=frozen_decompression_error_type,
            hash_bytes=frozen_hash_bytes,
            maximum_size=frozen_max_metadata_bytes,
            expected_size=frozen_release_decoded_size,
            expected_sha256=frozen_release_decoded_sha256,
            error_type=frozen_error_type,
        )

    def snapshot(value: object) -> tuple[object, ...]:
        if frozen_type(value) is frozen_cpython_evidence_type:
            return (
                "cpython",
                frozen_getattribute(value, "release_page_sha256"),
                frozen_getattribute(value, "release_page_size"),
                frozen_getattribute(value, "release_page_representation"),
                frozen_getattribute(value, "release_page_content_encoding"),
                frozen_getattribute(
                    value, "release_page_decoded_entity_sha256"
                ),
                frozen_getattribute(
                    value, "release_page_decoded_entity_size"
                ),
                frozen_getattribute(value, "ftp_index_sha256"),
                frozen_getattribute(value, "ftp_index_size"),
                frozen_getattribute(value, "bundle_sha256"),
                frozen_getattribute(value, "bundle_size"),
                frozen_getattribute(value, "artifact_sha256"),
                frozen_getattribute(value, "artifact_size"),
                frozen_getattribute(value, "certificate_der_sha256"),
                frozen_getattribute(value, "certificate_der_size"),
                frozen_getattribute(value, "signature_size"),
                frozen_getattribute(value, "tlog_entry_count"),
                frozen_getattribute(value, "expected_identity"),
                frozen_getattribute(value, "expected_oidc_issuer"),
                frozen_getattribute(
                    value, "release_page_decoder_authority_established"
                ),
                frozen_getattribute(
                    value, "sigstore_cryptographic_verification"
                ),
                frozen_getattribute(value, "certificate_chain_verification"),
                frozen_getattribute(value, "transparency_log_verification"),
                frozen_getattribute(value, "signature_verification"),
                frozen_object_id(frozen_getattribute(value, "release_page_raw")),
                frozen_object_id(frozen_getattribute(value, "ftp_index_raw")),
                frozen_object_id(
                    frozen_getattribute(value, "sigstore_bundle_raw")
                ),
            )
        if frozen_type(value) is frozen_microsoft_evidence_type:
            return (
                "microsoft",
                frozen_getattribute(value, "source_id"),
                frozen_getattribute(value, "raw_sha256"),
                frozen_getattribute(value, "raw_size"),
                frozen_getattribute(value, "release"),
                frozen_getattribute(value, "build"),
                frozen_getattribute(value, "artifact_url"),
                frozen_getattribute(value, "artifact_sha256"),
                frozen_getattribute(value, "artifact_size"),
                frozen_getattribute(value, "authenticode_verified"),
                frozen_object_id(frozen_getattribute(value, "raw")),
            )
        if frozen_type(value) is frozen_pypi_evidence_type:
            return (
                "pypi",
                frozen_getattribute(value, "pin_id"),
                frozen_getattribute(value, "source_id"),
                frozen_getattribute(value, "raw_sha256"),
                frozen_getattribute(value, "raw_size"),
                frozen_getattribute(value, "project"),
                frozen_getattribute(value, "version"),
                frozen_getattribute(value, "requires_python"),
                frozen_getattribute(value, "requires_dist"),
                frozen_getattribute(value, "filename"),
                frozen_getattribute(value, "url"),
                frozen_getattribute(value, "wheel_sha256"),
                frozen_getattribute(value, "wheel_size"),
                frozen_getattribute(value, "yanked"),
                frozen_object_id(frozen_getattribute(value, "raw")),
            )
        raise frozen_error_type("metadata_evidence_type_not_issued")

    issue, require_issued, consume_issued, release_issued = (
        make_bounded_issuance_registry(
            limits={"cpython": 1, "microsoft": 1, "pypi": 6},
            snapshot=snapshot,
            materialize=frozen_materialize,
            error_type=frozen_error_type,
            capacity_error="metadata_evidence_registry_capacity_exceeded",
            invalid_kind_error="metadata_evidence_kind_invalid",
            not_issued_error="metadata_evidence_not_issued_or_changed",
        )
    )

    def validate_cpython_source_metadata(
        release_page_raw: bytes,
        ftp_index_raw: bytes,
        sigstore_bundle_raw: bytes,
    ) -> CPythonSourceEvidence:
        return issue(cpython_impl(
            release_page_raw,
            ftp_index_raw,
            sigstore_bundle_raw,
            authenticate_source=frozen_authenticate_source,
            resolve_source=frozen_resolve_source,
            hash_bytes=frozen_hash_bytes,
            error_type=frozen_error_type,
            resolve_artifact=frozen_resolve_artifact,
            artifact_id=frozen_artifact_id,
            require_literals=frozen_require_literals,
            parse_json=frozen_parse_json,
            exact_object_validator=frozen_exact_object,
            decode_base64_value=frozen_decode_base64,
            exact_list_validator=frozen_exact_list,
            max_metadata_bytes=frozen_max_metadata_bytes,
            sigstore_media_type=frozen_sigstore_media_type,
            policy_identity=frozen_policy_identity,
            oidc_issuer=frozen_oidc_issuer,
            evidence_type=frozen_cpython_evidence_type,
            decode_release_page=decode_release_page,
            release_representation=frozen_release_representation,
            release_content_encoding=frozen_release_content_encoding,
            release_decoded_sha256=frozen_release_decoded_sha256,
            release_decoded_size=frozen_release_decoded_size,
        ), "cpython")

    def validate_microsoft_release_metadata(
        release_history_raw: bytes,
    ) -> MicrosoftReleaseEvidence:
        return issue(microsoft_impl(
            release_history_raw,
            authenticate_source=frozen_authenticate_source,
            resolve_source=frozen_resolve_source,
            hash_bytes=frozen_hash_bytes,
            error_type=frozen_error_type,
            resolve_artifact=frozen_resolve_artifact,
            require_literals=frozen_require_literals,
            evidence_type=frozen_microsoft_evidence_type,
        ), "microsoft")

    def validate_pypi_metadata(
        pin_or_id: str | WheelPin,
        raw_json: bytes,
    ) -> PyPIMetadataEvidence:
        return issue(pypi_impl(
            pin_or_id,
            raw_json,
            resolve_wheel=frozen_resolve_wheel,
            authenticate_source=frozen_authenticate_source,
            resolve_source=frozen_resolve_source,
            hash_bytes=frozen_hash_bytes,
            error_type=frozen_error_type,
            parse_json=frozen_parse_json,
            exact_object_validator=frozen_exact_object,
            canonical_project=frozen_canonical_project,
            require_text=frozen_require_text,
            normalizer=frozen_normalizer,
            exact_list_validator=frozen_exact_list,
            require_int=frozen_require_int,
            require_bool=frozen_require_bool,
            max_metadata_bytes=frozen_max_metadata_bytes,
            evidence_type=frozen_pypi_evidence_type,
        ), "pypi")

    return (
        validate_cpython_source_metadata,
        validate_microsoft_release_metadata,
        validate_pypi_metadata,
        require_issued,
        consume_issued,
        release_issued,
    )


(
    validate_cpython_source_metadata,
    validate_microsoft_release_metadata,
    validate_pypi_metadata,
    _require_issued_metadata_evidence,
    _consume_issued_metadata_evidence,
    _release_issued_metadata_evidence,
) = _freeze_metadata_validators()


__all__ = [
    "CPythonSourceEvidence",
    "MicrosoftReleaseEvidence",
    "PyPIMetadataEvidence",
    "validate_cpython_source_metadata",
    "validate_microsoft_release_metadata",
    "validate_pypi_metadata",
]

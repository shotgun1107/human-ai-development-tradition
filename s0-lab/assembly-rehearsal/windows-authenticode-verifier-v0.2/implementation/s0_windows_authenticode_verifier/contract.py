"""Exact v0.2 verifier contract; no certificate or algorithm identity pins."""

from __future__ import annotations

FIXED_BOOTSTRAPPER_URL = (
    "https://download.visualstudio.microsoft.com/download/pr/"
    "fa619120-9c0e-47e6-bfe0-3ee96fb671b2/"
    "236367b68ba9a51708263ab10a1c85546cc4a8eca78b365168811d19c4fb2f29/"
    "vs_BuildTools.exe"
)

ACQUISITION_SCHEMA_ID = "S0-PUBLIC-WINDOWS-AUTHENTICODE-ACQUISITION-RECORD-2"
OBSERVATION_SCHEMA_ID = "S0-PUBLIC-WINDOWS-AUTHENTICODE-NATIVE-OBSERVATION-2"
TRACE_SCHEMA_ID = "S0-PUBLIC-WINDOWS-AUTHENTICODE-SEMANTIC-TRACE-2"
DECISION_SCHEMA_ID = "S0-PUBLIC-WINDOWS-AUTHENTICODE-DECISION-2"
SUPPLIER_CRITERION_ID = "PROJECT-APPROVED-MICROSOFT-DISTRIBUTION-COMPOSITE-2"
RUNTIME_AUTHORITY_SCOPE = "TRUSTED-HOST-DISK-CONSISTENCY-ONLY"

ACQUISITION_HANDLE_CONTRACT = {
    "delete_share_allowed": False,
    "desired_access": "GENERIC_READ",
    "handle_inheritable": False,
    "share_mode": "FILE_SHARE_READ",
    "writable_mapping_created": False,
    "write_share_allowed": False,
}
IMMUTABLE_LEASE_CONTRACT = {
    "delete_sharing_denied": True,
    "desired_access": "GENERIC_READ",
    "handle_inheritable": False,
    "share_mode": "FILE_SHARE_READ",
    "write_sharing_denied": True,
}

# This remains an explicit project criterion. It is not represented as an
# official Microsoft leaf-publisher identity guarantee.
SUPPLIER_CRITERION_COMPONENTS = (
    "externally-pinned-acquisition-record-binds-fixed-url-handle-file-id-and-sha256",
    "private-read-lease-denies-write-delete-sharing-and-writable-mapping-conflicts",
    "wintrust-action-generic-verify-v2-long-zero",
    "same-chain-authenticode-policy-error-zero",
    "same-chain-microsoft-root-policy-error-zero",
    "microsoft-root-test-flag-disabled",
    "code-signing-eku-present",
    "trusted-timestamp-policy-error-zero",
    "hard-fail-revocation-and-observed-chain-input-stability",
)

WINTRUST_ACTION_GUID = "{00AAC56B-CD44-11D0-8CC2-00C04FC295EE}"
WINTRUST_PROV_FLAGS = ("WTD_DISABLE_MD2_MD4", "WTD_MOTW")
CHAIN_FLAGS = (
    "CERT_CHAIN_REVOCATION_CHECK_CHAIN_EXCLUDE_ROOT",
    "CERT_CHAIN_REVOCATION_ACCUMULATIVE_TIMEOUT",
    "CERT_CHAIN_TIMESTAMP_TIME",
)
CHAIN_ENGINE = "HCCE_LOCAL_MACHINE"
URL_RETRIEVAL_TIMEOUT_MS = 10_000
MAX_REVOCATION_FRESHNESS_SECONDS = 86_400
MAX_CHAIN_CALL_DURATION_SECONDS = 30
FILETIME_TICKS_PER_SECOND = 10_000_000
MAX_CANDIDATE_BYTES = 1_073_741_824
MAX_PROVIDER_CHAIN_CERTIFICATES = 32
MAX_REBUILT_CHAIN_CERTIFICATES = 32
MAX_CERTIFICATE_BYTES = 4_194_304
MAX_CTL_BYTES = 16_777_216
MAX_STORE_ENTRIES = 200_000
MAX_OBSERVATION_BYTES = 16_777_216
CODE_SIGNING_EKU = "1.3.6.1.5.5.7.3.3"
TIME_STAMPING_EKU = "1.3.6.1.5.5.7.3.8"

TRUST_SNAPSHOT_SCOPE = (
    "LOCAL-MACHINE-ROOT",
    "LOCAL-MACHINE-CA",
    "LOCAL-MACHINE-MY",
    "LOCAL-MACHINE-TRUST",
    "LOCAL-MACHINE-AUTHROOT",
    "LOCAL-MACHINE-DISALLOWED",
)

EVENT_SEQUENCE = (
    "ACQUISITION-RECORD-AUTHENTICATED",
    "IMMUTABLE-READ-LEASE-BOUND",
    "TRUST-SNAPSHOT-PRE",
    "WINTRUST-VERIFY-RETURNED",
    "PROVIDER-STATE-BOUND",
    "SIGNER-EXTRACTED",
    "TIMESTAMP-EXTRACTED",
    "SIGNER-CHAIN-REBUILT",
    "SIGNER-POLICIES-EVALUATED",
    "TIMESTAMP-CHAIN-REBUILT",
    "TIMESTAMP-POLICY-EVALUATED",
    "TRUST-SNAPSHOT-POST",
    "STATE-CLOSED",
    "PREEXECUTION-REHASHED",
)

SEMANTIC_RELATIONS = (
    "outer-implementation-manifest-equals-external-pin-and-observation",
    "policy-manifest-equals-authenticated-disk-closure",
    "acquisition-validator-manifest-equals-authenticated-disk-closure",
    "native-verifier-manifest-equals-authenticated-disk-closure-and-observation",
    "semantic-validator-manifest-equals-authenticated-disk-closure-and-observation",
    "observation-sha256-is-computed-from-canonical-input-bytes",
    "runtime-authority-is-explicitly-trusted-host-disk-consistency-only",
    "acquisition-record-canonical-hash-and-producer-authority-equal-external-pins",
    "acquisition-record-binds-fixed-url-zero-redirects-and-complete-transfer",
    "acquisition-record-binds-same-process-and-supplied-handle",
    "acquisition-handle-contract-denies-write-delete-and-writable-mapping",
    "private-lease-contract-denies-write-delete-and-is-noninheritable",
    "acquisition-and-three-verification-file-identities-are-equal",
    "acquisition-and-verification-file-are-not-reparse-points",
    "acquisition-and-three-byte-lengths-are-equal-positive-and-bounded",
    "acquisition-and-three-sha256-values-are-equal",
    "wintrust-input-contract-is-exact",
    "winverifytrust-return-is-long-zero",
    "event-sequence-and-provider-state-binding-are-exact",
    "provider-state-closes-after-policy-evaluation-with-long-zero",
    "signer-leaf-equals-provider-chain-position-zero",
    "provider-and-rebuilt-signer-chains-are-byte-identical",
    "signer-chain-call-binds-leaf-time-flags-bounds-and-output-chain",
    "authenticode-policy-input-binds-signer-chain-and-error-is-zero",
    "microsoft-root-policy-input-binds-same-chain-flags-zero-and-error-zero",
    "signer-code-signing-eku-is-present",
    "project-supplier-composite-is-exact-and-explicitly-not-an-official-leaf-claim",
    "timestamp-is-present-and-kind-is-supported",
    "timestamp-countersigner-index-and-provider-state-binding-are-exact",
    "timestamp-leaf-equals-provider-chain-position-zero",
    "provider-and-rebuilt-timestamp-chains-are-byte-identical",
    "timestamp-chain-call-binds-leaf-time-flags-bounds-and-output-chain",
    "authenticode-ts-policy-binds-chain-signing-time-and-error-is-zero",
    "chain-build-inputs-use-one-exact-network-capable-no-candidate-store-path",
    "every-nonroot-signer-element-has-good-conservatively-fresh-revocation",
    "every-nonroot-timestamp-element-has-good-conservatively-fresh-revocation",
    "chain-call-time-intervals-are-monotonic-bounded-and-not-claimed-exact",
    "signer-and-timestamp-roots-are-trusted-and-not-disallowed",
    "observed-chain-input-snapshot-scope-is-complete-and-not-claimed-effective",
    "pre-and-post-observed-chain-input-snapshots-are-equal",
    "trust-store-mutation-count-is-zero",
    "candidate-callback-store-and-custom-parser-are-absent",
    "process-count-before-decision-is-zero",
    "decision-never-grants-live-process-authority",
)

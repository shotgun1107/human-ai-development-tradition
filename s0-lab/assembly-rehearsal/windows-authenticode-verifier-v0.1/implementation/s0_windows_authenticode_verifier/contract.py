"""Exact implementation contract; no certificate or algorithm identity pins."""

from __future__ import annotations

FIXED_BOOTSTRAPPER_URL = (
    "https://download.visualstudio.microsoft.com/download/pr/"
    "fa619120-9c0e-47e6-bfe0-3ee96fb671b2/"
    "236367b68ba9a51708263ab10a1c85546cc4a8eca78b365168811d19c4fb2f29/"
    "vs_BuildTools.exe"
)

OBSERVATION_SCHEMA_ID = "S0-PUBLIC-WINDOWS-AUTHENTICODE-NATIVE-OBSERVATION-1"
TRACE_SCHEMA_ID = "S0-PUBLIC-WINDOWS-AUTHENTICODE-SEMANTIC-TRACE-1"
DECISION_SCHEMA_ID = "S0-PUBLIC-WINDOWS-AUTHENTICODE-DECISION-1"
SUPPLIER_CRITERION_ID = "PROJECT-APPROVED-MICROSOFT-DISTRIBUTION-COMPOSITE-1"

# This is an explicit project criterion, not a claim that Microsoft documents
# CERT_CHAIN_POLICY_MICROSOFT_ROOT as a leaf-publisher identity policy.
SUPPLIER_CRITERION_COMPONENTS = (
    "exact-fixed-microsoft-operated-url",
    "wintrust-action-generic-verify-v2-long-zero",
    "same-chain-authenticode-policy-error-zero",
    "same-chain-microsoft-root-policy-error-zero",
    "microsoft-root-test-flag-disabled",
    "code-signing-eku-present",
    "trusted-timestamp-policy-error-zero",
    "hard-fail-revocation-and-trust-state",
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
CODE_SIGNING_EKU = "1.3.6.1.5.5.7.3.3"
TIME_STAMPING_EKU = "1.3.6.1.5.5.7.3.8"

EVENT_SEQUENCE = (
    "ACQUISITION-BOUND",
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
    "outer-implementation-manifest-equals-independent-authority-and-observation",
    "policy-manifest-equals-independent-authority",
    "native-verifier-manifest-equals-independent-authority-and-observation",
    "semantic-validator-manifest-equals-independent-authority-and-observation",
    "observation-sha256-is-computed-from-canonical-input-bytes",
    "requested-and-final-uri-equal-fixed-microsoft-url",
    "redirect-count-is-zero",
    "one-original-file-handle-is-retained",
    "download-postsignature-preexecution-file-identity-is-equal",
    "retained-file-is-not-reparse-point",
    "download-postsignature-preexecution-byte-length-is-equal-positive",
    "download-postsignature-preexecution-sha256-is-equal",
    "wintrust-input-contract-is-exact",
    "winverifytrust-return-is-long-zero",
    "event-sequence-and-provider-state-binding-are-exact",
    "provider-state-closes-after-policy-evaluation-with-long-zero",
    "signer-leaf-equals-provider-chain-position-zero",
    "provider-and-rebuilt-signer-chains-are-byte-identical",
    "signer-chain-call-binds-leaf-time-flags-and-output-chain",
    "authenticode-policy-input-binds-signer-chain-and-error-is-zero",
    "microsoft-root-policy-input-binds-same-chain-flags-zero-and-error-zero",
    "signer-code-signing-eku-is-present",
    "project-supplier-composite-is-exact-and-explicitly-not-an-official-leaf-claim",
    "timestamp-is-present-and-kind-is-supported",
    "timestamp-countersigner-index-and-provider-state-binding-are-exact",
    "timestamp-leaf-equals-provider-chain-position-zero",
    "provider-and-rebuilt-timestamp-chains-are-byte-identical",
    "timestamp-chain-call-binds-leaf-time-flags-and-output-chain",
    "authenticode-ts-policy-binds-chain-signing-time-and-error-is-zero",
    "chain-build-inputs-use-one-exact-network-capable-no-candidate-store-path",
    "every-nonroot-signer-element-has-good-fresh-revocation",
    "every-nonroot-timestamp-element-has-good-fresh-revocation",
    "freshness-is-computed-from-recorded-reference-time-and-windows-age",
    "signer-and-timestamp-roots-are-trusted-and-not-disallowed",
    "pre-and-post-trust-authority-snapshots-are-equal",
    "trust-store-mutation-count-is-zero",
    "candidate-callback-store-and-custom-parser-are-absent",
    "process-count-before-decision-is-zero",
    "decision-never-grants-process-authority",
)

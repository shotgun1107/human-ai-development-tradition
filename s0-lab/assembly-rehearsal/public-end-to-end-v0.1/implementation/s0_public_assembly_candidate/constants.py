"""Frozen public constants for the bounded assembly candidate."""

from __future__ import annotations

from types import MappingProxyType


REHEARSAL_ID = "S0-PUBLIC-AR-B2-P01-001"
BLOCK_ID = "BLK-PRACTICE0002"
REPRESENTATION_ID = "P01"

STATE_ORDER = (
    "NEW",
    "PREFLIGHT_AUTHENTICATED",
    "REQUEST_RECONSTRUCTED",
    "OUTPUT_RESERVED",
    "RUNNER_ENTERED",
    "INVOKED_ONCE",
    "RESPONSE_CAPTURED",
    "ANSWER_VALIDATED",
    "TEMP_RECORD_VERIFIED",
    "COMPLETE",
)

OUTPUT_NAMES = (
    "run-record.pending",
    "run-record.json",
    "publication-receipt.pending",
    "publication-receipt.json",
)

RUN_RECORD_PENDING_NAME = OUTPUT_NAMES[0]
RUN_RECORD_FINAL_NAME = OUTPUT_NAMES[1]
RECEIPT_PENDING_NAME = OUTPUT_NAMES[2]
RECEIPT_FINAL_NAME = OUTPUT_NAMES[3]

REQUEST_MANIFEST_PATH = (
    "s0-lab/assembly-rehearsal/public-end-to-end-v0.1/request-files.sha256"
)
REQUEST_ENTRY_PREFIX = "s0-lab/assembly-rehearsal/public-end-to-end-v0.1/inputs/"
REQUEST_PATH = REQUEST_ENTRY_PREFIX + "request.json"
REQUEST_PURPOSE = "s0-public-assembly-rehearsal-v01"
REQUEST_SHA256 = "990f12bd98b0f2c7ce64e683a8165c6e67384d6dbc6b4f1f4ec62b19f28b75e2"
REQUEST_BYTES = 7917
REQUEST_MANIFEST_SHA256 = (
    "872f2bca8d2d56c9b664e37ad6092a4dd4d8750d40eb8ba99dfbad7f7c94c9f7"
)
REQUEST_MANIFEST_BYTES = (
    REQUEST_SHA256.encode("ascii") + b"  " + REQUEST_PATH.encode("ascii") + b"\n"
)

PUBLIC_BUNDLE_MANIFEST_PATH = "s0-lab/public-practice/v0.1/bundle-files.sha256"
PUBLIC_BUNDLE_MANIFEST_SHA256 = (
    "e41ee6c71169df646e3c8c0b0e8f3d77e7871d939f651b86a52ea5696feeb637"
)
PUBLIC_BUNDLE_ENTRY_COUNT = 90

CANONICAL_PATH = (
    "s0-lab/public-practice/v0.1/blocks/BLK-PRACTICE0002/canonical-input.json"
)
CANONICAL_SHA256 = "bf8e48e1bed4c061df7de896aa14848cdeab6692288a2eda5b445c1a87557863"
PACKAGE_PATH = "s0-lab/public-practice/v0.1/packages/P01B2EMBR001/input.json"
PACKAGE_SHA256 = "15bace158828b8a16a4fd9d76dddfa7b5870bdb580198f0da308c4fa575e03b7"
QUESTIONS_PATH = (
    "s0-lab/public-practice/v0.1/runner/BLK-PRACTICE0002/questions.json"
)
QUESTIONS_SHA256 = "661c09dfb20ea933f521370f9e3f94e2512f49e67020101d3767a6a92a07fe90"
PUBLIC_RESPONSE_PATH = (
    "s0-lab/public-practice/v0.1/blocks/BLK-PRACTICE0002/expected-answer-P01.json"
)
PUBLIC_RESPONSE_SHA256 = (
    "c2f824c6483b625e2fa50d0016443632809471f32ebb235e09f454cf04981bdf"
)
PUBLIC_RESPONSE_BYTES = 1936
ANSWER_SCHEMA_PATH = "s0-lab/control/sm0/answer.schema.json"
ANSWER_SCHEMA_SHA256 = "e21100f06d2715f42cd1fda812e17d22340a64327bfb48c03112a0f83d33ac6b"

I2_CONTRACT_PATH = "s0-lab/i2/spec/trust-root-role-isolation-contract-v0.4.json"
I2_CONTRACT_SHA256 = "713fc6b44c84126387dc492b93e22d928ba894e18bdc8705049a2ea5cb8cc7da"
I3_CONTRACT_PATH = "s0-lab/i3/spec/import-decision-contract-v0.1.json"
I3_CONTRACT_SHA256 = "ae834becfc393e4f525265aff473ae32d12f349713fb48b2e0bb60ea39fc7ac8"

COMPONENT_MANIFESTS = MappingProxyType(
    {
        "i0": (
            "s0-lab/i0/verification/implementation-files.sha256",
            "f57514f96a2c30366cdf1f1414524711da20c9410186b3017e3dbf902bb612ae",
        ),
        "i1": (
            "s0-lab/i1/verification/implementation-files.sha256",
            "668d3549ef6f7146ac7200e7be1f362967eca4c2cf66119a1f727bebd245332c",
        ),
        "i2": (
            "s0-lab/i2/verification/implementation-files.sha256",
            "18ccfbcbe73b1170e07bd000376b079528dcf135b806e3f6c77b10efae736bd6",
        ),
        "i3": (
            "s0-lab/i3/verification/implementation-files.sha256",
            "e07c9754d61b143bca9747bbcccb58b0861b14f60031422e1e4fd88a0fb93648",
        ),
    }
)

DESIGN_PACKAGE_MANIFEST_SHA256 = (
    "6292e322549c79f539b57c1087fd722c5cca96318c45d89fac5343247c429802"
)
DESIGN_INDEPENDENT_REVIEW_SHA256 = (
    "7c629c9c4aed5c2e36598e4ad08e4819fa06b73f3f77bf9e7d19714f61b35137"
)

STUB_TRANSPORT_ID = "S0-PUBLIC-EXACT-ANSWER-STUB-1"
STUB_RESPONSE_ID = "S0-PUBLIC-AR-B2-P01-RESPONSE-1"
REQUIRED_STUB_COUNTERS = MappingProxyType(
    {
        "transport_calls": 1,
        "script_frame_count": 1,
        "yielded_frame_count": 1,
        "close_count": 1,
        "unconsumed_frame_count_on_close": 0,
    }
)

RUN_RECORD_SCHEMA_ID = "S0-PUBLIC-ASSEMBLY-RUN-RECORD-3"
RUN_RECORD_BYTES = 2224
RUN_RECORD_SHA256 = "73b2091e7aab315bcafd487965dc8c3304b19afca56132de471c787254b7fda6"

EXPECTED_RUN_RECORD = MappingProxyType(
    {
        "actual_response_sha256": PUBLIC_RESPONSE_SHA256,
        "answer_validation_error_count": 0,
        "block_id": BLOCK_ID,
        "bundle_manifest_sha256": PUBLIC_BUNDLE_MANIFEST_SHA256,
        "canonical_sha256": CANONICAL_SHA256,
        "claim_kind": (
            "candidate-controller-completion-diagnostic-only-not-rehearsal-pass-not-s0"
        ),
        "denied_input_access_count": 0,
        "design_base_commit": "f7048e919ab0e698d78ca4ff4cc4eb31ca6f612c",
        "design_revision": "0.5",
        "expected_response_sha256": PUBLIC_RESPONSE_SHA256,
        "final_frames": 1,
        "i0_manifest_sha256": COMPONENT_MANIFESTS["i0"][1],
        "i1_manifest_sha256": COMPONENT_MANIFESTS["i1"][1],
        "i2_disposition": "contract-authenticated-no-import-route",
        "i2_manifest_sha256": COMPONENT_MANIFESTS["i2"][1],
        "i3_disposition": "contract-authenticated-no-import-attempt",
        "i3_manifest_sha256": COMPONENT_MANIFESTS["i3"][1],
        "offline_status": "offline-not-success-diagnostic-only",
        "package_sha256": PACKAGE_SHA256,
        "public_bundle_entry_count": PUBLIC_BUNDLE_ENTRY_COUNT,
        "questions_sha256": QUESTIONS_SHA256,
        "rehearsal_id": REHEARSAL_ID,
        "rehearsal_pass_authority": (
            "same-process-verifier-live-consumer-2-acceptance-only"
        ),
        "representation_id": REPRESENTATION_ID,
        "request_manifest_path": REQUEST_MANIFEST_PATH,
        "request_manifest_sha256": REQUEST_MANIFEST_SHA256,
        "request_path": REQUEST_PATH,
        "request_sha256": REQUEST_SHA256,
        "response_frames": 1,
        "result": "candidate-controller-complete-awaiting-live-consumer",
        "retry_count": 0,
        "schema_id": RUN_RECORD_SCHEMA_ID,
        "state": "COMPLETE",
        "stub_script_frame_count": 1,
        "stub_transport_id": STUB_TRANSPORT_ID,
        "stub_unconsumed_frame_count_on_close": 0,
        "stub_yielded_frame_count": 1,
        "transport_calls": 1,
    }
)

RECEIPT_SCHEMA_ID = "S0-PUBLIC-ASSEMBLY-PUBLICATION-RECEIPT-2"
RECEIPT_BYTES = 1173
RECEIPT_FIXED_VALUES = MappingProxyType(
    {
        "evidence_consumer_id": "S0-PUBLIC-ASSEMBLY-LIVE-CONSUMER-2",
        "observer_id": "S0-PUBLIC-ASSEMBLY-PUBLICATION-OBSERVER-2",
        "offline_status": "offline-not-success-diagnostic-only",
        "platform_profile_id": "S0-WIN64-NTFS-MOVEFILEEXW-CTYPES-ABI-2",
        "publication_outcome": "controller-files-published-awaiting-live-consumer",
        "publication_primitive": "MoveFileExW",
        "publication_primitive_flags": 0,
        "receipt_path": RECEIPT_FINAL_NAME,
        "record_path": RUN_RECORD_FINAL_NAME,
        "record_sha256": RUN_RECORD_SHA256,
        "rehearsal_id": REHEARSAL_ID,
        "rehearsal_pass_authority": (
            "same-process-verifier-live-consumer-2-acceptance-only"
        ),
        "schema_id": RECEIPT_SCHEMA_ID,
        "stub_close_count": 1,
        "stub_script_frame_count": 1,
        "stub_transport_calls": 1,
        "stub_unconsumed_frame_count_on_close": 0,
        "stub_yielded_frame_count": 1,
    }
)

PUBLISH_RECORD = b"PUBLISH_RECORD\n"
PUBLISH_RECEIPT = b"PUBLISH_RECEIPT\n"
PUBLISH_OK = b"OK\n"


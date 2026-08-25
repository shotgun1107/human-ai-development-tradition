from __future__ import annotations

import ast
import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "implementation"))

from s0_windows_authenticode_verifier.acquisition import (  # noqa: E402
    authenticate_acquisition_record,
)
from s0_windows_authenticode_verifier.authority import (  # noqa: E402
    authenticate_installed_implementation,
)
from s0_windows_authenticode_verifier.canonical import (  # noqa: E402
    canonical_json_lf,
    sha256_hex,
    strict_json_object,
)
from s0_windows_authenticode_verifier.contract import (  # noqa: E402
    ACQUISITION_HANDLE_CONTRACT,
    ACQUISITION_PATH_SEMANTICS_ID,
    ACQUISITION_SCHEMA_ID,
    CHAIN_ENGINE,
    CHAIN_FLAGS,
    CODE_SIGNING_EKU,
    EVENT_SEQUENCE,
    FILETIME_TICKS_PER_SECOND,
    FIXED_BOOTSTRAPPER_URL,
    IMMUTABLE_LEASE_CONTRACT,
    MAX_CHAIN_CALL_DURATION_SECONDS,
    MAX_PROVIDER_CHAIN_CERTIFICATES,
    MAX_REVOCATION_FRESHNESS_SECONDS,
    OBSERVATION_SCHEMA_ID,
    RUNTIME_AUTHORITY_SCOPE,
    SEMANTIC_RELATIONS,
    SUPPLIER_CRITERION_COMPONENTS,
    SUPPLIER_CRITERION_ID,
    TIME_STAMPING_EKU,
    TRUST_SNAPSHOT_SCOPE,
    URL_RETRIEVAL_TIMEOUT_MS,
    WINTRUST_ACTION_GUID,
    WINTRUST_PROV_FLAGS,
)
from s0_windows_authenticode_verifier.model import (  # noqa: E402
    VerificationAuthority,
)
from s0_windows_authenticode_verifier.semantic import (  # noqa: E402
    chain_call_input_sha256,
    evaluate_observation,
    policy_input_sha256,
)
from s0_windows_authenticode_verifier.verifier import (  # noqa: E402
    verify_open_file_trusted_host,
)
from s0_windows_authenticode_verifier import win32 as win32_module  # noqa: E402


_HANDLE = 0x1234
_PROCESS_ID = 4321


def _identity() -> dict[str, object]:
    return {
        "volume_serial_hex": "0000000000000001",
        "file_id_hex": "00000000000000000000000000000002",
        "reparse_point": False,
        "byte_length": 1234,
    }


def _acquisition_record(
    authority_manifest_sha256: str,
    *,
    handle: int = _HANDLE,
    process_id: int = _PROCESS_ID,
) -> dict[str, object]:
    return {
        "schema_id": ACQUISITION_SCHEMA_ID,
        "authority_manifest_sha256": authority_manifest_sha256,
        "sequence_id": "7" * 64,
        "producer_process_id": process_id,
        "created_filetime_hex": "01dbeebf12345678",
        "acquired_path": (
            r"\\?\Volume{11111111-2222-3333-4444-555555555555}"
            r"\downloads\vs_BuildTools.exe"
        ),
        "acquired_path_semantics": ACQUISITION_PATH_SEMANTICS_ID,
        "requested_uri": FIXED_BOOTSTRAPPER_URL,
        "final_uri": FIXED_BOOTSTRAPPER_URL,
        "redirect_count": 0,
        "transfer_complete": True,
        "retained_handle_hex": f"{handle:016x}",
        "handle_contract": dict(ACQUISITION_HANDLE_CONTRACT),
        "file_identity": _identity(),
        "byte_sha256": "b" * 64,
    }


def _authority_and_record() -> tuple[VerificationAuthority, dict[str, object], bytes]:
    producer_manifest = "6" * 64
    record = _acquisition_record(producer_manifest)
    raw = canonical_json_lf(record)
    authority = VerificationAuthority(
        "1" * 64,
        "2" * 64,
        "3" * 64,
        "4" * 64,
        "5" * 64,
        sha256_hex(raw),
        producer_manifest,
    )
    return authority, record, raw


def _element(index: int, count: int, digest: str) -> dict[str, object]:
    root = index == count - 1
    return {
        "position": index,
        "role": "LEAF" if index == 0 else "ROOT" if root else "INTERMEDIATE",
        "certificate_der_sha256": digest,
        "trust_error_status": 0,
        "trust_info_status": 0,
        "revocation_result": "ROOT-NOT-CHECKED" if root else "GOOD",
        "has_freshness_time": not root,
        "freshness_age_seconds": None if root else 60 + index,
        "disallowed": False,
    }


def _chain(digests: list[str]) -> list[dict[str, object]]:
    return [_element(index, len(digests), digest) for index, digest in enumerate(digests)]


def _chain_call(
    chain: list[dict[str, object]],
    leaf: str,
    verification_time: int,
    call_started: int,
    eku: str,
) -> dict[str, object]:
    value: dict[str, object] = {
        "api": "CertGetCertificateChain",
        "chain_engine": CHAIN_ENGINE,
        "flags": list(CHAIN_FLAGS),
        "url_retrieval_timeout_ms": URL_RETRIEVAL_TIMEOUT_MS,
        "leaf_certificate_der_sha256": leaf,
        "verification_time_filetime_hex": f"{verification_time:016x}",
        "cache_resync_filetime_hex": f"{call_started - MAX_REVOCATION_FRESHNESS_SECONDS * FILETIME_TICKS_PER_SECOND:016x}",
        "call_started_filetime_hex": f"{call_started:016x}",
        "call_returned_filetime_hex": f"{call_started + 2 * FILETIME_TICKS_PER_SECOND:016x}",
        "monotonic_frequency_hex": f"{FILETIME_TICKS_PER_SECOND:016x}",
        "monotonic_started_hex": f"{123_000_000_000:016x}",
        "monotonic_returned_hex": f"{123_000_000_000 + 2 * FILETIME_TICKS_PER_SECOND:016x}",
        "requested_eku": eku,
        "additional_candidate_store_used": False,
        "api_return": True,
        "output_chain_sha256": sha256_hex(canonical_json_lf(chain)),
        "input_sha256": "",
    }
    value["input_sha256"] = chain_call_input_sha256(value)
    return value


def _policy(
    policy_id: str,
    chain_sha256: str,
    verification_time: int,
    extra: dict[str, object],
) -> dict[str, object]:
    value: dict[str, object] = {
        "policy_id": policy_id,
        "chain_context_sha256": chain_sha256,
        "verification_time_filetime_hex": f"{verification_time:016x}",
        "flags": 0,
        "extra_policy": extra,
        "api_return": True,
        "policy_error": 0,
        "input_sha256": "",
    }
    value["input_sha256"] = policy_input_sha256(value)
    return value


def _observation(
    authority: VerificationAuthority,
    acquisition_record: dict[str, object],
) -> dict[str, object]:
    signing_time = 133_000_000_000_000_000
    signer_start = signing_time + 50_000_000
    timestamp_start = signer_start + 30_000_000
    state_id = "8" * 64
    signer_provider = ["9" * 64, "a" * 64, "b" * 64]
    timestamp_provider = ["c" * 64, "d" * 64, "e" * 64]
    signer_chain = _chain(signer_provider)
    timestamp_chain = _chain(timestamp_provider)
    signer_call = _chain_call(
        signer_chain,
        signer_provider[0],
        signing_time,
        signer_start,
        CODE_SIGNING_EKU,
    )
    timestamp_call = _chain_call(
        timestamp_chain,
        timestamp_provider[0],
        signing_time,
        timestamp_start,
        TIME_STAMPING_EKU,
    )
    identity = _identity()
    snapshot = {"sha256": "f" * 64, "entry_count": 42}
    return {
        "schema_id": OBSERVATION_SCHEMA_ID,
        "native_collection_status": "COMPLETED-NONAUTHORITATIVE-OBSERVATION",
        "implementation_manifest_sha256": authority.implementation_manifest_sha256,
        "policy_manifest_sha256": authority.policy_manifest_sha256,
        "acquisition_validator_manifest_sha256": (
            authority.acquisition_validator_manifest_sha256
        ),
        "native_verifier_manifest_sha256": authority.native_verifier_manifest_sha256,
        "semantic_validator_manifest_sha256": (
            authority.semantic_validator_manifest_sha256
        ),
        "runtime_authority": {
            "scope": RUNTIME_AUTHORITY_SCOPE,
            "executed_code_authority_established": False,
        },
        "acquisition_record": copy.deepcopy(acquisition_record),
        "acquisition_record_sha256": authority.acquisition_record_sha256,
        "runtime_binding": {
            "consumer_process_id": _PROCESS_ID,
            "supplied_handle_hex": f"{_HANDLE:016x}",
            "supplied_handle_path": acquisition_record["acquired_path"],
            "immutable_lease_path": acquisition_record["acquired_path"],
            "path_semantics": ACQUISITION_PATH_SEMANTICS_ID,
            "immutable_lease_contract": dict(IMMUTABLE_LEASE_CONTRACT),
        },
        "supplier": {
            "criterion_id": SUPPLIER_CRITERION_ID,
            "components": list(SUPPLIER_CRITERION_COMPONENTS),
            "official_leaf_guarantee_claimed": False,
            "project_reauthorization_acknowledged": True,
        },
        "file_identities": {
            "lease_open": copy.deepcopy(identity),
            "post_signature": copy.deepcopy(identity),
            "preexecution": copy.deepcopy(identity),
        },
        "byte_sha256": {
            "lease_open": "b" * 64,
            "post_signature": "b" * 64,
            "preexecution": "b" * 64,
        },
        "wintrust": {
            "action_guid": WINTRUST_ACTION_GUID,
            "window_handle": "INVALID_HANDLE_VALUE",
            "ui_choice": "WTD_UI_NONE",
            "ui_context": "WTD_UICONTEXT_INSTALL",
            "union_choice": "WTD_CHOICE_FILE",
            "revocation_checks": "WTD_REVOKE_NONE",
            "prov_flags": list(WINTRUST_PROV_FLAGS),
            "state_action_verify": "WTD_STATEACTION_VERIFY",
            "verify_return": 0,
            "state_action_close": "WTD_STATEACTION_CLOSE",
            "close_return": 0,
            "provider_state_id": state_id,
            "candidate_callback_used": False,
            "candidate_store_used": False,
            "custom_parser_used": False,
        },
        "events": [
            {
                "sequence": index,
                "kind": kind,
                "provider_state_id": state_id if 3 <= index <= 12 else None,
            }
            for index, kind in enumerate(EVENT_SEQUENCE)
        ],
        "signer": {
            "leaf_certificate_der_sha256": signer_provider[0],
            "provider_chain": signer_provider,
            "rebuilt_chain": signer_chain,
            "chain_call": signer_call,
            "code_signing_eku_present": True,
            "authenticode_policy": _policy(
                "CERT_CHAIN_POLICY_AUTHENTICODE",
                signer_call["output_chain_sha256"],
                signing_time,
                {"pv_extra_policy_para": "NULL"},
            ),
            "microsoft_root_policy": _policy(
                "CERT_CHAIN_POLICY_MICROSOFT_ROOT",
                signer_call["output_chain_sha256"],
                signing_time,
                {"test_root_enabled": False},
            ),
        },
        "timestamp": {
            "present": True,
            "kind": "WINDOWS-PROVIDER-TIMESTAMP-SIGNER",
            "signer_index": 0,
            "countersigner_index": 0,
            "provider_state_id": state_id,
            "signing_time_filetime_hex": f"{signing_time:016x}",
            "leaf_certificate_der_sha256": timestamp_provider[0],
            "provider_chain": timestamp_provider,
            "rebuilt_chain": timestamp_chain,
            "chain_call": timestamp_call,
            "timestamp_policy": _policy(
                "CERT_CHAIN_POLICY_AUTHENTICODE_TS",
                timestamp_call["output_chain_sha256"],
                signing_time,
                {"pv_extra_policy_para": "NULL"},
            ),
        },
        "trust_authority": {
            "pre_snapshot": copy.deepcopy(snapshot),
            "post_snapshot": copy.deepcopy(snapshot),
            "snapshot_scope": list(TRUST_SNAPSHOT_SCOPE),
            "enumeration_complete": True,
            "store_close_success": True,
            "effective_trust_authority_claimed": False,
            "store_mutation_count": 0,
        },
        "process_count_before_decision": 0,
    }


def _fixture() -> tuple[VerificationAuthority, dict[str, object]]:
    authority, record, _ = _authority_and_record()
    return authority, _observation(authority, record)


def _evaluate(value: dict[str, object], authority: VerificationAuthority):
    return evaluate_observation(canonical_json_lf(value), authority)


class AuthenticodeVerifierTests(unittest.TestCase):
    def test_installed_implementation_and_submanifests_authenticate(self) -> None:
        _, record, raw = _authority_and_record()
        manifest = ROOT / "verification" / "implementation-files.sha256"
        pin = sha256_hex(manifest.read_bytes())
        authority = authenticate_installed_implementation(
            pin,
            expected_acquisition_record_sha256=sha256_hex(raw),
            expected_acquisition_authority_manifest_sha256=(
                record["authority_manifest_sha256"]
            ),
        )
        self.assertEqual(pin, authority.implementation_manifest_sha256)
        self.assertFalse(authority.executed_code_authority_established)
        for field, name in (
            ("policy_manifest_sha256", "policy-contract-files.sha256"),
            ("acquisition_validator_manifest_sha256", "acquisition-validator-files.sha256"),
            ("native_verifier_manifest_sha256", "native-verifier-files.sha256"),
            ("semantic_validator_manifest_sha256", "semantic-validator-files.sha256"),
        ):
            self.assertEqual(
                sha256_hex((ROOT / "verification" / name).read_bytes()),
                getattr(authority, field),
            )

    def test_acquisition_record_authenticates_external_pins_process_and_handle(self) -> None:
        authority, record, raw = _authority_and_record()
        result = authenticate_acquisition_record(
            raw,
            expected_record_sha256=authority.acquisition_record_sha256,
            expected_authority_manifest_sha256=(
                authority.acquisition_authority_manifest_sha256
            ),
            retained_handle=_HANDLE,
            current_process_id=_PROCESS_ID,
        )
        self.assertEqual(raw, result.raw)
        mutations = (
            ("final_uri", FIXED_BOOTSTRAPPER_URL + "?changed=1"),
            ("producer_process_id", _PROCESS_ID + 1),
            ("retained_handle_hex", "0" * 16),
            (
                "acquired_path",
                r"\\?\Volume{11111111-2222-3333-4444-555555555555}"
                r"\other\vs_BuildTools.exe:stream",
            ),
            ("acquired_path_semantics", "OTHER"),
        )
        for field, replacement in mutations:
            with self.subTest(field=field):
                changed = copy.deepcopy(record)
                changed[field] = replacement
                changed_raw = canonical_json_lf(changed)
                with self.assertRaises(ValueError):
                    authenticate_acquisition_record(
                        changed_raw,
                        expected_record_sha256=sha256_hex(changed_raw),
                        expected_authority_manifest_sha256=(
                            authority.acquisition_authority_manifest_sha256
                        ),
                        retained_handle=_HANDLE,
                        current_process_id=_PROCESS_ID,
                    )

    def test_valid_observation_computes_all_relations_but_no_live_authority(self) -> None:
        authority, value = _fixture()
        raw = canonical_json_lf(value)
        result = evaluate_observation(raw, authority)
        self.assertTrue(result.trust_policy_pass)
        self.assertFalse(result.executed_code_authority_established)
        self.assertFalse(result.process_authority_granted)
        self.assertEqual(RUNTIME_AUTHORITY_SCOPE, result.runtime_authority_scope)
        self.assertEqual((), result.failure_relations)
        self.assertEqual(44, len(SEMANTIC_RELATIONS))
        decision = strict_json_object(result.decision_raw)
        self.assertEqual(
            "PASS-BOUNDED-TRUSTED-HOST-CONSISTENCY-NO-LIVE-AUTHORITY",
            decision["terminal_decision"],
        )

    def test_observation_bytes_are_canonical_and_actual_hash_is_bound(self) -> None:
        authority, value = _fixture()
        raw = canonical_json_lf(value)
        noncanonical = b" " + raw
        result = evaluate_observation(noncanonical, authority)
        self.assertFalse(result.trust_policy_pass)
        self.assertEqual(sha256_hex(noncanonical), result.observation_sha256)

    def test_all_manifest_and_acquisition_authorities_are_cross_bound(self) -> None:
        authority, baseline = _fixture()
        for field in (
            "implementation_manifest_sha256",
            "policy_manifest_sha256",
            "acquisition_validator_manifest_sha256",
            "native_verifier_manifest_sha256",
            "semantic_validator_manifest_sha256",
            "acquisition_record_sha256",
        ):
            with self.subTest(field=field):
                value = copy.deepcopy(baseline)
                value[field] = "0" * 63 + "1"
                self.assertFalse(_evaluate(value, authority).trust_policy_pass)

    def test_acquisition_provenance_and_private_lease_substitution_reject(self) -> None:
        authority, baseline = _fixture()
        mutations = (
            lambda value: value["acquisition_record"].__setitem__(
                "final_uri", FIXED_BOOTSTRAPPER_URL + "?other=1"
            ),
            lambda value: value["acquisition_record"].__setitem__(
                "byte_sha256", "0" * 63 + "1"
            ),
            lambda value: value["runtime_binding"].__setitem__(
                "supplied_handle_hex", "0" * 16
            ),
            lambda value: value["runtime_binding"].__setitem__(
                "immutable_lease_path",
                r"\\?\Volume{11111111-2222-3333-4444-555555555555}"
                r"\other\vs_BuildTools.exe",
            ),
            lambda value: value["runtime_binding"]["immutable_lease_contract"].__setitem__(
                "write_sharing_denied", False
            ),
        )
        for mutate in mutations:
            value = copy.deepcopy(baseline)
            mutate(value)
            self.assertFalse(_evaluate(value, authority).trust_policy_pass)

    def test_raw_record_cannot_claim_runtime_or_process_authority(self) -> None:
        authority, value = _fixture()
        value["runtime_authority"]["executed_code_authority_established"] = True
        self.assertFalse(_evaluate(value, authority).trust_policy_pass)
        value = _fixture()[1]
        value["process_authority_granted"] = True
        self.assertFalse(_evaluate(value, authority).trust_policy_pass)

    def test_event_order_state_binding_and_close_failure_reject(self) -> None:
        authority, baseline = _fixture()
        for mutate in (
            lambda value: value["events"].__setitem__(10, value["events"][12]),
            lambda value: value["events"][6].__setitem__("provider_state_id", "0" * 63 + "1"),
            lambda value: value["wintrust"].__setitem__("close_return", 1),
        ):
            value = copy.deepcopy(baseline)
            mutate(value)
            self.assertFalse(_evaluate(value, authority).trust_policy_pass)

    def test_native_source_places_verify_and_chain_resources_under_cleanup(self) -> None:
        source = (
            ROOT
            / "implementation"
            / "s0_windows_authenticode_verifier"
            / "win32.py"
        ).read_text(encoding="utf-8")
        ast.parse(source)
        self.assertIn("if verify_called:", source)
        self.assertIn("data.dwStateAction = WTD_STATEACTION_CLOSE", source)
        self.assertIn("except Exception:", source)
        self.assertIn("api.crypt32.CertFreeCertificateChain(context)", source)
        self.assertIn("CertFreeCertificateContext", source)
        self.assertIn("CertFreeCTLContext", source)
        self.assertIn("QueryPerformanceCounter", source)

        calls: list[str] = []

        class FakeCrypt32:
            def CertFreeCertificateContext(self, _context):
                calls.append("cert")
                return True

            def CertFreeCTLContext(self, _context):
                calls.append("ctl")
                return True

            def CertCloseStore(self, _store, _flags):
                calls.append("store")
                return True

        fake_api = type("FakeApi", (), {"crypt32": FakeCrypt32()})()
        win32_module._cleanup_store_contexts(fake_api, object(), object(), object())
        self.assertEqual(["cert", "ctl", "store"], calls)

        calls.clear()

        class FailingFreeCrypt32(FakeCrypt32):
            def CertFreeCertificateContext(self, _context):
                calls.append("cert")
                return False

        failing_api = type("FakeApi", (), {"crypt32": FailingFreeCrypt32()})()
        with self.assertRaises(ValueError):
            win32_module._cleanup_store_contexts(
                failing_api,
                object(),
                object(),
                object(),
            )
        self.assertEqual(["cert", "ctl", "store"], calls)

    def test_policy_chain_time_and_input_hash_substitution_reject(self) -> None:
        authority, baseline = _fixture()
        mutations = (
            ("signer", "authenticode_policy", "chain_context_sha256", "0" * 63 + "1"),
            ("signer", "microsoft_root_policy", "verification_time_filetime_hex", "000000000000007b"),
            ("timestamp", "timestamp_policy", "input_sha256", "0" * 63 + "1"),
            ("timestamp", "chain_call", "verification_time_filetime_hex", "000000000000007b"),
        )
        for first, second, field, replacement in mutations:
            value = copy.deepcopy(baseline)
            value[first][second][field] = replacement
            self.assertFalse(_evaluate(value, authority).trust_policy_pass)

    def test_countersigner_index_and_provider_state_substitution_reject(self) -> None:
        authority, baseline = _fixture()
        for field, replacement in (
            ("countersigner_index", 1),
            ("provider_state_id", "0" * 63 + "1"),
        ):
            value = copy.deepcopy(baseline)
            value["timestamp"][field] = replacement
            self.assertFalse(_evaluate(value, authority).trust_policy_pass)

    def test_freshness_uses_conservative_bounded_call_intervals(self) -> None:
        authority, baseline = _fixture()
        value = copy.deepcopy(baseline)
        value["signer"]["rebuilt_chain"][0]["freshness_age_seconds"] = (
            MAX_REVOCATION_FRESHNESS_SECONDS
        )
        self.assertFalse(_evaluate(value, authority).trust_policy_pass)

        value = copy.deepcopy(baseline)
        call = value["timestamp"]["chain_call"]
        call["call_returned_filetime_hex"] = f"{int(call['call_started_filetime_hex'], 16) - 1:016x}"
        self.assertFalse(_evaluate(value, authority).trust_policy_pass)

        value = copy.deepcopy(baseline)
        call = value["signer"]["chain_call"]
        call["call_returned_filetime_hex"] = f"{int(call['call_started_filetime_hex'], 16) + (MAX_CHAIN_CALL_DURATION_SECONDS + 1) * FILETIME_TICKS_PER_SECOND:016x}"
        self.assertFalse(_evaluate(value, authority).trust_policy_pass)

        value = copy.deepcopy(baseline)
        call = value["signer"]["chain_call"]
        call["call_returned_filetime_hex"] = f"{int(call['call_started_filetime_hex'], 16) + FILETIME_TICKS_PER_SECOND:016x}"
        call["monotonic_returned_hex"] = f"{int(call['monotonic_started_hex'], 16) + 10 * FILETIME_TICKS_PER_SECOND:016x}"
        self.assertFalse(_evaluate(value, authority).trust_policy_pass)

        value = copy.deepcopy(baseline)
        call = value["timestamp"]["chain_call"]
        call["monotonic_returned_hex"] = f"{int(call['monotonic_started_hex'], 16) - 1:016x}"
        self.assertFalse(_evaluate(value, authority).trust_policy_pass)

    def test_supplier_composite_remains_explicitly_not_official_leaf_claim(self) -> None:
        authority, baseline = _fixture()
        for field, replacement in (
            ("official_leaf_guarantee_claimed", True),
            ("project_reauthorization_acknowledged", False),
            ("criterion_id", "OTHER"),
        ):
            value = copy.deepcopy(baseline)
            value["supplier"][field] = replacement
            self.assertFalse(_evaluate(value, authority).trust_policy_pass)

    def test_file_trust_snapshot_and_process_mutations_reject(self) -> None:
        authority, baseline = _fixture()
        values: list[dict[str, object]] = []
        value = copy.deepcopy(baseline); value["file_identities"]["preexecution"]["file_id_hex"] = "f" * 32; values.append(value)
        value = copy.deepcopy(baseline); value["byte_sha256"]["post_signature"] = "f" * 64; values.append(value)
        value = copy.deepcopy(baseline); value["trust_authority"]["post_snapshot"]["sha256"] = "0" * 63 + "1"; values.append(value)
        value = copy.deepcopy(baseline); value["trust_authority"]["effective_trust_authority_claimed"] = True; values.append(value)
        value = copy.deepcopy(baseline); value["process_count_before_decision"] = 1; values.append(value)
        for item in values:
            self.assertFalse(_evaluate(item, authority).trust_policy_pass)

    def test_provider_chain_bound_rejects(self) -> None:
        authority, value = _fixture()
        value["signer"]["provider_chain"] = ["9" * 64] * (
            MAX_PROVIDER_CHAIN_CERTIFICATES + 1
        )
        self.assertFalse(_evaluate(value, authority).trust_policy_pass)

    def test_invalid_native_handle_fails_closed_without_native_or_process_authority(self) -> None:
        _, record, raw = _authority_and_record()
        implementation_pin = sha256_hex(
            (ROOT / "verification" / "implementation-files.sha256").read_bytes()
        )
        result = verify_open_file_trusted_host(
            full_path=str(Path.cwd() / "never-opened.exe"),
            file_handle=0,
            implementation_manifest_sha256=implementation_pin,
            acquisition_record_raw=raw,
            acquisition_record_sha256=sha256_hex(raw),
            acquisition_authority_manifest_sha256=(
                record["authority_manifest_sha256"]
            ),
        )
        self.assertFalse(result.trust_policy_pass)
        self.assertFalse(result.executed_code_authority_established)
        self.assertFalse(result.process_authority_granted)

    def test_package_import_is_inert(self) -> None:
        package = (
            ROOT
            / "implementation"
            / "s0_windows_authenticode_verifier"
            / "__init__.py"
        )
        tree = ast.parse(package.read_text(encoding="utf-8"))
        self.assertFalse(
            any(isinstance(node, (ast.Import, ast.ImportFrom)) for node in ast.walk(tree))
        )

    def test_strict_parser_rejects_duplicate_key(self) -> None:
        with self.assertRaises(ValueError):
            strict_json_object(b'{"a":1,"a":2}\n')


if __name__ == "__main__":
    unittest.main()

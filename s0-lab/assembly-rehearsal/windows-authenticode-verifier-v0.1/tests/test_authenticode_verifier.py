from __future__ import annotations

import copy
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "implementation"))

from s0_windows_authenticode_verifier import (  # noqa: E402
    FIXED_BOOTSTRAPPER_URL,
    SEMANTIC_RELATIONS,
    SUPPLIER_CRITERION_ID,
    VerificationAuthority,
    authenticate_installed_implementation,
    canonical_json_lf,
    chain_call_input_sha256,
    evaluate_observation,
    policy_input_sha256,
    sha256_hex,
    strict_json_object,
    verify_open_file,
)
from s0_windows_authenticode_verifier.contract import (  # noqa: E402
    CHAIN_ENGINE,
    CHAIN_FLAGS,
    CODE_SIGNING_EKU,
    EVENT_SEQUENCE,
    MAX_REVOCATION_FRESHNESS_SECONDS,
    OBSERVATION_SCHEMA_ID,
    SUPPLIER_CRITERION_COMPONENTS,
    TIME_STAMPING_EKU,
    URL_RETRIEVAL_TIMEOUT_MS,
    WINTRUST_ACTION_GUID,
    WINTRUST_PROV_FLAGS,
)


def _authority() -> VerificationAuthority:
    return VerificationAuthority("0" * 63 + "1", "1" * 64, "2" * 64, "3" * 64)


def _element(index: int, count: int, digest: str, reference_time: int) -> dict[str, object]:
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
        "freshness_reference_filetime": None if root else reference_time,
        "disallowed": False,
    }


def _chain(digests: list[str], reference_time: int) -> list[dict[str, object]]:
    return [_element(index, len(digests), digest, reference_time) for index, digest in enumerate(digests)]


def _chain_call(
    chain: list[dict[str, object]], leaf: str, verification_time: int, reference_time: int, eku: str
) -> dict[str, object]:
    value: dict[str, object] = {
        "api": "CertGetCertificateChain",
        "chain_engine": CHAIN_ENGINE,
        "flags": list(CHAIN_FLAGS),
        "url_retrieval_timeout_ms": URL_RETRIEVAL_TIMEOUT_MS,
        "leaf_certificate_der_sha256": leaf,
        "verification_time_filetime": verification_time,
        "reference_time_filetime": reference_time,
        "requested_eku": eku,
        "additional_candidate_store_used": False,
        "api_return": True,
        "output_chain_sha256": sha256_hex(canonical_json_lf(chain)),
        "input_sha256": "",
    }
    value["input_sha256"] = chain_call_input_sha256(value)
    return value


def _policy(
    policy_id: str, chain_sha256: str, verification_time: int, extra: dict[str, object]
) -> dict[str, object]:
    value: dict[str, object] = {
        "policy_id": policy_id,
        "chain_context_sha256": chain_sha256,
        "verification_time_filetime": verification_time,
        "flags": 0,
        "extra_policy": extra,
        "api_return": True,
        "policy_error": 0,
        "input_sha256": "",
    }
    value["input_sha256"] = policy_input_sha256(value)
    return value


def _observation(authority: VerificationAuthority) -> dict[str, object]:
    signing_time = 10_000_000_000
    reference_time = signing_time + 50_000_000
    state_id = "4" * 64
    signer_provider = ["5" * 64, "6" * 64, "7" * 64]
    timestamp_provider = ["8" * 64, "9" * 64, "a" * 64]
    signer_chain = _chain(signer_provider, reference_time)
    timestamp_chain = _chain(timestamp_provider, reference_time)
    signer_call = _chain_call(signer_chain, signer_provider[0], signing_time, reference_time, CODE_SIGNING_EKU)
    timestamp_call = _chain_call(timestamp_chain, timestamp_provider[0], signing_time, reference_time, TIME_STAMPING_EKU)
    identity = {
        "volume_serial_hex": "0000000000000001",
        "file_id_hex": "00000000000000000000000000000002",
        "reparse_point": False,
        "byte_length": 1234,
    }
    return {
        "schema_id": OBSERVATION_SCHEMA_ID,
        "native_collection_status": "COMPLETED-NONAUTHORITATIVE-OBSERVATION",
        "implementation_manifest_sha256": authority.implementation_manifest_sha256,
        "policy_manifest_sha256": authority.policy_manifest_sha256,
        "native_verifier_manifest_sha256": authority.native_verifier_manifest_sha256,
        "semantic_validator_manifest_sha256": authority.semantic_validator_manifest_sha256,
        "supplier": {
            "criterion_id": SUPPLIER_CRITERION_ID,
            "components": list(SUPPLIER_CRITERION_COMPONENTS),
            "official_leaf_guarantee_claimed": False,
            "project_reauthorization_acknowledged": True,
        },
        "requested_uri": FIXED_BOOTSTRAPPER_URL,
        "final_uri": FIXED_BOOTSTRAPPER_URL,
        "redirect_count": 0,
        "original_file_handle_retained": True,
        "file_identities": {
            "download_close": copy.deepcopy(identity),
            "post_signature": copy.deepcopy(identity),
            "preexecution": copy.deepcopy(identity),
        },
        "byte_sha256": {
            "download_close": "b" * 64,
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
                "provider_state_id": state_id if 2 <= index <= 11 else None,
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
            "signing_time_filetime": signing_time,
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
            "pre_snapshot_sha256": "c" * 64,
            "post_snapshot_sha256": "c" * 64,
            "snapshot_scope": [
                "LOCAL-MACHINE-ROOT",
                "LOCAL-MACHINE-CA",
                "LOCAL-MACHINE-DISALLOWED",
                "EFFECTIVE-WINDOWS-DISALLOWED-CTL",
            ],
            "store_mutation_count": 0,
        },
        "process_count_before_decision": 0,
    }


def _evaluate(value: dict[str, object], authority: VerificationAuthority | None = None):
    chosen = authority or _authority()
    return evaluate_observation(canonical_json_lf(value), chosen)


class AuthenticodeVerifierTests(unittest.TestCase):
    def test_installed_implementation_and_submanifests_authenticate(self) -> None:
        manifest = ROOT / "verification" / "implementation-files.sha256"
        pin = sha256_hex(manifest.read_bytes())
        authority = authenticate_installed_implementation(pin)
        self.assertEqual(pin, authority.implementation_manifest_sha256)
        self.assertEqual(
            sha256_hex((ROOT / "verification" / "policy-contract-files.sha256").read_bytes()),
            authority.policy_manifest_sha256,
        )
        self.assertEqual(
            sha256_hex((ROOT / "verification" / "native-verifier-files.sha256").read_bytes()),
            authority.native_verifier_manifest_sha256,
        )
        self.assertEqual(
            sha256_hex((ROOT / "verification" / "semantic-validator-files.sha256").read_bytes()),
            authority.semantic_validator_manifest_sha256,
        )

    def test_valid_observation_computes_all_relations_and_never_grants_process(self) -> None:
        authority = _authority()
        raw = canonical_json_lf(_observation(authority))
        result = evaluate_observation(raw, authority)
        self.assertTrue(result.trust_policy_pass)
        self.assertFalse(result.process_authority_granted)
        self.assertEqual((), result.failure_relations)
        self.assertEqual(39, len(SEMANTIC_RELATIONS))
        self.assertEqual(sha256_hex(raw), result.observation_sha256)
        self.assertEqual(result.trace_sha256, sha256_hex(result.trace_raw))
        self.assertEqual(result.decision_sha256, sha256_hex(result.decision_raw))
        self.assertEqual(result, evaluate_observation(raw, authority))

    def test_observation_bytes_are_canonical_and_actual_hash_is_bound(self) -> None:
        authority = _authority()
        raw = canonical_json_lf(_observation(authority))
        noncanonical = b" " + raw
        result = evaluate_observation(noncanonical, authority)
        self.assertFalse(result.trust_policy_pass)
        self.assertEqual(sha256_hex(noncanonical), result.observation_sha256)
        self.assertEqual(
            ("observation-sha256-is-computed-from-canonical-input-bytes",),
            result.failure_relations,
        )

    def test_all_three_manifest_authorities_are_cross_bound(self) -> None:
        authority = _authority()
        for field in (
            "implementation_manifest_sha256",
            "policy_manifest_sha256",
            "native_verifier_manifest_sha256",
            "semantic_validator_manifest_sha256",
        ):
            with self.subTest(field=field):
                value = _observation(authority)
                value[field] = "d" * 64
                self.assertFalse(_evaluate(value, authority).trust_policy_pass)

    def test_raw_record_cannot_supply_decision_or_relation_results(self) -> None:
        value = _observation(_authority())
        value["trust_policy_pass"] = True
        self.assertFalse(_evaluate(value).trust_policy_pass)

    def test_event_order_state_binding_and_early_close_reject(self) -> None:
        for mutate in (
            lambda value: value["events"].__setitem__(9, value["events"][11]),
            lambda value: value["events"][5].__setitem__("provider_state_id", "d" * 64),
            lambda value: value["wintrust"].__setitem__("close_return", 1),
        ):
            value = _observation(_authority())
            mutate(value)
            self.assertFalse(_evaluate(value).trust_policy_pass)

    def test_policy_chain_time_and_input_hash_substitution_reject(self) -> None:
        mutations = (
            ("signer", "authenticode_policy", "chain_context_sha256", "d" * 64),
            ("signer", "microsoft_root_policy", "verification_time_filetime", 123),
            ("timestamp", "timestamp_policy", "input_sha256", "d" * 64),
            ("timestamp", "chain_call", "verification_time_filetime", 123),
        )
        for first, second, field, replacement in mutations:
            with self.subTest(field=f"{first}.{second}.{field}"):
                value = _observation(_authority())
                value[first][second][field] = replacement
                self.assertFalse(_evaluate(value).trust_policy_pass)

    def test_countersigner_index_and_provider_state_substitution_reject(self) -> None:
        for field, replacement in (("countersigner_index", 1), ("provider_state_id", "d" * 64)):
            value = _observation(_authority())
            value["timestamp"][field] = replacement
            self.assertFalse(_evaluate(value).trust_policy_pass)

    def test_stale_unknown_or_wrong_reference_revocation_rejects(self) -> None:
        value = _observation(_authority())
        value["signer"]["rebuilt_chain"][0]["freshness_age_seconds"] = MAX_REVOCATION_FRESHNESS_SECONDS + 1
        self.assertFalse(_evaluate(value).trust_policy_pass)

        value = _observation(_authority())
        value["timestamp"]["rebuilt_chain"][1]["revocation_result"] = "UNKNOWN"
        self.assertFalse(_evaluate(value).trust_policy_pass)

        value = _observation(_authority())
        value["signer"]["rebuilt_chain"][0]["freshness_reference_filetime"] += 1
        self.assertFalse(_evaluate(value).trust_policy_pass)

    def test_supplier_composite_is_explicit_not_official_leaf_claim(self) -> None:
        mutations = (
            ("official_leaf_guarantee_claimed", True),
            ("project_reauthorization_acknowledged", False),
            ("criterion_id", "OTHER"),
        )
        for field, replacement in mutations:
            value = _observation(_authority())
            value["supplier"][field] = replacement
            self.assertFalse(_evaluate(value).trust_policy_pass)

        value = _observation(_authority())
        value["signer"]["microsoft_root_policy"]["policy_error"] = 1
        self.assertFalse(_evaluate(value).trust_policy_pass)

    def test_file_uri_trust_snapshot_and_process_mutations_reject(self) -> None:
        values: list[dict[str, object]] = []
        value = _observation(_authority()); value["final_uri"] += "?changed=1"; values.append(value)
        value = _observation(_authority()); value["file_identities"]["preexecution"]["file_id_hex"] = "f" * 32; values.append(value)
        value = _observation(_authority()); value["byte_sha256"]["post_signature"] = "f" * 64; values.append(value)
        value = _observation(_authority()); value["trust_authority"]["post_snapshot_sha256"] = "f" * 64; values.append(value)
        value = _observation(_authority()); value["process_count_before_decision"] = 1; values.append(value)
        for item in values:
            self.assertFalse(_evaluate(item).trust_policy_pass)

    def test_invalid_native_handle_fails_closed_without_process_authority(self) -> None:
        implementation_pin = sha256_hex(
            (ROOT / "verification" / "implementation-files.sha256").read_bytes()
        )
        result = verify_open_file(
            full_path=str(Path.cwd() / "never-opened.exe"),
            file_handle=0,
            implementation_manifest_sha256=implementation_pin,
            requested_uri=FIXED_BOOTSTRAPPER_URL,
            final_uri=FIXED_BOOTSTRAPPER_URL,
            redirect_count=0,
        )
        self.assertFalse(result.trust_policy_pass)
        self.assertFalse(result.process_authority_granted)

    def test_strict_parser_rejects_duplicate_key(self) -> None:
        with self.assertRaises(ValueError):
            strict_json_object(b'{"a":1,"a":2}\n')


if __name__ == "__main__":
    unittest.main()

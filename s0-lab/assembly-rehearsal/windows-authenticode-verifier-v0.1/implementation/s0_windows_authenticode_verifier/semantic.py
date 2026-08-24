"""Deterministic semantic validator over one canonical native observation."""

from __future__ import annotations

import re
from typing import Callable, Mapping

from .canonical import (
    VerificationError,
    canonical_json_lf,
    exact_bool,
    exact_int,
    exact_keys,
    exact_list,
    exact_text,
    require_sha256,
    sha256_hex,
    strict_json_object,
)
from .contract import (
    CHAIN_ENGINE,
    CHAIN_FLAGS,
    CODE_SIGNING_EKU,
    DECISION_SCHEMA_ID,
    EVENT_SEQUENCE,
    FIXED_BOOTSTRAPPER_URL,
    MAX_REVOCATION_FRESHNESS_SECONDS,
    OBSERVATION_SCHEMA_ID,
    SEMANTIC_RELATIONS,
    SUPPLIER_CRITERION_COMPONENTS,
    SUPPLIER_CRITERION_ID,
    TIME_STAMPING_EKU,
    TRACE_SCHEMA_ID,
    URL_RETRIEVAL_TIMEOUT_MS,
    WINTRUST_ACTION_GUID,
    WINTRUST_PROV_FLAGS,
)
from .model import VerificationAuthority, VerificationResult


_VOLUME = re.compile(r"^[0-9a-f]{16}$")
_FILE_ID = re.compile(r"^[0-9a-f]{32}$")
_TRUST_SCOPE = (
    "LOCAL-MACHINE-ROOT",
    "LOCAL-MACHINE-CA",
    "LOCAL-MACHINE-DISALLOWED",
    "EFFECTIVE-WINDOWS-DISALLOWED-CTL",
)


def _safe(check: Callable[[], bool]) -> bool:
    try:
        return check() is True
    except (KeyError, IndexError, TypeError, ValueError, VerificationError):
        return False


def _obj(value: object, keys: tuple[str, ...], name: str) -> dict[str, object]:
    return exact_keys(value, keys, name=name)


def _file_identity(value: object) -> dict[str, object]:
    item = _obj(value, ("volume_serial_hex", "file_id_hex", "reparse_point", "byte_length"), "file identity")
    if type(item["volume_serial_hex"]) is not str or _VOLUME.fullmatch(item["volume_serial_hex"]) is None:
        raise VerificationError("volume serial differs")
    if type(item["file_id_hex"]) is not str or _FILE_ID.fullmatch(item["file_id_hex"]) is None:
        raise VerificationError("file ID differs")
    exact_bool(item["reparse_point"], name="reparse point")
    exact_int(item["byte_length"], name="byte length", minimum=1)
    return item


def _chain(value: object, name: str) -> list[object]:
    items = exact_list(value, name=name, minimum=2)
    for index, raw in enumerate(items):
        element = _obj(
            raw,
            (
                "position",
                "role",
                "certificate_der_sha256",
                "trust_error_status",
                "trust_info_status",
                "revocation_result",
                "has_freshness_time",
                "freshness_age_seconds",
                "freshness_reference_filetime",
                "disallowed",
            ),
            f"{name} element",
        )
        if exact_int(element["position"], name="chain position", minimum=0) != index:
            raise VerificationError("chain positions are not contiguous")
        expected_role = "LEAF" if index == 0 else "ROOT" if index == len(items) - 1 else "INTERMEDIATE"
        if element["role"] != expected_role:
            raise VerificationError("chain role order differs")
        require_sha256(element["certificate_der_sha256"], name="certificate DER")
        exact_int(element["trust_error_status"], name="trust error", minimum=0)
        exact_int(element["trust_info_status"], name="trust info", minimum=0)
        exact_bool(element["has_freshness_time"], name="freshness presence")
        exact_bool(element["disallowed"], name="disallowed status")
        if element["freshness_age_seconds"] is not None:
            exact_int(element["freshness_age_seconds"], name="freshness age", minimum=0)
        if element["freshness_reference_filetime"] is not None:
            exact_int(element["freshness_reference_filetime"], name="freshness reference", minimum=1)
    return items


def _chain_sha256(chain: list[object]) -> str:
    return sha256_hex(canonical_json_lf(chain))


def _provider_chain(value: object, name: str) -> list[str]:
    items = exact_list(value, name=name, minimum=2)
    return [require_sha256(item, name=f"{name} certificate") for item in items]


def _chain_call(value: object) -> dict[str, object]:
    call = _obj(
        value,
        (
            "api",
            "chain_engine",
            "flags",
            "url_retrieval_timeout_ms",
            "leaf_certificate_der_sha256",
            "verification_time_filetime",
            "reference_time_filetime",
            "requested_eku",
            "additional_candidate_store_used",
            "api_return",
            "output_chain_sha256",
            "input_sha256",
        ),
        "chain call",
    )
    require_sha256(call["leaf_certificate_der_sha256"], name="chain leaf")
    require_sha256(call["output_chain_sha256"], name="chain output")
    require_sha256(call["input_sha256"], name="chain input")
    exact_int(call["verification_time_filetime"], name="chain verification time", minimum=1)
    exact_int(call["reference_time_filetime"], name="chain reference time", minimum=1)
    exact_bool(call["additional_candidate_store_used"], name="candidate store")
    exact_bool(call["api_return"], name="chain API return")
    return call


def chain_call_input_sha256(call: Mapping[str, object]) -> str:
    return sha256_hex(
        canonical_json_lf(
            {
                "additional_candidate_store_used": call["additional_candidate_store_used"],
                "api": call["api"],
                "chain_engine": call["chain_engine"],
                "flags": call["flags"],
                "leaf_certificate_der_sha256": call["leaf_certificate_der_sha256"],
                "reference_time_filetime": call["reference_time_filetime"],
                "requested_eku": call["requested_eku"],
                "url_retrieval_timeout_ms": call["url_retrieval_timeout_ms"],
                "verification_time_filetime": call["verification_time_filetime"],
            }
        )
    )


def _policy(value: object) -> dict[str, object]:
    policy = _obj(
        value,
        (
            "policy_id",
            "chain_context_sha256",
            "verification_time_filetime",
            "flags",
            "extra_policy",
            "api_return",
            "policy_error",
            "input_sha256",
        ),
        "chain policy call",
    )
    require_sha256(policy["chain_context_sha256"], name="policy chain context")
    require_sha256(policy["input_sha256"], name="policy input")
    exact_int(policy["verification_time_filetime"], name="policy verification time", minimum=1)
    exact_int(policy["flags"], name="policy flags", minimum=0)
    exact_bool(policy["api_return"], name="policy API return")
    exact_int(policy["policy_error"], name="policy error", minimum=0)
    if type(policy["extra_policy"]) is not dict:
        raise VerificationError("extra policy input differs")
    return policy


def policy_input_sha256(policy: Mapping[str, object]) -> str:
    return sha256_hex(
        canonical_json_lf(
            {
                "chain_context_sha256": policy["chain_context_sha256"],
                "extra_policy": policy["extra_policy"],
                "flags": policy["flags"],
                "policy_id": policy["policy_id"],
                "verification_time_filetime": policy["verification_time_filetime"],
            }
        )
    )


def _fresh_nonroot(chain: list[object], reference_time: int) -> bool:
    for raw in chain[:-1]:
        element = raw
        if (
            element["trust_error_status"] != 0
            or element["revocation_result"] != "GOOD"
            or element["has_freshness_time"] is not True
            or type(element["freshness_age_seconds"]) is not int
            or not 0 <= element["freshness_age_seconds"] <= MAX_REVOCATION_FRESHNESS_SECONDS
            or element["freshness_reference_filetime"] != reference_time
            or element["disallowed"] is not False
        ):
            return False
    return True


def _trusted_root(chain: list[object]) -> bool:
    root = chain[-1]
    return (
        root["role"] == "ROOT"
        and root["trust_error_status"] == 0
        and root["revocation_result"] == "ROOT-NOT-CHECKED"
        and root["has_freshness_time"] is False
        and root["freshness_age_seconds"] is None
        and root["disallowed"] is False
    )


def _reject_malformed(raw: bytes, authority: VerificationAuthority, reason: str) -> VerificationResult:
    observation_sha256 = sha256_hex(raw)
    rows = [
        {"id": relation, "index": index, "result": False}
        for index, relation in enumerate(SEMANTIC_RELATIONS)
    ]
    trace_raw = canonical_json_lf(
        {
            "failure_count": len(rows),
            "observation_sha256": observation_sha256,
            "relations": rows,
            "schema_id": TRACE_SCHEMA_ID,
        }
    )
    trace_sha256 = sha256_hex(trace_raw)
    decision_raw = canonical_json_lf(
        {
            "failure_class": reason,
            "failure_relations": list(SEMANTIC_RELATIONS),
            "implementation_manifest_sha256": authority.implementation_manifest_sha256,
            "native_verifier_manifest_sha256": authority.native_verifier_manifest_sha256,
            "observation_sha256": observation_sha256,
            "policy_manifest_sha256": authority.policy_manifest_sha256,
            "process_authority_granted": False,
            "schema_id": DECISION_SCHEMA_ID,
            "semantic_trace_sha256": trace_sha256,
            "semantic_validator_manifest_sha256": authority.semantic_validator_manifest_sha256,
            "supplier_criterion_id": authority.supplier_criterion_id,
            "terminal_decision": "REJECTED-BEFORE-PROCESS",
            "trust_policy_pass": False,
        }
    )
    return VerificationResult(
        observation_sha256,
        trace_raw,
        trace_sha256,
        decision_raw,
        sha256_hex(decision_raw),
        False,
        SEMANTIC_RELATIONS,
    )


def evaluate_observation(raw: bytes, authority: VerificationAuthority) -> VerificationResult:
    """Compute every relation from bound observation bytes; never trust booleans."""

    if type(raw) is not bytes:
        raise VerificationError("observation input must be exact bytes")
    try:
        observation = strict_json_object(raw)
        exact_keys(
            observation,
            (
                "schema_id",
                "native_collection_status",
                "implementation_manifest_sha256",
                "policy_manifest_sha256",
                "native_verifier_manifest_sha256",
                "semantic_validator_manifest_sha256",
                "supplier",
                "requested_uri",
                "final_uri",
                "redirect_count",
                "original_file_handle_retained",
                "file_identities",
                "byte_sha256",
                "wintrust",
                "events",
                "signer",
                "timestamp",
                "trust_authority",
                "process_count_before_decision",
            ),
            name="observation",
        )
    except VerificationError as error:
        return _reject_malformed(raw, authority, f"malformed-observation:{error}")

    observation_sha256 = sha256_hex(raw)
    relations: list[bool] = []
    add = relations.append

    add(_safe(lambda: observation["implementation_manifest_sha256"] == authority.implementation_manifest_sha256))
    add(_safe(lambda: observation["policy_manifest_sha256"] == authority.policy_manifest_sha256))
    add(_safe(lambda: observation["native_verifier_manifest_sha256"] == authority.native_verifier_manifest_sha256))
    add(_safe(lambda: observation["semantic_validator_manifest_sha256"] == authority.semantic_validator_manifest_sha256))
    add(_safe(lambda: observation["schema_id"] == OBSERVATION_SCHEMA_ID and canonical_json_lf(observation) == raw and sha256_hex(raw) == observation_sha256))
    add(_safe(lambda: observation["requested_uri"] == FIXED_BOOTSTRAPPER_URL and observation["final_uri"] == FIXED_BOOTSTRAPPER_URL))
    add(_safe(lambda: exact_int(observation["redirect_count"], name="redirect count", minimum=0) == 0))
    add(_safe(lambda: exact_bool(observation["original_file_handle_retained"], name="retained handle") is True))

    identities = observation.get("file_identities")
    identity_values: list[dict[str, object]] = []
    try:
        identity_map = _obj(identities, ("download_close", "post_signature", "preexecution"), "file identities")
        identity_values = [_file_identity(identity_map[name]) for name in ("download_close", "post_signature", "preexecution")]
    except VerificationError:
        identity_values = []
    add(_safe(lambda: len(identity_values) == 3 and identity_values[0] == identity_values[1] == identity_values[2]))
    add(_safe(lambda: len(identity_values) == 3 and all(item["reparse_point"] is False for item in identity_values)))
    add(_safe(lambda: len(identity_values) == 3 and len({item["byte_length"] for item in identity_values}) == 1 and identity_values[0]["byte_length"] > 0))

    hashes = observation.get("byte_sha256")
    try:
        hash_map = _obj(hashes, ("download_close", "post_signature", "preexecution"), "byte hashes")
        hash_values = [require_sha256(hash_map[name], name=f"{name} hash") for name in ("download_close", "post_signature", "preexecution")]
    except VerificationError:
        hash_values = []
    add(_safe(lambda: len(hash_values) == 3 and hash_values[0] == hash_values[1] == hash_values[2]))

    try:
        wintrust = _obj(
            observation["wintrust"],
            (
                "action_guid", "window_handle", "ui_choice", "ui_context", "union_choice",
                "revocation_checks", "prov_flags", "state_action_verify", "verify_return",
                "state_action_close", "close_return", "provider_state_id",
                "candidate_callback_used", "candidate_store_used", "custom_parser_used",
            ),
            "wintrust",
        )
    except VerificationError:
        wintrust = {}
    add(_safe(lambda: wintrust["action_guid"] == WINTRUST_ACTION_GUID and wintrust["window_handle"] == "INVALID_HANDLE_VALUE" and wintrust["ui_choice"] == "WTD_UI_NONE" and wintrust["ui_context"] == "WTD_UICONTEXT_INSTALL" and wintrust["union_choice"] == "WTD_CHOICE_FILE" and wintrust["revocation_checks"] == "WTD_REVOKE_NONE" and tuple(wintrust["prov_flags"]) == WINTRUST_PROV_FLAGS and wintrust["state_action_verify"] == "WTD_STATEACTION_VERIFY" and wintrust["state_action_close"] == "WTD_STATEACTION_CLOSE"))
    add(_safe(lambda: exact_int(wintrust["verify_return"], name="WinVerifyTrust return") == 0))

    events = observation.get("events")
    event_rows: list[dict[str, object]] = []
    try:
        raw_events = exact_list(events, name="events", minimum=len(EVENT_SEQUENCE))
        if len(raw_events) != len(EVENT_SEQUENCE):
            raise VerificationError("event count differs")
        for index, raw_event in enumerate(raw_events):
            event = _obj(raw_event, ("sequence", "kind", "provider_state_id"), "event")
            if exact_int(event["sequence"], name="event sequence", minimum=0) != index or event["kind"] != EVENT_SEQUENCE[index]:
                raise VerificationError("event order differs")
            event_rows.append(event)
    except VerificationError:
        event_rows = []
    add(_safe(lambda: len(event_rows) == len(EVENT_SEQUENCE) and require_sha256(wintrust["provider_state_id"], name="provider state") == wintrust["provider_state_id"] and all(event_rows[index]["provider_state_id"] == wintrust["provider_state_id"] for index in range(2, 12)) and all(event_rows[index]["provider_state_id"] is None for index in (0, 1, 12))))
    add(_safe(lambda: exact_int(wintrust["close_return"], name="WinVerifyTrust close return") == 0 and event_rows[11]["kind"] == "STATE-CLOSED" and event_rows[9]["kind"] == "TIMESTAMP-POLICY-EVALUATED"))

    try:
        signer = _obj(observation["signer"], ("leaf_certificate_der_sha256", "provider_chain", "rebuilt_chain", "chain_call", "code_signing_eku_present", "authenticode_policy", "microsoft_root_policy"), "signer")
        signer_leaf = require_sha256(signer["leaf_certificate_der_sha256"], name="signer leaf")
        signer_provider = _provider_chain(signer["provider_chain"], "provider signer chain")
        signer_rebuilt = _chain(signer["rebuilt_chain"], "rebuilt signer chain")
        signer_call = _chain_call(signer["chain_call"])
        signer_auth = _policy(signer["authenticode_policy"])
        signer_ms = _policy(signer["microsoft_root_policy"])
    except VerificationError:
        signer = {}; signer_leaf = ""; signer_provider = []; signer_rebuilt = []; signer_call = {}; signer_auth = {}; signer_ms = {}
    add(_safe(lambda: signer_leaf == signer_provider[0]))
    add(_safe(lambda: signer_provider == [element["certificate_der_sha256"] for element in signer_rebuilt]))
    add(_safe(lambda: signer_call["api"] == "CertGetCertificateChain" and signer_call["leaf_certificate_der_sha256"] == signer_leaf and signer_call["output_chain_sha256"] == _chain_sha256(signer_rebuilt) and signer_call["input_sha256"] == chain_call_input_sha256(signer_call) and signer_call["api_return"] is True))
    add(_safe(lambda: signer_auth["policy_id"] == "CERT_CHAIN_POLICY_AUTHENTICODE" and signer_auth["chain_context_sha256"] == signer_call["output_chain_sha256"] and signer_auth["verification_time_filetime"] == signer_call["verification_time_filetime"] and signer_auth["flags"] == 0 and signer_auth["extra_policy"] == {"pv_extra_policy_para": "NULL"} and signer_auth["input_sha256"] == policy_input_sha256(signer_auth) and signer_auth["api_return"] is True and signer_auth["policy_error"] == 0))
    add(_safe(lambda: signer_ms["policy_id"] == "CERT_CHAIN_POLICY_MICROSOFT_ROOT" and signer_ms["chain_context_sha256"] == signer_call["output_chain_sha256"] and signer_ms["verification_time_filetime"] == signer_call["verification_time_filetime"] and signer_ms["flags"] == 0 and signer_ms["extra_policy"] == {"test_root_enabled": False} and signer_ms["input_sha256"] == policy_input_sha256(signer_ms) and signer_ms["api_return"] is True and signer_ms["policy_error"] == 0))
    add(_safe(lambda: exact_bool(signer["code_signing_eku_present"], name="code signing EKU") is True and signer_call["requested_eku"] == CODE_SIGNING_EKU))

    try:
        supplier = _obj(observation["supplier"], ("criterion_id", "components", "official_leaf_guarantee_claimed", "project_reauthorization_acknowledged"), "supplier")
    except VerificationError:
        supplier = {}
    add(_safe(lambda: supplier["criterion_id"] == authority.supplier_criterion_id == SUPPLIER_CRITERION_ID and tuple(supplier["components"]) == SUPPLIER_CRITERION_COMPONENTS and supplier["official_leaf_guarantee_claimed"] is False and supplier["project_reauthorization_acknowledged"] is True))

    try:
        timestamp = _obj(observation["timestamp"], ("present", "kind", "signer_index", "countersigner_index", "provider_state_id", "signing_time_filetime", "leaf_certificate_der_sha256", "provider_chain", "rebuilt_chain", "chain_call", "timestamp_policy"), "timestamp")
        timestamp_leaf = require_sha256(timestamp["leaf_certificate_der_sha256"], name="timestamp leaf")
        timestamp_provider = _provider_chain(timestamp["provider_chain"], "provider timestamp chain")
        timestamp_rebuilt = _chain(timestamp["rebuilt_chain"], "rebuilt timestamp chain")
        timestamp_call = _chain_call(timestamp["chain_call"])
        timestamp_policy = _policy(timestamp["timestamp_policy"])
        signing_time = exact_int(timestamp["signing_time_filetime"], name="signing time", minimum=1)
    except VerificationError:
        timestamp = {}; timestamp_leaf = ""; timestamp_provider = []; timestamp_rebuilt = []; timestamp_call = {}; timestamp_policy = {}; signing_time = 0
    add(_safe(lambda: timestamp["present"] is True and timestamp["kind"] == "WINDOWS-PROVIDER-TIMESTAMP-SIGNER"))
    add(_safe(lambda: timestamp["signer_index"] == 0 and timestamp["countersigner_index"] == 0 and timestamp["provider_state_id"] == wintrust["provider_state_id"]))
    add(_safe(lambda: timestamp_leaf == timestamp_provider[0]))
    add(_safe(lambda: timestamp_provider == [element["certificate_der_sha256"] for element in timestamp_rebuilt]))
    add(_safe(lambda: timestamp_call["api"] == "CertGetCertificateChain" and timestamp_call["leaf_certificate_der_sha256"] == timestamp_leaf and timestamp_call["verification_time_filetime"] == signing_time and timestamp_call["output_chain_sha256"] == _chain_sha256(timestamp_rebuilt) and timestamp_call["input_sha256"] == chain_call_input_sha256(timestamp_call) and timestamp_call["api_return"] is True))
    add(_safe(lambda: timestamp_policy["policy_id"] == "CERT_CHAIN_POLICY_AUTHENTICODE_TS" and timestamp_policy["chain_context_sha256"] == timestamp_call["output_chain_sha256"] and timestamp_policy["verification_time_filetime"] == signing_time and timestamp_policy["flags"] == 0 and timestamp_policy["extra_policy"] == {"pv_extra_policy_para": "NULL"} and timestamp_policy["input_sha256"] == policy_input_sha256(timestamp_policy) and timestamp_policy["api_return"] is True and timestamp_policy["policy_error"] == 0))
    add(_safe(lambda: tuple(signer_call["flags"]) == CHAIN_FLAGS and tuple(timestamp_call["flags"]) == CHAIN_FLAGS and signer_call["chain_engine"] == timestamp_call["chain_engine"] == CHAIN_ENGINE and signer_call["url_retrieval_timeout_ms"] == timestamp_call["url_retrieval_timeout_ms"] == URL_RETRIEVAL_TIMEOUT_MS and signer_call["additional_candidate_store_used"] is False and timestamp_call["additional_candidate_store_used"] is False and timestamp_call["requested_eku"] == TIME_STAMPING_EKU))
    add(_safe(lambda: _fresh_nonroot(signer_rebuilt, signer_call["reference_time_filetime"])))
    add(_safe(lambda: _fresh_nonroot(timestamp_rebuilt, timestamp_call["reference_time_filetime"])))
    add(_safe(lambda: signer_call["reference_time_filetime"] == timestamp_call["reference_time_filetime"] and signer_call["reference_time_filetime"] >= signing_time and all(element["freshness_reference_filetime"] == signer_call["reference_time_filetime"] for element in signer_rebuilt[:-1] + timestamp_rebuilt[:-1])))
    add(_safe(lambda: _trusted_root(signer_rebuilt) and _trusted_root(timestamp_rebuilt)))

    try:
        trust = _obj(observation["trust_authority"], ("pre_snapshot_sha256", "post_snapshot_sha256", "snapshot_scope", "store_mutation_count"), "trust authority")
        pre_snapshot = require_sha256(trust["pre_snapshot_sha256"], name="pre trust snapshot")
        post_snapshot = require_sha256(trust["post_snapshot_sha256"], name="post trust snapshot")
    except VerificationError:
        trust = {}; pre_snapshot = ""; post_snapshot = ""
    add(_safe(lambda: pre_snapshot == post_snapshot and tuple(trust["snapshot_scope"]) == _TRUST_SCOPE))
    add(_safe(lambda: exact_int(trust["store_mutation_count"], name="store mutation count", minimum=0) == 0))
    add(_safe(lambda: wintrust["candidate_callback_used"] is False and wintrust["candidate_store_used"] is False and wintrust["custom_parser_used"] is False))
    add(_safe(lambda: exact_int(observation["process_count_before_decision"], name="process count", minimum=0) == 0 and observation["native_collection_status"] == "COMPLETED-NONAUTHORITATIVE-OBSERVATION"))
    add(True)

    if len(relations) != len(SEMANTIC_RELATIONS):
        raise VerificationError("semantic implementation relation count differs")
    relation_rows = [
        {"id": relation, "index": index, "result": relations[index]}
        for index, relation in enumerate(SEMANTIC_RELATIONS)
    ]
    failures = tuple(
        relation for relation, result in zip(SEMANTIC_RELATIONS, relations) if not result
    )
    trace_raw = canonical_json_lf(
        {
            "failure_count": len(failures),
            "observation_sha256": observation_sha256,
            "relations": relation_rows,
            "schema_id": TRACE_SCHEMA_ID,
        }
    )
    trace_sha256 = sha256_hex(trace_raw)
    passed = not failures
    decision_raw = canonical_json_lf(
        {
            "failure_class": None if passed else "semantic-relation-rejected",
            "failure_relations": list(failures),
            "implementation_manifest_sha256": authority.implementation_manifest_sha256,
            "native_verifier_manifest_sha256": authority.native_verifier_manifest_sha256,
            "observation_sha256": observation_sha256,
            "policy_manifest_sha256": authority.policy_manifest_sha256,
            "process_authority_granted": False,
            "schema_id": DECISION_SCHEMA_ID,
            "semantic_trace_sha256": trace_sha256,
            "semantic_validator_manifest_sha256": authority.semantic_validator_manifest_sha256,
            "supplier_criterion_id": authority.supplier_criterion_id,
            "terminal_decision": "PASS-TRUST-POLICY-FOR-LATER-GATE-CONSIDERATION" if passed else "REJECTED-BEFORE-PROCESS",
            "trust_policy_pass": passed,
        }
    )
    return VerificationResult(
        observation_sha256,
        trace_raw,
        trace_sha256,
        decision_raw,
        sha256_hex(decision_raw),
        passed,
        failures,
    )

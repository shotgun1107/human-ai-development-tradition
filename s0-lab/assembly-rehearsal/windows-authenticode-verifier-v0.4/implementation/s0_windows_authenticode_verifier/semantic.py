"""Deterministic v0.3 semantic validator over one canonical observation."""

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
    require_sha256,
    sha256_hex,
    strict_json_object,
)
from .contract import (
    ACQUISITION_HANDLE_CONTRACT,
    ACQUISITION_PATH_SEMANTICS_ID,
    ACQUISITION_SCHEMA_ID,
    CHAIN_ENGINE,
    CHAIN_FLAGS,
    CLOCK_DISCONTINUITY_TOLERANCE_SECONDS,
    CODE_SIGNING_EKU,
    DECISION_SCHEMA_ID,
    EVENT_SEQUENCE,
    FILETIME_TICKS_PER_SECOND,
    FIXED_BOOTSTRAPPER_URL,
    IMMUTABLE_LEASE_CONTRACT,
    MAX_CANDIDATE_BYTES,
    MAX_CHAIN_CALL_DURATION_SECONDS,
    MAX_OBSERVATION_BYTES,
    MAX_PROVIDER_CHAIN_CERTIFICATES,
    MAX_REBUILT_CHAIN_CERTIFICATES,
    MAX_REVOCATION_FRESHNESS_SECONDS,
    MAX_STORE_ENTRIES,
    OBSERVATION_SCHEMA_ID,
    RUNTIME_AUTHORITY_SCOPE,
    SEMANTIC_RELATIONS,
    SUPPLIER_CRITERION_COMPONENTS,
    SUPPLIER_CRITERION_ID,
    TIME_STAMPING_EKU,
    TRACE_SCHEMA_ID,
    TRUST_SNAPSHOT_SCOPE,
    URL_RETRIEVAL_TIMEOUT_MS,
    WINTRUST_ACTION_GUID,
    WINTRUST_PROV_FLAGS,
)
from .model import VerificationAuthority, VerificationResult


_VOLUME = re.compile(r"^[0-9a-f]{16}$")
_FILE_ID = re.compile(r"^[0-9a-f]{32}$")
_HANDLE = re.compile(r"^[0-9a-f]{16}$")
_FILETIME = re.compile(r"^[0-9a-f]{16}$")
_VOLUME_GUID_PATH = re.compile(
    r"^\\\\\?\\Volume\{[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-"
    r"[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\}\\"
)


def _safe(check: Callable[[], bool]) -> bool:
    try:
        return check() is True
    except (KeyError, IndexError, TypeError, ValueError, VerificationError):
        return False


def _obj(value: object, keys: tuple[str, ...], name: str) -> dict[str, object]:
    return exact_keys(value, keys, name=name)


def _file_identity(value: object) -> dict[str, object]:
    item = _obj(
        value,
        ("volume_serial_hex", "file_id_hex", "reparse_point", "byte_length"),
        "file identity",
    )
    if type(item["volume_serial_hex"]) is not str or _VOLUME.fullmatch(
        item["volume_serial_hex"]
    ) is None:
        raise VerificationError("volume serial differs")
    if type(item["file_id_hex"]) is not str or _FILE_ID.fullmatch(
        item["file_id_hex"]
    ) is None:
        raise VerificationError("file ID differs")
    exact_bool(item["reparse_point"], name="reparse point")
    length = exact_int(item["byte_length"], name="byte length", minimum=1)
    if length > MAX_CANDIDATE_BYTES:
        raise VerificationError("byte length exceeds the public bound")
    return item


def _filetime_int(value: object, *, name: str) -> int:
    if type(value) is not str or _FILETIME.fullmatch(value) is None:
        raise VerificationError(f"{name} must be fixed lowercase FILETIME hex")
    parsed = int(value, 16)
    if parsed <= 0:
        raise VerificationError(f"{name} must be positive")
    return parsed


def _acquired_path(value: object) -> str:
    if type(value) is not str or not value or len(value) > 32767:
        raise VerificationError("acquired path is not bounded exact text")
    match = _VOLUME_GUID_PATH.match(value)
    if match is None:
        raise VerificationError("acquired path is not a volume-GUID final path")
    tail = value[match.end():]
    if (
        not tail
        or tail.endswith("\\")
        or "\x00" in tail
        or "/" in tail
        or ":" in tail
        or any(character in tail for character in '*?"<>|')
    ):
        raise VerificationError("acquired path contains a forbidden component")
    segments = tail.split("\\")
    if any(
        not segment
        or segment in {".", ".."}
        or segment.endswith((" ", "."))
        for segment in segments
    ):
        raise VerificationError("acquired path normalization differs")
    return value


def _chain(value: object, name: str) -> list[object]:
    items = exact_list(value, name=name, minimum=2)
    if len(items) > MAX_REBUILT_CHAIN_CERTIFICATES:
        raise VerificationError("rebuilt chain exceeds the public bound")
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
                "disallowed",
            ),
            f"{name} element",
        )
        if exact_int(element["position"], name="chain position", minimum=0) != index:
            raise VerificationError("chain positions are not contiguous")
        expected_role = (
            "LEAF" if index == 0 else "ROOT" if index == len(items) - 1 else "INTERMEDIATE"
        )
        if element["role"] != expected_role:
            raise VerificationError("chain role order differs")
        require_sha256(element["certificate_der_sha256"], name="certificate DER")
        exact_int(element["trust_error_status"], name="trust error", minimum=0)
        exact_int(element["trust_info_status"], name="trust info", minimum=0)
        exact_bool(element["has_freshness_time"], name="freshness presence")
        exact_bool(element["disallowed"], name="disallowed status")
        if element["freshness_age_seconds"] is not None:
            exact_int(element["freshness_age_seconds"], name="freshness age", minimum=0)
    return items


def _chain_sha256(chain: list[object]) -> str:
    return sha256_hex(canonical_json_lf(chain))


def _provider_chain(value: object, name: str) -> list[str]:
    items = exact_list(value, name=name, minimum=2)
    if len(items) > MAX_PROVIDER_CHAIN_CERTIFICATES:
        raise VerificationError("provider chain exceeds the public bound")
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
            "verification_time_filetime_hex",
            "cache_resync_filetime_hex",
            "call_started_filetime_hex",
            "call_returned_filetime_hex",
            "monotonic_frequency_hex",
            "monotonic_started_hex",
            "monotonic_returned_hex",
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
    _filetime_int(call["verification_time_filetime_hex"], name="chain verification time")
    _filetime_int(call["cache_resync_filetime_hex"], name="cache resync time")
    _filetime_int(call["call_started_filetime_hex"], name="chain call start")
    _filetime_int(call["call_returned_filetime_hex"], name="chain call return")
    _filetime_int(call["monotonic_frequency_hex"], name="QPC frequency")
    _filetime_int(call["monotonic_started_hex"], name="QPC call start")
    _filetime_int(call["monotonic_returned_hex"], name="QPC call return")
    exact_bool(call["additional_candidate_store_used"], name="candidate store")
    exact_bool(call["api_return"], name="chain API return")
    return call


def chain_call_input_sha256(call: Mapping[str, object]) -> str:
    return sha256_hex(
        canonical_json_lf(
            {
                "additional_candidate_store_used": call["additional_candidate_store_used"],
                "api": call["api"],
                "cache_resync_filetime_hex": call["cache_resync_filetime_hex"],
                "chain_engine": call["chain_engine"],
                "flags": call["flags"],
                "leaf_certificate_der_sha256": call["leaf_certificate_der_sha256"],
                "requested_eku": call["requested_eku"],
                "url_retrieval_timeout_ms": call["url_retrieval_timeout_ms"],
                "verification_time_filetime_hex": call["verification_time_filetime_hex"],
            }
        )
    )


def _policy(value: object) -> dict[str, object]:
    policy = _obj(
        value,
        (
            "policy_id",
            "chain_context_sha256",
            "verification_time_filetime_hex",
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
    _filetime_int(policy["verification_time_filetime_hex"], name="policy verification time")
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
                "verification_time_filetime_hex": policy["verification_time_filetime_hex"],
            }
        )
    )


def _call_duration_seconds(call: Mapping[str, object]) -> int:
    frequency = _filetime_int(call["monotonic_frequency_hex"], name="QPC frequency")
    start = _filetime_int(call["monotonic_started_hex"], name="QPC call start")
    end = _filetime_int(call["monotonic_returned_hex"], name="QPC call return")
    if end < start:
        raise VerificationError("chain call monotonic clock moved backward")
    ticks = end - start
    seconds = (ticks + frequency - 1) // frequency
    if seconds > MAX_CHAIN_CALL_DURATION_SECONDS:
        raise VerificationError("chain call duration exceeds the public bound")
    return seconds


def _clock_interval_consistent(call: Mapping[str, object]) -> bool:
    frequency = _filetime_int(call["monotonic_frequency_hex"], name="QPC frequency")
    monotonic_start = _filetime_int(call["monotonic_started_hex"], name="QPC start")
    monotonic_end = _filetime_int(call["monotonic_returned_hex"], name="QPC return")
    utc_start = _filetime_int(call["call_started_filetime_hex"], name="UTC start")
    utc_end = _filetime_int(call["call_returned_filetime_hex"], name="UTC return")
    if monotonic_end < monotonic_start or utc_end < utc_start:
        return False
    delta = abs(
        (utc_end - utc_start) * frequency
        - (monotonic_end - monotonic_start) * FILETIME_TICKS_PER_SECOND
    )
    return delta <= (
        CLOCK_DISCONTINUITY_TOLERANCE_SECONDS
        * FILETIME_TICKS_PER_SECOND
        * frequency
    )


def _fresh_nonroot(chain: list[object], call: Mapping[str, object]) -> bool:
    margin = _call_duration_seconds(call)
    for element in chain[:-1]:
        age = element["freshness_age_seconds"]
        if (
            element["trust_error_status"] != 0
            or element["revocation_result"] != "GOOD"
            or element["has_freshness_time"] is not True
            or type(age) is not int
            or not 0 <= age + margin <= MAX_REVOCATION_FRESHNESS_SECONDS
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


def _snapshot(value: object) -> dict[str, object]:
    snapshot = _obj(value, ("sha256", "entry_count"), "trust snapshot")
    require_sha256(snapshot["sha256"], name="trust snapshot")
    count = exact_int(snapshot["entry_count"], name="trust snapshot entries", minimum=0)
    if count > MAX_STORE_ENTRIES:
        raise VerificationError("trust snapshot entry count exceeds the public bound")
    return snapshot


def _decision(
    raw: bytes,
    authority: VerificationAuthority,
    failure_class: str | None,
    failures: tuple[str, ...],
    trace_sha256: str,
) -> bytes:
    passed = not failures
    return canonical_json_lf(
        {
            "acquisition_authority_manifest_sha256": (
                authority.acquisition_authority_manifest_sha256
            ),
            "acquisition_record_sha256": authority.acquisition_record_sha256,
            "acquisition_validator_manifest_sha256": (
                authority.acquisition_validator_manifest_sha256
            ),
            "executed_code_authority_established": False,
            "failure_class": failure_class,
            "failure_relations": list(failures),
            "implementation_manifest_sha256": authority.implementation_manifest_sha256,
            "native_verifier_manifest_sha256": authority.native_verifier_manifest_sha256,
            "observation_sha256": sha256_hex(raw),
            "policy_manifest_sha256": authority.policy_manifest_sha256,
            "process_authority_granted": False,
            "runtime_authority_scope": authority.runtime_authority_scope,
            "schema_id": DECISION_SCHEMA_ID,
            "semantic_trace_sha256": trace_sha256,
            "semantic_validator_manifest_sha256": (
                authority.semantic_validator_manifest_sha256
            ),
            "supplier_criterion_id": authority.supplier_criterion_id,
            "terminal_decision": (
                "PASS-BOUNDED-TRUSTED-HOST-CONSISTENCY-NO-LIVE-AUTHORITY"
                if passed
                else "REJECTED-BEFORE-PROCESS"
            ),
            "trust_policy_pass": passed,
        }
    )


def _reject_malformed(
    raw: bytes,
    authority: VerificationAuthority,
    reason: str,
) -> VerificationResult:
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
    decision_raw = _decision(
        raw,
        authority,
        reason,
        SEMANTIC_RELATIONS,
        trace_sha256,
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
    """Compute every relation from bound observation bytes; trust no input Boolean."""

    if type(raw) is not bytes:
        raise VerificationError("observation input must be exact bytes")
    if len(raw) > MAX_OBSERVATION_BYTES:
        return _reject_malformed(raw, authority, "malformed-observation:byte-bound-exceeded")
    try:
        observation = strict_json_object(raw)
        exact_keys(
            observation,
            (
                "schema_id",
                "native_collection_status",
                "implementation_manifest_sha256",
                "policy_manifest_sha256",
                "acquisition_validator_manifest_sha256",
                "native_verifier_manifest_sha256",
                "semantic_validator_manifest_sha256",
                "runtime_authority",
                "acquisition_record",
                "acquisition_record_sha256",
                "runtime_binding",
                "supplier",
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
    add(_safe(lambda: observation["acquisition_validator_manifest_sha256"] == authority.acquisition_validator_manifest_sha256))
    add(_safe(lambda: observation["native_verifier_manifest_sha256"] == authority.native_verifier_manifest_sha256))
    add(_safe(lambda: observation["semantic_validator_manifest_sha256"] == authority.semantic_validator_manifest_sha256))
    add(_safe(lambda: observation["schema_id"] == OBSERVATION_SCHEMA_ID and canonical_json_lf(observation) == raw and sha256_hex(raw) == observation_sha256))

    try:
        runtime_authority = _obj(
            observation["runtime_authority"],
            ("scope", "executed_code_authority_established"),
            "runtime authority",
        )
    except VerificationError:
        runtime_authority = {}
    add(_safe(lambda: runtime_authority["scope"] == authority.runtime_authority_scope == RUNTIME_AUTHORITY_SCOPE and runtime_authority["executed_code_authority_established"] is authority.executed_code_authority_established is False))

    try:
        acquisition = _obj(
            observation["acquisition_record"],
            (
                "schema_id", "authority_manifest_sha256", "sequence_id",
                "producer_process_id", "created_filetime_hex", "acquired_path",
                "acquired_path_semantics", "requested_uri",
                "final_uri", "redirect_count", "transfer_complete",
                "retained_handle_hex", "handle_contract", "file_identity",
                "byte_sha256",
            ),
            "acquisition record",
        )
        acquisition_identity = _file_identity(acquisition["file_identity"])
        acquisition_hash = require_sha256(acquisition["byte_sha256"], name="acquisition bytes")
        acquisition_path = _acquired_path(acquisition["acquired_path"])
        acquisition_handle = acquisition["retained_handle_hex"]
        if type(acquisition_handle) is not str or _HANDLE.fullmatch(acquisition_handle) is None:
            raise VerificationError("acquisition handle differs")
        acquisition_contract = _obj(
            acquisition["handle_contract"],
            tuple(ACQUISITION_HANDLE_CONTRACT),
            "acquisition handle contract",
        )
        authority_record_bytes = canonical_json_lf(acquisition)
    except VerificationError:
        acquisition = {}; acquisition_identity = {}; acquisition_hash = ""; acquisition_path = ""; acquisition_handle = ""; acquisition_contract = {}; authority_record_bytes = b""
    add(_safe(lambda: acquisition["schema_id"] == ACQUISITION_SCHEMA_ID and canonical_json_lf(acquisition) == authority_record_bytes and observation["acquisition_record_sha256"] == authority.acquisition_record_sha256 == sha256_hex(authority_record_bytes) and acquisition["authority_manifest_sha256"] == authority.acquisition_authority_manifest_sha256 and require_sha256(acquisition["sequence_id"], name="acquisition sequence") == acquisition["sequence_id"] and _filetime_int(acquisition["created_filetime_hex"], name="acquisition time") > 0))
    add(_safe(lambda: acquisition["requested_uri"] == acquisition["final_uri"] == FIXED_BOOTSTRAPPER_URL and acquisition["acquired_path_semantics"] == ACQUISITION_PATH_SEMANTICS_ID and exact_int(acquisition["redirect_count"], name="redirects", minimum=0) == 0 and exact_bool(acquisition["transfer_complete"], name="transfer complete") is True))

    try:
        runtime_binding = _obj(
            observation["runtime_binding"],
            (
                "consumer_process_id", "supplied_handle_hex",
                "supplied_handle_path", "immutable_lease_path",
                "path_semantics", "immutable_lease_contract",
            ),
            "runtime binding",
        )
        supplied_handle_path = _acquired_path(runtime_binding["supplied_handle_path"])
        immutable_lease_path = _acquired_path(runtime_binding["immutable_lease_path"])
        lease_contract = _obj(
            runtime_binding["immutable_lease_contract"],
            tuple(IMMUTABLE_LEASE_CONTRACT),
            "immutable lease contract",
        )
    except VerificationError:
        runtime_binding = {}; supplied_handle_path = ""; immutable_lease_path = ""; lease_contract = {}
    add(_safe(lambda: exact_int(acquisition["producer_process_id"], name="producer process", minimum=1) == exact_int(runtime_binding["consumer_process_id"], name="consumer process", minimum=1) and acquisition_handle == runtime_binding["supplied_handle_hex"]))
    add(_safe(lambda: acquisition_path == supplied_handle_path == immutable_lease_path and runtime_binding["path_semantics"] == acquisition["acquired_path_semantics"] == ACQUISITION_PATH_SEMANTICS_ID and acquisition_contract == ACQUISITION_HANDLE_CONTRACT))
    add(_safe(lambda: lease_contract == IMMUTABLE_LEASE_CONTRACT))

    identities = observation.get("file_identities")
    identity_values: list[dict[str, object]] = []
    try:
        identity_map = _obj(
            identities,
            ("lease_open", "post_signature", "preexecution"),
            "file identities",
        )
        identity_values = [
            _file_identity(identity_map[name])
            for name in ("lease_open", "post_signature", "preexecution")
        ]
    except VerificationError:
        identity_values = []
    add(_safe(lambda: len(identity_values) == 3 and acquisition_identity == identity_values[0] == identity_values[1] == identity_values[2]))
    add(_safe(lambda: acquisition_identity["reparse_point"] is False and all(item["reparse_point"] is False for item in identity_values)))
    add(_safe(lambda: len(identity_values) == 3 and 0 < acquisition_identity["byte_length"] <= MAX_CANDIDATE_BYTES and len({item["byte_length"] for item in identity_values + [acquisition_identity]}) == 1))

    hashes = observation.get("byte_sha256")
    try:
        hash_map = _obj(hashes, ("lease_open", "post_signature", "preexecution"), "byte hashes")
        hash_values = [require_sha256(hash_map[name], name=f"{name} hash") for name in ("lease_open", "post_signature", "preexecution")]
    except VerificationError:
        hash_values = []
    add(_safe(lambda: len(hash_values) == 3 and acquisition_hash == hash_values[0] == hash_values[1] == hash_values[2]))

    try:
        wintrust = _obj(
            observation["wintrust"],
            (
                "action_guid", "window_handle", "ui_choice", "ui_context",
                "union_choice", "revocation_checks", "prov_flags",
                "state_action_verify", "verify_return", "state_action_close",
                "close_return", "provider_state_id", "candidate_callback_used",
                "candidate_store_used", "custom_parser_used",
            ),
            "wintrust",
        )
    except VerificationError:
        wintrust = {}
    add(_safe(lambda: wintrust["action_guid"] == WINTRUST_ACTION_GUID and wintrust["window_handle"] == "INVALID_HANDLE_VALUE" and wintrust["ui_choice"] == "WTD_UI_NONE" and wintrust["ui_context"] == "WTD_UICONTEXT_INSTALL" and wintrust["union_choice"] == "WTD_CHOICE_FILE" and wintrust["revocation_checks"] == "WTD_REVOKE_NONE" and tuple(wintrust["prov_flags"]) == WINTRUST_PROV_FLAGS and wintrust["state_action_verify"] == "WTD_STATEACTION_VERIFY" and wintrust["state_action_close"] == "WTD_STATEACTION_CLOSE"))
    add(_safe(lambda: exact_int(wintrust["verify_return"], name="WinVerifyTrust return") == 0))

    event_rows: list[dict[str, object]] = []
    try:
        raw_events = exact_list(observation["events"], name="events", minimum=len(EVENT_SEQUENCE))
        if len(raw_events) != len(EVENT_SEQUENCE):
            raise VerificationError("event count differs")
        for index, raw_event in enumerate(raw_events):
            event = _obj(raw_event, ("sequence", "kind", "provider_state_id"), "event")
            if exact_int(event["sequence"], name="event sequence", minimum=0) != index or event["kind"] != EVENT_SEQUENCE[index]:
                raise VerificationError("event order differs")
            event_rows.append(event)
    except VerificationError:
        event_rows = []
    add(_safe(lambda: len(event_rows) == len(EVENT_SEQUENCE) and require_sha256(wintrust["provider_state_id"], name="provider state") == wintrust["provider_state_id"] and all(event_rows[index]["provider_state_id"] == wintrust["provider_state_id"] for index in range(3, 13)) and all(event_rows[index]["provider_state_id"] is None for index in (0, 1, 2, 13))))
    add(_safe(lambda: exact_int(wintrust["close_return"], name="WinVerifyTrust close return") == 0 and event_rows[12]["kind"] == "STATE-CLOSED" and event_rows[10]["kind"] == "TIMESTAMP-POLICY-EVALUATED"))

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
    add(_safe(lambda: signer_call["api"] == "CertGetCertificateChain" and signer_call["leaf_certificate_der_sha256"] == signer_leaf and signer_call["output_chain_sha256"] == _chain_sha256(signer_rebuilt) and signer_call["input_sha256"] == chain_call_input_sha256(signer_call) and signer_call["api_return"] is True and len(signer_provider) <= MAX_PROVIDER_CHAIN_CERTIFICATES and len(signer_rebuilt) <= MAX_REBUILT_CHAIN_CERTIFICATES))
    add(_safe(lambda: signer_auth["policy_id"] == "CERT_CHAIN_POLICY_AUTHENTICODE" and signer_auth["chain_context_sha256"] == signer_call["output_chain_sha256"] and signer_auth["verification_time_filetime_hex"] == signer_call["verification_time_filetime_hex"] and signer_auth["flags"] == 0 and signer_auth["extra_policy"] == {"pv_extra_policy_para": "NULL"} and signer_auth["input_sha256"] == policy_input_sha256(signer_auth) and signer_auth["api_return"] is True and signer_auth["policy_error"] == 0))
    add(_safe(lambda: signer_ms["policy_id"] == "CERT_CHAIN_POLICY_MICROSOFT_ROOT" and signer_ms["chain_context_sha256"] == signer_call["output_chain_sha256"] and signer_ms["verification_time_filetime_hex"] == signer_call["verification_time_filetime_hex"] and signer_ms["flags"] == 0 and signer_ms["extra_policy"] == {"test_root_enabled": False} and signer_ms["input_sha256"] == policy_input_sha256(signer_ms) and signer_ms["api_return"] is True and signer_ms["policy_error"] == 0))
    add(_safe(lambda: exact_bool(signer["code_signing_eku_present"], name="code signing EKU") is True and signer_call["requested_eku"] == CODE_SIGNING_EKU))

    try:
        supplier = _obj(observation["supplier"], ("criterion_id", "components", "official_leaf_guarantee_claimed", "project_reauthorization_acknowledged"), "supplier")
    except VerificationError:
        supplier = {}
    add(_safe(lambda: supplier["criterion_id"] == authority.supplier_criterion_id == SUPPLIER_CRITERION_ID and tuple(supplier["components"]) == SUPPLIER_CRITERION_COMPONENTS and supplier["official_leaf_guarantee_claimed"] is False and supplier["project_reauthorization_acknowledged"] is True))

    try:
        timestamp = _obj(observation["timestamp"], ("present", "kind", "signer_index", "countersigner_index", "provider_state_id", "signing_time_filetime_hex", "leaf_certificate_der_sha256", "provider_chain", "rebuilt_chain", "chain_call", "timestamp_policy"), "timestamp")
        timestamp_leaf = require_sha256(timestamp["leaf_certificate_der_sha256"], name="timestamp leaf")
        timestamp_provider = _provider_chain(timestamp["provider_chain"], "provider timestamp chain")
        timestamp_rebuilt = _chain(timestamp["rebuilt_chain"], "rebuilt timestamp chain")
        timestamp_call = _chain_call(timestamp["chain_call"])
        timestamp_policy = _policy(timestamp["timestamp_policy"])
        signing_time = _filetime_int(timestamp["signing_time_filetime_hex"], name="signing time")
    except VerificationError:
        timestamp = {}; timestamp_leaf = ""; timestamp_provider = []; timestamp_rebuilt = []; timestamp_call = {}; timestamp_policy = {}; signing_time = 0
    add(_safe(lambda: timestamp["present"] is True and timestamp["kind"] == "WINDOWS-PROVIDER-TIMESTAMP-SIGNER"))
    add(_safe(lambda: timestamp["signer_index"] == 0 and timestamp["countersigner_index"] == 0 and timestamp["provider_state_id"] == wintrust["provider_state_id"]))
    add(_safe(lambda: timestamp_leaf == timestamp_provider[0]))
    add(_safe(lambda: timestamp_provider == [element["certificate_der_sha256"] for element in timestamp_rebuilt]))
    add(_safe(lambda: timestamp_call["api"] == "CertGetCertificateChain" and timestamp_call["leaf_certificate_der_sha256"] == timestamp_leaf and _filetime_int(timestamp_call["verification_time_filetime_hex"], name="timestamp chain verification time") == signing_time and timestamp_call["output_chain_sha256"] == _chain_sha256(timestamp_rebuilt) and timestamp_call["input_sha256"] == chain_call_input_sha256(timestamp_call) and timestamp_call["api_return"] is True and len(timestamp_provider) <= MAX_PROVIDER_CHAIN_CERTIFICATES and len(timestamp_rebuilt) <= MAX_REBUILT_CHAIN_CERTIFICATES))
    add(_safe(lambda: timestamp_policy["policy_id"] == "CERT_CHAIN_POLICY_AUTHENTICODE_TS" and timestamp_policy["chain_context_sha256"] == timestamp_call["output_chain_sha256"] and _filetime_int(timestamp_policy["verification_time_filetime_hex"], name="timestamp policy verification time") == signing_time and timestamp_policy["flags"] == 0 and timestamp_policy["extra_policy"] == {"pv_extra_policy_para": "NULL"} and timestamp_policy["input_sha256"] == policy_input_sha256(timestamp_policy) and timestamp_policy["api_return"] is True and timestamp_policy["policy_error"] == 0))
    add(_safe(lambda: tuple(signer_call["flags"]) == CHAIN_FLAGS and tuple(timestamp_call["flags"]) == CHAIN_FLAGS and signer_call["chain_engine"] == timestamp_call["chain_engine"] == CHAIN_ENGINE and signer_call["url_retrieval_timeout_ms"] == timestamp_call["url_retrieval_timeout_ms"] == URL_RETRIEVAL_TIMEOUT_MS and signer_call["additional_candidate_store_used"] is False and timestamp_call["additional_candidate_store_used"] is False and timestamp_call["requested_eku"] == TIME_STAMPING_EKU and _filetime_int(signer_call["cache_resync_filetime_hex"], name="signer cache resync") == _filetime_int(signer_call["call_started_filetime_hex"], name="signer call start") - MAX_REVOCATION_FRESHNESS_SECONDS * FILETIME_TICKS_PER_SECOND and _filetime_int(timestamp_call["cache_resync_filetime_hex"], name="timestamp cache resync") == _filetime_int(timestamp_call["call_started_filetime_hex"], name="timestamp call start") - MAX_REVOCATION_FRESHNESS_SECONDS * FILETIME_TICKS_PER_SECOND))
    add(_safe(lambda: _fresh_nonroot(signer_rebuilt, signer_call)))
    add(_safe(lambda: _fresh_nonroot(timestamp_rebuilt, timestamp_call)))
    add(_safe(lambda: _call_duration_seconds(signer_call) <= MAX_CHAIN_CALL_DURATION_SECONDS and _call_duration_seconds(timestamp_call) <= MAX_CHAIN_CALL_DURATION_SECONDS and _clock_interval_consistent(signer_call) and _clock_interval_consistent(timestamp_call) and _filetime_int(signer_call["call_started_filetime_hex"], name="signer call start") >= signing_time and _filetime_int(timestamp_call["call_started_filetime_hex"], name="timestamp call start") >= signing_time))
    add(_safe(lambda: _trusted_root(signer_rebuilt) and _trusted_root(timestamp_rebuilt)))

    try:
        trust = _obj(observation["trust_authority"], ("pre_snapshot", "post_snapshot", "snapshot_scope", "enumeration_complete", "store_close_success", "effective_trust_authority_claimed", "store_mutation_count"), "trust authority")
        pre_snapshot = _snapshot(trust["pre_snapshot"])
        post_snapshot = _snapshot(trust["post_snapshot"])
    except VerificationError:
        trust = {}; pre_snapshot = {}; post_snapshot = {}
    add(_safe(lambda: tuple(trust["snapshot_scope"]) == TRUST_SNAPSHOT_SCOPE and trust["enumeration_complete"] is True and trust["store_close_success"] is True and trust["effective_trust_authority_claimed"] is False))
    add(_safe(lambda: pre_snapshot == post_snapshot))
    add(_safe(lambda: exact_int(trust["store_mutation_count"], name="store mutation count", minimum=0) == 0))
    add(_safe(lambda: wintrust["candidate_callback_used"] is False and wintrust["candidate_store_used"] is False and wintrust["custom_parser_used"] is False))
    add(_safe(lambda: exact_int(observation["process_count_before_decision"], name="process count", minimum=0) == 0 and observation["native_collection_status"] == "COMPLETED-NONAUTHORITATIVE-OBSERVATION"))
    add(_safe(lambda: authority.executed_code_authority_established is False and runtime_authority["executed_code_authority_established"] is False))

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
    decision_raw = _decision(
        raw,
        authority,
        None if not failures else "semantic-relation-rejected",
        failures,
        trace_sha256,
    )
    return VerificationResult(
        observation_sha256,
        trace_raw,
        trace_sha256,
        decision_raw,
        sha256_hex(decision_raw),
        not failures,
        failures,
    )

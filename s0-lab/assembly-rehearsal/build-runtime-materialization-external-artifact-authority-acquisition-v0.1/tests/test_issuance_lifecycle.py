from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, replace
import gc
import hashlib
from pathlib import Path
import sys
from threading import Barrier, Event, Lock, Thread
import unittest
import weakref


CANDIDATE_ROOT = Path(__file__).resolve().parents[1]
IMPLEMENTATION_ROOT = CANDIDATE_ROOT / "implementation"
AUTHENTICODE_ROOT = (
    CANDIDATE_ROOT.parent
    / "windows-authenticode-verifier-v0.4"
    / "implementation"
)
sys.path.insert(0, str(AUTHENTICODE_ROOT))
sys.path.insert(0, str(IMPLEMENTATION_ROOT))

from s0_external_artifact_authority_acquisition import (
    buildtools,
    candidate,
    metadata,
    pins,
    wheel,
)
from s0_external_artifact_authority_acquisition._issuance import (
    make_bounded_issuance_registry,
)
from s0_external_artifact_authority_acquisition.errors import AuthorityError
from s0_windows_authenticode_verifier.model import VerificationResult


BLOCKER = "BUILD-TOOLS-AUTHENTICODE-TRANSITIVE-CLOSURE-UNVERIFIED"
LIVE_BLOCKER = "BUILD-TOOLS-AUTHENTICODE-LIVE-RESULT-PENDING"


@dataclass(frozen=True, slots=True, weakref_slot=True)
class _Evidence:
    kind: str
    marker: int
    raw: bytes


@dataclass(frozen=True, slots=True, weakref_slot=True)
class _RaceEvidence:
    authority: str
    number: int
    permitted: bool
    inventory: tuple[str, ...]
    raw: bytes


@dataclass(frozen=True, slots=True, weakref_slot=True)
class _SnapshotCarrier:
    payload: object


class _IntSubclass(int):
    pass


class _StrSubclass(str):
    pass


class _TupleSubclass(tuple):
    pass


_HOSTILE_CALLS: list[str] = []


class _Hostile:
    def _trap(self, name: str):
        _HOSTILE_CALLS.append(name)
        raise AssertionError(f"hostile trap called:{name}")

    def __eq__(self, _other):
        return self._trap("eq")

    def __iter__(self):
        return self._trap("iter")

    def __repr__(self):
        return self._trap("repr")

    def __hash__(self):
        return self._trap("hash")

    def __int__(self):
        return self._trap("int")

    def __index__(self):
        return self._trap("index")

    def __str__(self):
        return self._trap("str")

    def __bool__(self):
        return self._trap("bool")


def _closure_value(function, name: str):
    cells = dict(zip(function.__code__.co_freevars, function.__closure__ or ()))
    if name not in cells:
        raise AssertionError(f"closure value missing:{name}")
    return cells[name].cell_contents


def _carrier_registry(*, snapshot=None, materialize=replace):
    snapshot_function = snapshot or (lambda value: (value.payload,))
    return make_bounded_issuance_registry(
        limits={"authority": 1},
        snapshot=snapshot_function,
        materialize=materialize,
        error_type=AuthorityError,
        capacity_error="carrier_capacity_exceeded",
        invalid_kind_error="carrier_kind_invalid",
        not_issued_error="carrier_not_issued_or_changed",
    )


def _exact_snapshot_registry(snapshot, *, materialize=replace):
    return make_bounded_issuance_registry(
        limits={"authority": 1},
        snapshot=snapshot,
        materialize=materialize,
        error_type=AuthorityError,
        capacity_error="production_snapshot_capacity_exceeded",
        invalid_kind_error="production_snapshot_kind_invalid",
        not_issued_error="production_snapshot_not_issued_or_changed",
    )


def _race_snapshot(value: object) -> tuple[object, ...]:
    if type(value) is not _RaceEvidence:
        raise AuthorityError("race_snapshot_type_invalid")
    return (
        value.authority,
        value.number,
        value.permitted,
        value.inventory,
        id(value.raw),
    )


def _race_registry(materialize, *, snapshot=_race_snapshot):
    return make_bounded_issuance_registry(
        limits={"authority": 1},
        snapshot=snapshot,
        materialize=materialize,
        error_type=AuthorityError,
        capacity_error="race_capacity_exceeded",
        invalid_kind_error="race_kind_invalid",
        not_issued_error="race_not_issued_or_changed",
    )


def _race_value() -> _RaceEvidence:
    return _RaceEvidence("AUTHENTIC", 7, False, ("alpha", "beta"), b"raw-authority")


def _generic_registry(limit: int = 6):
    return make_bounded_issuance_registry(
        limits={"pypi": limit},
        snapshot=lambda value: (value.kind, value.marker, id(value.raw)),
        materialize=replace,
        error_type=AuthorityError,
        capacity_error="test_capacity_exceeded",
        invalid_kind_error="test_kind_invalid",
        not_issued_error="test_not_issued_or_changed",
    )


def _registry_entries(issue) -> dict[int, tuple[object, ...]]:
    for cell in issue.__closure__ or ():
        value = cell.cell_contents
        if (
            type(value) is dict
            and value
            and all(type(key) is int for key in value)
            and all(type(item) is tuple and len(item) == 4 for item in value.values())
        ):
            return value
    raise AssertionError("issuance entries closure not found")


def _freeze_metadata_seam(
    *, cpython_forbidden: bool = False, materialize=None
):
    def cpython_impl(
        release_page_raw: bytes,
        ftp_index_raw: bytes,
        sigstore_bundle_raw: bytes,
        **kwargs,
    ):
        evidence_type = kwargs["evidence_type"]
        release = pins.resolve_source_snapshot("cpython-3.12.10-release-page")
        index = pins.resolve_source_snapshot("cpython-3.12.10-ftp-index")
        bundle = pins.resolve_source_snapshot(
            "cpython-3.12.10-embed-amd64-sigstore-bundle"
        )
        artifact = pins.resolve_artifact_snapshot(pins.CPYTHON_ARTIFACT_ID)
        return evidence_type(
            release[2],
            release[3],
            kwargs["release_representation"],
            kwargs["release_content_encoding"],
            kwargs["release_decoded_sha256"],
            kwargs["release_decoded_size"],
            index[2],
            index[3],
            bundle[2],
            bundle[3],
            artifact[3],
            artifact[4],
            "a60bd3cd635e7561d81b243fd1112091501fff894cffa400e2416eb2f7834eb3",
            717,
            72,
            1,
            pins.CPYTHON_SIGSTORE_POLICY_IDENTITY,
            pins.CPYTHON_SIGSTORE_OIDC_ISSUER,
            sigstore_cryptographic_verification=cpython_forbidden,
            release_page_raw=release_page_raw,
            ftp_index_raw=ftp_index_raw,
            sigstore_bundle_raw=sigstore_bundle_raw,
        )

    def microsoft_impl(release_history_raw: bytes, **kwargs):
        evidence_type = kwargs["evidence_type"]
        source = pins.resolve_source_snapshot(
            "microsoft-vs-2022-release-history-17.14.39"
        )
        artifact = pins.resolve_artifact_snapshot(pins.BUILDTOOLS_ARTIFACT_ID)
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

    def pypi_impl(pin_or_id, raw_json: bytes, **kwargs):
        evidence_type = kwargs["evidence_type"]
        pin = pins.resolve_wheel_snapshot(pin_or_id)
        source = pins.resolve_source_snapshot(pin[7])
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

    originals = (
        metadata._validate_cpython_source_metadata_impl,
        metadata._validate_microsoft_release_metadata_impl,
        metadata._validate_pypi_metadata_impl,
        metadata.replace,
    )
    try:
        metadata._validate_cpython_source_metadata_impl = cpython_impl
        metadata._validate_microsoft_release_metadata_impl = microsoft_impl
        metadata._validate_pypi_metadata_impl = pypi_impl
        if materialize is not None:
            metadata.replace = materialize
        return metadata._freeze_metadata_validators()
    finally:
        (
            metadata._validate_cpython_source_metadata_impl,
            metadata._validate_microsoft_release_metadata_impl,
            metadata._validate_pypi_metadata_impl,
            metadata.replace,
        ) = originals


def _metadata_inputs(validate_pypi):
    return {
        pin_id: validate_pypi(pin_id, f"metadata:{pin_id}".encode("ascii"))
        for pin_id in pins.WHEEL_PIN_IDS
    }


def _wheel_inputs():
    result = {}
    for pin_id in pins.WHEEL_PIN_IDS:
        pin = pins.resolve_wheel_snapshot(pin_id)
        raw = f"wheel:{pin_id}".encode("ascii")
        result[pin_id] = wheel.WheelEvidence(
            pin[0],
            pin[5],
            pin[6],
            1,
            len(raw),
            hashlib.sha256(raw).hexdigest(),
            pin[1],
            pin[2],
            pin[8],
            pin[11],
            pin[12],
            pin[9],
            True,
            raw=raw,
        )
    return result


def _closure_registry(*, runtime_authority: bool = False):
    def snapshot(value):
        return (
            value.wheel_pin_ids,
            value.dependency_graph,
            value.pypi_json_requires_dist_inventory,
            value.wheel_metadata_requires_dist_inventory,
            value.metadata_aggregate_size,
            value.wheel_aggregate_size,
            value.extras_selected,
            value.imported,
            value.installed,
            value.runtime_authority,
        )

    issue, require, consume, release = make_bounded_issuance_registry(
        limits={"closure": 1},
        snapshot=snapshot,
        materialize=replace,
        error_type=AuthorityError,
        capacity_error="test_closure_capacity_exceeded",
        invalid_kind_error="test_closure_kind_invalid",
        not_issued_error="test_closure_not_issued_or_changed",
    )
    value = issue(
        wheel.JsonschemaClosureEvidence(
            pins.WHEEL_PIN_IDS,
            pins.JSONSCHEMA_DEPENDENCY_GRAPH,
            pins.PYPI_JSON_REQUIRES_DIST_INVENTORY,
            pins.WHEEL_METADATA_REQUIRES_DIST_INVENTORY,
            142110,
            469346,
            runtime_authority=runtime_authority,
        ),
        "closure",
    )
    return value, issue, require, consume, release


def _candidate_context(
    *, cpython_forbidden: bool = False, closure_forbidden: bool = False
):
    (
        validate_cpython,
        validate_microsoft,
        _validate_pypi,
        require_metadata,
        consume_metadata,
        release_metadata,
    ) = _freeze_metadata_seam(cpython_forbidden=cpython_forbidden)
    cpython = validate_cpython(b"release", b"index", b"bundle")
    microsoft = validate_microsoft(b"microsoft")
    closure, issue_closure, _require_closure, consume_closure, release_closure = (
        _closure_registry(runtime_authority=closure_forbidden)
    )
    originals = (
        candidate._consume_issued_metadata_evidence,
        candidate._release_issued_metadata_evidence,
        candidate._consume_issued_jsonschema_closure,
        candidate._release_issued_jsonschema_closure,
    )
    try:
        candidate._consume_issued_metadata_evidence = consume_metadata
        candidate._release_issued_metadata_evidence = release_metadata
        candidate._consume_issued_jsonschema_closure = (
            lambda value: consume_closure(value, "closure")
        )
        candidate._release_issued_jsonschema_closure = (
            lambda value: release_closure(value, "closure")
        )
        assemble = candidate._freeze_candidate_assembler()
    finally:
        (
            candidate._consume_issued_metadata_evidence,
            candidate._release_issued_metadata_evidence,
            candidate._consume_issued_jsonschema_closure,
            candidate._release_issued_jsonschema_closure,
        ) = originals
    return {
        "assemble": assemble,
        "closure": closure,
        "cpython": cpython,
        "issue_closure": issue_closure,
        "microsoft": microsoft,
        "release_closure": release_closure,
        "release_metadata": release_metadata,
        "validate_cpython": validate_cpython,
        "validate_microsoft": validate_microsoft,
    }


def _assert_candidate_capacity_recovered(test: unittest.TestCase, context) -> None:
    cpython = context["validate_cpython"](b"recovery-release", b"recovery-index", b"recovery-bundle")
    microsoft = context["validate_microsoft"](b"recovery-microsoft")
    closure = context["issue_closure"](
        wheel.JsonschemaClosureEvidence(
            pins.WHEEL_PIN_IDS,
            pins.JSONSCHEMA_DEPENDENCY_GRAPH,
            pins.PYPI_JSON_REQUIRES_DIST_INVENTORY,
            pins.WHEEL_METADATA_REQUIRES_DIST_INVENTORY,
            142110,
            469346,
        ),
        "closure",
    )
    test.assertTrue(context["release_metadata"](cpython, "cpython"))
    test.assertTrue(context["release_metadata"](microsoft, "microsoft"))
    test.assertTrue(context["release_closure"](closure, "closure"))


def _private_proposal():
    trace_raw = b'{"test":"candidate-private-trace"}\n'
    decision_raw = b'{"test":"candidate-private-decision"}\n'

    def verifier(**_kwargs):
        return VerificationResult(
            observation_sha256="a" * 64,
            trace_raw=trace_raw,
            trace_sha256=hashlib.sha256(trace_raw).hexdigest(),
            decision_raw=decision_raw,
            decision_sha256=hashlib.sha256(decision_raw).hexdigest(),
            trust_policy_pass=True,
            failure_relations=(),
        )

    original = buildtools.validate_microsoft_release_metadata
    try:
        buildtools.validate_microsoft_release_metadata = lambda _raw: object()
        adapter, checker = buildtools._freeze_buildtools_adapter(
            verifier, include_issuance_checker=True
        )
    finally:
        buildtools.validate_microsoft_release_metadata = original
    proposal = adapter(
        release_history_raw=b"private-release",
        verifier_full_path="C:\\bounded\\vs_BuildTools.exe",
        file_handle=7,
        sequence_id="1" * 64,
        producer_process_id=11,
        created_filetime_hex="0000000000000001",
        acquired_path=(
            "\\\\?\\Volume{01234567-89AB-CDEF-0123-456789ABCDEF}\\"
            "bounded\\vs_BuildTools.exe"
        ),
        volume_serial_hex="2" * 16,
        file_id_hex="3" * 32,
    )
    return proposal, checker


def _private_adapter_context():
    trace_raw = b'{"test":"canonical-private-trace"}\n'
    decision_raw = b'{"test":"canonical-private-decision"}\n'

    def verifier(**_kwargs):
        return VerificationResult(
            observation_sha256="a" * 64,
            trace_raw=trace_raw,
            trace_sha256=hashlib.sha256(trace_raw).hexdigest(),
            decision_raw=decision_raw,
            decision_sha256=hashlib.sha256(decision_raw).hexdigest(),
            trust_policy_pass=True,
            failure_relations=(),
        )

    original = buildtools.validate_microsoft_release_metadata
    try:
        buildtools.validate_microsoft_release_metadata = lambda _raw: object()
        adapter, checker = buildtools._freeze_buildtools_adapter(
            verifier, include_issuance_checker=True
        )
    finally:
        buildtools.validate_microsoft_release_metadata = original
    arguments = {
        "release_history_raw": b"canonical-private-release",
        "verifier_full_path": "C:\\bounded\\vs_BuildTools.exe",
        "file_handle": 7,
        "sequence_id": "1" * 64,
        "producer_process_id": 11,
        "created_filetime_hex": "0000000000000001",
        "acquired_path": (
            "\\\\?\\Volume{01234567-89AB-CDEF-0123-456789ABCDEF}\\"
            "bounded\\vs_BuildTools.exe"
        ),
        "volume_serial_hex": "2" * 16,
        "file_id_hex": "3" * 32,
    }
    proposal = adapter(**arguments)
    issue = _closure_value(adapter, "issue")
    snapshot = _closure_value(issue, "frozen_snapshot")
    return adapter, checker, issue, snapshot, proposal


def _closure_seam(*, materialize=None):
    (
        _validate_cpython,
        _validate_microsoft,
        validate_pypi,
        _require_metadata,
        consume_metadata,
        release_metadata,
    ) = _freeze_metadata_seam()
    wheels = _wheel_inputs()

    def wheel_validator(pin_id: str, raw: bytes):
        value = wheels[pin_id]
        if raw is not value.raw:
            raise AuthorityError("production_wheel_raw_identity_changed")
        return value

    original_replace = wheel.replace
    try:
        if materialize is not None:
            wheel.replace = materialize
        validate, require, consume, release = wheel._freeze_closure_validator(
            validate_pypi,
            consume_metadata,
            release_metadata,
            wheel_validator,
        )
    finally:
        wheel.replace = original_replace
    values = _metadata_inputs(validate_pypi)
    closure = validate(values, wheels)
    issue = _closure_value(validate, "issue")
    snapshot = _closure_value(issue, "frozen_snapshot")
    return {
        "closure": closure,
        "consume": consume,
        "issue": issue,
        "require": require,
        "release": release,
        "snapshot": snapshot,
        "validate": validate,
        "validate_pypi": validate_pypi,
        "wheels": wheels,
    }


class IssuanceRegistryTests(unittest.TestCase):
    def test_snapshot_raw_identity_mint_copy_mutation_consume_and_release(self) -> None:
        issue, require, consume, release = _generic_registry(limit=1)
        raw = b"payload-bytes-that-must-not-be-copied-into-the-snapshot"
        issued = issue(_Evidence("pypi", 1, raw), "pypi")
        entries = _registry_entries(issue)
        snapshot = entries[id(issued)][3]
        self.assertNotIn(raw, snapshot)
        self.assertEqual(
            snapshot,
            (
                "tuple",
                (("str", "pypi"), ("int", 1), ("int", id(raw))),
            ),
        )
        self.assertIs(require(issued, "pypi"), issued)
        with self.assertRaisesRegex(AuthorityError, "test_not_issued_or_changed"):
            require(_Evidence("pypi", 1, raw), "pypi")
        with self.assertRaisesRegex(AuthorityError, "test_not_issued_or_changed"):
            require(replace(issued), "pypi")

        original_marker = issued.marker
        try:
            object.__setattr__(issued, "marker", original_marker + 1)
            with self.assertRaisesRegex(AuthorityError, "test_not_issued_or_changed"):
                require(issued, "pypi")
        finally:
            object.__setattr__(issued, "marker", original_marker)
        original_raw = issued.raw
        try:
            object.__setattr__(issued, "raw", bytes(bytearray(original_raw)))
            self.assertEqual(issued.raw, original_raw)
            self.assertIsNot(issued.raw, original_raw)
            with self.assertRaisesRegex(AuthorityError, "test_not_issued_or_changed"):
                require(issued, "pypi")
        finally:
            object.__setattr__(issued, "raw", original_raw)

        detached = consume(issued, "pypi")
        self.assertIsNot(detached, issued)
        self.assertIs(detached.raw, raw)
        self.assertEqual(entries, {})
        self.assertFalse(release(detached, "pypi"))
        recovered = issue(_Evidence("pypi", 2, raw), "pypi")
        self.assertTrue(release(recovered, "pypi"))

    def test_monotonic_generation_and_aba_stale_callback_safety(self) -> None:
        issue, require, _consume, release = _generic_registry(limit=1)
        first = issue(_Evidence("pypi", 1, b"first"), "pypi")
        entries = _registry_entries(issue)
        first_key = id(first)
        first_entry = entries[first_key]
        first_reference = first_entry[1]
        stale_callback = first_reference.__callback__
        self.assertIsNotNone(stale_callback)
        self.assertTrue(release(first, "pypi"))

        second = issue(_Evidence("pypi", 2, b"second"), "pypi")
        second_key = id(second)
        second_entry = entries[second_key]
        self.assertGreater(second_entry[0], first_entry[0])
        if second_key != first_key:
            entries[first_key] = second_entry
        stale_callback(first_reference)
        self.assertIs(entries[first_key], second_entry)
        if second_key != first_key:
            del entries[first_key]
        self.assertIs(require(second, "pypi"), second)

        dropped = weakref.ref(second)
        del second
        gc.collect()
        self.assertIsNone(dropped())
        self.assertEqual(entries, {})
        recovered = issue(_Evidence("pypi", 3, b"recovered"), "pypi")
        self.assertTrue(release(recovered, "pypi"))

    def test_sequential_and_concurrent_floods_never_exceed_cap_and_recover(self) -> None:
        issue, _require, _consume, release = _generic_registry(limit=6)
        successes = []
        overflow = 0
        maximum = 0
        entries = None
        for index in range(32):
            try:
                value = issue(_Evidence("pypi", index, f"raw:{index}".encode()), "pypi")
                successes.append(value)
                entries = _registry_entries(issue)
                maximum = max(maximum, len(entries))
            except AuthorityError as exc:
                self.assertEqual(str(exc), "test_capacity_exceeded")
                overflow += 1
        self.assertEqual((len(successes), overflow, maximum), (6, 26, 6))
        for value in successes:
            self.assertTrue(release(value, "pypi"))
        self.assertEqual(entries, {})

        issue, _require, _consume, release = _generic_registry(limit=6)
        barrier = Barrier(32)
        result_lock = Lock()
        concurrent_successes = []
        concurrent_overflow = []

        def attempt(index: int) -> None:
            value = _Evidence("pypi", index, f"thread:{index}".encode())
            barrier.wait()
            try:
                issued = issue(value, "pypi")
            except AuthorityError as exc:
                with result_lock:
                    concurrent_overflow.append(str(exc))
            else:
                with result_lock:
                    concurrent_successes.append(issued)

        with ThreadPoolExecutor(max_workers=32) as executor:
            list(executor.map(attempt, range(32)))
        entries = _registry_entries(issue)
        self.assertEqual(len(concurrent_successes), 6)
        self.assertEqual(concurrent_overflow, ["test_capacity_exceeded"] * 26)
        self.assertEqual(len(entries), 6)
        for value in concurrent_successes:
            self.assertTrue(release(value, "pypi"))
        concurrent_successes.clear()
        gc.collect()
        self.assertEqual(entries, {})
        recovered = issue(_Evidence("pypi", 100, b"recovered"), "pypi")
        self.assertTrue(release(recovered, "pypi"))

    def test_metadata_exact_caps_1_1_6_and_explicit_lifecycle(self) -> None:
        (
            validate_cpython,
            validate_microsoft,
            validate_pypi,
            require,
            consume,
            release,
        ) = _freeze_metadata_seam()
        cpython = validate_cpython(b"release", b"index", b"bundle")
        microsoft = validate_microsoft(b"microsoft")
        pypi = _metadata_inputs(validate_pypi)
        with self.assertRaisesRegex(AuthorityError, "metadata_evidence_registry_capacity_exceeded"):
            validate_cpython(b"release-2", b"index-2", b"bundle-2")
        with self.assertRaisesRegex(AuthorityError, "metadata_evidence_registry_capacity_exceeded"):
            validate_microsoft(b"microsoft-2")
        with self.assertRaisesRegex(AuthorityError, "metadata_evidence_registry_capacity_exceeded"):
            validate_pypi(pins.WHEEL_PIN_IDS[0], b"pypi-overflow")
        self.assertIs(require(cpython, "cpython"), cpython)
        self.assertIs(require(microsoft, "microsoft"), microsoft)
        for value in pypi.values():
            self.assertTrue(release(value, "pypi"))
        self.assertTrue(release(microsoft, "microsoft"))

        detached = consume(cpython, "cpython")
        self.assertIsNot(detached, cpython)
        self.assertIs(detached.release_page_raw, cpython.release_page_raw)
        with self.assertRaisesRegex(AuthorityError, "metadata_evidence_not_issued_or_changed"):
            require(cpython, "cpython")
        recovered = validate_cpython(b"recovered", b"recovered-index", b"recovered-bundle")
        self.assertTrue(release(recovered, "cpython"))


class CanonicalizationHelperTests(unittest.TestCase):
    def test_exact_builtin_rows_accept_and_preserve_type_tags(self) -> None:
        values = (
            None,
            False,
            True,
            0,
            1,
            "text",
            (),
            (None, False, True, 0, 1, "text", ("nested", (False, 0))),
        )
        for value in values:
            with self.subTest(value_type=type(value).__name__):
                issue, _require, consume, _release = _carrier_registry()
                source = issue(_SnapshotCarrier(value), "authority")
                detached = consume(source, "authority")
                self.assertIsNot(detached, source)
                self.assertIs(detached.payload, source.payload)

    def test_bool_int_float_subclass_and_nested_discrimination_cleans(self) -> None:
        cases = (
            (False, 0),
            (True, 1),
            (7, 7.0),
            (7, _IntSubclass(7)),
            ("value", _StrSubclass("value")),
            (("value",), _TupleSubclass(("value",))),
            (("row", (False,)), ("row", (0,))),
        )
        for original, attacker in cases:
            with self.subTest(original_type=type(original).__name__, attacker_type=type(attacker).__name__):
                issue, _require, consume, release = _carrier_registry()
                source = issue(_SnapshotCarrier(original), "authority")
                entries = _registry_entries(issue)
                object.__setattr__(source, "payload", attacker)
                with self.assertRaisesRegex(AuthorityError, "carrier_not_issued_or_changed"):
                    consume(source, "authority")
                object.__setattr__(source, "payload", original)
                self.assertEqual(entries, {})
                self.assertIs(issue(source, "authority"), source)
                self.assertTrue(release(source, "authority"))

    def test_hostile_and_unsafe_values_never_dispatch_or_install_entry(self) -> None:
        unsafe = (
            1.0,
            b"bytes",
            _IntSubclass(1),
            _StrSubclass("text"),
            _TupleSubclass(("row",)),
            [],
            {},
            {"set"},
            object(),
            _Hostile(),
        )
        _HOSTILE_CALLS.clear()
        issue, _require, _consume, release = _carrier_registry()
        entries = _closure_value(issue, "entries")
        counts = _closure_value(issue, "counts")
        generation = dict(zip(issue.__code__.co_freevars, issue.__closure__ or ()))
        for value in unsafe:
            with self.subTest(value_type=type(value).__name__):
                with self.assertRaisesRegex(AuthorityError, "carrier_not_issued_or_changed"):
                    issue(_SnapshotCarrier(value), "authority")
                self.assertEqual(entries, {})
                self.assertEqual(counts, {"authority": 0})
                self.assertEqual(generation["next_generation"].cell_contents, 0)
        self.assertEqual(_HOSTILE_CALLS, [])
        safe = _SnapshotCarrier(("safe", False, 0))
        self.assertIs(issue(safe, "authority"), safe)
        self.assertTrue(release(safe, "authority"))

    def test_require_consume_and_result_snapshot_exceptions_cleanup(self) -> None:
        for operation in ("require", "consume", "result"):
            with self.subTest(operation=operation):
                state = {"enabled": False, "result": None}

                def snapshot(value):
                    if state["enabled"] and (
                        operation in {"require", "consume"}
                        or value is state["result"]
                    ):
                        raise AuthorityError("carrier_snapshot_failure")
                    return (value.payload,)

                def materialize(value):
                    result = replace(value)
                    state["result"] = result
                    return result

                issue, require, consume, release = _carrier_registry(
                    snapshot=snapshot, materialize=materialize
                )
                source = issue(_SnapshotCarrier(("safe",)), "authority")
                entries = _registry_entries(issue)
                state["enabled"] = True
                with self.assertRaisesRegex(AuthorityError, "carrier_snapshot_failure"):
                    if operation == "require":
                        require(source, "authority")
                    else:
                        consume(source, "authority")
                state["enabled"] = False
                self.assertEqual(entries, {})
                self.assertIs(issue(source, "authority"), source)
                self.assertTrue(release(source, "authority"))

    def test_unsafe_result_canonicalization_and_materializer_exception_cleanup(self) -> None:
        def materializer_error(_value):
            raise RuntimeError("carrier_materializer_failure")

        cases = (
            (lambda value: replace(value, payload=_Hostile()), AuthorityError),
            (materializer_error, RuntimeError),
        )
        for materialize, error_type in cases:
            with self.subTest(error_type=error_type.__name__):
                _HOSTILE_CALLS.clear()
                issue, _require, consume, release = _carrier_registry(
                    materialize=materialize
                )
                source = issue(_SnapshotCarrier(("safe",)), "authority")
                entries = _registry_entries(issue)
                with self.assertRaises(error_type):
                    consume(source, "authority")
                self.assertEqual(_HOSTILE_CALLS, [])
                self.assertEqual(entries, {})
                self.assertIs(issue(source, "authority"), source)
                self.assertTrue(release(source, "authority"))


class ProductionCanonicalizationTests(unittest.TestCase):
    def _assert_snapshot_discriminates(
        self, snapshot, source, field_name: str, attacker_value
    ) -> None:
        issue, _require, consume, release = _exact_snapshot_registry(snapshot)
        issue(source, "authority")
        entries = _registry_entries(issue)
        original = object.__getattribute__(source, field_name)
        object.__setattr__(source, field_name, attacker_value)
        with self.assertRaises(AuthorityError):
            consume(source, "authority")
        object.__setattr__(source, field_name, original)
        self.assertEqual(entries, {})
        self.assertIs(issue(source, "authority"), source)
        self.assertTrue(release(source, "authority"))

    def test_metadata_closure_and_proposal_snapshots_discriminate_tagged_values(self) -> None:
        (
            _validate_cpython,
            validate_microsoft,
            validate_pypi,
            _require_metadata,
            _consume_metadata,
            release_metadata,
        ) = _freeze_metadata_seam()
        microsoft = validate_microsoft(b"production-microsoft")
        pypi = validate_pypi(pins.WHEEL_PIN_IDS[0], b"production-pypi")
        metadata_issue = _closure_value(validate_microsoft, "issue")
        metadata_snapshot = _closure_value(metadata_issue, "frozen_snapshot")
        metadata_cases = (
            (microsoft, "authenticode_verified", 0),
            (replace(microsoft, authenticode_verified=True), "authenticode_verified", 1),
            (microsoft, "raw_size", float(microsoft.raw_size)),
            (microsoft, "source_id", _StrSubclass(microsoft.source_id)),
            (pypi, "requires_dist", _TupleSubclass(pypi.requires_dist)),
            (
                replace(pypi, requires_dist=(("row", (False,)),)),
                "requires_dist",
                (("row", (0,)),),
            ),
            (microsoft, "source_id", _Hostile()),
        )
        _HOSTILE_CALLS.clear()
        for source, field_name, attacker in metadata_cases:
            with self.subTest(path="metadata", field=field_name, attacker=type(attacker).__name__):
                self._assert_snapshot_discriminates(
                    metadata_snapshot, source, field_name, attacker
                )
        self.assertEqual(_HOSTILE_CALLS, [])
        self.assertTrue(release_metadata(microsoft, "microsoft"))
        self.assertTrue(release_metadata(pypi, "pypi"))

        closure_context = _closure_seam()
        closure = closure_context["closure"]
        closure_snapshot = closure_context["snapshot"]
        closure_cases = (
            (closure, "extras_selected", 0),
            (replace(closure, runtime_authority=True), "runtime_authority", 1),
            (closure, "metadata_aggregate_size", float(closure.metadata_aggregate_size)),
            (closure, "wheel_pin_ids", _TupleSubclass(closure.wheel_pin_ids)),
            (
                replace(closure, dependency_graph=(("row", (False,)),)),
                "dependency_graph",
                (("row", (0,)),),
            ),
            (
                replace(closure, dependency_graph=(("row", ("value",)),)),
                "dependency_graph",
                (("row", (_StrSubclass("value"),)),),
            ),
            (closure, "wheel_pin_ids", _Hostile()),
        )
        _HOSTILE_CALLS.clear()
        for source, field_name, attacker in closure_cases:
            with self.subTest(path="closure", field=field_name, attacker=type(attacker).__name__):
                self._assert_snapshot_discriminates(
                    closure_snapshot, source, field_name, attacker
                )
        self.assertEqual(_HOSTILE_CALLS, [])
        self.assertTrue(closure_context["release"](closure))

        _adapter, _checker, _proposal_issue, proposal_snapshot, proposal = (
            _private_adapter_context()
        )
        proposal_cases = (
            (proposal, "active_authority", 0),
            (proposal, "trust_policy_pass", 1),
            (proposal, "size", float(proposal.size)),
            (proposal, "status", _StrSubclass(proposal.status)),
            (proposal, "status", _TupleSubclass((proposal.status,))),
            (
                replace(proposal, status=("row", (False,))),
                "status",
                ("row", (0,)),
            ),
            (proposal, "status", _Hostile()),
        )
        _HOSTILE_CALLS.clear()
        for source, field_name, attacker in proposal_cases:
            with self.subTest(path="proposal", field=field_name, attacker=type(attacker).__name__):
                self._assert_snapshot_discriminates(
                    proposal_snapshot, source, field_name, attacker
                )
        self.assertEqual(_HOSTILE_CALLS, [])

    def test_production_require_and_issue_unsafe_cleanup_without_dispatch(self) -> None:
        _HOSTILE_CALLS.clear()
        (
            _validate_cpython,
            validate_microsoft,
            _validate_pypi,
            require_metadata,
            _consume_metadata,
            release_metadata,
        ) = _freeze_metadata_seam()
        microsoft = validate_microsoft(b"unsafe-production-microsoft")
        metadata_issue = _closure_value(validate_microsoft, "issue")
        metadata_entries = _registry_entries(metadata_issue)
        metadata_generation = dict(
            zip(metadata_issue.__code__.co_freevars, metadata_issue.__closure__ or ())
        )["next_generation"]
        original = microsoft.source_id
        object.__setattr__(microsoft, "source_id", _Hostile())
        with self.assertRaises(AuthorityError):
            require_metadata(microsoft, "microsoft")
        self.assertEqual(metadata_entries, {})
        generation_before = metadata_generation.cell_contents
        with self.assertRaises(AuthorityError):
            metadata_issue(microsoft, "microsoft")
        self.assertEqual(metadata_entries, {})
        self.assertEqual(metadata_generation.cell_contents, generation_before)
        object.__setattr__(microsoft, "source_id", original)
        self.assertIs(metadata_issue(microsoft, "microsoft"), microsoft)
        self.assertTrue(release_metadata(microsoft, "microsoft"))

        closure_context = _closure_seam()
        closure = closure_context["closure"]
        closure_entries = _registry_entries(closure_context["issue"])
        original = closure.wheel_pin_ids
        object.__setattr__(closure, "wheel_pin_ids", _Hostile())
        with self.assertRaises(AuthorityError):
            closure_context["require"](closure)
        self.assertEqual(closure_entries, {})
        generation = _closure_value(closure_context["issue"], "next_generation")
        with self.assertRaises(AuthorityError):
            closure_context["issue"](closure, "closure")
        self.assertEqual(closure_entries, {})
        self.assertEqual(_closure_value(closure_context["issue"], "next_generation"), generation)
        object.__setattr__(closure, "wheel_pin_ids", original)
        self.assertIs(closure_context["issue"](closure, "closure"), closure)
        self.assertTrue(closure_context["release"](closure))

        _adapter, checker, proposal_issue, _snapshot, proposal = _private_adapter_context()
        proposal_entries = _registry_entries(proposal_issue)
        original = proposal.status
        object.__setattr__(proposal, "status", _Hostile())
        with self.assertRaises(AuthorityError):
            checker(proposal)
        self.assertEqual(proposal_entries, {})
        generation = _closure_value(proposal_issue, "next_generation")
        with self.assertRaises(AuthorityError):
            proposal_issue(proposal, "proposal")
        self.assertEqual(proposal_entries, {})
        self.assertEqual(_closure_value(proposal_issue, "next_generation"), generation)
        object.__setattr__(proposal, "status", original)
        self.assertIs(proposal_issue(proposal, "proposal"), proposal)
        self.assertIs(checker(proposal), proposal)
        dropped = weakref.ref(proposal)
        del proposal
        gc.collect()
        self.assertIsNone(dropped())
        self.assertEqual(proposal_entries, {})
        self.assertEqual(_HOSTILE_CALLS, [])

    def _run_metadata_transient_case(
        self, producer: str, field_name: str, attacker_factory
    ) -> None:
        entered = Barrier(2)
        mutated = Barrier(2)
        captured = Barrier(2)
        restored = Barrier(2)

        def materialize(value):
            entered.wait(timeout=2)
            mutated.wait(timeout=2)
            result = replace(value)
            captured.wait(timeout=2)
            restored.wait(timeout=2)
            return result

        (
            validate_cpython,
            validate_microsoft,
            validate_pypi,
            _require,
            consume,
            release,
        ) = _freeze_metadata_seam(materialize=materialize)
        if producer == "cpython":
            source = validate_cpython(b"transient-release", b"transient-index", b"transient-bundle")
        elif producer == "microsoft":
            source = validate_microsoft(b"transient-microsoft")
        else:
            source = validate_pypi(pins.WHEEL_PIN_IDS[0], b"transient-pypi")
        issue = _closure_value(
            {
                "cpython": validate_cpython,
                "microsoft": validate_microsoft,
                "pypi": validate_pypi,
            }[producer],
            "issue",
        )
        entries = _registry_entries(issue)
        original = object.__getattribute__(source, field_name)
        attacker = attacker_factory(original)

        def mutate_and_restore() -> None:
            entered.wait(timeout=2)
            object.__setattr__(source, field_name, attacker)
            mutated.wait(timeout=2)
            captured.wait(timeout=2)
            object.__setattr__(source, field_name, original)
            restored.wait(timeout=2)

        mutator = Thread(target=mutate_and_restore, daemon=True)
        mutator.start()
        with self.assertRaises(AuthorityError):
            consume(source, producer)
        mutator.join(timeout=2)
        self.assertFalse(mutator.is_alive())
        self.assertIs(object.__getattribute__(source, field_name), original)
        self.assertEqual(entries, {})
        self.assertIs(issue(source, producer), source)
        self.assertTrue(release(source, producer))

    def test_production_metadata_transient_materialization_restore_fails_closed(self) -> None:
        cases = (
            ("cpython", "release_page_size", lambda value: value + 1),
            ("cpython", "release_page_raw", lambda value: bytes(bytearray(value))),
            ("microsoft", "raw_size", lambda value: value + 1),
            ("microsoft", "raw", lambda value: bytes(bytearray(value))),
            ("pypi", "raw_size", lambda value: value + 1),
            ("pypi", "raw", lambda value: bytes(bytearray(value))),
        )
        for producer, field_name, attacker_factory in cases:
            with self.subTest(producer=producer, field=field_name):
                self._run_metadata_transient_case(
                    producer, field_name, attacker_factory
                )

    def test_closure_and_private_proposal_transient_materialization_restore(self) -> None:
        cases = (
            ("closure", "metadata_aggregate_size", lambda value: value + 1),
            ("proposal", "size", lambda value: value + 1),
            ("proposal", "acquisition_record_raw", lambda value: bytes(bytearray(value))),
        )
        for path, field_name, attacker_factory in cases:
            with self.subTest(path=path, field=field_name):
                entered = Barrier(2)
                mutated = Barrier(2)
                captured = Barrier(2)
                restored = Barrier(2)

                def materialize(value):
                    entered.wait(timeout=2)
                    mutated.wait(timeout=2)
                    result = replace(value)
                    captured.wait(timeout=2)
                    restored.wait(timeout=2)
                    return result

                if path == "closure":
                    context = _closure_seam(materialize=materialize)
                    source = context["closure"]
                    consume = context["consume"]
                    issue = context["issue"]
                    release = context["release"]
                    kind = "closure"
                else:
                    _adapter, checker, _private_issue, snapshot, source = (
                        _private_adapter_context()
                    )
                    issue, _require, consume_raw, release_raw = (
                        _exact_snapshot_registry(snapshot, materialize=materialize)
                    )
                    issue(source, "authority")
                    consume = lambda value: consume_raw(value, "authority")
                    release = lambda value: release_raw(value, "authority")
                    kind = "authority"
                entries = _registry_entries(issue)
                original = object.__getattribute__(source, field_name)
                attacker = attacker_factory(original)

                def mutate_and_restore() -> None:
                    entered.wait(timeout=2)
                    object.__setattr__(source, field_name, attacker)
                    mutated.wait(timeout=2)
                    captured.wait(timeout=2)
                    object.__setattr__(source, field_name, original)
                    restored.wait(timeout=2)

                mutator = Thread(target=mutate_and_restore, daemon=True)
                mutator.start()
                with self.assertRaises(AuthorityError):
                    consume(source)
                mutator.join(timeout=2)
                self.assertFalse(mutator.is_alive())
                self.assertIs(object.__getattribute__(source, field_name), original)
                self.assertEqual(entries, {})
                self.assertIs(issue(source, kind), source)
                self.assertTrue(release(source))
                if path == "proposal":
                    self.assertIs(checker(source), source)


class ConsumeRaceTests(unittest.TestCase):
    def _assert_empty_and_recover(self, issue, release, entries, value) -> None:
        self.assertEqual(entries, {})
        self.assertIs(issue(value, "authority"), value)
        self.assertTrue(release(value, "authority"))
        self.assertEqual(entries, {})

    def test_transient_mutation_and_restore_of_every_snapshot_field_fails_closed(self) -> None:
        cases = {
            "authority": "TRANSIENT-ATTACKER",
            "number": 8,
            "permitted": True,
            "inventory": ("attacker",),
            "raw": bytes(bytearray(b"raw-authority")),
        }
        for field_name, attacker_value in cases.items():
            with self.subTest(field=field_name):
                materializer_entered = Barrier(2)
                mutation_visible = Barrier(2)
                detached_captured = Barrier(2)
                source_restored = Barrier(2)

                def materialize(value):
                    materializer_entered.wait(timeout=2)
                    mutation_visible.wait(timeout=2)
                    result = replace(value)
                    detached_captured.wait(timeout=2)
                    source_restored.wait(timeout=2)
                    return result

                issue, _require, consume, release = _race_registry(materialize)
                source = issue(_race_value(), "authority")
                entries = _registry_entries(issue)
                original = getattr(source, field_name)

                def mutate_and_restore() -> None:
                    materializer_entered.wait(timeout=2)
                    object.__setattr__(source, field_name, attacker_value)
                    mutation_visible.wait(timeout=2)
                    detached_captured.wait(timeout=2)
                    object.__setattr__(source, field_name, original)
                    source_restored.wait(timeout=2)

                mutator = Thread(target=mutate_and_restore, daemon=True)
                mutator.start()
                with self.assertRaisesRegex(AuthorityError, "race_not_issued_or_changed"):
                    consume(source, "authority")
                mutator.join(timeout=2)
                self.assertFalse(mutator.is_alive())
                self.assertEqual(getattr(source, field_name), original)
                self._assert_empty_and_recover(issue, release, entries, source)

    def test_result_raw_identity_mismatch_fails_closed_and_recovers(self) -> None:
        source = _race_value()
        issue, _require, consume, release = _race_registry(
            lambda value: replace(value, raw=bytes(bytearray(value.raw)))
        )
        issue(source, "authority")
        entries = _registry_entries(issue)
        with self.assertRaisesRegex(AuthorityError, "race_not_issued_or_changed"):
            consume(source, "authority")
        self._assert_empty_and_recover(issue, release, entries, source)

    def test_same_object_wrong_type_and_materializer_exception_cleanup(self) -> None:
        def materializer_error(_value):
            raise RuntimeError("race_materializer_failure")

        cases = (
            ("same_object", lambda value: value, AuthorityError, "race_not_issued_or_changed"),
            ("wrong_type", lambda _value: object(), AuthorityError, "race_snapshot_type_invalid"),
            ("exception", materializer_error, RuntimeError, "race_materializer_failure"),
        )
        for label, materialize, error_type, message in cases:
            with self.subTest(case=label):
                issue, _require, consume, release = _race_registry(materialize)
                source = issue(_race_value(), "authority")
                entries = _registry_entries(issue)
                with self.assertRaisesRegex(error_type, message):
                    consume(source, "authority")
                self._assert_empty_and_recover(issue, release, entries, source)

    def test_source_and_result_snapshot_exceptions_cleanup(self) -> None:
        for phase in ("source_pre", "result", "source_post"):
            with self.subTest(phase=phase):
                state = {"enabled": False, "result": None, "source_calls": 0}
                source = _race_value()

                def snapshot(value):
                    if value is source:
                        state["source_calls"] += 1
                        if state["enabled"] and phase == "source_pre":
                            raise AuthorityError("race_source_pre_snapshot_failure")
                        if (
                            state["enabled"]
                            and phase == "source_post"
                            and state["source_calls"] >= 3
                        ):
                            raise AuthorityError("race_source_post_snapshot_failure")
                    if state["enabled"] and phase == "result" and value is state["result"]:
                        raise AuthorityError("race_result_snapshot_failure")
                    return _race_snapshot(value)

                def materialize(value):
                    result = replace(value)
                    state["result"] = result
                    return result

                issue, _require, consume, release = _race_registry(
                    materialize, snapshot=snapshot
                )
                issue(source, "authority")
                entries = _registry_entries(issue)
                state["enabled"] = True
                with self.assertRaisesRegex(AuthorityError, f"race_{phase}_snapshot_failure"):
                    consume(source, "authority")
                state["enabled"] = False
                self._assert_empty_and_recover(issue, release, entries, source)

    def test_successful_distinct_consume_is_one_time(self) -> None:
        issue, _require, consume, release = _race_registry(replace)
        source = issue(_race_value(), "authority")
        entries = _registry_entries(issue)
        result = consume(source, "authority")
        self.assertIsNot(result, source)
        self.assertEqual(_race_snapshot(result), _race_snapshot(source))
        self.assertIs(result.raw, source.raw)
        self.assertEqual(entries, {})
        with self.assertRaisesRegex(AuthorityError, "race_not_issued_or_changed"):
            consume(source, "authority")
        self._assert_empty_and_recover(issue, release, entries, source)

    def test_concurrent_consume_wins_and_release_observes_absence(self) -> None:
        materializer_entered = Event()
        materializer_resume = Event()
        release_started = Event()
        outcomes: dict[str, object] = {}

        def materialize(value):
            materializer_entered.set()
            if not materializer_resume.wait(timeout=2):
                raise RuntimeError("race_materializer_timeout")
            return replace(value)

        issue, _require, consume, release = _race_registry(materialize)
        source = issue(_race_value(), "authority")
        entries = _registry_entries(issue)

        def consume_worker() -> None:
            try:
                outcomes["consume"] = consume(source, "authority")
            except BaseException as exc:
                outcomes["consume_error"] = exc

        def release_worker() -> None:
            release_started.set()
            try:
                outcomes["release"] = release(source, "authority")
            except BaseException as exc:
                outcomes["release_error"] = exc

        consumer = Thread(target=consume_worker, daemon=True)
        consumer.start()
        self.assertTrue(materializer_entered.wait(timeout=2))
        releaser = Thread(target=release_worker, daemon=True)
        releaser.start()
        self.assertTrue(release_started.wait(timeout=2))
        self.assertTrue(releaser.is_alive())
        materializer_resume.set()
        consumer.join(timeout=2)
        releaser.join(timeout=2)
        self.assertFalse(consumer.is_alive())
        self.assertFalse(releaser.is_alive())
        self.assertNotIn("consume_error", outcomes)
        self.assertNotIn("release_error", outcomes)
        self.assertIsInstance(outcomes["consume"], _RaceEvidence)
        self.assertIs(outcomes["release"], False)
        self._assert_empty_and_recover(issue, release, entries, source)

    def test_reentrant_aba_newer_entry_is_preserved(self) -> None:
        source = _race_value()
        newer = replace(source, number=8)
        context: dict[str, object] = {}

        def materialize(value):
            release = context["release"]
            issue = context["issue"]
            entries = context["entries"]
            self.assertTrue(release(value, "authority"))
            issue(newer, "authority")
            newer_entry = entries.pop(id(newer))
            entries[id(value)] = newer_entry
            context["newer_entry"] = newer_entry
            return replace(value)

        issue, _require, consume, release = _race_registry(materialize)
        issue(source, "authority")
        entries = _registry_entries(issue)
        old_entry = entries[id(source)]
        context.update(issue=issue, release=release, entries=entries)
        with self.assertRaisesRegex(AuthorityError, "race_not_issued_or_changed"):
            consume(source, "authority")
        newer_entry = context["newer_entry"]
        self.assertIs(entries[id(source)], newer_entry)
        self.assertGreater(newer_entry[0], old_entry[0])
        self.assertIs(newer_entry[1](), newer)
        entries[id(newer)] = entries.pop(id(source))
        self.assertTrue(release(newer, "authority"))
        self.assertEqual(entries, {})

    def test_reentrant_release_issue_and_weak_callback_complete_without_deadlock(self) -> None:
        context: dict[str, object] = {}
        weak_state: dict[str, object] = {}

        def materialize(value):
            self.assertTrue(context["release"](value, "authority"))
            temporary = context["issue"](
                replace(value, number=value.number + 1), "authority"
            )
            weak_state["reference"] = weakref.ref(temporary)
            del temporary
            gc.collect()
            return replace(value)

        issue, _require, consume, release = _race_registry(materialize)
        source = issue(_race_value(), "authority")
        entries = _registry_entries(issue)
        context.update(issue=issue, release=release)
        outcome: dict[str, object] = {}

        def worker() -> None:
            try:
                consume(source, "authority")
            except BaseException as exc:
                outcome["error"] = exc

        thread = Thread(target=worker, daemon=True)
        thread.start()
        thread.join(timeout=2)
        self.assertFalse(thread.is_alive(), "reentrant weak callback deadlocked")
        self.assertIsInstance(outcome.get("error"), AuthorityError)
        self.assertEqual(str(outcome["error"]), "race_not_issued_or_changed")
        self.assertIsNone(weak_state["reference"]())
        self._assert_empty_and_recover(issue, release, entries, source)


class ClosureCleanupTests(unittest.TestCase):
    def _context(self):
        (
            _validate_cpython,
            _validate_microsoft,
            validate_pypi,
            _require_metadata,
            consume_metadata,
            release_metadata,
        ) = _freeze_metadata_seam()
        control = {"phase": None, "position": -1}

        def metadata_validator(pin_id: str, raw: bytes):
            position = pins.WHEEL_PIN_IDS.index(pin_id)
            if control["phase"] == "metadata" and control["position"] == position:
                raise AuthorityError("test_metadata_revalidation_failure")
            value = validate_pypi(pin_id, raw)
            if control["phase"] == "mismatch" and control["position"] == position:
                object.__setattr__(value, "raw_size", value.raw_size + 1)
            return value

        wheels = _wheel_inputs()

        def wheel_validator(pin_id: str, raw: bytes):
            position = pins.WHEEL_PIN_IDS.index(pin_id)
            if control["phase"] == "wheel" and control["position"] == position:
                raise AuthorityError("test_wheel_validation_failure")
            value = wheels[pin_id]
            if raw is not value.raw:
                raise AuthorityError("test_wheel_raw_identity_changed")
            return value

        validate_closure, require_closure, consume_closure, release_closure = (
            wheel._freeze_closure_validator(
                metadata_validator,
                consume_metadata,
                release_metadata,
                wheel_validator,
            )
        )
        return {
            "control": control,
            "release_closure": release_closure,
            "release_metadata": release_metadata,
            "validate_closure": validate_closure,
            "validate_pypi": validate_pypi,
            "wheels": wheels,
        }

    def _assert_recovered(self, context) -> None:
        context["control"]["phase"] = None
        values = _metadata_inputs(context["validate_pypi"])
        closure = context["validate_closure"](values, context["wheels"])
        self.assertIs(closure.extras_selected, False)
        self.assertIs(closure.imported, False)
        self.assertIs(closure.installed, False)
        self.assertIs(closure.runtime_authority, False)
        self.assertTrue(context["release_closure"](closure))

    def test_success_and_every_six_position_failure_release_all_metadata(self) -> None:
        success = self._context()
        values = _metadata_inputs(success["validate_pypi"])
        closure = success["validate_closure"](values, success["wheels"])
        self.assertEqual(closure.wheel_pin_ids, pins.WHEEL_PIN_IDS)
        self.assertEqual(closure.dependency_graph, pins.JSONSCHEMA_DEPENDENCY_GRAPH)
        self.assertTrue(success["release_closure"](closure))
        self._assert_recovered(success)

        for phase in ("consume", "metadata", "wheel", "mismatch"):
            for position in range(6):
                with self.subTest(phase=phase, position=position):
                    context = self._context()
                    values = _metadata_inputs(context["validate_pypi"])
                    if phase == "consume":
                        target = values[pins.WHEEL_PIN_IDS[position]]
                        self.assertTrue(context["release_metadata"](target, "pypi"))
                    else:
                        context["control"].update(phase=phase, position=position)
                    with self.assertRaises(AuthorityError):
                        context["validate_closure"](values, context["wheels"])
                    self._assert_recovered(context)

    def test_closure_issue_capacity_failure_cleans_metadata_and_recovers(self) -> None:
        context = self._context()
        first = context["validate_closure"](
            _metadata_inputs(context["validate_pypi"]), context["wheels"]
        )
        with self.assertRaisesRegex(
            AuthorityError, "jsonschema_closure_registry_capacity_exceeded"
        ):
            context["validate_closure"](
                _metadata_inputs(context["validate_pypi"]), context["wheels"]
            )
        self.assertTrue(context["release_closure"](first))
        self._assert_recovered(context)


class CandidateCleanupTests(unittest.TestCase):
    def test_partial_consume_and_semantic_failures_release_all_entries(self) -> None:
        context = _candidate_context()
        self.assertTrue(context["release_metadata"](context["microsoft"], "microsoft"))
        with self.assertRaisesRegex(AuthorityError, "metadata_evidence_not_issued_or_changed"):
            context["assemble"](
                cpython=context["cpython"],
                microsoft=context["microsoft"],
                jsonschema_closure=context["closure"],
            )
        _assert_candidate_capacity_recovered(self, context)

        context = _candidate_context()
        self.assertTrue(context["release_closure"](context["closure"], "closure"))
        with self.assertRaisesRegex(AuthorityError, "test_closure_not_issued_or_changed"):
            context["assemble"](
                cpython=context["cpython"],
                microsoft=context["microsoft"],
                jsonschema_closure=context["closure"],
            )
        _assert_candidate_capacity_recovered(self, context)

        context = _candidate_context(cpython_forbidden=True)
        with self.assertRaisesRegex(AuthorityError, "candidate_sigstore_cryptographic_claim_forbidden"):
            context["assemble"](
                cpython=context["cpython"],
                microsoft=context["microsoft"],
                jsonschema_closure=context["closure"],
            )
        _assert_candidate_capacity_recovered(self, context)

        context = _candidate_context(closure_forbidden=True)
        with self.assertRaisesRegex(AuthorityError, "candidate_jsonschema_downstream_claim_forbidden"):
            context["assemble"](
                cpython=context["cpython"],
                microsoft=context["microsoft"],
                jsonschema_closure=context["closure"],
            )
        _assert_candidate_capacity_recovered(self, context)

    def test_private_proposal_cannot_satisfy_candidate_and_cleanup_recovers(self) -> None:
        context = _candidate_context()
        proposal, checker = _private_proposal()
        self.assertIs(checker(proposal), proposal)
        with self.assertRaisesRegex(AuthorityError, f"^{BLOCKER}$"):
            context["assemble"](
                cpython=context["cpython"],
                microsoft=context["microsoft"],
                jsonschema_closure=context["closure"],
                buildtools_proposal=proposal,
            )
        _assert_candidate_capacity_recovered(self, context)
        with self.assertRaisesRegex(AuthorityError, f"^{BLOCKER}$"):
            buildtools._require_issued_buildtools_proposal(proposal)

    def test_success_preserves_permanent_blockers_nonclaims_and_downstream_false(self) -> None:
        context = _candidate_context()
        state = context["assemble"](
            cpython=context["cpython"],
            microsoft=context["microsoft"],
            jsonschema_closure=context["closure"],
        )
        self.assertIn(BLOCKER, state.blockers)
        self.assertIn(LIVE_BLOCKER, state.blockers)
        self.assertIsNone(state.buildtools_proposal_sha256)
        self.assertIsNone(state.buildtools_acquired_path)
        self.assertIsNone(state.buildtools_verifier_full_path)
        self.assertTrue(all(value is False for _name, value in state.nonclaims))
        for field_name in (
            "acquired_or_downloaded_byte_executed",
            "imported",
            "installed",
            "compiled",
            "linked",
            "process_authority",
            "active_buildtools_authority",
            "offline_toolchain_layout",
            "build",
            "runtime",
            "rehearsal",
            "s0",
            "e0",
            "central_system",
            "project_brain_integration",
            "operational_safety",
            "economic_value",
            "model_to_model_transfer",
        ):
            self.assertIs(getattr(state, field_name), False, field_name)
        _assert_candidate_capacity_recovered(self, context)


if __name__ == "__main__":
    unittest.main(verbosity=2)

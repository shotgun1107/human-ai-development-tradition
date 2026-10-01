"""Same-process, one-use live publication consumer."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

from .authority import _PublicationWitness, _is_witness
from .canonical import expected_receipt_bytes, expected_run_record_bytes
from .errors import record_failure
from .observer import PublicationObserver
from .pins import ExternalPins
from .win32 import ABI_PROFILE_ID, _is_authenticated_win32_backend


CONSUMER_ID = "S0-PUBLIC-ASSEMBLY-LIVE-CONSUMER-2"
_LIVE_DECISION_TOKEN = object()
_LIVE_DECISION_REGISTRY: dict[int, tuple[object, object, object]] = {}
_ISSUED_WITNESS_IDENTITIES: set[int] = set()


class LiveDecision:
    """Opaque one-process authority; there is no public value constructor."""

    __slots__ = ("_token", "_witness", "_observer")

    def __init__(
        self,
        token: object = None,
        witness: object = None,
        observer: object = None,
    ) -> None:
        if token is not _LIVE_DECISION_TOKEN:
            raise TypeError("live decision has no public constructor")
        self._token = token
        self._witness = witness
        self._observer = observer

    def _require_authority(self) -> None:
        registered = _LIVE_DECISION_REGISTRY.get(id(self))
        if (
            getattr(self, "_token", None) is not _LIVE_DECISION_TOKEN
            or registered is None
            or registered[0] is not self
            or registered[1] is not getattr(self, "_witness", None)
            or registered[2] is not getattr(self, "_observer", None)
            or not _is_witness(self._witness)
            or self._witness.used is not True
            or self._witness.observer is not self._observer
            or not _is_authenticated_win32_backend(self._observer._backend)
        ):
            raise TypeError("live decision authority is invalid")

    @property
    def accepted(self) -> bool:
        self._require_authority()
        return True

    @property
    def claim_kind(self) -> str:
        self._require_authority()
        return "same-process-live-consumer-acceptance-only-not-s0"

    def __copy__(self) -> object:
        raise TypeError("live decisions cannot be copied")

    def __deepcopy__(self, memo: dict[int, object]) -> object:
        del memo
        raise TypeError("live decisions cannot be deep-copied")

    def __reduce__(self) -> object:
        raise TypeError("live decisions cannot be serialized")

    def __repr__(self) -> str:
        self._require_authority()
        return "<LiveDecision private-process-local>"


def _issue_live_decision(
    witness: _PublicationWitness,
    observer: PublicationObserver,
) -> LiveDecision:
    witness_identity = id(witness)
    if (
        not _is_witness(witness)
        or witness.used is not True
        or witness.observer is not observer
        or not _is_authenticated_win32_backend(observer._backend)
        or witness_identity in _ISSUED_WITNESS_IDENTITIES
    ):
        raise record_failure("live decision authority cannot be issued")
    decision = LiveDecision(_LIVE_DECISION_TOKEN, witness, observer)
    _ISSUED_WITNESS_IDENTITIES.add(witness_identity)
    _LIVE_DECISION_REGISTRY[id(decision)] = (decision, witness, observer)
    return decision


@dataclass(frozen=True)
class DiagnosticPredicateDecision:
    predicates_satisfied: bool
    claim_kind: str = "unit-test-predicates-only-not-live-acceptance-not-rehearsal-pass"


class LiveConsumer:
    """The sole in-process authority that may accept a rehearsal result."""

    __slots__ = ()

    def consume(
        self,
        *,
        workspace_root: Path,
        observer: PublicationObserver,
        witness: object,
        child_identity: object,
        parent_pipe_identity: object,
        external_pins: ExternalPins,
        quarantined: bool,
    ) -> LiveDecision:
        self._consume_predicates(
            workspace_root=workspace_root,
            observer=observer,
            witness=witness,
            child_identity=child_identity,
            parent_pipe_identity=parent_pipe_identity,
            external_pins=external_pins,
            quarantined=quarantined,
            require_authenticated_backend=True,
        )
        assert isinstance(witness, _PublicationWitness)
        return _issue_live_decision(witness, observer)

    def _consume_predicates(
        self,
        *,
        workspace_root: Path,
        observer: PublicationObserver,
        witness: object,
        child_identity: object,
        parent_pipe_identity: object,
        external_pins: ExternalPins,
        quarantined: bool,
        require_authenticated_backend: bool = False,
    ) -> None:
        if not _is_witness(witness):
            raise record_failure("live consumer requires the exact private witness type")
        assert isinstance(witness, _PublicationWitness)
        # The first terminal attempt irrevocably spends the witness/capability
        # pair before any predicate that can reject.  Repairing residue or
        # changing arguments therefore cannot turn a rejected run into an
        # accepted retry.
        with witness.lock:
            if witness.used:
                raise record_failure("publication witness was already consumed")
            witness.used = True
            if type(observer) is not PublicationObserver:
                raise record_failure("live consumer requires the exact observer type")
            if require_authenticated_backend and not _is_authenticated_win32_backend(
                observer._backend
            ):
                raise record_failure(
                    "only an authenticated real Win32 backend can reach live acceptance"
                )
            if quarantined:
                raise record_failure("quarantined output root cannot be consumed")
            if (
                witness.observer is not observer
                or witness.capability is not observer._capability
                or witness.child is not child_identity
                or witness.pipe is not parent_pipe_identity
                or witness.root != observer.output_root
                or witness.events != observer.trace
                or len(witness.events) != 2
                or tuple(event.ordinal for event in witness.events) != (1, 2)
            ):
                raise record_failure("witness, observer, child, pipe, root, or trace binding mismatch")
            capability = witness.capability
            if (
                capability.observer is not observer
                or capability.child is not child_identity
                or capability.pipe is not parent_pipe_identity
                or capability.root != observer.output_root
                or capability.terminal is not True
            ):
                raise record_failure("spent run capability binding changed before consumption")
            expected_pairs = (
                (Path("run-record.pending"), Path("run-record.json")),
                (Path("publication-receipt.pending"), Path("publication-receipt.json")),
            )
            for event, (source, destination) in zip(
                witness.events, expected_pairs, strict=True
            ):
                if (
                    event.observer_instance_identity != id(observer)
                    or event.run_capability_identity != id(capability)
                    or event.output_root_identity != observer.root_identity
                    or event.source_path != observer._backend.canonical_event_path(source)
                    or event.destination_path
                    != observer._backend.canonical_event_path(destination)
                    or event.destination_absent_before_call is not True
                    or event.abi_profile_id != ABI_PROFILE_ID
                    or type(event.flags_numeric) is not int
                    or event.flags_numeric != 0
                    or type(event.ffi_return_signed_int32) is not int
                    or event.ffi_return_signed_int32 == 0
                    or type(event.last_error_uint32) is not int
                    or event.last_error_uint32 != 0
                    or event.source_absent_after_success is not True
                    or event.terminal_status != "success"
                ):
                    raise record_failure("publication trace has a non-frozen event field")
            self._validate_files(workspace_root, observer, witness, external_pins)

    def _validate_files(
        self,
        workspace_root: Path,
        observer: PublicationObserver,
        witness: _PublicationWitness,
        external_pins: ExternalPins,
    ) -> None:
        backend = observer._backend
        for pending in (Path("run-record.pending"), Path("publication-receipt.pending")):
            if not backend.path_absent(pending):
                raise record_failure("pending publication name remains at live consumption")
        record = backend.inspect_file(Path("run-record.json"))
        receipt = backend.inspect_file(Path("publication-receipt.json"))
        expected_record = expected_run_record_bytes(workspace_root)
        expected_receipt = expected_receipt_bytes(workspace_root, external_pins.receipt_fields())
        if record.byte_length != len(expected_record) or record.sha256 != hashlib.sha256(expected_record).hexdigest():
            raise record_failure("current run record differs from frozen v3 bytes")
        if receipt.byte_length != len(expected_receipt) or receipt.sha256 != hashlib.sha256(expected_receipt).hexdigest():
            raise record_failure("current receipt differs from the externally frozen v2 bytes")
        for snapshot, event in zip((record, receipt), witness.events, strict=True):
            event_identity = (
                event.post_volume_serial_number,
                event.post_file_index_high,
                event.post_file_index_low,
            )
            current_identity = (
                snapshot.identity.volume_serial_number,
                snapshot.identity.file_index_high,
                snapshot.identity.file_index_low,
            )
            if (
                current_identity != event_identity
                or snapshot.byte_length != event.post_byte_length
                or snapshot.sha256 != event.post_sha256
            ):
                raise record_failure("current final file no longer matches its observed move event")


def _exercise_consumer_predicates_for_tests(
    *,
    workspace_root: Path,
    observer: PublicationObserver,
    witness: object,
    child_identity: object,
    parent_pipe_identity: object,
    external_pins: ExternalPins,
    quarantined: bool,
) -> DiagnosticPredicateDecision:
    """Exercise predicates without granting the real-backend acceptance type."""

    LiveConsumer()._consume_predicates(
        workspace_root=workspace_root,
        observer=observer,
        witness=witness,
        child_identity=child_identity,
        parent_pipe_identity=parent_pipe_identity,
        external_pins=external_pins,
        quarantined=quarantined,
    )
    return DiagnosticPredicateDecision(True)

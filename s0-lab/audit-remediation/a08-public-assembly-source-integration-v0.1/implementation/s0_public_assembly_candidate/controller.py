"""Ten-state bounded public child controller."""

from __future__ import annotations

import hashlib
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable

from .canonical import load_strict_json_bytes
from .channel import FixedAsciiPipeChannel
from .components import (
    ComponentApis,
    authenticate_component_manifests,
    load_component_apis,
)
from .constants import (
    ANSWER_SCHEMA_PATH,
    ANSWER_SCHEMA_SHA256,
    CANONICAL_PATH,
    CANONICAL_SHA256,
    I2_CONTRACT_PATH,
    I2_CONTRACT_SHA256,
    I3_CONTRACT_PATH,
    I3_CONTRACT_SHA256,
    PACKAGE_PATH,
    PACKAGE_SHA256,
    PUBLIC_BUNDLE_ENTRY_COUNT,
    PUBLIC_RESPONSE_BYTES,
    PUBLIC_RESPONSE_PATH,
    PUBLIC_RESPONSE_SHA256,
    QUESTIONS_PATH,
    QUESTIONS_SHA256,
    REHEARSAL_ID,
    REPRESENTATION_ID,
    REQUEST_BYTES,
    REQUEST_ENTRY_PREFIX,
    REQUEST_MANIFEST_BYTES,
    REQUEST_MANIFEST_PATH,
    REQUEST_MANIFEST_SHA256,
    REQUEST_PATH,
    REQUEST_PURPOSE,
    REQUEST_SHA256,
    RUN_RECORD_SHA256,
    STATE_ORDER,
)
from .errors import (
    AR_ANSWER,
    AR_AUTH,
    AR_BOUNDARY,
    AR_DETERMINISM,
    AR_INVOKE,
    AR_RECORD,
    AR_RESERVE,
    AR_RESPONSE,
    AR_TRANSFORM,
    AssemblyRunFailed,
    BoundaryViolation,
    FailureDiagnostic,
    StageFailure,
)
from .records import (
    ExternalPins,
    RunObservation,
    build_receipt_v2,
    build_run_record_v3,
    serialize_run_record_v3,
    validate_external_pins,
)
from .request import reconstruct_request, require_materialized_request
from .runtime_guard import require_runtime_sentinels_healthy_if_installed
from .storage import (
    OutputReservation,
    read_workspace_file,
    workspace_path,
)
from .stub import ExactAnswerStub, StubCounters


@dataclass(frozen=True)
class ControllerResult:
    """Child completion only; this object never represents rehearsal PASS."""

    schema_id: str
    state: str
    result: str
    offline_status: str
    rehearsal_pass_authority: str
    rehearsal_pass: bool
    run_record_sha256: str
    publication_receipt_sha256: str
    stub_transport_calls: int
    stub_close_count: int

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


class _StateMachine:
    def __init__(self) -> None:
        self._index = 0

    @property
    def state(self) -> str:
        return STATE_ORDER[self._index]

    def advance(self, target: str) -> None:
        if self._index + 1 >= len(STATE_ORDER) or STATE_ORDER[self._index + 1] != target:
            raise RuntimeError("controller state transition is not the frozen next state")
        self._index += 1


class AssemblyController:
    """Run the fixed public I0/I1 flow and request parent-owned publication."""

    def __init__(
        self,
        *,
        workspace_root: Path,
        output_root: Path,
        external_pins: ExternalPins,
        publication_channel: FixedAsciiPipeChannel,
        components: ComponentApis | None = None,
        component_loader: Callable[[Path], ComponentApis] = load_component_apis,
    ) -> None:
        self.workspace_root = workspace_root
        self.output_root = output_root
        self.external_pins = external_pins
        self.publication_channel = publication_channel
        self._supplied_components = components
        self._component_loader = component_loader
        self._machine = _StateMachine()
        self._storage: OutputReservation | None = None
        self._stub: ExactAnswerStub | None = None
        self._current_operation = "controller-initialization"
        self._current_failure_class = AR_AUTH

    @property
    def state(self) -> str:
        return self._machine.state

    def _stage(
        self,
        failure_class: str,
        operation: str,
        action: Callable[[], object],
    ) -> object:
        self._current_failure_class = failure_class
        self._current_operation = operation
        try:
            require_runtime_sentinels_healthy_if_installed()
            result = action()
            # The frozen commit point permits no fallible candidate operation
            # after the second parent OK.  Every earlier stage rechecks the
            # latched runtime boundary before its result can be relied upon.
            if operation != "publish-receipt-request":
                require_runtime_sentinels_healthy_if_installed()
            return result
        except BoundaryViolation:
            raise
        except StageFailure:
            raise
        except Exception as exc:
            raise StageFailure(failure_class, operation, type(exc).__name__) from exc

    def _load_components(self) -> ComponentApis:
        if self._supplied_components is None:
            return self._component_loader(self.workspace_root)
        authenticate_component_manifests(self.workspace_root)
        return self._supplied_components

    def _authenticate_inputs(self) -> tuple[
        ComponentApis,
        bytes,
        bytes,
        bytes,
        bytes,
        bytes,
    ]:
        validate_external_pins(self.external_pins)
        components = self._load_components()

        canonical_raw = read_workspace_file(
            self.workspace_root,
            CANONICAL_PATH,
            expected_sha256=CANONICAL_SHA256,
        )
        package_raw = read_workspace_file(
            self.workspace_root,
            PACKAGE_PATH,
            expected_sha256=PACKAGE_SHA256,
        )
        questions_raw = read_workspace_file(
            self.workspace_root,
            QUESTIONS_PATH,
            expected_sha256=QUESTIONS_SHA256,
        )
        response_raw = read_workspace_file(
            self.workspace_root,
            PUBLIC_RESPONSE_PATH,
            expected_sha256=PUBLIC_RESPONSE_SHA256,
            expected_bytes=PUBLIC_RESPONSE_BYTES,
        )
        read_workspace_file(
            self.workspace_root,
            ANSWER_SCHEMA_PATH,
            expected_sha256=ANSWER_SCHEMA_SHA256,
        )
        read_workspace_file(
            self.workspace_root,
            I2_CONTRACT_PATH,
            expected_sha256=I2_CONTRACT_SHA256,
        )
        read_workspace_file(
            self.workspace_root,
            I3_CONTRACT_PATH,
            expected_sha256=I3_CONTRACT_SHA256,
        )
        request_manifest_raw = read_workspace_file(
            self.workspace_root,
            REQUEST_MANIFEST_PATH,
            expected_sha256=REQUEST_MANIFEST_SHA256,
            expected_bytes=len(REQUEST_MANIFEST_BYTES),
        )
        if request_manifest_raw != REQUEST_MANIFEST_BYTES:
            raise ValueError("request manifest bytes are not the frozen one-row authority")
        request_artifact_raw = read_workspace_file(
            self.workspace_root,
            REQUEST_PATH,
            expected_sha256=REQUEST_SHA256,
            expected_bytes=REQUEST_BYTES,
        )

        components.i2_verify_contract_file(
            workspace_path(self.workspace_root, I2_CONTRACT_PATH)
        )
        components.i3_verify_contract_file(
            workspace_path(self.workspace_root, I3_CONTRACT_PATH)
        )
        bundle_result = components.i0_verify_public_bundle(self.workspace_root)
        if (
            type(bundle_result) is not dict
            or type(bundle_result.get("manifest_entries")) is not int
            or bundle_result["manifest_entries"] != PUBLIC_BUNDLE_ENTRY_COUNT
        ):
            raise ValueError("I0 public bundle result did not authenticate 90 entries")
        return (
            components,
            canonical_raw,
            package_raw,
            questions_raw,
            response_raw,
            request_artifact_raw,
        )

    def _ordered_run(self) -> ControllerResult:
        authenticated = self._stage(
            AR_AUTH,
            "preflight-authentication",
            self._authenticate_inputs,
        )
        assert isinstance(authenticated, tuple)
        (
            components,
            canonical_raw,
            package_raw,
            questions_raw,
            response_raw,
            request_artifact_raw,
        ) = authenticated
        self._machine.advance("PREFLIGHT_AUTHENTICATED")

        def transform() -> None:
            canonical = load_strict_json_bytes(canonical_raw, require_object=True)
            transformed = components.i0_transform_canonical(canonical, REPRESENTATION_ID)
            if type(transformed) is not bytes or transformed != package_raw:
                raise ValueError("I0 transformed bytes differ from the frozen package")

        self._stage(AR_TRANSFORM, "i0-transform-comparison", transform)

        reconstructed = self._stage(
            AR_AUTH,
            "request-reconstruction",
            lambda: reconstruct_request(package_raw, questions_raw),
        )
        require_materialized_request(reconstructed, request_artifact_raw)

        def bind_request() -> tuple[object, object]:
            grant = components.i1_bind_external_manifest_grant(
                expected_manifest_path=REQUEST_MANIFEST_PATH,
                expected_manifest_sha256=REQUEST_MANIFEST_SHA256,
                expected_entry_prefix=REQUEST_ENTRY_PREFIX,
                expected_allowed_paths=(REQUEST_PATH,),
                purpose=REQUEST_PURPOSE,
            )
            manifest = components.i1_load_authenticated_manifest(
                self.workspace_root,
                grant,
            )
            authenticated_request = components.i1_authenticate_manifest_entry(
                self.workspace_root,
                manifest,
                REQUEST_PATH,
                max_bytes=REQUEST_BYTES,
            )
            if (
                getattr(authenticated_request, "raw", None) != reconstructed.raw
                or getattr(authenticated_request, "sha256", None) != REQUEST_SHA256
            ):
                raise ValueError("I1 authenticated request binding mismatch")
            return grant, authenticated_request

        bound = self._stage(AR_AUTH, "i1-request-grant-binding", bind_request)
        assert isinstance(bound, tuple)
        grant, authenticated_request = bound

        self._stub = self._stage(
            AR_INVOKE,
            "stub-construction",
            lambda: ExactAnswerStub(
                expected_request_raw=reconstructed.raw,
                response_raw=response_raw,
                response_frame_type=components.i1_response_frame_type,
            ),
        )
        assert isinstance(self._stub, ExactAnswerStub)
        self._machine.advance("REQUEST_RECONSTRUCTED")

        self._storage = self._stage(
            AR_RESERVE,
            "four-name-output-reservation",
            lambda: OutputReservation.reserve(self.output_root),
        )
        assert isinstance(self._storage, OutputReservation)
        self._machine.advance("OUTPUT_RESERVED")

        self._machine.advance("RUNNER_ENTERED")

        def invoke() -> tuple[object, StubCounters]:
            result = components.i1_run_one_shot(
                REHEARSAL_ID,
                authenticated_request,
                self._stub,
                required_grant=grant,
                expected_authority_sha256=REQUEST_MANIFEST_SHA256,
                expected_authority_path=REQUEST_MANIFEST_PATH,
                expected_request_path=REQUEST_PATH,
                expected_purpose=REQUEST_PURPOSE,
            )
            counters = self._stub.require_integrity()
            return result, counters

        invoked = self._stage(AR_INVOKE, "i1-run-and-stub-integrity", invoke)
        assert isinstance(invoked, tuple)
        one_shot_result, counters = invoked
        self._machine.advance("INVOKED_ONCE")

        def compare_response() -> None:
            raw = getattr(one_shot_result, "raw_response", None)
            if type(raw) is not bytes or raw != response_raw:
                raise ValueError("I1 response bytes differ from the fixed public answer")
            if hashlib.sha256(raw).hexdigest() != PUBLIC_RESPONSE_SHA256:
                raise ValueError("I1 response hash differs from the fixed public answer")

        self._stage(AR_RESPONSE, "response-comparison", compare_response)
        self._machine.advance("RESPONSE_CAPTURED")

        validation_errors = self._stage(
            AR_ANSWER,
            "i0-answer-validation",
            lambda: components.i0_validate_answer_candidate_bytes(
                self.workspace_root,
                response_raw,
                answer_schema=ANSWER_SCHEMA_PATH,
                questions=QUESTIONS_PATH,
                input_package=PACKAGE_PATH,
            ),
        )
        if type(validation_errors) is not list or validation_errors:
            raise StageFailure(AR_ANSWER, "i0-answer-validation", "nonempty-errors")
        self._machine.advance("ANSWER_VALIDATED")

        observation = RunObservation(
            actual_response_sha256=PUBLIC_RESPONSE_SHA256,
            answer_validation_error_count=len(validation_errors),
            denied_input_access_count=0,
            retry_count=0,
            response_frames=counters.yielded_frame_count,
            final_frames=counters.yielded_final_frame_count,
            transport_calls=counters.transport_calls,
            stub_script_frame_count=counters.script_frame_count,
            stub_yielded_frame_count=counters.yielded_frame_count,
            stub_unconsumed_frame_count_on_close=(
                counters.unconsumed_frame_count_on_close
            ),
        )
        record = self._stage(
            AR_DETERMINISM,
            "run-record-determinism-audit",
            lambda: build_run_record_v3(observation),
        )
        record_raw = self._stage(
            AR_RECORD,
            "run-record-canonical-serialization",
            lambda: serialize_run_record_v3(record),
        )
        self._stage(
            AR_RECORD,
            "run-record-pending-write-verify",
            lambda: self._storage.write_reserved_record(record_raw, RUN_RECORD_SHA256),
        )
        self._machine.advance("TEMP_RECORD_VERIFIED")

        def publish_record() -> None:
            self._storage.begin_publication("record")
            self.publication_channel.publish_record()
            self._storage.confirm_publication("record")

        self._stage(AR_RECORD, "publish-record-request", publish_record)

        receipt = self._stage(
            AR_RECORD,
            "receipt-v2-construction",
            lambda: build_receipt_v2(self.external_pins, counters),
        )
        self._stage(
            AR_RECORD,
            "receipt-pending-write-verify",
            lambda: self._storage.write_receipt(receipt.raw, receipt.sha256),
        )

        completion = ControllerResult(
            schema_id="S0-PUBLIC-ASSEMBLY-CHILD-COMPLETION-1",
            state="COMPLETE",
            result="candidate-controller-complete-awaiting-live-consumer",
            offline_status="offline-not-success-diagnostic-only",
            rehearsal_pass_authority=(
                "same-process-verifier-live-consumer-2-acceptance-only"
            ),
            rehearsal_pass=False,
            run_record_sha256=RUN_RECORD_SHA256,
            publication_receipt_sha256=receipt.sha256,
            stub_transport_calls=counters.transport_calls,
            stub_close_count=counters.close_count,
        )

        def publish_receipt() -> None:
            self._storage.begin_publication("receipt")
            self.publication_channel.publish_receipt()

        self._stage(AR_RECORD, "publish-receipt-request", publish_receipt)
        # No fallible candidate check or method call follows the second parent OK.
        self._machine._index = len(STATE_ORDER) - 1
        return completion

    def _observed_transport_calls(self) -> int:
        if self._stub is None:
            return 0
        calls = self._stub.transport_calls
        return calls if type(calls) is int and calls >= 0 else 0

    def _failure_diagnostic(self, failure: StageFailure) -> FailureDiagnostic:
        if self._storage is None:
            cleanup_status = "not-required"
            output_root_status = (
                "RESERVATION-REJECTED"
                if failure.failure_class == AR_RESERVE
                else "NOT-RESERVED"
            )
        else:
            cleanup_status, output_root_status = self._storage.cleanup()
        return FailureDiagnostic.create(
            primary_class=failure.failure_class,
            observed_transport_calls=self._observed_transport_calls(),
            failed_operation=failure.operation,
            cause_label=failure.cause_label,
            state_at_failure=self.state,
            cleanup_status=cleanup_status,
            output_root_status=output_root_status,
        )

    def run(self) -> ControllerResult:
        try:
            return self._ordered_run()
        except BoundaryViolation as exc:
            failure = StageFailure(
                AR_BOUNDARY,
                self._current_operation,
                type(exc).__name__,
            )
            raise AssemblyRunFailed(self._failure_diagnostic(failure)) from exc
        except StageFailure as exc:
            raise AssemblyRunFailed(self._failure_diagnostic(exc)) from exc
        except Exception as exc:
            failure = StageFailure(
                self._current_failure_class,
                self._current_operation,
                type(exc).__name__,
            )
            raise AssemblyRunFailed(self._failure_diagnostic(failure)) from exc

from __future__ import annotations

import hashlib
import io
import os
import subprocess
import sys
import tempfile
import textwrap
import unittest
from dataclasses import dataclass, fields, replace
from pathlib import Path
from types import SimpleNamespace
from unittest import mock


HERE = Path(__file__).resolve()
WORKSPACE = next(parent for parent in HERE.parents if (parent / "AGENTS.md").is_file())
IMPLEMENTATION = HERE.parents[1] / "implementation"
sys.path.insert(0, str(IMPLEMENTATION))

import s0_public_assembly_candidate.components as component_module  # noqa: E402
import s0_public_assembly_candidate.controller as controller_module  # noqa: E402
from s0_public_assembly_candidate.canonical import (  # noqa: E402
    StrictJsonError,
    canonical_json_bytes,
    load_strict_json_bytes,
)
from s0_public_assembly_candidate.channel import (  # noqa: E402
    FixedAsciiPipeChannel,
    PublicationChannelError,
)
from s0_public_assembly_candidate.components import (  # noqa: E402
    ComponentApis,
    ComponentError,
    authenticate_component_manifests,
)
from s0_public_assembly_candidate.constants import (  # noqa: E402
    DESIGN_INDEPENDENT_REVIEW_SHA256,
    DESIGN_PACKAGE_MANIFEST_SHA256,
    EXPECTED_RUN_RECORD,
    PACKAGE_PATH,
    PUBLISH_OK,
    PUBLISH_RECEIPT,
    PUBLISH_RECORD,
    PUBLIC_RESPONSE_PATH,
    PUBLIC_RESPONSE_SHA256,
    QUESTIONS_PATH,
    RECEIPT_BYTES,
    RECEIPT_FINAL_NAME,
    RECEIPT_PENDING_NAME,
    REQUEST_BYTES,
    REQUEST_MANIFEST_PATH,
    REQUEST_MANIFEST_SHA256,
    REQUEST_PATH,
    REQUEST_PURPOSE,
    REQUEST_SHA256,
    RUN_RECORD_BYTES,
    RUN_RECORD_FINAL_NAME,
    RUN_RECORD_PENDING_NAME,
    RUN_RECORD_SHA256,
    STATE_ORDER,
    STUB_RESPONSE_ID,
)
from s0_public_assembly_candidate.controller import (  # noqa: E402
    AssemblyController,
    _StateMachine,
)
from s0_public_assembly_candidate.errors import (  # noqa: E402
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
)
from s0_public_assembly_candidate.records import (  # noqa: E402
    DeterminismError,
    ExternalPins,
    PinError,
    RecordEncodingError,
    RunObservation,
    audit_run_record_v3,
    build_receipt_v2,
    build_run_record_v3,
    serialize_run_record_v3,
    validate_external_pins,
)
from s0_public_assembly_candidate.request import (  # noqa: E402
    RequestError,
    reconstruct_request,
    require_materialized_request,
)
from s0_public_assembly_candidate.runtime_guard import (  # noqa: E402
    _audit,
    _is_forbidden,
)
from s0_public_assembly_candidate.storage import StorageError  # noqa: E402
from s0_public_assembly_candidate.stub import (  # noqa: E402
    ExactAnswerStub,
    StubCounters,
    StubIntegrityError,
)


IMPLEMENTATION_PIN = "a" * 64


def exact_pins() -> ExternalPins:
    return ExternalPins(
        assembly_implementation_manifest_sha256=IMPLEMENTATION_PIN,
        design_package_manifest_sha256=DESIGN_PACKAGE_MANIFEST_SHA256,
        design_independent_review_sha256=DESIGN_INDEPENDENT_REVIEW_SHA256,
    )


def exact_observation() -> RunObservation:
    return RunObservation(
        actual_response_sha256=PUBLIC_RESPONSE_SHA256,
        answer_validation_error_count=0,
        denied_input_access_count=0,
        retry_count=0,
        response_frames=1,
        final_frames=1,
        transport_calls=1,
        stub_script_frame_count=1,
        stub_yielded_frame_count=1,
        stub_unconsumed_frame_count_on_close=0,
    )


def exact_counters() -> StubCounters:
    return StubCounters(
        transport_calls=1,
        script_frame_count=1,
        yielded_frame_count=1,
        close_count=1,
        unconsumed_frame_count_on_close=0,
        yielded_final_frame_count=1,
    )


@dataclass(frozen=True)
class _Frame:
    response_id: str
    data: bytes
    final: bool


@dataclass(frozen=True)
class _AuthenticatedRequest:
    raw: bytes
    sha256: str


@dataclass(frozen=True)
class _OneShotResult:
    raw_response: bytes


def _policy() -> SimpleNamespace:
    return SimpleNamespace(
        invocation_limit=1,
        retry_limit=0,
        tool_count=0,
        state_mode="none",
        response_selection="first-final-only",
        max_response_bytes=8192,
        max_response_frames=256,
        empty_frame_mode="reject",
    )


class CanonicalRequestRecordTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.package_raw = (WORKSPACE / PACKAGE_PATH).read_bytes()
        cls.questions_raw = (WORKSPACE / QUESTIONS_PATH).read_bytes()
        cls.request_raw = (WORKSPACE / REQUEST_PATH).read_bytes()

    def test_strict_json_rejects_duplicate_bom_nonfinite_and_nonobject(self) -> None:
        bad_values = (
            b'{"a":1,"a":2}\n',
            b"\xef\xbb\xbf{}\n",
            b'{"value":NaN}\n',
            b"\xff",
        )
        for raw in bad_values:
            with self.subTest(raw=raw):
                with self.assertRaises(StrictJsonError):
                    load_strict_json_bytes(raw, require_object=True)
        with self.assertRaises(StrictJsonError):
            load_strict_json_bytes(b"[]\n", require_object=True)
        with self.assertRaises(StrictJsonError):
            load_strict_json_bytes(bytearray(b"{}\n"))  # type: ignore[arg-type]

    def test_canonical_encoding_is_ascii_sorted_compact_and_final_lf(self) -> None:
        self.assertEqual(
            canonical_json_bytes({"z": "\uc548", "a": 1}),
            b'{"a":1,"z":"\\uc548"}\n',
        )
        with self.assertRaises(StrictJsonError):
            canonical_json_bytes({"value": float("nan")})

    def test_exact_request_reconstruction_and_materialized_binding(self) -> None:
        reconstructed = reconstruct_request(self.package_raw, self.questions_raw)
        self.assertEqual(len(reconstructed.value), 8)
        self.assertEqual(len(reconstructed.raw), REQUEST_BYTES)
        self.assertEqual(reconstructed.sha256, REQUEST_SHA256)
        self.assertEqual(reconstructed.raw, self.request_raw)
        require_materialized_request(reconstructed, self.request_raw)

    def test_request_input_and_materialized_byte_mutations_reject(self) -> None:
        for package, questions in (
            (self.package_raw + b" ", self.questions_raw),
            (self.package_raw, self.questions_raw + b" "),
        ):
            with self.subTest(package_bytes=len(package), question_bytes=len(questions)):
                with self.assertRaises(RequestError):
                    reconstruct_request(package, questions)
        reconstructed = reconstruct_request(self.package_raw, self.questions_raw)
        mutation = bytearray(self.request_raw)
        mutation[len(mutation) // 2] ^= 1
        with self.assertRaises(RequestError):
            require_materialized_request(reconstructed, bytes(mutation))
        with self.assertRaises(RequestError):
            require_materialized_request(reconstructed, bytearray(self.request_raw))  # type: ignore[arg-type]

    def test_exact_run_record_and_every_semantic_field_mutation(self) -> None:
        record = build_run_record_v3(exact_observation())
        raw = serialize_run_record_v3(record)
        self.assertEqual(record, dict(EXPECTED_RUN_RECORD))
        self.assertEqual(len(record), 38)
        self.assertEqual(len(raw), RUN_RECORD_BYTES)
        self.assertEqual(hashlib.sha256(raw).hexdigest(), RUN_RECORD_SHA256)
        for key, value in tuple(record.items()):
            changed = dict(record)
            changed[key] = value + 1 if type(value) is int else str(value) + "-mutated"
            with self.subTest(field=key):
                with self.assertRaises(DeterminismError):
                    audit_run_record_v3(changed)

    def test_every_run_observation_mutation_rejects(self) -> None:
        baseline = exact_observation()
        for field in fields(baseline):
            value = getattr(baseline, field.name)
            changed = value + 1 if type(value) is int else value + "-mutated"
            with self.subTest(field=field.name):
                with self.assertRaises(DeterminismError):
                    build_run_record_v3(replace(baseline, **{field.name: changed}))

    def test_exact_receipt_and_pin_counter_mutations(self) -> None:
        receipt = build_receipt_v2(exact_pins(), exact_counters())
        self.assertEqual(len(receipt.value), 21)
        self.assertEqual(len(receipt.raw), RECEIPT_BYTES)
        self.assertEqual(hashlib.sha256(receipt.raw).hexdigest(), receipt.sha256)
        self.assertEqual(
            load_strict_json_bytes(receipt.raw)["offline_status"],
            "offline-not-success-diagnostic-only",
        )

        invalid_pin_sets = (
            replace(exact_pins(), assembly_implementation_manifest_sha256="0" * 64),
            replace(exact_pins(), assembly_implementation_manifest_sha256="A" * 64),
            replace(exact_pins(), design_package_manifest_sha256="b" * 64),
            replace(exact_pins(), design_independent_review_sha256="b" * 64),
        )
        for pins in invalid_pin_sets:
            with self.subTest(pins=pins):
                with self.assertRaises(PinError):
                    validate_external_pins(pins)
        with self.assertRaises(PinError):
            validate_external_pins(object())  # type: ignore[arg-type]

        counters = exact_counters()
        for name in (
            "transport_calls",
            "script_frame_count",
            "yielded_frame_count",
            "close_count",
            "unconsumed_frame_count_on_close",
        ):
            with self.subTest(counter=name):
                with self.assertRaises(RecordEncodingError):
                    build_receipt_v2(exact_pins(), replace(counters, **{name: 2}))
        with self.assertRaises(RecordEncodingError):
            build_receipt_v2(
                exact_pins(),
                replace(counters, transport_calls=True),
            )
        with self.assertRaises(RecordEncodingError):
            build_receipt_v2(
                exact_pins(),
                replace(counters, transport_calls=True),
            )


class StubAndChannelTests(unittest.TestCase):
    def test_stub_exact_one_frame_one_use_and_counters(self) -> None:
        stub = ExactAnswerStub(
            expected_request_raw=b"request",
            response_raw=b"response",
            response_frame_type=_Frame,
        )
        iterator = stub.invoke_once(b"request", policy=_policy())
        frame = next(iterator)
        self.assertEqual(
            (frame.response_id, frame.data, frame.final),
            (STUB_RESPONSE_ID, b"response", True),
        )
        with self.assertRaises(StopIteration):
            next(iterator)
        iterator.close()
        self.assertEqual(stub.require_integrity(), exact_counters())
        with self.assertRaises(StubIntegrityError):
            stub.invoke_once(b"request", policy=_policy())
        self.assertEqual(stub.transport_calls, 1)
        self.assertEqual(stub.snapshot().five_counter_dict()["transport_calls"], 1)

    def test_stub_wrong_request_policy_early_close_and_double_close_reject(self) -> None:
        wrong_request = ExactAnswerStub(
            expected_request_raw=b"request",
            response_raw=b"response",
            response_frame_type=_Frame,
        )
        with self.assertRaises(StubIntegrityError):
            wrong_request.invoke_once(b"mutated", policy=_policy())

        for name in vars(_policy()):
            policy = _policy()
            setattr(policy, name, object())
            stub = ExactAnswerStub(
                expected_request_raw=b"request",
                response_raw=b"response",
                response_frame_type=_Frame,
            )
            with self.subTest(policy_field=name):
                with self.assertRaises(StubIntegrityError):
                    stub.invoke_once(b"request", policy=policy)

        early = ExactAnswerStub(
            expected_request_raw=b"request",
            response_raw=b"response",
            response_frame_type=_Frame,
        )
        iterator = early.invoke_once(b"request", policy=_policy())
        with self.assertRaises(StubIntegrityError):
            iterator.close()
        with self.assertRaises(StubIntegrityError):
            iterator.close()
        with self.assertRaises(StubIntegrityError):
            early.require_integrity()

    def test_fixed_ascii_channel_exact_order_and_negative_frames(self) -> None:
        writer = io.BytesIO()
        channel = FixedAsciiPipeChannel(writer, io.BytesIO(PUBLISH_OK + PUBLISH_OK))
        channel.publish_record()
        channel.publish_receipt()
        self.assertEqual(channel.state, 2)
        self.assertEqual(writer.getvalue(), PUBLISH_RECORD + PUBLISH_RECEIPT)
        with self.assertRaises(PublicationChannelError):
            channel.publish_receipt()

        with self.assertRaises(PublicationChannelError):
            FixedAsciiPipeChannel(io.BytesIO(), io.BytesIO(PUBLISH_OK)).publish_receipt()
        for reply in (b"", b"O", b"NO\n", b"OK\r"):
            with self.subTest(reply=reply):
                with self.assertRaises(PublicationChannelError):
                    FixedAsciiPipeChannel(io.BytesIO(), io.BytesIO(reply)).publish_record()


class ComponentManifestTests(unittest.TestCase):
    def test_current_public_component_manifests_required_api_rows_authenticate(self) -> None:
        self.assertIsNone(authenticate_component_manifests(WORKSPACE))

    def _synthetic_i0(self, root: Path, manifest_raw: bytes, source_raw: bytes) -> dict[str, tuple[str, str]]:
        source = root / "s0-lab" / "i0" / "implementation" / "source.py"
        manifest = root / "s0-lab" / "i0" / "verification" / "implementation-files.sha256"
        source.parent.mkdir(parents=True)
        manifest.parent.mkdir(parents=True)
        source.write_bytes(source_raw)
        manifest.write_bytes(manifest_raw)
        relative = "s0-lab/i0/verification/implementation-files.sha256"
        return {"i0": (relative, hashlib.sha256(manifest_raw).hexdigest())}

    def test_component_manifest_row_mutation_duplicate_and_noncanonical_reject(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_raw = b"value = 1\n"
            row_hash = hashlib.sha256(source_raw).hexdigest()
            row = f"{row_hash}  implementation/source.py\n".encode("ascii")
            mapping = self._synthetic_i0(root, row, source_raw)
            with mock.patch.object(component_module, "COMPONENT_MANIFESTS", mapping):
                with mock.patch.object(
                    component_module,
                    "_REQUIRED_COMPONENT_SOURCE_ROWS",
                    {"i0": ("implementation/source.py",)},
                ):
                    authenticate_component_manifests(root)
                    (root / "s0-lab" / "i0" / "implementation" / "source.py").write_bytes(
                        b"value = 2\n"
                    )
                    with self.assertRaises(StorageError):
                        authenticate_component_manifests(root)

        for label, manifest_raw in (
            ("duplicate", row + row),
            ("crlf", row.replace(b"\n", b"\r\n")),
            ("bad-row", b"not-a-manifest-row\n"),
        ):
            with self.subTest(label=label), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                mapping = self._synthetic_i0(root, manifest_raw, source_raw)
                with mock.patch.object(component_module, "COMPONENT_MANIFESTS", mapping):
                    with mock.patch.object(
                        component_module,
                        "_REQUIRED_COMPONENT_SOURCE_ROWS",
                        {"i0": ("implementation/source.py",)},
                    ):
                        with self.assertRaises(ComponentError):
                            authenticate_component_manifests(root)

    def test_component_manifest_ignores_nonrequired_rows_but_requires_closure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            required_raw = b"required = 1\n"
            ignored_raw = b"ignored = 1\n"
            manifest = (
                f"{hashlib.sha256(required_raw).hexdigest()}  implementation/required.py\n"
                f"{hashlib.sha256(ignored_raw).hexdigest()}  implementation/ignored.py\n"
            ).encode("ascii")
            mapping = self._synthetic_i0(root, manifest, required_raw)
            implementation = root / "s0-lab" / "i0" / "implementation"
            (implementation / "source.py").rename(implementation / "required.py")
            (implementation / "ignored.py").write_bytes(b"mutated and deliberately unread\n")
            with mock.patch.object(component_module, "COMPONENT_MANIFESTS", mapping), mock.patch.object(
                component_module,
                "_REQUIRED_COMPONENT_SOURCE_ROWS",
                {"i0": ("implementation/required.py",)},
            ):
                authenticate_component_manifests(root)
                with mock.patch.object(
                    component_module,
                    "_REQUIRED_COMPONENT_SOURCE_ROWS",
                    {"i0": ("implementation/missing.py",)},
                ):
                    with self.assertRaises(ComponentError):
                        authenticate_component_manifests(root)

    def test_boundary_violation_from_component_import_is_not_wrapped(self) -> None:
        roots = [WORKSPACE / "s0-lab" / name / "implementation" for name in ("i0", "i1", "i2", "i3")]
        with mock.patch.object(component_module, "authenticate_component_manifests"), mock.patch.object(
            component_module, "workspace_path", side_effect=roots
        ), mock.patch.object(
            component_module.importlib,
            "import_module",
            side_effect=BoundaryViolation("denied import"),
        ):
            with self.assertRaises(BoundaryViolation):
                component_module.load_component_apis(WORKSPACE)


class RuntimeSentinelTests(unittest.TestCase):
    def test_forbidden_name_and_audit_event_matrix(self) -> None:
        for name in (
            "ctypes",
            "ctypes.wintypes",
            "socket",
            "subprocess",
            "openai",
            "urllib.request",
            "google.generativeai.client",
            "s0_public_assembly_verifier",
        ):
            with self.subTest(name=name):
                self.assertTrue(_is_forbidden(name))
        for name in ("json", "hashlib", "s0_i0", "urllib.parse"):
            with self.subTest(name=name):
                self.assertFalse(_is_forbidden(name))
        for event in (
            "os.rename",
            "socket.connect",
            "subprocess.Popen",
            "ctypes.dlopen",
            "os.system",
            "os.exec",
            "os.spawn",
        ):
            with self.subTest(event=event):
                with self.assertRaises(BoundaryViolation):
                    _audit(event, ())
        with self.assertRaises(BoundaryViolation):
            _audit("open", ())

    def test_installed_sentinel_blocks_import_rename_and_preloaded_ffi(self) -> None:
        implementation = repr(str(IMPLEMENTATION))
        blocked_script = textwrap.dedent(
            f"""
            import os
            import sys
            sys.path.insert(0, {implementation})
            from s0_public_assembly_candidate.errors import BoundaryViolation
            from s0_public_assembly_candidate.runtime_guard import install_runtime_sentinels
            install_runtime_sentinels()
            outcomes = []
            try:
                __import__('ctypes')
            except BoundaryViolation:
                outcomes.append('import')
            try:
                os.rename('definitely-absent-source', 'definitely-absent-target')
            except BoundaryViolation:
                outcomes.append('rename')
            print(','.join(outcomes))
            """
        )
        completed = subprocess.run(
            [sys.executable, "-S", "-c", blocked_script],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout.strip(), "import,rename")

        preloaded_script = textwrap.dedent(
            f"""
            import ctypes
            import sys
            sys.path.insert(0, {implementation})
            from s0_public_assembly_candidate.errors import BoundaryViolation
            from s0_public_assembly_candidate.runtime_guard import install_runtime_sentinels
            try:
                install_runtime_sentinels()
            except BoundaryViolation:
                print('preloaded-denied')
            """
        )
        completed = subprocess.run(
            [sys.executable, "-S", "-c", preloaded_script],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(completed.stdout.strip(), "preloaded-denied")


class _DiagnosticRenameChannel:
    """Test-only rename channel. It is never live-consumer or PASS authority."""

    def __init__(
        self,
        root: Path,
        *,
        fail_record_before_move: bool = False,
        fail_receipt_after_move: bool = False,
    ) -> None:
        self.root = root
        self.fail_record_before_move = fail_record_before_move
        self.fail_receipt_after_move = fail_receipt_after_move
        self.calls: list[str] = []

    def publish_record(self) -> None:
        self.calls.append("record")
        if self.fail_record_before_move:
            raise RuntimeError("diagnostic record publication failure")
        os.rename(self.root / RUN_RECORD_PENDING_NAME, self.root / RUN_RECORD_FINAL_NAME)

    def publish_receipt(self) -> None:
        self.calls.append("receipt")
        os.rename(self.root / RECEIPT_PENDING_NAME, self.root / RECEIPT_FINAL_NAME)
        if self.fail_receipt_after_move:
            raise RuntimeError("diagnostic uncertain receipt publication")


class ControllerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.package_raw = (WORKSPACE / PACKAGE_PATH).read_bytes()
        cls.request_raw = (WORKSPACE / REQUEST_PATH).read_bytes()
        cls.response_raw = (WORKSPACE / PUBLIC_RESPONSE_PATH).read_bytes()

    def _components(
        self,
        *,
        transform_raw: bytes | None = None,
        run_mode: str = "ok",
        validation_errors: list[object] | None = None,
        boundary_preflight: bool = False,
    ) -> ComponentApis:
        package_raw = self.package_raw if transform_raw is None else transform_raw
        request_raw = self.request_raw
        response_raw = self.response_raw

        def verify_bundle(_root: Path) -> dict[str, int]:
            if boundary_preflight:
                raise BoundaryViolation("diagnostic denied preflight")
            return {"manifest_entries": 90}

        def bind(**kwargs: object) -> object:
            self.assertEqual(kwargs["expected_manifest_path"], REQUEST_MANIFEST_PATH)
            self.assertEqual(kwargs["expected_manifest_sha256"], REQUEST_MANIFEST_SHA256)
            self.assertEqual(kwargs["expected_allowed_paths"], (REQUEST_PATH,))
            self.assertEqual(kwargs["purpose"], REQUEST_PURPOSE)
            return object()

        def authenticate(_root: Path, _manifest: object, path: str, *, max_bytes: int) -> _AuthenticatedRequest:
            self.assertEqual(path, REQUEST_PATH)
            self.assertEqual(max_bytes, REQUEST_BYTES)
            return _AuthenticatedRequest(request_raw, REQUEST_SHA256)

        def run_one_shot(
            _rehearsal_id: str,
            authenticated_request: _AuthenticatedRequest,
            transport: ExactAnswerStub,
            **_kwargs: object,
        ) -> _OneShotResult:
            if run_mode == "raise":
                raise RuntimeError("diagnostic invocation failure")
            stream = transport.invoke_once(authenticated_request.raw, policy=_policy())
            frame = next(stream)
            with self.assertRaises(StopIteration):
                next(stream)
            stream.close()
            selected = frame.data if run_mode == "ok" else frame.data + b" "
            return _OneShotResult(selected)

        return ComponentApis(
            i0_verify_public_bundle=verify_bundle,
            i0_transform_canonical=lambda _value, _representation: package_raw,
            i0_validate_answer_candidate_bytes=(
                lambda _root, _raw, **_kwargs: []
                if validation_errors is None
                else validation_errors
            ),
            i1_bind_external_manifest_grant=bind,
            i1_load_authenticated_manifest=lambda _root, _grant: object(),
            i1_authenticate_manifest_entry=authenticate,
            i1_run_one_shot=run_one_shot,
            i1_response_frame_type=_Frame,
            i2_verify_contract_file=lambda _path: None,
            i3_verify_contract_file=lambda _path: None,
        )

    def _run(
        self,
        root: Path,
        *,
        components: ComponentApis | None = None,
        channel: _DiagnosticRenameChannel | None = None,
        pins: ExternalPins | None = None,
    ):
        controller = AssemblyController(
            workspace_root=WORKSPACE,
            output_root=root,
            external_pins=exact_pins() if pins is None else pins,
            publication_channel=(
                _DiagnosticRenameChannel(root) if channel is None else channel
            ),  # type: ignore[arg-type]
            components=self._components() if components is None else components,
        )
        with mock.patch.object(
            controller_module,
            "authenticate_component_manifests",
            return_value=None,
        ):
            return controller, controller.run()

    def test_state_machine_allows_only_the_frozen_ten_state_order(self) -> None:
        machine = _StateMachine()
        self.assertEqual(machine.state, STATE_ORDER[0])
        with self.assertRaises(RuntimeError):
            machine.advance(STATE_ORDER[2])
        for state in STATE_ORDER[1:]:
            machine.advance(state)
            self.assertEqual(machine.state, state)
        with self.assertRaises(RuntimeError):
            machine.advance("COMPLETE")

    def test_fake_component_end_to_end_is_diagnostic_only_and_exact(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            channel = _DiagnosticRenameChannel(root)
            controller, result = self._run(root, channel=channel)
            self.assertEqual(controller.state, "COMPLETE")
            self.assertEqual(channel.calls, ["record", "receipt"])
            self.assertFalse(result.rehearsal_pass)
            self.assertEqual(result.offline_status, "offline-not-success-diagnostic-only")
            self.assertEqual(result.run_record_sha256, RUN_RECORD_SHA256)
            self.assertEqual(
                hashlib.sha256((root / RUN_RECORD_FINAL_NAME).read_bytes()).hexdigest(),
                RUN_RECORD_SHA256,
            )
            receipt_raw = (root / RECEIPT_FINAL_NAME).read_bytes()
            self.assertEqual(len(receipt_raw), RECEIPT_BYTES)
            self.assertEqual(
                load_strict_json_bytes(receipt_raw)[
                    "assembly_implementation_manifest_sha256"
                ],
                IMPLEMENTATION_PIN,
            )
            self.assertFalse((root / RUN_RECORD_PENDING_NAME).exists())
            self.assertFalse((root / RECEIPT_PENDING_NAME).exists())

    def _expect_failure(
        self,
        root: Path,
        expected_class: str,
        *,
        components: ComponentApis | None = None,
        channel: _DiagnosticRenameChannel | None = None,
        pins: ExternalPins | None = None,
        patch_target: str | None = None,
    ):
        context = (
            mock.patch.object(
                controller_module,
                patch_target,
                side_effect=RuntimeError("diagnostic injected failure"),
            )
            if patch_target is not None
            else mock.patch.object(controller_module, "__name__", controller_module.__name__)
        )
        with context:
            with self.assertRaises(AssemblyRunFailed) as caught:
                self._run(
                    root,
                    components=components,
                    channel=channel,
                    pins=pins,
                )
        diagnostic = caught.exception.diagnostic
        self.assertEqual(diagnostic.primary_class, expected_class)
        self.assertFalse(diagnostic.rehearsal_pass)
        self.assertEqual(diagnostic.offline_status, "offline-not-success-diagnostic-only")
        return diagnostic

    def test_failure_routing_before_reservation(self) -> None:
        cases = (
            (
                AR_AUTH,
                self._components(),
                replace(exact_pins(), design_package_manifest_sha256="b" * 64),
            ),
            (AR_BOUNDARY, self._components(boundary_preflight=True), exact_pins()),
            (AR_TRANSFORM, self._components(transform_raw=b"wrong"), exact_pins()),
        )
        for expected, components, pins in cases:
            with self.subTest(expected=expected), tempfile.TemporaryDirectory() as temporary:
                diagnostic = self._expect_failure(
                    Path(temporary),
                    expected,
                    components=components,
                    pins=pins,
                )
                self.assertEqual(diagnostic.observed_transport_calls, 0)
                self.assertEqual(diagnostic.cleanup_status, "not-required")
                self.assertEqual(diagnostic.output_root_status, "NOT-RESERVED")

    def test_reserve_invoke_response_and_answer_failure_routes_cleanup(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "foreign.txt").write_bytes(b"foreign")
            diagnostic = self._expect_failure(root, AR_RESERVE)
            self.assertEqual(diagnostic.observed_transport_calls, 0)
            self.assertEqual(diagnostic.output_root_status, "RESERVATION-REJECTED")
            self.assertEqual((root / "foreign.txt").read_bytes(), b"foreign")

        cases = (
            (AR_INVOKE, self._components(run_mode="raise"), 0),
            (AR_RESPONSE, self._components(run_mode="mutated"), 1),
            (AR_ANSWER, self._components(validation_errors=["error"]), 1),
        )
        for expected, components, calls in cases:
            with self.subTest(expected=expected), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                diagnostic = self._expect_failure(root, expected, components=components)
                self.assertEqual(diagnostic.observed_transport_calls, calls)
                self.assertEqual(diagnostic.cleanup_status, "complete")
                self.assertEqual(diagnostic.output_root_status, "CLEANED-FAILED")
                self.assertEqual(tuple(root.iterdir()), ())

    def test_determinism_record_and_publication_failure_routes(self) -> None:
        for expected, target in (
            (AR_DETERMINISM, "build_run_record_v3"),
            (AR_RECORD, "serialize_run_record_v3"),
        ):
            with self.subTest(expected=expected), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                diagnostic = self._expect_failure(root, expected, patch_target=target)
                self.assertEqual(diagnostic.observed_transport_calls, 1)
                self.assertEqual(diagnostic.cleanup_status, "complete")
                self.assertEqual(tuple(root.iterdir()), ())

        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            channel = _DiagnosticRenameChannel(root, fail_record_before_move=True)
            diagnostic = self._expect_failure(root, AR_RECORD, channel=channel)
            self.assertEqual(channel.calls, ["record"])
            self.assertEqual(diagnostic.cleanup_status, "complete")
            self.assertEqual(tuple(root.iterdir()), ())

    def test_uncertain_second_publication_is_quarantined_and_never_success(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            channel = _DiagnosticRenameChannel(root, fail_receipt_after_move=True)
            diagnostic = self._expect_failure(root, AR_RECORD, channel=channel)
            self.assertEqual(channel.calls, ["record", "receipt"])
            self.assertEqual(diagnostic.observed_transport_calls, 1)
            self.assertEqual(diagnostic.cleanup_status, "failed")
            self.assertEqual(diagnostic.output_root_status, "QUARANTINED-FAILED")
            self.assertFalse((root / RUN_RECORD_FINAL_NAME).exists())
            self.assertTrue((root / RECEIPT_FINAL_NAME).exists())


if __name__ == "__main__":
    unittest.main()

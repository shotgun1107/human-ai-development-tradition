from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


WORKSPACE = Path(__file__).resolve().parents[3]
IMPLEMENTATION = WORKSPACE / "s0-lab" / "i1" / "implementation"
sys.path.insert(0, str(IMPLEMENTATION))

from s0_i1.auth import (  # noqa: E402
    AuthenticatedBytes,
    authenticate_manifest_entry,
    bind_external_manifest_grant,
    load_authenticated_manifest,
    sha256_bytes,
)
from s0_i1.errors import JsonBytesError, OutputError, RunnerPolicyError  # noqa: E402
from s0_i1.runner import (  # noqa: E402
    MAX_RESPONSE_BYTES,
    MAX_RESPONSE_FRAMES,
    ONE_SHOT_POLICY,
    ResponseFrame,
    run_one_shot,
    run_one_shot_to_new_file,
)


def request(
    raw: bytes = b"non-semantic-public-request", *, purpose: str = "one-shot-request"
) -> tuple[AuthenticatedBytes, object, dict[str, object]]:
    with tempfile.TemporaryDirectory(
        dir=WORKSPACE / "s0-lab" / "i1" / "tests"
    ) as temporary:
        root = Path(temporary)
        input_path = root / "inputs" / "request.bin"
        input_path.parent.mkdir(parents=True)
        input_path.write_bytes(raw)
        manifest_raw = f"{sha256_bytes(raw)}  inputs/request.bin\n".encode("ascii")
        manifest_path = root / "inputs" / "files.sha256"
        manifest_path.write_bytes(manifest_raw)
        grant = bind_external_manifest_grant(
            expected_manifest_path="inputs/files.sha256",
            expected_manifest_sha256=sha256_bytes(manifest_raw),
            expected_entry_prefix="inputs/",
            expected_allowed_paths=("inputs/request.bin",),
            purpose=purpose,
        )
        manifest = load_authenticated_manifest(root, grant)
        authenticated = authenticate_manifest_entry(
            root, manifest, "inputs/request.bin"
        )
        kwargs = {
            "required_grant": grant,
            "expected_authority_sha256": grant.manifest_sha256,
            "expected_authority_path": grant.manifest_path,
            "expected_request_path": "inputs/request.bin",
            "expected_purpose": purpose,
        }
        return authenticated, grant, kwargs


class FakeTransport:
    def __init__(self, frames=None, error=None):
        self.frames = frames
        self.error = error
        self.calls = 0
        self.policies = []

    def invoke_once(self, request_bytes, *, policy):
        self.calls += 1
        self.policies.append(policy)
        if self.error is not None:
            raise self.error
        return iter(self.frames)


class RunnerTests(unittest.TestCase):
    def _run(self, run_id: str, transport: FakeTransport, authenticated=None):
        if authenticated is None:
            value, _grant, kwargs = request()
        else:
            value, _grant, kwargs = authenticated
        return run_one_shot(run_id, value, transport, **kwargs)

    def test_policy_is_exactly_one_call_zero_retry_tools_state_and_bounded_frames(self):
        transport = FakeTransport([ResponseFrame("first", b'{"ok":true}', True)])
        result = self._run("RUN.PUBLIC.1", transport)
        self.assertEqual(transport.calls, 1)
        self.assertEqual(transport.policies, [ONE_SHOT_POLICY])
        self.assertEqual(ONE_SHOT_POLICY.invocation_limit, 1)
        self.assertEqual(ONE_SHOT_POLICY.retry_limit, 0)
        self.assertEqual(ONE_SHOT_POLICY.tool_count, 0)
        self.assertEqual(ONE_SHOT_POLICY.state_mode, "none")
        self.assertEqual(ONE_SHOT_POLICY.response_selection, "first-final-only")
        self.assertEqual(ONE_SHOT_POLICY.max_response_frames, 256)
        self.assertEqual(ONE_SHOT_POLICY.empty_frame_mode, "reject")
        self.assertEqual(result.parsed_response, {"ok": True})

    def test_transport_failure_is_not_retried(self):
        transport = FakeTransport(error=RuntimeError("sentinel transport failure"))
        with self.assertRaisesRegex(RuntimeError, "sentinel"):
            self._run("RUN.PUBLIC.2", transport)
        self.assertEqual(transport.calls, 1)

    def test_authority_path_purpose_and_exact_grant_identity_reject_before_transport(self):
        authenticated = request()
        value, _grant, kwargs = authenticated
        transport = FakeTransport([ResponseFrame("first", b"{}", True)])
        attacks = (
            {**kwargs, "expected_authority_sha256": "0" * 64},
            {**kwargs, "expected_authority_path": "other/files.sha256"},
            {**kwargs, "expected_request_path": "inputs/other.bin"},
            {**kwargs, "expected_purpose": "other-purpose"},
        )
        for index, attack in enumerate(attacks):
            with self.subTest(index=index):
                with self.assertRaises(RunnerPolicyError):
                    run_one_shot("RUN.AUTH", value, transport, **attack)
        self.assertEqual(transport.calls, 0)

        other_value, _other_grant, other_kwargs = request(purpose="other-purpose")
        with self.assertRaisesRegex(RunnerPolicyError, "authority"):
            run_one_shot("RUN.AUTH.OTHER", other_value, transport, **kwargs)
        self.assertEqual(transport.calls, 0)

        # Even an equivalent, separately minted object is not the caller-held
        # capability that authenticated this request.
        original_grant = kwargs["required_grant"]
        equivalent_grant = bind_external_manifest_grant(
            expected_manifest_path=original_grant.manifest_path,
            expected_manifest_sha256=original_grant.manifest_sha256,
            expected_entry_prefix=original_grant.entry_prefix,
            expected_allowed_paths=original_grant.allowed_paths,
            purpose=original_grant.purpose,
        )
        equivalent_kwargs = {**kwargs, "required_grant": equivalent_grant}
        with self.assertRaisesRegex(RunnerPolicyError, "authority"):
            run_one_shot(
                "RUN.AUTH.EQUIVALENT", value, transport, **equivalent_kwargs
            )
        self.assertEqual(transport.calls, 0)

    def test_plain_forged_object_and_tampered_authenticated_bytes_reject(self):
        _value, _grant, kwargs = request()
        transport = FakeTransport([ResponseFrame("first", b"{}", True)])
        forged = SimpleNamespace(
            relative_path="inputs/request.bin",
            sha256=sha256_bytes(b"request"),
            raw=b"request",
            authority_sha256=kwargs["expected_authority_sha256"],
        )
        with self.assertRaises(RunnerPolicyError):
            run_one_shot("RUN.FORGED", forged, transport, **kwargs)

        inconsistent = object.__new__(AuthenticatedBytes)
        object.__setattr__(inconsistent, "relative_path", "inputs/request.bin")
        object.__setattr__(inconsistent, "sha256", sha256_bytes(b"request"))
        object.__setattr__(inconsistent, "raw", b"changed")
        with self.assertRaises(RunnerPolicyError):
            run_one_shot("RUN.TAMPERED", inconsistent, transport, **kwargs)
        self.assertEqual(transport.calls, 0)

    def test_8192_ceiling_is_checked_before_decode_or_parse(self):
        transport = FakeTransport(
            [ResponseFrame("first", b"x" * (MAX_RESPONSE_BYTES + 1), True)]
        )
        with patch("s0_i1.runner.parse_strict_json_bytes") as parser:
            with self.assertRaisesRegex(RunnerPolicyError, "8192"):
                self._run("RUN.PUBLIC.3", transport)
        parser.assert_not_called()

    def test_exact_8192_bytes_reach_parse(self):
        raw = b" " * (MAX_RESPONSE_BYTES - 2) + b"{}"
        result = self._run(
            "RUN.PUBLIC.4", FakeTransport([ResponseFrame("first", raw, True)])
        )
        self.assertEqual(len(result.raw_response), MAX_RESPONSE_BYTES)
        self.assertEqual(result.parsed_response, {})

    def test_first_final_stops_before_later_response(self):
        state = {"later_yielded": False}

        def frames():
            yield ResponseFrame("first", b'{"first":true}', True)
            state["later_yielded"] = True
            yield ResponseFrame("second", b'{"second":true}', True)

        result = self._run("RUN.PUBLIC.5", FakeTransport(frames()))
        self.assertEqual(result.parsed_response, {"first": True})
        self.assertFalse(state["later_yielded"])

    def test_empty_excessive_and_nonexact_frames_reject(self):
        with self.assertRaises(RunnerPolicyError):
            ResponseFrame("first", b"", False)
        with self.assertRaises(RunnerPolicyError):
            ResponseFrame("first", b"{}", 1)

        forged_empty = object.__new__(ResponseFrame)
        object.__setattr__(forged_empty, "response_id", "first")
        object.__setattr__(forged_empty, "data", b"")
        object.__setattr__(forged_empty, "final", False)
        with self.assertRaisesRegex(RunnerPolicyError, "empty"):
            self._run("RUN.EMPTY", FakeTransport([forged_empty]))

        frames = [ResponseFrame("first", b" ", False)] * MAX_RESPONSE_FRAMES
        frames.append(ResponseFrame("first", b"{}", True))
        with self.assertRaisesRegex(RunnerPolicyError, "256-frame"):
            self._run("RUN.FRAMES", FakeTransport(frames))

    def test_mixed_response_ids_before_final_reject(self):
        transport = FakeTransport(
            [
                ResponseFrame("first", b"{", False),
                ResponseFrame("second", b"}", True),
            ]
        )
        with self.assertRaisesRegex(RunnerPolicyError, "later response"):
            self._run("RUN.PUBLIC.6", transport)

    def test_cleanup_failure_semantics_are_deterministic(self):
        class CloseFailure:
            def __init__(self, values):
                self.values = iter(values)

            def __iter__(self):
                return self

            def __next__(self):
                return next(self.values)

            def close(self):
                raise RuntimeError("cleanup sentinel")

        with self.assertRaisesRegex(RunnerPolicyError, "cleanup"):
            self._run(
                "RUN.CLEANUP.SUCCESS",
                FakeTransport(CloseFailure([ResponseFrame("first", b"{}", True)])),
            )

        with self.assertRaisesRegex(RunnerPolicyError, "later response"):
            self._run(
                "RUN.CLEANUP.PRIMARY",
                FakeTransport(
                    CloseFailure(
                        [
                            ResponseFrame("first", b"{", False),
                            ResponseFrame("second", b"}", True),
                        ]
                    )
                ),
            )

        class CloseLookupFailure:
            def __init__(self):
                self.done = False

            def __iter__(self):
                return self

            def __next__(self):
                if self.done:
                    raise StopIteration
                self.done = True
                return ResponseFrame("first", b"{}", True)

            @property
            def close(self):
                raise RuntimeError("close lookup sentinel")

        with self.assertRaisesRegex(RunnerPolicyError, "lookup"):
            self._run(
                "RUN.CLEANUP.LOOKUP",
                FakeTransport(CloseLookupFailure()),
            )

    def test_strict_json_rejects_representation_and_number_attacks(self):
        cases = (
            b'\xef\xbb\xbf{"ok":true}',
            b'{"x":"\xff"}',
            b'{"x":1,"x":2}',
            b'{"x":"\\ud800"}',
            '{"x":"e\u0301"}'.encode("utf-8"),
            b'{"x":1e999}',
            b'{"x":123456789012345678901}',
        )
        for index, raw in enumerate(cases):
            with self.subTest(index=index):
                with self.assertRaises(JsonBytesError):
                    self._run(
                        f"RUN.STRICT.{index}",
                        FakeTransport([ResponseFrame("first", raw, True)]),
                    )

    def test_output_collision_is_reserved_before_the_only_invocation(self):
        authenticated = request()
        value, _grant, kwargs = authenticated
        with tempfile.TemporaryDirectory(
            dir=WORKSPACE / "s0-lab" / "i1" / "tests"
        ) as temporary:
            output = Path(temporary) / "result.json"
            output.write_bytes(b"existing")
            transport = FakeTransport([ResponseFrame("first", b"{}", True)])
            with self.assertRaisesRegex(OutputError, "overwrite"):
                run_one_shot_to_new_file(
                    "RUN.COLLISION", value, transport, output, **kwargs
                )
            self.assertEqual(transport.calls, 0)
            self.assertEqual(output.read_bytes(), b"existing")

    def test_reservation_exists_during_invocation_and_is_removed_on_failure(self):
        value, _grant, kwargs = request()
        with tempfile.TemporaryDirectory(
            dir=WORKSPACE / "s0-lab" / "i1" / "tests"
        ) as temporary:
            output = Path(temporary) / "result.json"

            class ObservingTransport(FakeTransport):
                def invoke_once(self, request_bytes, *, policy):
                    self.calls += 1
                    self.policies.append(policy)
                    self.reserved = output.exists() and output.read_bytes() == b""
                    return iter(self.frames)

            malformed = ObservingTransport(
                [ResponseFrame("first", b"not-json", True)]
            )
            with self.assertRaises(JsonBytesError):
                run_one_shot_to_new_file(
                    "RUN.RESERVED", value, malformed, output, **kwargs
                )
            self.assertTrue(malformed.reserved)
            self.assertFalse(output.exists())

    def test_successful_output_is_neutral_and_never_overwritten(self):
        value, _grant, kwargs = request()
        with tempfile.TemporaryDirectory(
            dir=WORKSPACE / "s0-lab" / "i1" / "tests"
        ) as temporary:
            output = Path(temporary) / "result.json"
            valid = FakeTransport([ResponseFrame("first", b'{"ok":true}', True)])
            run_one_shot_to_new_file(
                "RUN.PUBLIC.9", value, valid, output, **kwargs
            )
            first = output.read_bytes()
            parsed = json.loads(first)
            self.assertEqual(
                parsed["record_kind"], "i1-public-one-shot-structural-result"
            )
            self.assertNotIn("raw_response", parsed)
            with self.assertRaisesRegex(OutputError, "overwrite"):
                run_one_shot_to_new_file(
                    "RUN.PUBLIC.10",
                    value,
                    FakeTransport([ResponseFrame("first", b"{}", True)]),
                    output,
                    **kwargs,
                )
            self.assertEqual(output.read_bytes(), first)


if __name__ == "__main__":
    unittest.main()

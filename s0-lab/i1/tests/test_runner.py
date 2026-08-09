from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


WORKSPACE = Path(__file__).resolve().parents[3]
IMPLEMENTATION = WORKSPACE / "s0-lab" / "i1" / "implementation"
sys.path.insert(0, str(IMPLEMENTATION))

from s0_i1.auth import (  # noqa: E402
    AuthenticatedBytes,
    ManifestAnchor,
    authenticate_manifest_entry,
    load_authenticated_manifest,
    sha256_bytes,
)
from s0_i1.errors import JsonBytesError, OutputError, RunnerPolicyError  # noqa: E402
from s0_i1.runner import (  # noqa: E402
    MAX_RESPONSE_BYTES,
    ONE_SHOT_POLICY,
    ResponseFrame,
    run_one_shot,
    run_one_shot_to_new_file,
)


def request(raw: bytes = b"non-semantic-public-request") -> AuthenticatedBytes:
    with tempfile.TemporaryDirectory(dir=WORKSPACE / "s0-lab" / "i1" / "tests") as temporary:
        root = Path(temporary)
        input_path = root / "inputs" / "request.bin"
        input_path.parent.mkdir(parents=True)
        input_path.write_bytes(raw)
        manifest_raw = (
            f"{sha256_bytes(raw)}  inputs/request.bin\n".encode("ascii")
        )
        manifest_path = root / "inputs" / "files.sha256"
        manifest_path.write_bytes(manifest_raw)
        anchor = ManifestAnchor(
            "inputs/files.sha256", sha256_bytes(manifest_raw), "inputs/"
        )
        manifest = load_authenticated_manifest(root, anchor)
        return authenticate_manifest_entry(root, manifest, "inputs/request.bin")


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
    def test_policy_is_exactly_one_call_zero_retry_tools_and_state(self):
        transport = FakeTransport([ResponseFrame("first", b'{"ok":true}', True)])
        result = run_one_shot("RUN.PUBLIC.1", request(), transport)
        self.assertEqual(transport.calls, 1)
        self.assertEqual(transport.policies, [ONE_SHOT_POLICY])
        self.assertEqual(ONE_SHOT_POLICY.invocation_limit, 1)
        self.assertEqual(ONE_SHOT_POLICY.retry_limit, 0)
        self.assertEqual(ONE_SHOT_POLICY.tool_count, 0)
        self.assertEqual(ONE_SHOT_POLICY.state_mode, "none")
        self.assertEqual(ONE_SHOT_POLICY.response_selection, "first-only")
        self.assertEqual(result.parsed_response, {"ok": True})

    def test_transport_failure_is_not_retried(self):
        transport = FakeTransport(error=RuntimeError("sentinel transport failure"))
        with self.assertRaisesRegex(RuntimeError, "sentinel"):
            run_one_shot("RUN.PUBLIC.2", request(), transport)
        self.assertEqual(transport.calls, 1)

    def test_8192_ceiling_is_checked_before_decode_or_parse(self):
        transport = FakeTransport(
            [ResponseFrame("first", b"x" * (MAX_RESPONSE_BYTES + 1), True)]
        )
        with patch("s0_i1.runner.parse_strict_json_bytes") as parser:
            with self.assertRaisesRegex(RunnerPolicyError, "8192"):
                run_one_shot("RUN.PUBLIC.3", request(), transport)
        parser.assert_not_called()

    def test_exact_8192_bytes_reach_parse_but_malformed_json_rejects(self):
        raw = b" " * (MAX_RESPONSE_BYTES - 2) + b"{}"
        transport = FakeTransport([ResponseFrame("first", raw, True)])
        result = run_one_shot("RUN.PUBLIC.4", request(), transport)
        self.assertEqual(len(result.raw_response), MAX_RESPONSE_BYTES)
        self.assertEqual(result.parsed_response, {})

    def test_first_response_final_stops_before_later_response(self):
        state = {"later_yielded": False}

        def frames():
            yield ResponseFrame("first", b'{"first":true}', True)
            state["later_yielded"] = True
            yield ResponseFrame("second", b'{"second":true}', True)

        transport = FakeTransport(frames())
        result = run_one_shot("RUN.PUBLIC.5", request(), transport)
        self.assertEqual(result.parsed_response, {"first": True})
        self.assertFalse(state["later_yielded"])

    def test_mixed_response_ids_before_final_reject(self):
        transport = FakeTransport(
            [
                ResponseFrame("first", b"{", False),
                ResponseFrame("second", b"}", True),
            ]
        )
        with self.assertRaisesRegex(RunnerPolicyError, "later response"):
            run_one_shot("RUN.PUBLIC.6", request(), transport)

    def test_strict_json_rejects_bom_duplicate_keys_surrogate_and_non_nfc(self):
        cases = (
            b'\xef\xbb\xbf{"ok":true}',
            b'{"x":"\xff"}',
            b'{"x":1,"x":2}',
            b'{"x":"\\ud800"}',
            '{"x":"e\u0301"}'.encode("utf-8"),
            b'{"x":1e999}',
        )
        for index, raw in enumerate(cases):
            with self.subTest(index=index):
                with self.assertRaises(JsonBytesError):
                    run_one_shot(
                        f"RUN.STRICT.{index}",
                        request(),
                        FakeTransport([ResponseFrame("first", raw, True)]),
                    )

    def test_inconsistent_authenticated_request_rejects_before_transport(self):
        transport = FakeTransport([ResponseFrame("first", b"{}", True)])
        inconsistent = object.__new__(AuthenticatedBytes)
        object.__setattr__(inconsistent, "relative_path", "sentinel/request.bin")
        object.__setattr__(inconsistent, "sha256", sha256_bytes(b"request"))
        object.__setattr__(inconsistent, "raw", b"request")
        object.__setattr__(inconsistent, "authority_sha256", "0" * 64)
        object.__setattr__(inconsistent, "authority_kind", "forged")
        with self.assertRaisesRegex(RunnerPolicyError, "same-bytes"):
            run_one_shot("RUN.PUBLIC.7", inconsistent, transport)
        self.assertEqual(transport.calls, 0)

    def test_no_output_on_any_runner_failure_and_no_overwrite(self):
        with tempfile.TemporaryDirectory(dir=WORKSPACE / "s0-lab" / "i1" / "tests") as temporary:
            output = Path(temporary) / "result.json"
            malformed = FakeTransport([ResponseFrame("first", b"not-json", True)])
            with self.assertRaises(JsonBytesError):
                run_one_shot_to_new_file("RUN.PUBLIC.8", request(), malformed, output)
            self.assertFalse(output.exists())

            valid = FakeTransport([ResponseFrame("first", b'{"ok":true}', True)])
            run_one_shot_to_new_file("RUN.PUBLIC.9", request(), valid, output)
            first = output.read_bytes()
            parsed = json.loads(first)
            self.assertEqual(parsed["record_kind"], "i1-public-one-shot-structural-result")
            self.assertNotIn("raw_response", parsed)
            with self.assertRaisesRegex(OutputError, "overwrite"):
                run_one_shot_to_new_file(
                    "RUN.PUBLIC.10",
                    request(),
                    FakeTransport([ResponseFrame("first", b"{}", True)]),
                    output,
                )
            self.assertEqual(output.read_bytes(), first)


if __name__ == "__main__":
    unittest.main()

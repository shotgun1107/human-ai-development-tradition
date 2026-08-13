"""Candidate-owned eager one-frame exact-answer transport."""

from __future__ import annotations

from dataclasses import dataclass
from threading import Lock
from typing import Any

from .constants import REQUIRED_STUB_COUNTERS, STUB_RESPONSE_ID


class StubIntegrityError(RuntimeError):
    """The exact-answer script or any of its five counters is invalid."""


@dataclass(frozen=True)
class StubCounters:
    transport_calls: int
    script_frame_count: int
    yielded_frame_count: int
    close_count: int
    unconsumed_frame_count_on_close: int
    yielded_final_frame_count: int

    def five_counter_dict(self) -> dict[str, int]:
        return {
            "transport_calls": self.transport_calls,
            "script_frame_count": self.script_frame_count,
            "yielded_frame_count": self.yielded_frame_count,
            "close_count": self.close_count,
            "unconsumed_frame_count_on_close": self.unconsumed_frame_count_on_close,
        }


class _ExactScriptIterator:
    def __init__(self, owner: "ExactAnswerStub") -> None:
        self._owner = owner
        self._index = 0
        self._closed = False

    def __iter__(self) -> "_ExactScriptIterator":
        return self

    def __next__(self) -> Any:
        if self._closed or self._index >= len(self._owner._script):
            raise StopIteration
        frame = self._owner._script[self._index]
        self._index += 1
        self._owner._record_yield(frame)
        return frame

    def close(self) -> None:
        if self._closed:
            self._owner._record_second_close()
            raise StubIntegrityError("stub iterator close called more than once")
        self._closed = True
        self._owner._record_close()


class ExactAnswerStub:
    """One-use transport whose immutable script is fixed before reservation."""

    def __init__(
        self,
        *,
        expected_request_raw: bytes,
        response_raw: bytes,
        response_frame_type: type,
    ) -> None:
        if type(expected_request_raw) is not bytes or type(response_raw) is not bytes:
            raise StubIntegrityError("stub inputs must be exact bytes")
        frame = response_frame_type(
            response_id=STUB_RESPONSE_ID,
            data=response_raw,
            final=True,
        )
        self._expected_request_raw = expected_request_raw
        self._script = (frame,)
        self._lock = Lock()
        self._transport_calls = 0
        self._yielded_frame_count = 0
        self._yielded_final_frame_count = 0
        self._close_count = 0
        self._unconsumed_frame_count_on_close: int | None = None

    def invoke_once(self, request_bytes: bytes, *, policy: object) -> _ExactScriptIterator:
        with self._lock:
            if self._transport_calls != 0:
                # Reject the second entry without ever publishing an
                # impossible counter value above the frozen maximum of one.
                raise StubIntegrityError("stub transport entered more than once")
            self._transport_calls = 1
        if type(request_bytes) is not bytes or request_bytes != self._expected_request_raw:
            raise StubIntegrityError("stub received non-frozen request bytes")
        expected_policy = {
            "invocation_limit": 1,
            "retry_limit": 0,
            "tool_count": 0,
            "state_mode": "none",
            "response_selection": "first-final-only",
            "max_response_bytes": 8192,
            "max_response_frames": 256,
            "empty_frame_mode": "reject",
        }
        if any(getattr(policy, name, object()) != value for name, value in expected_policy.items()):
            raise StubIntegrityError("stub received a non-frozen one-shot policy")
        return _ExactScriptIterator(self)

    def _record_yield(self, frame: object) -> None:
        with self._lock:
            self._yielded_frame_count += 1
            if getattr(frame, "final", None) is True:
                self._yielded_final_frame_count += 1

    def _record_close(self) -> None:
        with self._lock:
            self._close_count += 1
            unconsumed = len(self._script) - self._yielded_frame_count
            self._unconsumed_frame_count_on_close = unconsumed
        if unconsumed != 0:
            raise StubIntegrityError("stub script was not exhausted at close")

    def _record_second_close(self) -> None:
        with self._lock:
            self._close_count += 1

    @property
    def transport_calls(self) -> int:
        with self._lock:
            return self._transport_calls

    def snapshot(self) -> StubCounters:
        with self._lock:
            unconsumed = self._unconsumed_frame_count_on_close
            return StubCounters(
                transport_calls=self._transport_calls,
                script_frame_count=len(self._script),
                yielded_frame_count=self._yielded_frame_count,
                close_count=self._close_count,
                unconsumed_frame_count_on_close=(
                    -1 if unconsumed is None else unconsumed
                ),
                yielded_final_frame_count=self._yielded_final_frame_count,
            )

    def require_integrity(self) -> StubCounters:
        counters = self.snapshot()
        if counters.five_counter_dict() != dict(REQUIRED_STUB_COUNTERS):
            raise StubIntegrityError("stub five-counter integrity mismatch")
        if counters.yielded_final_frame_count != 1:
            raise StubIntegrityError("stub final-frame count mismatch")
        return counters

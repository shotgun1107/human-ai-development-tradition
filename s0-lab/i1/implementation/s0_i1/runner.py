"""Provider-neutral, strictly one-shot public runner boundary.

There is deliberately no provider, network, model, executor-creation, tool, or
persistent-state implementation.  The only injectable operation is one call to
``invoke_once``.  The effective answer semantics remain closed; this layer
performs generic strict-JSON representation checks only.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable, Protocol

from .auth import AuthenticatedBytes, has_authenticated_provenance, sha256_bytes
from .errors import OutputError, RunnerPolicyError
from .json_bytes import parse_strict_json_bytes


MAX_RESPONSE_BYTES = 8192
_RUN_ID = re.compile(r"^[A-Za-z0-9._-]{1,128}$")


@dataclass(frozen=True)
class FrozenOneShotPolicy:
    invocation_limit: int = 1
    retry_limit: int = 0
    tool_count: int = 0
    state_mode: str = "none"
    response_selection: str = "first-only"
    max_response_bytes: int = MAX_RESPONSE_BYTES


ONE_SHOT_POLICY = FrozenOneShotPolicy()


@dataclass(frozen=True)
class ResponseFrame:
    """One chunk from the first response stream of an injected transport."""

    response_id: str
    data: bytes
    final: bool = False


class OneShotTransport(Protocol):
    def invoke_once(
        self, request_bytes: bytes, *, policy: FrozenOneShotPolicy
    ) -> Iterable[ResponseFrame]: ...


@dataclass(frozen=True)
class OneShotResult:
    run_id: str
    request_sha256: str
    raw_response: bytes
    parsed_response: dict[str, Any]

    def neutral_record(self) -> dict[str, Any]:
        return {
            "record_kind": "i1-public-one-shot-structural-result",
            "not_an_s0_run": True,
            "run_id": self.run_id,
            "request_sha256": self.request_sha256,
            "response_sha256": sha256_bytes(self.raw_response),
            "response_bytes": len(self.raw_response),
            "parsed_type": "object",
        }

    def neutral_record_bytes(self) -> bytes:
        return (
            json.dumps(
                self.neutral_record(),
                ensure_ascii=True,
                sort_keys=True,
                separators=(",", ":"),
            )
            + "\n"
        ).encode("ascii")


def _close_iterator(iterator: object) -> None:
    close = getattr(iterator, "close", None)
    if callable(close):
        close()


def run_one_shot(
    run_id: str,
    request: AuthenticatedBytes,
    transport: OneShotTransport,
) -> OneShotResult:
    """Invoke exactly once, retain only the first response, then parse."""

    if not _RUN_ID.fullmatch(run_id):
        raise RunnerPolicyError("opaque run ID syntax is invalid")
    if not has_authenticated_provenance(request):
        raise RunnerPolicyError("request must be authenticated same-bytes input")
    if request.sha256 != sha256_bytes(request.raw):
        raise RunnerPolicyError("request same-bytes authentication is inconsistent")

    # This is the only transport call in the implementation.  It receives a
    # frozen policy with no retries, tools, or state surface.
    frames = iter(transport.invoke_once(request.raw, policy=ONE_SHOT_POLICY))
    response_id: str | None = None
    chunks: list[bytes] = []
    total = 0
    final_seen = False
    try:
        for frame in frames:
            if not isinstance(frame, ResponseFrame):
                raise RunnerPolicyError("transport yielded a non-frame value")
            if not frame.response_id or not isinstance(frame.data, bytes):
                raise RunnerPolicyError("response frame identity or bytes are invalid")
            if response_id is None:
                response_id = frame.response_id
            elif frame.response_id != response_id:
                raise RunnerPolicyError("a later response entered the first-response stream")
            if final_seen:
                raise RunnerPolicyError("bytes followed the final first-response frame")
            total += len(frame.data)
            # The ceiling is checked before UTF-8 decoding or JSON parsing.
            if total > MAX_RESPONSE_BYTES:
                raise RunnerPolicyError("first response exceeds 8192 bytes")
            chunks.append(frame.data)
            if frame.final:
                final_seen = True
                break
    finally:
        # Do not consume a provider's second response after the first final
        # frame.  Closing is best-effort local iterator cleanup, not a retry.
        _close_iterator(frames)
    if response_id is None or not final_seen or total == 0:
        raise RunnerPolicyError("first response stream is empty or incomplete")

    raw = b"".join(chunks)
    parsed = parse_strict_json_bytes(raw, require_object=True)
    return OneShotResult(run_id, request.sha256, raw, parsed)


def run_one_shot_to_new_file(
    run_id: str,
    request: AuthenticatedBytes,
    transport: OneShotTransport,
    output_path: Path,
) -> OneShotResult:
    """Emit neutral metadata only after full success, never overwriting."""

    result = run_one_shot(run_id, request, transport)
    if not output_path.parent.is_dir() or output_path.is_symlink():
        raise OutputError("output parent must exist and output must not be a link")
    descriptor: int | None = None
    created = False
    try:
        descriptor = os.open(
            output_path,
            os.O_WRONLY
            | os.O_CREAT
            | os.O_EXCL
            | getattr(os, "O_BINARY", 0)
            | getattr(os, "O_CLOEXEC", 0),
            0o600,
        )
        created = True
        raw = result.neutral_record_bytes()
        offset = 0
        while offset < len(raw):
            written = os.write(descriptor, raw[offset:])
            if written <= 0:
                raise OutputError("neutral result write failed")
            offset += written
        os.fsync(descriptor)
    except FileExistsError as exc:
        raise OutputError("output already exists; overwrite is forbidden") from exc
    except Exception:
        if descriptor is not None:
            os.close(descriptor)
            descriptor = None
        if created:
            try:
                output_path.unlink()
            except OSError:
                pass
        raise
    finally:
        if descriptor is not None:
            os.close(descriptor)
    return result

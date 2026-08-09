"""Provider-neutral, bounded, one-shot public runner boundary.

There is no provider, network, model, executor-creation, tool, or persistent
state implementation.  The only injectable operation is one ``invoke_once``
call.  A request is usable only when it is bound to the exact manifest grant
held by the configured caller and matches separately expected authority/path
values.  Effective answer semantics remain closed; only strict generic JSON
representation checks are performed.
"""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Protocol

from .auth import (
    AuthenticatedBytes,
    ManifestGrant,
    has_authenticated_provenance,
    require_manifest_grant,
    sha256_bytes,
)
from .errors import OutputError, RunnerPolicyError
from .json_bytes import parse_strict_json_bytes


MAX_RESPONSE_BYTES = 8192
MAX_RESPONSE_FRAMES = 256
_RUN_ID = re.compile(r"^[A-Za-z0-9._-]{1,128}$")
_RESPONSE_ID = re.compile(r"^[A-Za-z0-9._-]{1,128}$")


@dataclass(frozen=True)
class FrozenOneShotPolicy:
    invocation_limit: int = 1
    retry_limit: int = 0
    tool_count: int = 0
    state_mode: str = "none"
    response_selection: str = "first-final-only"
    max_response_bytes: int = MAX_RESPONSE_BYTES
    max_response_frames: int = MAX_RESPONSE_FRAMES
    empty_frame_mode: str = "reject"


ONE_SHOT_POLICY = FrozenOneShotPolicy()


def _require_policy_integrity() -> None:
    expected = FrozenOneShotPolicy()
    if ONE_SHOT_POLICY != expected or any(
        type(value) is not expected_type
        for value, expected_type in (
            (ONE_SHOT_POLICY.invocation_limit, int),
            (ONE_SHOT_POLICY.retry_limit, int),
            (ONE_SHOT_POLICY.tool_count, int),
            (ONE_SHOT_POLICY.state_mode, str),
            (ONE_SHOT_POLICY.response_selection, str),
            (ONE_SHOT_POLICY.max_response_bytes, int),
            (ONE_SHOT_POLICY.max_response_frames, int),
            (ONE_SHOT_POLICY.empty_frame_mode, str),
        )
    ):
        raise RunnerPolicyError("one-shot policy integrity check failed")


@dataclass(frozen=True)
class ResponseFrame:
    """One non-empty chunk from the first response stream."""

    response_id: str
    data: bytes
    final: bool = False

    def __post_init__(self) -> None:
        if type(self.response_id) is not str or not _RESPONSE_ID.fullmatch(
            self.response_id
        ):
            raise RunnerPolicyError("response frame identity is invalid")
        if type(self.data) is not bytes or not self.data:
            raise RunnerPolicyError("response frame data must be non-empty exact bytes")
        if type(self.final) is not bool:
            raise RunnerPolicyError("response frame final flag must be exact boolean")


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


def _validate_request_authority(
    request: object,
    *,
    required_grant: ManifestGrant,
    expected_authority_sha256: str,
    expected_authority_path: str,
    expected_request_path: str,
    expected_purpose: str,
) -> AuthenticatedBytes:
    try:
        grant = require_manifest_grant(required_grant)
    except Exception as exc:
        raise RunnerPolicyError("required manifest grant is invalid") from exc
    expected_values = (
        (expected_authority_sha256, "expected authority digest"),
        (expected_authority_path, "expected authority path"),
        (expected_request_path, "expected request path"),
        (expected_purpose, "expected grant purpose"),
    )
    if any(type(value) is not str for value, _label in expected_values):
        raise RunnerPolicyError("runner authority expectations must be exact strings")
    if (
        expected_authority_sha256 != grant.manifest_sha256
        or expected_authority_path != grant.manifest_path
        or expected_request_path not in grant.allowed_paths
        or expected_purpose != grant.purpose
    ):
        raise RunnerPolicyError("runner expectations do not match the required grant")
    if not has_authenticated_provenance(
        request,
        required_grant=grant,
        expected_authority_sha256=expected_authority_sha256,
        expected_authority_path=expected_authority_path,
        expected_relative_path=expected_request_path,
        expected_purpose=expected_purpose,
    ):
        raise RunnerPolicyError(
            "request authority, path, grant, or same-bytes binding is invalid"
        )
    return request


def _close_iterator(iterator: object, primary_error: BaseException | None) -> None:
    try:
        close = getattr(iterator, "close", None)
    except Exception as exc:
        if primary_error is None:
            raise RunnerPolicyError("transport iterator cleanup lookup failed") from exc
        return
    if not callable(close):
        return
    try:
        close()
    except Exception as exc:
        # A cleanup failure invalidates an otherwise successful call.  When a
        # validation/transport failure is already active, it remains primary
        # and the cleanup failure is deliberately secondary.
        if primary_error is None:
            raise RunnerPolicyError("transport iterator cleanup failed") from exc


def run_one_shot(
    run_id: str,
    request: AuthenticatedBytes,
    transport: OneShotTransport,
    *,
    required_grant: ManifestGrant,
    expected_authority_sha256: str,
    expected_authority_path: str,
    expected_request_path: str,
    expected_purpose: str,
) -> OneShotResult:
    """Invoke once, accept the first final frame, close, then parse."""

    if type(run_id) is not str or not _RUN_ID.fullmatch(run_id):
        raise RunnerPolicyError("opaque run ID syntax is invalid")
    _require_policy_integrity()
    authenticated = _validate_request_authority(
        request,
        required_grant=required_grant,
        expected_authority_sha256=expected_authority_sha256,
        expected_authority_path=expected_authority_path,
        expected_request_path=expected_request_path,
        expected_purpose=expected_purpose,
    )
    request_raw = authenticated.raw
    request_digest = authenticated.sha256

    # This is the sole invocation in the implementation.  No retry surface is
    # present.  Iterator creation is part of that one invocation.
    iterable = transport.invoke_once(request_raw, policy=ONE_SHOT_POLICY)
    try:
        frames = iter(iterable)
    except Exception as exc:
        raise RunnerPolicyError("transport did not return an iterable stream") from exc

    response_id: str | None = None
    chunks: list[bytes] = []
    total = 0
    final_seen = False
    frame_count = 0
    primary_error: BaseException | None = None
    try:
        for frame in frames:
            frame_count += 1
            if frame_count > MAX_RESPONSE_FRAMES:
                raise RunnerPolicyError("first response exceeds the 256-frame ceiling")
            if type(frame) is not ResponseFrame:
                raise RunnerPolicyError("transport yielded a non-exact frame value")
            if type(frame.response_id) is not str or not _RESPONSE_ID.fullmatch(
                frame.response_id
            ):
                raise RunnerPolicyError("response frame identity is invalid")
            if type(frame.data) is not bytes or not frame.data:
                raise RunnerPolicyError("empty or non-byte response frame is forbidden")
            if type(frame.final) is not bool:
                raise RunnerPolicyError("response final flag must be exact boolean")
            if response_id is None:
                response_id = frame.response_id
            elif frame.response_id != response_id:
                raise RunnerPolicyError(
                    "a later response entered the first-response stream"
                )
            if final_seen:
                raise RunnerPolicyError("bytes followed the final first-response frame")
            total += len(frame.data)
            if total > MAX_RESPONSE_BYTES:
                raise RunnerPolicyError("first response exceeds 8192 bytes")
            chunks.append(frame.data)
            if frame.final:
                final_seen = True
                break
    except BaseException as exc:
        primary_error = exc
        raise
    finally:
        _close_iterator(frames, primary_error)

    if response_id is None or not final_seen or total == 0:
        raise RunnerPolicyError("first response stream is empty or incomplete")
    _require_policy_integrity()
    _validate_request_authority(
        request,
        required_grant=required_grant,
        expected_authority_sha256=expected_authority_sha256,
        expected_authority_path=expected_authority_path,
        expected_request_path=expected_request_path,
        expected_purpose=expected_purpose,
    )
    if authenticated.raw != request_raw or authenticated.sha256 != request_digest:
        raise RunnerPolicyError("request binding changed during the one-shot invocation")

    raw = b"".join(chunks)
    parsed = parse_strict_json_bytes(raw, require_object=True)
    return OneShotResult(run_id, request_digest, raw, parsed)


def _reserve_output(output_path: Path) -> int:
    if not isinstance(output_path, Path):
        raise OutputError("output path must be a Path")
    if not output_path.parent.is_dir() or output_path.parent.is_symlink():
        raise OutputError("output parent must be an existing non-link directory")
    if output_path.is_symlink():
        raise OutputError("output must not be a symbolic link")
    try:
        return os.open(
            output_path,
            os.O_WRONLY
            | os.O_CREAT
            | os.O_EXCL
            | getattr(os, "O_BINARY", 0)
            | getattr(os, "O_CLOEXEC", 0),
            0o600,
        )
    except FileExistsError as exc:
        raise OutputError("output already exists; overwrite is forbidden") from exc
    except OSError as exc:
        raise OutputError("output reservation failed") from exc


def _remove_reservation(output_path: Path, primary_error: BaseException) -> None:
    try:
        output_path.unlink()
    except OSError as exc:
        raise OutputError("output reservation cleanup failed") from exc


def run_one_shot_to_new_file(
    run_id: str,
    request: AuthenticatedBytes,
    transport: OneShotTransport,
    output_path: Path,
    *,
    required_grant: ManifestGrant,
    expected_authority_sha256: str,
    expected_authority_path: str,
    expected_request_path: str,
    expected_purpose: str,
) -> OneShotResult:
    """Reserve the collision-free output before the sole invocation."""

    # Authority and run ID are checked before reserving; reservation is still
    # completed before transport invocation or stream consumption.
    if type(run_id) is not str or not _RUN_ID.fullmatch(run_id):
        raise RunnerPolicyError("opaque run ID syntax is invalid")
    _validate_request_authority(
        request,
        required_grant=required_grant,
        expected_authority_sha256=expected_authority_sha256,
        expected_authority_path=expected_authority_path,
        expected_request_path=expected_request_path,
        expected_purpose=expected_purpose,
    )
    descriptor = _reserve_output(output_path)
    try:
        result = run_one_shot(
            run_id,
            request,
            transport,
            required_grant=required_grant,
            expected_authority_sha256=expected_authority_sha256,
            expected_authority_path=expected_authority_path,
            expected_request_path=expected_request_path,
            expected_purpose=expected_purpose,
        )
        raw = result.neutral_record_bytes()
        offset = 0
        while offset < len(raw):
            written = os.write(descriptor, raw[offset:])
            if type(written) is not int or written <= 0:
                raise OutputError("neutral result write failed")
            offset += written
        os.fsync(descriptor)
    except BaseException as exc:
        try:
            os.close(descriptor)
        except OSError:
            pass
        _remove_reservation(output_path, exc)
        raise
    try:
        os.close(descriptor)
    except OSError as exc:
        try:
            _remove_reservation(output_path, exc)
        except OutputError:
            raise
        raise OutputError("neutral result close failed") from exc
    return result

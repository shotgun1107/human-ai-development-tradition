"""Verifier-parent publication observer and exact two-event trace."""

from __future__ import annotations

from pathlib import Path
from typing import Protocol

from .authority import (
    _PublicationWitness,
    _RunCapability,
    _is_capability,
    _issue_capability,
    _issue_witness,
)
from .errors import record_failure
from .models import FileIdentity, FileSnapshot, MoveEvent, MoveResult
from .win32 import ABI_PROFILE_ID, Win32PublicationBackend


OBSERVER_ID = "S0-PUBLIC-ASSEMBLY-PUBLICATION-OBSERVER-2"

_EVENTS = (
    ("PUBLISH_RECORD\n", "run-record.pending", "run-record.json"),
    ("PUBLISH_RECEIPT\n", "publication-receipt.pending", "publication-receipt.json"),
)


class PublicationBackend(Protocol):
    @property
    def output_root(self) -> Path: ...

    @property
    def root_identity(self) -> FileIdentity: ...

    def inspect_file(self, path: Path) -> FileSnapshot: ...

    def path_absent(self, path: Path) -> bool: ...

    def move_no_replace(self, source: Path, destination: Path) -> MoveResult: ...

    def canonical_event_path(self, path: Path) -> str: ...


class PublicationObserver:
    """One observer instance for one child, pipe endpoint, and fresh root."""

    __slots__ = ("_backend", "_events", "_capability")

    def __init__(
        self,
        *,
        backend: PublicationBackend,
        child_identity: object,
        parent_pipe_identity: object,
    ) -> None:
        if not isinstance(backend.output_root, Path):
            raise TypeError("publication backend root must be pathlib.Path")
        self._backend = backend
        self._events: list[MoveEvent] = []
        self._capability = _issue_capability(
            observer=self,
            child=child_identity,
            pipe=parent_pipe_identity,
            root=backend.output_root,
        )

    @classmethod
    def for_real_win32(
        cls,
        *,
        output_root: Path,
        child_identity: object,
        parent_pipe_identity: object,
    ) -> "PublicationObserver":
        return cls(
            backend=Win32PublicationBackend(output_root),
            child_identity=child_identity,
            parent_pipe_identity=parent_pipe_identity,
        )

    @property
    def trace(self) -> tuple[MoveEvent, ...]:
        return tuple(self._events)

    @property
    def output_root(self) -> Path:
        return self._backend.output_root

    @property
    def root_identity(self) -> FileIdentity:
        return self._backend.root_identity

    def observe_message(
        self,
        message: bytes,
        *,
        child_identity: object,
        parent_pipe_identity: object,
    ) -> tuple[bytes, _PublicationWitness | None]:
        try:
            capability = self._require_live_capability(child_identity, parent_pipe_identity)
        except BaseException:
            self._terminate()
            raise
        ordinal = len(self._events) + 1
        if ordinal not in {1, 2} or type(message) is not bytes:
            self._terminate()
            raise record_failure("publication IPC is post-terminal or not exact bytes")
        expected_text, source_name, destination_name = _EVENTS[ordinal - 1]
        try:
            decoded = message.decode("ascii")
        except UnicodeDecodeError as exc:
            self._terminate()
            raise record_failure("publication IPC is not exact ASCII") from exc
        if decoded != expected_text:
            self._terminate()
            raise record_failure("publication IPC message is partial, extra, duplicate, or reordered")
        source = Path(source_name)
        destination = Path(destination_name)
        try:
            pre = self._backend.inspect_file(source)
            if not self._backend.path_absent(destination):
                raise record_failure("publication destination exists immediately before the call")
            result = self._backend.move_no_replace(source, destination)
            if result.ffi_return_signed_int32 == 0:
                raise record_failure(
                    f"MoveFileExW failed with captured error {result.last_error_uint32}"
                )
            if result.last_error_uint32 != 0:
                raise record_failure("successful MoveFileExW event has a nonzero last-error sentinel")
            if not self._backend.path_absent(source):
                raise record_failure("publication source remains after successful move")
            post = self._backend.inspect_file(destination)
            if pre != post:
                raise record_failure("publication destination identity, length, or hash changed")
            event = MoveEvent(
                observer_instance_identity=id(self),
                run_capability_identity=id(capability),
                ordinal=ordinal,
                output_root_identity=self.root_identity,
                source_path=self._backend.canonical_event_path(source),
                destination_path=self._backend.canonical_event_path(destination),
                pre_volume_serial_number=pre.identity.volume_serial_number,
                pre_file_index_high=pre.identity.file_index_high,
                pre_file_index_low=pre.identity.file_index_low,
                pre_byte_length=pre.byte_length,
                pre_sha256=pre.sha256,
                destination_absent_before_call=True,
                abi_profile_id=ABI_PROFILE_ID,
                flags_numeric=0,
                ffi_return_signed_int32=result.ffi_return_signed_int32,
                last_error_uint32=result.last_error_uint32,
                source_absent_after_success=True,
                post_volume_serial_number=post.identity.volume_serial_number,
                post_file_index_high=post.identity.file_index_high,
                post_file_index_low=post.identity.file_index_low,
                post_byte_length=post.byte_length,
                post_sha256=post.sha256,
                terminal_status="success",
            )
            if event.field_count() != 23:
                raise record_failure("observer event field count is not exactly 23")
            self._events.append(event)
            witness = None
            if ordinal == 2:
                witness = _issue_witness(
                    observer=self,
                    capability=capability,
                    events=tuple(self._events),
                )
            return b"OK\n", witness
        except BaseException:
            self._terminate()
            raise

    def _require_live_capability(self, child: object, pipe: object) -> _RunCapability:
        capability = self._capability
        if (
            not _is_capability(capability)
            or capability.observer is not self
            or capability.child is not child
            or capability.pipe is not pipe
            or capability.root != self.output_root
            or capability.terminal
        ):
            raise record_failure("run capability identity or binding is invalid")
        return capability

    def _terminate(self) -> None:
        self._capability.terminal = True

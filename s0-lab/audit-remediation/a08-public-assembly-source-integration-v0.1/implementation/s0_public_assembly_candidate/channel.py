"""The child side of the fixed two-message ASCII publication channel."""

from __future__ import annotations

from typing import BinaryIO

from .constants import PUBLISH_OK, PUBLISH_RECEIPT, PUBLISH_RECORD


class PublicationChannelError(RuntimeError):
    """The fixed request/reply protocol did not complete exactly."""


class FixedAsciiPipeChannel:
    """Send only RECORD then RECEIPT and accept only one OK per request."""

    def __init__(self, request_writer: BinaryIO, reply_reader: BinaryIO) -> None:
        self._request_writer = request_writer
        self._reply_reader = reply_reader
        self._state = 0

    @property
    def state(self) -> int:
        return self._state

    def _read_exact_ok(self) -> None:
        chunks: list[bytes] = []
        remaining = len(PUBLISH_OK)
        while remaining:
            chunk = self._reply_reader.read(remaining)
            if type(chunk) is not bytes or not chunk:
                raise PublicationChannelError("publication reply was partial or absent")
            chunks.append(chunk)
            remaining -= len(chunk)
        if b"".join(chunks) != PUBLISH_OK:
            raise PublicationChannelError("publication reply was not exact ASCII OK")

    def _send(self, request: bytes) -> None:
        written = self._request_writer.write(request)
        if type(written) is not int or written != len(request):
            raise PublicationChannelError("publication request write was not exact")
        self._request_writer.flush()
        self._read_exact_ok()

    def publish_record(self) -> None:
        if self._state != 0:
            raise PublicationChannelError("record request is out of order or duplicated")
        self._send(PUBLISH_RECORD)
        self._state = 1

    def publish_receipt(self) -> None:
        if self._state != 1:
            raise PublicationChannelError("receipt request is out of order or duplicated")
        self._send(PUBLISH_RECEIPT)
        self._state = 2


"""Stable public error surface for the bounded I3 candidate."""

from __future__ import annotations


class I3Error(ValueError):
    """Base class for deterministic public I3 failures."""

    code = "I3_ERROR"

    def __init__(self, detail: str) -> None:
        super().__init__(f"{self.code}: {detail}")
        self.detail = detail


class I3ByteError(I3Error):
    code = "I3_BYTE_ERROR"


class I3FieldError(I3Error):
    code = "I3_FIELD_ERROR"


class I3ValueError(I3Error):
    code = "I3_VALUE_ERROR"


class I3RouteError(I3Error):
    code = "I3_ROUTE_ERROR"


class I3TupleError(I3Error):
    code = "I3_TUPLE_ERROR"


class I3HashError(I3Error):
    code = "I3_HASH_ERROR"


class I3BindingError(I3Error):
    code = "I3_BINDING_ERROR"


class I3InputError(I3Error):
    code = "I3_INPUT_ERROR"


class I3EventError(I3Error):
    code = "I3_EVENT_ERROR"


class I3UnsupportedBoundaryError(I3Error):
    code = "I3_UNSUPPORTED_BOUNDARY"

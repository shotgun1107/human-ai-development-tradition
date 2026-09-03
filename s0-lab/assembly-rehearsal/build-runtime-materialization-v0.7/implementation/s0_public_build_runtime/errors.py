"""Fail-closed error taxonomy for PUBLIC runtime materialization v0.7."""


class BuildRuntimeError(RuntimeError):
    """Base class for a deterministic materializer rejection."""


class AuthenticationError(BuildRuntimeError):
    """A pinned input or an authority transition did not authenticate."""


class CanonicalError(BuildRuntimeError):
    """A canonical byte grammar or record binding was invalid."""


class PathSafetyError(BuildRuntimeError):
    """A Windows path lifecycle prerequisite was not satisfied."""


class AcquisitionError(BuildRuntimeError):
    """A cache or HTTPS acquisition did not yield the exact pinned bytes."""


class ArchiveError(BuildRuntimeError):
    """An archive inventory or extraction invariant was violated."""


class PublicationError(BuildRuntimeError):
    """No-replace publication or final readback failed."""


class ProbeError(BuildRuntimeError):
    """The isolated final-runtime import probe failed."""

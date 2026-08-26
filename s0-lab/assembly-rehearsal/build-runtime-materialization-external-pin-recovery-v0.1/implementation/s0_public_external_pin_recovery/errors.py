"""Errors raised by the public external-pin recovery implementation."""


class RecoveryError(Exception):
    """Base class for expected recovery failures."""


class AuthorityError(RecoveryError):
    """Raised when the requested operation exceeds granted authority."""


class AcquisitionError(RecoveryError):
    """Raised when a pinned artifact cannot be acquired safely."""


class MaterializationError(RecoveryError):
    """Raised when an acquired artifact cannot be materialized safely."""

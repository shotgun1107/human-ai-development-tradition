"""Errors raised by external-pin recovery implementation v0.2."""


class RecoveryError(Exception):
    """Base class for expected recovery failures."""


class AuthorityError(RecoveryError):
    """Raised when a requested operation exceeds frozen authority."""


class AcquisitionError(RecoveryError):
    """Raised when a pinned artifact cannot be acquired safely."""


class MaterializationError(RecoveryError):
    """Raised when an acquired artifact cannot be materialized safely."""

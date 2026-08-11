"""Stable public errors for the I2 trust-root/isolation candidate."""

from __future__ import annotations


class I2Error(ValueError):
    """Base class for deterministic public I2 validation failures."""


class CanonicalRecordError(I2Error):
    """A public import record is noncanonical or inconsistent."""


class BindingError(I2Error):
    """Two authenticated public records do not have identical bindings."""


class LifecycleError(I2Error):
    """An import route violates the frozen lifecycle."""


class VectorBindingError(I2Error):
    """The public hostile-vector package is not the frozen package."""

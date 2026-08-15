"""Stable error taxonomy for the bounded PUBLIC build/runtime candidate."""


class BuildRuntimeError(ValueError):
    """Base class for deterministic candidate rejection."""


class AuthenticationError(BuildRuntimeError):
    """An exact public input or manifest did not authenticate."""


class CanonicalError(BuildRuntimeError):
    """A byte grammar or canonical serialization was invalid."""


class SemanticError(BuildRuntimeError):
    """Authenticated inputs did not compose into the effective v0.5 contract."""


class PlanningError(BuildRuntimeError):
    """A non-executing build or materialization plan was invalid."""

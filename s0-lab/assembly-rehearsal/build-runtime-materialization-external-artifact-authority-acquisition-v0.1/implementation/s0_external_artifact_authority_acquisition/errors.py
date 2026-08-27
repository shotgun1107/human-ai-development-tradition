"""Fail-closed errors for external artifact authority acquisition v0.1."""


class AuthorityError(ValueError):
    """One independently labelled authority-acquisition rejection."""

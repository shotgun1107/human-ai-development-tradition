"""PUBLIC v0.3 package marker.

Importing the package deliberately imports no verifier implementation module.
Direct module use remains a trusted-host disk-consistency check and never
establishes executed-code or process authority.
"""

__all__: tuple[str, ...] = ()

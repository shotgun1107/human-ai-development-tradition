"""Verifier-owned authority for the bounded public assembly candidate.

Importing this package does not bind Win32 APIs, create a child, or mutate the
filesystem.  Runtime construction is deliberately explicit and remains a
separate gate from implementation review.
"""

from .consumer import LiveConsumer
from .observer import PublicationObserver
from .pins import ExternalPins

__all__ = ["ExternalPins", "LiveConsumer", "PublicationObserver"]
__version__ = "0.1.0"

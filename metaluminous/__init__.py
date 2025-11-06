"""Metaluminous Engine package"""
from .config import settings
from .core import MetaluminousEngine

__version__ = "0.1.0"

__all__ = [
    "settings",
    "MetaluminousEngine",
    "__version__",
]

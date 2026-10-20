"""mNumbers: a Python library for working with m-numbers (MNumber)."""

from importlib.metadata import PackageNotFoundError, version

from .mnumber import MNumber, MNumberError

try:
    __version__ = version("mnumbers")
except PackageNotFoundError:  # running from source without installation
    __version__ = "unknown"

__all__ = [
    "MNumber", 
    "MNumberError", 
    "__version__"
]
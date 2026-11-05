"""mWords: a Python library for working with m-words (MWord)."""

from importlib.metadata import PackageNotFoundError, version

from .mword import MWord, MWordError

try:
    __version__ = version("mwords")
except PackageNotFoundError:  # running from source without installation
    __version__ = "unknown"

__all__ = [
    "MWord", 
    "MWordError", 
    "__version__"
]

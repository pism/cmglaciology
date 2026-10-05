"""
cmglaciology is a package of colormaps for glaciology.

The packaging is adapted from cmcrameri by Callum Rollo
https://github.com/callumrollo/cmcrameri

See README.md for an overview and instructions.
"""

from importlib.metadata import PackageNotFoundError, version

from . import cm
from .cm import show_cmaps

__all__ = (
    "cm",
    "show_cmaps",
)


__authors__ = ["Andy Aschwanden <aaschwanden@alaska.edu>"]

try:
    # The version is computed from the git tags by setuptools_scm at install time
    __version__ = version("cmglaciology")
except PackageNotFoundError:  # running from a source tree that is not installed
    __version__ = "unknown"

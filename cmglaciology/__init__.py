"""
cmglaciology is a package of colormaps for glaciology.

The packaging is adapted from cmcrameri by Callum Rollo
https://github.com/callumrollo/cmcrameri

See README.md for an overview and instructions.
"""

from . import cm
from .cm import show_cmaps

__all__ = (
    "cm",
    "show_cmaps",
)


__authors__ = ["Andy Aschwanden <aaschwanden@alaska.edu>"]

__version__ = "0.1.0"

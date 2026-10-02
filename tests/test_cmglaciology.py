"""
Test that the program a) finds the text files and b) creates colormaps

Adapted from the cmcrameri test suite (https://github.com/callumrollo/cmcrameri).
"""

import sys
from pathlib import Path

import matplotlib
import numpy as np
from matplotlib.colors import Colormap

library_dir = Path(__file__).parent.parent.absolute()
sys.path.append(str(library_dir))
sys.path.append(str(library_dir / "scripts"))
from cmglaciology import cm


def test_find_files():
    assert len(cm.paths) > 0


def test_cmap_import():
    cmap_names = [name for name, cmap in vars(cm).items() if isinstance(cmap, Colormap)]
    # Should be as many colormaps as files, plus a reversed version of each
    assert len(cmap_names) == 2 * len(cm.paths)


def test_get_cmap():
    for name, cmap in vars(cm).items():
        # See if it is a colormap.
        if isinstance(cmap, Colormap):
            # if cmap hasn't been correctly registered as
            # cmg.name, it will raise a KeyError
            alt_cmap = matplotlib.colormaps["cmg." + name]
            # the registered cmap should be the same as cmap
            assert (np.array(cmap.colors) == np.array(alt_cmap.colors)).all()


def test_reversed():
    for path in cm.paths:
        cmap = getattr(cm, path.stem)
        cmap_r = getattr(cm, path.stem + "_r")
        assert (np.array(cmap.colors)[::-1] == np.array(cmap_r.colors)).all()


def test_matches_qgis_source():
    # The shipped tables should be up to date with the QGIS files in qgis/
    from qgis2txt import qgis2rgb, qgis_dir

    qgis_paths = sorted(qgis_dir.glob("*.txt"))
    assert [p.stem for p in qgis_paths] == [p.stem for p in cm.paths]
    for path in qgis_paths:
        cmap = getattr(cm, path.stem)
        np.testing.assert_allclose(cmap.colors, qgis2rgb(path), atol=1e-6)

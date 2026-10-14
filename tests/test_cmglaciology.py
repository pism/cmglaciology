"""
Test that the program a) finds the text files and b) creates colormaps

Adapted from the cmcrameri test suite (https://github.com/callumrollo/cmcrameri).
"""

import sys
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pytest
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


def test_show_cmaps():
    fig = cm.show_cmaps()
    # One row per colormap, without its reversed version
    assert len(fig.axes) == len(cm.paths)
    plt.close(fig)


def test_show_cmaps_cvd():
    pytest.importorskip("colorspacious")
    fig = cm.show_cmaps(cvd=True)
    # Normal vision, protanopia, deuteranopia and tritanopia for every colormap
    assert len(fig.axes) == 4 * len(cm.paths)
    titles = [ax.get_title() for ax in fig.axes[:4]]
    assert titles == ["Normal vision", "Protanopia", "Deuteranopia", "Tritanopia"]
    assert all(ax.get_title() == "" for ax in fig.axes[4:])
    plt.close(fig)


@pytest.mark.parametrize("cvd_type", ["protanomaly", "deuteranomaly", "tritanomaly"])
def test_simulate_cvd(cvd_type):
    pytest.importorskip("colorspacious")
    simulated = cm.simulate_cvd(cm.speed, cvd_type)
    colors = np.array(simulated.colors)
    assert simulated.name == f"speed_{cvd_type}"
    assert colors.shape == (256, 3)
    assert colors.min() >= 0 and colors.max() <= 1
    # The deficiency changes the colors
    assert not np.allclose(colors, np.array(cm.speed.colors))
    # A colormap can also be given by its registered name
    by_name = cm.simulate_cvd("cmg.speed", cvd_type)
    np.testing.assert_allclose(by_name.colors, colors)


def test_simulate_cvd_severity_zero_is_normal_vision():
    pytest.importorskip("colorspacious")
    simulated = cm.simulate_cvd(cm.speed, "deuteranomaly", severity=0)
    np.testing.assert_allclose(simulated.colors, cm.speed.colors, atol=1e-6)


def test_simulate_cvd_keeps_grays():
    # A gray has no hue to lose, so it looks the same with every deficiency
    pytest.importorskip("colorspacious")
    from matplotlib.colors import ListedColormap

    grays = ListedColormap(
        np.repeat(np.linspace(0, 1, 16)[:, np.newaxis], 3, axis=1), name="grays"
    )
    for cvd_type in ["protanomaly", "deuteranomaly", "tritanomaly"]:
        np.testing.assert_allclose(
            cm.simulate_cvd(grays, cvd_type).colors, grays.colors, atol=1e-3
        )


def test_simulate_cvd_rejects_unknown_type():
    pytest.importorskip("colorspacious")
    with pytest.raises(ValueError, match="cvd_type must be one of"):
        cm.simulate_cvd(cm.speed, "protanopia")

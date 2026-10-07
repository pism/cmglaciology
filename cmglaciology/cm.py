"""
Packaging of colormaps for glaciology.

The loading and registration machinery is adapted from cmcrameri by
Callum Rollo (https://github.com/callumrollo/cmcrameri), MIT License,
Copyright (c) 2020 Callum Rollo.
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np

_cmap_names_sequential = ("speed",)

_cmap_names_topographic = (
    "akbathtopo",
    "aktopo",
    "grisbathtopo",
    "gristopo",
)


def _load_cmaps():
    from pathlib import Path

    from matplotlib.colors import ListedColormap

    # Prepended to cmap names when registering
    cmap_reg_prefix = "cmg."

    cmaps = {}

    def register(cmap):
        # Register in Matplotlib
        matplotlib.colormaps.register(cmap=cmap, name=f"{cmap_reg_prefix}{cmap.name}")

        # Add to dict
        cmaps[cmap.name] = cmap

    # Find the colormap text files and make a list of the paths
    cmap_data_dir = Path(__file__).parent / "cmaps"
    paths = sorted(cmap_data_dir.glob("*.txt"))

    # Load data and generate Colormap objects
    for cmap_path in paths:
        # Name of colormap is taken from the text file name
        cmap_name = cmap_path.stem

        # Check categorization
        is_sequential = cmap_name in _cmap_names_sequential
        is_topographic = cmap_name in _cmap_names_topographic
        assert (
            sum([is_sequential, is_topographic]) == 1
        ), f"{cmap_name} not categorized properly"

        # Load data
        data = np.loadtxt(cmap_path)
        N = data.shape[0]
        assert N == 256, f"N should be 256 but is {N}"

        # Create and register colormap and its reverse version
        cmap = ListedColormap(colors=data, name=cmap_name)
        register(cmap)
        register(cmap.reversed())

    return paths, cmaps


paths, cmaps = _load_cmaps()

# Add all cmaps to the `cmglaciology.cm` namespace
locals().update(cmaps)


# Color vision deficiencies shown by `show_cmaps(cvd=True)`: label -> colorspacious name
_cvd_types = {
    "Protanopia": "protanomaly",
    "Deuteranopia": "deuteranomaly",
    "Tritanopia": "tritanomaly",
}


def simulate_cvd(cmap, cvd_type, severity=100):
    """
    Return a colormap as it is seen with a color vision deficiency.

    The simulation follows Machado et al. (2009), as implemented in the
    colorspacious package, which must be installed
    (``pip install cmglaciology[cvd]``).

    Parameters
    ----------
    cmap : str or Colormap
        The colormap, or the name of one, such as ``"cmg.speed"``.
    cvd_type : str
        ``"protanomaly"`` (red), ``"deuteranomaly"`` (green) or
        ``"tritanomaly"`` (blue).
    severity : float
        From 0 (normal vision) to 100 (the color is not seen at all:
        protanopia, deuteranopia or tritanopia). Default is 100.
    """
    try:
        from colorspacious import cspace_convert
    except ImportError as exc:
        raise ImportError(
            "Simulating color vision deficiencies needs the colorspacious package. "
            "Install it with: python -m pip install cmglaciology[cvd]"
        ) from exc
    from matplotlib.colors import ListedColormap

    if cvd_type not in _cvd_types.values():
        raise ValueError(
            f"cvd_type must be one of {sorted(_cvd_types.values())}, not {cvd_type!r}"
        )

    cmap = matplotlib.colormaps[cmap] if isinstance(cmap, str) else cmap
    rgb = cmap(np.linspace(0, 1, cmap.N))[:, :3]
    cvd_space = {"name": "sRGB1+CVD", "cvd_type": cvd_type, "severity": severity}
    simulated = np.clip(cspace_convert(rgb, cvd_space, "sRGB1"), 0, 1)
    return ListedColormap(simulated, name=f"{cmap.name}_{cvd_type}")


def show_cmaps(*, figwidth=8, cvd=False):
    """
    Plot all available colormaps, grouped by type.

    With ``cvd=True``, each colormap is also shown as it is seen with
    protanopia, deuteranopia and tritanopia, see `simulate_cvd`.
    """
    x = np.linspace(0, 1, 256)[np.newaxis, :]

    groups = (
        ("Sequential", _cmap_names_sequential),
        ("Topographic", _cmap_names_topographic),
    )
    names = [(group_name, name) for group_name, group in groups for name in group]

    # One column per kind of vision; normal vision only unless cvd is set
    columns = {"Normal vision": None}
    if cvd:
        columns |= _cvd_types

    hrow = 0.7  # size of cmap row, including its label
    htitle = 0.3 if cvd else 0.0  # room for the column titles
    height = hrow * len(names) + htitle
    fig, axs = plt.subplots(
        len(names),
        len(columns),
        figsize=(figwidth, height),
        gridspec_kw=dict(
            left=0.01,
            right=0.99,
            top=0.99 - htitle / height,
            bottom=0.15 * hrow * len(names) / height,
            hspace=1.0,
            wspace=0.04,
        ),
        squeeze=False,
    )
    fig.set_layout_engine("none")

    for k, (row, (group_name, cmap_name)) in enumerate(zip(axs, names)):
        for ax, (title, cvd_type) in zip(row, columns.items()):
            cmap = cmaps[cmap_name]
            if cvd_type is not None:
                cmap = simulate_cvd(cmap, cvd_type)
            ax.set_axis_off()
            ax.imshow(x, cmap=cmap, aspect="auto")
            if cvd and k == 0:
                ax.set_title(title, size=12, color="0.2")
        row[0].text(
            0.0,
            -0.1,
            cmap_name,
            size=12,
            color="0.2",
            va="top",
            transform=row[0].transAxes,
        )
        row[-1].text(
            1.0,
            -0.1,
            group_name,
            size=12,
            color="0.4",
            style="italic",
            va="top",
            ha="right",
            transform=row[-1].transAxes,
        )

    return fig


if __name__ == "__main__":
    show_cmaps()
    plt.savefig("colormaps.png", dpi=200)

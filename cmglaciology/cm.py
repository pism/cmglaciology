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
    "dem_ak",
    "dem_gris",
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


def show_cmaps(*, figwidth=8):
    """
    Plot all available colormaps, grouped by type.
    """
    x = np.linspace(0, 1, 256)[np.newaxis, :]

    groups = (
        ("Sequential", _cmap_names_sequential),
        ("Topographic", _cmap_names_topographic),
    )
    names = [(group_name, name) for group_name, group in groups for name in group]

    hrow = 0.7  # size of cmap row, including its label
    fig, axs = plt.subplots(
        len(names),
        1,
        figsize=(figwidth, hrow * len(names)),
        gridspec_kw=dict(left=0.01, right=0.99, top=0.99, bottom=0.15, hspace=1.0),
        squeeze=False,
    )
    fig.set_layout_engine("none")

    for ax, (group_name, cmap_name) in zip(axs.flat, names):
        ax.set_axis_off()
        ax.imshow(x, cmap=cmaps[cmap_name], aspect="auto")
        ax.text(
            0.0,
            -0.1,
            cmap_name,
            size=12,
            color="0.2",
            va="top",
            transform=ax.transAxes,
        )
        ax.text(
            1.0,
            -0.1,
            group_name,
            size=12,
            color="0.4",
            style="italic",
            va="top",
            ha="right",
            transform=ax.transAxes,
        )

    return fig


if __name__ == "__main__":
    show_cmaps()
    plt.savefig("colormaps.png", dpi=200)

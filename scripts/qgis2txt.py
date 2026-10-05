"""
Convert QGIS colormap export files into the plain RGB tables shipped in
``cmglaciology/cmaps``.

The QGIS files in ``qgis/`` are the source of truth. Each one is linearly
interpolated between its color stops and sampled at 256 evenly spaced levels,
giving a ``256 x 3`` table of RGB values in ``[0, 1]`` -- the same layout used
by cmcrameri (https://github.com/callumrollo/cmcrameri).

Examples
--------
    python scripts/qgis2txt.py                 # convert everything in qgis/
    python scripts/qgis2txt.py path/to/my.txt  # convert selected files
"""

import argparse
from pathlib import Path

import numpy as np
from matplotlib.colors import LinearSegmentedColormap

N_LEVELS = 256

repo_dir = Path(__file__).parent.parent.absolute()
qgis_dir = repo_dir / "qgis"
cmap_data_dir = repo_dir / "cmglaciology" / "cmaps"


def qgis2rgb(filename, num_levels=N_LEVELS):
    """
    Read a colormap exported from a QGIS raster layer and return an
    ``(num_levels, 3)`` array of RGB values in ``[0, 1]``.

    Rows of a QGIS export are ``value,red,green,blue,alpha,label``. The stops
    are placed according to ``value``; alpha and label are ignored.
    """
    data = np.loadtxt(filename, skiprows=2, delimiter=",", usecols=(0, 1, 2, 3))
    values = data[:, 0]
    values_scaled = (values - values.min()) / (values.max() - values.min())
    colors_scaled = data[:, 1:] / 255.0
    cmap = LinearSegmentedColormap.from_list(
        Path(filename).stem, list(zip(values_scaled, colors_scaled)), N=num_levels
    )
    return cmap(np.linspace(0, 1, num_levels))[:, :3]


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "files",
        nargs="*",
        type=Path,
        metavar="FILE",
        help=f"QGIS colormap export file(s) to convert (default: all *.txt in {qgis_dir}).",
    )
    parser.add_argument(
        "-o",
        "--outdir",
        type=Path,
        default=cmap_data_dir,
        metavar="DIR",
        help="Directory the RGB tables are written to, as <name>.txt (default: %(default)s).",
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    paths = args.files or sorted(qgis_dir.glob("*.txt"))
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        raise SystemExit(f"File(s) not found: {', '.join(missing)}")
    args.outdir.mkdir(parents=True, exist_ok=True)
    for path in paths:
        out = args.outdir / f"{path.stem}.txt"
        np.savetxt(out, qgis2rgb(path), fmt="%.6f")
        print(f"{path} -> {out}")


if __name__ == "__main__":
    main()

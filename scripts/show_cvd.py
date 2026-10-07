"""
Plot the colormaps as they are seen with a color vision deficiency.

Draws every colormap for normal vision, protanopia, deuteranopia and
tritanopia with ``cmglaciology.show_cmaps(cvd=True)`` and saves the figure
that is shown at the bottom of the README.

Needs the colorspacious package: ``python -m pip install cmglaciology[cvd]``.

Examples
--------
    python scripts/show_cvd.py                # write cmglaciology/colormaps_cvd.png
    python scripts/show_cvd.py -o my_cvd.png  # write somewhere else
"""

import argparse
import sys
from pathlib import Path

repo_dir = Path(__file__).parent.parent.absolute()
sys.path.insert(0, str(repo_dir))

from cmglaciology import show_cmaps  # noqa: E402

default_outfile = repo_dir / "cmglaciology" / "colormaps_cvd.png"


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0].strip())
    parser.add_argument(
        "-o", "--outfile", type=Path, default=default_outfile, help="Figure to write."
    )
    parser.add_argument(
        "--dpi", type=int, default=200, help="Resolution of the figure."
    )
    options = parser.parse_args()

    fig = show_cmaps(cvd=True, figwidth=12)
    fig.savefig(options.outfile, dpi=options.dpi)
    print(f"Wrote {options.outfile}")


if __name__ == "__main__":
    main()

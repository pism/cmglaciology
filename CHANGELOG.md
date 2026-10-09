# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [PEP 440](https://www.python.org/dev/peps/pep-0440/)
and uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.1]

### Added
- Example visualiation of Kennicott Glacier, Alaska.

## [0.2.0]

### Added
- `show_cmaps(cvd=True)` also draws every colormap as it is seen with protanopia, deuteranopia and tritanopia. `show_cmaps()` is unchanged.
- `cmglaciology.simulate_cvd(cmap, cvd_type, severity=100)` returns a colormap as it is seen with a color vision deficiency.
- The `cvd` extra installs colorspacious, which does the simulation: `python -m pip install "cmglaciology[cvd]"`.
- `scripts/show_cvd.py` makes `cmglaciology/colormaps_cvd.png`, which is shown at the bottom of the README.

## [0.1.1]

### Added
- A GitHub Actions workflow that builds the package and publishes it to PyPI when a version is tagged.

### Fixed
- The colormap overview in the README is linked by its full URL, so it also shows on the PyPI project page.

## [0.1.0]

### Added
- The colormaps `speed`, `akbathtopo`, `aktopo`, `grisbathtopo` and `gristopo`, as `cmglaciology.cm.<name>` and registered with Matplotlib as `cmg.<name>` on `import cmglaciology`. Every colormap has a reversed version, `<name>_r`.
- `cmglaciology.show_cmaps()` draws all colormaps, grouped by type.
- `scripts/qgis2txt.py` converts QGIS color map export files (kept in `qgis/`) into the 256-level RGB tables in `cmglaciology/cmaps/`. `-o/--outdir` writes them elsewhere.
- GitHub Actions workflows for testing, checking that this changelog is updated, tagging versions and creating releases, and pre-commit hooks.
- The package layout, the loading and registration code and the tests are adapted from [cmcrameri](https://github.com/callumrollo/cmcrameri) by Callum Rollo.

### Changed
- `dem_ak` is now called `akbathtopo` and `dem_gris` is now called `grisbathtopo`. The colors are unchanged.
- The version number is computed from the git tags by `setuptools_scm`.

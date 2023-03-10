# napari-pos-adjust

[![License BSD-3](https://img.shields.io/pypi/l/napari-pos-adjust.svg?color=green)](https://github.com/RebootVanChild/napari-pos-adjust/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/napari-pos-adjust.svg?color=green)](https://pypi.org/project/napari-pos-adjust)
[![Python Version](https://img.shields.io/pypi/pyversions/napari-pos-adjust.svg?color=green)](https://python.org)
[![tests](https://github.com/RebootVanChild/napari-pos-adjust/workflows/tests/badge.svg)](https://github.com/RebootVanChild/napari-pos-adjust/actions)
[![codecov](https://codecov.io/gh/RebootVanChild/napari-pos-adjust/branch/main/graph/badge.svg)](https://codecov.io/gh/RebootVanChild/napari-pos-adjust)
[![napari hub](https://img.shields.io/endpoint?url=https://api.napari-hub.org/shields/napari-pos-adjust)](https://napari-hub.org/plugins/napari-pos-adjust)

Manually adjust pos of 3D images.

----------------------------------

This [napari] plugin was generated with [Cookiecutter] using [@napari]'s [cookiecutter-napari-plugin] template.

<!--
Don't miss the full getting started guide to set up your new package:
https://github.com/napari/cookiecutter-napari-plugin#getting-started

and review the napari docs for plugin developers:
https://napari.org/stable/plugins/index.html
-->

## Installation

You can install `napari-pos-adjust` via [pip]:

    pip install napari-pos-adjust



To install latest development version :

    pip install git+https://github.com/RebootVanChild/napari-pos-adjust.git

## Usage

Please load in image layers before opening this plugin.<br>
Use tissue block to select the image layer to operate on.<br>
Load in previous transformation with "browse" and "apply".<br>
Drag sliders to adjust translation and rotation.<br>
Press "save transformation to file" to save it as a csv file.


## Contributing

Contributions are very welcome. Tests can be run with [tox], please ensure
the coverage at least stays the same before you submit a pull request.

## License

Distributed under the terms of the [BSD-3] license,
"napari-pos-adjust" is free and open source software

## Issues

If you encounter any problems, please [file an issue] along with a detailed description.

[napari]: https://github.com/napari/napari
[Cookiecutter]: https://github.com/audreyr/cookiecutter
[@napari]: https://github.com/napari
[MIT]: http://opensource.org/licenses/MIT
[BSD-3]: http://opensource.org/licenses/BSD-3-Clause
[GNU GPL v3.0]: http://www.gnu.org/licenses/gpl-3.0.txt
[GNU LGPL v3.0]: http://www.gnu.org/licenses/lgpl-3.0.txt
[Apache Software License 2.0]: http://www.apache.org/licenses/LICENSE-2.0
[Mozilla Public License 2.0]: https://www.mozilla.org/media/MPL/2.0/index.txt
[cookiecutter-napari-plugin]: https://github.com/napari/cookiecutter-napari-plugin

[file an issue]: https://github.com/RebootVanChild/napari-pos-adjust/issues

[napari]: https://github.com/napari/napari
[tox]: https://tox.readthedocs.io/en/latest/
[pip]: https://pypi.org/project/pip/
[PyPI]: https://pypi.org/

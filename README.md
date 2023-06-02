# surplus

plus code to iOS-Shortcuts-like shareable text

- Installing
- Usage
- Licence

```text
$ surplus 6PH59R3J+R9
surplus version 1.0.0
Thomson Plaza
301 Upper Thomson Road, Bishan
574408
Singapore
```

```python
>>> import surplus
>>> surplus.surplus("6PH58RPQ+JW")
(True, 'Caldecott Stn Exit 4\nToa Payoh Link\n298106\nSingapore')
```

## Installing

Install surplus directly from GitHub using pip:

```text
pip install git+https://github.com/markjoshwel/surplus
```

## Usage

```text
usage: surplus [-h] [-d] pluscode

plus code to iOS-Shortcuts-like shareable text

positional arguments:
  pluscode     full-length plus code including area code, e.g.: 6PH58QMF+FX

options:
  -h, --help   show this help message and exit
  -d, --debug  prints lat, long and reverser response dict to stderr
```

## Developing

Prerequisites:

- [Python >=3.10](https://www.python.org/)
- [Poetry](https://python-poetry.org/)

Alternatively, use [devbox](https://get.jetpack.io/devbox) for a hermetic development environment powered by [Nix](https://nixos.org/).

```text
devbox shell    # skip this if you aren't using devbox
poetry install
poetry shell
```

## Licence

surplus is free and unencumbered software released into the public domain.
For more information, please refer to the [UNLICENCE](UNLICENCE), <http://unlicense.org/> or the Python module docstring.

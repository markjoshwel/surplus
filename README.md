# surplus

Plus Code to iOS-Shortcuts-like shareable text

- [Installing](#installing)
- [Usage](#usage)
  - [Command-line Interface](#command-line-interface)
  - [API Reference](#api-reference)
    - [surplus.surplus()](#surplussurplus)
    - [surplus.parse_query()](#surplusparse_query)
    - [surplus.Localcode](#surpluslocalcode)
    - [surplus.Latlong](#surpluslatlong)
- [Developing](#developing)
- [The format is wrong/different!](#the-format-is-wrongdifferent)
- [Licence](#licence)

```text
$ surplus 9R3J+R9 Singapore
surplus version 1.1.0
Thomson Plaza
301 Upper Thomson Road, Bishan
574408
Singapore
```

```python
>>> from surplus import surplus, Localcode
>>> Localcode(code="8RPQ+JW", locality="Singapore").full_length()
(True, '6PH58RPQ+JW')
>>> surplus("6PH58RPQ+JW")
(True, 'Caldecott Stn Exit 4\nToa Payoh Link\n298106\nSingapore')
```

## Installing

Install surplus directly from GitHub using pip:

```text
pip install git+https://github.com/markjoshwel/surplus
```

## Usage

### Command-line Interface

```text
usage: surplus [-h] [-d] query

Plus Code to iOS-Shortcuts-like shareable text

positional arguments:
  query        full-length Plus Code (6PH58QMF+FX), local codes (8QMF+FX Singapore), or latlong (1.3336875, 103.7749375)

options:
  -h, --help   show this help message and exit
  -d, --debug  prints lat, long and reverser response dict to stderr
```

### API Reference

#### `surplus.surplus()`

pluscode to shareable text conversion function

- signature  

  ```python
  def surplus(
      query: str | Localcode | Latlong,
      reverser: typing.Callable = geopy.geocoders.Nominatim(user_agent="surplus").reverse,
      debug: bool = False,
  ) -> tuple[bool, str]:
    ...
  ```

- arguments

  - `query: str | surplus.Localcode | surplus.Latlong`  
      str - normal longcode (6PH58QMF+FX)
      surplus.Localcode - shortcode with locality (8QMF+FX Singapore)
      surplus.Latlong - latlong

  - `reverser: typing.Callable = geopy.geocoders.Nominatim(user_agent="surplus").reverser`  
      latlong to location function, accesses a dict from .raw attribute of return object
      function should be able to take a string with two floats and return a `geopy.Location`-like object (None checking is done)

      ```python
      # code used by surplus
      location: dict[str, Any] = reverser(f"{lat}, {lon}").raw
      ```

      dict should be similar to [nominatim raw dicts](https://nominatim.org/release-docs/latest/api/Output/#addressdetails)

  - `debug: bool = False`  
      prints lat, long and reverser response dict to stderr

- returns `tuple[bool, str]`  

  - `(True, <str>)`  
      conversion was successful, str is resultant text  
  - `(False, <str>)`  
      conversion failed, str is error message

---

#### `surplus.parse_query()`

function that parses a string Plus Code, local code or latlong into a str, surplus.Localcode or surplus.Latlong respectively

- signature:

    ```python
    def parse_query(
      query: str, debug: bool = False
    ) -> tuple[bool, str | Localcode | Latlong]:
    ```

- arguments:

  - `query: str`  
    string Plus Code, local code or latlong

- returns `tuple[bool, str | Localcode | Latlong]`

  - `(True, <str | Localcode | Latlong>)`  
      conversion was successful, second element is result
  - `(False, <str>)`  
      conversion failed, str is error message

---

#### `surplus.Localcode`

`typing.NamedTuple` representing short Plus Code with locality

- parameters:

  - `code: str`
      Plus Code - e.g.: "8QMF+FX"
  - `locality: str`
      e.g.: "Singapore"

---

##### `surplus.Localcode.full_length()`

method that calculates full-length Plus Code using locality

- signature:

    ```python
    def full_length(
        self, geocoder: Callable = Nominatim(user_agent="surplus").geocode
    ) -> tuple[bool, str]:
    ```

- arguments:

  - `geocoder: typing.Callable = geopy.geocoders.Nominatim(user_agent="surplus").geocode`  
    place/locality to location function, accesses .longitude and .latitude if returned object is not None

- returns:

  - `(True, <str>)`  
      conversion was successful, str is resultant Plus Code  
  - `(False, <str>)`  
      conversion failed, str is error message

---

#### `surplus.Latlong`

`typing.NamedTuple` representing a pair of latitude and longitude coordinates

- parameters:

  - `lat: float`  
      latitudinal coordinate
  - `long: float`  
      longitudinal coordinate

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

## The format is wrong/different!

If surplus generates wrong text for a particular Plus Code,
[submit an issue](https://github.com/markjoshwel/surplus/issues/new). 

Ensure you detail the following:

1. The erroneous Plus Code, local code or latlong, or a similar coordinate that reproduces the same error

2. Output from the terminal, with `--debug` enabled or `debug=True`

3. How it should look like instead

## Licence

surplus is free and unencumbered software released into the public domain.
For more information, please refer to the [UNLICENCE](UNLICENCE), <http://unlicense.org/> or the Python module docstring.

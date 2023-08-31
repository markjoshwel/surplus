# surplus

surplus is a Python script to convert
[Google Map Plus Codes](https://maps.google.com/pluscodes/)
to iOS Shortcuts-like human text.

- [installation](#installation)
- [command-line usage](#command-line-usaage)
- [developer's guide](#developers-guide)
  - [api reference](#api-reference)
- [contributor's guide](#contributors-guide)
  - [reporting incorrect output](#reporting-incorrect-output)
    - [the reporting process](#the-reporting-process)
    - [what counts as "incorrect"](#what-counts-as-incorrect)
- [output technical details](#the-technical-details-of-surpluss-output)
- [licence](#licence)

```text
$ surplus 9R3J+R9 Singapore
surplus version 1.1.3
Thomson Plaza
301 Upper Thomson Road
Sin Ming, Bishan
574408
Central, Singapore
```

```python
>>> from surplus import surplus, Localcode
>>> Localcode(code="8RPQ+JW", locality="Singapore").full_length()
(True, '6PH58RPQ+JW')
>>> surplus("6PH58RPQ+JW")
(True, 'Caldecott Stn Exit 4\nToa Payoh Link\n298106\nCentral, Singapore')
```

## installation

install surplus directly from the repository using pip:

```text
pip install git+https://github.com/markjoshwel/surplus
```

## command-line usage

```text
usage: surplus [-h] [-d] [-v] [query ...]

Plus Code to iOS-Shortcuts-like shareable text

positional arguments:
  query          full-length Plus Code (6PH58QMF+FX),
                 local code (8QMF+FX Singapore), or
                 latlong (1.3336875, 103.7749375)

options:
  -h, --help     show this help message and exit
  -d, --debug    prints lat, long and reverser
                 response dict to stderr
  -v, --version  prints version information to stderr
                 and exits
```

## developer's guide

prerequisites:

- [Python >=3.10](https://www.python.org/)
- [Poetry](https://python-poetry.org/)

alternatively, use [devbox](https://get.jetpack.io/devbox) for a hermetic development environment powered by [Nix](https://nixos.org/).

```text
devbox shell    # skip this if you aren't using devbox
poetry install
poetry shell
```

## contributor's guide

1. fork the repository and branch off from the `future` branch
2. make and commit your changes!
3. pull in any changes from `future`, and resolve any conflicts, if any
4. **commit your copyright waiver** (_see below_)
5. submit a pull request (_or mail in a diff_)

when contributing your first changes, please include an empty commit for a copyright
waiver using the following message (replace 'Your Name' with your name or nickname):

```
Your Name Copyright Waiver

I dedicate any and all copyright interest in this software to the
public domain.  I make this dedication for the benefit of the public at
large and to the detriment of my heirs and successors.  I intend this
dedication to be an overt act of relinquishment in perpetuity of all
present and future rights to this software under copyright law.
```

the command to create an empty commit is `git commit --allow-empty`

### reporting incorrect output

> **Note**  
> this section is independent from the rest of the contributing section.

different output from the iOS Shortcuts app is expected, however incorrect output is not.

#### the reporting process

open an issue in the
[repositories issue tracker](https://github.com/markjoshwel/surplus/issues/new),
and include the following:

1. ensure that your issue is not an error of incorrect data returned by your reverser 
   function, which by default is OpenStreetMap Nominatim.  
   (_don't know what the above means? then using the default reverser._)

   also look at "[what counts as 'incorrect'](#what-counts-as-incorrect)" before
   moving on.

2. include the erroneous Plus Code, local code, latitude and longitude coordinate, or 
   query string.

3. include output from the teminal with the
   [`--debug` flag](#command-line-usage) passed to the surplus CLI or with 
   `debug=True` set in function calls.

   > **Note**  
   > if you are using custom stdout and stderr parameters and redirecting output,
   > include that instead.

4. how it should look like instead, with reasoning if the error not obvious. (e.g., missing details)

   for reference, see how the following issues were written:

   - [issue #4: "Incorrect format: repeated lines"](https://github.com/markjoshwel/surplus/issues/4)
   - [issue #6: "Incorrect format: missing details"](https://github.com/markjoshwel/surplus/issues/6)
   - [issue #12: "Incorrect format: State before county"](https://github.com/markjoshwel/surplus/issues/12)

#### what counts as "incorrect"

- **example 1**

  - iOS Shortcuts Output

    ```
    Plaza Singapura
    68 Orchard Rd
    238839
    Singapore
    ```

  - surplus Output

    ```
    Plaza Singapura
    68 Orchard Road
    Museum
    238839
    Central, Singapore
    ```

  this _should not_ be reported as incorrect, as the only difference between the two is
  that surplus displays more information.

  note: for singaporean readers, "Musuem" here is correct as it refers to the
  [Museum planning area](https://en.wikipedia.org/wiki/Museum_Planning_Area),
  in which Plaza Singapura is located in.

other examples that _should not_ be reported are:

- name of place is incorrect/different

  this may be due to incorrect data from the geolocator function, which is OpenStreetMap Nominatim by default.
  in the case of Nominatim, it means that there the data on OpenStreetMap is incorrect.

  (_if so, then consider updating OpenStreetMap to help not just you, but other surplus
  and OpenStreetMap users!_)

you should report when the output does not make logical sense, or something similar 
wherein the output of surplus is illogical to read or is not correct in the traditional
sense of a correct address.

see the linked issues in [the reporting process](#the-reporting-process) for examples 
of incorrect outputs.

## the technical details of surplus's output

```
$ s+ 8QJF+RP --debug
surplus version 1.1.3, debug mode
debug: args.query='8QJF+RP Singapore'
debug: squery=['8QJF+RP', 'Singapore']
debug: pcode='8QJF+RP', locality='Singapore'
debug: lat=1.3320625, lon=103.7743125
debug: location={...}
debug: seen_names=['Ngee Ann Polytechnic', '', '', '']
debug: d=''     _dvtm4=[False, False, False, False]     _dvcm4=[False, False, False, False]
debug: d='Bukit Timah'  _dvtm4=[True, True, True, True] _dvcm4=[True, True, True, True]
debug: d='Singapore'    _dvtm4=[True, True, False, True]        _dvcm4=[True, True, True, True]
0       Ngee Ann Polytechnic
1
2
3       535 Clementi Road
4       Bukit Timah
5       599489
6       Northwest, Singapore
Ngee Ann Polytechnic
535 Clementi Road
Bukit Timah
599489
Northwest, Singapore
```

variables

- **variable `args.query`**

  space-combined query given by user, comes from
  [`argparse.ArgumentParser.parse_args`](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.parse_args)

- **variable `squery`**

  query split by comma

  ```text
  $ s+ 77Q4+7X Austin, Texas, USA
       --------------------------
       query

  squery -> ['77Q4+7X', 'Austin', 'Texas', 'USA']
  ```

- **variables `pcode` and `locality`**

  (_only shown if the query is a local code, not shown on full-length plus codes, 
  latlong coordinates or string queries_)

  represents the plus code and locality portions of a
  [shortened plus code](https://en.wikipedia.org/wiki/Open_Location_Code#Common_usage_and_shortening)
  (_referred to as a "short/local code" in the codebase_) respectively.

- **variables `lat` and `lon`**

  (_only shown if the query is a plus code_)

  the latitude longitude coordinates derived from the plus code.

- **variable `location`**

  the response dictionary from the reverser passed to
  [`surplus.surplus()`](#surplussurplus)

- **variable `seen_names`**

  a list of unique names/elements found in certain nominatim keys used in final output
  lines 0-3.

- **variables for seen name checks**

  the variables come from a check to reduce repeated elements found in `seen_names`.

  - **variable `d`**

    current element in the iteration of the final output line 4 (general regional 
    location) nominatim keys

  - **variable `_dvmt4`**

    list used in an `all()` check to see if the current nominatim key (variable `d`) can
    be wholly found in any of the seen names, in the general regional location, or in 
    the road name.

    reasoning is, if the previous lines wholly state the general regional location of the
    query, there is no need to restate it.

    ```
    # psuedocode
    _dvtm4 = [
        d != "",
        d not in road,
        d not in [output line 4 (general regional location) nominatim keys],
        any(_dvcm4),
    ]
    ```

  - **variable `_dvcm4`**

    list used in an `any()` check to see if the current nominatim key (variable `d`) can
    be wholly found in any of the seen names.

    ```python
    _dvcm4 = [True if (d not in sn) else False for sn in seen_names]
    ```

breakdown of each output line, accompanied by their nominatim key:

```
0       name of a place
1       building name
2       highway name
3       block/house/building number, house name, road
4       general regional location
5       postal code
6       general global information
```

0. **name of a place**

   (_usually important places or landmarks_)

   - examples

     ```
     The University of Queensland
     Ngee Ann Polytechnic
     Botanic Gardens
     ```

   - nominatim keys

     ```
     emergency, historic, military, natural, landuse, place, railway, man_made, 
     aerialway, boundary, amenity, aeroway, club, craft, leisure, office, mountain_pass, 
     shop, tourism, bridge, tunnel, waterway
     ```

1. **building name**

   - examples

     ```
     Novena Square Office Tower A
     Visitor Centre
     ```

   - nominatim keys

     ```
     building
     ```

2. **highway name**

   - examples

     ```
     Marina Coastal Expressway
     Lornie Highway
     ```

   - nominatim keys

     ```
     highway
     ```

3. **block/house/building number, house name, road**

   - examples

     ```
     131 Toa Payoh Rise
     535 Clementi Road
     Macquarie Street
     Braddell Road
     ```

   - nominatim keys

     ```
     house_number, house_name, road
     ```

4. **general regional location**

   - examples

     ```
     St Lucia, Greater Brisbane
     The Drag, Austin
     Toa Payoh Crest
     ```

   - nominatim keys

     ```
     residential, neighbourhood, allotments, quarter, city_district, district, borough, 
     suburb, subdivision, municipality, city, town, village
     ```

5. **postal code**

   - examples

     ```
     310131
     78705
     4066
     ```

   - nominatim key

     ```
     postcode
     ```

6. **general global information**

   - examples

     ```
     Travis County, Texas, United States
     Southeast, Singapore
     Queensland, Australia
     ```

   - nominatim keys

     ```
     region, county, state, state_district, country, continent
     ```

## api reference

### `surplus.surplus()`

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
    - str  
        normal longcode (6PH58QMF+FX)  
    - [`surplus.Localcode`](#surpluslocalcode)  
        shortcode with locality (8QMF+FX Singapore)  
    - [`surplus.Latlong`](#surpluslatlong)  
        latlong

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
      conversion succeeded, second element is the resultant string  
  - `(False, <str>)`  
      conversion failed, second element is an error message string

---

### `surplus.parse_query()`

function that parses a string Plus Code, local code or latlong into a str, [`surplus.Localcode`](#surpluslocalcode) or [`surplus.Latlong`](#surpluslatlong) respectively

- signature:

    ```python
    def parse_query(
      query: str, debug: bool = False
    ) -> tuple[typing.Literal[True], str | Localcode | Latlong] | tuple[typing.Literal[False], str]:
    ```

- arguments:

  - `query: str`  
    string Plus Code, local code or latlong

- returns `tuple[typing.Literal[True], str | Localcode | Latlong] | tuple[typing.Literal[False], str]`

  - `(True, <str | surplus.Localcode | surplus.Latlong>)`  
      conversion succeeded, second element is resultant Plus code string, [`surplus.Localcode`](#surpluslocalcode) or [`surplus.Latlong`](#surpluslatlong)
  - `(False, <str>)`  
      conversion failed, second element is an error message string

### `surplus.handle_query()`

function that gets returns a [surplus.Latlong](#surpluslatlong) from a Plus Code string, [`surplus.Localcode`](#surpluslocalcode) or [`surplus.Latlong`](#surpluslatlong) object.  
used after [`surplus.parse_query()`](#surplusparse_query).

- signature:

    ```python
    def handle_query(
        query: str | Localcode | Latlong, debug: bool = False
    ) -> tuple[typing.Literal[True], Latlong] | tuple[typing.Literal[False], str]:
    ```

- arguments:

  - `query: str | Localcode | Latlong`  
    - str  
        normal longcode (6PH58QMF+FX)  
    - [`surplus.Localcode`](#surpluslocalcode)  
        shortcode with locality (8QMF+FX Singapore)  
    - [`surplus.Latlong`](#surpluslatlong)  
        latlong

- returns `tuple[typing.Literal[True], Latlong] | tuple[typing.Literal[False], str]`  
  - `(True, <surplus.Latlong>)`  
    conversion succeeded, second element is a [`surplus.Latlong`](#surpluslatlong)
  - `(False, <str>)` 
    conversion failed, second element is an error message string

### `surplus.Localcode`

`typing.NamedTuple` representing short Plus Code with locality

- parameters:

  - `code: str`
      Plus Code - e.g.: `"8QMF+FX"`
  - `locality: str`
      e.g.: `"Singapore"`

#### `surplus.Localcode.full_length()`

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
      conversion succeeded, second element is the resultant Plus Code string  
  - `(False, <str>)`  
      conversion failed, second element is an error message string

#### `surplus.Latlong`

`typing.NamedTuple` representing a pair of latitude and longitude coordinates

- parameters:

  - `lat: float`  
      latitudinal coordinate
  - `long: float`  
      longitudinal coordinate

## licence

surplus is free and unencumbered software released into the public domain. for more
information, please refer to the [UNLICENCE](/UNLICENCE), <https://unlicense.org>, or the
python module docstring.

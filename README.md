# surplus

> **Warning**
>
> **this is surplus `2.0.0`.**  
> surplus is being rewritten to better incorporate with
> [sandplus](https://github.com/markjoshwel/sandplus.git).
> sandplus is surplus's Android application accompaniment, written in Kotlin with Jetpack
> Compose.
>
> you are on the `future` branch. if you see this warning, that means code is not
> finalised and ready to be used.  
> want the old, stable, working codebase? see the
> [`main`](https://github.com/markjoshwel/surplus/tree/main) branch.

surplus is a Python script to convert
[Google Maps Plus Codes](https://maps.google.com/pluscodes/)
to iOS Shortcuts-like shareable text.

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
TODO CLI DEMO
```

```python
>>> from surplus import surplus, Localcode
>>> Localcode(code="8RPQ+JW", locality="Singapore").full_length()
TODO API DEMO
```

## installation

> **Note**  
> python 3.11 or later is required due to a bug in earlier versions.
> [(python/cpython#88089)](https://github.com/python/cpython/issues/88089)

install surplus directly from the repository using pip:

```text
pip install git+https://github.com/markjoshwel/surplus.git@future
```

## command-line usage

```text
usage: surplus [-h] [-d] [-v] [-c {pluscode,localcode,latlong,string}]
               [query ...]

Google Maps Plus Code to iOS Shortcuts-like shareable text

positional arguments:
  query                 full-length Plus Code (6PH58QMF+FX), shortened
                        Plus Code/'local code' (8QMF+FX Singapore),
                        latlong (1.3336875, 103.7749375), or string
                        query (e.g., 'Wisma Atria')

options:
  -h, --help            show this help message and exit
  -d, --debug           prints lat, long and reverser response dict to
                        stderr
  -v, --version         prints version information to stderr and exits
  -c {pluscode,localcode,latlong,shareabletext},
  --convert-to {pluscode,localcode,latlong,shareabletext}
                        converts query a specific output type, defaults
                        to 'shareabletext'
```

## developer's guide

prerequisites:

- [Python >=3.11](https://www.python.org/)
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
and do the following:

1. ensure that your issue is not an error of incorrect data returned by your reverser
   function, which by default is OpenStreetMap Nominatim.
   (_don't know what the above means? then you are using the default reverser._)

   also look at the [what counts as "incorrect"](#what-counts-as-incorrect) section
   before moving on.

2. include the erroneous query.
   (_the Plus Code/local code/latlong coord/query string you passed into surplus_)

3. include output from the teminal with the
   [`--debug` flag](#command-line-usage) passed to the surplus CLI or with
   `debug=True` set in function calls.

   > **Note**
   > if you are using the surplus API and have passed custom stdout and stderr parameters
   > to redirect output, include that instead.

4. how it should look like instead, with reasoning if the error is not obvious. (e.g.,
   missing details)

   for reference, see how the following issues were written:

   - [issue #4: "Incorrect format: repeated lines"](https://github.com/markjoshwel/surplus/issues/4)
   - [issue #6: "Incorrect format: missing details"](https://github.com/markjoshwel/surplus/issues/6)
   - [issue #12: "Incorrect format: State before county"](https://github.com/markjoshwel/surplus/issues/12)

#### what counts as "incorrect"

- **example** (correct)

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

**you should report** when the output does not make logical sense, or something similar
wherein the output of surplus is illogical to read or is not correct in the traditional
sense of a correct address.

see the linked issues in [the reporting process](#the-reporting-process) for examples
of incorrect outputs.

## the technical details of surplus's output

```
$ s+ --debug 8QJF+RP Singapore
surplus version 2.0.0, debug mode
debug: behaviour.query=['8QJF+RP', 'Singapore']
debug: portion_plus_code='8QJF+RP', portion_locality='Singapore'
debug: query=Result(value=LocalCodeQuery(code='8QJF+RP', locality='Singapore'), error=None)
debug: latlong.get()=Latlong(latitude=1.3320625, longitude=103.7743125)
debug: location={'amenity': 'Ngee Ann Polytechnic', 'house_number': '535', 'road': 'Clementi Road', 'suburb': 'Bukit Timah', 'city': 'Singapore', 'county': 'Northwest', 'ISO3166-2-lvl6': 'SG-03', 'postcode': '599489', 'country': 'Singapore', 'country_code': 'sg', 'raw': "{...}", 'latitude': '1.33318835', 'longitude': '103.77461234638255'}
debug: seen_names=['Ngee Ann Polytechnic', 'Clementi Road']
debug: _generate_text_line: [True]               -> True   --------  'Ngee Ann Polytechnic'
debug: _generate_text_line: [True]               -> True   --------  '535'
debug: _generate_text_line: [True]               -> True   --------  'Clementi Road'
debug: _generate_text_line: [True, True]         -> True   --------  'Bukit Timah'
debug: _generate_text_line: [False, True]        -> False  filtered  'Singapore'
debug: _generate_text_line: [True]               -> True   --------  '599489'
debug: _generate_text_line: [True]               -> True   --------  'Northwest'
debug: _generate_text_line: [True]               -> True   --------  'Singapore'
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

- **variable `behaviour.query`**

  query split by comma, comes from
  [`argparse.ArgumentParser.parse_args`](https://docs.python.org/3/library/argparse.html#argparse.ArgumentParser.parse_args)

  ```text
  $ s+ 77Q4+7X Austin, Texas, USA
       --------------------------
       query

  behaviour.query -> ['77Q4+7X', 'Austin', 'Texas', 'USA']
  ```

- **variables `portion_plus_code` and `portion_locality`**

  (_only shown if the query is a local code, not shown on full-length plus codes,
  latlong coordinates or string queries_)

  represents the plus code and locality portions of a
  [shortened plus code](https://en.wikipedia.org/wiki/Open_Location_Code#Common_usage_and_shortening)
  (_referred to as a "short/local code" in the codebase_) respectively.

- **variable `query`**

  query is a variable of type `surplus.Result[surplus.Query]`, where `surplus.Query` is
  a TypeAlias of `PlusCodeQuery | LocalCodeQuery | LatlongQuery | StringQuery`.

  this variable is displayed to show what query type
  `surplus.parse_query` has recognised, and if there were any errors
  during query parsing.

- **expression `latlong.get()=`**

  (_only shown if the query is a plus code_)

  the latitude longitude coordinates derived from the plus code.

- **variable `location`**

  the response dictionary from the reverser passed to
  [`surplus.surplus()`](#surplussurplus)

  for more information on what the dictionary should contain or how it should look like,
  see the [playground notebook](playground.ipynb), documentation on surplus.Behaviour or
  the surplus's implementation of the reverser function in `surplus.default_reverser`.

- **variable `seen_names`**

  a list of unique important names found in certain nominatim keys used in final output
  lines 0-3.

- **`_generate_text_line` seen name checks**

  ```text
  #                           filter function boolean list   status    element
  #                           =============================  ========  ======================
  debug: _generate_text_line: [True]               -> True   --------  'Ngee Ann Polytechnic'
  debug: _generate_text_line: [False, True]        -> False  filtered  'Singapore'
  ```

  a check is done on shareable text line 4 keys (`SHAREABLE_TEXT_LINE_4_KEYS` - general
  regional location) to reduce repeated elements found in `seen_names`.

  reasoning is, if an element on line 4 (general regional location) is the exact same as
  a previously seen name, there is no need to include the element.

  - **filter function boolean list**

    `_generate_text_line`, an internal function defined inside `_generate_text` can be
    passed a filter function as a way to filter out certain elements on a line.

    ```python
    # the filter used in _generate_text, for line 4's seen name checks
    filter=lambda ak: [
        # everything here should be True if the element is to be kept
        ak not in general_global_info,
        not any(True if (ak in sn) else False for sn in seen_names),
    ]
    ```

    `general_global_info` is a list of strings containing elements from line 6. (general
    global information)

  - **status**

    what `all(filter(detail))` evaluates to, `filter` being the filter function passed to
    `_generate_text_line` and `detail` being the current element

  - **element**

    the current iteration from iterating through a list of strings containing elements
    from line 4. (general regional location)

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

TODO API REF

## licence

surplus is free and unencumbered software released into the public domain. for more
information, please refer to the [UNLICENCE](/UNLICENCE), <https://unlicense.org>, or the
python module docstring.

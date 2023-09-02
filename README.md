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
- [usage](#usage)
  - [command-line usage](#command-line-usaage)
  - [example api usage](#example-api-usage)
- [developer's guide](#developers-guide)
- [contributor's guide](#contributors-guide)
  - [reporting incorrect output](#reporting-incorrect-output)
    - [the reporting process](#the-reporting-process)
    - [what counts as "incorrect"](#what-counts-as-incorrect)
- [output technical details](#the-technical-details-of-surpluss-output)
- [api reference](#api-reference)
- [licence](#licence)

```text
$ surplus 9R3J+R9 Singapore
surplus version 2.0.0
Thomson Plaza
301 Upper Thomson Road
Sin Ming, Bishan
574408
Central, Singapore
```

## installation

> **Note**  
> python 3.11 or later is required due to a bug in earlier versions.
> [(python/cpython#88089)](https://github.com/python/cpython/issues/88089)

install surplus directly from the repository using pip:

```text
pip install git+https://github.com/markjoshwel/surplus.git@future
```

## usage

### command-line usage

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
  -c {pluscode,localcode,latlong,sharetext},
  --convert-to {pluscode,localcode,latlong,sharetext}
                        converts query a specific output type, defaults
                        to 'sharetext'
```

### example api usage

here are a few examples to get you quickly started using surplus in your own program:

1. let surplus do the heavy lifiting

   ```python
   >>> from surplus import surplus, Behaviour
   >>> result = surplus("Ngee Ann Polytechnic, Singapore", Behaviour())
   >>> result.get()
   'Ngee Ann Polytechnic\n535 Clementi Road\nBukit Timah\n599489\nNorthwest, Singapore'
   ```

2. handle queries seperately

  ```python
  >>> import surplus
  >>> behaviour = surplus.Behaviour("6PH58R3M+F8")
  >>> query = surplus.parse_query(behaviour)
  >>> result = surplus.surplus(query.get(), behaviour)
  >>> result.get()
  'MacRitchie Nature Trail\nCentral Water Catchment\n574325\nCentral, Singapore'
  ```

3. start from a Query object

   ```python
   >>> import surplus
   >>> localcode = surplus.LocalCodeQuery(code="8R3M+F8", locality="Singapore")
   >>> pluscode_str = localcode.to_full_plus_code(geocoder=surplus.default_geocoder).get()
   >>> pluscode = surplus.PlusCodeQuery(pluscode_str)
   >>> result = surplus.surplus(pluscode, surplus.Behaviour())
   >>> result.get()
   'Wisma Atria\n435 Orchard Road\n238877\nCentral, Singapore'
   ```

notes:

- you can change what surplus does by passing in a custom `Behaviour` object.

- most surplus functions return a `Result` object. while you can `.get()` the Result to
  obtain the proper return value, this is dangerous and might raise an exception.

see the [api reference](#api-reference) for more information.

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

for information on surplus's exposed api, see the [api reference](#api-reference).

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

> **Note**  
> this is a breakdown of surplus's output when converting to shareable text.
> when converting to other output types, n

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
  (_referred to as a "local code" in the codebase_) respectively.

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

- [constants](#constants)
- [exception classes](#exception-classes)
- [types](#types)
- [`class Behaviour`](#class-behaviour)
- [`class ConversionResultTypeEnum`](#class-conversionresulttypeenum)
- [`class Result`](#class-result)
  - [`Result.__bool__()`](#result__bool__)
  - [`Result.cry()`](#resultcry)
  - [`Result.get()`](#resultget)
- [`class Latlong`](#class-latlong)
- [`class PlusCodeQuery`](#class-pluscodequery)
- [`class LocalCodeQuery`](#class-localcodequery)
- [`class LatlongQuery`](#class-latlongquery)
- [`class StringQuery`](#class-stringquery)
- [`def surplus()`](#def-surplus)
- [`def parse_query()`](#def-parse_query)
- [`def default_geocoder()`](#def-default_geocoder)
- [`def default_reverser()`](#def-default_reverser)

### constants

- `VERSION: tuple[int, int, int]`

  a tuple of integers representing the version of surplus, in the format
  `[major, minor, patch]`

- `SHAREABLE_TEXT_LINE_0_KEYS: tuple[str, ...]`  
  `SHAREABLE_TEXT_LINE_1_KEYS: tuple[str, ...]`  
  `SHAREABLE_TEXT_LINE_2_KEYS: tuple[str, ...]`  
  `SHAREABLE_TEXT_LINE_3_KEYS: tuple[str, ...]`  
  `SHAREABLE_TEXT_LINE_4_KEYS: tuple[str, ...]`  
  `SHAREABLE_TEXT_LINE_5_KEYS: tuple[str, ...]`  
  `SHAREABLE_TEXT_LINE_6_KEYS: tuple[str, ...]`  

  a tuple of strings containing nominatim keys used in shareable text line 0-6

- `SHAREABLE_TEXT_NAMES: tuple[str, ...]`
  
  a tuple of strings containing nominatim keys used in shareable text line 0-2 and
  special keys in line 3

- `EMPTY_LATLONG: Latlong`  
  a constant for an empty latlong coordinate, with latitude and longitude set to 0.0

### exception classes

- `class SurplusException(Exception)`  
  base skeleton exception for handling and typing surplus exception classes
- `class NoSuitableLocationError(SurplusException)`
- `class IncompletePlusCodeError(SurplusException)`
- `class PlusCodeNotFoundError(SurplusException)`
- `class LatlongParseError(SurplusException)`
- `class EmptyQueryError(SurplusException)`
- `class UnavailableFeatureError(SurplusException)`

### types

#### `Query`

```python
Query: typing.TypeAlias = PlusCodeQuery | LocalCodeQuery | LatlongQuery | StringQuery
```

[type alias](https://docs.python.org/3/library/typing.html#type-aliases) representing
either a
[`PlusCodeQuery`](#class-pluscodequery),
[`LocalCodeQuery`](#class-localcodequery),
[`LatlongQuery`](#class-latlongquery) or
[`StringQuery`](#class-stringquery)

#### `ResultType`

```python
ResultType = TypeVar("ResultType")
```

[generic type](https://docs.python.org/3/library/typing.html#generics) used by
[`Result`](#class-result)

### `class Behaviour`

[`typing.NamedTuple`](https://docs.python.org/3/library/typing.html#typing.NamedTuple) 
representing how surplus operations should behave

attributes

- `query: str | list[str] = ""`  
  original user-passed query string or a list of strings from splitting user-passed query 
  string by spaces

- `geocoder: typing.Callable[[str], Latlong] = default_geocoder`  
  name string to location function, must take in a string and return a
  [`Latlong`](#class-latlong), exceptions are handled by the caller

- `reverser: Callable[[Latlong], dict[str, Any]] = default_reverser`  
  [`Latlong`] object to dictionary function, must take in a string and return a dict. 
  keys found in SHAREABLE_TEXT_LINE_*_KEYS used to access address details are placed 
  top-level in the dict, exceptions are handled by the caller.
  see the [playground notebook](playground.ipynb) for example output

- `stderr: typing.TextIO = sys.stderr`  
  [TextIO-like object](https://docs.python.org/3/library/io.html#text-i-o)
  representing a writeable file.
  defaults to [`sys.stderr`](https://docs.python.org/3/library/sys.html#sys.stderr).

- `stdout: typing.TextIO = sys.stdout`  
  [TextIO-like object](https://docs.python.org/3/library/io.html#text-i-o)
  representing a writeable file.
  defaults to [`sys.stdout`](https://docs.python.org/3/library/sys.html#sys.stdout).

- `debug: bool = False`  
  whether to print debug information to stderr

- `version_header: bool = False`  
  whether to print version information and exit

- `convert_to_type: ConversionResultTypeEnum = ConversionResultTypeEnum.SHAREABLE_TEXT`  
  what type to convert the query to

### `class ConversionResultTypeEnum`

[enum.Enum](https://docs.python.org/3/library/enum.html)
representing what the result type of conversion should be

values

- `PLUS_CODE: str = "pluscode"`
- `LOCAL_CODE: str = "localcode"`
- `LATLONG: str = "latlong"`
- `SHAREABLE_TEXT: str = "sharetext"`

### `class Result`

[`typing.NamedTuple`](https://docs.python.org/3/library/typing.html#typing.NamedTuple) 
representing the result for safe value retrieval

attributes

- `value: ResultType`  
  value to return or fallback value if erroneous

- `error: BaseException | None = None`  
  exception if any

example usage

```python
# do something
def some_operation(path) -> Result[str]:
    try:
        file = open(path)
        contents = file.read()

    except Exception as exc:
        # must pass a default value
        result = Result[str]("", error=exc)

    else:
        result = Result[str](contents)

# call function and handle result
result = some_operation("some_file.txt")

if not result:  # check if the result is erroneous
    # .cry() raises the exception
    # (or returns it as a string error message using string=True)
    result.cry()
    ...

else:
    # .get() raises exception or returns value,
    # but since we checked for errors this is safe
    print(result.get())
```

methods

- [`def __bool__(self) -> bool: ...`](#result__bool__)
- [`def get(self) -> ResultType: ...`](#resultcry)
- [`def cry(self, string: bool = False) -> str: ...`](#resultget)

#### `Result.__bool__()`

method that returns `True` if `self.error` is not `None`

- signature

  ```python
  def __bool__(self) -> bool: ...
  ```

- returns `bool`

#### `Result.cry()`

method that raises `self.error` if is an instance of `BaseException`, returns
`self.error` if is an instance of str, or returns an empty string if `self.error` is None

- signature

  ```python
  def cry(self, string: bool = False) -> str: ...
  ```

- arguments

  - `string: bool = False`  
    if `self.error` is an Exception, returns it as a string error message

- returns `str`

#### `Result.get()`

method that returns `self.value` if Result is non-erroneous else raises error

- signature

  ```python
  def get(self) -> ResultType: ...
  ```

- returns `self.value`

### `class Latlong`

[`typing.NamedTuple`](https://docs.python.org/3/library/typing.html#typing.NamedTuple) 
representing a latitude-longitude coordinate pair

attributes

- `latitude: float`
- `longitude: float`

methods

- [`def __str__(self) -> str: ...`](#latlong__str__)

#### `Latlong.__str__()`

method that returns a comma-and-space-seperated string of `self.latitude` and
`self.longitude`

- signature

  ```python
  def __str__(self) -> str: ...
  ```

- returns `str`

### `class PlusCodeQuery`

[`typing.NamedTuple`](https://docs.python.org/3/library/typing.html#typing.NamedTuple) 
representing a full-length Plus Code (e.g., 6PH58QMF+FX)

attributes

- `code: str`

methods

- [`def to_lat_long_coord(self, ...) -> Result[Latlong]: ...`](#pluscodequeryto_lat_long_coord)
- [`def __str__(self) -> str: ...`](#pluscodequery__str__)

#### `PlusCodeQuery.to_lat_long_coord()`

- signature

  ```python
  def to_lat_long_coord(self, geocoder: Callable[[str], Latlong]) -> Result[Latlong]:
      ...
  ```

- arguments

  - `geocoder: typing.Callable[[str], Latlong]`  
    name string to location function, must take in a string and return a
    [`Latlong`](#class-latlong), exceptions are handled by the caller

- returns [`Result`](#class-result)[`[Latlong]`](#class-latlong)

#### `PlusCodeQuery.__str__()`

method that returns string representation of query

- signature

  ```python
  def __str__(self) -> str: ...
  ```

- returns `str`

### `class LocalCodeQuery`

[`typing.NamedTuple`](https://docs.python.org/3/library/typing.html#typing.NamedTuple) 
representing a
[shortened Plus Code](https://en.wikipedia.org/wiki/Open_Location_Code#Common_usage_and_shortening)
with locality, referred to by surplus as a "local code"

attributes

- `code: str`  
  Plus Code portion of local code, e.g., "8QMF+FX"

- `locality: str`  
  remaining string of local code, e.g., "Singapore"

methods

- [`def to_full_plus_code(self, ...) -> Result[str]: ...`](#localcodequeryto_full_plus_code)
- [`def to_lat_long_coord(self, ...) -> Result[Latlong]: ...`](#localcodequeryto_lat_long_coord)
- [`def __str__(self) -> str: ...`](#localcodequery__str__)

#### `LocalCodeQuery.to_full_plus_code()`

exclusive method that returns a full-length Plus Code as a string

- signature

  ```python
  def to_full_plus_code(self, geocoder: Callable[[str], Latlong]) -> Result[str]:
      ...
  ```

- arguments

  - `geocoder: typing.Callable[[str], Latlong]`  
    name string to location function, must take in a string and return a
    [`Latlong`](#class-latlong), exceptions are handled by the caller

- returns [`Result`](#class-result)`[str]`

#### `LocalCodeQuery.to_lat_long_coord()`

method that returns a latitude-longitude coordinate pair

- signature

  ```python
  def to_lat_long_coord(self, geocoder: Callable[[str], Latlong]) -> Result[Latlong]:
      ...
  ```

- arguments

  - `geocoder: typing.Callable[[str], Latlong]`  
    name string to location function, must take in a string and return a
    [`Latlong`](#class-latlong), exceptions are handled by the caller

- returns [`Result`](#class-result)[`[Latlong]`](#class-latlong)

#### `LocalCodeQuery.__str__()`

method that returns string representation of query

- signature

  ```python
  def __str__(self) -> str: ...
  ```

- returns `str`

### `class LatlongQuery`

[`typing.NamedTuple`](https://docs.python.org/3/library/typing.html#typing.NamedTuple) 
representing a latitude-longitude coordinate pair

attributes

- `latlong: Latlong`

methods

- [`def to_lat_long_coord(self, ...) -> Result[Latlong]: ...`](#latlongqueryto_lat_long_coord)
- [`def __str__(self) -> str: ...`](#latlongquery__str__)

#### `LatlongQuery.to_lat_long_coord()`

method that returns a latitude-longitude coordinate pair

- signature

  ```python
  def to_lat_long_coord(self, geocoder: Callable[[str], Latlong]) -> Result[Latlong]:
      ...
  ```

- arguments

  - `geocoder: typing.Callable[[str], Latlong]`  
    name string to location function, must take in a string and return a
    [`Latlong`](#class-latlong), exceptions are handled by the caller

- returns [`Result`](#class-result)[`[Latlong]`](#class-latlong)

#### `LatlongQuery.__str__()`

method that returns string representation of query

- signature

  ```python
  def __str__(self) -> str: ...
  ```

- returns `str`

### `class StringQuery`

[`typing.NamedTuple`](https://docs.python.org/3/library/typing.html#typing.NamedTuple) 
representing a pure string query

attributes

- `query: str`

methods

- [`def to_lat_long_coord(self, ...) -> Result[Latlong]: ...`](#latlongqueryto_lat_long_coord)
- [`def __str__(self) -> str: ...`](#latlongquery__str__)

#### `LatlongQuery.to_lat_long_coord()`

method that returns a latitude-longitude coordinate pair

- signature

  ```python
  def to_lat_long_coord(self, geocoder: Callable[[str], Latlong]) -> Result[Latlong]:
      ...
  ```

- arguments

  - `geocoder: typing.Callable[[str], Latlong]`  
    name string to location function, must take in a string and return a
    [`Latlong`](#class-latlong), exceptions are handled by the caller

- returns [`Result`](#class-result)[`[Latlong]`](#class-latlong)

#### `LatlongQuery.__str__()`

method that returns string representation of query

- signature

  ```python
  def __str__(self) -> str: ...
  ```

- returns `str`

### `def surplus()`

query to shareable text conversion function

- signature

  ```python
  def surplus(query: Query | str, behaviour: Behaviour) -> Result[str]: ..
  ```

- arguments

  - `query: str | Query`  
    [query object](#query) to convert or string to attempt to query for then convert

  - `behaviour: Behaviour`  
    [surplus behaviour namedtuple](#class-behaviour)

- returns [`Result`](#class-result)`[str]`

### `def parse_query()`

function that parses a query string into a query object

- signature

  ```python
  def parse_query(behaviour: Behaviour) -> Result[Query]: ...
  ```

- arguments

  - `behaviour: Behaviour`  
    [surplus behaviour namedtuple](#class-behaviour)

- returns [`Result`](#class-result)[`[Query]`](#query)

### `def default_geocoder()`

default geocoder for surplus, uses OpenStreetMap Nominatim

> **Note**  
> function is not used by surplus and not directly by the user, but is exposed for
> convenience
>
> pass in a custom function to [Behaviour](#class-behaviour) to override the default 
> reverser
>
> see [Behaviour](#class-behaviour) for more information on what the function does

- signature

  ```python
  def default_geocoder(place: str) -> Latlong:
  ```

### `def default_reverser()`

default reverser for surplus, uses OpenStreetMap Nominatim

> **Note**  
> function is not used by surplus and not directly by the user, but is exposed for
> convenience
>
> pass in a custom function to [Behaviour](#class-behaviour) to override the default 
> reverser
>
> see [Behaviour](#class-behaviour) for more information on what the function does

- signature

  ```python
  def default_reverser(latlong: Latlong) -> dict[str, Any]:
  ```

## licence

surplus is free and unencumbered software released into the public domain. for more
information, please refer to the [UNLICENCE](/UNLICENCE), <https://unlicense.org>, or the
python module docstring.

# surplus

surplus is a Python script to convert
[Google Maps Plus Codes](https://maps.google.com/pluscodes/)
to iOS Shortcuts-like shareable text.

- [installation](#installation)
- [usage](#usage)
  - [command-line usage](#command-line-usage)
  - [example api usage](#example-api-usage)
- [developer's guide](/DEVELOPING.md)
- [contributor's guide](/CONTRIBUTING.md)
- [api reference](#api-reference)
  - [details on the fingerprinted user agent](#details-on-the-fingerprinted-user-agent)
- [licence](#licence)

```text
$ surplus 9R3J+R9 Singapore
surplus version 2.2.0
Thomson Plaza
301 Upper Thomson Road
Sin Ming, Bishan
574408
Central, Singapore
```

## installation

> [!IMPORTANT]  
> python 3.11 or later is required due to a bug in earlier versions.
> [(python/cpython#88089)](https://github.com/python/cpython/issues/88089)

for most, you can install surplus built from the latest stable release:

```text
pipx install https://github.com/markjoshwel/surplus/releases/latest/download/surplus-latest-py3-none-any.whl
```

or directly from the repository using pip:

```text
pipx install git+https://github.com/markjoshwel/surplus.git@main
```

**Termux users:** consider [surplus on wheels](https://github.com/markjoshwel/surplus-on-wheels),
a sister project that allows you to run surplus regularly throughout the day and send it
to someone on a messaging platform.

surplus is also a public domain dedicated [single python file](surplus/surplus.py), so
feel free to grab that and embed it into your own program as you see fit.

see [licence](#licence) for licensing information.

## usage

### command-line usage

```text
usage: surplus [-h] [-d] [-v] [-c {pluscode,localcode,latlong,sharetext}]
               [-u USER_AGENT] [--show-user-agent] [-t]
               [query ...]

Google Maps Plus Code to iOS Shortcuts-like shareable text

positional arguments:
  query                 full-length Plus Code (6PH58QMF+FX), shortened
                        Plus Code/'local code' (8QMF+FX Singapore),
                        latlong (1.3336875, 103.7749375), string query
                        (e.g., 'Wisma Atria'), or '-' to read from stdin

options:
  -h, --help            show this help message and exit
  -d, --debug           prints lat, long and reverser response dict to
                        stderr
  -v, --version         prints version information to stderr and exits
  -c {pluscode,localcode,latlong,sharetext}, --convert-to {pluscode,localcode,latlong,sharetext}
                        converts query a specific output type, defaults
                        to 'sharetext'
  -u USER_AGENT, --user-agent USER_AGENT
                        user agent string to use for geocoding service,
                        defaults to fingerprinted user agent string
  --show-user-agent     prints fingerprinted user agent string and exits
  -t, --using-termux-location
                        treats input as a termux-location output json
                        string, and parses it accordingly
```

### example api usage

here are a few examples to get you quickly started using surplus in your own program:

1. let surplus do the heavy lifting

   ```python
   >>> from surplus import surplus, Behaviour
   >>> result = surplus("Ngee Ann Polytechnic, Singapore", Behaviour())
   >>> result.get()
   'Ngee Ann Polytechnic\n535 Clementi Road\nBukit Timah\n599489\nNorthwest, Singapore'
   ```

2. handle queries separately

   ```python
   >>> import surplus
   >>> behaviour = surplus.Behaviour("6PH59R48+WP")
   >>> query = surplus.parse_query(behaviour)
   >>> result = surplus.surplus(query.get(), behaviour)
   >>> result.get()
   'MacRitchie Nature Trail\nCentral Water Catchment\n574325\nCentral, Singapore'
   ```

3. start from a Query object

   ```python
   >>> import surplus
   >>> localcode = surplus.LocalCodeQuery(code="8R3M+F8", locality="Singapore")
   >>> geocoder = surplus.SurplusDefaultGeocoding().geocoder
   >>> pluscode_str = localcode.to_full_plus_code(geocoder=geocoder).get()
   >>> pluscode = surplus.PlusCodeQuery(pluscode_str)
   >>> result = surplus.surplus(pluscode, surplus.Behaviour())
   >>> result.get()
   'Wisma Atria\n435 Orchard Road\n238877\nCentral, Singapore'
   ```

notes:

- you can change what surplus does when passing in a custom [`Behaviour`](#class-behaviour)
  object

- most surplus functions return a [`Result`](#class-result) object. while you can
  call [`.get()`](#resultget) to obtain the proper return value, this is dangerous and
  might raise an exception

see the [api reference](#api-reference) for more information.

## api reference

- [constants](#constants)
- [exception classes](#exception-classes)
- [types](#types)
  - [`Query`](#query)
  - [`ResultType`](#resulttype)
  - [`SurplusGeocoderProtocol`](#surplusgeocoderprotocol)
  - [`SurplusReverserProtocol`](#surplusreverserprotocol)
- [`class Behaviour`](#class-behaviour)
- [`class SurplusDefaultGeocoding`](#class-surplusdefaultgeocoding)
  - [`SurplusDefaultGeocoding.update_geocoding_functions()`](#surplusdefaultgeocodingupdate_geocoding_functions)
  - [`SurplusDefaultGeocoding.geocoder()`](#surplusdefaultgeocodinggeocoder)
  - [`SurplusDefaultGeocoding.reverser()`](#surplusdefaultgeocodingreverser)
- [`class ConversionResultTypeEnum`](#class-conversionresulttypeenum)
- [`class Result`](#class-result)
  - [`Result.__bool__()`](#result__bool__)
  - [`Result.cry()`](#resultcry)
  - [`Result.get()`](#resultget)
- [`class Latlong`](#class-latlong)
  - [`Latlong.__str__()`](#latlong__str__)
- [`class PlusCodeQuery`](#class-pluscodequery)
  - [`PlusCodeQuery.to_lat_long_coord()`](#pluscodequeryto_lat_long_coord)
  - [`PlusCodeQuery.__str__()`](#pluscodequery__str__)
- [`class LocalCodeQuery`](#class-localcodequery)
  - [`LocalCodeQuery.to_full_plus_code()`](#localcodequeryto_full_plus_code)
  - [`LocalCodeQuery.to_lat_long_coord()`](#localcodequeryto_lat_long_coord)
  - [`LocalCodeQuery.__str__()`](#localcodequery__str__)
- [`class LatlongQuery`](#class-latlongquery)
  - [`LatlongQuery.to_lat_long_coord()`](#latlongqueryto_lat_long_coord)
  - [`LatlongQuery.__str__()`](#latlongquery__str__)
- [`class StringQuery`](#class-stringquery)
  - [`StringQuery.to_lat_long_coord()`](#stringqueryto_lat_long_coord)
  - [`StringQuery.__str__()`](#stringquery__str__)
- [`def surplus()`](#def-surplus)
- [`def parse_query()`](#def-parse_query)
- [`def generate_fingerprinted_user_agent`](#def-generate_fingerprinted_user_agent)
  - [details on the fingerprinted user agent](#details-on-the-fingerprinted-user-agent)

### constants

- `VERSION: tuple[int, int, int]`

  a tuple of integers representing the version of surplus, in the format
  `[major, minor, patch]`

- `VERSION_SUFFIX: typing.Final[str]`  
  `BUILD_BRANCH: typing.Final[str]`  
  `BUILD_COMMIT: typing.Final[str]`  
  `BUILD_DATETIME: typing.Final[datetime]`

  string and a [datetime.datetime](https://docs.python.org/3/library/datetime.html) object
  containing version and build information, set by [releaser.py](releaser.py)

- `CONNECTION_MAX_RETRIES: int = 9`  
  `CONNECTION_WAIT_SECONDS: int = 10`

  defines if and how many times to retry a connection, alongside how many seconds to wait
  in between tries, for Nominatim

  > [!NOTE]  
  > this constant only affects the default surplus Nominatim geocoding functions. custom
  > functions do not read from this, unless deliberately programmed to do so

- `SHAREABLE_TEXT_LINE_0_KEYS: dict[str, tuple[str, ...]]`  
  `SHAREABLE_TEXT_LINE_1_KEYS: dict[str, tuple[str, ...]]`  
  `SHAREABLE_TEXT_LINE_2_KEYS: dict[str, tuple[str, ...]]`  
  `SHAREABLE_TEXT_LINE_3_KEYS: dict[str, tuple[str, ...]]`  
  `SHAREABLE_TEXT_LINE_4_KEYS: dict[str, tuple[str, ...]]`  
  `SHAREABLE_TEXT_LINE_5_KEYS: dict[str, tuple[str, ...]]`  
  `SHAREABLE_TEXT_LINE_6_KEYS: dict[str, tuple[str, ...]]`

  a dictionary of iso3166-2 country-portion string keys with a tuple of Nominatim keys
  used in shareable text line 0-6 as their values

  ```python
  {
    "default": (...),
    "SG": (...,),
    ...
  }
  ```

- `SHAREABLE_TEXT_LINE_SETTINGS: dict[str, dict[int, tuple[str, bool]]]`

  a dictionary of iso3166-2 country-portion string keys with a dictionary as their values

  the dictionary values are dictionaries with integers as keys, and a tuple of two strings

  the first string is the separator string to use, and the second string is a boolean flag
  that if `True` will check the line for seen names

  ```python
  {
      "default": {
          0: (", ", False),
          ...
          6: (", ", False),
      },
      "IT": {
          0: (", ", False),
          ...
          6: (", ", False),
      },
      ...
  }
  ```

- `SHAREABLE_TEXT_NAMES: dict[str, tuple[str, ...]]`

  a dictionary of iso3166-2 country-portion string keys with a tuple of strings as their
  values
  a tuple of strings containing Nominatim keys used in shareable text line 0-2 and
  special keys in line 3

  used for seen name checks

- `SHAREABLE_TEXT_LOCALITY: dict[str, tuple[str, ...]]`

  a dictionary of iso3166-2 country-portion string keys with a tuple of strings as their
  values

  used when generating the locality portions of shortened Plus Codes/local codes

  ```python
  {
    "default": (...),
    "SG": (...,),
    ...
  }
  ```

- `SHAREABLE_TEXT_DEFAULT: typing.Final[str]`  
  constant for what is the "default" key in the `SHAREABLE*` constants

- `EMPTY_LATLONG: typing.Final[Latlong]`  
  a constant for an empty latlong coordinate, with latitude and longitude set to 0.0

### exception classes

- `class SurplusError(Exception)`  
  base skeleton exception for handling and typing surplus exception classes
- `class NoSuitableLocationError(SurplusError)`
- `class IncompletePlusCodeError(SurplusError)`
- `class PlusCodeNotFoundError(SurplusError)`
- `class LatlongParseError(SurplusError)`
- `class EmptyQueryError(SurplusError)`
- `class UnavailableFeatureError(SurplusError)`

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

#### `SurplusGeocoderProtocol`

[typing_extensions.Protocol](https://mypy.readthedocs.io/en/stable/protocols.html#callback-protocols)
class for documentation and static type checking of surplus geocoder functions

- **signature and conforming function signature**

  ```python
  class SurplusGeocoderProtocol(Protocol):
      def __call__(self, place: str) -> Latlong:
          ...
  ```

  functions that conform to this protocol should have the following signature:

  ```python
  def example(place: str) -> Latlong: ...
  ```

- **information on conforming functions**

  function takes in a location name as a string, and returns a [Latlong](#class-latlong).

  **function MUST supply a `bounding_box` attribute to the to-be-returned
  [Latlong](#class-latlong).** the bounding box is used when surplus shortens Plus Codes.

  function can and should be at minimum
  [`functools.lru_cache()`-wrapped](https://docs.python.org/3/library/functools.html#functools.lru_cache)
  if the geocoding service asks for caching

  exceptions are handled by the caller

#### `SurplusReverserProtocol`

[typing_extensions.Protocol](https://mypy.readthedocs.io/en/stable/protocols.html#callback-protocols)
class for documentation and static type checking of surplus reverser functions

- **signature and conforming function signature**

  ```python
  class SurplusReverserProtocol(Protocol):
      def __call__(self, latlong: Latlong, level: int = 18) -> dict[str, Any]:
          ...
  ```

  functions that conform to this protocol should have the following signature:

  ```python
  def example(latlong: Latlong, level: int = 18) -> dict[str, Any]: ...
  ```

- **information on conforming functions**

  function takes in a [Latlong](#class-latlong) object and return a dictionary with [`SHAREABLE_TEXT_LINE_*_KEYS`](#constants) keys at the dictionaries' top-level.  
  keys are used to access address information.

  function should also take in an int representing the level of detail for the returned
  address, 0-18 (country-level to building), inclusive. should default to 18.

  keys for latitude, longitude and an iso3166-2 (or closest equivalent) should also be
  included at the dictionaries top level as the keys `latitude`, `longitude` and
  `ISO3166-2` (non-case sensitive, or at least something starting with `ISO3166`)
  respectively.

  ```python
  {
      'ISO3166-2-lvl6': 'SG-03',
      'amenity': 'Ngee Ann Polytechnic',
      ...
      'country': 'Singapore',
      'latitude': 1.33318835,
      'longitude': 103.77461234638255,
      'postcode': '599489',
      'raw': {...},
  }
  ```

  function can and should be at minimum
  [`functools.lru_cache()`-wrapped](https://docs.python.org/3/library/functools.html#functools.lru_cache)
  if the geocoding service asks for caching

  exceptions are handled by the caller

### `class Behaviour`

[`typing.NamedTuple`](https://docs.python.org/3/library/typing.html#typing.NamedTuple)
representing how surplus operations should behave

attributes

- `query: str | list[str] = ""`  
  original user-passed query string or a list of strings from splitting user-passed query
  string by spaces

- `geocoder: SurplusGeocoderProtocol = default_geocoding.geocoder`  
  name string to location function, see
  [`SurplusGeocoderProtocol`](#surplusgeocoderprotocol) for more information

- `reverser: SurplusReverserProtocol = default_geocoding.reverser`  
  Latlong object to address information dictionary function, see
  [`SurplusReverserProtocol`](#surplusreverserprotocol) for more information

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

- `using_termux_location: bool = False`  
  treats query as a termux-location output json string, and parses it accordingly

- `show_user_agent: bool = False`  
  whether to print the user agent string to stderr

### `class SurplusDefaultGeocoding`

> [!IMPORTANT]  
> this has replaced the now deprecated default geocoding functions, `default_geocoder()`
> and `default_reverser()`, in surplus 2.1 and later.

see [SurplusGeocoderProtocol](#surplusgeocoderprotocol) and
[SurplusReverserProtocol](#surplusreverserprotocol) for more information how to
implement a compliant custom geocoder functions.

[`dataclasses.dataclass`](https://docs.python.org/3/library/dataclasses.html) providing
the default geocoding functionality for surplus, via
[OpenStreetMap Nominatim](https://nominatim.openstreetmap.org/)

attributes

- `user_agent: str = default_fingerprint`  
  pass in a custom user agent here, else it will be the default
  [fingerprinted user agent](#details-on-the-fingerprinted-user-agent)

example usage

```python
from surplus import surplus, Behaviour, SurplusDefaultGeocoding

geocoding = SurplusDefaultGeocoding("custom user agent")
geocoding.update_geocoding_functions()  # not necessary but recommended

behaviour = Behaviour(
    ...,
    geocoder=geocoding.geocoder,
    reverser=geocoding.reverser
)

result = surplus("query", behaviour=behaviour)

...
```

methods

- [`def update_geocoding_functions(self) -> None: ...`](#surplusdefaultgeocodingupdate_geocoding_functions)
- [`def geocoder(self, place: str) -> Latlong: ...`](#surplusdefaultgeocodinggeocoder)
- [`def reverser(self, latlong: Latlong, level: int = 18) -> dict[str, Any]: ...`](#surplusdefaultgeocodingreverser)

#### `SurplusDefaultGeocoding.update_geocoding_functions()`

re-initialise the geocoding functions with the current user agent, also generate a new
user agent if not set properly

it is recommended to call this before using surplus as by default the geocoding functions
are uninitialised

- signature

  ```python
  def update_geocoding_functions(self) -> None: ...
  ```

#### `SurplusDefaultGeocoding.geocoder()`

> [!WARNING]  
> this function is primarily given to be passed into a [`Behaviour`](#class-behaviour)
> object, and is not meant to be called directly.

default geocoder for surplus

see [SurplusGeocoderProtocol](#surplusgeocoderprotocol) for more information on surplus
geocoder functions

#### `SurplusDefaultGeocoding.reverser()`

> [!WARNING]  
> this function is primarily given to be passed into a [`Behaviour`](#class-behaviour)
> object, and is not meant to be called directly.

default reverser for surplus

see [SurplusReverserProtocol](#surplusreverserprotocol) for more information on surplus
reverser functions

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
        return Result[str]("", error=exc)

    else:
        return Result[str](contents)

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
- [`def cry(self, string: bool = False) -> str: ...`](#resultcry)
- [`def get(self) -> ResultType: ...`](#resultget)

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
- `bounding_box: tuple[float, float, float, float] | None = None`  
  a four-tuple representing a bounding box, `(lat1, lat2, lon1, lon2)` or None.

  the user does not need to enter this. the attribute is only used when shortening plus
  codes, and would be supplied by the geocoding service during shortening.

methods

- [`def __str__(self) -> str: ...`](#latlong__str__)

#### `Latlong.__str__()`

method that returns a comma-and-space-separated string of `self.latitude` and
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
  def to_lat_long_coord(self, geocoder: SurplusGeocoderProtocol) -> Result[Latlong]:
      ...
  ```

- arguments

  - `geocoder: SurplusGeocoderProtocol`  
    name string to location function, see
    [SurplusGeocoderProtocol](#surplusgeocoderprotocol) for more information

- returns [`Result[Latlong]`](#class-latlong)

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
  def to_full_plus_code(self, geocoder: SurplusGeocoderProtocol) -> Result[str]:
      ...
  ```

- arguments

  - `geocoder: SurplusGeocoderProtocol`  
    name string to location function, see
    [SurplusGeocoderProtocol](#surplusgeocoderprotocol) for more information

- returns [`Result`](#class-result)`[str]`

#### `LocalCodeQuery.to_lat_long_coord()`

method that returns a latitude-longitude coordinate pair

- signature

  ```python
  def to_lat_long_coord(self, geocoder: SurplusGeocoderProtocol) -> Result[Latlong]:
      ...
  ```

- arguments

  - `geocoder: SurplusGeocoderProtocol`  
    name string to location function, see
    [SurplusGeocoderProtocol](#surplusgeocoderprotocol) for more information

- returns [`Result[Latlong]`](#class-latlong)

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
  def to_lat_long_coord(self, geocoder: SurplusGeocoderProtocol) -> Result[Latlong]:
      ...
  ```

- arguments

  - `geocoder: SurplusGeocoderProtocol`  
    name string to location function, see
    [SurplusGeocoderProtocol](#surplusgeocoderprotocol) for more information

- returns [`Result[Latlong]`](#class-latlong)

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

- [`def to_lat_long_coord(self, ...) -> Result[Latlong]: ...`](#stringqueryto_lat_long_coord)
- [`def __str__(self) -> str: ...`](#stringquery__str__)

#### `StringQuery.to_lat_long_coord()`

method that returns a latitude-longitude coordinate pair

- signature

  ```python
  def to_lat_long_coord(self, geocoder: SurplusGeocoderProtocol) -> Result[Latlong]:
      ...
  ```

- arguments

  - `geocoder: SurplusGeocoderProtocol`  
    name string to location function, see
    [SurplusGeocoderProtocol](#surplusgeocoderprotocol) for more information

- returns [`Result[Latlong]`](#class-latlong)

#### `StringQuery.__str__()`

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

- returns [`Result[Query]`](#query)

### `def generate_fingerprinted_user_agent()`

function that attempts to return a unique user agent string.

- signature

```python
def generate_fingerprinted_user_agent() -> Result[str]:
```

- returns [`Result[str]`](#class-result)

  this result will always have a valid value as erroneous results will have a
  resulting value of `'surplus/<version> (generic-user)'`

  valid results will have a value of `'surplus/<version> (<fingerprin hasht>)'`, where
  the fingerprint hash is a 12 character hexadecimal string

#### details on the fingerprinted user agent

**why do this in the first place?**  
if too many people use surplus at the same time,
Nominatim will start to think it's just one person being greedy. so to prevent this,
surplus will try to generate a unique user agent string for each user through
fingerprinting.

at the time of writing, the pre-hashed fingerprint string is as follows:

```python
unique_info: str = f"{version}-{system_info}-{hostname}-{mac_address}"
```

it contains the following, in order, alongside an example:

1. `version` - the surplus version alongside a suffix, if any

   ```text
   2.2.0-local
   ```

2. `system_info` - generic machine and operating system information

   ```text
   Linux-6.5.0-locietta-WSL2-xanmod1-x86_64-with-glibc2.35
   ```

3. `hostname` - your computer's hostname

   ```text
   mark
   ```

4. `mac_address` - your computer's mac address

   ```text
   A9:36:3C:98:79:33
   ```

after hashing, this string becomes a 12 character hexadecimal string, as shown below:

```text
surplus/2024.0.0 (1fdbfa0b0cfb)
                  ^^^^^^^^^^^^
                  this is the hashed result of unique_info
```

if at any time the retrieval of any of these four elements fail, surplus will just give
up and default to `'surplus/<version> (generic-user)'`.

you can see the fingerprinted user agent string by running the following command:

```text
$ surplus --show-user-agent
...
```

if any of this seems weird to you, that's fine. pass in a custom user agent flag to
surplus with `-u` or `--user-agent` to override the default user agent, or override the
default user agent in your own code by passing in a custom user agent string to
[`Behaviour`](#class-behaviour).

```text
$ surplus --user_agent "a-shiny-custom-and-unique-user-agent" 77Q4+7X Austin, Texas, USA
...
```

```python
>>> from surplus import surplus, Behaviour
>>> surplus(..., Behaviour(user_agent="a-shiny-custom-and-unique-user-agent"))
...
```

## licence

surplus is free and unencumbered software released into the public domain. for more
information, please refer to the [UNLICENCE](/UNLICENCE), <https://unlicense.org>, or the
python module docstring.

however, direct dependencies of surplus are licensed under different, but still permissive
and open-source licences.

- [geopy](https://pypi.org/project/geopy/):
  Python Geocoding Toolbox

  MIT Licence

  - [geographiclib](https://pypi.org/project/geographiclib/):
    The geodesic routines from GeographicLib

    MIT Licence

- [pluscodes](https://pypi.org/project/pluscodes/):
  Compute Plus Codes (Open Location Codes)

  Apache 2.0

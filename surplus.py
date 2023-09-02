"""
surplus: Google Maps Plus Code to iOS Shortcuts-like shareable text
-------------------------------------------------------------------
by mark <mark@joshwel.co> and contributors

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
"""

from argparse import ArgumentParser
from collections import OrderedDict
from enum import Enum
from sys import stderr, stdout
from typing import (
    Any,
    Callable,
    Final,
    Generic,
    NamedTuple,
    Sequence,
    TextIO,
    TypeAlias,
    TypeVar,
)

from geopy import Location as _geopy_Location  # type: ignore
from geopy.geocoders import Nominatim as _geopy_Nominatim  # type: ignore
from pluscodes import PlusCode as _PlusCode  # type: ignore
from pluscodes.validator import Validator as _PlusCode_Validator  # type: ignore

from pluscodes.openlocationcode import (  # type: ignore # isort: skip
    recoverNearest as _PlusCode_recoverNearest,
)

# constants

VERSION: Final[tuple[int, int, int]] = (2, 0, 0)
USER_AGENT: Final[str] = "surplus"
OUTPUT_LINE_0_KEYS: Final[tuple[str, ...]] = (
    "emergency",
    "historic",
    "military",
    "natural",
    "landuse",
    "place",
    "railway",
    "man_made",
    "aerialway",
    "boundary",
    "amenity",
    "aeroway",
    "club",
    "craft",
    "leisure",
    "office",
    "mountain_pass",
    "shop",
    "tourism",
    "bridge",
    "tunnel",
    "waterway",
)
OUTPUT_LINE_1_KEYS: Final[tuple[str, ...]] = ("building",)
OUTPUT_LINE_2_KEYS: Final[tuple[str, ...]] = ("highway",)
OUTPUT_LINE_3_KEYS: Final[tuple[str, ...]] = (
    "house_number",
    "house_name",
    "road",
)
OUTPUT_LINE_4_KEYS: Final[tuple[str, ...]] = (
    "residential",
    "neighbourhood",
    "allotments",
    "quarter",
    "city_district",
    "district",
    "borough",
    "suburb",
    "subdivision",
    "municipality",
    "city",
    "town",
    "village",
)
OUTPUT_LINE_5_KEYS: Final[tuple[str, ...]] = ("postcode",)
OUTPUT_LINE_6_KEYS: Final[tuple[str, ...]] = (
    "region",
    "county",
    "state",
    "state_district",
    "country",
    "continent",
)

# exceptions


class NoSuitableLocationError(Exception):
    ...


class IncompletePlusCodeError(Exception):
    ...


# data structures


class ConversionResultTypeEnum(Enum):
    """enum representing what the result type of conversion should be"""

    PLUS_CODE = "pluscode"
    LOCAL_CODE = "localcode"
    LATLONG = "latlong"
    SHAREABLE_TEXT = "shareabletext"


ResultType = TypeVar("ResultType")


class Result(NamedTuple, Generic[ResultType]):
    """
    typing.NamedTuple representing a result for safe value handling

    arguments
        value: ResultType
            value to return or fallback value if erroneous
        error: BaseException | str | None = None
            exception if any, or an error message

    methods
        def __bool__(self) -> bool: ...
        def get(self) -> ResultType: ...
        def cry(self, string: bool = False) -> str: ...

    example
        # do something
        try:
            file_contents = Path(...).read_text()
        except Exception as exc:
            # must pass a default value
            result = Result[str]("", error=exc)
        else:
            result = Result[str](file_contents)

        # handle result
        if not result:
            # .cry() either raises an exception or returns an error message
            error_message = result.cry()
            ...
        else:
            data = result.get()  # raises exception or returns value
    """

    value: ResultType
    error: BaseException | str | None = None

    def __bool__(self) -> bool:
        """method that returns True if self.error is not None"""
        return self.error is None

    def cry(self, string: bool = False) -> str:
        """
        method that raises self.error if is an instance of BaseException,
        returns self.error if is an instance of str, or returns an empty string if
        self.error is None.

        arguments
            string: bool = False
                if self.error is an instance Exception, returns it as a string.
        """

        if isinstance(self.error, BaseException):
            if string:
                message = f"{self.error}"
                name = self.error.__class__.__name__
                return f"{message} ({name})" if (message != "") else name

            raise self.error

        if isinstance(self.error, str):
            return self.error

        return ""

    def get(self) -> ResultType:
        """method that returns self.value if Result is non-erroneous else raises error"""
        if isinstance(self.error, BaseException):
            raise self.error
        return self.value


class Latlong(NamedTuple):
    """
    typing.NamedTuple representing a latitude-longitude coordinate pair

    arguments
        latitude: float
        longitude: float

    methods
        def __str__(self) -> str: ...
    """

    latitude: float
    longitude: float

    def __str__(self) -> str:
        """
        method that returns a comma-and-space-seperated string of self.latitude and
        self.longitude
        """
        return f"{self.latitude}, {self.longitude}"


EMPTY_LATLONG: Final[Latlong] = Latlong(latitude=0.0, longitude=0.0)


class PlusCodeQuery(NamedTuple):
    """
    typing.NamedTuple representing a complete Plus Code

    arguments
        code: str

    methods
        def to_lat_long_coord(self, ...) -> Result[Latlong]: ...
    """

    code: str

    def to_lat_long_coord(self, geocoder: Callable[[str], Latlong]) -> Result[Latlong]:
        """
        method that returns a latitude-longitude coordinate pair

        arguments
            geocoder: typing.Callable[[str], Latlong]
                name string to location function, must take in a string and return a
                Latlong. exceptions are handled.

        returns Result[Latlong]
        """

        latitude: float = 0.0
        longitude: float = 0.0

        try:
            plus_code = _PlusCode(self.code)
            latitude = plus_code.area.center().lat
            longitude = plus_code.area.center().lon

        except KeyError:
            return Result[Latlong](
                EMPTY_LATLONG,
                error=IncompletePlusCodeError(
                    "Plus Code is not full-length (e.g., 6PH58QMF+FX)"
                ),
            )

        except Exception as exc:
            return Result[Latlong](EMPTY_LATLONG, error=exc)

        return Result[Latlong](Latlong(latitude=latitude, longitude=longitude))


class LocalCodeQuery(NamedTuple):
    """
    typing.NamedTuple representing a complete shortened Plus Code with locality, referred
    to by surplus as a "local code"

    arguments
        code: str
            Plus Code portion of local code, e.g., "8QMF+FX"
        locality: str
            remaining string of local code, e.g., "Singapore"

    methods
        def to_lat_long_coord(self, ...) -> Result[Latlong]: ...
    """

    code: str
    locality: str

    def to_full_plus_code(self, geocoder: Callable[[str], Latlong]) -> Result[str]:
        """
        method that returns a full-length Plus Code

        arguments
            geocoder: typing.Callable[[str], Latlong]
                name string to location function, must take in a string and return a
                Latlong. exceptions are handled.

        returns Result[str]
        """

        try:
            locality_location = geocoder(self.locality)

            recovered_pluscode = _PlusCode_recoverNearest(
                code=self.code,
                referenceLatitude=locality_location.latitude,
                referenceLongitude=locality_location.longitude,
            )

            return Result[str](recovered_pluscode)

        except Exception as exc:
            return Result[str]("", error=exc)

    def to_lat_long_coord(self, geocoder: Callable[[str], Latlong]) -> Result[Latlong]:
        """
        method that returns a latitude-longitude coordinate pair

        arguments
            geocoder: typing.Callable[[str], Latlong]
                name string to location function, must take in a string and return a
                Latlong. exceptions are handled.

        returns Result[Latlong]
        """

        recovered_pluscode = self.to_full_plus_code(geocoder=geocoder)

        if not recovered_pluscode:
            return Result[Latlong](EMPTY_LATLONG, error=recovered_pluscode.error)

        return Result[Latlong](
            PlusCodeQuery(recovered_pluscode.get())
            .to_lat_long_coord(geocoder=geocoder)
            .get()  # PlusCodeQuery can get latlong coord offline, so no need to handle
        )


class LatlongQuery(NamedTuple):
    """
    typing.NamedTuple representing a latitude-longitude coordinate pair

    arguments
        latlong: Latlong

    methods
        def to_lat_long_coord(self, ...) -> Result[Latlong]: ...
    """

    latlong: Latlong

    def to_lat_long_coord(self, geocoder: Callable[[str], Latlong]) -> Result[Latlong]:
        """
        method that returns a latitude-longitude coordinate pair

        arguments
            geocoder: typing.Callable[[str], Latlong]
                name string to location function, must take in a string and return a
                Latlong. exceptions are handled.

        returns Result[Latlong]
        """

        return Result[Latlong](self.latlong)


class StringQuery(NamedTuple):
    """
    typing.NamedTuple representing a complete Plus Code

    arguments
        code: str

    methods
        def to_lat_long_coord(self, ...) -> Result[Latlong]: ...
    """

    query: str

    def to_lat_long_coord(self, geocoder: Callable[[str], Latlong]) -> Result[Latlong]:
        """
        method that returns a latitude-longitude coordinate pair

        arguments
            geocoder: typing.Callable[[str], Latlong]
                name string to location function, must take in a string and return a
                Latlong. exceptions are handled.

        returns Result[Latlong]
        """

        try:
            return Result[Latlong](geocoder(self.query))

        except Exception as exc:
            return Result[Latlong](EMPTY_LATLONG, error=exc)


Query: TypeAlias = PlusCodeQuery | LocalCodeQuery | LatlongQuery | StringQuery


def default_geocoder(place: str) -> Latlong:
    """default geocoder for surplus, uses OpenStreetMap Nominatim"""

    location: _geopy_Location | None = _geopy_Nominatim(user_agent=USER_AGENT).geocode(
        place
    )

    if location is None:
        raise NoSuitableLocationError(
            f"No suitable location could be geolocated from '{place}'"
        )

    return Latlong(
        latitude=location.latitude,
        longitude=location.longitude,
    )


def default_reverser(latlong: Latlong) -> dict[str, Any]:
    """default geocoder for surplus, uses OpenStreetMap Nominatim"""
    location: _geopy_Location | None = _geopy_Nominatim(user_agent=USER_AGENT).reverse(
        str(latlong)
    )

    if location is None:
        raise NoSuitableLocationError(
            f"No suitable location could be reversed from '{str(latlong)}'"
        )

    return location.raw


class Behaviour(NamedTuple):
    """
    typing.NamedTuple representing expected behaviour of surplus

    arguments
        query: list[str]
            original user-passed query string split by spaces
        geocoder: Callable[[str], Latlong]
            name string to location function, must take in a string and return a Latlong.
            exceptions are handled by the caller.
        reverser: Callable[[str], dict[str, Any]]
            Latlong object to dictionary function, must take in a string and return a
            dict. exceptions are handled by the caller.
        stderr: TextIO = stderr
            TextIO-like object representing a writeable file. defaults to sys.stderr.
        stdout: TextIO = stdout
            TextIO-like object representing a writeable file. defaults to sys.stdout.
        debug: bool = False
            whether to print debug information to stderr
        version_header: bool = False
            whether to print version information and exit
        convert_to_type: ConversionResultTypeEnum = ConversionResultTypeEnum.SHAREABLE_TEXT
            what type to convert query to
    """

    query: list[str]
    geocoder: Callable[[str], Latlong] = default_geocoder
    reverser: Callable[[Latlong], dict[str, Any]] = default_reverser
    stderr: TextIO = stderr
    stdout: TextIO = stdout
    debug: bool = False
    version_header: bool = False
    convert_to_type: ConversionResultTypeEnum = ConversionResultTypeEnum.SHAREABLE_TEXT


# functions


def parse_query(
    behaviour: Behaviour,
) -> Result[Query]:
    """
    function that parses a query string into a query object

    arguments
        behaviour: Behaviour

    returns Result[Query]
    """

    def _match_plus_code(
        behaviour: Behaviour,
    ) -> Result[Query]:
        """
        internal helper code reuse function

        looks through each 'word' and attempts to match to a Plus Code
        if found, remove from original query and strip of whitespace and commas
        use resulting stripped query as locality
        """

        validator = _PlusCode_Validator()
        portion_plus_code: str = ""
        portion_locality: str = ""

        original_query = " ".join(behaviour.query)
        split_query = behaviour.query

        for word in split_query:
            if validator.is_valid(word):
                portion_plus_code = word

                if validator.is_full(word):
                    return Result[Query](PlusCodeQuery(portion_plus_code))

                break

        # didn't find a plus code. :(
        if portion_plus_code == "":
            return Result[Query](
                LatlongQuery(EMPTY_LATLONG),
                error="unable to find a Plus Code",
            )

        # did find plus code, but not full-length. :(
        if not validator.is_full(portion_plus_code):
            return Result[Query](
                LatlongQuery(EMPTY_LATLONG),
                error=IncompletePlusCodeError(
                    "Plus Code is not full-length (e.g., 6PH58QMF+FX)"
                ),
            )

        # found a plus code!
        portion_locality = original_query.replace(portion_plus_code, "")
        portion_locality = portion_locality.strip().strip(",").strip()

        if behaviour.debug:
            behaviour.stderr.write(f"debug: {portion_plus_code=}, {portion_locality=}\n")

        return Result[Query](
            LocalCodeQuery(
                code=portion_plus_code,
                locality=portion_locality,
            )
        )

    # types to handle:
    #
    # plus codes
    #   6PH58R3M+F8
    # local codes
    #   8RQQ+4Q Singapore                        (single-word-long locality suffix)
    #   St Lucia, Queensland, Australia G227+XF  (multi-word-long locality prefix)
    # latlong coords
    #   1.3521,103.8198   (single-word-long with comma)
    #   1.3521, 103.8198  (space-seperated with comma)
    #   1.3521 103.8198   (space-seperated without comma)
    # string queries
    #   Ngee Ann Polytechnic, Singapore  (has a comma)
    #   Toa Payoh North                  (no commas)

    if behaviour.debug:
        behaviour.stderr.write(f"debug: {behaviour.query=}\n")

    # check if empty
    if behaviour.query == []:
        return Result[Query](
            LatlongQuery(EMPTY_LATLONG),
            error="query is empty",
        )

    # try to find a plus/local code
    if mpc_result := _match_plus_code(behaviour=behaviour):
        # found one!
        return Result[Query](mpc_result.get())

    # is a plus/local code, but missing details
    if isinstance(mpc_result.error, IncompletePlusCodeError):
        return mpc_result  # propagate back up to caller

    # not a plus/local code, try to match for latlong or string query
    match behaviour.query:
        case [single]:
            # possibly a:
            #   comma-seperated single-word-long latlong coord
            #   (fallback) single word string query

            if "," not in single:  # no comma, not a latlong coord
                return Result[Query](StringQuery(" ".join(behaviour.query)))

            else:  # has comma, possibly a latlong coord
                split_query: list[str] = single.split(",")

                if len(split_query) > 2:
                    return Result[Query](
                        LatlongQuery(EMPTY_LATLONG),
                        error="unable to parse latlong coord",
                    )

                try:  # try to type cast query
                    latitude = float(split_query[0].strip(","))
                    longitude = float(split_query[-1].strip(","))

                except ValueError:  # not a latlong coord, fallback
                    return Result[Query](StringQuery(single))

                else:  # are floats, so is a latlong coord
                    return Result[Query](
                        LatlongQuery(
                            Latlong(
                                latitude=latitude,
                                longitude=longitude,
                            )
                        )
                    )

        case [left_single, right_single]:
            # possibly a:
            #   space-seperated latlong coord
            #   (fallback) space-seperated string query

            try:  # try to type cast query
                latitude = float(left_single.strip(","))
                longitude = float(right_single.strip(","))

            except ValueError:  # not a latlong coord, fallback
                return Result[Query](StringQuery(" ".join(behaviour.query)))

            else:  # are floats, so is a latlong coord
                return Result[Query](
                    LatlongQuery(Latlong(latitude=latitude, longitude=longitude))
                )

        case _:
            # possibly a:
            #   (fallback) space-seperated string query

            return Result[Query](StringQuery(" ".join(behaviour.query)))


def handle_args() -> Behaviour:
    """
    internal function that handles command-line arguments

    returns Behaviour
        program behaviour namedtuple
    """

    parser = ArgumentParser(
        prog="surplus",
        description=__doc__[__doc__.find(":") + 2 : __doc__.find("\n", 1)],
    )
    parser.add_argument(
        "query",
        type=str,
        help=(
            "full-length Plus Code (6PH58QMF+FX), "
            "shortened Plus Code/'local code' (8QMF+FX Singapore), "
            "latlong (1.3336875, 103.7749375), "
            "or string query (e.g., 'Wisma Atria')"
        ),
        nargs="*",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        default=False,
        help="prints lat, long and reverser response dict to stderr",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        default=False,
        help="prints version information to stderr and exits",
    )
    parser.add_argument(
        "-c",
        "--convert-to",
        type=str,
        choices=[str(v.value) for v in ConversionResultTypeEnum],
        help=(
            "converts query a specific output type, defaults to "
            f"'{Behaviour([]).convert_to_type.value}'"
        ),
        default=Behaviour([]).convert_to_type.value,
    )

    args = parser.parse_args()
    behaviour = Behaviour(
        query=args.query,
        geocoder=default_geocoder,
        reverser=default_reverser,
        stderr=stderr,
        stdout=stdout,
        debug=args.debug,
        version_header=args.version,
        convert_to_type=ConversionResultTypeEnum(args.convert_to),
    )

    return behaviour


def surplus(
    query: PlusCodeQuery | LocalCodeQuery | LatlongQuery | StringQuery,
    behaviour: Behaviour,
) -> Result[str]:
    """
    query to shareable text conversion function

    query: PlusCodeQuery | LocalCodeQuery | LatlongQuery | StringQuery
        query object to convert, see respective docstrings for more information on each
        type of query object
    behaviour: Behaviour
        program behaviour namedtuple

    returns Result[str]
    """

    def _unique(l: Sequence[str]) -> list[str]:
        """(internal function) returns a in-order unique list from list"""
        unique: OrderedDict = OrderedDict()
        for line in l:
            unique.update({line: None})
        return list(unique.keys())

    def _generate_text(line_keys: Sequence[str]) -> str:
        """(internal function) TODO DOCSTRING"""
        # TODO
        return ""

    """
    # get latlong and handle result
    latlong = query.to_lat_long_coord(geocoder=behaviour.geocoder)

    if not latlong:
        return Result[str]("", error=latlong.error)

    if behaviour.debug:
        behaviour.stderr.write(f"debug: {latlong.get()=}\n")
    """

    # operate on query
    text: str = ""

    match behaviour.convert_to_type:
        case ConversionResultTypeEnum.SHAREABLE_TEXT:
            # TODO
            return Result[str](text, error="TODO")

        case ConversionResultTypeEnum.PLUS_CODE:
            # TODO: https://github.com/markjoshwel/surplus/issues/18
            return Result[str](
                text, error="converting to Plus Code is not implemented yet"
            )

        case ConversionResultTypeEnum.LOCAL_CODE:
            # TODO: https://github.com/markjoshwel/surplus/issues/18
            return Result[str](
                text, error="converting to Plus Code is not implemented yet"
            )

        case ConversionResultTypeEnum.LATLONG:
            # TODO: https://github.com/markjoshwel/surplus/issues/18
            return Result[str](text, error="converting to Latlong is not implemented yet")

        case _:
            return Result[str](
                "", error=f"unknown conversion result type '{behaviour.convert_to_type}'"
            )


# command-line entry


def cli() -> int:
    """command-line entry point, returns an exit code int"""

    # handle arguments and print version header
    behaviour = handle_args()

    (behaviour.stdout if behaviour.version_header else behaviour.stderr).write(
        f"surplus version {'.'.join([str(v) for v in VERSION])}"
        + (f", debug mode" if behaviour.debug else "")
        + "\n"
    )

    if behaviour.version_header:
        exit(0)

    # parse query and handle result
    query = parse_query(behaviour=behaviour)

    if not query:
        behaviour.stderr.write(f"error: {query.cry(string=not behaviour.debug)}\n")
        return -1

    if behaviour.debug:
        behaviour.stderr.write(f"debug: {query.get()=}\n")

    # run surplus
    text = surplus(
        query=query.get(),
        behaviour=behaviour,
    )

    # handle and display surplus result
    if not text:
        behaviour.stderr.write(f"error: {text.cry(string=not behaviour.debug)}\n")
        return -2

    behaviour.stdout.write(text.get() + "\n")
    return 0


if __name__ == "__main__":
    exit(cli())

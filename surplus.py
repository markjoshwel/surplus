"""
surplus: Plus Code to iOS-Shortcuts-like shareable text
-------------------------------------------------------
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

For more information, please refer to <http:m/unlicense.org/>
"""

from argparse import ArgumentParser
from collections import OrderedDict
from dataclasses import dataclass
from sys import stderr, stdout
from typing import Any, Callable, Final, Generic, Literal, NamedTuple, TextIO, TypeVar

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


class InvalidPlusCodeError(Exception):
    ...


class NoSuitableLocationError(Exception):
    ...


# data structures

ResultType = TypeVar("ResultType")


class Result(NamedTuple, Generic[ResultType]):
    """
    typing.NamedTuple representing a result for safe value handling

    arguments
        value: ResultType
            value to return or fallback value if erroneous
        error: Exception | None = None
            exception if any

    methods
        def __bool__(self) -> bool: ...
        def get(self) -> ResultType: ...

    example
        int_result = Result[int](0)
        str_err_result = Result[str]("", FileNotFoundError(...))
    """

    value: ResultType
    error: BaseException | None = None

    def __bool__(self) -> bool:
        """method that returns True if self.error is not None"""
        return self.error is None

    def get(self) -> ResultType:
        """method that returns self.value if Result is non-erroneous else raises error"""
        if self.error is not None:
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
                error=InvalidPlusCodeError(
                    "Plus Code is not full-length, e.g, 6PH58QMF+FX"
                ),
            )

        except Exception as err:
            return Result[Latlong](EMPTY_LATLONG, error=err)

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

        except Exception as err:
            return Result[str]("", error=err)

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

        except Exception as err:
            return Result[Latlong](EMPTY_LATLONG, error=err)


# functions


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


def surplus(
    query: PlusCodeQuery | LocalCodeQuery | LatlongQuery | StringQuery,
    geocoder: Callable[[str], Latlong],
    reverser: Callable[[str], dict[str, Any]],
    stderr: TextIO = stderr,
    stdout: TextIO = stdout,
    debug: bool = False,
) -> Result[str]:
    return Result[str]("", error=NotImplementedError())


# command-line entry


def main():
    ...


if __name__ == "__main__":
    main()

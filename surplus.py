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

For more information, please refer to <http://unlicense.org/>
"""

from argparse import ArgumentParser
from collections import OrderedDict
from sys import stderr
from typing import Any, Callable, Final, Literal, NamedTuple

from geopy import Location  # type: ignore
from geopy.geocoders import Nominatim  # type: ignore
from pluscodes import PlusCode  # type: ignore
from pluscodes.openlocationcode import recoverNearest  # type: ignore
from pluscodes.validator import Validator  # type: ignore


# constants

VERSION: Final[tuple[int, int, int]] = (2, 0, 0)

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

# program body

...

# program entry


def main():
    pass


if __name__ == "__main__":
    main()

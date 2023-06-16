"""
surplus: Plus Code to iOS-Shortcuts-like shareable text
-------------------------------------------------------
by mark <mark@joshwel.co>

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

VERSION: Final[tuple[int, int, int]] = (1, 1, 1)


class Localcode(NamedTuple):
    """
    typing.NamedTuple representing short Plus Code with locality

    code: str
        Plus Code - e.g.: "8QMF+FX"
    locality: str
        e.g.: "Singapore"
    """

    code: str
    locality: str

    def full_length(
        self, geocoder: Callable = Nominatim(user_agent="surplus").geocode
    ) -> tuple[bool, str]:
        """
        method that calculates full-length Plus Code using locality

        geocoder: typing.Callable = geopy.geocoders.Nominatim(user_agent="surplus").geocode
            place/locality to location function, accesses .longitude and .latitude if
            returned object is not None

        returns tuple[bool, str]
            (True, <str>) - conversion was successful, str is resultant Plus Code
            (False, <str>) - conversion failed, str is error message
        """
        location: Location | None = geocoder(self.locality)
        lat: float = 0.0
        lon: float = 0.0

        if location is None:
            return False, f"no coordinates found for '{self.locality}'"

        recv_pcode = recoverNearest(
            code=self.code,
            referenceLongitude=location.longitude,
            referenceLatitude=location.latitude,
        )

        return True, recv_pcode


class Latlong(NamedTuple):
    """
    typing.NamedTuple representing a pair of latitude and longitude coordinates

    lat: float
        latitudinal coordinate
    long: float
        longitudinal coordinate
    """

    lat: float
    long: float


def surplus(
    query: str | Localcode | Latlong,
    reverser: Callable = Nominatim(user_agent="surplus").reverse,
    debug: bool = False,
) -> tuple[bool, str]:
    """
    pluscode to shareable text conversion function

    query: str | surplus.Localcode | surplus.Latlong
        str - normal longcode (6PH58QMF+FX)
        surplus.Localcode - shortcode with locality (8QMF+FX Singapore)
        surplus.Latlong - latlong

    reverser: typing.Callable = geopy.geocoders.Nominatim(user_agent="surplus").reverser
        latlong to data function, accesses a dict from .raw attribute of return object
        function should be able to take a string with two floats and return a
        geopy.Location-like object (None checking is done)

            # code used by surplus
            location: dict[str, Any] = reverser(f"{lat}, {lon}").raw

        dict should be similar to nominatim raw dicts, see
        <https://nominatim.org/release-docs/latest/api/Output/#addressdetails>

    debug: bool = False
        prints lat, long and reverser response dict to stderr

    returns tuple[bool, str]
        (True, <str>)  - conversion was successful, str is resultant text
        (False, <str>) - conversion failed, str is error message
    """

    def _unique(l: list[str]) -> list[str]:
        unique: OrderedDict = OrderedDict()
        for line in l:
            unique.update({line: None})
        return list(unique.keys())

    _latlong = handle_query(query=query, debug=debug)

    if _latlong[0] is False:
        assert isinstance(_latlong[1], str)
        return False, _latlong[1]

    assert isinstance(_latlong[1], Latlong)
    latlong = _latlong[1]

    try:
        _reversed: Location | None = reverser(f"{latlong.lat}, {latlong.long}")

        if _reversed is None:
            raise Exception(f"reverser function returned None")

        location: dict[str, Any] = _reversed.raw

    except Exception as reverr:
        return (
            False,
            f"error while reversing latlong ({Latlong}): {reverr.__class__.__name__} - {reverr}",
        )

    if debug:
        stderr.write(f"debug: {location=}\n")

    text: list[str] = _unique(
        [
            (
                ", ".join(
                    [
                        d
                        for d in _unique(
                            [
                                location["address"].get(detail, None)
                                for detail in (
                                    "emergency, historic, military, natural, landuse, place, railway, "
                                    "man_made, aerialway, boundary, amenity, aeroway, club, craft, "
                                    "leisure, office, mountain_pass, shop, tourism, bridge, tunnel, waterway"
                                ).split(", ")
                            ]
                        )
                        if d is not None
                    ]
                )
            ).strip(",  "),
            (
                location["address"].get("building")
                if (
                    location["address"].get("building")
                    != location["address"].get("house_number")
                )
                else None
            ),
            location["address"].get("highway"),
            (
                location["address"].get("house_number", "")
                + (" " + location["address"].get("house_name", "")).strip()
                + " "
                + location["address"].get("road", "")
                # + (
                #     ", " + location["address"].get("suburb", "")
                #     # dont repeat if suburb is mentioned in the road itself
                #     # 'Toa Payoh' in 'Lorong 1A Toa Payoh'
                #     if location["address"].get("suburb", "")
                #     not in location["address"].get("road", "")
                #     else None
                # )
            ).strip(),
            (
                ", ".join(
                    [
                        d
                        for d in _unique(
                            [
                                location["address"].get(detail, "")
                                for detail in (
                                    "residential, neighbourhood, allotments, quarter, "
                                    "city_district, district, borough, suburb, subdivision, "
                                    "municipality, city, town, village"
                                ).split(", ")
                            ]
                        )
                        if all(
                            [
                                d != "",
                                d not in location["address"].get("road", ""),
                                d
                                not in [
                                    location["address"].get(detail, "")
                                    for detail in (
                                        "region, state, state_district, county, "
                                        "state, country, continent"
                                    ).split(", ")
                                ],
                            ]
                        )
                    ]
                )
            ).strip(","),
            location["address"].get("postcode"),
            (
                ", ".join(
                    [
                        d
                        for d in _unique(
                            [
                                location["address"].get(detail, None)
                                for detail in (
                                    "region, state, state_district, county, "
                                    "state, country, continent"
                                ).split(", ")
                            ]
                        )
                        if d is not None
                    ]
                )
            ),
        ]
    )

    return True, "\n".join([d for d in text if ((d != None) and d != "")])


def parse_query(
    query: str, debug: bool = False
) -> tuple[Literal[True], str | Localcode | Latlong] | tuple[Literal[False], str]:
    """
    function that parses a string Plus Code, local code or latlong into a str,
    surplus.Localcode or surplus.Latlong respectively

    query: str
        string Plus Code, local code or latlong
    debug: bool = False
        prints query parsing information to stderr

    returns tuple[bool, str | Localcode | Latlong]
        (True, <str | Localcode | Latlong>)  - conversion was successful, second element is result
        (False, <str>) - conversion failed, str is error message
    """

    def _word_match(
        oquery: str, squery: list[str]
    ) -> tuple[Literal[True], str | Localcode | Latlong] | tuple[Literal[False], str]:
        """
        internal helper code reuse function

        looks through each 'word' and attempts to match to a Plus Code
        if found, remove from original query and strip of whitespace and commas
        use resulting stripped query as locality
        """

        pcode: str = ""

        for word in squery:
            if Validator().is_valid(word):
                pcode = word

                if Validator().is_full(word):
                    return True, word

        if pcode != "":  # found a pluscode
            locality = oquery.replace(pcode, "")
            locality = locality.strip().strip(",").strip()

            if debug:
                stderr.write(f"debug: {pcode=}, {locality=}\n")

            return True, Localcode(code=pcode, locality=locality)

        return False, "unable to find a pluscode/match to a format"

    squery = [word.strip(",").strip() for word in query.split()]

    if debug:
        stderr.write(f"debug: {squery=}\n")

    match squery:
        # attempt to match to conjoined latlong ('lat,long')
        case [a]:
            try:
                plat, plong = a.split(",")
                lat = float(plat)
                long = float(plong)

            except ValueError:
                return _word_match(oquery=query, squery=squery)

            else:
                return True, Latlong(lat=lat, long=long)

        # attempt to match to latlong ('lat, long')
        case [a, b]:
            try:
                lat = float(a)
                long = float(b)

            except ValueError:
                return _word_match(oquery=query, squery=squery)

            else:
                return True, Latlong(lat=lat, long=long)

        case _:
            return _word_match(oquery=query, squery=squery)


def handle_query(
    query: str | Localcode | Latlong, debug: bool = False
) -> tuple[Literal[True], Latlong] | tuple[Literal[False], str]:
    """
    function that gets returns a surplus.Latlong from a Plus Code string,
    surplus.Localcode or surplus.Latlong object.
    used after surplus.parse_query().

    query: str | Localcode | Latlong

    debug: bool = False

    returns tuple[bool, str | Latlong]
        (True, Latlong)  - conversion was successful, second element is latlong
        (False, <str>) - conversion failed, str is error message
    """
    lat: float = 0.0
    lon: float = 0.0

    if isinstance(query, Latlong):
        return True, query

    else:  # instances: str | Localcode
        str_pcode: str = ""

        if isinstance(query, Localcode):
            result = query.full_length()

            if not result[0]:
                return False, result[1]

            str_pcode = result[1]

        else:
            str_pcode = query

        try:
            pcode = PlusCode(str_pcode)

        except KeyError:
            return (
                False,
                "code given is not a full-length Plus Code (including area code), e.g.: 6PH58QMF+FX",
            )

        except Exception as pcderr:
            return (
                False,
                f"error while decoding Plus Code: {pcderr.__class__.__name__} - {pcderr}",
            )

        lat = pcode.area.center().lat
        lon = pcode.area.center().lon

        if debug:
            stderr.write(f"debug: {lat=}, {lon=}\n")

    return True, Latlong(lat=lat, long=lon)


def cli() -> None:
    parser = ArgumentParser(
        prog="surplus",
        description=__doc__[__doc__.find(":") + 2 : __doc__.find("\n", 1)],
    )
    parser.add_argument(
        "query",
        type=str,
        help="full-length Plus Code (6PH58QMF+FX), local code (8QMF+FX Singapore), or latlong (1.3336875, 103.7749375)",
        nargs="+",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        default=False,
        help="prints lat, long and reverser response dict to stderr",
    )
    args = parser.parse_args()

    stderr.write(
        f"surplus version {'.'.join([str(v) for v in VERSION])}"
        + (f", debug mode" if args.debug else "")
        + "\n"
    )

    if args.debug:
        stderr.write("debug: args.query='" + " ".join(args.query) + "'\n")

    query = parse_query(" ".join(args.query), debug=args.debug)
    if not query[0]:
        stderr.write(f"{query[-1]}\n")
        exit(1)

    result: tuple[bool, str] = surplus(query[-1], debug=args.debug)
    if not result[0]:
        stderr.write(f"{result[-1]}\n")
        exit(2)

    print(result[-1])


if __name__ == "__main__":
    cli()

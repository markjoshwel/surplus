"""
surplus: plus code to iOS-Shortcuts-like shareable text
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
from sys import stderr
from typing import Any, Callable, Final

from geopy.geocoders import Nominatim  # type: ignore
from pluscodes import PlusCode  # type: ignore

VERSION: Final[tuple[int, int, int]] = (1, 0, 0)


def surplus(
    pluscode: str,
    reverser: Callable = Nominatim(user_agent="surplus").reverse,
    debug: bool = False,
) -> tuple[bool, str]:
    """
    pluscode to shareable text conversion function

    pluscode: str
        pluscode as a string

    reverser: Callable = Nominatim(user_agent="surplus").reverser
        latlong to data function, accesses a dict from .raw attribute of return object
        function should be able to take a string with two floats

            # code used by surplus
            location: dict[str, Any] = reverser(f"{lat}, {lon}").raw

        dict should be similar to geopy's geocoder provider .raw dicts

    debug: bool = False
        prints lat, long and reverser response dict to stderr

    returns tuple[bool, str]
        (True, <str>)  - conversion was successful, str is resultant text
        (False, <str>) - conversion failed, str is error message
    """
    try:
        pcode = PlusCode(pluscode)
    except KeyError:
        return (
            False,
            "enter full-length plus code including area code, e.g.: 6PH58QMF+FX",
        )

    lat: float = pcode.area.center().lat
    lon: float = pcode.area.center().lon

    if debug:
        stderr.write(f"debug: {lat=}, {lon=}\n")

    try:
        location: dict[str, Any] = reverser(f"{lat}, {lon}").raw
    except Exception as reverr:
        return (
            False,
            f"error while reversing latlong ({lat},{lon}): {reverr.__class__.__name__} - {reverr}",
        )

    if debug:
        stderr.write(f"debug: {location=}\n")

    data: list[str] = [
        location["address"].get("shop"),
        location["address"].get("building"),
        location["address"].get("highway"),
        (
            location["address"].get("house_number", "")
            + " "
            + location["address"].get("road", "")
            + (
                ", " + location["address"].get("suburb", "")
                # dont repeat if suburb is mentioned in the road itself
                # 'Toa Payoh' in 'Lorong 1A Toa Payoh'
                if location["address"].get("suburb", "")
                not in location["address"].get("road")
                else ""
            )
        ).strip(),
        location["address"].get("neighbourhood", ""),
        location["address"].get("postcode"),
        location["address"].get("country"),
    ]

    return True, "\n".join([d for d in data if ((d != None) and d != "")])


def cli() -> None:
    parser = ArgumentParser(
        prog="surplus",
        description=__doc__[__doc__.find(":") + 2 : __doc__.find("\n", 1)],
    )
    parser.add_argument(
        "pluscode",
        type=str,
        help="full-length plus code including area code, e.g.: 6PH58QMF+FX",
    )
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        default=False,
        help="prints lat, long and reverser response dict to stderr",
    )
    args = parser.parse_args()

    stderr.write(f"surplus version {'.'.join([str(v) for v in VERSION])}\n")

    result: tuple[bool, str] = surplus(args.pluscode, debug=args.debug)
    if result[0] is False:
        stderr.write(f"{result[-1]}\n")
        exit(-1)

    print(result[-1])


if __name__ == "__main__":
    cli()

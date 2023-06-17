"""
surplus test runner
-------------------
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

from sys import stderr
from textwrap import indent
from traceback import format_exception
from typing import Final, NamedTuple

import surplus

INDENT: Final[int] = 3


class ContinuityTest(NamedTuple):
    query: str
    expected: str


class TestFailure(NamedTuple):
    test: ContinuityTest
    exception: Exception
    output: str


tests: list[ContinuityTest] = [
    ContinuityTest(
        query="8RPQ+JW Singapore",
        expected=(
            "Caldecott Stn Exit 4\n" "Toa Payoh Link\n" "298106\n" "Central, Singapore"
        ),
    ),
    ContinuityTest(
        query="9R3J+R9 Singapore",
        expected=(
            "Thomson Plaza\n"
            "301 Upper Thomson Road\n"
            "Sin Ming, Bishan\n"
            "574408\n"
            "Central, Singapore"
        ),
    ),
    ContinuityTest(
        query="3RQ3+HW3 Pemping, Batam City, Riau Islands, Indonesia",
        expected=("Batam\n" "Kepulauan Riau, Indonesia"),
    ),
    ContinuityTest(
        query="CQPP+QM9 Singapore",
        expected=(
            "Woodlands Integrated Transport Hub\n" "738343\n" "Northwest, Singapore"
        ),
    ),
    ContinuityTest(
        query="8RRX+75Q Singapore",
        expected=(
            "Braddell Station/Blk 106\n"
            "Lorong 1 Toa Payoh\n"
            "319758\n"
            "Central, Singapore"
        ),
    ),
]


class SurplusFailure(Exception):
    ...


class QueryParseFailure(Exception):
    ...


class ContinuityFailure(Exception):
    ...


def main() -> int:
    failures: list[TestFailure] = []

    for idx, test in enumerate(tests, start=1):
        print(f"[{idx}/{len(tests)}] {test.query}")
        output: str = ""

        try:
            query = surplus.parse_query(query=test.query)

            if query[0] is False:
                raise QueryParseFailure(f"test query parse result returned False")

            result = surplus.surplus(query=query[1])

            if result[0] is False:
                raise SurplusFailure(result[1])

            output = result[1]

            stderr.write(indent(text=output, prefix=INDENT * " ") + "\n")

            if output != test.expected:
                raise ContinuityFailure(f"test did not match output")

        except Exception as exc:
            failures.append(TestFailure(test=test, exception=exc, output=output))
            stderr.write(indent(text="(fail)", prefix=INDENT * " ") + "\n")

        else:
            stderr.write(indent(text="(pass)", prefix=INDENT * " ") + "\n\n")

    if len(failures) > 0:
        print(f"\n--- failures ---\n")

    for fail in failures:
        print(
            f"[{tests.index(fail.test) + 1}/({len(tests)})] {fail.test.query}\n"
            + (
                indent("\n".join(format_exception(fail.exception)), prefix=INDENT * " ")
                + "\n"
            )
            + (indent(text="Expected:", prefix=INDENT * " ") + "\n")
            + (indent(text=repr(fail.test.expected), prefix=(2 * INDENT) * " ") + "\n")
            + (indent(text=fail.test.expected, prefix=(2 * INDENT) * " ") + "\n\n")
            + (indent(text="Actual:", prefix=INDENT * " ") + "\n")
            + (indent(text=repr(fail.output), prefix=(2 * INDENT) * " ") + "\n")
            + (indent(text=fail.output, prefix=(2 * INDENT) * " "))
        )

    print(f"\ncomplete: {len(tests) - len(failures)} passed, {len(failures)} failed")

    return len(failures)


if __name__ == "__main__":
    exit(main())

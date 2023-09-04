# type: ignore

"""
surplus test runner
-------------------
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

from io import StringIO
from sys import stderr
from textwrap import indent
from traceback import format_exception
from typing import Final, NamedTuple

import surplus

INDENT: Final[int] = 3
MINIMUM_PASS_RATE: Final[float] = 0.7  # because results can be flaky


class ContinuityTest(NamedTuple):
    query: str
    expected: list[str]


class TestFailure(NamedTuple):
    test: ContinuityTest
    exception: Exception
    output: str
    stderr: StringIO


tests: list[ContinuityTest] = [
    ContinuityTest(
        query="8R3M+F8 Singapore",
        expected=("Wisma Atria\n" "435 Orchard Road\n" "238877\n" "Central, Singapore"),
    ),
    ContinuityTest(
        query="9R3J+R9 Singapore",
        expected=[
            (
                "Thomson Plaza\n"
                "301 Upper Thomson Road\n"
                "Sin Ming, Bishan\n"
                "574408\n"
                "Central, Singapore"
            )
        ],
    ),
    ContinuityTest(
        query="3RQ3+HW3 Pemping, Batam City, Riau Islands, Indonesia",
        expected=[
            ("Batam\n" "Kepulauan Riau, Indonesia"),
            ("Batam\n" "Sumatera, Kepulauan Riau, Indonesia"),
        ],
    ),
    ContinuityTest(
        query="St Lucia, Queensland, Australia G227+XF",
        expected=[
            (
                "The University of Queensland\n"
                "Macquarie Street\n"
                "St Lucia, Greater Brisbane\n"
                "4072\n"
                "Queensland, Australia"
            ),
            (
                "The University of Queensland\n"
                "Eleanor Schonell Bridge\n"
                "St Lucia, Greater Brisbane, Dutton Park\n"
                "4072\n"
                "Queensland, Australia"
            ),
        ],
    ),
    ContinuityTest(
        query="Ngee Ann Polytechnic, Singapore",
        expected=(
            "Ngee Ann Polytechnic\n"
            "535 Clementi Road\n"
            "Bukit Timah\n"
            "599489\n"
            "Northwest, Singapore"
        ),
    ),
    ContinuityTest(
        query="1.3521, 103.8198",
        expected=(
            "MacRitchie Nature Trail\n"
            "Central Water Catchment\n"
            "574325\n"
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

        test_stderr = StringIO()

        output: str = ""
        behaviour = surplus.Behaviour(test.query, stderr=test_stderr, debug=True)

        try:
            query = surplus.parse_query(behaviour)

            if not query:
                raise QueryParseFailure(query.cry())

            result = surplus.surplus(query.get(), behaviour)

            if not result:
                raise SurplusFailure(result.cry())

            output = result.get()

            if output not in test.expected:
                raise ContinuityFailure("did not match any expected outputs")

        except Exception as exc:
            failures.append(
                TestFailure(test=test, exception=exc, output=output, stderr=test_stderr)
            )
            stderr.write(indent(text="(fail)", prefix=INDENT * " ") + "\n\n")

        else:
            stderr.write(indent(text="(pass)", prefix=INDENT * " ") + "\n\n")

    if len(failures) > 0:
        print(f"\n--- failures ---\n")

    for fail in failures:
        print(
            f"[{tests.index(fail.test) + 1}/{len(tests)}] {fail.test.query}\n"
            + (
                indent("\n".join(format_exception(fail.exception)), prefix=INDENT * " ")
                + "\n"
            )
            + (indent(text="Expected:", prefix=INDENT * " "))
        )

        for expected_output in fail.test.expected:
            print(
                indent(text=repr(expected_output), prefix=(2 * INDENT) * " ")
                + "\n"
                + (indent(text=expected_output, prefix=(2 * INDENT) * " ") + "\n")
            )

        print(
            indent(text="Actual:", prefix=INDENT * " ")
            + "\n"
            + (indent(text=repr(fail.output), prefix=(2 * INDENT) * " ") + "\n")
            + (indent(text=fail.output, prefix=(2 * INDENT) * " ") + "\n\n")
            + (indent(text="stderr:", prefix=INDENT * " ") + "\n")
            + (indent(text=fail.stderr.getvalue(), prefix=(2 * INDENT) * " "))
        )

    passes = len(tests) - len(failures)
    pass_rate = passes / len(tests)

    print(
        f"complete: {passes} passed, {len(failures)} failed "
        f"({pass_rate * 100:.0f}%/{MINIMUM_PASS_RATE * 100:.0f}%)"
    )

    if pass_rate < MINIMUM_PASS_RATE:
        print("continuity pass rate is under minimum, test suite failed ;<")
        return 1

    print("continuity tests passed :>")
    return 0


if __name__ == "__main__":
    exit(main())

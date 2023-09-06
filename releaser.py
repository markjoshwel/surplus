"""
surplus: Google Maps Plus Code to iOS Shortcuts-like shareable text
-------------------------------------------------------------------
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

from datetime import datetime, timedelta, timezone
from os import getenv
from pathlib import Path
from subprocess import run


# NOTE: change this if surplus has moved
path_surplus = Path(__file__).parent.joinpath("./surplus/surplus.py")

build_time = datetime.now(timezone(timedelta(hours=8)))  # using SGT

_insert_build_branch = getenv(
    "SURPLUS_BUILD_BRANCH",
    run(
        "git branch --show-current",
        capture_output=True,
        text=True,
        shell=True,
    ).stdout.strip("\n"),
)
insert_build_branch = _insert_build_branch if _insert_build_branch != "" else "unknown"

insert_build_commit: str = run(
    "git rev-parse HEAD",
    capture_output=True,
    text=True,
    shell=True,
).stdout.strip("\n")

insert_build_datetime: str = repr(build_time).replace("datetime.", "")

# NOTE: change this if the respective lines in surplus.py have changed
targets: list[tuple[str, str]] = [
    (
        'VERSION_SUFFIX: Final[str] = "-local"',
        'VERSION_SUFFIX: Final[str] = ""',
    ),
    (
        'BUILD_BRANCH: Final[str] = "future"',
        f'BUILD_BRANCH: Final[str] = "{insert_build_branch}"',
    ),
    (
        'BUILD_COMMIT: Final[str] = "latest"',
        f'BUILD_COMMIT: Final[str] = "{insert_build_commit}"',
    ),
    (
        "BUILD_DATETIME: Final[datetime] = datetime.now(timezone(timedelta(hours=8)))  # using SGT",
        f"BUILD_DATETIME: Final[datetime] = {insert_build_datetime}",
    ),
]


def main() -> int:
    assert path_surplus.is_file() and path_surplus.exists(), f"{path_surplus} not found"

    source_surplus: str = path_surplus.read_text(encoding="utf-8")

    for old, new in targets:
        print(f"new: {new}\nold: {old}\n")
        source_surplus = source_surplus.replace(old, new)

    path_surplus.write_text(source_surplus, encoding="utf-8")

    return 0


if __name__ == "__main__":
    exit(main())

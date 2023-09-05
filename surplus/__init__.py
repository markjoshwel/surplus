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

# surplus was and would've been a single-file module, but typing is in the way :(
# https://github.com/python/typing/issues/1333

from .surplus import (
    EMPTY_LATLONG,
    SHAREABLE_TEXT_LINE_0_KEYS,
    SHAREABLE_TEXT_LINE_1_KEYS,
    SHAREABLE_TEXT_LINE_2_KEYS,
    SHAREABLE_TEXT_LINE_3_KEYS,
    SHAREABLE_TEXT_LINE_4_KEYS,
    SHAREABLE_TEXT_LINE_5_KEYS,
    SHAREABLE_TEXT_LINE_6_KEYS,
    SHAREABLE_TEXT_NAMES,
    USER_AGENT,
    VERSION,
    Behaviour,
    ConversionResultTypeEnum,
    EmptyQueryError,
    IncompletePlusCodeError,
    Latlong,
    LatlongParseError,
    LatlongQuery,
    LocalCodeQuery,
    NoSuitableLocationError,
    PlusCodeNotFoundError,
    PlusCodeQuery,
    Query,
    Result,
    ResultType,
    StringQuery,
    SurplusException,
    UnavailableFeatureError,
    cli,
    default_geocoder,
    default_reverser,
    handle_args,
    parse_query,
    surplus,
)

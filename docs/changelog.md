# changelog

## surplus v2024.0.0

(unreleased)

!!! information
    this is a tentative release. surplus is currently versioned as `2024.0.0-beta`, as its
    behaviour is not stabilized

!!! warning
    this is an api-breaking release. see 'the great api break'.
    command-line usage of surplus has not changed

### what's new

- added flag `--show-user-agent`, printing the fingerprinted user agent string and exiting

### what's changed

- `default_geocoder()` and `default_reverser()` have been deprecated since v2.1.0 and are now
    removed. use the `SurplusDefaultGeocoding` class instead
- `SurplusException` is now `SurplusError`

### the great api break

TODO

### thanks!

- [vlshields](https://github.com/vlshields/) for their support with a drink!

full changelog: <https://github.com/markjoshwel/surplus/compare/v2.2.0...v2024.0.0>

## surplus on wheels v2

(released on the 1st of July 2024 on tag `v2.2024.25+spow`)

### changes

- you can now customize command invocations with `SURPLUS_CMD` and `LOCATION_CMD` environment variables
- surplus on wheels will purge logs when setting the `SPOW_PRIVATE` environment flag

### thanks!

- [vlshields](https://github.com/vlshields/) for their support with a drink!

---

## surplus on wheels: WhatsApp Bridge v2.2024.25

(released on the 17th of June 2024 on tag `v2.2024.25+spow-whatsapp-bridge`)

!!! note
    from henceforth, the WhatsApp Bridge is now versioned with a modified calendar versioning scheme
    of `MAJOR.YEAR.ISOWEEK`, where the `MAJOR` version segment will be bumped with codebase changes,
    whereas the `YEAR` and `ISOWEEK` segments will represent the time of which the release was
    built at

### changes

- updated dependencies to latest versions
- added `pair-phone` and `reconnect` subcommands
- TODO added optional helper script to auto-update to newer versions via a user-made daily cron job

### thanks!

- [vlshields](https://github.com/vlshields/) for their support with a drink!

---

## surplus on wheels: Telegram Bridge v2.2024.25

(released on the 17th of June 2024 on tag `v2.2024.25+spow-telegram-bridge`)

!!! note
    from henceforth, the Telegram Bridge will automatically release a new version once a week if
    there are updates to its dependencies
    
    as such, the bridge is now versioned with a modified calendar versioning scheme of
    `MAJOR.YEAR.ISOWEEK`, where the `MAJOR` version segment will be bumped with codebase changes,
    whereas the `YEAR` and `ISOWEEK` segments will represent the time of which the release was
    built at

### changes

- updated dependencies to latest versions
- added `logout` subcommand
- TODO added optional helper script to auto-update to newer versions via a user-made daily cron job

### thanks!

- [vlshields](https://github.com/vlshields/) for their support with a drink!

---

## surplus on wheels v1

initial release on the 9th of November 2023

---

## surplus on wheels: WhatsApp Bridge v1

initial release on the 7th of November 2023

---

## surplus on wheels: Telegram Bridge v1

initial release on the 7th of November 2023

---

## surplus v2.2.0

(released on the 14th of October 2023)

!!! warning
    constants are changed in this update!

fixed a bug installing surplus on Python 3.12 and italian sharetext fixes

### what's new

- special key arrangements for malaysia
- support for termux-location json input

### what's fixed

- fixed typing-extensions as an unwritten dependency  
  this also fixes a bug in not being able to run surplus in Python 3.12
- fixed italian key arrangements [#34](https://github.com/markjoshwel/surplus/pull/34)

### what's changed

- **`SHAREABLE*` constants are now dictionaries, see api docs for more information**

<https://github.com/markjoshwel/surplus/compare/v2.1.1...v2.2.0>

---

## surplus v2.1.1 

(released on the 19th of September 2023)

fix roads not coming first in Italian addresses (#31)

- documentation enhancements
    - remove self in `SurplusReverserProtocol` conforming signature
    - fix mismatching carets and add info on `split_iso3166_2`
- alternative line 3 arrangement for IT/Italy in [#31](https://github.com/markjoshwel/surplus/pull/31)

<https://github.com/markjoshwel/surplus/compare/v2.1.0...v2.1.1>

---

## surplus v2.1.0

(released on the 6th of September 2023)

!!! warning
    there are backwards-compatible api changes in this release.

type-to-type location representation conversions and quality of life changes/fixes

- **`default_geocoder()` and `default_reverser()` functions have been deprecated in favour of the
  new [`SurplusDefaultGeocoding` class](https://github.com/markjoshwel/surplus/tree/main#class-surplusdefaultgeocoding)**
- add reading from stdin when query is "-" in [#23](https://github.com/markjoshwel/surplus/pull/23)
- type to type conversion in [#24](https://github.com/markjoshwel/surplus/pull/24)
- fix local codes not being recognised if split with comma in [#29](https://github.com/markjoshwel/surplus/pull/29)
- more verbose -v/--version information in [#21](https://github.com/markjoshwel/surplus/pull/21)

<https://github.com/markjoshwel/surplus/compare/v2.0.1...v2.1.0>

---

## surplus v2.0.1

(released on the 5th of September 2023)

- expose surplus.Result in `__init__.py` by in [#28](https://github.com/markjoshwel/surplus/pull/28)

<https://github.com/markjoshwel/surplus/compare/v2.0.0...v2.0.1>

---

## surplus v2.0.0

(released on the 3rd of September 2023)

!!! warning
    this is an api-breaking release. see 'the great api break'.
    command-line usage of surplus has not changed

!!! information
    python 3.11 or later is required due to a bug in earlier versions
    [(python/cpython#88089)](https://github.com/python/cpython/issues/88089)

complete rewrite and string query support

### changes

- surplus has been fully rewritten in [#19](https://github.com/markjoshwel/surplus/pull/19)
- support for string queries
  ```text
  $ s+ Wisma Atria
  surplus version 2.0.0
  Wisma Atria
  435 Orchard Road
  238877
  Central, Singapore
  ```
- mypy will now recognise surplus as a typed module
- **python 3.11 is now the minimum version**

### the great api break

#### what is new

- nominatim keys are now stored in tuple constants
- surplus exception classes are now a thing
- surplus functions now operate using a unified `Behaviour` object
- surplus functions now return a `Result` object for safer value retrieval instead of the previous
  `(bool, value)` tuple
- dedicated NamedTuple classes for each query type 

#### what has been removed

- `surplus.handle_query()`

  instead, use `.to_lat_long_coord()` on your surplus 2.x query object

#### what has remained

- `surplus.surplus()`, the function
- `surplus.parse_query()`, the function

#### what has changed

- `surplus.surplus()`
    1. `reverser` and `debug` arguments are now under the unified `surplus.Behaviour` object
    2. function now returns a `surplus.Result[str]` for safer error handling

- `surplus.parse_query()`
    1. `query` and `debug` arguments are now under the unified `surplus.Behaviour` object
    2. function now returns a `surplus.Result[surplus.Query]` for safer error handling

- `surplus.Latlong`  
    attributes `lat` and `long` have been renamed to `latitude` and `longitude` respectively

- `surplus.Localcode`  
    renamed to `surplus.LocalCodeQuery`

- `Localcode.full_length()`  
    renamed to `LocalCodeQuery.to_full_plus_code()`, and returns a `surplus.Result[str]` for safer
    error handling

full changelog: <https://github.com/markjoshwel/surplus/compare/v1.1.3...v2.0.0>

## surplus v1.1.3

(released on the 21st of June 2023)

general output fixes and quality of life updates

- ci(qc) workflow tweaks by [markjoshwel](https://github.com/markjoshwel) in [#13](https://github.com/markjoshwel/surplus/pull/13)
- cc: remove woodlands test + brackets by [markjoshwel](https://github.com/markjoshwel) in [#14](https://github.com/markjoshwel/surplus/pull/14)
- s+: display county before state by [markjoshwel](https://github.com/markjoshwel) in [#15](https://github.com/markjoshwel/surplus/pull/15)

<https://github.com/markjoshwel/surplus/compare/v1.1.2...v1.1.3>

---

## surplus v1.1.2

(released on the 18th of June 2023)

general output fixes and quality of life updates

- do not repeat details by [markjoshwel](https://github.com/markjoshwel) in #9
- add -v/--version flag by [markjoshwel](https://github.com/markjoshwel) in #11

<https://github.com/markjoshwel/surplus/compare/v1.1.0...v1.1.1>

---

## surplus v1.1.1

(released on the 16th of June 2023)

### changes

fixes and output tweaks

- fix reverser returning a None location by [shamsu07](https://github.com/shamsu07) in #5

### thanks!

- [shamsu07](https://github.com/shamsu07) made their first contribution!

<https://github.com/markjoshwel/surplus/compare/v1.1.0...v1.1.1>

---

## surplus v1.1.0

(released on the 3rd of June 2023)

short code and latitude longitude coordinate pair support!

- code: s+ alternative shorthand script
- code: handle none/list locations
- code: query by lat long support
- code: support shortcodes with localities
- code: implement more address detail tags from nominatim
- meta: slsa 3 compliance

<https://github.com/markjoshwel/surplus/compare/v1.0.0...v1.1.0>

---

## surplus v1.0.0

initial release on the 2nd of June 2023

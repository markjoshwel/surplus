# surplus

surplus is a Python script to convert
[Google Maps Plus Codes](https://maps.google.com/pluscodes/)
to iOS Shortcuts-like shareable text.

- [installation](#installation)
  - [on Termux: surplus on wheels](#on-termux-surplus-on-wheels)
- [usage](#usage)
  - [command-line usage](#command-line-usage)
  - [example api usage](#example-api-usage)
- [developer's guide](#developers-guide)
- [contributor's guide](#contributors-guide)
  - [reporting incorrect output](#reporting-incorrect-output)
    - [the reporting process](#the-reporting-process)
    - [what counts as "incorrect"](#what-counts-as-incorrect)
- [output technical details](#the-technical-details-of-surpluss-output)
- [api reference](#api-reference)
  - [details on the fingerprinted user agent](#details-on-the-fingerprinted-user-agent)
- [licence](#licence)

```text
$ surplus 9R3J+R9 Singapore
surplus version 2.2.0
Thomson Plaza
301 Upper Thomson Road
Sin Ming, Bishan
574408
Central, Singapore
```

## installation

> [!IMPORTANT]  
> python 3.11 or later is required due to a bug in earlier versions.
> [(python/cpython#88089)](https://github.com/python/cpython/issues/88089)

for most, you can install surplus built from the latest stable release:

```text
pip install https://github.com/markjoshwel/surplus/releases/latest/download/surplus-latest-py3-none-any.whl
```

or directly from the repository using pip:

```text
pip install git+https://github.com/markjoshwel/surplus.git@main
```

surplus is also a public domain dedicated [single python file](surplus/surplus.py), so
feel free to grab that and embed it into your own program as you see fit.

see [licence](#licence) for licensing information.

### on Termux: surplus on wheels

surplus on wheels (s+ow) is a pure shell script to get your location using
`termux-location`, process it through surplus, and send it to a WhatsApp user/group using a
[modified mdtest demonstration binary from the tulir/whatsmeow project](https://github.com/markjoshwel/whatsmeow-termux/tree/main/mdtest).

> [!IMPORTANT]  
> if you just want to use surplus by itself, follow the normal installation guide above.

there are two ways to install and setup s+ow:

- [by itself](#by-itself)
- or [with an hourly cronjob](#with-an-hourly-cronjob)

see [s+ow usage instructions here](#using-sow).

#### by itself

1. firstly install python and termux-api if you haven't already:

   ```text
   pkg install python termux-api
   ```

   also install the accompanying the Termux:API app from [F-Froid](https://f-droid.org/en/packages/com.termux.api/).

2. install surplus:

   ```text
   pip install https://github.com/markjoshwel/surplus/releases/latest/download/surplus-latest-py3-none-any.whl
   ```

3. install the modified mdtest binary for aarch64:

   ```text
   wget https://github.com/markjoshwel/whatsmeow-termux/releases/latest/download/mdtest.tar.gz
   tar -xvf mdtest.tar.gz
   chmod +x mdtest
   mkdir -p ~/.local/bin/
   mv mdtest ~/.local/bin/
   rm mdtest.tar.gz
   ```

4. install surplus on wheels:

   ```text
   mkdir -p ~/.local/bin/
   curl https://raw.githubusercontent.com/markjoshwel/surplus/s+ow/s+ow > ~/.local/bin/s+ow
   chmod +x ~/.local/bin/s+ow
   ```

if `~/.local/bin` is not in your `$PATH`, add the following to your shell's rc file:

```shell
export PATH="$HOME/.local/bin:$PATH"
```

#### with an hourly cronjob

> [!IMPORTANT]  
> these instructions rely on following the previous instructions, and assumes that s+ow works.

1. install necessary packages to run cron jobs:

   ```text
   pkg install cronie termux-services
   ```

2. restart termux and start the cron service:

   ```text
   sv-enable cron
   ```

3. setup the cron job:

   > [!IMPORTANT]  
   > fill in the `JID_NOMINAL_TARGET` and `JID_ERRORED_TARGET` variables before running s+ow.  
   > [(see using s+ow)](#using-sow)

   run the following command:

   ```text
   crontab -e
   ```

   and add the following text:

   ```text
   59 * * * *      (sleep 30; JID_NOMINAL_TARGET="" JID_ERRORED_TARGET="" LOCATION_PRIORITISE_NETWORK=n SPOW_CRON=y ~/.local/bin/s+ow)
   ```

   this will run s+ow every hour, thirty seconds before a new hour. modify the variables
   as per your needs. see [using s+ow](#using-sow) for more information.

#### using s+ow

for first-time setup of mdtest, run the following command and pair your WhatsApp account
with mdtest:

```text
~/.local/bin/s+ow mdtest
```

wait for mdtest to sync with WhatsApp. you can safely leave after a minute or after the
console stops moving. whichever comes first.

s+ow uses two environment variables:

1. `JID_NOMINAL_TARGET`  
   JID of the WhatsApp user/group to send the location to if everything runs correctly.

2. `JID_ERRORED_TARGET`  
   JID of the WhatsApp user/group to send the stderr/logs to if something goes wrong.

3. `SPOW_CRON`  
   set as non-empty to declare that s+ow is being run as a cron job.  
   cron jobs are run thirty seconds in advance to attempt to display surplus output
   on time as waiting for a GPS lock may be slow.

4. `LOCATION_PRIORITISE_NETWORK`  
   set as non-empty to declare that s+ow can just use network location instead of GPS
   if GPS is taking too long.  
   you should only turn this on if punctuality means that much to you, or you’re in a
   country with cell towers close by or everywhere, like Singapore.

   setting it to `n` will also be treated as empty.

the JIDs can be obtained by sending a message to the user/group, while running
`s+ow mdtest`, and examining the output for your message. JIDs are email address-like
strings.

you can fake your s+ow messages by either:

1. setting a dummy `last` file in s+ow cache

   `$HOME/.cache/s+ow/last` is used as the fallback response when a part of s+ow (either
   `termux-location` or `surplus` errors out). you can set this file to whatever you want
   and just disable location permissions for Termux.

2. setting a `fake` file in s+ow cache

   > [!IMPORTANT]  
   > this is currently unimplemented.

   you can also write text to `$HOME/.cache/s+ow/fake` to fake upcoming messages. the file
   is delimited by two newlines. as such, arrange the file like so:

   ```text
   The Clementi Mall
   3155 Commonwealth Avenue West
   Westpeak Terrace
   129588
   Southwest, Singapore

   Westgate
   3 Gateway Drive
   Jurong East
   608532
   Southwest, Singapore

   ...
   ```

   on every run of s+ow, the first group of lines will be consumed, and the file will be
   updated with the remaining lines. if the file is empty, it will be deleted.

#### quick install scripts

> [!WARNING]  
> these scripts assume you're starting from a fresh base install of Termux.
> if you have already cron jobs, then manually carry out the instructiions in
> [with an hourly cronjob](#with-an-hourly-cronjob).

1. setup s+ow:

   ```text
   curl https://raw.githubusercontent.com/markjoshwel/surplus/s+ow/termux-s+ow-setup | sh
   ```

2. restart termux

3. setup cron job:

   ```text
   curl https://raw.githubusercontent.com/markjoshwel/surplus/s+ow/termux-s+ow-setup-cron | sh
   ```

you can then run `crontab -e` to edit the variables as per your needs.  
see [using s+ow](#using-sow) for more information.

## usage

### command-line usage

```text
usage: surplus [-h] [-d] [-v] [-c {pluscode,localcode,latlong,sharetext}]
               [-u USER_AGENT] [-t]
               [query ...]

Google Maps Plus Code to iOS Shortcuts-like shareable text

positional arguments:
  query                 full-length Plus Code (6PH58QMF+FX), shortened
                        Plus Code/'local code' (8QMF+FX Singapore),
                        latlong (1.3336875, 103.7749375), string query
                        (e.g., 'Wisma Atria'), or '-' to read from stdin

options:
  -h, --help            show this help message and exit
  -d, --debug           prints lat, long and reverser response dict to
                        stderr
  -v, --version         prints version information to stderr and exits
  -c {pluscode,localcode,latlong,sharetext}, --convert-to {pluscode,localcode,latlong,sharetext}
                        converts query a specific output type, defaults
                        to 'sharetext'
  -u USER_AGENT, --user-agent USER_AGENT
                        user agent string to use for geocoding service,
                        defaults to fingerprinted user agent string
  -t, --using-termux-location
                        treats input as a termux-location output json
                        string, and parses it accordingly
```

### example api usage

here are a few examples to get you quickly started using surplus in your own program:

1. let surplus do the heavy lifting

   ```python
   >>> from surplus import surplus, Behaviour
   >>> result = surplus("Ngee Ann Polytechnic, Singapore", Behaviour())
   >>> result.get()
   'Ngee Ann Polytechnic\n535 Clementi Road\nBukit Timah\n599489\nNorthwest, Singapore'
   ```

2. handle queries separately

   ```python
   >>> import surplus
   >>> behaviour = surplus.Behaviour("6PH58R3M+F8")
   >>> query = surplus.parse_query(behaviour)
   >>> result = surplus.surplus(query.get(), behaviour)
   >>> result.get()
   'MacRitchie Nature Trail\nCentral Water Catchment\n574325\nCentral, Singapore'
   ```

3. start from a Query object

   ```python
   >>> import surplus
   >>> localcode = surplus.LocalCodeQuery(code="8R3M+F8", locality="Singapore")
   >>> pluscode_str = localcode.to_full_plus_code(geocoder=surplus.default_geocoder).get()
   >>> pluscode = surplus.PlusCodeQuery(pluscode_str)
   >>> result = surplus.surplus(pluscode, surplus.Behaviour())
   >>> result.get()
   'Wisma Atria\n435 Orchard Road\n238877\nCentral, Singapore'
   ```

notes:

- you can change what surplus does when passing in a custom [`Behaviour`](#class-behaviour)
  object

- most surplus functions return a [`Result`](#class-result) object. while you can
  call [`.get()`](#resultget) to obtain the proper return value, this is dangerous and
  might raise an exception

see the [api reference](#api-reference) for more information.

## developer's guide

prerequisites:

- [Python >=3.11](https://www.python.org/)
- [Poetry](https://python-poetry.org/)

alternatively, use [devbox](https://get.jetpack.io/devbox) for a hermetic development environment powered by [Nix](https://nixos.org/).

```text
devbox shell    # skip this if you aren't using devbox
poetry install
poetry shell
```

for information on surplus's exposed api, see the [api reference](#api-reference).

## contributor's guide

1. fork the repository and branch off from the `future` branch
2. make and commit your changes!
3. pull in any changes from `future`, and resolve any conflicts, if any
4. **commit your copyright waiver** (_see below_)
5. submit a pull request (_or mail in a diff_)

when contributing your first changes, please include an empty commit for a copyright
waiver using the following message (replace 'Your Name' with your name or nickname):

```text
Your Name Copyright Waiver

I dedicate any and all copyright interest in this software to the
public domain.  I make this dedication for the benefit of the public at
large and to the detriment of my heirs and successors.  I intend this
dedication to be an overt act of relinquishment in perpetuity of all
present and future rights to this software under copyright law.
```

the command to create an empty commit is `git commit --allow-empty`

### reporting incorrect output

> [!NOTE]  
> this section is independent of the rest of the contributing section.

different output from the iOS Shortcuts app is expected, however incorrect output is not.

#### the reporting process

open an issue in the
[repositories issue tracker](https://github.com/markjoshwel/surplus/issues/new),
and do the following:

1. ensure that your issue is not an error of incorrect data returned by your reverser
   function, which by default is OpenStreetMap Nominatim.
   (_don't know what the above means? then you are using the default reverser._)

   also look at the ['what counts as "incorrect"'](#what-counts-as-incorrect) section
   before moving on.

2. include the erroneous query.
   (_the Plus Code/local code/latlong coordinate/query string you passed into surplus_)

3. include output from the terminal with the
   [`--debug` flag](#command-line-usage) passed to the surplus CLI or with
   `debug=True` set in function calls.

   > [!NOTE]  
   > if you are using the surplus API and have passed custom stdout and stderr parameters
   > to redirect output, include that instead.

4. how it should look like instead, with reasoning if the error is not obvious. (e.g.,
   missing details)

   for reference, see how the following issues were written:

   - [issue #4: "Incorrect format: repeated lines"](https://github.com/markjoshwel/surplus/issues/4)
   - [issue #6: "Incorrect format: missing details"](https://github.com/markjoshwel/surplus/issues/6)
   - [issue #12: "Incorrect format: State before county"](https://github.com/markjoshwel/surplus/issues/12)

#### what counts as "incorrect"

- **example** (correct)

  - iOS Shortcuts Output

    ```text
    Plaza Singapura
    68 Orchard Rd
    238839
    Singapore
    ```

  - surplus Output

    ```text
    Plaza Singapura
    68 Orchard Road
    Museum
    238839
    Central, Singapore
    ```

  this _should not_ be reported as incorrect, as the only difference between the two is
  that surplus displays more information.

other examples that _should not_ be reported are:

- name of place is incorrect/different

  this may be due to incorrect data from the geocoder function, which is OpenStreetMap
  Nominatim by default. in the case of Nominatim, it means that the data on OpenStreetMap
  is incorrect.

  (_if so, then consider updating OpenStreetMap to help not just you, but other surplus
  and OpenStreetMap users!_)

**you should report** when the output does not make logical sense, or something similar
wherein the output of surplus is illogical to read or is not correct in the traditional
sense of a correct address.

see the linked issues in [the reporting process](#the-reporting-process) for examples
of incorrect outputs.

## the technical details of surplus's output

> [!NOTE]  
> this is a breakdown of surplus's output when converting to shareable text.
> when converting to other output types, output may be different.

```text
$ s+ --debug 8QJF+RP Singapore
surplus version 2.2.0, debug mode (latest@future, Tue 05 Sep 2023 23:38:59 +0800)
debug: parse_query: behaviour.query=['8QJF+RP', 'Singapore']
debug: _match_plus_code: portion_plus_code='8QJF+RP', portion_locality='Singapore'
debug: cli: query=Result(value=LocalCodeQuery(code='8QJF+RP', locality='Singapore'), error=None)
debug: latlong_result.get()=Latlong(latitude=1.3320625, longitude=103.7743125)
debug: location={...}
debug: _generate_text: split_iso3166_2=['SG', '03']
debug: _generate_text: using special key arrangements for 'SG-03' (Singapore)
debug: _generate_text: seen_names=['Ngee Ann Polytechnic', 'Clementi Road']
debug: _generate_text_line: [True]               -> True   --------  'Ngee Ann Polytechnic'
debug: _generate_text_line: [True]               -> True   --------  '535'
debug: _generate_text_line: [True]               -> True   --------  'Clementi Road'
debug: _generate_text_line: [True, True]         -> True   --------  'Bukit Timah'
debug: _generate_text_line: [False, True]        -> False  filtered  'Singapore'
debug: _generate_text_line: [True]               -> True   --------  '599489'
debug: _generate_text_line: [True]               -> True   --------  'Northwest'
debug: _generate_text_line: [True]               -> True   --------  'Singapore'
0       Ngee Ann Polytechnic
1
2
3       535 Clementi Road
4       Bukit Timah
5       599489
6       Northwest, Singapore
Ngee Ann Polytechnic
535 Clementi Road
Bukit Timah
599489
Northwest, Singapore
```

variables

- **variables `behaviour.query`, `split_query` and `original_query`**

  (_`split_query` and `original_query` are only shown if query is a latlong coordinate
  or query string_)

  `behaviour.query` is the original query string or a list of strings from space-splitting the original query
  string passed to [`parse_query()`](#def-parse_query) for parsing

  `split_query` is the original query string split by spaces

  `original_query` is a single non-split string

  ```text
  $ s+ Temasek Polytechnic
       -------------------
       query

  behaviour.query -> ['Temasek', 'Polytechnic']
  split_query     -> ['Temasek', 'Polytechnic']
  original_query  -> 'Temasek Polytechnic'
  ```

  ```text
  >>> surplus("77Q4+7X Austin, Texas, USA", surplus.Behaviour())

  behaviour.query -> '77Q4+7X Austin, Texas, USA'
  split_query     -> ['77Q4+7X', 'Austin,', 'Texas,', 'USA']
  original_query  -> '77Q4+7X Austin, Texas, USA'
  ```

- **variables `portion_plus_code` and `portion_locality`**

  (_only shown if the query is a local code, not shown on full-length Plus Codes,
  latlong coordinates or string queries_)

  represents the Plus Code and locality portions of a
  [shortened Plus Code](https://en.wikipedia.org/wiki/Open_Location_Code#Common_usage_and_shortening)
  (_referred to as a "local code" in the codebase_) respectively

- **variable `query`**

  query is a variable of type [`Result`](#class-result)[`[Query]`](#query)

  this variable is displayed to show what query type [`parse_query()`](#def-parse_query) has
  recognised, and if there were any errors during query parsing

- **expression `latlong_result.get()=`**

  (_only shown if the query is a Plus Code_)

  the latitude longitude coordinates derived from the Plus Code

- **variable `location`**

  the response dictionary from the reverser function passed to
  [`surplus()`](#def-surplus)

  for more information on the reverser function, see
  [`SurplusReverserProtocol`](#surplusreverserprotocol)

- **variable `split_iso3166_2` and special key arrangements**

  a list of strings containing the split iso3166-2 code (country/subdivision identifier)

  if special key arrangements are available for the code, a line similar to the following
  will be shown:

  ```text
  debug: _generate_text: using special key arrangements for 'SG-03' (Singapore)
  ```

- **variable `seen_names`**

  a list of unique important names found in certain Nominatim keys used in final output
  lines 0-3

- **`_generate_text_line` seen name checks**

  ```text
  #                           filter function boolean list   status    element
  #                           =============================  ========  ======================
  debug: _generate_text_line: [True]               -> True   --------  'Ngee Ann Polytechnic'
  debug: _generate_text_line: [False, True]        -> False  filtered  'Singapore'
  ```

  a check is done on shareable text line 4 keys (`SHAREABLE_TEXT_LINE_4_KEYS` - general
  regional location) to reduce repeated elements found in `seen_names`

  reasoning is, if an element on line 4 (general regional location) is the exact same as
  a previously seen name, there is no need to include the element

  - **filter function boolean list**

    `_generate_text_line`, an internal function defined inside `_generate_text` can be
    passed a filter function as a way to filter out certain elements on a line

    ```python
    # the filter used in _generate_text, for line 4's seen name checks
    filter=lambda ak: [
        # everything here should be True if the element is to be kept
        ak not in general_global_info,
        not any(True if (ak in sn) else False for sn in seen_names),
    ]
    ```

    `general_global_info` is a list of strings containing elements from line 6. (general
    global information)

  - **status**

    what `all(filter(detail))` evaluates to, `filter` being the filter function passed to
    `_generate_text_line` and `detail` being the current element

  - **element**

    the current iteration from iterating through a list of strings containing elements
    from line 4. (general regional location)

line breakdown of shareable text output, accompanied by their Nominatim keys:

```text
0       name of a place
1       building name
2       highway name
3       block/house/building number, house name, road
4       general regional location
5       postal code
6       general global information
```

0. **name of a place**

   (_usually important places or landmarks_)

   - examples

     ```text
     The University of Queensland
     Ngee Ann Polytechnic
     Botanic Gardens
     ```

   - nominatim keys

     ```text
     emergency, historic, military, natural, landuse, place, railway, man_made,
     aerialway, boundary, amenity, aeroway, club, craft, leisure, office, mountain_pass,
     shop, tourism, bridge, tunnel, waterway
     ```

1. **building name**

   - examples

     ```text
     Novena Square Office Tower A
     Visitor Centre
     ```

   - nominatim keys

     ```text
     building
     ```

2. **highway name**

   - examples

     ```text
     Marina Coastal Expressway
     Lornie Highway
     ```

   - nominatim keys

     ```text
     highway
     ```

3. **block/house/building number, house name, road**

   - examples

     ```text
     535 Clementi Road
     Macquarie Street
     Braddell Road
     ```

   - nominatim keys

     ```text
     house_number, house_name, road
     ```

4. **general regional location**

   - examples

     ```text
     St Lucia, Greater Brisbane
     The Drag, Austin
     Toa Payoh Crest
     ```

   - nominatim keys

     ```text
     residential, neighbourhood, allotments, quarter, city_district, district, borough,
     suburb, subdivision, municipality, city, town, village
     ```

5. **postal code**

   - examples

     ```text
     310131
     78705
     4066
     ```

   - nominatim key

     ```text
     postcode
     ```

6. **general global information**

   - examples

     ```text
     Travis County, Texas, United States
     Southeast, Singapore
     Queensland, Australia
     ```

   - nominatim keys

     ```text
     region, county, state, state_district, country, continent
     ```

## api reference

- [constants](#constants)
- [exception classes](#exception-classes)
- [types](#types)
  - [`Query`](#query)
  - [`ResultType`](#resulttype)
  - [`SurplusGeocoderProtocol`](#surplusgeocoderprotocol)
  - [`SurplusReverserProtocol`](#surplusreverserprotocol)
- [`class Behaviour`](#class-behaviour)
- [`class SurplusDefaultGeocoding`](#class-surplusdefaultgeocoding)
  - [`SurplusDefaultGeocoding.update_geocoding_functions()`](#surplusdefaultgeocodingupdate_geocoding_functions)
  - [`SurplusDefaultGeocoding.geocoder()`](#surplusdefaultgeocodinggeocoder)
  - [`SurplusDefaultGeocoding.reverser()`](#surplusdefaultgeocodingreverser)
- [`class ConversionResultTypeEnum`](#class-conversionresulttypeenum)
- [`class Result`](#class-result)
  - [`Result.__bool__()`](#result__bool__)
  - [`Result.cry()`](#resultcry)
  - [`Result.get()`](#resultget)
- [`class Latlong`](#class-latlong)
  - [`Latlong.__str__()`](#latlong__str__)
- [`class PlusCodeQuery`](#class-pluscodequery)
  - [`PlusCodeQuery.to_lat_long_coord()`](#pluscodequeryto_lat_long_coord)
  - [`PlusCodeQuery.__str__()`](#pluscodequery__str__)
- [`class LocalCodeQuery`](#class-localcodequery)
  - [`LocalCodeQuery.to_full_plus_code()`](#localcodequeryto_full_plus_code)
  - [`LocalCodeQuery.to_lat_long_coord()`](#localcodequeryto_lat_long_coord)
  - [`LocalCodeQuery.__str__()`](#localcodequery__str__)
- [`class LatlongQuery`](#class-latlongquery)
  - [`LatlongQuery.to_lat_long_coord()`](#latlongqueryto_lat_long_coord)
  - [`LatlongQuery.__str__()`](#latlongquery__str__)
- [`class StringQuery`](#class-stringquery)
  - [`StringQuery.to_lat_long_coord()`](#stringqueryto_lat_long_coord)
  - [`StringQuery.__str__()`](#stringquery__str__)
- [`def surplus()`](#def-surplus)
- [`def parse_query()`](#def-parse_query)
- [`def generate_fingerprinted_user_agent`](#def-generate_fingerprinted_user_agent)
  - [details on the fingerprinted user agent](#details-on-the-fingerprinted-user-agent)

### constants

- `VERSION: tuple[int, int, int]`

  a tuple of integers representing the version of surplus, in the format
  `[major, minor, patch]`

- `VERSION_SUFFIX: typing.Final[str]`  
  `BUILD_BRANCH: typing.Final[str]`  
  `BUILD_COMMIT: typing.Final[str]`  
  `BUILD_DATETIME: typing.Final[datetime]`

  string and a [datetime.datetime](https://docs.python.org/3/library/datetime.html) object
  containing version and build information, set by [releaser.py](releaser.py)

- `CONNECTION_MAX_RETRIES: int = 9`  
  `CONNECTION_WAIT_SECONDS: int = 10`

  defines if and how many times to retry a connection, alongside how many seconds to wait
  in between tries, for Nominatim

  > [!NOTE]  
  > this constant only affects the default surplus Nominatim geocoding functions. custom
  > functions do not read from this, unless deliberately programmed to do so

- `SHAREABLE_TEXT_LINE_0_KEYS: dict[str, tuple[str, ...]]`  
  `SHAREABLE_TEXT_LINE_1_KEYS: dict[str, tuple[str, ...]]`  
  `SHAREABLE_TEXT_LINE_2_KEYS: dict[str, tuple[str, ...]]`  
  `SHAREABLE_TEXT_LINE_3_KEYS: dict[str, tuple[str, ...]]`  
  `SHAREABLE_TEXT_LINE_4_KEYS: dict[str, tuple[str, ...]]`  
  `SHAREABLE_TEXT_LINE_5_KEYS: dict[str, tuple[str, ...]]`  
  `SHAREABLE_TEXT_LINE_6_KEYS: dict[str, tuple[str, ...]]`

  a dictionary of iso3166-2 country-portion string keys with a tuple of Nominatim keys
  used in shareable text line 0-6 as their values

  ```python
  {
    "default": (...),
    "SG": (...,),
    ...
  }
  ```

- `SHAREABLE_TEXT_LINE_SETTINGS: dict[str, dict[int, tuple[str, bool]]]`

  a dictionary of iso3166-2 country-portion string keys with a dictionary as their values

  the dictionary values are dictionaries with integers as keys, and a tuple of two strings

  the first string is the separator string to use, and the second string is a boolean flag
  that if `True` will check the line for seen names

  ```python
  {
      "default": {
          0: (", ", False),
          ...
          6: (", ", False),
      },
      "IT": {
          0: (", ", False),
          ...
          6: (", ", False),
      },
      ...
  }
  ```

- `SHAREABLE_TEXT_NAMES: dict[str, tuple[str, ...]]`

  a dictionary of iso3166-2 country-portion string keys with a tuple of strings as their
  values
  a tuple of strings containing Nominatim keys used in shareable text line 0-2 and
  special keys in line 3

  used for seen name checks

- `SHAREABLE_TEXT_LOCALITY: dict[str, tuple[str, ...]]`

  a dictionary of iso3166-2 country-portion string keys with a tuple of strings as their
  values

  used when generating the locality portions of shortened Plus Codes/local codes

  ```python
  {
    "default": (...),
    "SG": (...,),
    ...
  }
  ```

- `SHAREABLE_TEXT_DEFAULT: typing.Final[str]`  
  constant for what is the "default" key in the `SHAREABLE*` constants

- `EMPTY_LATLONG: typing.Final[Latlong]`  
  a constant for an empty latlong coordinate, with latitude and longitude set to 0.0

### exception classes

- `class SurplusException(Exception)`  
  base skeleton exception for handling and typing surplus exception classes
- `class NoSuitableLocationError(SurplusException)`
- `class IncompletePlusCodeError(SurplusException)`
- `class PlusCodeNotFoundError(SurplusException)`
- `class LatlongParseError(SurplusException)`
- `class EmptyQueryError(SurplusException)`
- `class UnavailableFeatureError(SurplusException)`

### types

#### `Query`

```python
Query: typing.TypeAlias = PlusCodeQuery | LocalCodeQuery | LatlongQuery | StringQuery
```

[type alias](https://docs.python.org/3/library/typing.html#type-aliases) representing
either a
[`PlusCodeQuery`](#class-pluscodequery),
[`LocalCodeQuery`](#class-localcodequery),
[`LatlongQuery`](#class-latlongquery) or
[`StringQuery`](#class-stringquery)

#### `ResultType`

```python
ResultType = TypeVar("ResultType")
```

[generic type](https://docs.python.org/3/library/typing.html#generics) used by
[`Result`](#class-result)

#### `SurplusGeocoderProtocol`

[typing_extensions.Protocol](https://mypy.readthedocs.io/en/stable/protocols.html#callback-protocols)
class for documentation and static type checking of surplus geocoder functions

- **signature and conforming function signature**

  ```python
  class SurplusGeocoderProtocol(Protocol):
      def __call__(self, place: str) -> Latlong:
          ...
  ```

  functions that conform to this protocol should have the following signature:

  ```python
  def example(place: str) -> Latlong: ...
  ```

- **information on conforming functions**

  function takes in a location name as a string, and returns a [Latlong](#class-latlong).

  **function MUST supply a `bounding_box` attribute to the to-be-returned
  [Latlong](#class-latlong).** the bounding box is used when surplus shortens Plus Codes.

  function can and should be at minimum
  [`functools.lru_cache()`-wrapped](https://docs.python.org/3/library/functools.html#functools.lru_cache)
  if the geocoding service asks for caching

  exceptions are handled by the caller

#### `SurplusReverserProtocol`

[typing_extensions.Protocol](https://mypy.readthedocs.io/en/stable/protocols.html#callback-protocols)
class for documentation and static type checking of surplus reverser functions

- **signature and conforming function signature**

  ```python
  class SurplusReverserProtocol(Protocol):
      def __call__(self, latlong: Latlong, level: int = 18) -> dict[str, Any]:
          ...
  ```

  functions that conform to this protocol should have the following signature:

  ```python
  def example(latlong: Latlong, level: int = 18) -> dict[str, Any]: ...
  ```

- **information on conforming functions**

  function takes in a [Latlong](#class-latlong) object and return a dictionary with [`SHAREABLE_TEXT_LINE_*_KEYS`](#constants) keys at the dictionaries' top-level.  
  keys are used to access address information.

  function should also take in an int representing the level of detail for the returned
  address, 0-18 (country-level to building), inclusive. should default to 18.

  keys for latitude, longitude and an iso3166-2 (or closest equivalent) should also be
  included at the dictionaries top level as the keys `latitude`, `longitude` and
  `ISO3166-2` (non-case sensitive, or at least something starting with `ISO3166`)
  respectively.

  ```python
  {
      'ISO3166-2-lvl6': 'SG-03',
      'amenity': 'Ngee Ann Polytechnic',
      ...
      'country': 'Singapore',
      'latitude': 1.33318835,
      'longitude': 103.77461234638255,
      'postcode': '599489',
      'raw': {...},
  }
  ```

  function can and should be at minimum
  [`functools.lru_cache()`-wrapped](https://docs.python.org/3/library/functools.html#functools.lru_cache)
  if the geocoding service asks for caching

  see the [playground notebook](/playground.ipynb) in repository root for detailed
  sample output  
  exceptions are handled by the caller

### `class Behaviour`

[`typing.NamedTuple`](https://docs.python.org/3/library/typing.html#typing.NamedTuple)
representing how surplus operations should behave

attributes

- `query: str | list[str] = ""`  
  original user-passed query string or a list of strings from splitting user-passed query
  string by spaces

- `geocoder: SurplusGeocoderProtocol = default_geocoding.geocoder`  
  name string to location function, see
  [`SurplusGeocoderProtocol`](#surplusgeocoderprotocol) for more information

- `reverser: SurplusReverserProtocol = default_geocoding.reverser`  
  Latlong object to address information dictionary function, see
  [`SurplusReverserProtocol`](#surplusreverserprotocol) for more information

- `stderr: typing.TextIO = sys.stderr`  
  [TextIO-like object](https://docs.python.org/3/library/io.html#text-i-o)
  representing a writeable file.
  defaults to [`sys.stderr`](https://docs.python.org/3/library/sys.html#sys.stderr).

- `stdout: typing.TextIO = sys.stdout`  
  [TextIO-like object](https://docs.python.org/3/library/io.html#text-i-o)
  representing a writeable file.
  defaults to [`sys.stdout`](https://docs.python.org/3/library/sys.html#sys.stdout).

- `debug: bool = False`  
  whether to print debug information to stderr

- `version_header: bool = False`  
  whether to print version information and exit

- `convert_to_type: ConversionResultTypeEnum = ConversionResultTypeEnum.SHAREABLE_TEXT`  
  what type to convert the query to

- `using_termux_location: bool = False`  
  treats query as a termux-location output json string, and parses it accordingly

### `class SurplusDefaultGeocoding`

> [!IMPORTANT]  
> this has replaced the now deprecated default geocoding functions, `default_geocoder()`
> and `default_reverser()`, in surplus 2.1 and later.

see [SurplusGeocoderProtocol](#surplusgeocoderprotocol) and
[SurplusReverserProtocol](#surplusreverserprotocol) for more information how to
implement a compliant custom geocoder functions.

[`dataclasses.dataclass`](https://docs.python.org/3/library/dataclasses.html) providing
the default geocoding functionality for surplus, via
[OpenStreetMap Nominatim](https://nominatim.openstreetmap.org/)

attributes

- `user_agent: str = default_fingerprint`  
  pass in a custom user agent here, else it will be the default
  [fingerprinted user agent](#details-on-the-fingerprinted-user-agent)

example usage

```python
from surplus import surplus, Behaviour, SurplusDefaultGeocoding

geocoding = SurplusDefaultGeocoding("custom user agent")
geocoding.update_geocoding_functions()  # not necessary but recommended

behaviour = Behaviour(
    ...,
    geocoder=geocoding.geocoder,
    reverser=geocoding.reverser
)

result = surplus("query", behaviour=behaviour)

...
```

methods

- [`def update_geocoding_functions(self) -> None: ...`](#surplusdefaultgeocodingupdate_geocoding_functions)
- [`def geocoder(self, place: str) -> Latlong: ...`](#surplusdefaultgeocodinggeocoder)
- [`def reverser(self, latlong: Latlong, level: int = 18) -> dict[str, Any]: ...`](#surplusdefaultgeocodingreverser)

#### `SurplusDefaultGeocoding.update_geocoding_functions()`

re-initialise the geocoding functions with the current user agent, also generate a new
user agent if not set properly

it is recommended to call this before using surplus as by default the geocoding functions
are uninitialised

- signature

  ```python
  def update_geocoding_functions(self) -> None: ...
  ```

#### `SurplusDefaultGeocoding.geocoder()`

> [!WARNING]  
> this function is primarily given to be passed into a [`Behaviour`](#class-behaviour)
> object, and is not meant to be called directly.

default geocoder for surplus

see [SurplusGeocoderProtocol](#surplusgeocoderprotocol) for more information on surplus
geocoder functions

#### `SurplusDefaultGeocoding.reverser()`

> [!WARNING]  
> this function is primarily given to be passed into a [`Behaviour`](#class-behaviour)
> object, and is not meant to be called directly.

default reverser for surplus

see [SurplusReverserProtocol](#surplusreverserprotocol) for more information on surplus
reverser functions

### `class ConversionResultTypeEnum`

[enum.Enum](https://docs.python.org/3/library/enum.html)
representing what the result type of conversion should be

values

- `PLUS_CODE: str = "pluscode"`
- `LOCAL_CODE: str = "localcode"`
- `LATLONG: str = "latlong"`
- `SHAREABLE_TEXT: str = "sharetext"`

### `class Result`

[`typing.NamedTuple`](https://docs.python.org/3/library/typing.html#typing.NamedTuple)
representing the result for safe value retrieval

attributes

- `value: ResultType`  
  value to return or fallback value if erroneous

- `error: BaseException | None = None`  
  exception if any

example usage

```python
# do something
def some_operation(path) -> Result[str]:
    try:
        file = open(path)
        contents = file.read()

    except Exception as exc:
        # must pass a default value
        return Result[str]("", error=exc)

    else:
        return Result[str](contents)

# call function and handle result
result = some_operation("some_file.txt")

if not result:  # check if the result is erroneous
    # .cry() raises the exception
    # (or returns it as a string error message using string=True)
    result.cry()
    ...

else:
    # .get() raises exception or returns value,
    # but since we checked for errors this is safe
    print(result.get())
```

methods

- [`def __bool__(self) -> bool: ...`](#result__bool__)
- [`def cry(self, string: bool = False) -> str: ...`](#resultcry)
- [`def get(self) -> ResultType: ...`](#resultget)

#### `Result.__bool__()`

method that returns `True` if `self.error` is not `None`

- signature

  ```python
  def __bool__(self) -> bool: ...
  ```

- returns `bool`

#### `Result.cry()`

method that raises `self.error` if is an instance of `BaseException`, returns
`self.error` if is an instance of str, or returns an empty string if `self.error` is None

- signature

  ```python
  def cry(self, string: bool = False) -> str: ...
  ```

- arguments

  - `string: bool = False`  
    if `self.error` is an Exception, returns it as a string error message

- returns `str`

#### `Result.get()`

method that returns `self.value` if Result is non-erroneous else raises error

- signature

  ```python
  def get(self) -> ResultType: ...
  ```

- returns `self.value`

### `class Latlong`

[`typing.NamedTuple`](https://docs.python.org/3/library/typing.html#typing.NamedTuple)
representing a latitude-longitude coordinate pair

attributes

- `latitude: float`
- `longitude: float`
- `bounding_box: tuple[float, float, float, float] | None = None`  
  a four-tuple representing a bounding box, `(lat1, lat2, lon1, lon2)` or None.

  the user does not need to enter this. the attribute is only used when shortening plus
  codes, and would be supplied by the geocoding service during shortening.

methods

- [`def __str__(self) -> str: ...`](#latlong__str__)

#### `Latlong.__str__()`

method that returns a comma-and-space-separated string of `self.latitude` and
`self.longitude`

- signature

  ```python
  def __str__(self) -> str: ...
  ```

- returns `str`

### `class PlusCodeQuery`

[`typing.NamedTuple`](https://docs.python.org/3/library/typing.html#typing.NamedTuple)
representing a full-length Plus Code (e.g., 6PH58QMF+FX)

attributes

- `code: str`

methods

- [`def to_lat_long_coord(self, ...) -> Result[Latlong]: ...`](#pluscodequeryto_lat_long_coord)
- [`def __str__(self) -> str: ...`](#pluscodequery__str__)

#### `PlusCodeQuery.to_lat_long_coord()`

- signature

  ```python
  def to_lat_long_coord(self, geocoder: SurplusGeocoderProtocol) -> Result[Latlong]:
      ...
  ```

- arguments

  - `geocoder: SurplusGeocoderProtocol`  
    name string to location function, see
    [SurplusGeocoderProtocol](#surplusgeocoderprotocol) for more information

- returns [`Result`](#class-result)[`[Latlong]`](#class-latlong)

#### `PlusCodeQuery.__str__()`

method that returns string representation of query

- signature

  ```python
  def __str__(self) -> str: ...
  ```

- returns `str`

### `class LocalCodeQuery`

[`typing.NamedTuple`](https://docs.python.org/3/library/typing.html#typing.NamedTuple)
representing a
[shortened Plus Code](https://en.wikipedia.org/wiki/Open_Location_Code#Common_usage_and_shortening)
with locality, referred to by surplus as a "local code"

attributes

- `code: str`  
  Plus Code portion of local code, e.g., "8QMF+FX"

- `locality: str`  
  remaining string of local code, e.g., "Singapore"

methods

- [`def to_full_plus_code(self, ...) -> Result[str]: ...`](#localcodequeryto_full_plus_code)
- [`def to_lat_long_coord(self, ...) -> Result[Latlong]: ...`](#localcodequeryto_lat_long_coord)
- [`def __str__(self) -> str: ...`](#localcodequery__str__)

#### `LocalCodeQuery.to_full_plus_code()`

exclusive method that returns a full-length Plus Code as a string

- signature

  ```python
  def to_full_plus_code(self, geocoder: SurplusGeocoderProtocol) -> Result[str]:
      ...
  ```

- arguments

  - `geocoder: SurplusGeocoderProtocol`  
    name string to location function, see
    [SurplusGeocoderProtocol](#surplusgeocoderprotocol) for more information

- returns [`Result`](#class-result)`[str]`

#### `LocalCodeQuery.to_lat_long_coord()`

method that returns a latitude-longitude coordinate pair

- signature

  ```python
  def to_lat_long_coord(self, geocoder: SurplusGeocoderProtocol) -> Result[Latlong]:
      ...
  ```

- arguments

  - `geocoder: SurplusGeocoderProtocol`  
    name string to location function, see
    [SurplusGeocoderProtocol](#surplusgeocoderprotocol) for more information

- returns [`Result`](#class-result)[`[Latlong]`](#class-latlong)

#### `LocalCodeQuery.__str__()`

method that returns string representation of query

- signature

  ```python
  def __str__(self) -> str: ...
  ```

- returns `str`

### `class LatlongQuery`

[`typing.NamedTuple`](https://docs.python.org/3/library/typing.html#typing.NamedTuple)
representing a latitude-longitude coordinate pair

attributes

- `latlong: Latlong`

methods

- [`def to_lat_long_coord(self, ...) -> Result[Latlong]: ...`](#latlongqueryto_lat_long_coord)
- [`def __str__(self) -> str: ...`](#latlongquery__str__)

#### `LatlongQuery.to_lat_long_coord()`

method that returns a latitude-longitude coordinate pair

- signature

  ```python
  def to_lat_long_coord(self, geocoder: SurplusGeocoderProtocol) -> Result[Latlong]:
      ...
  ```

- arguments

  - `geocoder: SurplusGeocoderProtocol`  
    name string to location function, see
    [SurplusGeocoderProtocol](#surplusgeocoderprotocol) for more information

- returns [`Result`](#class-result)[`[Latlong]`](#class-latlong)

#### `LatlongQuery.__str__()`

method that returns string representation of query

- signature

  ```python
  def __str__(self) -> str: ...
  ```

- returns `str`

### `class StringQuery`

[`typing.NamedTuple`](https://docs.python.org/3/library/typing.html#typing.NamedTuple)
representing a pure string query

attributes

- `query: str`

methods

- [`def to_lat_long_coord(self, ...) -> Result[Latlong]: ...`](#stringqueryto_lat_long_coord)
- [`def __str__(self) -> str: ...`](#stringquery__str__)

#### `StringQuery.to_lat_long_coord()`

method that returns a latitude-longitude coordinate pair

- signature

  ```python
  def to_lat_long_coord(self, geocoder: SurplusGeocoderProtocol) -> Result[Latlong]:
      ...
  ```

- arguments

  - `geocoder: SurplusGeocoderProtocol`  
    name string to location function, see
    [SurplusGeocoderProtocol](#surplusgeocoderprotocol) for more information

- returns [`Result`](#class-result)[`[Latlong]`](#class-latlong)

#### `StringQuery.__str__()`

method that returns string representation of query

- signature

  ```python
  def __str__(self) -> str: ...
  ```

- returns `str`

### `def surplus()`

query to shareable text conversion function

- signature

  ```python
  def surplus(query: Query | str, behaviour: Behaviour) -> Result[str]: ..
  ```

- arguments

  - `query: str | Query`  
    [query object](#query) to convert or string to attempt to query for then convert

  - `behaviour: Behaviour`  
    [surplus behaviour namedtuple](#class-behaviour)

- returns [`Result`](#class-result)`[str]`

### `def parse_query()`

function that parses a query string into a query object

- signature

  ```python
  def parse_query(behaviour: Behaviour) -> Result[Query]: ...
  ```

- arguments

  - `behaviour: Behaviour`  
    [surplus behaviour namedtuple](#class-behaviour)

- returns [`Result`](#class-result)[`[Query]`](#query)

### `def generate_fingerprinted_user_agent()`

function that attempts to return a unique user agent string.

- signature

```python
def generate_fingerprinted_user_agent() -> Result[str]:
```

- returns [`Result[str]`](#class-result)

  this result will always have a valid value as erroneous results will have a
  resulting value of `'surplus/<version> (generic-user)'`

  valid results will have a value of `'surplus/<version> (<fingerprin hasht>)'`, where
  the fingerprint hash is a 12 character hexadecimal string

#### details on the fingerprinted user agent

**why do this in the first place?**  
if too many people use surplus at the same time,
Nominatim will start to think it's just one person being greedy. so to prevent this,
surplus will try to generate a unique user agent string for each user through
fingerprinting.

at the time of writing, the pre-hashed fingerprint string is as follows:

```python
unique_info: str = f"{version}-{system_info}-{hostname}-{mac_address}"
```

it contains the following, in order, alongside an example:

1. `version` - the surplus version alongside a suffix, if any

   ```text
   2.2.0-local
   ```

2. `system_info` - generic machine and operating system information

   ```text
   Linux-6.5.0-locietta-WSL2-xanmod1-x86_64-with-glibc2.35
   ```

3. `hostname` - your computer's hostname

   ```text
   mark
   ```

4. `mac_address` - your computer's mac address

   ```text
   A9:36:3C:98:79:33
   ```

after hashing, this string becomes a 12 character hexadecimal string, as shown below:

```text
surplus/2.2.0-local (1fdbfa0b0cfb)
                     ^^^^^^^^^^^^
                     this is the hashed result of unique_info
```

if at any time the retrieval of any of these four elements fail, surplus will just give
up and default to `'surplus/<version> (generic-user)'`.

if any of this seems weird to you, that's fine. pass in a custom user agent flag to
surplus with `-u` or `--user-agent` to override the default user agent, or override the
default user agent in your own code by passing in a custom user agent string to
[`Behaviour`](#class-behaviour).

```text
$ surplus --user_agent "a-shiny-custom-and-unique-user-agent" 77Q4+7X Austin, Texas, USA
...
```

```python
>>> from surplus import surplus, Behaviour
>>> surplus(..., Behaviour(user_agent="a-shiny-custom-and-unique-user-agent"))
...
```

## licence

surplus is free and unencumbered software released into the public domain. for more
information, please refer to the [UNLICENCE](/UNLICENCE), <https://unlicense.org>, or the
python module docstring.

however, direct dependencies of surplus are licensed under different, but still permissive
and open-source licences.

- [geopy](https://pypi.org/project/geopy/):
  Python Geocoding Toolbox

  MIT Licence

  - [geographiclib](https://pypi.org/project/geographiclib/):
    The geodesic routines from GeographicLib

    MIT Licence

- [pluscodes](https://pypi.org/project/pluscodes/):
  Compute Plus Codes (Open Location Codes)

  Apache 2.0

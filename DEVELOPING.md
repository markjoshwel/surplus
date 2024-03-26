# the developers guide to surplus

- [quickstart](#quickstart)
- [common commands](#common-commands)
- [the technical details of surplus's output](#the-technical-details-of-surpluss-output)

## quickstart

prerequisites:

- [Python >=3.11](https://www.python.org/)
- [Hatch](https://hatch.pypa.io/latest/)

alternatively, use [devbox](https://get.jetpack.io/devbox) for a hermetic development environment powered by [Nix](https://nixos.org/).

```text
devbox shell    # skip this if you aren't using devbox
hatch shell
```

## common commands

- `hatch fmt`  
  formats and statically analyses the codebase

- `hatch run dev:check`  
  runs mypy and isort to check the codebase

- `hatch run dev:fix`  
  runs isort to fix imports

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
  string passed to [`parse_query()`](/README.md#def-parse_query) for parsing

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

  query is a variable of type [`Result[Query]`](/README.md#query)

  this variable is displayed to show what query type [`parse_query()`](/README.md#def-parse_query) has
  recognised, and if there were any errors during query parsing

- **expression `latlong_result.get()=`**

  (_only shown if the query is a Plus Code_)

  the latitude longitude coordinates derived from the Plus Code

- **variable `location`**

  the response dictionary from the reverser function passed to
  [`surplus()`](/README.md#def-surplus)

  for more information on the reverser function, see
  [`SurplusReverserProtocol`](/README.md#surplusreverserprotocol)

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

# surplus

surplus (s+) is a Python script to convert [Google Maps Plus Codes](https://maps.google.com/pluscodes/)
to iOS Shortcuts-like shareable text

- [quickstart](#quickstart)
- [documentation](https://surplus.joshwel.co)
  - [the user's guide (command-line)](https://surplus.joshwel.co/using#as-a-command-line-tool)
  - [the user's guide (library)](https://surplus.joshwel.co/using#as-a-library)
  - [the developer's guide](https://surplus.joshwel.co/developing)
      - [api reference](https://surplus.joshwel.co/developing)
  - [the contributor's guide](https://surplus.joshwel.co/contributing)

this repository is also monorepo for the following sibling projects:

- **surplus on wheels** (s+ow)  
  a pure shell script to get your location using `termux-location`, process it through surplus, and
  send it to messaging service or wherever, using "bridges"
- **surplus on wheels: Whatsapp Bridge**
- **surplus on wheels: Telegram Bridge**

## quickstart

> [!TIP]  
> termux users can consider [surplus on wheels](https://surplus.joshwel.co/onwheels), a sibling
> project that allows you to run surplus regularly throughout the day and send it to someone on a
> messaging platform

> [!IMPORTANT]  
> python 3.11 or later is required due to a bug in earlier versions
> [(python/cpython#88089)](https://github.com/python/cpython/issues/88089)

install surplus with pip, or [pipx](https://pipx.pypa.io/) (recommended):

```text
pipx install surplus
```

then, use the `surplus` command, or its `s+` shorthand:

```text
$ s+ 7RGX+GJ Singapore
surplus version 2024.0.0-beta
Singapore Conference Hall
7 Shenton Way
068809
Central, Singapore
```

the types of queries you can pass in are:

- full-length Plus Codes  
  `6PH58QMF+FX`
- shortened Plus Codes / 'local codes'  
  `8QMF+FX Singapore`
- latitude and longitude coordinate pairs  
  `1.3336875, 103.7749375`
- string queries  
  `Wisma Atria`

or, alternatively pass in `-` to read from stdin

more documentation is available at <https://surplus.joshwel.co>,
or alternatively available locally in the [docs/](docs) folder

## licences

- [**surplus**](src/surplus)  
  The Unlicence

  surplus is free and unencumbered software released into the public domain. for more information,
  please refer to the [UNLICENCE](src/surplus/UNLICENCE), <https://unlicense.org>, or the python
  module docstring

  however, the dependencies surplus relies on are licenced under different, but still permissive
  and open-source licences:

    - [**geopy**](https://pypi.org/project/geopy/) — 
      Python Geocoding Toolbox  
      MIT Licence

        - [**geographiclib**](https://pypi.org/project/geographiclib/) — 
          The geodesic routines from GeographicLib  
          MIT Licence

    - [**pluscodes**](https://pypi.org/project/pluscodes/) — 
      Compute Plus Codes (Open Location Codes)  
      Apache 2.0

- [**surplus on wheels**](src/surplus-on-wheels)  
  The Unlicence

  surplus on wheels is free and unencumbered software released into the public domain. for more
  information, please refer to [UNLICENCE](src/surplus-on-wheels/UNLICENCE) or
  <http://unlicense.org/>

- [**surplus on wheels: WhatsApp Bridge**](src/spow-whatsapp-bridge)  
  Mozilla Public Licence 2.0

  the s+ow WhatsApp Bridge is based off mdtest code from the
  [whatsmeow](https://github.com/tulir/whatsmeow) project, which is licenced under the Mozilla
  Public Licence 2.0. for more information, see [LICENCE](src/spow-whatsapp-bridge/LICENCE), or
  <https://www.mozilla.org/en-US/MPL/2.0/>

  the direct dependencies s+ow-whatsapp-bridge relies on are licenced under different, but still
  permissive and open-source licences:

    - [**whatsmeow**](https://github.com/tulir/whatsmeow) — 
      Go library for the WhatsApp web multidevice API  
      Mozilla Public Licence 2.0

- [**surplus on wheels: Telegram Bridge**](src/spow-telegram-bridge)  
  The Unlicence

  the s+ow Telegram Bridge is free and unencumbered software released into the public domain. for
  more information, please refer to the [UNLICENCE](src/spow-telegram-bridge/UNLICENCE),
  <https://unlicense.org>, or the python module docstring

  however, the direct dependencies surplus relies on are licenced under different, but still
  permissive and open-source licences:

    - [**Telethon**](https://pypi.org/project/Telethon/) — 
      Pure Python 3 MTProto API Telegram client library, for bots too!  
      MIT Licence

- [**surplus documentation**](docs)  
  CC0 1.0 Universal

  the textual contents of surplus documentation by [Mark Joshwel](https://joshwel.co) is marked
  with [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/).
  to view a copy of this license, visit <https://creativecommons.org/publicdomain/zero/1.0/>

  the fonts the documentation website relies on are licenced under different, but still
  permissive and open-source licences:

    - [**Geist and Geist Mono**](https://github.com/vercel/geist-font)  
      SIL Open Font Licence 1.1 ([file](docs/fonts/LICENSE.txt))
    
  the direct software dependencies the documentation are also licenced under different, but still
  permissive and open-source licences:

    - [**mkdocs-material**](https://squidfunk.github.io/mkdocs-material/) — 
      Documentation that simply works  
      MIT Licence

    - [**mkdocs**](https://www.mkdocs.org/) — 
      Project documentation with Markdown  
      BSD-2-Clause Licence

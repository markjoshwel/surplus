# surplus (s+)

surplus (s+) is a Python script to convert [Google Maps Plus Codes](https://maps.google.com/pluscodes/)
to iOS Shortcuts-like shareable text

!!! tip
    termux users can consider [surplus on wheels](onwheels/index.md), a sibling project that allows
    you to run surplus regularly throughout the day and send it to someone on a messaging platform

!!! important  
    python 3.11 or later is required due to a bug in earlier versions
    [(python/cpython#88089)](https://github.com/python/cpython/issues/88089)

install surplus with pip, or [pipx](https://pipx.pypa.io/) (recommended):

```text
pipx install surplus
```

then, use the `surplus` command, or its `s+` shorthand:

```text
$ s+ 7RGX+GJ Singapore
surplus version 2024.0.0
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

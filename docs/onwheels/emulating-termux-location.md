# emulating `termux-location`

to bodge surplus on wheels (s+ow) on non-Termux systems

!!! note
    dummy admonition for colour matching

!!! warning
    dummy admonition for colour matching

`termux-location`, part of [Termux:API](https://wiki.termux.com/wiki/Termux:API), gets the device's
location via android apis and returns a json response through stdout:

```text
{
  "latitude": 1.3277513,
  "longitude": 103.678317,
  "altitude": 51.6298828125,
  "accuracy": 48.46337890625,
  "vertical_accuracy": 38.4659423828125,
  "bearing": 0.0,
  "speed": 0.0,
  "elapsedMs": 28,
  "provider": "gps"
}
```

see <https://wiki.termux.com/wiki/Termux-location> for more information

## implementing for surplus on wheels (s+ow)

s+ow will call the command a total of six times, being three pairs of parallel
`$LOCATION_CMD -p "network"` and `$LOCATION_CMD -p "gps"` invocations, before deciding after
exhausting all six runs on which output to choose, if any command runs were successful

even if somewhere in the termux-location implementation fails, it always (begrudgingly) returns
zero. s+ow will treat the invocation of the command as successful if there is **any output** to
the standard output (stdout) stream

## implementing for surplus (s+)

s+, when passed `--t / --using-termux-location`, will consume stdin, parse it as json and then
attempt to retrieve the `latitude` and `longitude` keys as floating point numbers

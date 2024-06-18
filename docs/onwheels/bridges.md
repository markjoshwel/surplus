# surplus on wheel bridges

## official bridges

there are two currently “official” bridges:

- [surplus on wheels: WhatsApp Bridge](whatsapp-bridge.md)
- [surplus on wheels: Telegram Bridge](telegram-bridge.md)

## bring your own bridge

### an informal specification

s+ow bridges are relatively simple as they are:

1. an executable or script

2. that reads in `SPOW_TARGETS` given by surplus to the bridge, using the standard input (stdin)
   stream

    1. bridges do not need to account for the possibility of multiple lines sent to stdin

    2. bridges should account for the possibility of comma and space (`", "` instead of just `","`)
        delimited targets, and strip each target of preceding and trailing whitespace

    3. bridges should recognise a platform based on a prefix  
        (e.g. `wa:` for WhatsApp, `tg:` for Telegram, etc.)

3. reads `SPOW_MESSAGE` (`~/.cache/spow/message`) for the message content

notes:

1. stderr and stdout are redirected to s+ow’s error and output logs respectively unless the
   `-p / --private` flag is passed to surplus

2. any errors encountered by the bridge should always result in a non-zero return. error logs will
   show the exact error code, so feel free to use other numbers than 1

3. persistent data such as credentials and session data storage are to be handled by the
   bridge itself. consider storing them in `$HOME/.local/share/<bridge-name>/`, or wherever
   appropriate

### example

if i were to recommend an example on a basic bridge implementation, it would be the
[Telegram Bridge](telegram-bridge.md):

```python title="src/spow-telegram-bridge/bridge.py"
--8<-- "src/spow-telegram-bridge/bridge.py"
```

!!! note
    the feature of deleting the last sent message (`--delete-last`) is a non-standard feature for
    bridges, and was simply a use case i personally needed. if you're going to implement a bridge,
    all you really need is the ability to `login`, `logout`, and [send a message](#an-informal-specification)

    you can add other features as per the needs of your platform, like how the WhatsApp Bridge has
    a `pair-phone` subcommand, or per your use case needs, like in the Telegram Bridge's `--delete-last`.

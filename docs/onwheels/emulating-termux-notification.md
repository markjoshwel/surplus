# emulating `termux-notification`

to bodge surplus on wheels (s+ow) on non-Termux systems

`termux-notification`, part of [Termux:API](https://wiki.termux.com/wiki/Termux:API), sends out an
android notification

without `termux-notification`, s+ow will still run as it doesn't use `set -e` and very carefully
handles all command invocations, with `termux-notification` being the graceful exception\

however, if you would like to emulate it, make an executable globally reachable with the same name

s+ow uses the command as such:

```shell
termux-notification \
    --priority "default" \
    --title "surplus on wheels: No bridges" \
    --content "No '$SPOW_BRIDGES' file; message is not sent."
```

```shell
termux-notification \
    --priority "min" \
    --ongoing \
    --id "s+ow" \
    --title "surplus on wheels" \
    --content "s+ow has started running."
```

```shell
termux-notification \
    --priority "min" \
    --id "s+ow" \
    --title "surplus on wheels" \
    --content ...
```

```shell
termux-notification \
    --priority "default" \
    --title "surplus on wheels has errored" \
    --content ...
```

see <https://wiki.termux.com/wiki/Termux-notification> for more information

# surplus on wheels: Telegram Bridge

Telegram Bridge for surplus on wheels (s+ow)

s+ow bridges are defined in a file named `$HOME/.s+ow-bridges`. each command in the file is run,
and comma-seperated target chat IDs are passed using stdin.

this bridge recognises targets prefixed with `tg:`.

```text
tg:<chat id>,...
```

## installation

!!! important
    the following instructions implies that [surplus](../index.md) and [surplus on wheels](bridges.md)
    have already been installed

1. install prerequisite software if not installed:

    ```text
    pkg install git
    ```

    ```text
    pip install pipx
    ```

2. install spow-telegram-bridge:

    ```text
    wget -O- https://surplus.joshwel.co/telegram.sh | sh
    ```

    !!! note
        if `wget` throws a 404, see [backup links](../links.md)

3. add the following to your `$HOME/.s+ow-bridges` file:

    ```text
    SPOW_TELEGRAM_API_HASH="" SPOW_TELEGRAM_API_ID="" s+ow-telegram-bridge
    ```
    
    fill in SPOW_TELEGRAM_API_HASH and SPOW_TELEGRAM_API_ID accordingly.
    see the [Telethon docs](https://docs.telethon.dev/en/stable/basic/signing-in.html) for
    more information

to keep up to date, look at [updating](#updating) to set up a daily update cron job:

## updating

the installation script also sets up a shell script under the `s+ow-telegram-bridge-update` command

```text
s+ow-telegram-bridge-update
```

to do this automatically, make a cron job with `crontab -e`
and make a new line with the following text:

```text
0 0 * * *      bash -l -c "s+ow-telegram-bridge-update"
```

this cron job will run the command every day at midnight

## usage

- `s+ow-telegram-bridge`
    normal usage; sends latest message to tg:-prefixed targets given in stdin

- `s+ow-telegram-bridge login`
    logs in to Telegram

- `s+ow-telegram-bridge logout`
    logs out of Telegram

- `s+ow-telegram-bridge list`
    lists all chats and their IDs

optional arguments:

- `--silent`
    asks telegram to send message silently
- `--delete-last`
    deletes last location message to prevent clutter

## versioning scheme

from `v2.2024.27`, the Telegram Bridge will automatically release a new version once a week if there
are updates to its dependencies

as such, the bridge is now versioned with a modified calendar versioning scheme of
`MAJOR.YEAR.ISOWEEK`, where the `MAJOR` version segment will be bumped with codebase changes, whereas
the `YEAR` and `ISOWEEK` segments will represent the time of which the release was built at

## licence

the s+ow Telegram Bridge is free and unencumbered software released into the public domain.
for more information, see [licences](../licences.md).

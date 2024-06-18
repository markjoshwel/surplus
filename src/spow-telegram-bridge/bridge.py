#!/usr/bin/env python3
"""
s+ow-telegram-bridge: add-on bridge for surplus on wheels (s+ow) to telegram
----------------------------------------------------------------------------
by mark <mark@joshwel.co>

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

import asyncio
from datetime import datetime
from os import environ, chdir
from pathlib import Path
from sys import argv, stderr, stdin
from traceback import print_tb
from typing import Generic, NamedTuple, TypeVar

from telethon import TelegramClient  # type: ignore
from telethon.tl import functions  # type: ignore

# exit codes:
# 1 - bad command usage or missing env vars
# 2 - bad target
# 3 - could not send message

# rundown:
# 1. if argv[-1] is 'login', then run login() and exit
# 2. read stdin and comma split it
# 3. read ~/.cache/s+ow/message
# 4. for each target in comma split stdin that starts with "tg:",
#    send ~/.cache/s+ow/message


dir_data: Path = Path.home().joinpath(".local/share/s+ow-telegram-bridge")
dir_data.mkdir(parents=True, exist_ok=True)
chdir(dir_data)
dir_cache: Path = Path.home().joinpath(".cache/s+ow-telegram-bridge")
dir_cache.mkdir(parents=True, exist_ok=True)


session = "s+ow-telegram-bridge"
api_id = environ.get("SPOW_TELEGRAM_API_ID", None)
api_hash = environ.get("SPOW_TELEGRAM_API_HASH", None)
message = Path.home().joinpath(".cache/s+ow/message")


def handle_error(
    exc: Exception | None = None,
    message: str = "error",
    recoverable: bool = False,
    exit_code: int = -1,
) -> None:
    try:
        exc_details: str = ""
        if isinstance(exc, Exception):
            exc_details = f": {exc} ({exc.__class__.__name__})"
            print_tb(exc.__traceback__, file=stderr)

        print(
            f"s+ow-telegram-bridge: {message}{exc_details}",
            file=stderr,
        )

    except Exception as exc:
        pass

    if not recoverable:
        exit(exit_code)


def validate_vars() -> None:
    if api_id is None:
        print("s+ow-telegram-bridge: error: SPOW_TELEGRAM_API_ID not set", file=stderr)
        exit(1)

    if api_hash is None:
        print("s+ow-telegram-bridge: error: SPOW_TELEGRAM_API_HASH not set", file=stderr)
        exit(1)

    if not (message.exists() and message.is_file()):
        print("s+ow-telegram-bridge: error: ~/.cache/s+ow/message not found", file=stderr)
        exit(1)


async def run() -> None:
    validate_vars()
    silent: bool = "--silent" in argv
    delete_last: bool = "--delete-last" in argv

    if silent:
        print("s+ow-telegram-bridge: info: --silent passed", file=stderr)

    if delete_last:
        print("s+ow-telegram-bridge: info: --delete-last passed", file=stderr)

    targets: list[int] = []
    for line in stdin:
        for _target in line.split(","):
            if (_target := _target.strip()).startswith("tg:"):
                _target = _target[3:]
                if not (
                    _target.isnumeric()
                    or (_target.startswith("-") and _target.lstrip("-").isnumeric())
                ):
                    continue

                try:
                    targets.append(int(_target))

                except Exception as exc:
                    handle_error(
                        exc=exc,
                        message=f"error: could not cast '{_target}' as int",
                        recoverable=True,
                        exit_code=2,
                    )
                    continue

    async with TelegramClient(session, api_id, api_hash) as client:
        for target in targets:
            try:
                if delete_last is False:
                    await client.send_message(
                        int(target),
                        message.read_text(encoding="utf-8"),
                        silent=silent,
                    )

                else:
                    target_persist: Path = dir_cache.joinpath(str(target))

                    try:
                        # delete old message if persist file exists
                        if target_persist.exists() and target_persist.is_file():
                            await client.delete_messages(
                                entity=target,
                                message_ids=[int(target_persist.read_text(encoding="utf-8"))],
                            )

                    except Exception as exc:
                        handle_error(
                            exc=exc,
                            message=f"error: could not delete old message",
                            recoverable=True,
                            exit_code=3,
                        )
                        continue

                    # send new message
                    target_sent_message = await client.send_message(
                        target,
                        message.read_text(),
                        silent=silent,
                    )

                    # persist new message id
                    target_persist.write_text(str(target_sent_message.id), encoding="utf-8")

            except Exception as exc:
                handle_error(
                    exc=exc,
                    message=f"error: could not send message",
                    recoverable=True,
                    exit_code=3,
                )
                continue

            print("s+ow-telegram-bridge: success: message sent to", target)
    exit()


def login() -> None:
    validate_vars()
    with TelegramClient(session, api_id, api_hash) as client:
        client.start()
    exit()


def list_chats() -> None:
    validate_vars()
    with TelegramClient(session, api_id, api_hash) as client:
        for dialog in client.iter_dialogs():
            print(dialog.id, "\t", dialog.name)
    exit()


def entry() -> None:
    if len(argv) < 1:
        print("s+ow-telegram-bridge: error: len(argv) < 1", file=stderr)
        exit(1)

    if "login" in argv:
        login()

    elif "list" in argv:
        list_chats()

    else:
        asyncio.run(run())


if __name__ == "__main__":
    entry()

# the contributor's handbook

expected details on development workflows? see [the developer's handbook](developing.md)

## which forge do i use?

as at the time of writing this documentation, i am actively using both
<https://github.com/markjoshwel/surplus> and <https://forge.joshwel.co/mark/surplus>

use whatever is more comfortable to you. do you not like microsoft and/or have moved away from github?
feel free to use <https://forge.joshwel.co>. don't want to make an account for either? did the forge
implode and is down? okay! mail in a git patch at <mark@joshwel.co>

## git workflow

1. fork the repository and branch off from the `future` branch,  
   or `main` if not available
2. make and commit your changes!
3. pull in any changes from upstream, and resolve any conflicts, if any
4. if needed, **commit your copyright waiver** (_see [waiving copyright](#waiving-copyright)_)
5. submit a pull request (_or mail in a patch_)

### waiving copyright

!!! danger "Warning"
    this section is a **must** to follow if you have modified **any** unlicenced code:

    - top-level surplus files (`releaser.py`, etc)
    - surplus (`src/surplus`)
    - surplus Documentation (`docs/`)
    - surplus on wheels (`src/surplus-on-wheels`)
    - surplus on wheels: Telegram Bridge (`src/spow-telegram-bridge`)

!!! info
    the command to create an empty commit is `git commit --allow-empty`

when contributing your first changes, please include an empty commit for a copyright
waiver using the following message (replace `Your Name` with your name or username):

```text
Your Name Copyright Waiver

I dedicate any and all copyright interest in this software to the
public domain. I make this dedication for the benefit of the public at
large and to the detriment of my heirs and successors. I intend this
dedication to be an overt act of relinquishment in perpetuity of all
present and future rights to this software under copyright law.

To the best of my knowledge and belief, my contributions are either
originally authored by me or are derived from prior works which I have
verified are also in the public domain and are not subject to claims
of copyright by other parties.

To the best of my knowledge and belief, no individual, business,
organization, government, or other entity has any copyright interest
in my contributions, and I affirm that I will not make contributions
that are otherwise encumbered.
```

(from <https://unlicense.org/WAIVER>)

for documentation contributors, if you have contributed a
[legally significant](https://www.gnu.org/prep/maintain/maintain.html#Legally-Significant) or have
repeatedly commited multiple small changes, waive your copyright with the CC0 deed
(replace `Your Name` with your name or username):

```text
Your Name Copyright Waiver

The person who associated a work with this deed has dedicated the work to
the public domain by waiving all of his or her rights to the work worldwide
under copyright law, including all related and neighboring rights, to the
extent allowed by law. 
```

(from <https://creativecommons.org/publicdomain/zero/1.0/>)

## reporting incorrect output

TODO

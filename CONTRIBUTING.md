# the contributors guide to surplus

- [git workflow](#git-workflow)
- [reporting incorrect output](#reporting-incorrect-output)
  - [the reporting process](#the-reporting-process)
    - [what counts as "incorrect"](#what-counts-as-incorrect)

also see the [DEVELOPING.md](/DEVELOPING.md) file for more information on the codebase.

## git workflow

1. fork the repository and branch off from the `future` branch,  
   or `main` if `future` is not available
2. make and commit your changes!
3. pull in any changes from upstream, and resolve any conflicts, if any
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

## reporting incorrect output

> [!NOTE]  
> this section is independent of the rest of the contributing section.

different output from the iOS Shortcuts app is expected, however incorrect output is not.

### the reporting process

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
   [`--debug` flag](/README.md#command-line-usage) passed to the surplus CLI or with
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

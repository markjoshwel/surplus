#!/bin/sh

SURPLUS_CMD_DEFAULT="surplus    --debugp -tp"
SURPLUS_CMD=${SURPLUS_CMD:-$SURPLUS_CMD_DEFAULT}

# parse SURPLUS_CMD to see if "-p" or "--private" is in the args
set -f
# shellcheck disable=SC2086
set -- $SURPLUS_CMD
for arg; do
    case "$arg" in
        --private)
            echo YAY
            break
            ;;
        --*)
            ;;
        -*)
            if echo "$arg" | grep -q "p"; then
                echo YAY
                break
            fi
            ;;
    esac
done
set +f

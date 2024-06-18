#!/bin/sh
failures=0

FMT_HASH=$(shfmt s+ow | md5sum)
ORI_HASH=$(md5sum < s+ow)
if ! [ "$FMT_HASH" = "$ORI_HASH" ]; then
	printf "formatted file (%s) is not the same as the original file (%s)" "$FMT_HASH" "$ORI_HASH"
	failures=$((failures + 1))
else
	printf "formatted file is same as original file - %s (yay!)" "$FMT_HASH"
fi

shellcheck s+ow
failures=$((failures + $?))

if [ $failures -eq 0 ]; then
	printf "\n\nall checks okay! (❁´◡\`❁)\n"
else
	printf "\n\nsome checks failed...\n"
fi
exit $failures

#!/bin/sh
failures=0

ORI_HASH=$(md5sum < bridge.go)
FMT_HASH=$(gofmt bridge.go | md5sum)
if ! [ "$FMT_HASH" = "$ORI_HASH" ]; then
	printf "formatted file (%s) is not the same as the original file (%s)" "$FMT_HASH" "$ORI_HASH"
	failures=$((failures + 1))
else
	printf "formatted file is same as original file - %s (yay!)" "$FMT_HASH"
fi

go vet bridge.go
failures=$((failures + $?))

golint bridge.go
failures=$((failures + $?))

if [ $failures -eq 0 ]; then
	printf "\n\nall checks okay! (❁´◡\`❁)\n"
else
	printf "\n\nsome checks failed...\n"
fi
exit $failures

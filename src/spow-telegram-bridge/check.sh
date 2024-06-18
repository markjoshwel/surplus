#!/bin/sh
failures=0

mypy bridge.py
failures=$((failures + $?))

ruff check bridge.py
failures=$((failures + $?))

ruff format bridge.py
failures=$((failures + $?))

isort --check bridge.py
failures=$((failures + $?))

if [ $failures -eq 0 ]; then
	printf "\n\nall checks okay! (❁´◡\`❁)\n"
else
	printf "\n\nsome checks failed...\n"
fi
exit $failures

#!/bin/bash
# Diagnostic what-if (worker only): compile <file.c> with the private traced compiler and the
# given TX* override environment, then print the align.py summary of the resulting assembly.
# usage: what.sh <file.c> <tag> [VAR=value ...]     Never a match claim.
SRC=$1; TAG=$2; shift 2
env "$@" TXDBG= docs/finish4-1115/sound/tr.sh $SRC $TAG > /dev/null 2>&1
python3 docs/finish4-1115/sound/align.py build/tr/$TAG/t.s ${MAXH:-0} | sed "s|build/tr/$TAG/t.s|$TAG $*|"

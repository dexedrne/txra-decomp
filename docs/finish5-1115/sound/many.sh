#!/bin/bash
# usage: many.sh <file.c>...  (worker) align.py summary lines for each file, JOBS parallel
J=${JOBS:-6}
printf '%s\n' "$@" | xargs -P $J -I{} sh -c 'python3 docs/finish5-1115/sound/align.py {} 0 2>&1 | head -2 | paste -sd " "' | sort

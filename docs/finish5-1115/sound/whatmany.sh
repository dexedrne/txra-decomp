#!/bin/bash
# Diagnostic (worker only): what.sh for many files with the same override env, parallel.
# usage: whatmany.sh "VAR=value ..." <file.c>...     prints: DIFF tag emit frame regions
E=$1; shift
printf '%s\n' "$@" | xargs -P ${JOBS:-6} -I{} sh -c "f={}; t=wm_\$(basename \$f .c); docs/finish5-1115/sound/what.sh \$f \$t $E | paste -sd ' '" | python3 -c '
import sys, re
rows = []
for l in sys.stdin:
    m = re.search(r"^(\S+).* emit (\d+) frame (\S+) dist \d+ DIFF (\d+).*region: (.*)", l)
    if m: rows.append((int(m.group(4)), m.group(1), m.group(2), m.group(3), m.group(5).strip()))
for r in sorted(rows): print(*r)
'

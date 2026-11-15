#!/bin/bash
# Diagnostic (worker only): ga.sh for many files in parallel.  usage: gamany.sh "<pseudos>" <file.c>...
P=$1; shift
printf '%s\n' "$@" | xargs -P ${JOBS:-10} -I{} sh -c "docs/finish5-1115/sound/ga.sh {} $P | paste -sd ' '" | sed -E 's/ GA ord=[0-9]+ reg=/ | r/g; s/ refs=/:/g; s/ len=/\//g; s/ pri=/ p=/g' | sort -t' ' -k3 -n

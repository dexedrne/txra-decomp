#!/bin/bash
# Diagnostic (worker only): for each pseudo conflicting with WATCH (from a traced compile of
# <file.c>), apply the what-if TXPREF=<pseudo>:<reg> and print the align summary.  Never a claim.
# usage: zscan.sh <file.c> <watch-pseudo> <reg[+reg..]> [JOBS]
SRC=$1; W=$2; R=$3; J=${4:-6}
TXWATCH=$W TXDBG= docs/finish5-1115/sound/tr.sh $SRC zs_base > /dev/null 2>&1
grep -A400 "^GW reg=$W " build/tr/zs_base/trace.txt | sed -n '2,400p' | grep -m1 -n "^G[FW]" > /dev/null
awk -v w="$W" '$1=="GW" && $2=="reg="w {p=1; next} p && /^  GWc/ {sub("reg=","",$2); print $2; next} p {exit}' build/tr/zs_base/trace.txt > build/tr/zs_list.txt
wc -l < build/tr/zs_list.txt
cat build/tr/zs_list.txt | xargs -P $J -I{} sh -c "docs/finish5-1115/sound/what.sh $SRC zs_{} TXPREF=$(echo $R | sed 's/+/,{}:/g; s/^/{}:/') | paste -sd ' ' | sed -E 's/.*(TXPREF=[^ ]*) emit ([0-9]+) .*DIFF ([0-9]+).*region: (.*)/\\3 \\1 emit \\2 \\4/'" | sort -n | head -${TOP:-25}

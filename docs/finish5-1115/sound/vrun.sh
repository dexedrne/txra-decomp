#!/bin/bash
# Diagnostic (worker only): generate the variants of <spec> from <base.c> and print the
# align.py summary of each (official compiler, measure path), best first.
# usage: vrun.sh <base.c> <spec> [JOBS]
B=$1; S=$2; J=${3:-10}
D=build/v/$(basename $S .spec)
rm -rf $D; mkdir -p $D
python3 docs/finish5-1115/sound/vgen.py $B $S $D > $D/list.txt || exit 1
cat $D/list.txt | xargs -P $J -I{} sh -c 'python3 docs/finish5-1115/sound/align.py {} 0 2>&1 | head -2 | paste -sd " "' \
 | sed -E 's|^build/v/[^/]+/||; s/exact\/reg-only rows per region: //' | awk '{for(i=1;i<=NF;i++) if($i=="DIFF") print $(i+1), $0}' | sort -n | cut -d' ' -f2-

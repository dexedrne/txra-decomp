#!/bin/bash
# print the tempo-block register signature (the 5 insns after the second literal load) for each mini file
for f in "$@"; do
  s=$(docs/finish5-1115/sound/mini/mc.sh $f | awk '/cmp\tr0, #0/{p=1;next} p && /ldr|add/{printf "%s; ", $0; n++} n>=6{exit}' | tr -s '\t ' ' ')
  echo "$(basename $f): $s"
done

#!/bin/bash
# loopinfo.sh SRC.c... : first-pass part-loop movable decisions (diagnostic, worker only)
D=docs/near-misses/finish2-1115-renderer
for s in "$@"; do
  o=build/li-$$; rm -rf $o
  bash $D/dump.sh "$s" $o -dL >/dev/null 2>&1
  awk '/^Loop from/ && !/phony/ {n++} n==2' $o/t.i.loop | grep -E "^Loop from|^Insn" | grep -v "done matches" | head -18 | \
    sed -E 's/Insn ([0-9]+): regno [0-9]+ \(life ([0-9]+)\),.*savings ([0-9]+).*(moved|not desirable|not safe).*/\1:l\2s\3:\4/; s/Insn ([0-9]+): .*(not safe|not desirable).*/\1:\2/' | tr '\n' ' ' | sed "s|^|$(basename $s): |"; echo
  rm -rf $o
done

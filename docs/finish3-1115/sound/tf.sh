#!/bin/bash
# usage: tf.sh <force-spec> <file.c>...  (worker; diagnostic forced spill, prints frame + 0x67 block)
F=$1; shift
for f in "$@"; do
  t=$(basename $f .c)
  TXFORCE=$F TXDBG=S docs/finish3-1115/sound/tr.sh $f tf_$t > /dev/null 2>&1
  s=build/tr/tf_$t/t.s
  echo "== $t $(grep -o 'add\s*sp, sp, #-[0-9]*' $s | head -1) $(grep -c FORCED build/tr/tf_$t/trace.txt)"
  awk '/cmp\tr[0-7], #103/{p=1} p{print; n++} n>=20{exit}' $s | tr '\t' ' ' | paste -sd ';' | cut -c1-500
done

#!/bin/bash
# Receipts (worker only): official measure_candidate for each step of receipts.spec, from the finish4 source.
B=docs/near-misses/finish4-1115-sound/func_080064A4.c
D=build/rcpt; rm -rf $D; mkdir -p $D
python3 docs/finish5-1115/sound/vgen.py $B docs/finish5-1115/sound/specs/receipts.spec $D > $D/list.txt
for f in $B $(cat $D/list.txt) src/generated/func_080064A4.c; do
  python3 tools/measure_candidate.py $f 080064A4 08007398 old $D/m_$(basename $f .c) | python3 -c "
import json,sys; d=json.load(sys.stdin)
print(json.dumps({k: d[k] for k in ('source','source_sha256','emitted_bytes','local_frame_bytes','instruction_distance','different_bytes','exact','compiled_sha256')}))"
done

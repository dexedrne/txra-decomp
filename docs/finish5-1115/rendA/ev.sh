#!/bin/bash
# ev.sh CAND.c [--log] [--lq] : score, projection-loop side-by-side, trace + block view (worker only)
C=$1; shift
python3 docs/finish3-1115/renderer/sbs2.py $C --score
python3 docs/finish3-1115/renderer/sbs2.py $C 08017338 08017420
O=~/rendA-out/$(basename $C .c)
bash docs/finish5-1115/rendA/trace.sh $C $O >/dev/null 2>$O.err || true; tail -1 $O.err
python3 docs/finish5-1115/rendA/blk.py $O "$@" | sed -n '/sched1 order/,$p'

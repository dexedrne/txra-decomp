#!/bin/bash
# tryorders.sh CAND.c NONLOCAL ORDER... : what-if score for each order (worker only, diagnostic)
C=$1; NL=$2; shift 2
for O in "$@"; do
  r=$(TXNONLOCAL=$NL TXORDER=$O python3 docs/finish6-1115/deps/wi.py $C --trace | head -1)
  v=$(grep -c "TXORDER violation" build/deps-wi-trace.txt)
  echo "$r viol=$v :: $O" | cut -c1-200
done

#!/bin/bash
# tryorders.sh CAND.c NONLOCAL ORDER... : what-if score for each order (worker only, diagnostic)
C=$1; NL=$2; shift 2
for O in "$@"; do
  r=$(TXNONLOCAL=$NL TXORDER=$O python3 docs/finish5-1115/rendA/wi.py $C --trace | head -1)
  v=$(grep -c "TXORDER violation" build/rendA-wi-trace.txt)
  echo "$r viol=$v :: $O" | cut -c1-200
done

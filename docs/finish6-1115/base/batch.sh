#!/bin/bash
# batch.sh FILE... : real (official-equivalent) score of each candidate with the private cc1, no hooks (worker only)
for f in "$@"; do printf '%-40s %s\n' "$(basename $f)" "$(env -u TXORDER -u TXNONLOCAL -u TXLFORCE python3 docs/finish6-1115/base/wi.py $f 2>&1 | head -1)"; done

#!/bin/bash
# dies.sh cand.c : register info lines (deaths/blocks) for pseudos of the projection block (worker only)
set -e
D=$(mktemp -d build/dies-XXXX)
TXDBG= bash docs/finish5-1115/rendB/trace.sh "$1" $D > /dev/null 2>&1 || true
python3 - "$D" <<'PY'
import re, sys
d = sys.argv[1]
t = open(d + '/t.i.lreg').read()
i = t.index('(const_int 65536)'); s = t.rfind('(code_label', 0, i); e = t.find('(code_label', i)
regs = set(int(x) for x in re.findall(r'\(reg(?:/v)?:SI (\d+)\)', t[s:e]))
for m in re.finditer(r'(?m)^Register (\d+) used .*$', t):
    if int(m.group(1)) in regs and ('dies in' in m.group(0) or 'in block 18' not in m.group(0)) and int(m.group(1)) < 1700:
        print(m.group(0)[:150])
PY
rm -rf $D

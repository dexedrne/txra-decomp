#!/usr/bin/env python3
"""Full side-by-side of target vs candidate for 08016DA8 (worker only, diagnostic).
    python3 sbs2.py cand.c [lo_hex hi_hex] [--score] [--regs]
Listings carry no encodings and no pool words."""
import re, sys, difflib
from pathlib import Path
sys.path.insert(0, 'tools'); sys.path.insert(0, 'recomp')
import measure_candidate as mc, draft, reloc, variant_search, diffhint, llm_match as match
START, END = 0x08016DA8, 0x08017E68
args = [a for a in sys.argv[1:] if not a.startswith('--')]
prog = draft.Program(); table = reloc.symbols(prog)
want = prog.rom[START - match.BASE:END - match.BASE]
got, frame = mc.diagnostic_compile(Path(args[0]).read_text(), 'func_%08X' % START, START, table, 'arm')
lo = int(args[1], 16) if len(args) > 1 else 0
hi = int(args[2], 16) if len(args) > 2 else 1 << 40
def lst(data):
    out = []
    for line in diffhint.listing(data, START, 'arm'):
        a, rest = line.split(':', 1)
        if '.word' in rest:
            ins = '.word <pool>'
        else:
            ins = re.split(r'\s{2,}', rest.strip(), maxsplit=1)[-1]
            ins = re.sub(r'\[pc, #-?\d+\] @ =0x[0-9A-F]+', '[pc] =POOL', ins)
        out.append((int(a, 16), ins))
    return out
def norm(ins):
    ins = re.sub(r'\b(r\d+|sb|sl|fp|ip|lr|sp)\b', 'R', ins)
    ins = re.sub(r'0x080[0-9A-Fa-f]{5}', 'ADDR', ins)
    return ins.strip()
T = lst(want); C = lst(got)
A = [norm(i) for _, i in T]; B = [norm(i) for _, i in C]
sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
rows = []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    for k in range(max(i2 - i1, j2 - j1)):
        t = T[i1 + k] if i1 + k < i2 else None
        c = C[j1 + k] if j1 + k < j2 else None
        mark = '  ' if (t and c and t[1] == c[1]) else ('~ ' if tag == 'equal' else '! ')
        rows.append((t[0] if t else None, mark, t, c))
dist, diff = variant_search.score(want, got, START, 'arm')
if '--score' in sys.argv:
    print('diff=%d dist=%d len=%d frame=%s struct=%d reg=%d' % (diff, dist, len(got), frame,
          sum(r[1] == '! ' for r in rows), sum(r[1] == '~ ' for r in rows)))
    sys.exit()
last = 0
for a, mark, t, c in rows:
    if a: last = a
    if lo <= last < hi:
        print('%s%-44s | %s' % (mark, ('%08X %s' % t) if t else '', ('%08X %s' % c) if c else ''))

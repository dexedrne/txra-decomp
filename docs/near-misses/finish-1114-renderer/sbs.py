#!/usr/bin/env python3
"""Side-by-side aligned view of a measure_candidate diff: python3 work/sbs.py work/out/X.diff.txt [start_hex end_hex]"""
import re, sys, difflib
args = [a for a in sys.argv[1:] if not a.startswith('--')]
path = args[0]
lo = int(args[1], 16) if len(args) > 1 else 0
hi = int(args[2], 16) if len(args) > 2 else 1 << 40
tgt, cmp_ = [], []
for line in open(path):
    m = re.match(r'^([ +\-])([0-9A-F]{8}): (.*)$', line.rstrip('\n'))
    if not m: continue
    s, a, ins = m.groups()
    if s in ' -': tgt.append((int(a, 16), ins))
    if s in ' +': cmp_.append((int(a, 16), ins))
def norm(ins):
    ins = re.sub(r'\b(r\d+|sb|sl|fp|ip|lr|sp)\b', 'R', ins)
    ins = re.sub(r'0x[0-9A-Fa-f]{8}', 'ADDR', ins)
    ins = re.sub(r'@.*', '', ins)
    ins = re.sub(r'\[pc, #-?\d+\]', '[pc]', ins)
    ins = re.sub(r'#0x[0-9A-Fa-f]+|#-?\d+', lambda m: m.group(0), ins)
    return ins.strip()
A = [norm(i) for _, i in tgt]; B = [norm(i) for _, i in cmp_]
sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
out = []
last = [0]
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    n = max(i2 - i1, j2 - j1)
    for k in range(n):
        t = tgt[i1 + k] if i1 + k < i2 else None
        c = cmp_[j1 + k] if j1 + k < j2 else None
        if t: last[0] = t[0]
        if not (lo <= last[0] < hi): continue
        mark = '  ' if (t and c and t[1] == c[1]) else ('~ ' if tag == 'equal' else '! ')
        out.append((True, '%s%-46s | %s' % (mark, ('%08X %s' % t) if t else '', ('%08X %s' % c) if c else '')))
if '--score' in sys.argv:
    print('struct=%d reg=%d' % (sum(1 for _, l in out if l.startswith('!')), sum(1 for _, l in out if l.startswith('~'))))
else:
    for _, l in out: print(l)

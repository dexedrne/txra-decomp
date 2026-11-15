#!/usr/bin/env python3
"""Generate dependency-respecting orders of the 8 face-header statements of a base candidate.
    python3 hperm.py base.c outdir"""
import itertools, sys, os
from pathlib import Path
base = Path(sys.argv[1]).read_text(); out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
H = ['a = face->idx[0];', 'b = face->idx[1];', 'c = face->idx[2];', 'd = face->idx[3];',
     'depth[0] = pts[a].depth;', 'depth[1] = pts[b].depth;', 'depth[2] = pts[c].depth;', 'depth[3] = pts[d].depth;']
lines = base.split('\n')
idx = [next(i for i, l in enumerate(lines) if l.strip() == h) for h in H]
assert idx == list(range(idx[0], idx[0] + 8)), idx
ind = lines[idx[0]][:len(lines[idx[0]]) - len(lines[idx[0]].lstrip())]
n = 0
for perm in itertools.permutations(range(8)):
    pos = {p: k for k, p in enumerate(perm)}
    if any(pos[i] > pos[i + 4] for i in range(4)): continue
    new = lines[:idx[0]] + [ind + H[p] for p in perm] + lines[idx[0] + 8:]
    (out / ('h%04d_%s.c' % (n, ''.join(map(str, perm))))).write_text('\n'.join(new))
    n += 1
print(n)

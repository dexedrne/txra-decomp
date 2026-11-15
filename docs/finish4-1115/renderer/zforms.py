#!/usr/bin/env python3
"""Depth-sum spellings for both finish blocks of 08016DA8 (diagnostic, worker only).
    python3 zforms.py BASE.c OUTDIR
BASE.c must contain the two-statement sum `z = depth[0] + depth[3]; z += depth[2] + depth[1];
z = (z >> 7) + 32;` in both paths (g4.c). Writes every order and grouping of the four depth
terms as one expression for the part path, `z = SUM >> 7; z += 32;`, against each of the
120 forms (and the two statement forms) for the direct path."""
import itertools, os, sys
base = open(sys.argv[1]).read(); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
Z = "z = depth[0] + depth[3]; z += depth[2] + depth[1]; z = (z >> 7) + 32;"
i = base.index(Z); j = base.index(Z, i + 1)
D = ['depth[0]', 'depth[1]', 'depth[2]', 'depth[3]']
def trees(xs):
    if len(xs) == 1: yield xs[0]; return
    for k in range(1, len(xs)):
        for l in trees(xs[:k]):
            for r in trees(xs[k:]):
                yield '(%s + %s)' % (l, r)
forms = sorted({t for p in itertools.permutations(D) for t in trees(list(p))})
B = lambda f: 'z = %s >> 7; z += 32;' % f
directs = {('d%03d' % k): B(f) for k, f in enumerate(forms)}
directs['dA'] = Z
directs['dF'] = "z = depth[0] + depth[3]; z += depth[2] + depth[1]; z >>= 7; z += 32;"
for p, pf in enumerate(forms):
    for dk, dv in directs.items():
        s = base[:i] + B(pf) + base[i + len(Z):j] + dv + base[j + len(Z):]
        open(os.path.join(out, 'p%03d_%s.c' % (p, dk)), 'w').write(s)
open(os.path.join(out, 'forms.txt'), 'w').write('\n'.join('%03d %s' % (k, f) for k, f in enumerate(forms)))

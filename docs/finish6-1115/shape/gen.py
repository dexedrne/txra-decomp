#!/usr/bin/env python3
"""Variant generator for the 08016DA8 projection loop (worker or laptop; text only).
    python3 gen.py variants.py OUTDIR      -> OUTDIR/<name>.c for every spec in VARIANTS
A spec is a dict: loop (text replacing the projection block, base.c lines 120-143),
decl (extra function-scope declarations after `s32 tx, k, ty;`), pre (text before the
function, e.g. helpers), rep (list of (old, new) exact replacements applied to the result)."""
import sys, runpy
from pathlib import Path
HERE = Path(__file__).resolve().parent
base = (HERE / 'c' / 'base.c').read_text().split('\n')
head, block, tail = base[:119], base[119:143], base[143:]
assert block[1].strip() == 'for (i = 0; i < 4; i++) {', block[1]
def build(spec):
    h = list(head)
    k = h.index('    s32 tx, k, ty;')
    if spec.get('decl'):
        h.insert(k + 1, spec['decl'])
    if spec.get('pre'):
        f = h.index('void func_08016DA8(void)')
        h.insert(f, spec['pre'])
    loop = spec.get('loop')
    text = '\n'.join(h + ([loop] if loop is not None else block) + tail)
    for old, new in spec.get('rep', []):
        assert text.count(old) == 1, (old, text.count(old))
        text = text.replace(old, new)
    return text
if __name__ == '__main__':
    V = runpy.run_path(sys.argv[1])['VARIANTS']
    out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    for name, spec in V.items():
        (out / (name + '.c')).write_text(build(spec))
    print(len(V), 'written')

#!/usr/bin/env python3
"""gen3.py BODY.c OUTDIR PFX : toggle function-scope sharing of tx/k/ty (direct-path copies) in a tx1_a-based source."""
import sys, os, itertools
src, out, pfx = sys.argv[1:4]; os.makedirs(out, exist_ok=True)
t0 = open(src).read()
SH = {
 'tx': ('                tx = pts[b].sx;\n                gCurPacket->x[1] = tx;\n', '                gCurPacket->x[1] = pts[b].sx;\n'),
 'k':  ('                k = pts[b].sy;\n                gCurPacket->y[1] = k;\n', '                gCurPacket->y[1] = pts[b].sy;\n'),
 'ty': ('                ty = pts[c].sx;\n                gCurPacket->x[2] = ty;\n', '                gCurPacket->x[2] = pts[c].sx;\n'),
}
for bits in itertools.product([1, 0], repeat=3):
    t = t0; loc = []
    for (name, (a, b)), on in zip(SH.items(), bits):
        if not on:
            assert a in t, name
            t = t.replace(a, b); loc.append(name)
    keep = [n for n, on in zip(SH, bits) if on]
    t = t.replace('    s32 tx, k, ty;\n', ('    s32 %s;\n' % ', '.join(keep)) if keep else '')
    if loc:
        t = t.replace('s32 dx, dy, dz, tz, f, sy, sv;', 's32 dx, dy, dz, tz, f, sy, sv, %s;' % ', '.join(loc))
    name = '%s_%s' % (pfx, ''.join(str(x) for x in bits))
    open(os.path.join(out, name + '.c'), 'w').write(t)

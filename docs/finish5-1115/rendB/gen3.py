#!/usr/bin/env python3
"""Rotation-macro shapes for the projection loop: one ROT macro used for the yaw and pitch rotations.
    python3 gen3.py OUTDIR"""
import itertools, sys
sys.path.insert(0, '.')
import mk
from pathlib import Path
C, S, D, F = 'g_03002A18', 'g_03001B28', 'g_03000DF8', 'g_03005F58'
BODIES = {   # x = a*c - b*s ; y = a*s + b*c
 'p': 'x = (a) * (c) - (b) * (s); y = (a) * (s) + (b) * (c);',
 'q': 'x = (a) * (c); x -= (b) * (s); y = (a) * (s); y += (b) * (c);',
 'r': 'y = (a) * (s) + (b) * (c); x = (a) * (c) - (b) * (s);',
 's': 'x = (a) * (c); y = (a) * (s); x -= (b) * (s); y += (b) * (c);',
 't': 'x = (a) * (c) - (b) * (s); y = (b) * (c) + (a) * (s);',
 'u': 'x = (a) * (c); x -= (b) * (s); y = (a) * (s) + (b) * (c);',
}
WRAP = {'d': ('do {', '} while (0)'), 'b': ('{', '}'), 'n': ('', '')}
def macro(body, wrap):
    a, b = WRAP[wrap]
    return '#define ROT(a, b, c, s, x, y) %s %s %s' % (a, body, b)
PRE = {
 'A': ['dx = gScratch[i].x;', 'dx -= gCamera.x;', 'dy = -gScratch[i].y;', 'dy -= gCamera.y;', 'dz = gScratch[i].z - gCamera.z;'],
 'B': ['dx = gScratch[i].x - gCamera.x;', 'dy = -gScratch[i].y - gCamera.y;', 'dz = gScratch[i].z - gCamera.z;'],
}
MID = {
 'a': ['ROT(dx, dz, %s, %s, tx, tz);' % (C, S), 'tz >>= 12;', 'ROT(dy, tz, %s, %s, t, ty);' % (D, F)],
}
POST = {
 'a': ['dx = gOffset.x + (tx >> 12);', 'sy = gOffset.y + (ty >> 12);', 'dy = gOffset.z + (t >> 12);'],
 'b': ['dy = gOffset.z + (t >> 12);', 'dx = gOffset.x + (tx >> 12);', 'sy = gOffset.y + (ty >> 12);'],
 'c': ['dx = gOffset.x + (tx >> 12);', 'dy = gOffset.z + (t >> 12);', 'sy = gOffset.y + (ty >> 12);'],
 'w': ['dx = gOffset.x + (tx >> 12);', 'sy = gOffset.y + (ty >> 12);', 'w = gOffset.z + (t >> 12);'],
}
TAIL = ['g_030055F8[i].x = dy;', 'dy >>= 1;', 'f = g_0804F330[dy + 0x10000];',
        'gCurPacket->x[i] = (((dx << 3) * f) >> 16) + 60;', 'gCurPacket->y[i] = (((sy << 3) * f) >> 15) + 80;']
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
for (bk, body), wk, pk, mk_, qk in itertools.product(BODIES.items(), WRAP, PRE, MID, POST):
    tail = TAIL if qk != 'w' else [x.replace('dy', 'w') if 'dy' in x and x != 'gCurPacket' else x for x in TAIL]
    L = PRE[pk] + MID[mk_] + POST[qk] + tail
    b = 's32 dx, dy, dz, tx, ty, tz, f, sy, t, w;\n' + '\n'.join(L)
    src = mk.build(b, pre_func=macro(body, wk))
    (out / ('m_%s%s%s%s%s.c' % (bk, wk, pk, mk_, qk))).write_text(src)

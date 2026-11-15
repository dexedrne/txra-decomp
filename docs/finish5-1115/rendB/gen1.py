#!/usr/bin/env python3
"""Generate projection-loop spelling variants (tx / s / ty / sy forms) on the dy-reuse base."""
import itertools, sys
sys.path.insert(0, '.')
import mk
from pathlib import Path
C, S, D, F = 'g_03002A18', 'g_03001B28', 'g_03000DF8', 'g_03005F58'
TX = {
 'a': ['tx = dx * %s;' % C, 'tx -= dz * %s;' % S],
 'b': ['s = dz * %s;' % S, 'tx = dx * %s;' % C, 'tx -= s;'],
 'c': ['tx = dx * %s;' % C, 's = dz * %s;' % S, 'tx -= s;'],
 'd': ['tx = dz * %s;' % S, 'tx = dx * %s - tx;' % C],
 'e': ['tx = -(dz * %s);' % S, 'tx += dx * %s;' % C],
 'f': ['tx = dx * %s;' % C, 'tx = tx - dz * %s;' % S],
 'g': ['s = dz * %s;' % S, 'tx = dx * %s - s;' % C],
 'h': ['tx = dx * %s;' % C, 's = dz * %s;' % S, 'tx = tx - s;'],
}
TY = {
 'a': ['ty = dy * %s + tz * %s;' % (F, D)],
 'b': ['ty = dy * %s;' % F, 'ty += tz * %s;' % D],
 'c': ['ty = tz * %s;' % D, 'ty += dy * %s;' % F],
 'd': ['ty = tz * %s + dy * %s;' % (D, F)],
 'e': ['ty = tz * %s;' % D, 'ty = dy * %s + ty;' % F],
 'f': ['u = tz * %s;' % D, 'ty = dy * %s + u;' % F],
}
SY = {
 'a': ['sy = gOffset.y + (ty >> 12);'],
 'b': ['ty >>= 12;', 'sy = gOffset.y + ty;'],
 'c': ['ty = gOffset.y + (ty >> 12);'],
 'd': ['ty >>= 12;', 'ty += gOffset.y;'],
}
def body(tx, ty, sy):
    L = ['dx = gScratch[i].x;', 'dx -= gCamera.x;', 'dy = -gScratch[i].y;', 'dy -= gCamera.y;',
         'dz = gScratch[i].z - gCamera.z;'] + TX[tx] + [
         'tz = (dx * %s + dz * %s) >> 12;' % (S, C),
         't = dy * %s - tz * %s;' % (D, F)] + TY[ty] + [
         'dx = gOffset.x + (tx >> 12);'] + SY[sy] + [
         'dy = gOffset.z + (t >> 12);', 'g_030055F8[i].x = dy;', 'dy >>= 1;', 'f = g_0804F330[dy + 0x10000];',
         'gCurPacket->x[i] = (((dx << 3) * f) >> 16) + 60;']
    yv = 'ty' if sy in ('c', 'd') else 'sy'
    L.append('gCurPacket->y[i] = ((((%s) << 3) * f) >> 15) + 80;' % yv)
    return 's32 dx, dy, dz, tx, ty, tz, f, sy, t, s, u;\n' + '\n'.join(L)
for tx, ty, sy in itertools.product(TX, TY, SY):
    t = mk.build(body(tx, ty, sy))
    (Path('v') / ('g1_%s%s%s.c' % (tx, ty, sy))).write_text(t)

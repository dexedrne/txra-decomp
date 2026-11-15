# Batch 2: scheduling barriers from empty loops at several positions (loop-note effects on loop.c).
import runpy
from pathlib import Path
v1 = runpy.run_path(str(Path(__file__).resolve().parent / 'v1.py'))
L, BASE = v1['L'], v1['BASE']
lines = BASE.split('\n')
BAR = {'dw': 'do { } while (0);', 'w0': 'while (0) { }', 'f0': 'for (;;) break;'}
V = {}
for bn, b in BAR.items():
    for pos in range(0, len(lines) + 1):
        body = '\n'.join(lines[:pos] + [b] + lines[pos:])
        V['b_%s_%02d' % (bn, pos)] = dict(loop=L(body))
# reordered: tz split, tx -= k late, barrier before the DF8 statement
R = """dx = gScratch[i].x;
dx -= gCamera.x;
dy = -gScratch[i].y;
dy -= gCamera.y;
dz = gScratch[i].z - gCamera.z;
tx = dx * g_03002A18;
k = dz * g_03001B28;
tz = dx * g_03001B28 + dz * g_03002A18;
BAR
tz >>= 12;
t = dy * g_03000DF8 - tz * g_03005F58;
ty = dy * g_03005F58 + tz * g_03000DF8;
tx -= k;
dx = gOffset.x + (tx >> 12);
sy = gOffset.y + (ty >> 12);
dy = gOffset.z + (t >> 12);
g_030055F8[i].x = dy;
dy >>= 1;
f = g_0804F330[dy + 0x10000];
gCurPacket->x[i] = (((dx << 3) * f) >> 16) + 60;
gCurPacket->y[i] = (((sy << 3) * f) >> 15) + 80;"""
for bn, b in BAR.items():
    V['r_%s' % bn] = dict(loop=L(R.replace('BAR', b)))
V['r_none'] = dict(loop=L(R.replace('BAR\n', '')))
VARIANTS = V

#!/usr/bin/env python3
"""gen1.py OUTDIR : variants of s2 (saved_y copy) around the tx statement and statement order."""
import sys, itertools, os, subprocess
BASE = sys.argv[2] if len(sys.argv) > 2 else 'c/h7x2.c'; out = sys.argv[1]; os.makedirs(out, exist_ok=True)
IND = ' ' * 28
pre = ['s32 dx, dy, dz, tz, f, sy, sv;',
       'dx = gScratch[i].x;', 'dx -= gCamera.x;', 'dy = -gScratch[i].y;', 'dy -= gCamera.y;',
       'dz = gScratch[i].z - gCamera.z;']
TX = {
 'a': ['tx = dx * g_03002A18;', 'k = dz * g_03001B28;', 'tx -= k;'],
 'b': ['k = dz * g_03001B28;', 'tx = dx * g_03002A18 - k;'],
 'c': ['tx = dx * g_03002A18 - (k = dz * g_03001B28);'],
 'd': ['k = dz * g_03001B28;', 'tx = dx * g_03002A18;', 'tx -= k;'],
 'e': ['tx = dx * g_03002A18;', 'tx -= k = dz * g_03001B28;'],
 'f': ['k = dz * g_03001B28;', 'tx = -k + dx * g_03002A18;'],
}
SV = ['sv = dy;']
TZ = ['tz = (dx * g_03001B28 + dz * g_03002A18) >> 12;']
ROT = ['dy = (sv * g_03000DF8 - tz * g_03005F58) >> 12;', 'ty = sv * g_03005F58 + tz * g_03000DF8;']
OFF = {'xyz': ['dx = gOffset.x + (tx >> 12);', 'sy = gOffset.y + (ty >> 12);', 'dy += gOffset.z;'],
       'zxy': ['dy += gOffset.z;', 'dx = gOffset.x + (tx >> 12);', 'sy = gOffset.y + (ty >> 12);'],
       'xzy': ['dx = gOffset.x + (tx >> 12);', 'dy += gOffset.z;', 'sy = gOffset.y + (ty >> 12);']}
post = ['g_030055F8[i].x = dy;', 'dy >>= 1;', 'f = g_0804F330[dy + 0x10000];',
        'gCurPacket->x[i] = (((dx << 3) * f) >> 16) + 60;', 'gCurPacket->y[i] = (((sy << 3) * f) >> 15) + 80;']
PFX = sys.argv[3] if len(sys.argv) > 3 else 'g1'
n = 0
for tk, tx in TX.items():
    for order in ['tx,sv,tz', 'sv,tx,tz', 'tx,tz,sv', 'sv,tz,tx', 'tz,tx,sv', 'tz,sv,tx']:
        for ok, off in OFF.items():
            parts = {'tx': tx, 'sv': SV, 'tz': TZ}
            mid = sum((parts[p] for p in order.split(',')), [])
            # tz must precede ROT; sv must precede ROT: all orders keep ROT after
            body = pre + mid + ROT + off + post
            name = PFX + '_%s_%s_%s' % (tk, order.replace(',', ''), ok)
            open(os.path.join(out, name + '.txt'), 'w').write('\n'.join(IND + l for l in body) + '\n')
            subprocess.run(['python3', 'mk.py', BASE, os.path.join(out, name + '.txt'), os.path.join(out, name + '.c')], check=True)
            n += 1
print(n)

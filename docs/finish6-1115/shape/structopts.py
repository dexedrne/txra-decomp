#!/usr/bin/env python3
"""Exhaustive structural options for the 08016DA8 projection loop (text generator only):
DF8/F58 load in a direct-path-shared variable or inline; y chain form and depth reuse; tx/k form;
tx/k/ty homes (block-local or the finish-5 shared variables); tz split; t in place.
    python3 structopts.py OUTDIR   -> OUTDIR/<name>.c, OUTDIR/index.txt"""
import sys, itertools
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen
SL = {
 'x1': ('                gCurPacket->x[1] = pts[b].sx;', '                %s = pts[b].sx;\n                gCurPacket->x[1] = %s;'),
 'y2': ('                gCurPacket->y[2] = pts[c].sy;', '                %s = pts[c].sy;\n                gCurPacket->y[2] = %s;'),
 'x3': ('                gCurPacket->x[3] = pts[d].sx;', '                %s = pts[d].sx;\n                gCurPacket->x[3] = %s;'),
 'y3': ('                gCurPacket->y[3] = pts[d].sy;', '                %s = pts[d].sy;\n                gCurPacket->y[3] = %s;'),
}
BASE_TXH = ('            tx = pts[b].depth;\n            depth[1] = tx;', '            depth[1] = pts[b].depth;')
BASE_K = ('                k = pts[b].sy;\n                gCurPacket->y[1] = k;', '                gCurPacket->y[1] = pts[b].sy;')
BASE_TY = ('                ty = pts[c].sx;\n                gCurPacket->x[2] = ty;', '                gCurPacket->x[2] = pts[c].sx;')
def build(o):
    c8 = 'c8' if o['d8'] != '-' else 'g_03000DF8'
    c5 = 'c5' if o['f5'] != '-' else 'g_03005F58'
    TX = 'tx'; K = 'k'; TY = 'ty'
    L = ['dx = gScratch[i].x;', 'dx -= gCamera.x;']
    if o['dy'] == 'g6':
        L += ['dy = -gScratch[i].y - gCamera.y;']
    elif o['dy'] == 'ip':
        L += ['dy = -gScratch[i].y;', 'dy -= gCamera.y;']
    else:
        L += ['dy = -gScratch[i].y - gCamera.y;']
    L += ['dz = gScratch[i].z - gCamera.z;']
    if o['tx'] == 'single':
        L += ['%s = dx * g_03002A18 - dz * g_03001B28;' % TX]
    elif o['tx'] == 'ip':
        L += ['%s = dx * g_03002A18;' % TX, '%s = dz * g_03001B28;' % K, '%s -= %s;' % (TX, K)]
    else:
        L += ['%s = dz * g_03001B28;' % K, '%s = dx * g_03002A18 - %s;' % (TX, K)]
    if o['tz']:
        L += ['tz = dx * g_03001B28 + dz * g_03002A18;', 'tz >>= 12;']
    else:
        L += ['tz = (dx * g_03001B28 + dz * g_03002A18) >> 12;']
    if o['d8'] != '-': L += ['c8 = g_03000DF8;']
    if o['f5'] != '-': L += ['c5 = g_03005F58;']
    if o['t']:
        L += ['t = dy * %s;' % c8, 't -= tz * %s;' % c5]
    else:
        L += ['t = dy * %s - tz * %s;' % (c8, c5)]
    L += ['%s = dy * %s + tz * %s;' % (TY, c5, c8)]
    DP = 'w' if o['dy'] == 'g6' else 'dy'
    L += ['dx = gOffset.x + (%s >> 12);' % TX, 'sy = gOffset.y + (%s >> 12);' % TY,
          '%s = gOffset.z + (t >> 12);' % DP, 'g_030055F8[i].x = %s;' % DP, '%s >>= 1;' % DP,
          'f = g_0804F330[%s + 0x10000];' % DP,
          'gCurPacket->x[i] = (((dx << 3) * f) >> 16) + 60;', 'gCurPacket->y[i] = (((sy << 3) * f) >> 15) + 80;']
    locs = ['dx', 'dy', 'dz']
    if o['txh'] == 'l': locs.append('tx')
    if o['tyh'] == 'l': locs.append('ty')
    if o['tx'] != 'single' and o['kh'] == 'l': locs.append('k')
    locs += ['tz', 'f', 'sy'] + (['w'] if o['dy'] == 'g6' else []) + ['t']
    I, J = ' ' * 24, ' ' * 28
    loop = '\n'.join([I[:-4] + '{', I + 'for (i = 0; i < 4; i++) {', J + 's32 ' + ', '.join(locs) + ';']
                     + [J + s for s in L] + [I + '}', I[:-4] + '}'])
    rep, dec = [], []
    if o['txh'] == 'l': rep.append(BASE_TXH)
    if o['tyh'] == 'l': rep.append(BASE_TY)
    if o['tx'] == 'single' or o['kh'] == 'l': rep.append(BASE_K)
    for v, s in (('c8', o['d8']), ('c5', o['f5'])):
        if s != '-':
            old, new = SL[s]; rep.append((old, new % (v, v))); dec.append(v)
    text = gen.build(dict(loop=loop, decl=('    s32 ' + ', '.join(dec) + ';') if dec else None))
    for old, new in rep:
        assert text.count(old) == 1, (old, o)
        text = text.replace(old, new)
    if o['txh'] == 'l' and o['tyh'] == 'l' and (o['tx'] == 'single' or o['kh'] == 'l'):
        text = text.replace('    s32 tx, k, ty;\n', '')
    return text
def opts():
    for d8, f5 in itertools.product(['-', 'x1', 'y2', 'x3', 'y3'], repeat=2):
        if d8 != '-' and d8 == f5: continue
        for dy, tx, txh, kh, tyh, tz, t in itertools.product(['g6', 'ip', 'sr'], ['single', 'ip', 'ks'], 'ls', 'ls', 'ls', (0, 1), (0, 1)):
            if tx == 'single' and kh == 's': continue
            yield dict(d8=d8, f5=f5, dy=dy, tx=tx, txh=txh, kh=kh, tyh=tyh, tz=tz, t=t)
if __name__ == '__main__':
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    idx = []
    for n, o in enumerate(opts()):
        name = 's%05d' % n
        (out / (name + '.c')).write_text(build(o))
        idx.append('%s %s' % (name, ','.join('%s=%s' % kv for kv in o.items())))
    (out / 'index.txt').write_text('\n'.join(idx) + '\n')
    print(len(idx), 'written')

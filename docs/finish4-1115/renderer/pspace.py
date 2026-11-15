#!/usr/bin/env python3
"""Structured space of projection-loop spellings for 08016DA8 (diagnostic, worker only).
    python3 pspace.py BASE.c OUTDIR
Every variant is behaviour-preserving plain C: in-place forms, temporaries placed
before use, variable reuse only where the old value is dead, output statements in
any order that respects data dependencies."""
import itertools, os, sys
base = open(sys.argv[1]).read(); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
head = '                        for (i = 0; i < 4; i++) {\n'
s0 = base.index(head) + len(head)
s1 = base.index('\n                        }', s0)
IND = ' ' * 28
G = {'cos': 'g_03002A18', 'sin': 'g_03001B28', 'df8': 'g_03000DF8', 'f58': 'g_03005F58'}
n = 0
opts = itertools.product(
    [0, 1],          # dy in place
    [0, 1],          # dz in place
    [0, 1],          # tx in place
    [0, 1],          # tz shift as its own statement
    ['dy', 'w'],     # variable holding the depth
    ['sy', 'dz'],    # variable holding screen y
    [0, 1, 2],       # t: 0 temp before ty, 1 temp after ty, 2 inline
    list(itertools.permutations(['SX', 'SY', 'W'])),
)
for dyip, dzip, txip, tzsp, wv, syv, tpos, oord in opts:
    if syv == 'dz' and False:
        continue
    L = ['dx = gScratch[i].x;', 'dx -= gCamera.x;']
    L += (['dy = -gScratch[i].y;', 'dy -= gCamera.y;'] if dyip else ['dy = -gScratch[i].y - gCamera.y;'])
    L += (['dz = gScratch[i].z;', 'dz -= gCamera.z;'] if dzip else ['dz = gScratch[i].z - gCamera.z;'])
    L += (['tx = dx * %(cos)s;' % G, 'tx -= dz * %(sin)s;' % G] if txip else ['tx = dx * %(cos)s - dz * %(sin)s;' % G])
    L += (['tz = dx * %(sin)s + dz * %(cos)s;' % G, 'tz >>= 12;'] if tzsp else ['tz = (dx * %(sin)s + dz * %(cos)s) >> 12;' % G])
    T = 't = dy * %(df8)s - tz * %(f58)s;' % G
    TY = 'ty = dy * %(f58)s + tz * %(df8)s;' % G
    if tpos == 0: L += [T, TY]
    elif tpos == 1: L += [TY, T]
    else: L += [TY]
    wexpr = '(t >> 12)' if tpos != 2 else '((dy * %(df8)s - tz * %(f58)s) >> 12)' % G
    # reuse checks: w in dy needs dy dead -> after t/ty (true here). sy in dz: dz dead after tx/tz (true).
    S = {'SX': 'dx = gOffset.x + (tx >> 12);', 'SY': '%s = gOffset.y + (ty >> 12);' % syv,
         'W': '%s = gOffset.z + %s;' % (wv, wexpr)}
    if tpos == 2 and wv == 'dy' and oord.index('W') > 0:
        pass
    L += [S[k] for k in oord]
    L += ['g_030055F8[i].x = %s;' % wv, '%s >>= 1;' % wv, 'f = g_0804F330[%s + 0x10000];' % wv,
          'gCurPacket->x[i] = (((dx << 3) * f) >> 16) + 60;',
          'gCurPacket->y[i] = (((%s << 3) * f) >> 15) + 80;' % syv]
    used = ['dx', 'dy', 'dz', 'tx', 'ty', 'tz', 'f'] + (['sy'] if syv == 'sy' else []) + (['w'] if wv == 'w' else []) + (['t'] if tpos != 2 else [])
    body = IND + 's32 ' + ', '.join(used) + ';\n' + '\n'.join(IND + l for l in L)
    tag = 'v%d%d%d%d_%s_%s_%d_%s' % (dyip, dzip, txip, tzsp, wv, syv, tpos, ''.join(k[0] + k[-1] for k in oord))
    open(os.path.join(out, tag + '.c'), 'w').write(base[:s0] + body + base[s1:])
    n += 1
print(n)

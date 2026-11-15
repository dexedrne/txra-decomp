#!/usr/bin/env python3
"""Random dependence-respecting statement orders and spelling options for the 08016DA8 projection
loop (text generator only). Family: DF8 (or F58) in a function-scope variable that the direct path
also uses, final tx in a birthing temporary u.
    python3 perm.py OUTDIR N SEED [FAMILY]   -> OUTDIR/<hash>.c and OUTDIR/index.txt"""
import sys, random, hashlib, re
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen
SLOT = {
 'w1': ('                gCurPacket->x[1] = pts[b].sx;', '                w = pts[b].sx;\n                gCurPacket->x[1] = w;'),
 'y2': ('                gCurPacket->y[2] = pts[c].sy;', '                w = pts[c].sy;\n                gCurPacket->y[2] = w;'),
 'x3': ('                gCurPacket->x[3] = pts[d].sx;', '                w = pts[d].sx;\n                gCurPacket->x[3] = w;'),
 'y3': ('                gCurPacket->y[3] = pts[d].sy;', '                w = pts[d].sy;\n                gCurPacket->y[3] = w;'),
}
def stmts(o):
    C8 = 'w' if o['g'] == 'd8' else 'g_03000DF8'
    C5 = 'w' if o['g'] == 'f58' else 'g_03005F58'
    S = []   # (name, text, reads, writes)
    def add(n, t, r, w): S.append((n, t, set(r.split()), set(w.split())))
    add('x1', 'dx = gScratch[i].x;', 'SX', 'dx')
    add('x2', 'dx -= gCamera.x;', 'dx CX', 'dx')
    add('y1', 'dy = -gScratch[i].y;', 'SY', 'dy')
    add('y2', 'dy -= gCamera.y;', 'dy CY', 'dy')
    add('z1', 'dz = gScratch[i].z - gCamera.z;', 'SZ CZ', 'dz')
    add('tx', 'tx = dx * g_03002A18;', 'dx', 'tx')
    add('k', 'k = dz * g_03001B28;', 'dz', 'k')
    if o['u'] == 'u':
        add('u', 'u = tx - k;', 'tx k', 'u'); TXF = 'u'
    else:
        add('u', 'tx -= k;', 'tx k', 'tx'); TXF = 'tx'
    if o['tzsplit']:
        add('tz1', 'tz = dx * g_03001B28 + dz * g_03002A18;', 'dx dz', 'tz')
        add('tz2', 'tz >>= 12;', 'tz', 'tz')
    else:
        add('tz1', 'tz = (dx * g_03001B28 + dz * g_03002A18) >> 12;', 'dx dz', 'tz')
    if o['g'] == 'd8': add('w', 'w = g_03000DF8;', '', 'w')
    if o['g'] == 'f58': add('w', 'w = g_03005F58;', '', 'w')
    gw = 'w' if o['g'] in ('d8', 'f58') else ''
    if o['tinp']:
        add('t1', 't = dy * %s;' % C8, 'dy ' + gw, 't'); add('t2', 't -= tz * %s;' % C5, 't tz ' + gw, 't')
    else:
        add('t1', 't = dy * %s - tz * %s;' % (C8, C5), 'dy tz ' + gw, 't')
    if o['tyinp']:
        add('ty1', 'ty = tz * %s;' % C8, 'tz ' + gw, 'ty'); add('ty2', 'ty += dy * %s;' % C5, 'ty dy ' + gw, 'ty')
    else:
        add('ty1', 'ty = dy * %s + tz * %s;' % (C5, C8), 'dy tz ' + gw, 'ty')
    add('sx', 'dx = gOffset.x + (%s >> 12);' % TXF, TXF + ' OX', 'dx')
    add('sy', 'sy = gOffset.y + (ty >> 12);', 'ty OY', 'sy')
    add('dp', 'dy = gOffset.z + (t >> 12);', 't OZ', 'dy')
    add('st', 'g_030055F8[i].x = dy;', 'dy', 'MEM')
    add('h', 'dy >>= 1;', 'dy', 'dy')
    add('f', 'f = g_0804F330[dy + 0x10000];', 'dy', 'f')
    add('px', 'gCurPacket->x[i] = (((dx << 3) * f) >> 16) + 60;', 'dx f', 'MEM')
    add('py', 'gCurPacket->y[i] = (((sy << 3) * f) >> 15) + 80;', 'sy f', 'MEM')
    return S
FIXED = [('x1', 'y1'), ('y1', 'z1'), ('x2', 'y2'), ('y2', 'z1'), ('sx', 'sy'), ('sy', 'dp'), ('px', 'py')]
def order(S, rnd, keep_prob):
    n = len(S); idx = {s[0]: i for i, s in enumerate(S)}
    pred = {i: set() for i in range(n)}
    for j in range(n):
        for i in range(j):
            ri, wi_, rj, wj = S[i][2], S[i][3], S[j][2], S[j][3]
            if (wi_ & rj) or (ri & wj) or (wi_ & wj):
                pred[j].add(i)
    for a, b in FIXED:
        if a in idx and b in idx: pred[idx[b]].add(idx[a])
    done, out = set(), []
    while len(out) < n:
        ready = [i for i in range(n) if i not in done and pred[i] <= done]
        i = min(ready) if rnd.random() < keep_prob else rnd.choice(ready)
        done.add(i); out.append(S[i])
    return out
def build(o, seq):
    I, J = ' ' * 24, ' ' * 28
    locs = 's32 dx, dy, dz, tz, f, sy, t' + (', u' if o['u'] == 'u' else '') + ';'
    loop = '\n'.join([I[:-4] + '{', I + 'for (i = 0; i < 4; i++) {', J + locs] + [J + s[1] for s in seq] + [I + '}', I[:-4] + '}'])
    spec = dict(loop=loop)
    if o['g'] in ('d8', 'f58'):
        spec['decl'] = '    s32 w;'; spec['rep'] = [SLOT[o['slot']]]
    return gen.build(spec)
def rand_opts(rnd, fam):
    return dict(g=fam if fam != 'mix' else rnd.choice(['d8', 'f58', 'none']), slot=rnd.choice(list(SLOT)),
                u=rnd.choice(['u', 'u', 'tx']), tzsplit=rnd.random() < 0.3, tinp=rnd.random() < 0.3,
                tyinp=rnd.random() < 0.2)
if __name__ == '__main__':
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    n, rnd = int(sys.argv[2]), random.Random(int(sys.argv[3]))
    fam = sys.argv[4] if len(sys.argv) > 4 else 'd8'
    idx, seen = [], set()
    while len(idx) < n:
        o = rand_opts(rnd, fam)
        seq = order(stmts(o), rnd, rnd.choice([0.5, 0.8, 0.95]))
        key = '%s|%s' % (','.join('%s=%s' % kv for kv in sorted(o.items())), ' '.join(s[0] for s in seq))
        if key in seen: continue
        seen.add(key)
        h = hashlib.sha1(key.encode()).hexdigest()[:10]
        (out / (h + '.c')).write_text(build(o, seq)); idx.append('%s %s' % (h, key))
    (out / 'index.txt').write_text('\n'.join(idx) + '\n')
    print(len(idx), 'written')

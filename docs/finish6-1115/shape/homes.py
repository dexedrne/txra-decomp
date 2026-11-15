#!/usr/bin/env python3
"""'Generic temporaries' family for the 08016DA8 projection loop (text generator only).
Each loop value is spelled with a chosen home variable: a fresh block-local, an existing
function-scope variable that is dead during the loop (n, z, tick), or a new function-scope
variable that the direct path also uses for one point-to-packet copy (w1..w4).
    python3 homes.py OUTDIR N SEED        -> N random specs, OUTDIR/<hash>.c + OUTDIR/index.txt
    python3 homes.py --one 'KEY=VAL,...' OUT.c"""
import sys, random, hashlib, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gen
SLOTS = {
 'w1': ('                gCurPacket->x[1] = pts[b].sx;', '                w1 = pts[b].sx;\n                gCurPacket->x[1] = w1;'),
 'w2': ('                gCurPacket->y[2] = pts[c].sy;', '                w2 = pts[c].sy;\n                gCurPacket->y[2] = w2;'),
 'w3': ('                gCurPacket->x[3] = pts[d].sx;', '                w3 = pts[d].sx;\n                gCurPacket->x[3] = w3;'),
 'w4': ('                gCurPacket->y[3] = pts[d].sy;', '                w4 = pts[d].sy;\n                gCurPacket->y[3] = w4;'),
}
HOMES = ['loc', 'n', 'z', 'tick', 'w1', 'w2', 'w3', 'w4']
# value -> default local name
VALS = ['DX', 'DY', 'DZ', 'TZ', 'T', 'SY', 'F', 'DF8', 'F58', 'CAMY', 'COS', 'SIN']
LOCAL = {'DX': 'dx', 'DY': 'dy', 'DZ': 'dz', 'TZ': 'tz', 'T': 't', 'SY': 'sy', 'F': 'f',
         'DF8': 'c8', 'F58': 'c5', 'CAMY': 'cy', 'COS': 'cc', 'SIN': 'ss'}
OPTIONAL = {'DF8', 'F58', 'CAMY', 'COS', 'SIN'}   # 'inl' = not named
def body(spec):
    v = {k: (LOCAL[k] if spec.get(k, 'loc') == 'loc' else spec[k]) for k in VALS}
    nm = lambda k: spec.get(k, 'inl' if k in OPTIONAL else 'loc') != 'inl'
    cos = v['COS'] if nm('COS') else 'g_03002A18'
    sin = v['SIN'] if nm('SIN') else 'g_03001B28'
    d8 = v['DF8'] if nm('DF8') else 'g_03000DF8'
    f58 = v['F58'] if nm('F58') else 'g_03005F58'
    DX, DY, DZ, TZ, T, SY, F = (v[k] for k in ('DX', 'DY', 'DZ', 'TZ', 'T', 'SY', 'F'))
    L = []
    L += ['%s = gScratch[i].x;' % DX, '%s -= gCamera.x;' % DX]
    L += ['%s = -gScratch[i].y;' % DY]
    if nm('CAMY'): L += ['%s = gCamera.y;' % v['CAMY'], '%s -= %s;' % (DY, v['CAMY'])]
    else: L += ['%s -= gCamera.y;' % DY]
    L += ['%s = gScratch[i].z - gCamera.z;' % DZ]
    if nm('COS'): L += ['%s = g_03002A18;' % cos]
    if nm('SIN'): L += ['%s = g_03001B28;' % sin]
    L += ['tx = %s * %s;' % (DX, cos), 'k = %s * %s;' % (DZ, sin), 'tx -= k;']
    if spec.get('tzsplit'):
        L += ['%s = %s * %s + %s * %s;' % (TZ, DX, sin, DZ, cos), '%s >>= 12;' % TZ]
    else:
        L += ['%s = (%s * %s + %s * %s) >> 12;' % (TZ, DX, sin, DZ, cos)]
    if nm('DF8'): L += ['%s = g_03000DF8;' % d8]
    if nm('F58'): L += ['%s = g_03005F58;' % f58]
    if spec.get('tinp'):
        L += ['%s = %s * %s;' % (T, DY, d8), '%s -= %s * %s;' % (T, TZ, f58)]
    else:
        L += ['%s = %s * %s - %s * %s;' % (T, DY, d8, TZ, f58)]
    L += ['ty = %s * %s + %s * %s;' % (DY, f58, TZ, d8)]
    L += ['%s = gOffset.x + (tx >> 12);' % DX, '%s = gOffset.y + (ty >> 12);' % SY,
          '%s = gOffset.z + (%s >> 12);' % (DY, T), 'g_030055F8[i].x = %s;' % DY, '%s >>= 1;' % DY,
          '%s = g_0804F330[%s + 0x10000];' % (F, DY),
          'gCurPacket->x[i] = (((%s << 3) * %s) >> 16) + 60;' % (DX, F),
          'gCurPacket->y[i] = (((%s << 3) * %s) >> 15) + 80;' % (SY, F)]
    ORDER = ['dx', 'dy', 'dz', 'tz', 'f', 'sy', 't', 'c8', 'c5', 'cy', 'cc', 'ss']
    have = {LOCAL[k] for k in VALS if spec.get(k, 'inl' if k in OPTIONAL else 'loc') == 'loc'}
    locs = [x for x in ORDER if x in have]
    return L, locs
def build(spec):
    L, locs = body(spec)
    I, J = ' ' * 24, ' ' * 28
    loop = '\n'.join([I[:-4] + '{', I + 'for (i = 0; i < 4; i++) {'] + ([J + 's32 ' + ', '.join(locs) + ';'] if locs else [])
                     + [J + s for s in L] + [I + '}', I[:-4] + '}'])
    used = sorted({spec[k] for k in VALS if spec.get(k) in SLOTS})
    s = dict(loop=loop, rep=[SLOTS[w] for w in used])
    if used: s['decl'] = '    s32 ' + ', '.join(used) + ';'
    return gen.build(s)
def valid(spec):
    hs = [spec[k] for k in VALS if spec.get(k) not in (None, 'loc', 'inl')]
    return len(hs) == len(set(hs))
def rand_spec(rnd):
    while True:
        s = {}
        for k in VALS:
            p = rnd.random()
            if k in OPTIONAL:
                s[k] = 'inl' if p < 0.55 else ('loc' if p < 0.7 else rnd.choice(HOMES[1:]))
            else:
                s[k] = 'loc' if p < 0.6 else rnd.choice(HOMES[1:])
        s['tzsplit'] = rnd.random() < 0.3
        s['tinp'] = rnd.random() < 0.3
        if valid(s): return s
def key(spec):
    return ','.join('%s=%s' % (k, spec[k]) for k in sorted(spec) if spec[k] not in ('loc', 'inl', False))
def parse(txt):
    s = {}
    for kv in filter(None, txt.split(',')):
        a, b = kv.split('=')
        s[a] = True if b == 'True' else b
    return s
if __name__ == '__main__':
    if sys.argv[1] == '--one':
        Path(sys.argv[3]).write_text(build(parse(sys.argv[2]))); sys.exit()
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    n, rnd = int(sys.argv[2]), random.Random(int(sys.argv[3]))
    idx = []
    seen = set()
    while len(idx) < n:
        s = rand_spec(rnd); kk = key(s)
        if kk in seen: continue
        seen.add(kk)
        h = hashlib.sha1(kk.encode()).hexdigest()[:10]
        (out / (h + '.c')).write_text(build(s)); idx.append('%s %s' % (h, kk))
    (out / 'index.txt').write_text('\n'.join(idx) + '\n')
    print(len(idx), 'written')

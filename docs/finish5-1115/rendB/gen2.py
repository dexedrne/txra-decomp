#!/usr/bin/env python3
"""Random spelling generator for the projection loop (dy reused for the depth), for the locality
scan.  python3 gen2.py OUTDIR N SEED"""
import random, re, sys
sys.path.insert(0, '.')
import mk
from pathlib import Path
C, S, D, F = 'g_03002A18', 'g_03001B28', 'g_03000DF8', 'g_03005F58'
G = {
 'dx': [['dx = gScratch[i].x;', 'dx -= gCamera.x;'], ['dx = gScratch[i].x - gCamera.x;']],
 'dy': [['dy = -gScratch[i].y;', 'dy -= gCamera.y;'], ['dy = -gScratch[i].y - gCamera.y;']],
 'dz': [['dz = gScratch[i].z - gCamera.z;'], ['dz = gScratch[i].z;', 'dz -= gCamera.z;']],
 'tx': [['tx = dx * C;', 'tx -= dz * S;'], ['s = dz * S;', 'tx = dx * C;', 'tx -= s;'],
        ['tx = dx * C;', 's = dz * S;', 'tx -= s;'], ['s = dz;', 's *= S;', 'tx = dx * C;', 'tx -= s;'],
        ['tx = dx;', 'tx *= C;', 's = dz;', 's *= S;', 'tx -= s;'], ['tx = dx * C;', 'tx = tx - dz * S;'],
        ['s = dz * S;', 'tx = dx * C - s;'], ['tx = C;', 'tx *= dx;', 's = S;', 's *= dz;', 'tx -= s;'],
        ['s = dz * S;', 's = -s;', 'tx = dx * C;', 'tx += s;'], ['s = -dz * S;', 'tx = dx * C;', 'tx += s;'],
        ['s = dz * S;', 'tx = -s;', 'tx += dx * C;'], ['tx = dx * C;', 's = dz;', 's = s * S;', 'tx -= s;']],
 'tz': [['tz = (dx * S + dz * C) >> 12;'], ['tz = dx * S + dz * C;', 'tz >>= 12;'],
        ['tz = dx * S;', 'tz += dz * C;', 'tz >>= 12;'], ['tz = dz * C;', 'tz += dx * S;', 'tz >>= 12;'],
        ['tz = (dz * C + dx * S) >> 12;']],
 't':  [['t = dy * D - tz * F;'], ['t = dy * D;', 't -= tz * F;']],
 'ty': [['ty = dy * F + tz * D;'], ['ty = dy * F;', 'ty += tz * D;'], ['u = tz * D;', 'ty = dy * F + u;'],
        ['u = tz * D;', 'ty = dy * F;', 'ty += u;'], ['ty = dy;', 'ty *= F;', 'ty += tz * D;']],
 'sx': [['dx = gOffset.x + (tx >> 12);'], ['tx >>= 12;', 'dx = gOffset.x + tx;'], ['dx = tx >> 12;', 'dx += gOffset.x;']],
 'sy': [['sy = gOffset.y + (ty >> 12);'], ['ty >>= 12;', 'sy = gOffset.y + ty;'], ['sy = ty >> 12;', 'sy += gOffset.y;']],
 'w':  [['dy = gOffset.z + (t >> 12);'], ['t >>= 12;', 'dy = gOffset.z + t;'], ['dy = t >> 12;', 'dy += gOffset.z;']],
}
ORDER = ['dx', 'dy', 'dz', 'tx', 'tz', 't', 'ty', 'sx', 'sy', 'w']
DEPS = {'tx': {'dx', 'dz'}, 'tz': {'dx', 'dz'}, 't': {'dy', 'tz'}, 'ty': {'dy', 'tz'}, 'sx': {'tx', 'tz'},
        'sy': {'ty'}, 'w': {'t', 'ty'}}
TAIL = ['g_030055F8[i].x = dy;', 'dy >>= 1;', 'f = g_0804F330[dy + 0x10000];',
        'gCurPacket->x[i] = (((dx << 3) * f) >> 16) + 60;', 'gCurPacket->y[i] = (((sy << 3) * f) >> 15) + 80;']
def one(rng):
    pick = {k: rng.randrange(len(v)) for k, v in G.items()}
    # random topological order of groups
    done, out = set(), []
    while len(out) < len(ORDER):
        ready = [k for k in ORDER if k not in done and DEPS.get(k, set()) <= done]
        k = ready[0] if rng.random() < 0.6 else rng.choice(ready)
        done.add(k); out.append(k)
    L = []
    for k in out:
        L += [x.replace(' C', ' ' + C).replace(' S', ' ' + S).replace(' D', ' ' + D).replace(' F', ' ' + F)
              .replace('(C', '(' + C).replace('= C;', '= %s;' % C).replace('= S;', '= %s;' % S) for x in G[k][pick[k]]]
    tag = ''.join('%s%d' % (k[0:2], pick[k]) for k in ORDER) + '_' + ''.join(o[:2] for o in out)
    return 's32 dx, dy, dz, tx, ty, tz, f, sy, t, s, u;\n' + '\n'.join(L + TAIL), tag
if __name__ == '__main__':
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    rng = random.Random(int(sys.argv[3])); seen = set(); n = 0
    while n < int(sys.argv[2]):
        b, tag = one(rng)
        if b in seen: continue
        seen.add(b); n += 1
        (out / ('r%05d.c' % n)).write_text(mk.build(b))

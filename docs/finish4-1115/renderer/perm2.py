#!/usr/bin/env python3
"""Annealing search over projection-loop spellings of 08016DA8 (diagnostic, worker only).
    python3 perm2.py BASE.c OUTDIR SECONDS WORKERS SEED [start-options-json]
Candidates differ only inside `for (i = 0; i < 4; i++) { ... }` of the projection loop.
Each candidate is generated from option toggles plus a priority list of statement keys;
the body is a topological order of the statements under RAW/WAR/WAW dependencies on the
loop's locals and store/load dependencies on memory objects, so every candidate is
behaviour-preserving plain C. Scored with the repository scorer (3*distance + bytes/3).
Writes only C sources and a score log (no ROM bytes)."""
import json, math, os, random, re, sys, time
from multiprocessing import Pool
from pathlib import Path
START, END = 0x08016DA8, 0x08017E68
S = {}
def init():
    sys.path.insert(0, 'tools'); sys.path.insert(0, 'recomp')
    import measure_candidate as mc, draft, reloc, variant_search, llm_match as match
    prog = draft.Program()
    S.update(mc=mc, vs=variant_search, table=reloc.symbols(prog), want=prog.rom[START - match.BASE:END - match.BASE])
def evaluate(src):
    try:
        got, frame = S['mc'].diagnostic_compile(src, 'func_%08X' % START, START, S['table'], 'arm')
    except Exception:
        return None
    dist, diff = S['vs'].score(S['want'], got, START, 'arm')
    return diff, dist, len(got), frame
def scalar(r):
    if r is None: return 10 ** 9
    diff, dist, ln, fr = r
    return 3 * dist + diff / 3 + (0 if ln == END - START else 400) + (0 if str(fr) == '96' else 400)

G = dict(cos='g_03002A18', sin='g_03001B28', df8='g_03000DF8', f58='g_03005F58')
OPTS = {
    'dyip': [0, 1], 'dzip': [0, 1], 'txip': [0, 1, 2], 'tzsp': [0, 1], 'tyip': [0, 1], 'tip': [0, 1],
    'wv': ['w', 'dy'], 'syv': ['sy', 'dz'], 'tpos': ['before', 'after', 'inline'],
    'tzc': [0, 1], 'tyc': [0, 1], 'tc': [0, 1], 'sxc': [0, 1], 'syc': [0, 1], 'wc': [0, 1],
}
def stmts(o):
    """Return list of (key, text) for options o."""
    L = [('dx1', 'dx = gScratch[i].x;'), ('dx2', 'dx -= gCamera.x;')]
    L += [('dy1', 'dy = -gScratch[i].y;'), ('dy2', 'dy -= gCamera.y;')] if o['dyip'] else [('dy1', 'dy = -gScratch[i].y - gCamera.y;')]
    L += [('dz1', 'dz = gScratch[i].z;'), ('dz2', 'dz -= gCamera.z;')] if o['dzip'] else [('dz1', 'dz = gScratch[i].z - gCamera.z;')]
    if o['txip'] == 1: L += [('tx1', 'tx = dx * %(cos)s;' % G), ('tx2', 'tx -= dz * %(sin)s;' % G)]
    elif o['txip'] == 2: L += [('tx1', 'tx = -(dz * %(sin)s);' % G), ('tx2', 'tx += dx * %(cos)s;' % G)]
    else: L += [('tx1', 'tx = dx * %(cos)s - dz * %(sin)s;' % G)]
    a, b = ('dx * %(sin)s' % G, 'dz * %(cos)s' % G)
    if o['tzc']: a, b = b, a
    if o['tzsp']: L += [('tz1', 'tz = %s + %s;' % (a, b)), ('tz2', 'tz >>= 12;')]
    else: L += [('tz1', 'tz = (%s + %s) >> 12;' % (a, b))]
    a, b = ('dy * %(f58)s' % G, 'tz * %(df8)s' % G)
    if o['tyc']: a, b = b, a
    TY = [('ty1', 'ty = %s;' % a), ('ty2', 'ty += %s;' % b)] if o['tyip'] else [('ty1', 'ty = %s + %s;' % (a, b))]
    if o['tpos'] != 'inline':
        T = [('t1', 't = dy * %(df8)s;' % G), ('t2', 't -= tz * %(f58)s;' % G)] if o['tip'] else [('t1', 't = dy * %(df8)s - tz * %(f58)s;' % G)]
    else:
        T = []
    L += (T + TY) if o['tpos'] == 'before' else (TY + T)
    wexpr = 't >> 12' if o['tpos'] != 'inline' else '(dy * %(df8)s - tz * %(f58)s) >> 12' % G
    sx = 'gOffset.x + (tx >> 12)' if not o['sxc'] else '(tx >> 12) + gOffset.x'
    sy = 'gOffset.y + (ty >> 12)' if not o['syc'] else '(ty >> 12) + gOffset.y'
    ww = 'gOffset.z + (%s)' % wexpr if not o['wc'] else '(%s) + gOffset.z' % wexpr
    L += [('SX', 'dx = %s;' % sx), ('SY', '%s = %s;' % (o['syv'], sy)), ('W', '%s = %s;' % (o['wv'], ww))]
    L += [('ST', 'g_030055F8[i].x = %s;' % o['wv']), ('SH', '%s >>= 1;' % o['wv']),
          ('F', 'f = g_0804F330[%s + 0x10000];' % o['wv']),
          ('PX', 'gCurPacket->x[i] = (((dx << 3) * f) >> 16) + 60;'),
          ('PY', 'gCurPacket->y[i] = (((%s << 3) * f) >> 15) + 80;' % o['syv'])]
    return L
ID = re.compile(r'[A-Za-z_]\w*')
LOCAL = {'dx', 'dy', 'dz', 'tx', 'ty', 'tz', 'f', 'sy', 'w', 't', 'i'}
def rw(text):
    m = re.match(r'^(.*?)\s*(>>|<<|\+|-|\*)?=\s*(.*);$', text)
    lhs, op, rhs = m.group(1), m.group(2), m.group(3)
    reads = set(ID.findall(rhs))
    if re.fullmatch(r'\w+', lhs):
        w = {lhs}
        if op: reads.add(lhs)
    else:
        w = {'@' + ID.findall(lhs)[0]}; reads |= set(ID.findall(lhs))
    return w, reads
def order(L, prio):
    keys = [k for k, _ in L]; txt = dict(L)
    info = {k: rw(txt[k]) for k in keys}
    pos = {k: i for i, k in enumerate(keys)}
    dep = {k: set() for k in keys}
    for j in keys:
        for i in keys:
            if pos[i] >= pos[j]: continue
            wi, ri = info[i]; wj, rj = info[j]
            li, lj = ri & LOCAL, rj & LOCAL
            if (wi & lj) or (wi & wj) or (li & wj): dep[j].add(i)
            mi = {x for x in wi if x[0] == '@'}; mj = {x for x in wj if x[0] == '@'}
            oi = {'@' + x for x in ri if x not in LOCAL}; oj = {'@' + x for x in rj if x not in LOCAL}
            if mi & oj or mj & oi or (mi and mj): dep[j].add(i)
    rank = {k: (prio.index(k) if k in prio else 1000 + pos[k]) for k in keys}
    done, out = set(), []
    while len(out) < len(keys):
        ready = [k for k in keys if k not in done and dep[k] <= done]
        k = min(ready, key=lambda x: rank[x]); done.add(k); out.append(k)
    return [txt[k] for k in out]
ALLKEYS = ['dx1', 'dx2', 'dy1', 'dy2', 'dz1', 'dz2', 'tx1', 'tx2', 'tz1', 'tz2', 't1', 't2', 'ty1', 'ty2',
           'SX', 'SY', 'W', 'ST', 'SH', 'F', 'PX', 'PY']
def build(base, o, prio):
    head = '                        for (i = 0; i < 4; i++) {\n'
    s0 = base.index(head) + len(head); s1 = base.index('\n                        }', s0)
    L = stmts(o); body = order(L, prio)
    used = ['dx', 'dy', 'dz', 'tx', 'ty', 'tz', 'f'] + (['sy'] if o['syv'] == 'sy' else []) + \
           (['w'] if o['wv'] == 'w' else []) + (['t'] if o['tpos'] != 'inline' else [])
    ind = ' ' * 28
    return base[:s0] + ind + 's32 ' + ', '.join(used) + ';\n' + '\n'.join(ind + l for l in body) + base[s1:]
def mutate(o, prio, rng):
    o = dict(o); prio = list(prio)
    if rng.random() < 0.5:
        k = rng.choice(list(OPTS)); o[k] = rng.choice(OPTS[k])
    else:
        i = rng.randrange(len(prio)); j = min(len(prio) - 1, max(0, i + rng.choice([-3, -2, -1, 1, 2, 3])))
        prio[i], prio[j] = prio[j], prio[i]
    return o, prio
def main():
    base = Path(sys.argv[1]).read_text(); out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    secs = float(sys.argv[3]); workers = int(sys.argv[4]); rng = random.Random(int(sys.argv[5]))
    o0 = {k: v[0] for k, v in OPTS.items()}
    o0.update({'tpos': 'before'})
    if len(sys.argv) > 6: o0.update(json.loads(sys.argv[6]))
    prio0 = list(ALLKEYS)
    seen = {}
    log = open(out / 'log.txt', 'a')
    with Pool(workers, initializer=init) as pool:
        cur = (o0, prio0); src = build(base, o0, prio0)
        r = pool.apply(evaluate, (src,)); cs = scalar(r); best = (cs, r, src)
        seen[src] = r
        T0 = 6.0; t_end = time.time() + secs; it = 0
        while time.time() < t_end:
            cands = []
            for _ in range(workers * 2):
                o, p = mutate(*cur, rng)
                if rng.random() < 0.3: o, p = mutate(o, p, rng)
                s = build(base, o, p)
                if s in seen: continue
                cands.append((o, p, s))
            if not cands: continue
            res = pool.map(evaluate, [c[2] for c in cands])
            for (o, p, s), r in zip(cands, res):
                seen[s] = r; sc = scalar(r); it += 1
                temp = T0 * max(0.05, (t_end - time.time()) / secs)
                if sc < cs or rng.random() < math.exp(-(sc - cs) / temp):
                    cur = (o, p); cs = sc
                if sc < best[0]:
                    best = (sc, r, s)
                    (out / 'best.c').write_text(s)
                    log.write('%d %.1f %s %s\n' % (it, sc, r, json.dumps(o))); log.flush()
                    if r and r[0] == 0:
                        log.write('EXACT\n'); log.flush(); return
        log.write('done %d evaluated, best %s\n' % (it, best[1])); log.flush()
if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""What-if search (diagnostic only): anneal over projection-loop spellings and statement orders
(finish-4 perm4 option space) while tx, s (sin*dz) and ty are treated as non-local (TXNONLOCAL),
so the objective only sees the sched1-order part of the problem.
    python3 nlanneal.py BASE.c OUTDIR SECONDS WORKERS SEED [start-options-json]
Writes C sources and a score log only. Worker only."""
import json, math, os, random, sys, time, tempfile
from multiprocessing import Pool
from pathlib import Path
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '../../finish4-1115/renderer'))
sys.path.insert(0, 'tools'); sys.path.insert(0, 'recomp')
import perm4, roles
START, END = 0x08016DA8, 0x08017E68
CC1 = os.path.expanduser('~/rendB-cc/gcc_arm/cc1')
S = {}
def init():
    import measure_candidate as mc, draft, reloc, variant_search, llm_match as match
    wd = Path(tempfile.mkdtemp(prefix='nacc-', dir='build'))
    (wd / 'agbcc_arm').symlink_to(CC1)
    match.CC = wd / 'agbcc'
    prog = draft.Program()
    S.update(mc=mc, vs=variant_search, table=reloc.symbols(prog), want=prog.rom[START - match.BASE:END - match.BASE], wd=wd)
def ev(src):
    try:
        p = S['wd'] / ('c%d.c' % os.getpid()); p.write_text(src)
        _, r = roles.info(str(p))
        regs = [x.split('=')[1].split(':')[0] for x in r.split() if x[:2] in ('tx', 's=', 'ty')]
        os.environ['TXNONLOCAL'] = ','.join(x for x in regs if x.isdigit())
        got, frame = S['mc'].diagnostic_compile(src, 'func_%08X' % START, START, S['table'], 'arm')
    except Exception:
        return None
    dist, diff = S['vs'].score(S['want'], got, START, 'arm')
    return diff, dist, len(got), frame
def main():
    base = Path(sys.argv[1]).read_text(); out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    secs = float(sys.argv[3]); W = int(sys.argv[4]); rng = random.Random(int(sys.argv[5]))
    o0 = {k: v[0] for k, v in perm4.OPTS.items()}
    o0.update({'tpos': 'before', 'wv': 'dy', 'dyip': 1, 'txip': 1})
    if len(sys.argv) > 6: o0.update(json.loads(sys.argv[6]))
    fixed = {'wv': 'dy', 'dyip': 1}
    prio0 = list(perm4.ALLKEYS)
    log = open(out / 'log.txt', 'a'); seen = {}
    with Pool(W, initializer=init) as pool:
        cur = (o0, prio0); src = perm4.build(base, o0, prio0)
        r = pool.apply(ev, (src,)); cs = perm4.scalar(r); best = (cs, r, src)
        log.write('start %s\n' % (r,)); log.flush()
        t_end = time.time() + secs; it = 0; T0 = 8.0
        while time.time() < t_end:
            cands = []
            for _ in range(W * 2):
                o, pr = perm4.mutate(*cur, rng)
                if rng.random() < 0.3: o, pr = perm4.mutate(o, pr, rng)
                o.update(fixed)
                s = perm4.build(base, o, pr)
                if s in seen: continue
                seen[s] = 1; cands.append((o, pr, s))
            if not cands: continue
            for (o, pr, s), r in zip(cands, pool.map(ev, [c[2] for c in cands])):
                sc = perm4.scalar(r); it += 1
                temp = T0 * max(0.05, (t_end - time.time()) / secs)
                if sc < cs or rng.random() < math.exp(-(sc - cs) / temp): cur, cs = (o, pr), sc
                if sc < best[0]:
                    best = (sc, r, s); (out / 'best.c').write_text(s)
                    log.write('%d %.1f %s %s\n' % (it, sc, r, json.dumps(o))); log.flush()
                    if r and r[0] == 0:
                        log.write('EXACT-UNDER-NL\n'); log.flush(); return
        log.write('done %d best %s\n' % (it, best[1])); log.flush()
if __name__ == '__main__':
    main()

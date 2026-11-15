#!/usr/bin/env python3
"""What-if search (diagnostic only, never for matching): anneal over forced sched1 orders of the
projection block for ONE fixed source, to learn which order (if any) gives the cartridge's
allocation. Orders are topological w.r.t. the sched1 dependence links of the block.
    python3 oanneal.py cand.c OUTDIR SECONDS WORKERS SEED
Writes only uid orders and scores (no ROM bytes). Worker only."""
import os, re, sys, math, random, time, subprocess, tempfile, json
from multiprocessing import Pool
from pathlib import Path
sys.path.insert(0, 'tools'); sys.path.insert(0, 'recomp')
START, END = 0x08016DA8, 0x08017E68
CC1 = os.path.expanduser('~/rendB-cc/gcc_arm/cc1')
S = {}
def init(src):
    import measure_candidate as mc, draft, reloc, variant_search, llm_match as match
    wd = Path(tempfile.mkdtemp(prefix='oacc-', dir='build'))
    (wd / 'agbcc_arm').symlink_to(CC1)
    match.CC = wd / 'agbcc'
    prog = draft.Program()
    S.update(mc=mc, vs=variant_search, table=reloc.symbols(prog), want=prog.rom[START - match.BASE:END - match.BASE], src=src)
def ev(order):
    os.environ['TXS1ORDER'] = ','.join(map(str, order))
    try:
        got, frame = S['mc'].diagnostic_compile(S['src'], 'func_%08X' % START, START, S['table'], 'arm')
    except Exception:
        return None
    dist, diff = S['vs'].score(S['want'], got, START, 'arm')
    w = S['want']; n = min(len(w), len(got))
    first = next((k for k in range(n) if w[k] != got[k]), n)
    return diff, dist, len(got), frame, first
def scalar(r):
    if r is None: return 10 ** 9
    diff, dist, ln, fr, first = r
    return diff + 3 * dist + (0 if ln == END - START else 2000) + (0 if str(fr) == '96' else 2000)
def block(src):
    import llm_match as match
    with tempfile.TemporaryDirectory(prefix='oa-', dir='build') as td:
        d = Path(td)
        (d / 't.c').write_text(src if 'typedef unsigned char u8;' in src else match.PRELUDE + src)
        match.run([match.ARM + 'gcc', '-E', '-P', '-Isrc', d / 't.c', '-o', d / 't.i'])
        subprocess.run([CC1, '-quiet', 't.i', '-O2', '-mthumb-interwork', '-dl', '-o', 't.s'], cwd=d, capture_output=True, timeout=120)
        t = (d / 't.i.lreg').read_text()
    i = t.index('(const_int 65536)'); s = t.rfind('(code_label', 0, i)
    order, deps = [], {}
    for m in re.finditer(r'(?ms)^\((insn|jump_insn|call_insn) (\d+) (.*?)(?=^\(|\Z)', t[s:]):
        u = int(m.group(2)); order.append(u)
        deps[u] = set(int(x) for x in re.findall(r'\(insn_list(?::REG_DEP_\w+)? (\d+) ', m.group(3)))
        if m.group(1) == 'jump_insn': break
    for u in order: deps[u] &= set(order)
    return order, deps
def valid(o, deps):
    pos = {u: k for k, u in enumerate(o)}
    return all(pos[d] < pos[u] for u in o for d in deps[u])
def mutate(o, deps, rng):
    o = list(o)
    for _ in range(50):
        k = rng.randrange(len(o) - 1); u = o[k]
        lo = max([o.index(d) for d in deps[u]] + [-1]) + 1
        succ = [j for j, v in enumerate(o) if u in deps[v]]
        hi = min(succ + [len(o) - 1])
        if hi - lo < 1: continue
        o2 = o[:k] + o[k + 1:]
        j = rng.randint(lo, hi - 1)
        o2.insert(j, u)
        if o2 != o and valid(o2, deps): return o2
    return o
def main():
    import sys as _s
    sys.path.insert(0, 'tools'); sys.path.insert(0, 'recomp')
    src = Path(sys.argv[1]).read_text(); out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    secs = float(sys.argv[3]); W = int(sys.argv[4]); rng = random.Random(int(sys.argv[5]))
    order, deps = block(src)
    log = open(out / 'log.txt', 'a')
    with Pool(W, initializer=init, initargs=(src,)) as pool:
        cur = order; r = pool.apply(ev, (cur,)); cs = scalar(r); best = (cs, r, cur)
        log.write('start %s %s\n' % (r, ' '.join(map(str, cur)))); log.flush()
        seen = {tuple(cur)}; t_end = time.time() + secs; it = 0; T0 = 30.0
        while time.time() < t_end:
            cands = []
            for _ in range(W * 2):
                o = mutate(cur, deps, rng)
                if rng.random() < 0.4: o = mutate(o, deps, rng)
                if tuple(o) not in seen: seen.add(tuple(o)); cands.append(o)
            if not cands: continue
            for o, r in zip(cands, pool.map(ev, cands)):
                sc = scalar(r); it += 1
                temp = T0 * max(0.03, (t_end - time.time()) / secs)
                if sc < cs or rng.random() < math.exp(-(sc - cs) / temp): cur, cs = o, sc
                if sc < best[0]:
                    best = (sc, r, o)
                    log.write('%d %s %s\n' % (it, r, ' '.join(map(str, o)))); log.flush()
                    if r and r[0] == 0:
                        log.write('EXACT-ORDER\n'); log.flush(); return
        log.write('done %d best %s\n' % (it, best[1])); log.flush()
if __name__ == '__main__':
    main()

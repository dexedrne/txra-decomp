#!/usr/bin/env python3
"""What-if search over the sched1 order of the projection-loop block (diagnostic, worker only,
never for matching). Uses the private cc1's TXORDER hook to emit the block in a given order and
hill-climbs single-insn moves on the differing bytes of the whole function.
    python3 ordsearch.py CAND.c ORDER(comma uids) [WORKERS] [RADIUS]
Prints each improvement and the final order. Reads no ROM bytes except through the scorer."""
import os, re, sys, subprocess, tempfile
from multiprocessing import Pool
from pathlib import Path
START, END = 0x08016DA8, 0x08017E68
CC = os.path.expanduser('~/txra-rendA-cc/gcc_arm/cc1')
S = {}

def init(src):
    sys.path.insert(0, 'tools'); sys.path.insert(0, 'recomp')
    import draft, reloc, variant_search, llm_match as match
    prog = draft.Program()
    S.update(reloc=reloc, vs=variant_search, match=match, table=reloc.symbols(prog),
             want=prog.rom[START - match.BASE:END - match.BASE])
    td = tempfile.mkdtemp(prefix='os-', dir='build')
    code = src if 'typedef unsigned char u8;' in src else match.PRELUDE + src
    Path(td, 'trial.c').write_text(code)
    match.run([match.ARM + 'gcc', '-E', '-P', '-Isrc', Path(td, 'trial.c'), '-o', Path(td, 'trial.i')])
    S['td'] = td

def compile_order(order, nl=()):
    match, reloc = S['match'], S['reloc']
    td = Path(tempfile.mkdtemp(prefix='o-', dir=S['td']))
    env = dict(os.environ); env['TXORDER'] = ','.join(map(str, order)); env.pop('TXDBG', None)
    if nl: env['TXNONLOCAL'] = ','.join(map(str, sorted(nl)))
    r = subprocess.run([CC, '-quiet', str(Path(S['td'], 'trial.i')), '-O2', '-mthumb-interwork', '-o', str(td / 'trial.s')],
                       capture_output=True, text=True, env=env, timeout=120)
    if 'TXORDER violation' in r.stderr or r.returncode != 0:
        subprocess.run(['rm', '-rf', str(td)]); return None
    name = 'func_%08X' % START
    asm = (td / 'trial.s').read_text()
    b = re.search(r'(?m)^' + re.escape(name) + ':', asm).start(); tail = asm[b:]
    e = re.search(r'\n\s*\.size\s+' + re.escape(name) + r',[^\n]*', tail).end()
    (td / 'one.s').write_text('.syntax divided\n.text\n.arm\n' + tail[:e] + '\n')
    match.run([match.ARM + 'as', '-mcpu=arm7tdmi', td / 'one.s', '-o', td / 'one.o'])
    match.run([match.ARM + 'objcopy', '-O', 'binary', '-j', '.text', td / 'one.o', td / 'one.bin'])
    got = reloc.function_bytes(td / 'one.o', (td / 'one.bin').read_bytes(), name, match.ARM + 'objdump')
    ent = reloc.parse(match.run([match.ARM + 'objdump', '-r', td / 'one.o']).stdout)
    got = reloc.relocate(got, ent, START, S['table']) if ent else got
    subprocess.run(['rm', '-rf', str(td)])
    dist, diff = S['vs'].score(S['want'], got, START, 'arm')
    pen = 0 if len(got) == END - START else 1000
    return (diff + pen, dist)

def ev(state):
    order, nl = state
    try:
        return state, compile_order(order, nl)
    except Exception as ex:
        return state, None

CONSTR = [tuple(int(x) for x in p.split('<')) for p in os.environ.get('OS_CONSTR', '').split(',') if p]
def ok(o):
    pos = {u: k for k, u in enumerate(o)}
    return all(pos[a] < pos[b] for a, b in CONSTR if a in pos and b in pos)

def neighbours(order, radius):
    body = order[:-1]   # keep the jump last
    out = []
    n = len(body)
    for i in range(n):
        for j in range(max(0, i - radius), min(n, i + radius + 1)):
            if j == i: continue
            b = body[:]; x = b.pop(i); b.insert(j, x)
            if ok(b): out.append(b + order[-1:])
    return out

def _main_climb():
    # ordsearch.py CAND.c ORDER WORKERS RADIUS [NONLOCAL_START] [TOGGLE_CANDIDATES]
    src = Path(sys.argv[1]).read_text()
    order = [int(x) for x in sys.argv[2].split(',')]
    W = int(sys.argv[3]) if len(sys.argv) > 3 else 6
    R = int(sys.argv[4]) if len(sys.argv) > 4 else 6
    nl = frozenset(int(x) for x in sys.argv[5].split(',') if x) if len(sys.argv) > 5 else frozenset()
    tog = [int(x) for x in sys.argv[6].split(',') if x] if len(sys.argv) > 6 else []
    with Pool(W, initializer=init, initargs=(src,)) as pool:
        best = pool.apply(ev, ((order, nl),))[1]
        print('start', best, sorted(nl), flush=True)
        while True:
            cand = [(o, nl) for o in neighbours(order, R)] + [(order, nl ^ {p}) for p in tog]
            res = [r for r in pool.map(ev, cand, chunksize=4) if r[1] is not None]
            res.sort(key=lambda r: r[1])
            if not res or res[0][1] >= best:
                break
            (order, nl), best = res[0]
            print('improved', best, 'NL=' + ','.join(map(str, sorted(nl))), ','.join(map(str, order)), flush=True)
            if best[0] == 0: break
    print('final', best, 'NL=' + ','.join(map(str, sorted(nl))), ','.join(map(str, order)))

def ils(src, order, W, R, nl, seconds, seed=1):
    """Iterated local search: hill-climb, then perturb with 3 random moves and climb again."""
    import random, time
    rnd = random.Random(seed)
    t_end = time.time() + seconds
    with Pool(W, initializer=init, initargs=(src,)) as pool:
        def climb(o, b):
            while True:
                cand = [(x, nl) for x in neighbours(o, R)]
                res = [r for r in pool.map(ev, cand, chunksize=4) if r[1] is not None]
                res.sort(key=lambda r: r[1])
                if not res or res[0][1] >= b: return o, b
                (o, _), b = res[0]
                if b[0] == 0: return o, b
        cur = pool.apply(ev, ((order, nl),))[1]
        best_o, best = climb(order, cur)
        print('climb', best, ','.join(map(str, best_o)), flush=True)
        while time.time() < t_end and best[0] != 0:
            o = best_o
            for _ in range(3):
                nb = neighbours(o, R)
                if nb: o = rnd.choice(nb)
            r = pool.apply(ev, ((o, nl),))[1]
            if r is None: continue
            o2, b2 = climb(o, r)
            if b2 < best:
                best_o, best = o2, b2
                print('ils', best, ','.join(map(str, best_o)), flush=True)
    print('final', best, ','.join(map(str, best_o)))

if __name__ == '__main__':
    if os.environ.get('OS_ILS'):
        src = Path(sys.argv[1]).read_text()
        order = [int(x) for x in sys.argv[2].split(',')]
        nl = frozenset(int(x) for x in sys.argv[5].split(',') if x) if len(sys.argv) > 5 else frozenset()
        ils(src, order, int(sys.argv[3]), int(sys.argv[4]), nl, int(os.environ['OS_ILS']))
    else:
        _main_climb()

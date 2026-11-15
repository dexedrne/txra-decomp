#!/usr/bin/env python3
"""Choice-point search over a C template (run on a worker; copied from the 11/15 wsearch.py,
with /*SUB:NAME=value*/ substitution for linked alternatives).

Template markers are «name@option0@option1@...»; every marker with the same name takes the
same option.  Neighbourhood = all single changes plus random pairs/triples; scored by
batch.one() as register-only rows + 2 * shape rows + differing bytes / 50.  The best choice
and its rendered source are written next to the state file; a log records each improvement.
usage: wsearch.py <template> <state.json> <minutes> [seed]"""
import sys, json, time, random, os, re
sys.path.insert(0, "docs/near-misses/finish2-1115-sound")
from multiprocessing import Pool
import batch
from pathlib import Path
PAT = re.compile(r'«(\w+)((?:@[^«»@]*)*)»', re.S)
def parse(tpl):
    pts = {}
    for m in PAT.finditer(tpl):
        pts.setdefault(m.group(1), [o.replace('\\n', '\n') for o in m.group(2).split('@')[1:]])
    return pts
def render0(tpl, ch):
    return PAT.sub(lambda m: m.group(2).split('@')[1:][ch.get(m.group(1), 0)].replace('\\n', '\n'), tpl)
def score(r):
    if 'error' in r: return 10**9
    return r['reg'] + 2 * r['shape'] + r['diff'] / 50.0
def render(tpl, ch):
    s = render0(tpl, ch)
    for k, v in re.findall(r'/\*SUB:(\w+)=(\w+)\*/', s):
        s = s.replace(k, v)
    return s
tpl = Path(sys.argv[1]).read_text(); sp = Path(sys.argv[2]); limit = time.time() + 60 * float(sys.argv[3])
random.seed(int(sys.argv[4]) if len(sys.argv) > 4 else 1)
pts = parse(tpl)
st = json.loads(sp.read_text()) if sp.exists() else {}
cur = {k: v for k, v in st.get('choice', {}).items() if k in pts}
d = Path('build/ws4'); d.mkdir(parents=True, exist_ok=True)
seen = {}
def key(c): return tuple(sorted((k, v) for k, v in c.items() if v))
def evaluate(cands, pool):
    todo = [c for c in cands if key(c) not in seen]
    files = []
    for i, c in enumerate(todo):
        f = d / ('w%05d_%d.c' % (len(seen) + i, os.getpid())); f.write_text(render(tpl, c)); files.append(str(f))
    for c, r in zip(todo, pool.map(batch.one, files)):
        seen[key(c)] = r
    for f in files: os.unlink(f)
    return [seen[key(c)] for c in cands]
log = open(str(sp) + '.log', 'a')
with Pool(int(os.environ.get('JOBS', '6'))) as pool:
    best_r = evaluate([cur], pool)[0]; best = score(best_r)
    print('start', best, best_r, file=log, flush=True)
    names = list(pts)
    while time.time() < limit:
        # neighbourhood: all single changes + some random pairs/triples
        cands = []
        for n in names:
            for o in range(len(pts[n])):
                if o != cur.get(n, 0):
                    c = dict(cur); c[n] = o; cands.append(c)
        for _ in range(24):
            c = dict(cur)
            for n in random.sample(names, random.choice([2, 2, 3])):
                c[n] = random.randrange(len(pts[n]))
            cands.append(c)
        rs = evaluate(cands, pool)
        sc = sorted(zip([score(r) for r in rs], range(len(rs))))
        if sc[0][0] < best:
            cur = cands[sc[0][1]]; best = sc[0][0]; best_r = rs[sc[0][1]]
            print(time.strftime('%H:%M:%S'), 'improve', best, best_r, {k: v for k, v in cur.items() if v}, file=log, flush=True)
            sp.write_text(json.dumps(dict(choice=cur, result=best_r), indent=1))
            Path(str(sp).replace('.json', '.c')).write_text(render(tpl, cur))
        else:
            # random restart-ish kick: accept a random pair that is within 1% to escape plateaus
            near = [i for s, i in sc if s <= best * 1.003 and cands[i] != cur]
            if near:
                cur = cands[random.choice(near)]
                print(time.strftime('%H:%M:%S'), 'plateau move', file=log, flush=True)
            else:
                print(time.strftime('%H:%M:%S'), 'stuck', best, file=log, flush=True)
                # big kick
                c = dict(cur)
                for n in random.sample(names, 4): c[n] = random.randrange(len(pts[n]))
                cur = c
print('done', best, file=log, flush=True)

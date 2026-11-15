#!/usr/bin/env python3
"""Enumerate choice-point combinations of a template (worker only) and rank them.
Markers «name@opt0@opt1...» as in the 11/15 wsearch.py.  usage: choices.py <tpl> [max] [seed]
Prints the best combinations (score = reg rows + 2*shape rows + differing bytes/50)."""
import sys, os, re, itertools, random, json
sys.path.insert(0, 'docs/near-misses/finish2-1115-sound')
from multiprocessing import Pool
from pathlib import Path
import batch
PAT = re.compile(r'«(\w+)((?:@[^«»@]*)*)»', re.S)
tpl = Path(sys.argv[1]).read_text()
mx = int(sys.argv[2]) if len(sys.argv) > 2 else 400
random.seed(int(sys.argv[3]) if len(sys.argv) > 3 else 1)
pts = {}
for m in PAT.finditer(tpl):
    pts.setdefault(m.group(1), len(m.group(2).split('@')[1:]))
names = sorted(pts)
def render(ch):
    s = PAT.sub(lambda m: m.group(2).split('@')[1:][ch[m.group(1)]].replace('\\n', '\n'), tpl)
    for k, v in re.findall(r'/\*SUB:(\w+)=(\w+)\*/', s):
        s = s.replace(k, v)
    return s
allc = list(itertools.product(*[range(pts[n]) for n in names]))
if len(allc) > mx:
    allc = [tuple([0] * len(names))] + random.sample(allc, mx - 1)
d = Path('build/en'); d.mkdir(parents=True, exist_ok=True)
files = []
for i, c in enumerate(allc):
    f = d / ('e%05d.c' % i); f.write_text(render(dict(zip(names, c)))); files.append(str(f))
def score(r):
    return 10**9 if 'error' in r else r['reg'] + 2 * r['shape'] + r['diff'] / 50.0
with Pool(int(os.environ.get('JOBS', '6'))) as p:
    rs = p.map(batch.one, files)
res = sorted(zip([score(r) for r in rs], range(len(rs))))
print('combos', len(allc), 'names', names)
for s, i in res[:int(os.environ.get('TOP', '15'))]:
    r = rs[i]
    print("%8.2f %s %s" % (s, dict(zip(names, allc[i])), r.get("error") or {k: r.get(k) for k in ("emit", "frame", "diff", "same", "reg", "shape", "rs", "exact")}))
base = rs[0]
print('base', score(base), {k: base.get(k) for k in ('emit', 'frame', 'diff', 'same', 'reg', 'shape', 'rs')})
for f in files: os.unlink(f)
json.dump([[s, dict(zip(names, allc[i]))] for s, i in res[:50]], open(str(d / 'last.json'), 'w'))

#!/usr/bin/env python3
"""Generate dependency-respecting orders of the projection-loop statements of a base candidate
(worker only).  python3 pperm.py base.c outdir [limit]
Statements are the simple assignments inside `for (i = 0; i < 4; i++) {` (the projection loop)."""
import re, sys
from pathlib import Path
base = Path(sys.argv[1]).read_text(); out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
limit = int(sys.argv[3]) if len(sys.argv) > 3 else 5000
lines = base.split('\n')
s = next(i for i, l in enumerate(lines) if l.strip() == 'for (i = 0; i < 4; i++) {')
decl = s + 1
assert lines[decl].strip().startswith('s32 ')
body = []
k = decl + 1
while lines[k].strip() != '}':
    body.append(lines[k]); k += 1
end = k
ind = re.match(r'\s*', body[0]).group(0)
stm = [b.strip() for b in body]
IDENT = re.compile(r'[A-Za-z_]\w*')
info = []
for st in stm:
    m = re.match(r'^(.*?)\s*=\s*(.*);$', st)
    l, r = m.group(1), m.group(2)
    w = l if re.fullmatch(r'\w+', l) else None
    mem_w = None if w else l
    reads = set(IDENT.findall(r)) | (set(IDENT.findall(l)) if not w else set())
    info.append((w, mem_w, reads, st))
n = len(stm)
dep = [set() for _ in range(n)]
for j in range(n):
    for i in range(j):
        wi, mi, ri, si = info[i]; wj, mj, rj, sj = info[j]
        if wi and (wi in rj or wi == wj): dep[j].add(i)
        if wj and wj in ri: dep[j].add(i)
        if mi and mj: dep[j].add(i)
        elif mi and ('gCurPacket' in sj or 'g_' in sj): dep[j].add(i)
        elif mj and ('gCurPacket' in si or 'g_' in si): dep[j].add(i)
orders = []
def rec(done, seq):
    if len(orders) >= limit: return
    if len(seq) == n:
        orders.append(seq[:]); return
    for x in range(n):
        if x not in done and dep[x] <= done:
            done.add(x); seq.append(x); rec(done, seq); seq.pop(); done.discard(x)
rec(set(), [])
print(n, 'statements', len(orders), 'orders')
for idx, o in enumerate(orders):
    new = lines[:decl + 1] + [ind + stm[x] for x in o] + lines[end:]
    (out / ('p%05d_%s.c' % (idx, '-'.join(map(str, o))))).write_text('\n'.join(new))

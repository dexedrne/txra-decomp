#!/usr/bin/env python3
"""Enumerate dependency-respecting statement orders of the projection loop body (diagnostic,
worker only).
    python3 porder.py BASE.c OUTDIR [--limit N] [--sample N] [--keep-stores]
The loop is the `for (i = 0; i < 4; i++) {` block whose first line declares its locals.
Each body line must be one simple statement `lhs [op]= rhs;`. Dependencies kept: RAW, WAR
and WAW on the loop's locals, and every memory store against every statement that reads the
same object (by first identifier) or another store (with --keep-stores). Distinct globals are
distinct objects, so reordering them preserves behaviour. One C file per order."""
import random, re, sys
from pathlib import Path
args = sys.argv[1:]
base = Path(args[0]).read_text(); out = Path(args[1]); out.mkdir(parents=True, exist_ok=True)
limit = int(args[args.index('--limit') + 1]) if '--limit' in args else 10 ** 9
sample = int(args[args.index('--sample') + 1]) if '--sample' in args else 0
keep_stores = '--keep-stores' in args
lines = base.split('\n')
s = next(i for i, l in enumerate(lines) if l.strip() == 'for (i = 0; i < 4; i++) {')
decl = s + 1
assert lines[decl].strip().startswith('s32 ')
local = set(re.findall(r'[A-Za-z_]\w*', lines[decl].strip()[4:])) | {'i'}
k = decl + 1; body = []
while lines[k].strip() != '}':
    body.append(lines[k]); k += 1
end = k
ind = re.match(r'\s*', body[0]).group(0)
ID = re.compile(r'[A-Za-z_]\w*')
S = []
for b in body:
    st = b.strip()
    m = re.match(r'^(.*?)\s*(>>|<<|\+|-|\*|&|\|)?=\s*(.*);$', st)
    assert m, st
    lhs, op, rhs = m.group(1), m.group(2), m.group(3)
    reads = set(ID.findall(rhs))
    if re.fullmatch(r'\w+', lhs):
        w = {lhs}
        if op: reads.add(lhs)
    else:
        w = {'@' + ID.findall(lhs)[0]}
        reads |= set(ID.findall(lhs))
    S.append((st, w, reads))
n = len(S)
def objs(r): return {'@' + x for x in r if x not in local}
dep = [set() for _ in range(n)]
for j in range(n):
    for i in range(j):
        wi, ri = S[i][1], S[i][2]; wj, rj = S[j][1], S[j][2]
        li, lj = ri & local, rj & local
        if (wi & lj) or (wi & wj) or (li & wj): dep[j].add(i)
        mi = {x for x in wi if x.startswith('@')}; mj = {x for x in wj if x.startswith('@')}
        if mi & objs(rj) or mj & objs(ri): dep[j].add(i)
        if keep_stores and mi and mj: dep[j].add(i)
orders = []
def rec(done, seq):
    if len(orders) >= limit: return
    if len(seq) == n: orders.append(seq[:]); return
    for x in range(n):
        if x not in done and dep[x] <= done:
            done.add(x); seq.append(x); rec(done, seq); seq.pop(); done.discard(x)
rec(set(), [])
print(n, 'statements', len(orders), 'orders', file=sys.stderr)
if sample and sample < len(orders):
    random.seed(1); orders = random.sample(orders, sample)
for o in orders:
    new = lines[:decl + 1] + [ind + S[x][0] for x in o] + lines[end:]
    (out / ('o_%s.c' % '-'.join('%x' % x for x in o))).write_text('\n'.join(new))

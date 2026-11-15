#!/usr/bin/env python3
"""Allocation summary of the projection block from a trace.sh output dir (our own source only; worker).
    python3 qa.py TRACEDIR"""
import re, sys
from pathlib import Path
d = Path(sys.argv[1])
lreg = (d / 't.i.lreg').read_text(); L = (d / 'trace.txt').read_text().splitlines()
greg = (d / 't.i.greg').read_text()
defs = {}; order = []
i = lreg.index('(const_int 65536)'); s = lreg.rfind('(code_label', 0, i); e = lreg.find('(code_label', i)
blkuids = set()
for m in re.finditer(r'(?ms)^\((insn|jump_insn) (\d+) \d+ \d+ (.*?)(?=^\(|\Z)', lreg):
    b = ' '.join(m.group(3).split()); uid = int(m.group(2))
    if s <= m.start() < e: blkuids.add(uid); order.append(uid)
    mm = re.match(r'\(set \(reg(?:/v)?:SI (\d+)\) (.*)', b)
    if mm:
        rhs = re.sub(r'\(expr_list.*$|\(insn_list.*$|\d+ \{[^}]*\}.*$', '', mm.group(2)).replace('/v', '').replace(':SI', '')
        defs.setdefault(int(mm.group(1)), []).append((uid, ' '.join(rhs.split())[:70]))
disp = {int(a): int(b) for a, b in re.findall(r'(\d+) in (\d+)', greg.split(';; Register dispositions:')[1].split('\n\n')[0])}
pos = {u: k for k, u in enumerate(order)}
# LQ block id: the one containing a reg set in the block
lqs = [l for l in L if l.startswith('LQ ')]
blk = None
for l in lqs:
    f = dict(x.split('=', 1) for x in l.split()[1:] if '=' in x)
    for g in f['regs'].strip(',').split(','):
        if g and any(u in blkuids for u, _ in defs.get(int(g), [])): blk = f['b']
    if blk: break
print('local qtys (block %s):' % blk)
for l in lqs:
    f = dict(x.split('=', 1) for x in l.split()[1:] if '=' in x)
    if f['b'] != blk: continue
    regs = [int(x) for x in f['regs'].strip(',').split(',') if x]
    desc = ' | '.join('%d=%s' % (g, defs.get(g, [('?', '?')])[0][1]) for g in regs[:3])
    print(' ord=%-2s pri=%-5s [%3s,%3s) refs=%-3s sg=%s/%s -> %-3s %s' % (f['ord'], f['pri'], f['birth'], f['death'], f['refs'], f['sugg'], f['csugg'], f['phys'], desc))
print('global pseudos set in block:')
gl = {}
for l in L:
    if l.startswith('GF reg='):
        f = dict(x.split('=', 1) for x in l.split() if '=' in x)
        gl.setdefault(int(f['reg']), f)
for g in sorted(gl):
    if any(u in blkuids for u, _ in defs.get(g, [])):
        f = gl[g]
        print(' %d -> %s (best=%s refs=%s len=%s) %s' % (g, disp.get(g), f['best'], f['refs'], f['len'], '; '.join(x[1] for x in defs[g])[:120]))

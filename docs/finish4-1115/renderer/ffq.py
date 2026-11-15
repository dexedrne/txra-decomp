#!/usr/bin/env python3
"""find_free_reg masks joined with qty members for the projection block (private cc1, worker only).
    python3 ffq.py cand.c"""
import os, re, subprocess, sys, tempfile
from pathlib import Path
sys.path.insert(0, 'tools'); sys.path.insert(0, 'recomp')
import llm_match as match
src = Path(sys.argv[1]).read_text()
with tempfile.TemporaryDirectory(prefix='ffq-', dir='build') as td:
    d = Path(td)
    (d / 't.c').write_text(src if 'typedef unsigned char u8;' in src else match.PRELUDE + src)
    match.run([match.ARM + 'gcc', '-E', '-P', '-Isrc', d / 't.c', '-o', d / 't.i'])
    r = subprocess.run([os.path.expanduser('~/txra-renderer-cc/gcc_arm/cc1'), '-quiet', 't.i', '-O2', '-mthumb-interwork', '-dl', '-o', 't.s'],
                       cwd=d, capture_output=True, text=True, env=dict(os.environ, TXDBG='LFG'), timeout=120)
    lreg = (d / 't.i.lreg').read_text()
defs = {}
for m in re.finditer(r'(?ms)^\((insn|jump_insn) (\d+) \d+ \d+ (.*?)(?=^\(|\Z)', lreg):
    b = ' '.join(m.group(3).split())
    mm = re.match(r'\(set \(reg(?:/v)?:SI (\d+)\) (.*)', b)
    if mm and int(mm.group(1)) not in defs:
        defs[int(mm.group(1))] = re.sub(r'\(expr_list.*$|\(insn_list.*$|\d+ \{[^}]*\}.*$', '', mm.group(2))[:60]
L = r.stderr.splitlines()
# projection block = the LQ block containing a reg defined by (const_int 65536) plus
target = None
for l in L:
    if l.startswith('LQ '):
        f = dict(x.split('=', 1) for x in l.split()[1:] if '=' in x)
        for g in f['regs'].strip(',').split(','):
            if g and '65536' in defs.get(int(g), ''): target = f['b']
blk = [i for i, l in enumerate(L) if l.startswith('LQ b=%s ' % target)]
lq = {}
for i in blk:
    f = dict(x.split('=', 1) for x in L[i].split()[1:] if '=' in x); lq[int(f['q'])] = f
j = blk[0] - 1; ff = []
while j >= 0 and not L[j].startswith('LQ '):
    if L[j].startswith('FF '): ff.append(L[j])
    j -= 1
for l in reversed(ff):
    q, b, dd, u, s, rr = re.match(r'FF q=(\d+) born=(\d+) dead=(\d+) used=([0-9a-f]+) sugg=(\d) -> (\d+)', l).groups()
    u = int(u, 16); regs = [k for k in range(15) if u >> k & 1 and k not in (11, 13)]
    mem = [int(x) for x in lq[int(q)]['regs'].strip(',').split(',') if x]
    print('ord=%-2s [%3s,%3s) -> r%-2s used=%-18s %s' % (lq[int(q)]['ord'], b, dd, rr, ','.join(map(str, regs)),
          ' | '.join('%d:%s' % (g, defs.get(g, '?')) for g in mem[:2])))
for l in L:
    if l.startswith('GF reg=') and ' best=' in l:
        g = int(l.split()[1].split('=')[1])
        if g in defs and ('gScratch' in defs[g] or g in (724, 725, 726)):
            print(l.split(' used1')[0], defs.get(g))

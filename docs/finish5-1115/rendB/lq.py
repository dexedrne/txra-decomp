#!/usr/bin/env python3
"""Local-alloc qtys of one block with the defining insn of each reg (private tracing cc1; worker only).
    python3 lq.py cand.c BLOCK"""
import os, re, sys, subprocess, tempfile
from pathlib import Path
sys.path.insert(0, 'tools'); sys.path.insert(0, 'recomp')
import llm_match as match
src = Path(sys.argv[1]).read_text(); blk = sys.argv[2]
with tempfile.TemporaryDirectory(prefix='lq-', dir='build') as td:
    d = Path(td)
    (d / 't.c').write_text(src if 'typedef unsigned char u8;' in src else match.PRELUDE + src)
    match.run([match.ARM + 'gcc', '-E', '-P', '-Isrc', d / 't.c', '-o', d / 't.i'])
    cc = os.path.expanduser('~/rendB-cc/gcc_arm/cc1')
    r = subprocess.run([cc, '-quiet', 't.i', '-O2', '-mthumb-interwork', '-dl', '-dg', '-o', 't.s'], cwd=d,
                       capture_output=True, text=True, env=dict(os.environ, TXDBG='LG'), timeout=120)
    lreg = (d / 't.i.lreg').read_text(); greg = (d / 't.i.greg').read_text()
defs = {}
for m in re.finditer(r'(?ms)^\((insn|jump_insn) (\d+) \d+ \d+ (.*?)(?=^\(|\Z)', lreg):
    b = ' '.join(m.group(3).split())
    mm = re.match(r'\(set \(reg(?:/v)?:SI (\d+)\) (.*)', b)
    if mm and int(mm.group(1)) not in defs:
        rhs = re.sub(r'\(expr_list.*$|\(insn_list.*$|\d+ \{[^}]*\}.*$', '', mm.group(2))
        defs[int(mm.group(1))] = (int(m.group(2)), rhs[:90])
disp = {int(a): int(b) for a, b in re.findall(r'(\d+) in (\d+)', greg.split(';; Register dispositions:')[1].split('\n\n')[0])}
for l in r.stderr.splitlines():
    if l.startswith('LQ b=%s ' % blk):
        f = dict(x.split('=', 1) for x in l.split()[1:] if '=' in x)
        regs = [int(x) for x in f['regs'].strip(',').split(',') if x]
        desc = '; '.join('%d:%s' % (g, defs.get(g, ('?', '?'))[1]) for g in regs[:2])
        print('ord=%-2s pri=%-6s b=%-3s d=%-3s refs=%-3s phys=%-3s %s' % (f['ord'], f['pri'], f['birth'], f['death'], f['refs'], f['phys'], desc))
glob = [l for l in r.stderr.splitlines() if l.startswith('GF ')]
print('globals with best in 0..3/12/14 (first 12):')
for l in glob[:12]: print(' ', l.split(' used1')[0])

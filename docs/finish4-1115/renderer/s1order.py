#!/usr/bin/env python3
"""Print sched1 order (and sched log) of the block containing the first (mult ... g_03001B28-load) for a candidate.
    python3 s1order.py cand.c  (worker only, official agbcc_arm with -dS)"""
import re, sys, subprocess, tempfile
from pathlib import Path
sys.path.insert(0, 'tools'); sys.path.insert(0, 'recomp')
import llm_match as match
src = Path(sys.argv[1]).read_text()
with tempfile.TemporaryDirectory(prefix='s1-', dir='build') as td:
    d = Path(td)
    (d / 't.c').write_text(src if 'typedef unsigned char u8;' in src else match.PRELUDE + src)
    match.run([match.ARM + 'gcc', '-E', '-P', '-Isrc', d / 't.c', '-o', d / 't.i'])
    subprocess.run([str(match.CC.with_name('agbcc_arm')), 't.i', '-O2', '-mthumb-interwork', '-dS', '-o', 't.s'],
                   cwd=d, capture_output=True, timeout=120)
    t = (d / 't.i.sched').read_text()
m = re.search(r'\(symbol_ref:SI \("g_03005F58"\)\)', t)
# find the loop block: first insn using ashiftrt 12 near the F58 address set... use block containing 'const_int 65536'
i = t.index('(const_int 65536)')
s = t.rfind('(code_label', 0, i); e = t.find('(jump_insn', i); e = t.find('\n\n', e)
names = {}
for mm in re.finditer(r'(?ms)^\((insn|jump_insn) (\d+) \d+ \d+ (.*?)(?=^\(|\Z)', t[s:e]):
    b = ' '.join(mm.group(3).split()); b = re.sub(r'\(expr_list:REG_\w+ .*$', '', b); b = re.sub(r' \(insn_list.*$', '', b)
    b = re.sub(r'\d+ \{[^}]*\}.*$', '', b)
    print('%s %s' % (mm.group(2), b[:110]))

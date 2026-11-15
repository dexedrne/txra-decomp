#!/usr/bin/env python3
"""Natural sched1 order of the projection block, one line per insn (our own source; worker only).
    python3 nat.py cand.c"""
import os, re, sys
sys.path.insert(0, os.path.dirname(__file__)); sys.path.insert(0, 'tools'); sys.path.insert(0, 'recomp')
import subprocess, tempfile
from pathlib import Path
import llm_match as match
CC1 = os.path.expanduser('~/rendB-cc/gcc_arm/cc1')
src = Path(sys.argv[1]).read_text()
with tempfile.TemporaryDirectory(prefix='nat-', dir='build') as td:
    d = Path(td)
    (d / 't.c').write_text(src if 'typedef unsigned char u8;' in src else match.PRELUDE + src)
    match.run([match.ARM + 'gcc', '-E', '-P', '-Isrc', d / 't.c', '-o', d / 't.i'])
    subprocess.run([CC1, '-quiet', 't.i', '-O2', '-mthumb-interwork', '-dl', '-o', 't.s'], cwd=d, capture_output=True, timeout=120)
    t = (d / 't.i.lreg').read_text()
i = t.index('(const_int 65536)'); s = t.rfind('(code_label', 0, i)
for m in re.finditer(r'(?ms)^\((insn|jump_insn|call_insn) (\d+) \d+ \d+ (.*?)(?=^\(|\Z)', t[s:]):
    b = ' '.join(m.group(3).split())
    b = re.sub(r'\(expr_list.*$|\(insn_list.*$', '', b); b = re.sub(r' \d+ \{[^}]*\}.*$', '', b)
    b = b.replace('/v', '').replace(':SI', '').replace('/s', '').replace('/f', '').replace('/u', '')
    deps = re.findall(r'\(insn_list(?::REG_DEP_(\w+))? (\d+) ', m.group(3))
    print('%5s %-90s %s' % (m.group(2), b[:90], ' '.join(('%s%s' % (k[0].lower() if k else '', u)) for k, u in deps)))
    if m.group(1) == 'jump_insn': break

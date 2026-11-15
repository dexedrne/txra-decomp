#!/usr/bin/env python3
"""Print the sched1 log of the block containing (const_int 65536) for a candidate (worker only)."""
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
i = t.index('(const_int 65536)')
s = t.rfind('(code_label', 0, i)
first = re.search(r'\(insn (\d+) ', t[s:]).group(1)
logs = t.split(';; ready list initially:')
for L in logs:
    if (';; insn[%s]' % first.rjust(4)) in L or (';; insn[%s]' % first) in L:
        print(L[:12000]); break

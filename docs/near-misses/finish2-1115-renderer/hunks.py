#!/usr/bin/env python3
"""hunks.py REF.c CAND.c OUTDIR : write CAND with each single hunk reverted to REF (text only)."""
import difflib, sys
from pathlib import Path
ref = Path(sys.argv[1]).read_text().split('\n')
cur = Path(sys.argv[2]).read_text().split('\n')
out = Path(sys.argv[3]); out.mkdir(parents=True, exist_ok=True)
ops = [op for op in difflib.SequenceMatcher(None, ref, cur, autojunk=False).get_opcodes() if op[0] != 'equal']
for n, (tag, i1, i2, j1, j2) in enumerate(ops):
    trial = cur[:j1] + ref[i1:i2] + cur[j2:]
    (out / ('r%02d_%d.c' % (n, i1 + 1))).write_text('\n'.join(trial))
print(len(ops))

#!/usr/bin/env python3
"""mapord.py OUT_A OUT_B ORDER_A : map a TXORDER uid list from trace dir A to trace dir B by the
position of each insn in the pre-sched1 block (both blocks must have the same insn count)."""
import sys, importlib.util, os
spec = importlib.util.spec_from_file_location('blk', os.path.join(os.path.dirname(__file__), 'blk.py'))
src = open(spec.origin).read().split("\npre = block(")[0]
ns = {}; exec(compile(src, 'blk', 'exec'), ns)
from pathlib import Path
A = ns['block'](ns['parse'](Path(sys.argv[1]) / 't.i.combine'))
B = ns['block'](ns['parse'](Path(sys.argv[2]) / 't.i.combine'))
assert len(A) == len(B), (len(A), len(B))
m = {ns['uid'](a): ns['uid'](b) for a, b in zip(A, B)}
print(','.join(str(m[int(x)]) for x in sys.argv[3].split(',')))

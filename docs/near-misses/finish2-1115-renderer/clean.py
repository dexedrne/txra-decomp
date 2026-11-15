#!/usr/bin/env python3
"""Drop search noise from a candidate (run on a worker, never the laptop):
    python3 clean.py BEST.c REFERENCE.c OUT.c

Every line hunk where BEST differs from REFERENCE is reverted to the reference
text, one at a time, and kept reverted only if the compiled ARM bytes stay
identical to BEST's. The result compiles to exactly the same function bytes
with the fewest source edits. Diagnostic only; nothing ROM-derived is written.
"""
import difflib, hashlib, sys
from pathlib import Path
sys.path.insert(0, 'tools'); sys.path.insert(0, 'recomp')
import measure_candidate as mc, draft, reloc

START = 0x08016DA8
prog = draft.Program(); table = reloc.symbols(prog)


def code(lines):
    try:
        got, frame = mc.diagnostic_compile('\n'.join(lines), 'func_%08X' % START, START, table, 'arm')
    except Exception:
        return None
    return hashlib.sha256(got).hexdigest(), frame


best = Path(sys.argv[1]).read_text().split('\n')
ref = Path(sys.argv[2]).read_text().split('\n')
target = code(best)
cur = best
changed = True
while changed:
    changed = False
    ops = [op for op in difflib.SequenceMatcher(None, ref, cur, autojunk=False).get_opcodes() if op[0] != 'equal']
    for tag, i1, i2, j1, j2 in reversed(ops):
        trial = cur[:j1] + ref[i1:i2] + cur[j2:]
        if code(trial) == target:
            cur = trial
            changed = True
            print('reverted hunk ref %d-%d' % (i1 + 1, i2), flush=True)
            break
Path(sys.argv[3]).write_text('\n'.join(cur))
left = [op for op in difflib.SequenceMatcher(None, ref, cur, autojunk=False).get_opcodes() if op[0] != 'equal']
print('remaining hunks', len(left), 'identical code', code(cur) == target)

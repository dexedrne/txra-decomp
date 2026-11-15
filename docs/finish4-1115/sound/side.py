#!/usr/bin/env python3
"""Diagnostic (worker only): side-by-side instruction text of the original 080064A4 listing
(rebuilt in memory) and a candidate (.c through the official measure path, or a .s from the
private traced compiler), aligned by opcode shape, for one address range.  Instruction text
only; no encodings or pool values are printed.  usage: side.py <file.c|file.s> <lo> <hi>"""
import sys, re, difflib
sys.path.insert(0, 'tools'); sys.path.insert(0, 'recomp')
sys.path.insert(0, 'docs/near-misses/finish2-1115-sound')
sys.path.insert(0, 'docs/finish4-1115/sound')
import batch as B
import importlib.util
spec = importlib.util.spec_from_file_location('al', 'docs/finish4-1115/sound/align_lib.py')
al = importlib.util.module_from_spec(spec); spec.loader.exec_module(al)
path, lo, hi = sys.argv[1], int(sys.argv[2], 16), int(sys.argv[3], 16)
actual, frame = al.actual_of(path)
rows = B.norm_rows(B.listing(actual))
rows = [re.sub(r'=[0-9A-F]{8}', '=pool', r) for r in rows]
tgt = [re.sub(r'=[0-9A-F]{8}', '=pool', r) for r in B.TARGET]
shape = lambda s: re.sub(r'\b(r\d|sl|sb|ip|r8)\b', 'R', s)
sm = difflib.SequenceMatcher(None, [shape(x) for x in tgt], [shape(x) for x in rows], autojunk=False)
for op, i1, i2, j1, j2 in sm.get_opcodes():
    n = max(i2 - i1, j2 - j1)
    for k in range(n):
        ti = i1 + k if i1 + k < i2 else None
        cj = j1 + k if j1 + k < j2 else None
        a = B.TADDR[ti] if ti is not None else (B.TADDR[i1] if i1 < len(B.TADDR) else 0)
        if not (lo <= a < hi): continue
        t = tgt[ti] if ti is not None else ''
        c = rows[cj] if cj is not None else ''
        mark = '  ' if t == c else ('r ' if op == 'equal' else 'X ')
        print('%s%08X  %-34s %s' % (mark, a, t, c))

#!/usr/bin/env python3
"""Score many 08016DA8 candidates in parallel (worker only). Prints metadata only:
    python3 batch.py [-j N] a.c b.c ...   ->  diff dist len frame name"""
import sys, os
from multiprocessing import Pool
from pathlib import Path
START, END = 0x08016DA8, 0x08017E68
S = {}
def init():
    sys.path.insert(0, 'tools'); sys.path.insert(0, 'recomp')
    import measure_candidate as mc, draft, reloc, variant_search, llm_match as match
    prog = draft.Program()
    S.update(mc=mc, vs=variant_search, table=reloc.symbols(prog), want=prog.rom[START - match.BASE:END - match.BASE])
def ev(path):
    try:
        got, frame = S['mc'].diagnostic_compile(Path(path).read_text(), 'func_%08X' % START, START, S['table'], 'arm')
    except Exception as e:
        return path, None
    dist, diff = S['vs'].score(S['want'], got, START, 'arm')
    return path, (diff, dist, len(got), frame)
if __name__ == '__main__':
    a = sys.argv[1:]; j = 10
    if a and a[0] == '-j': j = int(a[1]); a = a[2:]
    with Pool(j, initializer=init) as p:
        for path, r in p.imap(ev, a):
            print(('%-5s %-4s %-5s %-4s %s' % (r + (os.path.basename(path),))) if r else 'ERR %s' % path, flush=True)

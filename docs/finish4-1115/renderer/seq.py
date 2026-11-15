#!/usr/bin/env python3
"""Print our compiled instructions in [lo,hi) for candidates (worker only; our own output only)."""
import re, sys
from multiprocessing import Pool
from pathlib import Path
START = 0x08016DA8
S = {}
def init():
    sys.path.insert(0, 'tools'); sys.path.insert(0, 'recomp')
    import measure_candidate as mc, draft, reloc, diffhint
    prog = draft.Program()
    S.update(mc=mc, dh=diffhint, table=reloc.symbols(prog))
def run(a):
    path, lo, hi = a
    try:
        got, frame = S['mc'].diagnostic_compile(Path(path).read_text(), 'func_%08X' % START, START, S['table'], 'arm')
    except Exception as e:
        return '%s ERR' % path
    out = []
    for line in S['dh'].listing(got, START, 'arm'):
        ad, rest = line.split(':', 1)
        if lo <= int(ad, 16) < hi and '.word' not in rest:
            out.append(re.split(r'\s{2,}', rest.strip(), maxsplit=1)[-1].replace(', ', ','))
    return '%s | %s' % (Path(path).name, ' ; '.join(out))
if __name__ == '__main__':
    lo, hi = int(sys.argv[1], 16), int(sys.argv[2], 16)
    with Pool(int(sys.argv[3]), initializer=init) as p:
        for l in p.imap(run, [(f, lo, hi) for f in sys.argv[4:]]):
            print(l, flush=True)

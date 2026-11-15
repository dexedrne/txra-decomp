#!/usr/bin/env python3
"""Batch region score for 08016DA8 candidates (worker only, diagnostic).
    python3 rscore.py LO HI WORKERS a.c b.c ...   (or @listfile)
One line per file: name diff dist len frame struct reg | region struct/reg rows inside [LO,HI) of the target."""
import re, sys, difflib
from multiprocessing import Pool
from pathlib import Path
START, END = 0x08016DA8, 0x08017E68
S = {}
def init():
    sys.path.insert(0, 'tools'); sys.path.insert(0, 'recomp')
    import measure_candidate as mc, draft, reloc, variant_search, diffhint, llm_match as match
    prog = draft.Program()
    S.update(mc=mc, vs=variant_search, dh=diffhint, table=reloc.symbols(prog),
             want=prog.rom[START - match.BASE:END - match.BASE])
    S['T'] = lst(S['want'])
def lst(data):
    out = []
    for line in S['dh'].listing(data, START, 'arm'):
        a, rest = line.split(':', 1)
        if '.word' in rest: ins = '.word'
        else:
            ins = re.split(r'\s{2,}', rest.strip(), maxsplit=1)[-1]
            ins = re.sub(r'\[pc, #-?\d+\] @ =0x[0-9A-F]+', '[pc]', ins)
        out.append((int(a, 16), ins))
    return out
def norm(ins):
    ins = re.sub(r'\b(r\d+|sb|sl|fp|ip|lr|sp)\b', 'R', ins)
    return re.sub(r'0x080[0-9A-Fa-f]{5}', 'ADDR', ins)
def run(args):
    path, lo, hi = args
    try:
        got, frame = S['mc'].diagnostic_compile(Path(path).read_text(), 'func_%08X' % START, START, S['table'], 'arm')
    except Exception as e:
        return '%s ERR' % Path(path).name
    T = S['T']; C = lst(got)
    sm = difflib.SequenceMatcher(None, [norm(i) for _, i in T], [norm(i) for _, i in C], autojunk=False)
    st = rg = rst = rrg = 0; last = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        for k in range(max(i2 - i1, j2 - j1)):
            t = T[i1 + k] if i1 + k < i2 else None
            c = C[j1 + k] if j1 + k < j2 else None
            if t: last = t[0]
            if t and c and t[1] == c[1]: continue
            inr = lo <= last < hi
            if tag == 'equal': rg += 1; rrg += inr
            else: st += 1; rst += inr
    dist, diff = S['vs'].score(S['want'], got, START, 'arm')
    return '%s %d %d %d %s %d %d | %d %d' % (Path(path).name, diff, dist, len(got), frame, st, rg, rst, rrg)
if __name__ == '__main__':
    lo, hi, w = int(sys.argv[1], 16), int(sys.argv[2], 16), int(sys.argv[3])
    files = []
    for a in sys.argv[4:]:
        files += Path(a[1:]).read_text().split() if a.startswith('@') else [a]
    with Pool(w, initializer=init) as p:
        for line in p.imap(run, [(f, lo, hi) for f in files], chunksize=4):
            print(line, flush=True)

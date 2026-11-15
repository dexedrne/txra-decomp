#!/usr/bin/env python3
"""Measure many complete 080064A4 candidates in parallel (run on a worker with the private ROM).

For each source: differing bytes and instruction distance from the unchanged measure_candidate
compiler path, plus a text alignment against the original listing (opcode shape first, then
registers).  The original listing is rebuilt in memory from recomp/draft.py on every run; it is
never written to disk or printed.  usage: batch.py <file.c>...   (JOBS=n for parallelism)"""
import sys, re, struct, json, os
from multiprocessing import Pool
sys.path.insert(0, 'tools'); sys.path.insert(0, 'recomp')
from pathlib import Path
import measure_candidate as mc, draft, reloc, variant_search
prog = draft.Program()
table = reloc.symbols(prog)
START, END = 0x080064A4, 0x08007398
want = prog.rom[START - 0x08000000:END - 0x08000000]

def norm_rows(lines):
    import difflib
    rows = []
    for l in lines:
        m = re.match(r'([0-9A-F]{8}): (.*)', l.rstrip())
        if not m: continue
        asm = m.group(2)
        sym = re.search(r'; =0x([0-9A-F]{8})', asm)
        asm = re.sub(r'\s*;.*', '', asm); asm = re.sub(r'\s*@.*', '', asm)
        if sym: asm = re.sub(r'\[pc, #\d+\]', '=' + sym.group(1), asm)
        asm = re.sub(r'\b(b\w*|bl) 0x[0-9A-F]+', r'\1 L', asm)
        asm = re.sub(r'^[0-9A-F]{8} ', '', asm)
        asm = asm.replace('r10', 'sl').replace('r9', 'sb').replace('r12', 'ip')
        rows.append(asm)
    return rows

def target_listing():
    out = []
    for i in prog.insns[START]:
        extra = ''
        if i.ir[0] == 'pool':
            v = prog.word(i.ir[2])
            extra = ' ; =0x%08X' % v if v is not None else ''
        out.append('%08X: %s%s' % (i.addr, i.asm, extra))
    return out
_TL = target_listing()
TARGET = norm_rows(_TL)
TADDR = [int(l[:8], 16) for l in _TL]
del _TL
REGIONS = [(0x080064A4,0x080065C2,'A'),(0x080065C2,0x08006712,'B'),(0x08006712,0x08006776,'C'),(0x08006776,0x08006D62,'D'),(0x08006D62,0x08006ECC,'E'),(0x08006ECC,0x08006FCC,'F'),(0x08006FCC,0x08007352,'G'),(0x08007352,0x08007398,'H')]
def region(a):
    for lo, hi, n in REGIONS:
        if lo <= a < hi: return n
    return '?'

def listing(actual):
    lines = draft.disassemble_thumb(actual, START)
    pools = {int(m.group(1), 16) for l in lines for m in [re.search(r'@ =0x([0-9A-Fa-f]{8})', l)] if m}
    out = []
    for l in lines:
        a = int(l.split(':', 1)[0], 16)
        if a - 2 in pools or a in pools: continue
        m = re.search(r'@ =0x([0-9A-Fa-f]{8})', l)
        asm = re.sub(r'^(\w{8}):\s+[0-9A-Fa-f]{4}(?: [0-9A-Fa-f]{4})?\s+', r'\1: ', l)
        if m:
            p = int(m.group(1), 16) - START
            if 0 <= p <= len(actual) - 4:
                asm += ' ; =0x%08X' % struct.unpack_from('<I', actual, p)[0]
        out.append(asm)
    return out

def one(path):
    import difflib
    try:
        code = Path(path).read_text()
        actual, frame = mc.diagnostic_compile(code, 'func_080064A4', START, table, 'old')
    except Exception as e:
        return dict(file=path, error=str(e)[:200])
    score = variant_search.score(want, actual, START, 'thumb')
    rows = norm_rows(listing(actual))
    shape = lambda s: re.sub(r'\b(r\d|sl|sb|ip|r8)\b', 'R', s)
    sm = difflib.SequenceMatcher(None, [shape(x) for x in TARGET], [shape(x) for x in rows], autojunk=False)
    same = reg = shp = 0
    rs = {}
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == 'equal':
            for k in range(i2 - i1):
                if TARGET[i1 + k] == rows[j1 + k]: same += 1; rs[region(TADDR[i1+k])] = rs.get(region(TADDR[i1+k]), 0) + 1
                else: reg += 1
        else:
            shp += max(i2 - i1, j2 - j1)
    exact = actual == want
    return dict(rs=''.join('%s%d ' % (n, rs.get(n, 0)) for _, _, n in REGIONS), file=path, emit=len(actual), frame=frame, dist=score[0], diff=score[1], same=same, reg=reg, shape=shp, exact=exact)

if __name__ == '__main__':
    files = sys.argv[1:]
    with Pool(int(os.environ.get('JOBS', '6'))) as p:
        for r in p.imap(one, files):
            if 'error' in r: print('%-40s ERROR %s' % (r['file'], r['error']))
            else: print('%-40s emit %4d frame %3s dist %4d DIFF %4d same %4d reg %4d shape %4d%s' % (r['file'], r['emit'], r['frame'], r['dist'], r['diff'], r['same'], r['reg'], r['shape'], ' EXACT' if r['exact'] else '') + '  ' + r['rs'])
            sys.stdout.flush()

#!/usr/bin/env python3
"""Shape alignment of a candidate (.c via the official measure path, or a diagnostic .s from the
private traced compiler) against the original 080064A4 listing, rebuilt in memory on the worker.
Prints per-region exact-row counts and every non-equal shape hunk.  Nothing is written to disk.
usage: align.py <file.c|file.s> [maxhunks]"""
import sys, re, difflib, tempfile
sys.path.insert(0, 'tools'); sys.path.insert(0, 'recomp')
sys.path.insert(0, 'docs/near-misses/finish2-1115-sound')
from pathlib import Path
import batch as B
import measure_candidate as mc, reloc, variant_search
import llm_match as match

def actual_of(path):
    if path.endswith('.c'):
        a, frame = mc.diagnostic_compile(Path(path).read_text(), 'func_080064A4', B.START, B.table, 'old')
        return a, frame
    asm = Path(path).read_text()
    name = 'func_080064A4'
    with tempfile.TemporaryDirectory(prefix='al-', dir='build') as td:
        f = Path(td)
        begin = re.search(r'(?m)^' + name + ':', asm).start()
        tail = asm[begin:]
        end = re.search(r'\n\s*\.size\s+' + name + r',[^\n]*', tail).end()
        (f / 'one.s').write_text('.syntax divided\n.text\n.thumb\n' + tail[:end] + '\n')
        match.run([match.ARM + 'as', '-mcpu=arm7tdmi', f / 'one.s', '-o', f / 'one.o'])
        match.run([match.ARM + 'objcopy', '-O', 'binary', '-j', '.text', f / 'one.o', f / 'one.bin'])
        a = reloc.function_bytes(f / 'one.o', (f / 'one.bin').read_bytes(), name, match.ARM + 'objdump')
        e = reloc.parse(match.run([match.ARM + 'objdump', '-r', f / 'one.o']).stdout)
        a = reloc.relocate(a, e, B.START, B.table) if e else a
    fr = re.search(r'add\s+sp, sp, #-(\d+)', asm)
    return a, int(fr[1]) if fr else None

path = sys.argv[1]; maxh = int(sys.argv[2]) if len(sys.argv) > 2 else 40
actual, frame = actual_of(path)
score = variant_search.score(B.want, actual, B.START, 'thumb')
rows = B.norm_rows(B.listing(actual))
shape = lambda s: re.sub(r'\b(r\d|sl|sb|ip|r8)\b', 'R', s)
sm = difflib.SequenceMatcher(None, [shape(x) for x in B.TARGET], [shape(x) for x in rows], autojunk=False)
same = reg = shp = 0; rs = {}; rr = {}; hunks = []
for op, i1, i2, j1, j2 in sm.get_opcodes():
    if op == 'equal':
        for k in range(i2 - i1):
            n = B.region(B.TADDR[i1 + k])
            if B.TARGET[i1 + k] == rows[j1 + k]: same += 1; rs[n] = rs.get(n, 0) + 1
            else: reg += 1; rr[n] = rr.get(n, 0) + 1
    else:
        shp += max(i2 - i1, j2 - j1)
        hunks.append((op, B.TADDR[i1] if i1 < len(B.TADDR) else 0, B.TARGET[i1:i2], rows[j1:j2]))
print('%s emit %d frame %s dist %d DIFF %d same %d reg %d shape %d %s' % (path, len(actual), frame, score[0], score[1], same, reg, shp, 'EXACT' if actual == B.want else ''))
print('  exact/reg-only rows per region: ' + ' '.join('%s%d/%d' % (n, rs.get(n, 0), rr.get(n, 0)) for _, _, n in B.REGIONS))
for op, a, t, c in hunks[:maxh]:
    print('  %s @%08X  T: %s  |  C: %s' % (op, a, ' ; '.join(t)[:160], ' ; '.join(c)[:160]))

#!/usr/bin/env python3
"""What-if compile with the private tracing cc1 (worker only, diagnostic, never for matching).
    TXFORCE=70:4,75:14 python3 whatif.py cand.c [--sbs [lo hi]] [--trace]
Prints diff/dist/len/frame/struct/reg rows like sbs2 --score; --sbs prints the side-by-side."""
import os, re, sys, subprocess, tempfile, difflib
from pathlib import Path
sys.path.insert(0, 'tools'); sys.path.insert(0, 'recomp')
import draft, reloc, variant_search, diffhint, llm_match as match
START, END = 0x08016DA8, 0x08017E68
args = [a for a in sys.argv[1:] if not a.startswith('--')]
src = Path(args[0]).read_text()
prog = draft.Program(); table = reloc.symbols(prog)
want = prog.rom[START - match.BASE:END - match.BASE]
CC = os.path.expanduser('~/txra-shape-cc/gcc_arm/cc1')
name = 'func_%08X' % START
with tempfile.TemporaryDirectory(prefix='wi-', dir='build') as td:
    folder = Path(td)
    code = src if 'typedef unsigned char u8;' in src else match.PRELUDE + src
    (folder / 'trial.c').write_text(code)
    match.run([match.ARM + 'gcc', '-E', '-P', '-Isrc', folder / 'trial.c', '-o', folder / 'trial.i'])
    env = dict(os.environ); env.setdefault('TXDBG', 'GR')
    r = subprocess.run([CC, '-quiet', str(folder / 'trial.i'), '-O2', '-mthumb-interwork', '-o', str(folder / 'trial.s')],
                       capture_output=True, text=True, env=env, timeout=120)
    if '--trace' in sys.argv:
        Path('build/shape-wi-trace.txt').write_text(r.stderr)
    assembly = (folder / 'trial.s').read_text()
    begin = re.search(r'(?m)^' + re.escape(name) + ':', assembly).start()
    tail = assembly[begin:]
    end = re.search(r'\n\s*\.size\s+' + re.escape(name) + r',[^\n]*', tail).end()
    (folder / 'one.s').write_text('.syntax divided\n.text\n.arm\n' + tail[:end] + '\n')
    match.run([match.ARM + 'as', '-mcpu=arm7tdmi', folder / 'one.s', '-o', folder / 'one.o'])
    match.run([match.ARM + 'objcopy', '-O', 'binary', '-j', '.text', folder / 'one.o', folder / 'one.bin'])
    obj = folder / 'one.o'
    got = reloc.function_bytes(obj, (folder / 'one.bin').read_bytes(), name, match.ARM + 'objdump')
    entries = reloc.parse(match.run([match.ARM + 'objdump', '-r', obj]).stdout)
    got = reloc.relocate(got, entries, START, table) if entries else got
    frame = re.search(r'frame = (\d+)', assembly)
def lst(data):
    out = []
    for line in diffhint.listing(data, START, 'arm'):
        a, rest = line.split(':', 1)
        if '.word' in rest: ins = '.word <pool>'
        else:
            ins = re.split(r'\s{2,}', rest.strip(), maxsplit=1)[-1]
            ins = re.sub(r'\[pc, #-?\d+\] @ =0x[0-9A-F]+', '[pc] =POOL', ins)
        out.append((int(a, 16), ins))
    return out
def norm(ins):
    ins = re.sub(r'\b(r\d+|sb|sl|fp|ip|lr|sp)\b', 'R', ins)
    return re.sub(r'0x080[0-9A-Fa-f]{5}', 'ADDR', ins).strip()
T = lst(want); C = lst(got)
sm = difflib.SequenceMatcher(None, [norm(i) for _, i in T], [norm(i) for _, i in C], autojunk=False)
rows = []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    for k in range(max(i2 - i1, j2 - j1)):
        t = T[i1 + k] if i1 + k < i2 else None
        c = C[j1 + k] if j1 + k < j2 else None
        mark = '  ' if (t and c and t[1] == c[1]) else ('~ ' if tag == 'equal' else '! ')
        rows.append((t[0] if t else None, mark, t, c))
dist, diff = variant_search.score(want, got, START, 'arm')
first = next((i for i in range(min(len(want), len(got))) if want[i] != got[i]), None)
print('diff=%d dist=%d len=%d frame=%s struct=%d reg=%d first=%s' % (diff, dist, len(got), frame and frame[1],
      sum(r[1] == '! ' for r in rows), sum(r[1] == '~ ' for r in rows), '%08X' % (START + first) if first is not None else 'none'))
if '--sbs' in sys.argv:
    lo = int(args[1], 16) if len(args) > 1 else 0
    hi = int(args[2], 16) if len(args) > 2 else 1 << 40
    last = 0
    for a, mark, t, c in rows:
        if a: last = a
        if lo <= last < hi:
            print('%s%-44s | %s' % (mark, ('%08X %s' % t) if t else '', ('%08X %s' % c) if c else ''))

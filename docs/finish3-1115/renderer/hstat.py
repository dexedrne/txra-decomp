#!/usr/bin/env python3
"""Header allocation stats for 08016DA8 candidates (worker only, diagnostic).
    python3 hstat.py a.c [b.c ...]
Per file: diff/dist/len/frame, then for the four header depth loads: the depth pseudo and
its base-pointer pseudo with refs/live/priority and the hard register they got."""
import math, re, subprocess, sys, tempfile, os
from pathlib import Path
sys.path.insert(0, 'tools'); sys.path.insert(0, 'recomp')
import measure_candidate as mc, draft, reloc, variant_search, llm_match as match
START, END = 0x08016DA8, 0x08017E68
prog = draft.Program(); table = reloc.symbols(prog)
want = prog.rom[START - match.BASE:END - match.BASE]
CC = str(match.CC.with_name('agbcc_arm'))
def pri(u, l): return int(math.log2(u)) * u / l if u > 0 and l > 0 else 0
def stats(src):
    with tempfile.TemporaryDirectory(prefix='hs-', dir='build') as td:
        d = Path(td)
        code = src if 'typedef unsigned char u8;' in src else match.PRELUDE + src
        (d / 't.c').write_text(code)
        match.run([match.ARM + 'gcc', '-E', '-P', '-Isrc', d / 't.c', '-o', d / 't.i'])
        subprocess.run([CC, 't.i', '-O2', '-mthumb-interwork', '-dl', '-dg', '-o', 't.s'], cwd=d, check=True,
                       capture_output=True, timeout=120)
        lreg = (d / 't.i.lreg').read_text(); greg = (d / 't.i.greg').read_text()
    disp = {int(a): int(b) for a, b in re.findall(r'(\d+) in (\d+)', greg.split(';; Register dispositions:')[1].split('\n\n')[0])}
    info = {int(a): (int(b), int(c)) for a, b, c in re.findall(r'Register (\d+) used (\d+) times across (\d+) insns', lreg)}
    ld = dict(re.findall(r'\(set \(reg:SI (\d+)\)\s+\(mem/s:SI \(plus:SI \(reg:SI (\d+)\)\s+\(const_int 24\)\) 1\)\)', lreg))
    loads = []
    for off in (-16, -12, -8, -4):
        m = re.search(r'\(set \(mem/s:SI \(plus:SI \(reg:SI 25 sfp\)\s+\(const_int %d\)\) 1\)\s+\(reg:SI (\d+)\)\)' % off, lreg)
        v = m.group(1) if m else '0'
        loads.append((v, ld.get(v, '0')))
    out = []
    for k, (v, p) in enumerate(loads):
        v, p = int(v), int(p)
        uv, lv = info.get(v, (0, 1)); up, lp = info.get(p, (0, 1))
        out.append('d%d:%d r%s %d/%d %.2f | p%d:%d r%s %d/%d %.2f' % (k, v, disp.get(v, '-'), uv, lv, pri(uv, lv),
                                                               k, p, disp.get(p, '-'), up, lp, pri(up, lp)))
    return out
for path in sys.argv[1:]:
    src = Path(path).read_text()
    try:
        got, frame = mc.diagnostic_compile(src, 'func_%08X' % START, START, table, 'arm')
        dist, diff = variant_search.score(want, got, START, 'arm')
        first = next((i for i in range(min(len(want), len(got))) if want[i] != got[i]), None)
        print('%s diff=%d dist=%d len=%d frame=%s first=%08X' % (Path(path).name, diff, dist, len(got), frame, START + (first or 0)))
        for l in stats(src): print('   ', l)
    except Exception as e:
        print(Path(path).name, 'ERR', str(e)[:200])
    sys.stdout.flush()

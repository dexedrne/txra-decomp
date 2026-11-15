#!/usr/bin/env python3
"""Batch-measure 08016DA8 candidates on a worker (never the laptop):
    python3 fm.py a.c [b.c ...]
One line per source: differing bytes, instruction distance, emitted bytes, frame,
and the global-alloc priority / hard register of the points base and the scratch
pointer (from -dl -dg dumps). Diagnostic only: no admission authority, nothing kept."""
import math, re, subprocess, sys, tempfile
from pathlib import Path
sys.path.insert(0, 'tools'); sys.path.insert(0, 'recomp')
import measure_candidate as mc, draft, reloc, variant_search, llm_match as match
START, END = 0x08016DA8, 0x08017E68
prog = draft.Program(); table = reloc.symbols(prog)
want = prog.rom[START - match.BASE:END - match.BASE]
CC = match.CC.with_name('agbcc_arm')

def prio(src):
    with tempfile.TemporaryDirectory(prefix='fm-', dir='build') as td:
        d = Path(td)
        code = src if 'typedef unsigned char u8;' in src else match.PRELUDE + src
        (d / 't.c').write_text(code)
        match.run([match.ARM + 'gcc', '-E', '-P', '-Isrc', d / 't.c', '-o', d / 't.i'])
        subprocess.run([str(CC), 't.i', '-O2', '-mthumb-interwork', '-dl', '-dg', '-o', 't.s'],
                       cwd=d, check=True, capture_output=True, timeout=60)
        lreg = (d / 't.i.lreg').read_text(); greg = (d / 't.i.greg').read_text()
    disp = dict(re.findall(r'(\d+) in (\d+)', greg.split(';; Register dispositions:')[1].split(';;')[0]))
    def find(pat):
        m = re.search(pat, lreg); return m.group(1) if m else None
    out = {}
    for name, pat in (('pts', r'\(set \(reg/v:SI (\d+)\)\s+\(const_int 33554432'),
                      ('scr', r'\(set \(reg(?:/v)?:SI (\d+)\)\s+\(mem/u:SI \(symbol_ref/u:SI \("\*\.LC\d+"\)\)\)\s*\n?[^\n]*\n?[^\n]*g_030057A0'),
                      ('scr2', r'\(set \(reg(?:/v)?:SI (\d+)\)\s+\(symbol_ref:SI \("g_030057A0"\)\)\)')):
        r = find(pat)
        m = r and re.search(r'Register %s used (\d+) times across (\d+) insns' % r, lreg)
        if m:
            u, l = int(m.group(1)), int(m.group(2))
            out[name] = '%s:r%s u%d l%d p%d' % (r, disp.get(r, '-'), u, l, int(int(math.log2(u)) * u * 10000 / l))
    return ' '.join('%s=%s' % kv for kv in out.items())

for path in sys.argv[1:]:
    src = Path(path).read_text()
    try:
        got, frame = mc.diagnostic_compile(src, 'func_%08X' % START, START, table, 'arm')
    except Exception as exc:
        print('%-40s ERROR %s' % (Path(path).name, str(exc)[:200])); continue
    dist, diff = variant_search.score(want, got, START, 'arm')
    try:
        p = prio(src)
    except Exception as exc:
        p = 'prio-error %s' % str(exc)[:80]
    print('%-40s diff=%5d dist=%4d len=%d frame=%s %s' % (Path(path).name, diff, dist, len(got), frame, p), flush=True)

#!/usr/bin/env python3
"""Diagnostic only: compile a complete 080181C0 candidate with allocation dumps.

Runs the historical ARM compiler with the unchanged `arm` profile flags
(-O2 -mthumb-interwork) plus -dl -dg (local and global allocation dumps) on
OUR OWN C, keeps the dumps under build/contact-alloc/<tag>/ on the worker and
prints the global allocation order with refs, live length and priority.
Optional extra flags are for diagnosis only. Reads no ROM bytes, writes no
binary data and has no admission or installation authority.

  contact_alloc1115c.py SOURCE TAG [--cc COMPILER] [EXTRA_FLAG...]
"""
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import llm_match as match


def main():
    args = sys.argv[1:]
    cc = match.CC.with_name('agbcc_arm')
    if '--cc' in args:
        i = args.index('--cc'); cc = Path(args[i + 1]); del args[i:i + 2]
    source, tag, extra = Path(args[0]), args[1], args[2:]
    out = Path('build/contact-alloc') / tag
    out.mkdir(parents=True, exist_ok=True)
    code = source.read_text()
    (out / 'trial.c').write_text(code if 'typedef unsigned char u8;' in code else match.PRELUDE + code)
    match.run([match.ARM + 'gcc', '-E', '-P', '-Isrc', out / 'trial.c', '-o', out / 'trial.i'])
    r = match.run([cc.resolve(), 'trial.i', '-O2', '-mthumb-interwork', '-dl', '-dg', *extra,
                   '-o', 'trial.s'], cwd=out)
    asm = (out / 'trial.s').read_text()
    frame = re.search(r'frame = (\d+)', asm)
    print('frame', frame[1] if frame else '?')
    greg = out / 'trial.i.greg'
    if not greg.exists():
        print('no greg'); return
    text = greg.read_text()
    m = re.search(r'Pass 1 registers to be allocated in sorted order:\n(.*?)\n\n', text, re.S)
    rows = m[1].splitlines() if m else []
    regs = {}
    rm = re.search(r';; Register dispositions:\n(.*?)\n\n', text, re.S)
    if rm:
        for a, b in re.findall(r'(\d+) in (\d+)', rm[1]):
            regs[int(a)] = int(b)
    for n, row in enumerate(rows):
        mm = re.match(r'Register (\d+), refs = (\d+), live_length = (-?\d+), size = (\d+)', row)
        if not mm:
            print(row); continue
        reg, refs, live, size = map(int, mm.groups())
        pri = (int(math.floor(math.log2(refs))) if refs > 0 else 0) * refs / live * size if live else 0
        print('%3d reg %4d refs %4d live %5d pri %6.3f -> %s %s' % (n, reg, refs, live, pri, regs.get(reg, '-'), row[mm.end():]))


if __name__ == '__main__':
    main()

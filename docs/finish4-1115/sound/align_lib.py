#!/usr/bin/env python3
"""(library form of align.py) Shape alignment of a candidate (.c via the official measure path, or a diagnostic .s from the
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


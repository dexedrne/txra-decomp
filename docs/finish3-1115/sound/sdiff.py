#!/usr/bin/env python3
"""Diagnostic only (worker): measure an assembly file produced by the private traced compiler
against the original owner, to learn what an allocator decision would change.  Never an
admission or match claim.  usage: sdiff.py <file.s> <out-prefix>"""
import sys, re, tempfile
from pathlib import Path
sys.path.insert(0, 'tools'); sys.path.insert(0, 'recomp')
import measure_candidate as mc, draft, reloc, variant_search
import llm_match as match
START, END = 0x080064A4, 0x08007398
name = 'func_%08X' % START
prog = draft.Program(); table = reloc.symbols(prog)
asm = Path(sys.argv[1]).read_text()
with tempfile.TemporaryDirectory(prefix='sdiff-', dir='build') as td:
    f = Path(td)
    begin = re.search(r'(?m)^' + re.escape(name) + ':', asm).start()
    tail = asm[begin:]
    end = re.search(r'\n\s*\.size\s+' + re.escape(name) + r',[^\n]*', tail).end()
    (f / 'one.s').write_text('.syntax divided\n.text\n.thumb\n' + tail[:end] + '\n')
    match.run([match.ARM + 'as', '-mcpu=arm7tdmi', f / 'one.s', '-o', f / 'one.o'])
    match.run([match.ARM + 'objcopy', '-O', 'binary', '-j', '.text', f / 'one.o', f / 'one.bin'])
    actual = reloc.function_bytes(f / 'one.o', (f / 'one.bin').read_bytes(), name, match.ARM + 'objdump')
    entries = reloc.parse(match.run([match.ARM + 'objdump', '-r', f / 'one.o']).stdout)
    actual = reloc.relocate(actual, entries, START, table) if entries else actual
want = prog.rom[START - match.BASE:END - match.BASE]
score = variant_search.score(want, actual, START, 'thumb')
print('emitted', len(actual), 'target', len(want), 'distance', score[0], 'differing', score[1])
Path(sys.argv[2] + '.diff.txt').write_text(mc.sanitized_diff(want, actual, START, 'thumb'))

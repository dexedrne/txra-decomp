#!/usr/bin/env python3
"""Quick batch score (no dumps): python3 fq.py a.c b.c ... -> name diff dist len frame (worker only)."""
import sys
from pathlib import Path
sys.path.insert(0, 'tools'); sys.path.insert(0, 'recomp')
import measure_candidate as mc, draft, reloc, variant_search, llm_match as match
START, END = 0x08016DA8, 0x08017E68
prog = draft.Program(); table = reloc.symbols(prog)
want = prog.rom[START - match.BASE:END - match.BASE]
for p in sys.argv[1:]:
    try:
        got, frame = mc.diagnostic_compile(Path(p).read_text(), 'func_%08X' % START, START, table, 'arm')
    except Exception as e:
        print(Path(p).name, 'ERR'); continue
    dist, diff = variant_search.score(want, got, START, 'arm')
    print(Path(p).name, diff, dist, len(got), frame, flush=True)

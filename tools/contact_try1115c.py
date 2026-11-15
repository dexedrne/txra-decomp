#!/usr/bin/env python3
"""Diagnostic only: score complete 080181C0 candidates (arm profile, unchanged
flags) in parallel and print differing bytes / instruction edits / size.
Writes nothing except optional per-candidate assembly of OUR OWN C under
build/contact-try/.  No ROM bytes are printed; no admission authority.

  contact_try1115c.py [-j N] [--asm] SOURCE...
"""
import multiprocessing as mp
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'recomp')]
import draft
import llm_match as judge
import reloc
import variant_search as vs

START, END = 0x080181C0, 0x08018854
NAME = 'func_080181C0'


def init_worker():
    global TABLE, ROM, WANT
    program = draft.Program()
    TABLE = reloc.symbols(program)
    ROM = program.rom
    WANT = program.rom[START - draft.BASE:END - draft.BASE]
    if os.environ.get('TXCCDIR'):
        judge.CC = Path(os.environ['TXCCDIR']) / 'old_agbcc'
    os.nice(5)


def evaluate(path):
    source = Path(path).read_text()
    try:
        exact, size, _, expected, actual = judge.compile_candidate(
            source, NAME, START, START + 65536, TABLE, target_end=END, compiler='arm', rom=ROM)
        got = bytes.fromhex(actual)
        edits, diff = vs.score(WANT, got, START, mode='arm')
        if os.environ.get('TXDIFF'):
            import measure_candidate as mc
            text = mc.sanitized_diff(WANT, got, START, 'arm')
            rows = [r for r in text.splitlines() if r[:1] in '+-' and not r.startswith(('---', '+++'))]
            print(path + '\n' + '\n'.join(rows), flush=True)
        return path, diff, edits, len(got), got == WANT
    except Exception as exc:
        return path, None, type(exc).__name__ + ':' + str(exc)[:80], 0, False


def main():
    args = sys.argv[1:]
    jobs = 8
    if args and args[0] == '-j':
        jobs = int(args[1]); args = args[2:]
    if args and args[0] == '--ccdir':
        # diagnostic only: a private debug build of the same compiler sources
        os.environ['TXCCDIR'] = args[1]; args = args[2:]
    with mp.Pool(jobs, initializer=init_worker) as pool:
        for path, diff, edits, size, exact in pool.imap(evaluate, args):
            print('%-60s diff %s edits %s size %d%s' % (path, diff, edits, size, '  EXACT' if exact else ''), flush=True)


if __name__ == '__main__':
    main()

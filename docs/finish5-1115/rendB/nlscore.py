#!/usr/bin/env python3
"""What-if scorer (diagnostic only): for each candidate, find the pseudos of tx, s (sin*dz) and ty,
then compile with the private cc1 treating them as non-local (TXNONLOCAL) and the real sched1
order, and print the score. Answers: does this spelling give the cartridge's sched1 order?
    python3 nlscore.py [-j N] a.c b.c ...     (worker only; metadata output only)"""
import os, sys, tempfile
from multiprocessing import Pool
from pathlib import Path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, 'tools'); sys.path.insert(0, 'recomp')
import roles, oanneal
START, END = 0x08016DA8, 0x08017E68
CC1 = os.path.expanduser('~/rendB-cc/gcc_arm/cc1')
S = {}
def init():
    import measure_candidate as mc, draft, reloc, variant_search, llm_match as match
    wd = Path(tempfile.mkdtemp(prefix='nlcc-', dir='build'))
    (wd / 'agbcc_arm').symlink_to(CC1)
    match.CC = wd / 'agbcc'
    prog = draft.Program()
    S.update(mc=mc, vs=variant_search, table=reloc.symbols(prog), want=prog.rom[START - match.BASE:END - match.BASE])
def ev(path):
    try:
        _, r = roles.info(path)
        regs = [x.split('=')[1].split(':')[0] for x in r.split() if x[:2] in ('tx', 's=', 'ty')]
        regs = [x for x in regs if x.isdigit()]
        os.environ['TXNONLOCAL'] = ','.join(regs)
        got, frame = S['mc'].diagnostic_compile(Path(path).read_text(), 'func_%08X' % START, START, S['table'], 'arm')
        dist, diff = S['vs'].score(S['want'], got, START, 'arm')
        return path, (diff, dist, len(got), frame), r
    except Exception as e:
        return path, None, str(e)[:60]
if __name__ == '__main__':
    a = sys.argv[1:]; j = 8
    if a and a[0] == '-j': j = int(a[1]); a = a[2:]
    with Pool(j, initializer=init) as p:
        for path, r, info in p.imap(ev, a, chunksize=2):
            print(('%-5s %-4s %-5s %-4s ' % r if r else 'ERR ') + '%-14s %s' % (os.path.basename(path), info), flush=True)

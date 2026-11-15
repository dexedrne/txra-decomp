#!/usr/bin/env python3
"""Which single-insn moves of a forced sched1 order keep the what-if score (diagnostic, worker only).
    python3 freedom.py CAND.c ORDER WORKERS RADIUS  -> 'uid from->to score' for every legal move"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ordsearch as O
from multiprocessing import Pool
from pathlib import Path
if __name__ == '__main__':
    src = Path(sys.argv[1]).read_text()
    order = [int(x) for x in sys.argv[2].split(',')]
    W, R = int(sys.argv[3]), int(sys.argv[4])
    body = order[:-1]
    cand = []
    for i in range(len(body)):
        for j in range(max(0, i - R), min(len(body), i + R + 1)):
            if j == i: continue
            b = body[:]; x = b.pop(i); b.insert(j, x)
            cand.append(((b + order[-1:], frozenset()), (body[i], i, j)))
    with Pool(W, initializer=O.init, initargs=(src,)) as pool:
        res = pool.map(O.ev, [c[0] for c in cand], chunksize=4)
    for (st, sc), (_, mv) in zip(res, cand):
        if sc is not None:
            print('%d %d->%d %s' % (mv[0], mv[1], mv[2], sc[0]), flush=True)

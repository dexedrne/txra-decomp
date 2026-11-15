#!/usr/bin/env python3
"""What-if (diagnostic only): enumerate every dependence-respecting order of a window of the
projection block (from uid A to uid B in a given base order) and score each forced sched1 order.
    python3 wenum.py cand.c 'spec' A B WORKERS [LIMIT]
'spec' is applied first (whatif.py syntax). Prints the best orders (metadata only). Worker only."""
import os, sys, itertools
from multiprocessing import Pool
from pathlib import Path
sys.path.insert(0, os.path.dirname(__file__)); sys.path.insert(0, 'tools'); sys.path.insert(0, 'recomp')
import oanneal, whatif
def topo(items, deps, limit, K=99):
    out = []; base = {u: k for k, u in enumerate(items)}
    def rec(prefix, rest):
        if len(out) >= limit: return
        if not rest: out.append(list(prefix)); return
        n = len(prefix)
        if any(base[u] < n - K for u in rest): return
        for u in rest:
            if deps[u] & set(rest) - {u}: continue
            if abs(base[u] - n) > K: continue
            prefix.append(u); rec(prefix, [x for x in rest if x != u]); prefix.pop()
    rec([], items)
    return out
def main():
    src = Path(sys.argv[1]).read_text(); spec = sys.argv[2]; A, B = int(sys.argv[3]), int(sys.argv[4])
    W = int(sys.argv[5]); limit = int(sys.argv[6]) if len(sys.argv) > 6 else 20000
    K = int(os.environ.get('K', '99'))
    order, deps = oanneal.block(src)
    order = whatif.apply(order, spec)
    i, j = order.index(A), order.index(B)
    win = order[i:j + 1]
    d = {u: deps[u] & set(win) for u in win}
    orders = topo(win, d, limit, K)
    print('window', len(win), 'orders', len(orders), flush=True)
    full = [order[:i] + o + order[j + 1:] for o in orders]
    res = []
    with Pool(W, initializer=oanneal.init, initargs=(src,)) as pool:
        for o, r in zip(full, pool.imap(oanneal.ev, full, chunksize=4)):
            if r: res.append((r[0], r[1], r[2], o[i:j + 1]))
    res.sort()
    for r in res[:15]:
        print(r[0], r[1], r[2], ' '.join(map(str, r[3])))
    import collections
    print('hist', sorted(collections.Counter(min(x[0] // 10 * 10, 999) for x in res).items())[:12])
if __name__ == "__main__":
    main()

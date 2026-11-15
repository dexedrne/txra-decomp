#!/usr/bin/env python3
"""Targeted mutation search (a small permuter) for the 08016DA8 renderer owner.

Run on a worker with the private ROM, from the repository root, never on the laptop:
    python3 perm.py BASE.c OUTDIR SECONDS [WORKERS] [SEED]

Every candidate is compiled with the historical ARM profile (agbcc_arm -O2
-mthumb-interwork) through tools/measure_candidate.py's diagnostic compile and
scored against the owner with the repository scorer (differing bytes and
instruction distance). The search only applies semantics-preserving source edits
aimed at register allocation and reload choices:

  wrap     put a run of sibling statements inside `do { ... } while (0);`
           (never around a bare continue/break, which would change control flow)
  unwrap   remove such a wrapper
  swap     exchange two adjacent independent assignments
  comm     swap the operands of a commutative + or * in one statement
  decl     reorder names inside a declaration, or two declaration lines

Nothing ROM-derived is written: OUTDIR receives C sources and a score log only.
A candidate found here is not admitted by this script; it must go through the
normal admission gate and full rebuild.
"""
import math, os, random, re, sys, time
from multiprocessing import Pool
from pathlib import Path

START, END = 0x08016DA8, 0x08017E68
_state = {}


def _init():
    sys.path.insert(0, 'tools'); sys.path.insert(0, 'recomp')
    import measure_candidate as mc, draft, reloc, variant_search, llm_match as match
    prog = draft.Program()
    _state.update(mc=mc, vs=variant_search, table=reloc.symbols(prog),
                  want=prog.rom[START - match.BASE:END - match.BASE])


def evaluate(src):
    st = _state
    try:
        got, frame = st['mc'].diagnostic_compile(src, 'func_%08X' % START, START, st['table'], 'arm')
    except Exception:
        return None
    dist, diff = st['vs'].score(st['want'], got, START, 'arm')
    return diff, dist, len(got), frame


def scalar(r):
    diff, dist, length, frame = r
    return 3 * dist + diff // 3 + (0 if length == END - START else 300) + (0 if frame == 96 else 300)


# ---------------------------------------------------------------- structure
def depths(lines):
    before, after, d = [], [], 0
    for l in lines:
        before.append(d)
        code = l.split('//')[0]
        d += code.count('{') - code.count('}')
        after.append(d)
    return before, after


def unit_end(lines, i, before, after):
    base = before[i]
    for j in range(i, len(lines)):
        if after[j] < base:
            return None
        s = lines[j].strip()
        if after[j] == base and (s.endswith(';') or s.endswith('}')):
            nxt = lines[j + 1].strip() if j + 1 < len(lines) else ''
            if nxt.startswith('else') or nxt.startswith('} else'):
                continue
            return j
    return None


def units(lines):
    """Top-of-statement units inside the function body: (start, end, depth)."""
    before, after = depths(lines)
    out = []
    i = 0
    body = next(k for k, l in enumerate(lines) if l.startswith('void func_08016DA8')) + 2
    i = body
    while i < len(lines):
        s = lines[i].strip()
        if before[i] >= 1 and s and not s.startswith('}') and not s.startswith('/*'):
            j = unit_end(lines, i, before, after)
            if j is not None:
                out.append((i, j, before[i]))
        i += 1
    return out


def siblings(lines):
    """Group units into runs of consecutive siblings (same depth, adjacent)."""
    us = units(lines)
    by_start = {u[0]: u for u in us}
    runs, seen = [], set()
    for u in us:
        if u[0] in seen:
            continue
        run = [u]; seen.add(u[0])
        nxt = u[1] + 1
        while nxt in by_start and by_start[nxt][2] == u[2]:
            run.append(by_start[nxt]); seen.add(nxt); nxt = by_start[nxt][1] + 1
        runs.append(run)
    return runs


LOOP = re.compile(r'^(for|while|do)\b')
DECL = re.compile(r'^\s*(s32|u32|u16|s16|Face|Point|Packet)\b[^=(]*;\s*$')


def wrappable(lines, run):
    for (a, b, d) in run:
        text = '\n'.join(lines[a:b + 1])
        if DECL.match(lines[a]) or 'Packet *p' in text or 's32 n = ' in text:
            return False
        if re.search(r'\b(continue|break)\b', text) and not LOOP.match(lines[a].strip()):
            return False
    return True


def m_wrap(lines, rng):
    runs = [r for r in siblings(lines)]
    rng.shuffle(runs)
    for run in runs:
        if not run:
            continue
        k = rng.randint(1, min(len(run), 12))
        s = rng.randint(0, len(run) - k)
        sub = run[s:s + k]
        if not wrappable(lines, sub):
            continue
        a, b = sub[0][0], sub[-1][1]
        ind = re.match(r'\s*', lines[a]).group(0)
        return lines[:a] + [ind + 'do {'] + lines[a:b + 1] + [ind + '} while (0);'] + lines[b + 1:]
    return None


def m_unwrap(lines, rng):
    cands = [i for i, l in enumerate(lines) if l.strip() == 'do {']
    if not cands:
        return None
    i = rng.choice(cands)
    before, after = depths(lines)
    j = unit_end(lines, i, before, after)
    if j is None or lines[j].strip() != '} while (0);':
        return None
    return lines[:i] + lines[i + 1:j] + lines[j + 1:]


ASSIGN = re.compile(r'^\s*([A-Za-z_][\w\[\]\.\->]*?)\s*(=|\+=|-=|\+\+|--)\s*(.*);\s*$')
IDENT = re.compile(r'[A-Za-z_]\w*')


def deps_ok(l1, l2):
    m1, m2 = ASSIGN.match(l1), ASSIGN.match(l2)
    if not (m1 and m2) or l1.count(';') != 1 or l2.count(';') != 1:
        return False
    if re.search(r'\b(if|for|while|return|continue|break)\b', l1 + l2):
        return False
    lhs1, lhs2 = m1.group(1), m2.group(1)
    def touches(lhs, other):
        if re.fullmatch(r'[A-Za-z_]\w*', lhs):
            return lhs in IDENT.findall(other)
        # compound lvalue: same text, or the other writes its base pointer
        return lhs in other
    if touches(lhs1, l2) or touches(lhs2, l1):
        return False
    b1, b2 = IDENT.match(lhs1).group(0), IDENT.match(lhs2).group(0)
    # a plain-variable write must not feed the other's address
    if re.fullmatch(r'[A-Za-z_]\w*', lhs2) and lhs2 in IDENT.findall(lhs1):
        return False
    if re.fullmatch(r'[A-Za-z_]\w*', lhs1) and lhs1 in IDENT.findall(lhs2):
        return False
    return True


def m_swap(lines, rng):
    idx = [i for i in range(len(lines) - 1) if deps_ok(lines[i], lines[i + 1])
           and re.match(r'\s*', lines[i]).group(0) == re.match(r'\s*', lines[i + 1]).group(0)]
    if not idx:
        return None
    i = rng.choice(idx)
    out = lines[:]
    out[i], out[i + 1] = out[i + 1], out[i]
    return out


def m_move(lines, rng):
    """Move one assignment several places up or down past independent assignments."""
    ind = lambda l: re.match(r'\s*', l).group(0)
    cands = [i for i in range(len(lines)) if ASSIGN.match(lines[i]) and lines[i].count(';') == 1
             and not re.search(r'\b(if|for|while)\b', lines[i])]
    rng.shuffle(cands)
    for i in cands[:20]:
        lo = i
        while lo - 1 >= 0 and ind(lines[lo - 1]) == ind(lines[i]) and deps_ok(lines[lo - 1], lines[i]):
            lo -= 1
        hi = i
        while hi + 1 < len(lines) and ind(lines[hi + 1]) == ind(lines[i]) and deps_ok(lines[i], lines[hi + 1]):
            hi += 1
        if hi - lo < 2:
            continue
        j = rng.randint(lo, hi)
        if j == i:
            continue
        out = lines[:i] + lines[i + 1:]
        out.insert(j, lines[i])
        return out
    return None


OPND = r'(?:[A-Za-z_][\w]*(?:\[[^\[\]]*\])*(?:(?:\.|->)\w+(?:\[[^\[\]]*\])*)*|\d+)'
COMM = re.compile(r'(?<![\w\]\)\.>])(' + OPND + r') ([+*]) (' + OPND + r')(?![\w\[\(\.]|->)')


def m_comm(lines, rng):
    body = next(k for k, l in enumerate(lines) if l.startswith('void func_08016DA8'))
    cands = []
    for i in range(body, len(lines)):
        for m in COMM.finditer(lines[i]):
            l = lines[i]
            pre = l[:m.start()].rstrip()
            post = l[m.end():].lstrip()
            # only swap when the pair is a whole operand of its context
            if m.group(2) == '+':
                ok = pre[-1:] in ('(', '=', '+', ',') and \
                    (post[:1] in (')', ';', '+', '-', ',') and not post.startswith('->'))
            else:
                ok = pre[-1:] not in ('/', '%', '*', ')') and post[:1] not in ('*', '/', '%', '[', '(', '.')
            if ok:
                cands.append((i, m))
    if not cands:
        return None
    i, m = rng.choice(cands)
    l = lines[i]
    out = lines[:]
    out[i] = l[:m.start()] + m.group(3) + ' ' + m.group(2) + ' ' + m.group(1) + l[m.end():]
    return out


def m_decl(lines, rng):
    body = next(k for k, l in enumerate(lines) if l.startswith('void func_08016DA8'))
    cands = [i for i in range(body, len(lines)) if DECL.match(lines[i]) and ',' in lines[i]]
    pairs = [i for i in range(body, len(lines) - 1) if DECL.match(lines[i]) and DECL.match(lines[i + 1])]
    out = lines[:]
    if pairs and (not cands or rng.random() < 0.4):
        i = rng.choice(pairs)
        out[i], out[i + 1] = out[i + 1], out[i]
        return out
    if not cands:
        return None
    i = rng.choice(cands)
    m = re.match(r'^(\s*\w+\s+)(.*);\s*$', lines[i])
    names = [n.strip() for n in m.group(2).split(',')]
    a, b = rng.sample(range(len(names)), 2)
    names[a], names[b] = names[b], names[a]
    out[i] = m.group(1) + ', '.join(names) + ';'
    return out


MUTS = [(m_wrap, 3), (m_unwrap, 2), (m_swap, 4), (m_move, 3), (m_comm, 3), (m_decl, 1)]


def mutate(lines, rng):
    n = rng.choice([1, 1, 1, 2, 2, 3])
    cur = lines
    for _ in range(n):
        for _try in range(10):
            f = rng.choices([m for m, _ in MUTS], weights=[w for _, w in MUTS])[0]
            new = f(cur, rng)
            if new is not None and new != cur:
                cur = new
                break
    return cur


def main():
    base, outdir, seconds = Path(sys.argv[1]), Path(sys.argv[2]), float(sys.argv[3])
    workers = int(sys.argv[4]) if len(sys.argv) > 4 else 6
    seed = int(sys.argv[5]) if len(sys.argv) > 5 else int(time.time())
    rng = random.Random(seed)
    outdir.mkdir(parents=True, exist_ok=True)
    log = open(outdir / 'log.txt', 'a')
    cur = base.read_text().split('\n')
    with Pool(workers, initializer=_init) as pool:
        r = pool.apply(evaluate, ('\n'.join(cur),))
        cur_s = best_s = scalar(r); best = cur
        print('start', r, cur_s, file=log, flush=True)
        t0 = time.time(); n = 0; temp = 6.0
        while time.time() - t0 < seconds:
            cands = [mutate(cur, rng) for _ in range(workers * 4)]
            res = pool.map(evaluate, ['\n'.join(c) for c in cands])
            for c, r in zip(cands, res):
                n += 1
                if r is None:
                    continue
                s = scalar(r)
                if s < best_s:
                    best_s, best = s, c
                    (outdir / 'best.c').write_text('\n'.join(c))
                    (outdir / ('best-%05d.c' % s)).write_text('\n'.join(c))
                    print('%7.0fs n=%d best %d %s' % (time.time() - t0, n, s, r), file=log, flush=True)
                    if r[0] == 0:
                        print('EXACT', file=log, flush=True)
                        return
                if s <= cur_s or rng.random() < math.exp(-(s - cur_s) / temp):
                    cur, cur_s = c, s
            # drift back to the best now and then
            if rng.random() < 0.05:
                cur, cur_s = best, best_s
            if n % 2000 < workers * 4:
                print('%7.0fs n=%d cur %d best %d' % (time.time() - t0, n, cur_s, best_s), file=log, flush=True)
    print('done n=%d best %d' % (n, best_s), file=log, flush=True)


if __name__ == '__main__':
    main()

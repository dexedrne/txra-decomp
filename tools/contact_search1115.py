#!/usr/bin/env python3
"""Diagnostic source search for the complete 080181C0 owner (arm profile only).

Beam search over source rewrites of one complete C body, scored against the
owner bytes with the unchanged historical `arm` profile (-O2 -mthumb-interwork).
Neighbourhoods come from tools/variant_search.mutations plus operand swaps of
commutative operators around array/field expressions. It writes only source
text and a JSON log of scores; it never writes ROM bytes or compiled binaries,
and it has no admission authority: a hit must still pass the normal checker,
the full rebuild and the ROM hash.

  contact_search1115.py SOURCE OUTDIR --seconds N [--jobs J] [--beam B]
"""
import argparse
import hashlib
import json
import multiprocessing as mp
import os
from pathlib import Path
import random
import re
import sys
import time

ROOT = Path(__file__).resolve().parent.parent
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'recomp')]
import draft
import llm_match as judge
import reloc
import variant_search as vs

START, END = 0x080181C0, 0x08018854
NAME = 'func_080181C0'
PRIMARY = r'[A-Za-z_]\w*(?:\[[^\[\]]*\])*(?:\.\w+)?'
LEFT = {'*': '(=,+-', '+': '(=,', '&': '(=,', '|': '(=,', '==': '(|&', '!=': '(|&'}
RIGHT = {'*': ');,+-', '+': ');,', '&': ');,', '|': ');,', '==': ')|&', '!=': ')|&'}


def swaps(code):
    for op in ('*', '+', '&', '|', '==', '!='):
        pat = re.compile(r'(%s)\s*%s\s*(%s)' % (PRIMARY, re.escape(op), PRIMARY))
        for m in pat.finditer(code):
            if op in ('&', '|') and (code[m.end(1):m.start(2)].strip() != op):
                continue
            before = code[:m.start()].rstrip()[-1:] or '('
            after = code[m.end():].lstrip()[:1] or ')'
            if before not in LEFT[op] or after not in RIGHT[op]:
                continue
            if m[1] == m[2]:
                continue
            yield code[:m.start()] + m[2] + ' ' + op + ' ' + m[1] + code[m.end():]


TYPES = re.compile(r'\b(u8|u16|s16|s8|u32|s32|int)\s+\**\w+\s*[;=,]')


def natural(code, base_types):
    # Keep declared scalar types and literal spellings: only equivalent rewrites.
    if sorted(TYPES.findall(code)) != base_types:
        return False
    return not re.search(r'\b\d+U\b|\(1U <<', code)


PAIRS = [
    ('i + j * 16', 'j * 16 + i'), ('j + i * 16', 'i * 16 + j'),
    ('if (!known) {', 'if (known == 0) {'), ('if (!g_030021CC) {', 'if (g_030021CC == 0) {'),
    ('if (i != 0)', 'if (i)'), ('if (j != 0)', 'if (j)'),
    ('model * 2]', '2 * model]'), ('j != i)', 'i != j)'),
    ('    s32 model;\n', '    int model;\n'), ('    s32 k;\n', '    int k;\n'), ('    s32 a;\n', '    int a;\n'),
    ('                    s32 x;\n                    s32 z;\n', '                    s32 z;\n                    s32 x;\n'),
    ('                    s32 xx;\n                    s32 zz;\n', '                    s32 zz;\n                    s32 xx;\n'),
    ('mask |= g_080202E4[i];', 'mask = mask | g_080202E4[i];'),
]


def pairs(code):
    for a, b in PAIRS:
        for x, y in ((a, b), (b, a)):
            start = 0
            while True:
                n = code.find(x, start)
                if n < 0:
                    break
                yield code[:n] + y + code[n + len(x):]
                start = n + 1


CACHE = {}


def neighbours(code, rng):
    if code in CACHE:
        out = list(CACHE[code])
        rng.shuffle(out)
        return out
    base_types = sorted(TYPES.findall(code))
    out = list(swaps(code)) + list(pairs(code))
    try:
        for i, c in enumerate(vs.mutations(code, rng)):
            if i >= 600:
                break
            if natural(c, base_types):
                out.append(c)
    except Exception:
        pass
    if len(CACHE) > 200:
        CACHE.clear()
    CACHE[code] = list(out)
    rng.shuffle(out)
    return out


def init_worker():
    global TABLE, ROM, WANT
    program = draft.Program()
    TABLE = reloc.symbols(program)
    ROM = program.rom
    WANT = program.rom[START - draft.BASE:END - draft.BASE]
    os.nice(5)


def evaluate(source):
    try:
        exact, size, _, expected, actual = judge.compile_candidate(
            source, NAME, START, START + 65536, TABLE, target_end=END, compiler='arm', rom=ROM)
        got = bytes.fromhex(actual)
        edits, diff = vs.score(WANT, got, START, mode='arm')
        return (diff, edits, abs(len(got) - len(WANT))), got == WANT
    except Exception as exc:
        return None, type(exc).__name__


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('source', type=Path)
    ap.add_argument('outdir', type=Path)
    ap.add_argument('--seconds', type=float, required=True)
    ap.add_argument('--jobs', type=int, default=6)
    ap.add_argument('--beam', type=int, default=6)
    ap.add_argument('--seed', type=int, default=1115)
    args = ap.parse_args()
    args.outdir.mkdir(parents=True, exist_ok=True)
    rng = random.Random(args.seed)
    deadline = time.monotonic() + args.seconds
    base = args.source.read_text()
    log = (args.outdir / 'log.jsonl').open('a')
    seen = set()
    with mp.Pool(args.jobs, initializer=init_worker) as pool:
        first = pool.map(evaluate, [base])[0]
        best = (first[0], base)
        elite = [best]
        print('start', first[0], flush=True)
        tried = 0
        stagnant = 0
        while time.monotonic() < deadline:
            batch = []
            for score, src in elite:
                for cand in neighbours(src, rng)[:60]:
                    h = hashlib.sha256(cand.encode()).hexdigest()
                    if h in seen:
                        continue
                    seen.add(h)
                    batch.append(cand)
            if stagnant >= 2:
                # multi-edit escape from the elite
                for score, src in elite:
                    s = src
                    for _ in range(3):
                        opts = neighbours(s, rng)
                        if not opts:
                            break
                        s = rng.choice(opts)
                        h = hashlib.sha256(s.encode()).hexdigest()
                        if h not in seen:
                            seen.add(h)
                            batch.append(s)
            if not batch:
                break
            rng.shuffle(batch)
            improved = False
            for lo in range(0, len(batch), args.jobs * 4):
                if time.monotonic() >= deadline:
                    break
                wave = batch[lo:lo + args.jobs * 4]
                for cand, (score, flag) in zip(wave, pool.map(evaluate, wave)):
                    tried += 1
                    if tried % 500 == 0:
                        print('progress tried', tried, 'best', best[0], flush=True)
                    if score is None:
                        continue
                    elite.append((score, cand))
                    if score < best[0]:
                        best = (score, cand)
                        improved = True
                        (args.outdir / 'best.c').write_text(cand)
                        log.write(json.dumps({'t': round(time.monotonic() - deadline + args.seconds, 1),
                                              'tried': tried, 'score': score, 'exact': flag}) + '\n')
                        log.flush()
                        print('best', score, 'tried', tried, flush=True)
                    if flag is True:
                        (args.outdir / 'exact.c').write_text(cand)
                        print('EXACT', flush=True)
                        return
            uniq = {}
            for e in sorted(elite, key=lambda e: e[0]):
                uniq.setdefault(e[1], e)
            elite = list(uniq.values())[:args.beam]
            stagnant = 0 if improved else stagnant + 1
        print('done tried', tried, 'best', best[0], flush=True)


if __name__ == '__main__':
    main()

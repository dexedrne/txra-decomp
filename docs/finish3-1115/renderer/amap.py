#!/usr/bin/env python3
"""Map each allocated pseudo of a candidate to the hard register the cartridge uses for the
same value (worker only, diagnostic).  python3 amap.py cand.c [--all] [--trace]
Compiles with -dp -dl -dg, aligns the candidate listing with the target by instruction shape,
and votes per pseudo over operand positions.  Prints global-alloc order (from the tracing cc1
when --trace) with refs/live and priority, flagging pseudos whose cartridge register differs."""
import re, sys, os, subprocess, tempfile, difflib, collections
from pathlib import Path
sys.path.insert(0, 'tools'); sys.path.insert(0, 'recomp')
import measure_candidate as mc, draft, reloc, diffhint, llm_match as match
START, END = 0x08016DA8, 0x08017E68
src = Path(sys.argv[1]).read_text()
prog = draft.Program(); table = reloc.symbols(prog)
want = prog.rom[START - match.BASE:END - match.BASE]
got, frame = mc.diagnostic_compile(src, 'func_%08X' % START, START, table, 'arm')
HN = {'lr': 14, 'sp': 13, 'pc': 15}
def hnum(t): return HN[t] if t in HN else int(t[1:])
def lst(data):
    out = []
    for line in diffhint.listing(data, START, 'arm'):
        a, rest = line.split(':', 1)
        if '.word' in rest: out.append((int(a, 16), None)); continue
        ins = re.split(r'\s{2,}', rest.strip(), maxsplit=1)[-1]
        ins = re.sub(r'@.*', '', ins).strip()
        out.append((int(a, 16), ins))
    return out
def norm(ins):
    if ins is None: return '.word'
    ins = re.sub(r'\b(r\d+|lr|sp|pc)\b', 'R', ins)
    return re.sub(r'0x080[0-9A-Fa-f]{5}', 'ADDR', ins)
T = lst(want); C = lst(got)
with tempfile.TemporaryDirectory(prefix='amap-', dir='build') as td:
    d = Path(td)
    code = src if 'typedef unsigned char u8;' in src else match.PRELUDE + src
    (d / 't.c').write_text(code)
    match.run([match.ARM + 'gcc', '-E', '-P', '-Isrc', d / 't.c', '-o', d / 't.i'])
    env = dict(os.environ, TXDBG='G')
    cc = os.path.expanduser('~/txra-renderer-cc/gcc_arm/cc1') if '--trace' in sys.argv else str(match.CC.with_name('agbcc_arm'))
    r = subprocess.run([cc, '-quiet', 't.i', '-O2', '-mthumb-interwork', '-dp', '-dl', '-dg', '-o', 't.s'],
                       cwd=d, capture_output=True, text=True, env=env, timeout=120)
    asm = (d / 't.s').read_text(); lreg = (d / 't.i.lreg').read_text(); greg = (d / 't.i.greg').read_text()
    gtrace = [l for l in r.stderr.splitlines() if l.startswith('GF ')]
# asm instruction uids in order
uids = []; cur = None; rem = 0
body = asm[asm.index('func_%08X:' % START):]
for line in body.splitlines()[1:]:
    if line.strip().startswith('.size'): break
    s = line.strip()
    if not s or s.startswith('.') or s.endswith(':') or s.startswith('@'): continue
    m = re.search(r'@ (\d+)\s.*\[length = (\d+)\]', line)
    if m:
        cur, rem = int(m.group(1)), int(m.group(2)) // 4 - 1
        uids.append(cur)
    elif rem > 0:
        rem -= 1; uids.append(cur)
    else:
        uids.append(None)
cins = [i for i, (a, ins) in enumerate(C) if ins is not None]
assert len(cins) == len(uids), (len(cins), len(uids))
uid_of = {ci: u for ci, u in zip(cins, uids)}
# pseudos per insn from lreg
pseudos = collections.defaultdict(set)
for m in re.finditer(r'(?ms)^\((?:insn|jump_insn|call_insn) (\d+) (.*?)(?=^\(|\Z)', lreg):
    for p in re.findall(r'\(reg(?:/[a-z])*:[A-Z]+ (\d+)\)', m.group(2)):
        if int(p) >= 27: pseudos[int(m.group(1))].add(int(p))
disp = {int(a): int(b) for a, b in re.findall(r'(\d+) in (\d+)', greg.split(';; Register dispositions:')[1].split('\n\n')[0])}
info = {int(a): (int(b), int(c)) for a, b, c in re.findall(r'Register (\d+) used (\d+) times across (\d+) insns', lreg)}
A = [norm(i) for _, i in T]; B = [norm(i) for _, i in C]
sm = difflib.SequenceMatcher(None, A, B, autojunk=False)
votes = collections.defaultdict(collections.Counter)
where = collections.defaultdict(list)
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag != 'equal': continue
    for k in range(i2 - i1):
        t = T[i1 + k]; c = C[j1 + k]
        if c[1] is None: continue
        u = uid_of.get(j1 + k)
        if u is None: continue
        tt = re.findall(r'\b(r\d+|lr|sp|pc)\b', t[1]); ct = re.findall(r'\b(r\d+|lr|sp|pc)\b', c[1])
        for p in pseudos.get(u, ()):
            h = disp.get(p)
            if h is None: continue
            for x, y in zip(ct, tt):
                if hnum(x) == h:
                    votes[p][hnum(y)] += 1
                    where[p].append(t[0])
order = []
for l in gtrace:
    m = re.match(r'GF reg=(\d+) .* best=(-?\d+) refs=(\d+) len=(-?\d+)', l)
    order.append((int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))))
def pri(refs, ln):
    import math
    return (int(math.log2(refs)) * refs / ln) if refs > 0 and ln > 0 else 0
seen = set()
print('global order: pseudo ours->cart  refs/len pri  votes  first-addr')
for idx, (p, best, refs, ln) in enumerate(order):
    seen.add(p)
    v = votes.get(p)
    top = v.most_common(1)[0][0] if v else None
    flag = '' if (v is None or top == best) else '  <<< MISMATCH'
    if v is None and '--all' not in sys.argv: continue
    print('%3d %5d r%-3s-> %-5s %3d/%-4d %.3f %s %s%s' % (idx, p, best, ('r%d' % top) if top is not None else '-', refs, ln,
          pri(refs, ln), dict(v) if v else {}, ('%08X' % min(where[p])) if where[p] else '', flag))
print('local/other pseudos with mismatching votes:')
for p, v in sorted(votes.items()):
    if p in seen: continue
    top = v.most_common(1)[0][0]
    if top != disp.get(p) or '--all' in sys.argv:
        print('  %5d r%-3s-> r%-3d %s %08X %s' % (p, disp.get(p), top, dict(v), min(where[p]), info.get(p)))

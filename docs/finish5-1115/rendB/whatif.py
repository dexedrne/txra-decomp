#!/usr/bin/env python3
"""What-if (diagnostic only, never for matching): force the sched1 order of the projection block.
    python3 whatif.py cand.c 'A>B C<D ...' [--sbs] [--keep DIR]
'A>B' moves insn uid A to just after uid B, 'A<B' to just before B (applied left to right on the
natural sched1 order). Compiles with the private cc1 (TXS1ORDER), prints the score and optionally
the sanitized loop side-by-side. Worker only."""
import os, re, sys, subprocess, tempfile, shutil
from pathlib import Path
sys.path.insert(0, 'tools'); sys.path.insert(0, 'recomp')
import measure_candidate as mc, draft, reloc, variant_search, llm_match as match
START, END = 0x08016DA8, 0x08017E68
CC1 = os.path.expanduser('~/rendB-cc/gcc_arm/cc1')
def natural(src):
    with tempfile.TemporaryDirectory(prefix='wi-', dir='build') as td:
        d = Path(td)
        (d / 't.c').write_text(src if 'typedef unsigned char u8;' in src else match.PRELUDE + src)
        match.run([match.ARM + 'gcc', '-E', '-P', '-Isrc', d / 't.c', '-o', d / 't.i'])
        subprocess.run([CC1, '-quiet', 't.i', '-O2', '-mthumb-interwork', '-dl', '-o', 't.s'], cwd=d, capture_output=True, timeout=120)
        t = (d / 't.i.lreg').read_text()
    i = t.index('(const_int 65536)'); s = t.rfind('(code_label', 0, i); e = t.find('(code_label', i)
    out = []
    for k, u in re.findall(r'(?m)^\((insn|jump_insn|call_insn) (\d+) ', t[s:e]):
        out.append(int(u))
        if k == 'jump_insn': break
    return out
def apply(order, spec):
    o = list(order)
    for m in spec.split():
        a, op, b = re.match(r'(\d+)([<>])(\d+)$', m).groups(); a, b = int(a), int(b)
        o.remove(a); k = o.index(b); o.insert(k + 1 if op == '>' else k, a)
    return o
def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    src = Path(args[0]).read_text(); spec = args[1] if len(args) > 1 else ''
    nat = natural(src); order = apply(nat, spec)
    wd = Path(tempfile.mkdtemp(prefix='wicc-', dir='build'))
    (wd / 'agbcc_arm').symlink_to(CC1)
    match.CC = wd / 'agbcc'
    os.environ['TXS1ORDER'] = ','.join(map(str, order))
    prog = draft.Program(); table = reloc.symbols(prog)
    want = prog.rom[START - match.BASE:END - match.BASE]
    try:
        got, frame = mc.diagnostic_compile(src, 'func_%08X' % START, START, table, 'arm')
    finally:
        shutil.rmtree(wd)
    dist, diff = variant_search.score(want, got, START, 'arm')
    print('order:', ' '.join(map(str, order[:60])))
    print('whatif diff=%d dist=%d len=%d frame=%s' % (diff, dist, len(got), frame))
    if '--sbs' in sys.argv:
        sbs(want, got, int(os.environ.get('LO', '08017338'), 16), int(os.environ.get('HI', '08017470'), 16))
def sbs(want, got, lo, hi):
    import difflib, diffhint
    def lst(data):
        out = []
        for line in diffhint.listing(data, START, 'arm'):
            a, rest = line.split(':', 1)
            ins = '.word <pool>' if '.word' in rest else re.sub(r'\[pc, #-?\d+\] @ =0x[0-9A-F]+', '[pc] =POOL', re.split(r'\s{2,}', rest.strip(), maxsplit=1)[-1])
            out.append((int(a, 16), ins))
        return out
    def norm(ins):
        ins = re.sub(r'\b(r\d+|sb|sl|fp|ip|lr|sp)\b', 'R', ins)
        return re.sub(r'0x080[0-9A-Fa-f]{5}', 'ADDR', ins).strip()
    T = lst(want); C = lst(got)
    sm = difflib.SequenceMatcher(None, [norm(i) for _, i in T], [norm(i) for _, i in C], autojunk=False)
    last = 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        for k in range(max(i2 - i1, j2 - j1)):
            tt = T[i1 + k] if i1 + k < i2 else None
            cc = C[j1 + k] if j1 + k < j2 else None
            if tt: last = tt[0]
            if not (lo <= last < hi): continue
            mark = '  ' if (tt and cc and tt[1] == cc[1]) else ('~ ' if tag == 'equal' else '! ')
            print('%s%-44s | %s' % (mark, ('%08X %s' % tt) if tt else '', ('%08X %s' % cc) if cc else ''))
if __name__ == '__main__':
    main()

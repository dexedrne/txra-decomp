#!/usr/bin/env python3
"""Projection-loop block view for a trace.sh output dir (worker only, diagnostic).
    python3 blk.py OUTDIR [--log] [--lq]
Prints the block that holds (const_int 65536): pre-sched1 insn order (combine dump),
sched1 order (sched dump) with each pseudo's final hard register (greg dispositions),
optionally the sched1 log of the block and the local-alloc qty lines (TXDBG=L)."""
import re, sys
from pathlib import Path
D = Path(sys.argv[1]) if __name__ == "__main__" and len(sys.argv) > 1 else None
HR = {0: 'r0', 1: 'r1', 2: 'r2', 3: 'r3', 4: 'r4', 5: 'r5', 6: 'r6', 7: 'r7', 8: 'r8', 9: 'sb', 10: 'sl',
      11: 'fp', 12: 'ip', 13: 'sp', 14: 'lr', 15: 'pc', 24: 'cc'}

def toplevel(text):
    out = []; i = 0; n = len(text)
    while True:
        m = re.compile(r'(?m)^\((insn|jump_insn|code_label|note|barrier|call_insn) ').search(text, i)
        if not m: break
        s = m.start(); depth = 0; j = s; instr = False
        while j < n:
            c = text[j]
            if instr:
                if c == '\\': j += 1
                elif c == '"': instr = False
            elif c == '"': instr = True
            elif c == '(': depth += 1
            elif c == ')':
                depth -= 1
                if depth == 0: break
            j += 1
        out.append(text[s:j + 1]); i = j + 1
    return out

def parse(path):
    t = Path(path).read_text()
    # only the function body dump (last occurrence of func if several passes) -- dumps hold one function
    return toplevel(t)

def uid(x):
    return int(x.split()[1])

def simp(x, disp=None):
    body = ' '.join(x.split())
    m = re.match(r'\((?:insn|jump_insn) \d+ \d+ \d+ (.*)\)$', body)
    if not m: return body[:100]
    b = m.group(1)
    b = re.sub(r' \d+ \{[^}]*\}.*$', '', b)
    b = re.sub(r' \(insn_list .*$', '', b); b = re.sub(r' \(expr_list:REG_.*$', '', b); b = re.sub(r' \(nil\)$', '', b)
    def reg(m):
        r = int(m.group(1))
        if r < 64 and r in HR and r < 32: return HR[r]
        s = 'p%d' % r
        if disp is not None and r in disp: s += '=' + HR.get(disp[r], str(disp[r]))
        return s
    b = re.sub(r'\(reg(?:/[a-z]+)*:[A-Z]+ (\d+)\)', reg, b)
    b = re.sub(r'\(symbol_ref(?:/[a-z]+)*:SI \("([^"]+)"\)\)', r'\1', b)
    b = re.sub(r'\(const_int (-?\d+)\)', r'\1', b)
    b = re.sub(r'\(mem(?:/[a-z]+)*:([A-Z]+) ', lambda m: '(mem' + ('' if m.group(1) == 'SI' else ':' + m.group(1)) + ' ', b)
    b = re.sub(r':SI\b', '', b)
    b = re.sub(r'\(set ', '(= ', b)
    return b

def disp_of(path):
    t = Path(path).read_text()
    i = t.rfind(';; Register dispositions:')
    d = {}
    if i < 0: return d
    seg = t[i:t.find('\n\n', i)]
    for a, b in re.findall(r'(\d+) in (\d+)', seg):
        d[int(a)] = int(b)
    return d

def block(items):
    k = next(i for i, x in enumerate(items) if '(const_int 65536)' in x)
    s = k
    while not items[s].startswith('(code_label'): s -= 1
    e = k
    while not items[e].startswith('(jump_insn'): e += 1
    return [x for x in items[s:e + 1] if x.startswith('(insn') or x.startswith('(jump_insn')]

pre = block(parse(D / 't.i.combine'))
post = block(parse(D / 't.i.sched'))
disp = disp_of(D / 't.i.greg')
print('== pre-sched1 order (combine) ==')
for x in pre: print('%5d %s' % (uid(x), simp(x)))
print('== sched1 order, final hard regs ==')
for x in post: print('%5d %s' % (uid(x), simp(x, disp)))
if '--log' in sys.argv:
    t = (D / 't.i.sched').read_text()
    first = uid(post[0])
    for L in t.split(';;\t -- basic block number')[1:]:
        hdr = L.split('\n', 1)[0]
        m = re.search(r'from (\d+) to (\d+)', hdr)
        ids = {uid(x) for x in pre}
        if m and (int(m.group(1)) in ids or int(m.group(2)) in ids):
            print('== sched1 log ==')
            print(L[:20000]); break
if '--lq' in sys.argv:
    tr = (D / 'trace.txt').read_text().splitlines()
    ids = {uid(x) for x in pre}
    bs = set()
    for ln in tr:
        m = re.match(r'LI b=(\d+) uid=(\d+) num=(\d+)', ln)
        if m and int(m.group(2)) in ids: bs.add(m.group(1))
    print('== local-alloc (blocks %s) ==' % ','.join(sorted(bs)))
    for ln in tr:
        m = re.match(r'(LI|LQ|FF) b=(\d+)', ln)
        if (m and m.group(2) in bs) or (ln.startswith('FF') and False):
            print(ln)

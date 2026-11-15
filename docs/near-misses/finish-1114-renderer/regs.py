#!/usr/bin/env python3
"""Report key pseudos (pts, scratch) stats from lreg/greg dumps: regs.py dumpdir name"""
import re, sys, glob
d, n = sys.argv[1], sys.argv[2]
lreg = open('%s/%s.i.lreg' % (d, n)).read()
greg = open('%s/%s.i.greg' % (d, n)).read()
disp = dict(re.findall(r'(\d+) in (\d+)', greg.split(';; Register dispositions:')[1].split(';;')[0]))
stats = {m.group(1): m.group(0) for m in re.finditer(r'Register (\d+) used (\d+) times across (\d+) insns[^\n]*', lreg)}
def find(pat):
    m = re.search(pat, lreg)
    return m.group(1) if m else None
pts = find(r'\(set \(reg/v:SI (\d+)\)\s+\(const_int 33554432')
scr = find(r'\(set \(reg:SI (\d+)\)\s+\(symbol_ref:SI \("g_030057A0"\)\)\)')
def pri(r):
    m = re.search(r'Register %s used (\d+) times across (\d+) insns' % r, lreg)
    if not m: return None
    import math
    u, l = int(m.group(1)), int(m.group(2))
    return round(int(math.log2(u)) * u / l, 3)
for name, r in (('pts', pts), ('scratch', scr)):
    print(name, r, 'hard', disp.get(r), 'pri', pri(r) if r else None, '|', stats.get(r, '')[:90])

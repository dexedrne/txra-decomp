#!/usr/bin/env python3
"""Locality of the projection loop's long-lived values (tx, s = sin*dz, ty, dy/w) for many candidates
(our own sources, private cc1 -dl; worker only).  python3 roles.py a.c b.c ...
Prints, per candidate, each role's pseudo and whether local-alloc may take it (local) or not."""
import os, re, sys, subprocess, tempfile
from multiprocessing import Pool
from pathlib import Path
sys.path.insert(0, 'tools'); sys.path.insert(0, 'recomp')
import llm_match as match
CC1 = os.path.expanduser('~/rendB-cc/gcc_arm/cc1')
def info(path):
    src = Path(path).read_text()
    with tempfile.TemporaryDirectory(prefix='ro-', dir='build') as td:
        d = Path(td)
        (d / 't.c').write_text(src if 'typedef unsigned char u8;' in src else match.PRELUDE + src)
        match.run([match.ARM + 'gcc', '-E', '-P', '-Isrc', d / 't.c', '-o', d / 't.i'])
        subprocess.run([CC1, '-quiet', 't.i', '-O2', '-mthumb-interwork', '-dl', '-o', 't.s'], cwd=d, capture_output=True, timeout=120)
        t = (d / 't.i.lreg').read_text()
    i = t.index('(const_int 65536)'); s = t.rfind('(code_label', 0, i); e = t.find('(code_label', i)
    ins = []
    for m in re.finditer(r'(?ms)^\((insn|jump_insn) (\d+) \d+ \d+ (.*?)(?=^\(|\Z)', t[s:e]):
        b = ' '.join(m.group(3).split()).replace('/v', '').replace(':SI', '')
        b = re.sub(r'\(expr_list.*$|\(insn_list.*$', '', b)
        ins.append(b)
    regline = {int(m.group(1)): m.group(0) for m in re.finditer(r'(?m)^Register (\d+) used .*$', t)}
    def setters(r): return [b for b in ins if b.startswith('(set (reg %d) ' % r)]
    def users(r): return [b for b in ins if re.search(r'\(reg %d\)' % r, b) and not b.startswith('(set (reg %d) ' % r)]
    out = {}
    for b in ins:
        m = re.match(r'\(set \(reg (\d+)\) \(ashift \(reg (\d+)\) \(const_int 3\)\)\)', b)
        if not m: continue
        X = int(m.group(2))
        # which path: follow product then shift 16 or 15
        prod = [int(x) for x in re.findall(r'\(set \(reg (\d+)\) \(mult \(reg \d+\) \(reg %s\)\)\)' % m.group(1), ' '.join(ins))]
        kind = '?'
        for p in prod:
            if re.search(r'\(ashiftrt \(reg %d\) \(const_int 16\)\)' % p, ' '.join(ins)): kind = 'x'
            if re.search(r'\(ashiftrt \(reg %d\) \(const_int 15\)\)' % p, ' '.join(ins)): kind = 'y'
        for b2 in setters(X):
            mm = re.search(r'\(plus \(ashiftrt \(reg (\d+)\) \(const_int 12\)\)', b2)
            if mm: out['t' + kind] = int(mm.group(1))
    if 'tx' in out:
        for b2 in setters(out['tx']):
            mm = re.match(r'\(set \(reg \d+\) \(minus \(reg \d+\) \(reg (\d+)\)\)', b2)
            if mm: out['s'] = int(mm.group(1))
    # dy/w: the reg stored to g_030055F8 (mem plus) whose value later shifts by 1
    for b in ins:
        mm = re.match(r'\(set \(reg (\d+)\) \(ashiftrt \(reg (\d+)\) \(const_int 1\)\)\)', b)
        if mm: out['w'] = int(mm.group(2))
    res = []
    for k in ('tx', 's', 'ty', 'w'):
        r = out.get(k)
        if r is None: res.append('%s=?' % k); continue
        L = regline.get(r, '')
        loc = 'block' in L and 'dies in' not in L
        dz = re.search(r'dies in (\d+)', L)
        res.append('%s=%d:%s%s' % (k, r, 'L' if loc else 'G', ('d' + dz.group(1)) if dz else ''))
    return path, ' '.join(res)
if __name__ == '__main__':
    with Pool(8) as p:
        for path, r in p.imap(info, sys.argv[1:]):
            print('%-40s %s' % (os.path.basename(path), r), flush=True)

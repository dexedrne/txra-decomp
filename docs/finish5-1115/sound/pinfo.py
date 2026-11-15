#!/usr/bin/env python3
"""Diagnostic (worker only): for pseudos of our own C, print the lreg summary line, the global
find_reg result from the private trace, and the RTL insns (compact) that mention each pseudo.
usage: pinfo.py <trace-dir> <pseudo>... [-n maxinsns]"""
import sys, re
d = sys.argv[1]; args = sys.argv[2:]; mx = 6
if '-n' in args:
    k = args.index('-n'); mx = int(args[k + 1]); del args[k:k + 2]
lreg = open(d + '/t.i.lreg').read()
greg = open(d + '/t.i.greg').read()
tr = open(d + '/trace.txt').read()
# split greg into insns
insns = re.findall(r'\n\((?:insn|jump_insn|call_insn) (\d+) .*?\n(?=\n|\(note|\(insn|\(jump|\(call|\(code|\(barrier)', greg, re.S)
blocks = re.split(r'\n(?=\((?:insn|jump_insn|call_insn) \d+ )', greg)
def compact(s):
    s = re.sub(r'\s+', ' ', s)
    s = re.sub(r'\(nil\)', '', s)
    s = re.sub(r':SI|:HI|:QI|/v|/u|/s|/f|/i', '', s)
    return s[:260]
for p in args:
    m = re.search(r'^Register %s used[^\n]*' % p, lreg, re.M)
    print('== %s  %s' % (p, m.group(0)[len('Register '):] if m else '(no lreg info)'))
    for g in re.findall(r'^G[FK] reg=%s [^\n]*' % p, tr, re.M): print('   ', g)
    n = 0
    for b in blocks:
        if re.search(r'\(reg(?:/[a-z])*:\w+ %s\b' % p, b) or re.search(r'\(reg(?:/[a-z])*:\w+ \d+ \w+\) ?;?', b) and False:
            pass
    # in greg, pseudos are replaced by hard regs; use lreg insns instead (pseudo numbers intact)
    for b in re.split(r'\n(?=\((?:insn|jump_insn|call_insn) \d+ )', lreg):
        if re.search(r'\(reg(?:/[a-z])*:\w+ %s\)' % p, b):
            hdr = re.match(r'\((\w+) (\d+)', b)
            body = re.sub(r'^\((\w+) (\d+) \d+ \d+ ', '', b)
            body = body.split('(expr_list')[0].split('(insn_list')[0]
            print('    %s %s' % (hdr.group(2) if hdr else '?', compact(body)))
            n += 1
            if n >= mx: break

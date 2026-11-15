#!/usr/bin/env python3
"""Compact listing of the RTL block containing a marker in a dump (worker only, our own source).
    python3 blk.py DUMP [marker] [--all]   (default marker '(const_int 65536)')"""
import re, sys
t = open(sys.argv[1]).read()
mk = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else '(const_int 65536)'
i = t.index(mk)
s = t.rfind('(code_label', 0, i); e = t.find('(code_label', i)
seg = t[s:e]
for m in re.finditer(r'(?ms)^\((insn|jump_insn|note|code_label|call_insn) (\d+) (.*?)(?=^\(|\Z)', seg):
    kind, uid, body = m.group(1), m.group(2), ' '.join(m.group(3).split())
    if kind == 'note':
        if 'NOTE_INSN_DELETED' in body and '--all' not in sys.argv: continue
        print('   note', body[-40:]); continue
    body = re.sub(r'^\d+ \d+ ', '', body)
    body = re.sub(r'\(expr_list:REG_(\w+) ', r'{\1 ', body)
    body = re.sub(r'\(insn_list(:REG_DEP_\w+)? (\d+) ', r'<\2 ', body)
    body = body.replace('(nil)', '').replace('/v', '').replace(':SI', '').replace('/u', '').replace('/s', '').replace('/i', '')
    print('%5s %s' % (uid, body[:260]))

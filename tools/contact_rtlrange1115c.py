#!/usr/bin/env python3
"""Diagnostic only: compact listing of a compiler RTL dump of OUR OWN C between
two insn uids (inclusive, in dump order).  contact_rtlrange1115c.py DUMP FROM TO"""
import re
import sys
text = open(sys.argv[1]).read()
lo, hi = sys.argv[2], sys.argv[3]
on = False
# use the last function body in the file (after the final ;; Function header)
for chunk in re.split(r'\n(?=\((?:insn|jump_insn|call_insn|note|code_label|barrier) )', text):
    m = re.match(r'\((insn|jump_insn|call_insn|note|code_label|barrier) (\d+) ', chunk)
    if not m:
        continue
    if m[2] == lo:
        on = True
    if on:
        body = re.sub(r'\s+', ' ', chunk)
        body = re.sub(r'^\((\w+) \d+ \d+ \d+ ', r'\1 ', body)
        print(m[2], body[:300])
    if m[2] == hi and on:
        break

#!/usr/bin/env python3
"""Diagnostic only: print compact RTL insns of a compiler dump of OUR OWN C that
mention the given pseudo registers.  contact_rtlgrep1115c.py DUMP REGNO..."""
import re
import sys
text = open(sys.argv[1]).read()
want = set(sys.argv[2:])
for chunk in re.split(r'\n(?=\((?:insn|jump_insn|call_insn|note|code_label|barrier) )', text):
    m = re.match(r'\((insn|jump_insn|call_insn) (\d+) ', chunk)
    if not m:
        continue
    body = re.sub(r'\s+', ' ', chunk)
    regs = set(re.findall(r'\(reg(?:/[a-z]+)*:\w+ (\d+)\)', body))
    if regs & want:
        body = re.sub(r'^\((?:insn|jump_insn|call_insn) \d+ \d+ \d+ ', '', body)
        print(m[2], body[:260])

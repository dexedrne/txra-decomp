#!/usr/bin/env python3
"""Sanitized side-by-side of the projection loop of 08016DA8 (worker only; mnemonics, no encodings or pool words).
    python3 sbsr.py cand.c [lo hi] [--diff]"""
import subprocess, sys
a = [x for x in sys.argv[1:] if not x.startswith('--')]
lo, hi = (a[1], a[2]) if len(a) > 2 else ('08017338', '08017470')
out = subprocess.run([sys.executable, 'docs/finish3-1115/renderer/sbs2.py', a[0], lo, hi], capture_output=True, text=True).stdout
for l in out.splitlines():
    if '--diff' in sys.argv and l.startswith('  '): continue
    print(l)

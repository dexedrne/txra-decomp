#!/usr/bin/env python3
"""Compile a trial with RTL dumps (-dl -dg -dj ...) into build/dump-<name>/ (compiler output only; run on a worker)."""
import sys, os, shutil
from pathlib import Path
sys.path.insert(0, 'tools'); sys.path.insert(0, 'recomp')
import llm_match as m
code = Path(sys.argv[1]).read_text()
flags = sys.argv[2:] or ['-dl', '-dg']
src = code if 'typedef unsigned char u8;' in code else m.PRELUDE + code
d = Path('build') / ('dump-' + Path(sys.argv[1]).stem)
shutil.rmtree(d, ignore_errors=True); d.mkdir(parents=True)
(d / 't.c').write_text(src)
m.run([m.ARM + 'gcc', '-E', '-P', '-Isrc', d / 't.c', '-o', d / 't.i'])
import subprocess
subprocess.run([str(m.CC), 't.i', '-O2', '-mthumb-interwork', *flags, '-o', 't.s'], cwd=d, check=True, capture_output=True, timeout=120)
print('\n'.join(sorted(os.listdir(d))))

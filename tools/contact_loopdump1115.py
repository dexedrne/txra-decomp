#!/usr/bin/env python3
"""Diagnostic only: compile a complete 080181C0 candidate with loop dumps.

Runs the historical ARM compiler with the unchanged `arm` profile flags
(-O2 -mthumb-interwork) plus -dL, keeps the assembly and loop dump of OUR OWN C
under build/contact-dump/<tag>/ on the worker, and prints the movable decisions
for every loop. Optional extra flags are for diagnosis only. It reads no ROM
bytes, writes no binary data and has no admission or installation authority.

  contact_loopdump1115.py SOURCE TAG [EXTRA_FLAG...]
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'recomp'))
import llm_match as match


def main():
    source, tag, extra = Path(sys.argv[1]), sys.argv[2], sys.argv[3:]
    out = Path('build/contact-dump') / tag
    out.mkdir(parents=True, exist_ok=True)
    code = source.read_text()
    (out / 'trial.c').write_text(code if 'typedef unsigned char u8;' in code else match.PRELUDE + code)
    match.run([match.ARM + 'gcc', '-E', '-P', '-Isrc', out / 'trial.c', '-o', out / 'trial.i'])
    match.run([match.CC.with_name('agbcc_arm'), 'trial.i', '-O2', '-mthumb-interwork', '-dL', '-dG', *extra,
               '-o', 'trial.s'], cwd=out)
    asm = (out / 'trial.s').read_text()
    frame = re.search(r'frame = (\d+)', asm)
    print('frame', frame[1] if frame else '?', 'asm lines', asm.count('\n'))
    dump = out / 'trial.i.loop'
    if not dump.exists():
        print('no loop dump'); return
    gcse = out / 'trial.i.gcse'
    pats = {}
    if gcse.exists():
        for chunk in re.split(r'\n(?=\()', gcse.read_text()):
            m = re.match(r'\((?:insn|jump_insn|call_insn) (\d+) ', chunk)
            if m:
                body = re.sub(r'\s+', ' ', chunk)
                body = re.sub(r'^\((?:insn|jump_insn|call_insn) \d+ \d+ \d+ ', '', body)
                pats[int(m[1])] = body[:150]
    for line in dump.read_text().splitlines():
        if line.startswith('Loop from') or line.startswith('Insn ') or 'is phony' in line:
            m = re.match(r'Insn (\d+): regno', line)
            if m and int(m[1]) in pats:
                line += '    || ' + pats[int(m[1])]
            print(line)


if __name__ == '__main__':
    main()

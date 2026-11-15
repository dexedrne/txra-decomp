#!/usr/bin/env python3
"""Diagnostic only: compact rotate-loop movable decisions (both loop passes)
for a complete 080181C0 candidate (our own C, unchanged arm flags + -dL).
Also reports whether the strength-reduced probe pointer's live length is
doubled.  No ROM bytes, no admission authority.

  contact_passes1115c.py SOURCE TAG
"""
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import llm_match as match


def short(body):
    m = re.search(r'REG_EQUAL (\(.*?\))\s*\(nil\)', body)
    eq = m[1] if m else ''
    eq = re.sub(r'symbol_ref:SI \("(\w+)"\)', r'\1', eq)
    eq = re.sub(r'(reg/v|reg):SI ', 'r', eq).replace('const_int ', '').replace('const:SI ', '')
    pat = re.sub(r'^\(set ', '', body)
    pat = re.sub(r'symbol_ref:SI \("(\w+)"\)', r'\1', pat)
    pat = re.sub(r'(reg/v|reg):SI ', 'r', pat).replace('const_int ', '').replace('mem/s:SI ', 'mem')
    pat = re.sub(r'\) \d+ \{.*', ')', pat)
    return (pat[:70] + ('  =' + eq[:50] if eq else ''))


def main():
    source, tag = Path(sys.argv[1]), sys.argv[2]
    out = Path('build/contact-passes') / tag
    out.mkdir(parents=True, exist_ok=True)
    code = source.read_text()
    (out / 'trial.c').write_text(code if 'typedef unsigned char u8;' in code else match.PRELUDE + code)
    match.run([match.ARM + 'gcc', '-E', '-P', '-Isrc', out / 'trial.c', '-o', out / 'trial.i'])
    cc = sys.argv[3] if len(sys.argv) > 3 else str(match.CC.with_name('agbcc_arm'))
    match.run([cc, 'trial.i', '-O2', '-mthumb-interwork', '-dL', '-o', 'trial.s'], cwd=out)
    dump = (out / 'trial.i.loop').read_text()
    # find insn bodies
    bodies = {}
    for chunk in re.split(r'\n(?=\()', dump):
        m = re.match(r'\((?:insn|jump_insn) (\d+) \d+ \d+ (.*)', chunk, re.S)
        if m:
            bodies[int(m[1])] = re.sub(r'\s+', ' ', m[2])
    loops = re.split(r'\n(?=\nLoop from )', dump.split('\n;; Function')[0] if False else dump)
    passno = {}
    for block in re.findall(r'Loop from (\d+) to (\d+): (\d+) real insns\.\n(.*?)(?=\nLoop from |\n\n\(|\Z)', dump, re.S):
        start, end, count, text = block
        if 'g_083D2280' not in text and 'g_083C2280' not in text and int(count) < 40:
            continue
        key = (start, end)
        if int(count) > 120:
            continue
        passno[key] = passno.get(key, 0) + 1
        print('== loop %s-%s pass %d: %s insns' % (start, end, passno[key], count))
        for line in text.splitlines():
            m = re.match(r'Insn (\d+): regno (\d+) \(life (\d+)\), (.*)', line)
            if not m:
                continue
            uid, regno, life, rest = m.groups()
            rest = re.sub(r'\s+moved to \d+', ' MOVED', rest).strip()
            print('  %5s r%-4s life %-3s %-40s %s' % (uid, regno, life, rest[:40], short(bodies.get(int(uid), ''))[:110]))
    asm = (out / 'trial.s').read_text()
    m = re.search(r'\tsubs\t(\w+), \1, #1\n\tadd\t(\w+), \2, #12\n\tbpl', asm)
    print('rotate loop: counter %s pointer %s' % (m[1], m[2]) if m else 'rotate loop shape not found')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Differential check of a natural-C renderer candidate against the textual ARM
executor from docs/near-misses/arm-16da8-1107/check_semantics.py.

The candidate source is compiled unchanged for i386 (32-bit pointers, so the
packet/bucket layouts match), linked freestanding, and run on the same synthetic
fixtures as the 11/7 checker. ROM-free; not a byte-match or gameplay test.
usage: check32.py candidate.c
"""
import hashlib, json, re, subprocess, sys, tempfile
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'docs/near-misses/arm-16da8-1107'))
import check_semantics as cs

def build(candidate, folder):
    src = Path(candidate).read_text()
    syms = sorted(set(re.findall(r'\bg_([0-9A-F]{8})\b', src)))
    flags = ['-m32', '-O1', '-fwrapv', '-fno-strict-aliasing', '-ffreestanding', '-fno-pic', '-fno-pie',
             '-fno-stack-protector', '-fno-asynchronous-unwind-tables', '-w']
    subprocess.run(['gcc', *flags, '-c', candidate, '-o', folder / 'cand.o'], check=True)
    subprocess.run(['gcc', *flags, '-c', HERE / 'harness32.c', '-o', folder / 'h.o'], check=True)
    exe = folder / 'h.elf'
    subprocess.run(['ld', '-m', 'elf_i386', '-static', '-nostdlib', '-Ttext=0x10000000', '-e', '_start',
                    *['--defsym=g_%s=0x%s' % (s, s) for s in syms], folder / 'h.o', folder / 'cand.o', '-o', exe], check=True)
    return exe

def compare(exe, memory, label):
    order = [0x02000000, 0x03000000, 0x07F00000]
    image = b''.join(bytes(memory.regions[b]) for b in order)
    arm = cs.Arm(memory)
    arm.run()
    out = subprocess.run([str(exe)], input=image, capture_output=True, check=True).stdout
    pos = 0
    for base in order:
        expected = bytes(memory.regions[base]); actual = out[pos:pos + len(expected)]; pos += len(expected)
        spans = [(0, 0x7D00), (0x7E00, len(expected))] if base == 0x03000000 else [(0, len(expected))]
        for lo, hi in spans:
            if actual[lo:hi] != expected[lo:hi]:
                i = next(i for i in range(lo, hi) if actual[i] != expected[i])
                raise AssertionError('%s: at %08x: C %02x, ARM %02x' % (label, base + i, actual[i], expected[i]))
    return arm.visited

def main():
    candidate = sys.argv[1]
    visited, count, failures = set(), 0, []
    with tempfile.TemporaryDirectory(prefix='txra-16da8-check32-') as folder:
        exe = build(candidate, Path(folder))
        cases = []
        for i in range(48):
            for mode in ('near', 'far', 'mixed'):
                cases.append(('%s-%d' % (mode, i), (i, mode), {}))
        for k in (1, 2, 3, 4, 9):
            for d in (-1, 0, 766, 767, 768, 0x7fffffff, 0x80000000):
                cases.append(('boundary-%d-%d' % (k, d), (700 + k, 'near'), {'depths': [d] * 4, 'kind': k}))
        for tick in (0, 5, 6, 28, 29, 31, 32, 0xffffffff):
            cases.append(('ring-%d' % tick, (99, 'mixed'), {'tick': tick}))
        for kind in (1, 2, 3, 4):
            for empty in (False, True):
                cases.append(('direct-insert-%d-%s' % (kind, empty), (123, 'far'),
                              {'kind': kind, 'depths': [1000] * 4, 'empty': empty,
                               'screen': ([10, 20, 20, 10], [10, 10, 20, 20])}))
        for mode in ('near', 'far'):
            for kind in (1, 3):
                cases.append(('two-faces-%s-%d' % (mode, kind), (123, mode),
                              {'kind': kind, 'faces': 2, 'depths': [767 if mode == 'near' else 1000] * 4,
                               'screen': ([10, 20, 20, 10], [10, 10, 20, 20])}))
        for label, args, kwargs in cases:
            try:
                visited.update(compare(exe, cs.fixture(*args, **kwargs), label))
            except AssertionError as e:
                failures.append(str(e))
            count += 1
    all_code = set(cs.Arm(cs.Memory()).code)
    print(json.dumps({'candidate': Path(candidate).name, 'differential_fixtures': count,
                      'failures': len(failures), 'first_failures': failures[:5],
                      'executed_instruction_addresses': len(visited), 'instruction_addresses': len(all_code),
                      'source_sha256': hashlib.sha256(Path(candidate).read_bytes()).hexdigest(),
                      'rom_used': False, 'byte_match_verified': False}, indent=2))
    sys.exit(1 if failures else 0)

if __name__ == '__main__':
    main()

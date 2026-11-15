#!/usr/bin/env python3
"""Compare a C trial with a mapped function; never writes original bytes.

Usage: python3 tools/diffhint.py 0801604C build/trial.c
The reusable hint() also supplies the retry feedback in the matching loop.
"""
import argparse
import difflib
import sys
import re
import struct
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'recomp'))
import draft


def listing(code, start, mode='thumb'):
    """Mark referenced pool words as data instead of decoding them as instructions."""
    if mode == 'arm':
        lines = []
        for offset in range(0, len(code) - 3, 4):
            word = struct.unpack_from('<I', code, offset)[0]
            address = start + offset
            asm, ir = draft.arm_ir(draft.generate.decode(word, False, address), address, word)[:2]
            if ir[0] == 'pool':
                asm += ' @ =0x%08X' % ir[2]
            lines.append('%08X: %08X  %s' % (address, word, asm))
    else:
        lines = draft.disassemble_thumb(code, start)
    pools = {int(m.group(1), 16) for line in lines
             for m in [re.search(r'@ =0x([0-9A-Fa-f]{8})', line)] if m}
    out = []
    for line in lines:
        address = int(line.split(':', 1)[0], 16)
        if mode == 'thumb' and address - 2 in pools:
            continue
        if address in pools and 0 <= address - start <= len(code) - 4:
            out.append('%08X: .word 0x%08X (literal pool)' % (address, struct.unpack_from('<I', code, address-start)[0]))
        else:
            out.append(line)
    return out


def mismatch_summary(want, got, start, mode='thumb'):
    """Localize byte changes without confusing a shifted listing with new behavior."""
    if want == got:
        return ['All bytes agree.']
    common = min(len(want), len(got))
    first = next((i for i in range(common) if want[i] != got[i]), common)
    suffix = 0
    while suffix < common-first and want[-1-suffix] == got[-1-suffix]:
        suffix += 1
    out = ['First difference at +0x%X (0x%08X); exact prefix %d bytes, exact suffix %d bytes.' %
           (first, start+first, first, suffix)]
    if len(want) != len(got):
        out.append('Length differs by %+d bytes; resolve missing/extra instructions or pools before allocation.' %
                   (len(got)-len(want)))
    def shape(data):
        result = []
        for line in listing(data, start, mode):
            if '.word ' in line:
                result.append(line.split('.word ', 1)[1])
            else:
                # Remove addresses, encodings and register numbers, retaining
                # immediates and branch destinations to avoid overclaiming.
                asm = re.split(r'\s{2,}', line, maxsplit=1)[-1]
                result.append(re.sub(r'\br(?:1[0-5]|[0-9])\b', 'REG', asm))
        return result
    if len(want) == len(got) and shape(want) == shape(got):
        out.append('Instruction shapes, constants and pools agree; inspect register allocation and variable lifetimes.')
    return out


def hint(want, got, start, rows=32, mode='thumb'):
    """Bounded instruction diff, including lengths, offsets and literal-pool changes."""
    a = listing(want, start, mode)
    b = listing(got, start, mode)
    result = ['Compiled output differs: target %d bytes, compiled %d bytes.' % (len(want), len(got)),
              *mismatch_summary(want, got, start, mode), '--- target', '+++ compiled']
    changes = list(difflib.unified_diff(a, b, n=2, lineterm=''))[2:]
    result.extend(changes[:rows])
    if len(changes) > rows:
        result.append('... %d further diff lines omitted' % (len(changes) - rows))
    if want == got:
        result.append('Exact byte match.')
    result.append('Check register allocation, signed widths, statement order, constants and pool alignment.')
    return '\n'.join(result)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('address', type=lambda s: int(s, 16))
    parser.add_argument('source', type=Path)
    parser.add_argument('--rows', type=int, default=32)
    parser.add_argument('--compiler', choices=('old', 'standard', 'old-no-gcse', 'old-o1', 'standard-o1',
                                               'old-no-interwork', 'arm', 'modern-arm'),
                        help='compiler profile; defaults to the installed profile, or old for an unmatched entry')
    args = parser.parse_args()
    import llm_match as m
    p = draft.Program()
    a = args.address
    if a not in p.by_start:
        parser.error('address must name a mapped function')
    mode = p.by_start[a]['mode']
    following = min((x for x in p.by_start if x > a), default=m.BASE + p.cfg['scan_end'])
    target_end = max(int(p.by_start[a]['end'], 16), max(draft.pool_words(p, a), default=a-4)+4)
    compiler = args.compiler or p.matched.get(a, {}).get('compiler', 'arm' if mode == 'arm' else 'old')
    if (compiler in ('arm', 'modern-arm')) != (mode == 'arm'):
        parser.error('compiler profile must match the mapped instruction mode')
    ok, size, _, expected, actual = m.compile_candidate(args.source.read_text(), 'func_%08X' % a, a, following, m.reloc.symbols(p), target_end=target_end, compiler=compiler)
    print(hint(bytes.fromhex(expected), bytes.fromhex(actual), a, args.rows, mode=mode))
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())

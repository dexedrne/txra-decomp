#!/usr/bin/env python3
"""Diagnostic only: compare a complete ARM owner with an extra compiler flag.

The installed `arm` profile is unchanged. This helper appends extra flags
(for example -fno-rerun-loop-opt) to the historical ARM compiler for a
measurement or for re-checking the installed ARM replacements. It has no
admission or installation authority and writes no binary data.

  diag_rerun1114.py measure SOURCE START END OUT FLAG...
  diag_rerun1114.py installed FLAG...
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'recomp'))
import draft
import reloc
import llm_match as match
import measure_candidate

INSTALLED_ARM = [('func_08017E68', 97896, 252), ('func_08018854', 100436, 512),
                 ('func_08016C18', 93208, 400), ('func_080165BC', 91580, 1628),
                 ('func_08017F64', 98148, 604), ('func_080076F4', 30452, 1076)]


def with_flags(extra):
    original = match.run

    def run(args, **kwargs):
        args = list(args)
        if args and str(args[0]).endswith('agbcc_arm'):
            args += extra
        return original(args, **kwargs)
    match.run = run


def main():
    mode = sys.argv[1]
    if mode == 'measure':
        source, start, end, out = sys.argv[2], int(sys.argv[3], 16), int(sys.argv[4], 16), sys.argv[5]
        extra = sys.argv[6:]
        with_flags(extra)
        result = measure_candidate.measure(source, start, end, 'arm', out)
        result['diagnostic_extra_flags'] = extra
        result['admissible'] = False
        Path(out).with_suffix('.json').write_text(json.dumps(result, indent=2) + '\n')
        print(json.dumps(result, indent=2))
    elif mode == 'installed':
        extra = sys.argv[2:]
        with_flags(extra)
        program = draft.Program()
        table = reloc.symbols(program)
        for name, offset, size in INSTALLED_ARM:
            code = (Path('src/generated') / (name + '.c')).read_text()
            start = match.BASE + offset
            try:
                exact = match.compile_candidate(code, name, start, start + size, table,
                                                target_end=start + size, compiler='arm',
                                                rom=program.rom)[0]
                print(name, ' '.join(extra) or '(profile flags)', 'exact' if exact else 'differs')
            except ValueError as exc:
                print(name, ' '.join(extra) or '(profile flags)', 'rejected:', exc)
    else:
        raise SystemExit(__doc__)


if __name__ == '__main__':
    main()

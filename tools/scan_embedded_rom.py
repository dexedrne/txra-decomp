#!/usr/bin/env python3
"""Count ROM bytes that a build output reproduces; prints counts only, never ROM content.

Executables and objects are searched for every WINDOW-byte run of the supplied ROM
(sliding by one byte inside each region of tools/rom.cfg). Runs with fewer than
--min-distinct byte values (padding, fills) are skipped and counted separately.
The generated C is checked separately: its raw instruction guard words and the
instruction words it decodes are attributed to the ROM region they come from.
"""
import argparse
import bisect
import hashlib
import json
from pathlib import Path
import re
import struct
import sys

BASE = 0x08000000
ROOT = Path(__file__).resolve().parent.parent


def load_map():
    cfg = json.loads((ROOT / 'tools/rom.cfg').read_text())
    mapping = sorted(cfg['mapping'], key=lambda m: m['offset'])
    return cfg, mapping


def region_of(starts, mapping, offset):
    i = bisect.bisect_right(starts, offset) - 1
    return mapping[i] if i >= 0 else None


def scan_binary(path, rom, mapping, window, min_distinct):
    blob = Path(path).read_bytes()
    index = {hash(blob[i:i + window]) for i in range(len(blob) - window + 1)}
    result = {'file': Path(path).name, 'size': len(blob), 'window': window,
              'data': {'windows_checked': 0, 'trivial_windows_skipped': 0, 'windows_found': 0,
                       'rom_bytes_covered': 0, 'by_type': {}, 'found_by_distinct_values': {}},
              'code': {'windows_checked': 0, 'trivial_windows_skipped': 0, 'windows_found': 0,
                       'rom_bytes_covered': 0}}
    for m in mapping:
        kind = 'code' if m['type'] == 'code' else 'data'
        bucket = result[kind]
        start, end = m['offset'], m['offset'] + m['size']
        covered = bytearray(m['size'])
        found = 0
        for at in range(start, end - window + 1):
            piece = rom[at:at + window]
            if len(set(piece)) < min_distinct:
                bucket['trivial_windows_skipped'] += 1
                continue
            bucket['windows_checked'] += 1
            if hash(piece) in index and piece in blob:
                found += 1
                if kind == 'data':
                    histogram = bucket['found_by_distinct_values']
                    histogram[len(set(piece))] = histogram.get(len(set(piece)), 0) + 1
                covered[at - start:at - start + window] = b'\1' * window
        if found:
            bucket['windows_found'] += found
            count = sum(covered)
            bucket['rom_bytes_covered'] += count
            if kind == 'data':
                key = f"{m['type']}/{m.get('format')}"
                bucket['by_type'][key] = bucket['by_type'].get(key, 0) + count
    return result


def entry_deltas():
    """Each generated function is a ROM span lifted at a run address (alias - start)."""
    functions = json.loads((ROOT / 'docs/map/functions.json').read_text())['functions']
    starts = {f['start'] for f in functions}
    functions += [f for f in json.loads((ROOT / 'recomp/observed.json').read_text())['functions']
                  if f['start'] not in starts]
    deltas = {}
    for f in functions:
        start, thumb = int(f['start'], 16), int(f['mode'] == 'thumb')
        deltas[start, thumb] = 0
        for alias in f['runtime_aliases']:
            deltas[int(alias['start'], 16), thumb] = int(alias['start'], 16) - start
    return deltas


def scan_generated(path, rom, mapping):
    """Attribute generated C instruction cases and raw guard words to ROM regions."""
    starts = [m['offset'] for m in mapping]
    deltas = entry_deltas()
    out = {'file': Path(path).name, 'instruction_cases': 0,
           'instruction_bytes': {'code': 0, 'data': 0, 'unattributed': 0},
           'data_instruction_bytes_by_type': {},
           'raw_guard_words': 0, 'raw_guard_bytes': {'code': 0, 'data': 0, 'mismatch': 0}}
    unique = {'code': set(), 'data': set()}
    entry = None
    for line in Path(path).read_text().splitlines():
        head = re.match(r'static __attribute__\(\(noinline\)\) void fn_([0-9a-f]{8})_([01])\(GBA\*g\)\{', line)
        if head:
            entry = (int(head.group(1), 16), int(head.group(2)))
            continue
        case = re.match(r'case (\d+)u: (?:if\(rd(16|32)\(g,(\d+)u\)!=(\d+)u\)return;)?', line)
        if not case or entry is None:
            continue
        width = 2 if entry[1] else 4
        delta = deltas.get(entry)
        offset = int(case.group(1)) - delta - BASE if delta is not None else None
        region = region_of(starts, mapping, offset) if offset is not None and 0 <= offset < len(rom) else None
        out['instruction_cases'] += 1
        if region is None:
            out['instruction_bytes']['unattributed'] += width
            kind = None
        else:
            kind = 'code' if region['type'] == 'code' else 'data'
            out['instruction_bytes'][kind] += width
            unique[kind].update(range(offset, offset + width))
            if kind == 'data':
                key = f"{region['type']}/{region.get('format')}"
                out['data_instruction_bytes_by_type'][key] = out['data_instruction_bytes_by_type'].get(key, 0) + width
        if case.group(2):
            size = int(case.group(2)) // 8
            out['raw_guard_words'] += 1
            same = kind is not None and \
                struct.unpack_from('<H' if size == 2 else '<I', rom, offset)[0] == int(case.group(4))
            out['raw_guard_bytes'][kind if same else 'mismatch'] += size
    out['unique_rom_bytes_lifted'] = {kind: len(offsets) for kind, offsets in unique.items()}
    return out


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('files', nargs='+', type=Path, help='executables/objects to search')
    p.add_argument('--rom', type=Path, default=ROOT / 'baserom.gba')
    p.add_argument('--generated', type=Path, help='also attribute build/generated.c')
    p.add_argument('--window', type=int, default=32)
    p.add_argument('--min-distinct', type=int, default=8)
    p.add_argument('--max-data-bytes', type=int, default=0,
                   help='fail when an executable reproduces more ROM data bytes than this')
    p.add_argument('--json', type=Path, help='write the counts here')
    a = p.parse_args()
    rom = a.rom.read_bytes()
    cfg, mapping = load_map()
    if hashlib.sha1(rom).hexdigest() != cfg['sha1']:
        p.error('Supply the supported ROM to compare against.')
    report = {'window': a.window, 'min_distinct': a.min_distinct,
              'rom_data_bytes': sum(m['size'] for m in mapping if m['type'] != 'code'),
              'rom_code_bytes': sum(m['size'] for m in mapping if m['type'] == 'code'),
              'files': [scan_binary(f, rom, mapping, a.window, a.min_distinct) for f in a.files]}
    if a.generated:
        report['generated'] = scan_generated(a.generated, rom, mapping)
    text = json.dumps(report, indent=1)
    if a.json:
        a.json.write_text(text + '\n')
    print(text)
    worst = max(f['data']['rom_bytes_covered'] for f in report['files'])
    if worst > a.max_data_bytes:
        print(f'FAIL: {worst} ROM data bytes reproduced (limit {a.max_data_bytes})', file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()

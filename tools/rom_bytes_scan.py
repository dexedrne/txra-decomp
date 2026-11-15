#!/usr/bin/env python3
"""Count player-ROM bytes embedded in build outputs, reporting counts and ROM offsets only.

Every 32-byte window of the ROM's non-code regions (graphics, sound, tables, text,
compressed and unclassified data from tools/rom.cfg; code and fill excluded) that is
non-trivial (at least 4 distinct byte values and no repeat period of 8 bytes or less)
is searched for, byte for byte, in each scanned file. Code regions are counted
separately. No ROM content is printed or written; run this where the ROM already is.
"""
import argparse
import array
import collections
import hashlib
import json
from pathlib import Path
import re

WINDOW = 32


def nontrivial(window):
    if len(set(window)) < 4:
        return False
    return not any(window[p:] == window[:-p] for p in range(1, 9))


def windows(rom, entries):
    """Offsets and region types of non-trivial windows lying fully inside one mapping entry."""
    kinds = sorted({e['type'] for e in entries})
    offsets, types = array.array('I'), bytearray()
    for e in entries:
        start, end = e['offset'], e['offset'] + e['size']
        for at in range(start, end - WINDOW + 1):
            if nontrivial(rom[at:at + WINDOW]):
                offsets.append(at)
                types.append(kinds.index(e['type']))
    return offsets, types, kinds


def scan(rom, regions, data):
    offsets, types, kinds = regions
    view = memoryview(data)
    present = {hash(view[i:i + WINDOW].tobytes()) for i in range(len(data) - WINDOW + 1)}
    candidates = [i for i, at in enumerate(offsets) if hash(rom[at:at + WINDOW]) in present]
    del present
    # Hash hits are confirmed byte for byte.
    matched = [i for i in candidates if data.find(rom[offsets[i]:offsets[i] + WINDOW]) >= 0]
    covered = bytearray(len(rom))
    by_kind = collections.Counter()
    for i in matched:
        covered[offsets[i]:offsets[i] + WINDOW] = b'\1' * WINDOW
        by_kind[kinds[types[i]]] += 1
    spans, run_start = [], None
    for i, v in enumerate(covered + b'\0'):
        if v and run_start is None:
            run_start = i
        elif not v and run_start is not None:
            spans.append((run_start, i - run_start))
            run_start = None
    return {
        'matched_windows': len(matched),
        'embedded_rom_bytes': sum(covered),
        'longest_embedded_run': max((n for _, n in spans), default=0),
        'embedded_spans': [{'rom_offset': f'0x{a:06x}', 'bytes': n} for a, n in spans[:20]],
        'matched_windows_by_type': dict(by_kind),
    }


def main():
    root = Path(__file__).resolve().parent.parent
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('files', nargs='+', type=Path)
    p.add_argument('--rom', type=Path, default=root / 'baserom.gba')
    p.add_argument('--json', type=Path, help='write the counts here as well')
    p.add_argument('--window', type=int, default=32, help='window length in bytes (default 32)')
    a = p.parse_args()
    global WINDOW
    WINDOW = a.window
    cfg = json.loads((root / 'tools/rom.cfg').read_text())
    rom = a.rom.read_bytes()
    if hashlib.sha1(rom).hexdigest() != cfg['sha1']:
        p.error('Supply the supported player ROM')
    data_entries = [e for e in cfg['mapping'] if e['type'] not in ('code', 'fill')]
    code_entries = [e for e in cfg['mapping'] if e['type'] == 'code']
    data_windows, code_windows = windows(rom, data_entries), windows(rom, code_entries)
    totals = {
        'window_bytes': WINDOW,
        'data_bytes_considered': sum(e['size'] for e in data_entries),
        'data_windows_nontrivial': len(data_windows[0]),
        'code_bytes_considered': sum(e['size'] for e in code_entries),
        'code_windows_nontrivial': len(code_windows[0]),
    }
    rule = __doc__.strip().split('\n\n')[1].replace('\n', ' ').replace('32-byte', f'{WINDOW}-byte')
    report = {'rule': rule, 'rom': totals, 'files': {}}
    for path in a.files:
        data = path.read_bytes()
        entry = {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
                 'data_regions': scan(rom, data_windows, data),
                 'code_regions': scan(rom, code_windows, data)}
        if path.suffix == '.c':
            # Self-modifying-code guards compare RAM-resident instruction words as C constants.
            guards = re.findall(r'if\(rd(16|32)\(g,\d+u\)!=\d+u\)return;', data.decode())
            entry['instruction_guard_constants'] = len(guards)
            entry['instruction_guard_bytes'] = sum(int(bits) // 8 for bits in guards)
        report['files'][path.name] = entry
    text = json.dumps(report, indent=1)
    print(text)
    if a.json:
        a.json.write_text(text + '\n')


if __name__ == '__main__':
    main()

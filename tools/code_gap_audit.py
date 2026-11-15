#!/usr/bin/env python3
"""Find unreferenced function candidates in gaps between established code.

This complements the pointer audit: unused leaf functions may have neither a
PUSH-LR prologue nor a ROM pointer. It does not accept seeds, alter mappings or
establish execution. Restrict the scan to the independently established program
enclosure; arbitrary data that happens to decode is not executable evidence.
"""
import argparse
import hashlib
import json
from pathlib import Path

from code_audit import validate_thumb


def scan(rom, cfg, splits, start=0x2000, end=0x18E8C):
    blocked = {p for s in splits if s['kind'] in {'literal', 'arm', 'thumb'}
             for p in range(int(s['start'], 16)-cfg['base'],
                            int(s['end'], 16)-cfg['base'])}
    proposals = []
    tested = 0
    for block in cfg['mapping']:
        if block['type'] != 'unknown' or block['size'] < 6:
            continue
        a, z = max(start, block['offset']), min(end, block['offset']+block['size'])
        a += a % 2
        for at in range(a, z, 2):
            word = int.from_bytes(rom[at:at+2], 'little')
            # Permit frameless leaves immediately after the usual zero aligner.
            edge = at == a or (at == a+2 and rom[a:a+2] == b'\0\0')
            prologue = word & 0xFE00 == 0xB400 or word & 0xFF80 == 0xB080
            if word == 0 or not (edge or prologue):
                continue
            tested += 1
            result = validate_thumb(rom, at, [{'kind': 'unreferenced-code-gap'}],
                                    blocked, budget=4096, base=cfg['base'])
            if result['valid']:
                proposals.append(dict(offset=at, mode='thumb', spans=result['spans'],
                                      return_sites=result['return_sites'],
                                      reason='unreferenced candidate; all paths decode; balanced return; ARMv4T',
                                      execution_verified=False))
    return dict(complete=False, tested=tested, candidates=proposals,
                scan_start=start, scan_end=end,
                caveat='Manual boundary, literal and semantic review required; no runtime reachability claimed.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    cfg = json.loads(Path('tools/rom.cfg').read_text())
    rom = Path('baserom.gba').read_bytes()
    assert len(rom) == cfg['size'] and hashlib.sha1(rom).hexdigest() == cfg['sha1']
    splits = json.loads(Path('docs/map/splits.json').read_text())['regions']
    result = scan(rom, cfg, splits)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print('%d candidates from %d gap entry checks' % (len(result['candidates']), result['tested']))


if __name__ == '__main__':
    main()

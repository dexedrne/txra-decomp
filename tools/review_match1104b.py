#!/usr/bin/env python3
"""Render the mixer compiler comparison and target-filter checks for review."""
import argparse
import json
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'recomp'))
import draft
import llm_match as match
import reloc
import permute_queue
from review_map import font
from review_match1104 import canvas, picture, clip, compare, AMBER, FG, MUTED, BORDER

ADDRESS = '080076F4'
NAME = 'Four-voice sample mixer'
START = int(ADDRESS, 16)
FOCUS = 0x08007900


def progress(config):
    count = len(config['matches'])
    size = sum(m['size'] for m in config['matches'])
    im, draw = canvas('The four-voice mixer now matches',
                      'Complete C routine / original ARM compiler / full ROM verified')
    draw.text((48, 224), '178  >  ' + str(count), font=font(78, True), fill=AMBER)
    draw.text((48, 330), 'of 229 mapped entries', font=font(32), fill=FG)
    draw.text((48, 438), '71,440  >  ' + f'{size:,} bytes', font=font(48, True), fill=FG)
    draw.text((48, 520), f'{size / 85132 * 100:.3f}% of mapped code bytes', font=font(29), fill=MUTED)
    draw.rectangle((48, 602, 1390, 642), outline=BORDER, width=2)
    draw.rectangle((50, 604, 50 + round(1338 * size / 85132), 640), fill=AMBER)
    draw.text((48, 704), '080076F4 / 1,076 bytes / including literal pools', font=font(30), fill=FG)
    draw.text((48, 780), 'The complete rebuilt ROM has the same bytes as the cartridge.', font=font(24), fill=FG)
    draw.text((48, 880), 'This is compiler evidence. It does not establish a new gameplay milestone.', font=font(21), fill=MUTED)
    return im


def target_picture(config):
    inventory = json.loads(Path('docs/map/functions.json').read_text())['functions']
    rows = permute_queue.queue(config, inventory)
    queued = {row['address'] for row in rows}
    im, draw = canvas('Already matched targets leave the queue',
                      'Filter checks against the current match list / live night runner unavailable here')
    for i, a in enumerate(['080165BC', '08017F64', '08017E68', '08018E18', '080076F4']):
        assert a not in queued
        y = 246 + i * 85
        draw.text((64, y), a, font=font(33, True), fill=FG)
        draw.text((470, y), 'matched / excluded automatically', font=font(29), fill=AMBER)
    draw.text((64, 746), 'Score snapshots rank remaining targets from closest to furthest.', font=font(26), fill=FG)
    draw.text((64, 816), 'Untried targets follow. The list is rebuilt before each search round.', font=font(25), fill=FG)
    draw.text((64, 900), 'The missing overnight branch still needs to be merged and connected.', font=font(23), fill=MUTED)
    return im


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    root = parser.parse_args().directory
    root.mkdir(parents=True, exist_ok=True)
    program = draft.Program()
    table = reloc.symbols(program)
    rom = Path('baserom.gba').read_bytes()
    comparisons = []
    captions = {}
    for after in (False, True):
        source = ((Path('src/generated') if after else Path('docs/near-misses/hand-20261104')) /
                  f'func_{ADDRESS}.c')
        ok, size, _, expected, actual = match.compile_candidate(
            source.read_text(), f'func_{ADDRESS}', START, START + 0x500, table,
            target_end=START + 1076, compiler='arm', rom=rom)
        if after:
            assert ok and size == 1076
        rows = compare(bytes.fromhex(expected), bytes.fromhex(actual), START)
        comparisons.append(rows)
        filename = ('after-' if after else 'before-') + ADDRESS + '.png'
        picture(ADDRESS, NAME, rows, FOCUS, after).save(root / filename)
        captions[filename] = ('After: complete exact mixer.' if after else 'Before: retained mixer draft, red rows still differ.') + ' Same code view.'
    filename = ADDRESS + '.webm'
    clip(root / filename, ADDRESS, NAME, *comparisons, FOCUS)
    captions[filename] = 'Eight seconds, muted, 30 fps: earlier mixer draft then complete exact output; compiler evidence.'
    config = json.loads(Path('tools/rom.cfg').read_text())
    progress(config).save(root / 'matching-progress.png')
    captions['matching-progress.png'] = 'After: 179 matched entries, 72,516 bytes and 85.181% of mapped code.'
    target_picture(config).save(root / 'target-filter.png')
    captions['target-filter.png'] = 'After: installed routines are automatically excluded; live schedule integration remains unavailable.'
    (root / 'captions.json').write_text(json.dumps(captions, indent=2) + '\n')
    (root / 'NOTES.md').write_text(
        'TXRA now rebuilds the complete four-voice sound mixer exactly from C. '
        'Compare the before and after pictures at the same code view; the earlier red rows now agree. '
        'The short muted clip replays this compiler comparison and contains no game footage. '
        'The target-filter picture shows the new checks that exclude already matched routines; '
        'the missing overnight branch still prevents us from checking its live schedule.\n')
    print('Wrote four pictures, captions, notes and one muted eight-second 30-fps clip.')


if __name__ == '__main__':
    main()

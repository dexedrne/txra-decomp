#!/usr/bin/env python3
"""Render deep slice j3 review pictures and one muted clip.

Usage: python3 tools/review_deep_j3.py <review-directory>
Listings compare the mapped original code with a trial compile of a retained
draft. The pictures are written outside the repository only.
"""
import argparse
import difflib
import re
import textwrap
import json
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'recomp'))
from review_map import font
import draft
import diffhint
import llm_match as m

BG = '#080e1a'
FG = '#f2e4c8'
MUTED = '#abb6cb'
AMBER = '#ffb12a'
LINE = '#354157'
RED = '#5a1f28'
GREEN = '#173a2a'
W, H = 1600, 1000
MAPPED = 85132
BEFORE = (147, 28714)

MATCHES = [
    ('0800B3A0', 'old', 'docs/deep-l/drafts/func_0800B3A0.c', 'old',
     'Point plot', 'Pixel value shared by both parity branches: two local quantities, not three.'),
    ('0800C850', 'old', 'docs/match10-search/0800C850/func_0800C850.c', 'old',
     'Track-position update', 'The dead add is an unused second wrap; record fields indexed directly.'),
    ('0800A940', 'old', 'docs/deep-a/candidates/0800A940.c', 'old',
     'Stat scaling', '2-D stats array, one product temporary, factors built in two statements.'),
    ('0800AC3C', 'old', 'docs/deep-g/drafts/func_0800AC3C.c', 'old',
     'Grade stat scaling', 'Same macro; grade read through p; the two level factors are two variables.'),
    ('0800A17C', 'old', 'docs/deep-a/candidates/0800A17C.c', 'old',
     'Race HUD bars', 'Record field 0x4c, next row first, bonus values held before their stores.'),
    ('0800C3C4', 'old', 'docs/deep-c/candidates/func_0800C3C4.c', 'old',
     'Steering and heading', 'Nested flag tests, one record pointer per block, one shared diff variable.'),
    ('08005238', 'old', 'docs/deep-a/candidates/08005238.c', 'old',
     'Menu sprite builder', '2-D column table so loop.c reduces i*2; slide + 120 placed by PRE.'),
]


def canvas(title, subtitle):
    im = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(im)
    d.text((55, 32), 'TXRA  /  DEEP MATCHING  /  SLICE J, THIRD PASS', font=font(22, True), fill=MUTED)
    d.text((55, 78), title, font=font(42, True), fill=FG)
    d.text((55, 140), subtitle, font=font(22), fill=MUTED)
    return im, d


def status(count, size, label):
    percent = 100 * size / MAPPED
    im, d = canvas('Exact C replacements', label + '  /  full ROM byte equality is required')
    d.text((60, 235), str(count), font=font(110, True), fill=AMBER)
    d.text((330, 275), 'matched functions', font=font(39, True), fill=FG)
    d.text((60, 410), f'{percent:.3f}% of mapped code', font=font(44, True), fill=FG)
    d.text((60, 485), f'{size:,} replacement bytes, including literal pools', font=font(27), fill=MUTED)
    d.rectangle((60, 560, 1535, 600), outline=LINE, width=2)
    d.rectangle((62, 562, 62 + int(1471 * percent / 100), 598), fill=AMBER)
    d.text((60, 625), f'Fixed denominator: {MAPPED:,} mapped code bytes', font=font(25), fill=MUTED)
    d.line((60, 705, 1535, 705), fill=LINE, width=2)
    d.text((60, 740), 'Only complete exact matches enter the build.', font=font(28, True), fill=FG)
    d.text((60, 795), 'No runtime boot or playability claim is made by this pass.', font=font(24), fill=MUTED)
    return im


def compiled(address, path, profile):
    p = draft.Program()
    start = int(address, 16)
    target_end = max(int(p.by_start[start]['end'], 16), max(draft.pool_words(p, start), default=start - 4) + 4)
    ok, _, _, expected, actual = m.compile_candidate(Path(path).read_text(), 'func_' + address, start,
                                                     start + 0x2000, m.reloc.symbols(p),
                                                     target_end=target_end, compiler=profile)
    return ok, bytes.fromhex(expected), bytes.fromhex(actual), start


def norm(line):
    text = line.split(':', 1)[-1].strip()
    parts = text.split(None, 1)
    text = parts[1] if len(parts) > 1 and all(c in '0123456789ABCDEF' for c in parts[0]) else text
    text = re.sub(r'\[pc, #\d+\] @ =0x[0-9A-F]+', '=pool', text)
    text = re.sub(r'0x0[0-9A-F]{7}', 'label', text)
    return text


def rows(want, got, start):
    """Align the two listings on instruction text so a length change does not paint every later row."""
    left = diffhint.listing(want, start)
    right = diffhint.listing(got, start)
    sm = difflib.SequenceMatcher(None, [norm(x) for x in left], [norm(x) for x in right], autojunk=False)
    out = []
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            out += [(left[i], right[j], left[i].split(':', 1)[-1] == right[j].split(':', 1)[-1])
                    for i, j in zip(range(i1, i2), range(j1, j2))]
        else:
            a, b = left[i1:i2], right[j1:j2]
            n = max(len(a), len(b))
            out += [(x, y, False) for x, y in zip(a + [''] * (n - len(a)), b + [''] * (n - len(b)))]
    return out


def listing_frame(title, subtitle, table, top, count=31):
    im, d = canvas(title, subtitle)
    d.text((60, 190), 'original', font=font(22, True), fill=AMBER)
    d.text((820, 190), 'our compile', font=font(22, True), fill=AMBER)
    y = 228
    for left, right, same in table[top:top + count]:
        d.rectangle((55, y - 2, 1545, y + 20), fill=GREEN if same else RED)
        d.text((60, y), left[:58], font=font(17), fill=FG)
        d.text((820, y), right[:58], font=font(17), fill=FG)
        y += 22
    differing = sum(1 for _, _, same in table if not same)
    d.text((60, 990 - 30), f'{differing} of {len(table)} rows differ  /  green = same instruction, red = different',
           font=font(20), fill=MUTED)
    return im


FOCUS = {0x0800B3A0: 0x0800B45E, 0x0800C850: 0x0800C870}

IMPROVED = [('0800841C', None, 'docs/deep-j3/drafts/func_0800841C.c', 'Palette fade by tile'),
            ('0800BDC0', 'docs/deep-a/candidates/0800BDC0.c', 'docs/deep-j3/drafts/func_0800BDC0.c',
             'AI lane choice')]


def window(table, address=None):
    if address is not None and int(address, 16) in FOCUS:
        return next((i for i, (left, _, _) in enumerate(table)
                     if left and int(left.split(':')[0], 16) >= FOCUS[int(address, 16)]), 0)
    first = next((i for i, (_, _, same) in enumerate(table) if not same), 0)
    return max(0, first - 4)


def findings():
    im, d = canvas('What made each function match', 'Source shapes found from the compiler dumps; existing old profile, no flags')
    y = 205
    for address, profile, _, _, name, why in MATCHES:
        d.text((60, y), address, font=font(30, True), fill=AMBER)
        d.text((260, y), name + f'  ({profile})', font=font(28, True), fill=FG)
        d.text((260, y + 42), why, font=font(22), fill=MUTED)
        y += 98
    return im


def outcomes(table):
    groups = {}
    for row in table:
        groups.setdefault(row['group'], []).append(row['address'])
    im, d = canvas('Slice j3: all 41 entries accounted for', 'Details per entry are in LOG.md')
    y = 220
    for name, entries in groups.items():
        d.text((60, y), f'{len(entries):2d}', font=font(46, True), fill=AMBER)
        d.text((150, y + 4), name, font=font(30, True), fill=FG)
        lines = textwrap.wrap(', '.join(entries), 100, break_long_words=False)
        for k, text in enumerate(lines):
            d.text((150, y + 50 + 28 * k), text, font=font(19), fill=MUTED)
        y += 95 + 28 * (len(lines) - 1)
    return im


def clip(path, before_table, after_table, title):
    frames = []
    top = window(before_table)
    for i in range(120):
        frames.append(listing_frame(title, 'Before: deep-a draft (red rows differ)',
                                    before_table, min(top + i // 12, max(0, len(before_table) - 31))))
    for i in range(120):
        frames.append(listing_frame(title, 'After: the installed source (exact)',
                                    after_table, min(top + i // 12, max(0, len(after_table) - 31))))
    enc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pixel_format', 'rgb24',
                            '-video_size', f'{W}x{H}', '-framerate', '30', '-i', '-', '-an',
                            '-c:v', 'libvpx-vp9', '-threads', '2', '-b:v', '900k', '-crf', '38',
                            '-r', '30', str(path)], stdin=subprocess.PIPE)
    for frame in frames:
        enc.stdin.write(frame.tobytes())
    enc.stdin.close()
    if enc.wait():
        raise RuntimeError('ffmpeg failed')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('directory', type=Path)
    args = ap.parse_args()
    root = args.directory
    (root / 'before').mkdir(parents=True, exist_ok=True)
    (root / 'after').mkdir(parents=True, exist_ok=True)
    cfg = json.loads(Path('tools/rom.cfg').read_text())
    count, size = len(cfg['matches']), sum(x['size'] for x in cfg['matches'])
    status(*BEFORE, 'Before slice j3').save(root / 'before' / 'matching-status.png')
    status(count, size, 'After slice j3').save(root / 'after' / 'matching-status.png')
    caps = {'before': {'matching-status.png': f'Before: {BEFORE[0]} functions, {100 * BEFORE[1] / MAPPED:.3f}% of mapped code.'},
            'after': {'matching-status.png': f'After: {count} functions, {100 * size / MAPPED:.3f}% of mapped code.'}}
    tables = {}
    for address, profile, before_src, before_profile, name, _ in MATCHES:
        source = next(x['source'] for x in cfg['matches'] if x['name'] == 'func_' + address)
        ok, want, got, start = compiled(address, source, profile)
        if not ok:
            raise RuntimeError(address + ' no longer matches')
        after_table = rows(want, got, start)
        tables[address] = after_table
        listing_frame(f'{address}  {name}  /  after', 'Installed source: every row agrees',
                      after_table, window(after_table, address)).save(root / 'after' / f'{address}-listing.png')
        caps['after'][f'{address}-listing.png'] = f'After: {name} ({address}), original left, our compile right, all rows green.'
        if before_src:
            _, want, got, start = compiled(address, before_src, before_profile)
            table = rows(want, got, start)
            tables[address + '-before'] = table
            listing_frame(f'{address}  {name}  /  before', 'Previous best draft: red rows differ',
                          table, window(table, address)).save(root / 'before' / f'{address}-listing.png')
            caps['before'][f'{address}-listing.png'] = f'Before: {name} ({address}) previous draft, original left, our compile right; red rows differ.'
    for address, before_src, after_src, name in IMPROVED:
        if before_src is None:
            _, want, got, start = compiled(address, after_src, 'old')
            table = rows(want, got, start)
            listing_frame(f'{address}  {name}  /  new draft', 'Not matched yet: the remaining red rows',
                          table, window(table, address)).save(root / 'after' / f'{address}-listing.png')
            caps['after'][f'{address}-listing.png'] = f'After: {name} ({address}) new draft, still unmatched; the red rows are what is left.'
            continue
        _, want, got, start = compiled(address, before_src, 'old')
        table = rows(want, got, start)
        listing_frame(f'{address}  {name}  /  before', 'Earlier draft: red rows differ',
                      table, window(table, address)).save(root / 'before' / f'{address}-listing.png')
        caps['before'][f'{address}-listing.png'] = f'Before: {name} ({address}) earlier draft, original left, our compile right; red rows differ.'
        _, want, got, start = compiled(address, after_src, 'old')
        table = rows(want, got, start)
        listing_frame(f'{address}  {name}  /  improved draft', 'Not matched yet: the remaining red rows',
                      table, window(table, address)).save(root / 'after' / f'{address}-listing.png')
        caps['after'][f'{address}-listing.png'] = f'After: {name} ({address}) improved draft, still unmatched; the red rows are what is left.'
    findings().save(root / 'matching-findings.png')
    outcome_rows = json.loads(Path('docs/deep-j3/outcomes.json').read_text())
    outcomes(outcome_rows).save(root / 'slice-outcomes.png')
    clip(root / '08005238-menu.webm', tables['08005238-before'], tables['08005238'],
         '08005238  menu sprite builder')
    top = {'matching-findings.png': 'What made each of the seven routines match, one line each.',
           'slice-outcomes.png': 'All 41 entries of this slice grouped by outcome.',
           '08005238-menu.webm': '8 s muted clip: the menu sprite builder listing from the earlier draft (red rows), then the installed source (all green).'}
    for name, data in (('before', caps['before']), ('after', caps['after']), ('.', top)):
        (root / name / 'captions.json').write_text(json.dumps(data, indent=1) + '\n')


if __name__ == '__main__':
    main()

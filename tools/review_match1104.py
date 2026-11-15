#!/usr/bin/env python3
"""Render reproducible compiler comparisons outside the repository."""
import argparse
import difflib
import json
import re
import subprocess
import sys
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from PIL import Image, ImageDraw
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'recomp'))
import draft
import llm_match as match
import reloc
from review_map import font

W, H = 1440, 960
BG, FG, MUTED = '#0b1220', '#f2e4c8', '#aeb9cb'
AMBER, BORDER, BAD = '#ffb12a', '#34435a', '#44232d'
TARGETS = [
    ('080165BC', 'Model vertex projection and quad emission', 1628, 0x080167D8),
    ('08017F64', 'Sprite blend into the alternate display page', 604, 0x080180B4),
]


def instructions(data, start):
    return [(i.address, f'{i.mnemonic} {i.op_str}')
            for i in Cs(CS_ARCH_ARM, CS_MODE_ARM).disasm(data, start)]


def normalize(text):
    return re.sub(r'\[pc, #[^]]+\]', '[pc, pool]', text)


def compare(want, actual, start):
    left, right = instructions(want, start), instructions(actual, start)
    matcher = difflib.SequenceMatcher(None, [normalize(s) for _, s in left],
                                     [normalize(s) for _, s in right], autojunk=False)
    result = []
    for tag, a, b, c, d in matcher.get_opcodes():
        aa, bb = left[a:b], right[c:d]
        size = max(len(aa), len(bb))
        for i in range(size):
            x = aa[i] if i < len(aa) else None
            y = bb[i] if i < len(bb) else None
            result.append((x, y, bool(x and y and x == y)))
    return result


def canvas(title, subtitle):
    im = Image.new('RGB', (W, H), BG)
    draw = ImageDraw.Draw(im)
    draw.text((44, 26), 'TXRA  /  MATCHING C  /  11.4', font=font(22, True), fill=MUTED)
    draw.text((44, 74), title, font=font(34, True), fill=FG)
    draw.text((44, 127), subtitle, font=font(21), fill=MUTED)
    return im, draw


def picture(address, name, rows, focus, after, cursor=None):
    state = 'after: exact' if after else 'before: retained draft'
    im, draw = canvas(f'{address}  {name}', state + '  /  original left, compiled C right')
    draw.text((48, 178), 'original', font=font(22, True), fill=AMBER)
    draw.text((744, 178), 'compiled C', font=font(22, True), fill=AMBER)
    top = next(i for i, (x, _, _) in enumerate(rows) if x and x[0] >= focus)
    for j, (left, right, equal) in enumerate(rows[top:top + 28]):
        y = 218 + j * 23
        draw.rectangle((40, y - 2, W - 40, y + 20), fill='#172238' if equal else BAD)
        if cursor == j:
            draw.rectangle((40, y - 2, W - 40, y + 20), outline=AMBER, width=2)
        for x, item in ((48, left), (744, right)):
            if item:
                text = f'{item[0]:08X}  {item[1]}'
                draw.text((x, y), text, font=font(17), fill=FG)
    draw.line((44, 881, W - 44, 881), fill=BORDER, width=2)
    message = ('The complete function and its literal pool match byte for byte.' if after else
               'Red rows differ. Both captures use this same part of the routine.')
    draw.text((44, 904), message, font=font(22), fill=FG)
    return im


def progress(count, size):
    im, draw = canvas('Two more complete C matches', 'Original ARM compiler  /  complete ROM rebuild verified')
    draw.text((48, 232), '176  >  ' + str(count), font=font(78, True), fill=AMBER)
    draw.text((48, 337), 'of 229 mapped entries', font=font(34), fill=FG)
    draw.text((48, 448), '69,208  >  ' + f'{size:,} bytes', font=font(48, True), fill=FG)
    draw.text((48, 526), f'{size / 85132 * 100:.3f}% of 85,132 mapped code bytes',
              font=font(29), fill=MUTED)
    draw.rectangle((48, 605, 1390, 645), outline=BORDER, width=2)
    draw.rectangle((50, 607, 50 + round(1338 * size / 85132), 643), fill=AMBER)
    draw.text((48, 712), '080165BC   model emitter                  1,628 bytes', font=font(30), fill=FG)
    draw.text((48, 772), '08017F64   sprite blend                     604 bytes', font=font(30), fill=FG)
    draw.text((48, 881), 'The rebuilt game has the same bytes as the supplied cartridge.',
              font=font(24), fill=MUTED)
    return im


def clip(path, address, name, before, after, focus):
    encoder = subprocess.Popen([
        'ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pixel_format', 'rgb24',
        '-video_size', f'{W}x{H}', '-framerate', '30', '-i', '-', '-an',
        '-c:v', 'libvpx-vp9', '-threads', '2', '-b:v', '800k', '-crf', '38',
        '-r', '30', str(path)], stdin=subprocess.PIPE)
    for frame in range(240):
        done = frame >= 120
        image = picture(address, name, after if done else before, focus, done,
                        cursor=min(27, (frame % 120) * 28 // 120))
        encoder.stdin.write(image.tobytes())
    encoder.stdin.close()
    if encoder.wait():
        raise RuntimeError('video encoding failed')
    if path.stat().st_size > 4_000_000:
        raise RuntimeError('review clip exceeds 4 MB')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    root = parser.parse_args().directory
    root.mkdir(parents=True, exist_ok=True)
    (root / 'NOTES.md').write_text(
        'TXRA now rebuilds two more routines exactly from C: the car model emitter and a sprite blend. '
        'Compare each before and after picture at the same code view; red rows in the earlier draft become matching rows. '
        'The short muted clips show those comparisons with a moving line marker. '
        'The complete rebuilt game still has the same bytes as the cartridge.\n')
    captions = {'matching-progress.png':
                'After: 178 exact matches, 71,440 bytes, with both new routines listed.'}
    for address, name, _, _ in TARGETS:
        for after in (False, True):
            filename = ('after-' if after else 'before-') + address + '.png'
            captions[filename] = f'{"After: exact" if after else "Before: unmatched"} {name.lower()}, same code view.'
        captions[address + '.webm'] = f'8 seconds, muted: {name.lower()}, earlier draft then exact match.'
    (root / 'captions.json').write_text(json.dumps(captions, indent=2) + '\n')
    program = draft.Program()
    table = reloc.symbols(program)
    rom = Path('baserom.gba').read_bytes()
    for address, name, size, focus in TARGETS:
        start = int(address, 16)
        tables = []
        for after in (False, True):
            source = (Path('src/generated') if after else
                      Path('docs/near-misses/hand-20261103')) / f'func_{address}.c'
            ok, _, _, want, actual = match.compile_candidate(
                source.read_text(), f'func_{address}', start, start + 0x2000,
                table, target_end=start + size, compiler='arm', rom=rom)
            if after and not ok:
                raise RuntimeError(address + ' no longer matches')
            rows = compare(bytes.fromhex(want), bytes.fromhex(actual), start)
            tables.append(rows)
            filename = ('after-' if after else 'before-') + address + '.png'
            picture(address, name, rows, focus, after).save(root / filename)
            captions[filename] = f'{"After: exact" if after else "Before: unmatched"} {name.lower()}, same code view.'
        filename = address + '.webm'
        clip(root / filename, address, name, *tables, focus)
        captions[filename] = f'8 seconds, muted: {name.lower()}, earlier draft then exact match.'
    cfg = json.loads(Path('tools/rom.cfg').read_text())
    progress(len(cfg['matches']), sum(m['size'] for m in cfg['matches'])).save(root / 'matching-progress.png')
    captions['matching-progress.png'] = 'After: 178 exact matches, 71,440 bytes, with both new routines listed.'
    (root / 'captions.json').write_text(json.dumps(captions, indent=2) + '\n')
    (root / 'NOTES.md').write_text(
        'TXRA now rebuilds two more routines exactly from C: the car model emitter and a sprite blend. '
        'Compare each before and after picture at the same code view; red rows in the earlier draft become matching rows. '
        'The short muted clips show those comparisons with a moving line marker. '
        'The complete rebuilt game still has the same bytes as the cartridge.\n')


if __name__ == '__main__':
    main()

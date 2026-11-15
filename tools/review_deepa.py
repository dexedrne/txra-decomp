#!/usr/bin/env python3
"""Render accepted matching metadata and a short muted progress replay."""
import argparse
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw
from review_map import font

W, H = 1440, 1000
BG, FG, MUTED, AMBER, GRID = '#101827', '#f5ead3', '#b6bfce', '#ffb12a', '#344258'
MATCHES = [
    ('080164D0', 'Coordinate transform', 236),
    ('08017E68', 'ARM queue dispatcher', 252),
    ('0801533C', 'Palette and sprite submission', 368),
    ('0800C9C4', 'Row interpolation', 408),
    ('0800237C', 'Eight-octant line renderer', 386),
    ('08018854', 'ARM startup copies', 512),
    ('080157A0', 'Character mapping switch', 1162),
]


def canvas(title, subtitle):
    im = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(im)
    d.text((60, 36), 'TXRA / DEEP HAND MATCHING / SLICE A', font=font(22, True), fill=MUTED)
    d.text((60, 89), title, font=font(42, True), fill=FG)
    d.text((60, 156), subtitle, font=font(23), fill=MUTED)
    return im, d


def notes(folder, text, captions):
    folder.mkdir(parents=True, exist_ok=True)
    (folder / 'NOTES.md').write_text(text + '\n')
    (folder / 'captions.json').write_text(json.dumps(captions, indent=2) + '\n')


def status(data, label, denominator):
    im, d = canvas('Accepted C replacements', 'Same view and same mapped-code denominator before and after')
    d.text((65, 270), label, font=font(38, True), fill=MUTED)
    d.text((65, 355), f"{data['count']} functions", font=font(76, True), fill=FG)
    d.text((65, 475), f"{data['bytes_including_pools'] * 100 / denominator:.3f}% of mapped code", font=font(55, True), fill=AMBER)
    d.text((65, 590), f"{data['bytes_including_pools']:,} bytes, including literal pools", font=font(32), fill=FG)
    d.rectangle((65, 700, 1370, 762), fill=GRID)
    d.rectangle((65, 700, 65 + int(1305 * data['bytes_including_pools'] / denominator), 762), fill=AMBER)
    d.text((65, 825), f'{denominator:,} mapped bytes / Only complete byte equality counts', font=font(25), fill=MUTED)
    d.text((65, 885), 'Code recovery evidence; gameplay and boot status are unverified.', font=font(25), fill=MUTED)
    return im


def results(before, denominator, accepted=7):
    im, d = canvas('Seven exact replacements', 'Accepted code recovery replay / Compiler metadata only')
    total = before['bytes_including_pools'] + sum(row[2] for row in MATCHES[:accepted])
    d.text((60, 235), f"{before['count']} → {before['count'] + accepted} functions", font=font(38, True), fill=FG)
    d.text((800, 235), f'{total * 100 / denominator:.3f}% mapped', font=font(38, True), fill=AMBER)
    d.line((60, 320, 1380, 320), fill=GRID, width=2)
    for x, text in [(60, 'ENTRY'), (330, 'RECOVERED ROUTINE'), (1170, 'BYTES')]:
        d.text((x, 346), text, font=font(22, True), fill=MUTED)
    for i, (address, name, size) in enumerate(MATCHES):
        y = 407 + i * 62
        active = i < accepted
        color = FG if active else GRID
        d.text((60, y), address, font=font(27, True), fill=AMBER if active else GRID)
        d.text((330, y), name, font=font(27), fill=color)
        d.text((1170, y), str(size) if active else 'pending', font=font(27), fill=color)
    d.text((60, 885), 'Each accepted routine passed a full rebuild and whole-ROM equality.', font=font(25), fill=MUTED)
    d.text((60, 935), 'Unfinished drafts and assembly exclusions are listed in outcomes.md.', font=font(24), fill=MUTED)
    return im


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('directory', type=Path)
    args = ap.parse_args()
    root = args.directory
    before = json.loads((root / 'baseline.json').read_text())
    current = json.loads(Path('progress.json').read_text())
    b, a = before['functions_matched_c'], current['functions_matched_c']
    denominator = current['code_bytes_mapped']
    assert a['count'] == b['count'] + len(MATCHES)
    assert a['bytes_including_pools'] == b['bytes_including_pools'] + sum(row[2] for row in MATCHES)
    for label, data in [('before', b), ('after', a)]:
        folder = root / label
        notes(folder, f'TXRA exact code recovery totals {label} this pass. Compare the same view in the other folder to see the change. These numbers describe recovered code, and do not establish that the game runs.', {'status.png': f'{label.capitalize()}: accepted replacement totals using the same mapped bytes.'})
        status(data, label.capitalize(), denominator).save(folder / 'status.png')
    results(b, denominator).save(root / 'results.png')
    path = root / 'matching-progress.webm'
    encoder = subprocess.Popen([
        'ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pixel_format', 'rgb24',
        '-video_size', f'{W}x{H}', '-framerate', '30', '-i', '-', '-an',
        '-c:v', 'libvpx-vp9', '-threads', '2', '-b:v', '1000k', '-crf', '36', '-r', '30', str(path),
    ], stdin=subprocess.PIPE)
    frames = [results(b, denominator, i).tobytes() for i in range(8)]
    for frame in range(180):
        encoder.stdin.write(frames[min(7, frame // 21)])
    encoder.stdin.close()
    if encoder.wait():
        raise RuntimeError('Review video encoding failed')
    if path.stat().st_size > 4_000_000:
        raise RuntimeError('Review video exceeds size limit')
    notes(root, 'TXRA deep hand matching, slice a, recovered seven complete C routines. Compare before/ and after/ for accepted totals, then use the results picture to identify each routine. The short muted clip replays accepted code recovery; it is a metadata animation, with no game footage. The running table records all forty assigned entries, including unfinished work and assembly boundaries. Gameplay and boot are still unverified.', {
        'results.png': 'After: seven exact replacements, their purpose and their full byte counts.',
        'matching-progress.webm': 'Six-second muted metadata replay of seven accepted replacements, 30 fps.',
    })


if __name__ == '__main__':
    main()

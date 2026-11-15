#!/usr/bin/env python3
"""Render matching metadata for deep slice b; no ROM content is read."""
import argparse
import json
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw
from review_map import font

BG = '#080e1a'
FG = '#f2e4c8'
MUTED = '#abb6cb'
AMBER = '#ffb12a'
LINE = '#354157'
W, H = 1440, 900


def canvas(title, subtitle):
    im = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(im)
    d.text((55, 35), 'TXRA / DEEP MATCHING / SLICE B', font=font(23, True), fill=MUTED)
    d.text((55, 90), title, font=font(43, True), fill=FG)
    d.text((55, 155), subtitle, font=font(23), fill=MUTED)
    return im, d


def status(count, size, percent, label):
    im, d = canvas('Exact C replacements', label + ' / Full ROM byte equality is required')
    d.text((60, 245), str(count), font=font(110, True), fill=AMBER)
    d.text((310, 283), 'matched functions', font=font(39, True), fill=FG)
    d.text((60, 420), f'{percent:.3f}% of mapped code', font=font(44, True), fill=FG)
    d.text((60, 495), f'{size:,} replacement bytes, including literal pools', font=font(27), fill=MUTED)
    d.rectangle((60, 570, 1375, 610), outline=LINE, width=2)
    d.rectangle((62, 572, 62 + int(1311 * percent / 100), 608), fill=AMBER)
    d.text((60, 635), 'Fixed denominator: 85,132 mapped code bytes', font=font(25), fill=MUTED)
    d.line((60, 715, 1375, 715), fill=LINE, width=2)
    d.text((60, 752), 'Only complete exact matches enter the build.', font=font(28, True), fill=FG)
    d.text((60, 805), 'Runtime boot and playability have not been established by this pass.', font=font(24), fill=MUTED)
    return im


def categories(outcomes):
    counts = {'Exact C': 0, 'Unmatched C': 0, 'Boundary / ABI recovery': 0, 'Assembly / private renderer': 0}
    for row in outcomes.values():
        result = row['outcome']
        if result.startswith('exact:'):
            counts['Exact C'] += 1
        elif result.startswith('unmatched:'):
            counts['Unmatched C'] += 1
        elif result.startswith(('boundary', 'ABI/')):
            counts['Boundary / ABI recovery'] += 1
        else:
            counts['Assembly / private renderer'] += 1
    return counts


def outcomes_picture(outcomes):
    im, d = canvas('Forty assigned entries reviewed', 'One exact match / Full outcomes in LOG.md')
    for i, (name, count) in enumerate(categories(outcomes).items()):
        y = 245 + i * 110
        d.text((60, y), name, font=font(29, True), fill=FG)
        d.rectangle((650, y + 2, 1250, y + 38), outline=LINE, width=2)
        if count:
            d.rectangle((652, y + 4, 652 + int(596 * count / 40), y + 36), fill=AMBER)
        d.text((1290, y - 3), str(count), font=font(34, True), fill=AMBER)
    d.line((60, 704, 1375, 704), fill=LINE, width=2)
    d.text((60, 735), 'New match: the 94-byte runtime copy routine.', font=font(28, True), fill=FG)
    d.text((60, 784), 'Separate library compiler settings reproduce its exact return.', font=font(25), fill=MUTED)
    d.text((60, 831), 'Closer drafts remain unfinished and stay outside the build.', font=font(24), fill=MUTED)
    return im


def notes(directory, text, captions):
    directory.mkdir(parents=True, exist_ok=True)
    (directory / 'NOTES.md').write_text(text + '\n')
    (directory / 'captions.json').write_text(json.dumps(captions, indent=2) + '\n')


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('directory', type=Path)
    args = ap.parse_args()
    root = args.directory
    outcomes = json.loads(Path('docs/deep-b/outcomes.json').read_text())
    current = json.loads(Path('progress.json').read_text())['functions_matched_c']
    before = status(109, 10698, 12.566, 'Before')
    after = status(current['count'], current['bytes_including_pools'], current['percent_of_mapped_code'], 'After')
    notes(root, 'This is TXRA’s original-build matching work, slice b. One more function now reproduces the original build exactly. Compare before/ and after/; LOG.md explains the entries that remain unfinished. The short clip replays the matching totals.', {
        'outcomes.png': 'After: outcomes for all forty entries assigned to slice b.',
        'matching-review.webm': 'Six-second matching-totals replay at 30 fps, without audio.'})
    notes(root / 'before', 'TXRA matching totals before this slice. Compare the same view in after/ to see the one added exact match.', {'status.png': 'Before: 109 exact C functions, covering 12.566% of mapped code.'})
    notes(root / 'after', 'TXRA matching totals after this slice. The added runtime copy routine reproduces all 94 bytes and the full rebuilt ROM remains identical.', {'status.png': 'After: 110 exact C functions, covering 12.677% of mapped code.'})
    before.save(root / 'before/status.png')
    after.save(root / 'after/status.png')
    outcomes_picture(outcomes).save(root / 'outcomes.png')
    frames = Path('build/deep-b/review-frames')
    frames.mkdir(parents=True, exist_ok=True)
    for i in range(180):
        frame = (before if i < 90 else after).copy()
        d = ImageDraw.Draw(frame)
        d.rectangle((60, 875, 60 + int(1315 * (i + 1) / 180), 883), fill=AMBER)
        frame.resize((1152, 720), Image.Resampling.LANCZOS).save(frames / f'{i:03d}.png')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-framerate', '30', '-i', str(frames / '%03d.png'),
                    '-an', '-c:v', 'libvpx-vp9', '-threads', '2', '-b:v', '450k', '-pix_fmt', 'yuv420p',
                    str(root / 'matching-review.webm')], check=True)


if __name__ == '__main__':
    main()

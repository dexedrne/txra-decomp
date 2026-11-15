#!/usr/bin/env python3
"""Render matching counts over committed batch times; reads only our metadata."""
import argparse
import datetime as dt
import json
import math
from pathlib import Path
import subprocess
from review_map import base, font, FG, MUTED, COLORS
from review_match2 import summary


def git(*args):
    return subprocess.check_output(['git', *args], text=True)


def snapshot(revision, timestamp):
    cfg = json.loads(git('show', revision + ':tools/rom.cfg'))
    return {'time': timestamp, 'functions': len(cfg['matches']),
            'bytes': sum(m['size'] for m in cfg['matches'])}


def chart(records, key, title, dest):
    times = [dt.datetime.fromisoformat(r['time']).timestamp() for r in records]
    elapsed = max(1, times[-1] - times[0])
    im, d = base(title, 'Accepted build batches at their commit times / metadata from our matching tools')
    left, right, top, bottom = 150, 1460, 285, 790
    values = [r[key] for r in records]
    ceiling = math.ceil(max(values) / (20 if key == 'functions' else 2000)) * (20 if key == 'functions' else 2000)
    for n in range(5):
        value = ceiling * n / 4
        y = bottom - int((bottom - top) * n / 4)
        d.line((left, y, right, y), fill='#344258', width=2)
        d.text((25, y - 14), f'{value:,.0f}', font=font(23), fill=MUTED)
    points = [(left + int((t - times[0]) / elapsed * (right - left)),
               bottom - int(v / ceiling * (bottom - top))) for t, v in zip(times, values)]
    steps = [points[0]]
    for previous, point in zip(points, points[1:]): steps += [(point[0], previous[1]), point]
    d.line(steps, fill=COLORS['code'], width=6)
    for x, y in points: d.ellipse((x-6, y-6, x+6, y+6), fill=FG)
    for index in (0, len(records)-1):
        x, y = points[index]
        d.text((max(left, min(x-55, right-160)), y-50), f'{values[index]:,}', font=font(30, True), fill=FG)
    d.text((left, bottom+28), dt.datetime.fromisoformat(records[0]['time']).strftime('%m-%d %H:%M UTC'), font=font(22), fill=MUTED)
    d.text((right-270, bottom+28), dt.datetime.fromisoformat(records[-1]['time']).strftime('%m-%d %H:%M UTC'), font=font(22), fill=MUTED)
    d.text((80, 900), 'Steps are verified batches saved in version history, not measurements of matching speed.', font=font(24), fill=MUTED)
    d.text((80, 945), 'Byte totals include literal pools and in-function alignment. No private ROM content is shown.', font=font(22), fill=MUTED)
    im.save(dest)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--baseline', required=True, help='revision immediately before this matching pass')
    parser.add_argument('--target-additions', type=int, help='show an unmet matching target honestly in review notes')
    args = parser.parse_args()
    root = args.directory
    root.mkdir(parents=True, exist_ok=True)
    stamp = lambda rev: git('show', '-s', '--format=%cI', rev).strip()
    rows = [snapshot(args.baseline, stamp(args.baseline))]
    for rev in git('log', '--reverse', '--format=%H', args.baseline+'..HEAD', '--', 'tools/rom.cfg').splitlines():
        row = snapshot(rev, stamp(rev))
        if (row['functions'], row['bytes']) != (rows[-1]['functions'], rows[-1]['bytes']): rows.append(row)
    cfg = json.loads(Path('tools/rom.cfg').read_text())
    progress = json.loads(Path('progress.json').read_text())
    matches = cfg['matches']
    before = rows[0]['functions']
    if rows[-1]['functions'] != len(matches):
        raise ValueError('commit accepted matches before recording their batch times')
    for row in rows:
        row['time'] = dt.datetime.fromisoformat(row['time']).astimezone(dt.timezone.utc).isoformat()
    added = len(matches) - before
    totals = [sum(m['size'] for m in matches[:n]) for n in range(before, len(matches)+1)]
    for folder, count, size, label in [('before', before, totals[0], 'Before this matching pass'),
                                      ('after', len(matches), totals[-1], 'After this matching pass')]:
        target = root/folder
        target.mkdir(exist_ok=True)
        summary(count, size, progress['code_bytes_mapped'], label).save(target/'matching-status.png')
        (target/'NOTES.md').write_text('TXRA matching progress from our tools. Compare before/ and after/ from the same view. The byte total includes compiler literal pools.\n')
        (target/'captions.json').write_text(json.dumps({'matching-status.png': label+'; verified function and byte totals.'}, indent=2)+'\n')
    chart(rows, 'functions', 'Matched functions over time', root/'matched-functions.png')
    chart(rows, 'bytes', 'Matched bytes over time', root/'matched-bytes.png')
    encoder = subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pixel_format','rgb24',
        '-video_size','1600x1000','-framerate','30','-i','-','-an','-c:v','libvpx-vp9',
        '-threads','2','-b:v','700k','-crf','36','-r','30',str(root/'matching-progress.webm')], stdin=subprocess.PIPE)
    for frame in range(180):
        k = min(added, int(frame * (added+1) / 180))
        im = summary(before+k, totals[k], progress['code_bytes_mapped'], 'Accepted replacement milestones')
        encoder.stdin.write(im.tobytes())
    encoder.stdin.close()
    if encoder.wait(): raise RuntimeError('clip encoding failed')
    if (root/'matching-progress.webm').stat().st_size > 4000000: raise RuntimeError('clip exceeds review limit')
    (root/'batch-history.json').write_text(json.dumps(rows, indent=2)+'\n')
    pending = ''
    if args.target_additions is not None and added < args.target_additions:
        pending = f' The requested {args.target_additions} additions are unfinished; {args.target_additions-added} remain.'
    (root/'NOTES.md').write_text(f'TXRA now rebuilds {added} more complete functions from ordinary C. Compare before/ and after/ for the same-view totals; the two charts show accepted batches at their recorded commit times. The muted six-second clip walks through the accepted replacements using only our tool output. Every installed replacement passed a complete ROM identity check.{pending}\n')
    (root/'captions.json').write_text(json.dumps({
        'matched-functions.png': f'Before and after: {before} to {len(matches)} matched functions, at accepted batch times.',
        'matched-bytes.png': f'Before and after: {totals[0]:,} to {totals[-1]:,} matched bytes, including pools.',
        'matching-progress.webm': 'Six-second muted walkthrough of accepted matching milestones, 30 fps; metadata only.'}, indent=2)+'\n')
    print(f'Rendered {added} new matches, four pictures and a muted progress clip.')


if __name__ == '__main__': main()

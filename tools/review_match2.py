#!/usr/bin/env python3
"""Render matching metadata and a muted progress clip. Never reads ROM contents."""
import argparse
import json
from pathlib import Path
import subprocess
from review_map import base, font, FG, MUTED, COLORS


def summary(count, size, mapped, label):
    im, d = base('Matching ordinary C to the original', label + ' / exact compiler comparisons and full ROM verification')
    for y, title, value in [(265, 'Functions matched', str(count)),
                             (455, 'Matched bytes, including literal pools', f'{size:,}'),
                             (645, 'Share of mapped instruction bytes', f'{100*size/mapped:.3f}%')]:
        d.text((80,y), title, font=font(29), fill=MUTED)
        d.text((80,y+45), value, font=font(68, True), fill=FG)
    d.text((80,860),'Pool bytes are included: the percentage is an approximate code-coverage measure.', font=font(24), fill=MUTED)
    d.text((80,915),'Private ROM contents and game images are excluded from this review.', font=font(24), fill=MUTED)
    return im


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    args = parser.parse_args()
    root = args.directory; root.mkdir(parents=True, exist_ok=True)
    cfg = json.loads(Path('tools/rom.cfg').read_text())
    progress = json.loads(Path('progress.json').read_text())
    matches = cfg['matches']; before_count = 25
    if len(matches) != 55: raise ValueError('this review expects thirty additions to the twenty-five baseline matches')
    totals = [sum(m['size'] for m in matches[:n]) for n in range(25, 56)]
    if totals[0] != 582: raise ValueError('baseline matches differ')
    mapped = progress['code_bytes_mapped']
    for folder, index, label in [('before', 0, 'Before this matching pass'), ('after', 30, 'After thirty additional matches')]:
        dest = root/folder; dest.mkdir(exist_ok=True)
        summary(25+index, totals[index], mapped, label).save(dest/'matching-status.png')
        (dest/'NOTES.md').write_text('TXRA C matching progress. Compare before/ and after/ from the same view; the totals include literal pools. Every added replacement passed a complete ROM identity check.\n')
        (dest/'captions.json').write_text(json.dumps({'matching-status.png':label+'; matching totals from our tools only.'},indent=2)+'\n')
    im, d = base('Matched percentage through this session', 'One point per accepted replacement; horizontal axis is work order, not elapsed minutes')
    left, right, top, bottom = 140, 1450, 245, 810
    for percent in range(4):
        y = bottom-int(percent/3*(bottom-top))
        d.line((left,y,right,y),fill='#344258',width=2)
        d.text((50,y-14),f'{percent}%',font=font(23),fill=MUTED)
    points=[(left+int(k/30*(right-left)),bottom-int(size/mapped*100/3*(bottom-top))) for k,size in enumerate(totals)]
    d.line(points,fill=COLORS['code'],width=6)
    for x,y in points:d.ellipse((x-4,y-4,x+4,y+4),fill=FG)
    for k,label in [(0,'Start'),(10,'+10'),(20,'+20'),(30,'+30 matches')]:
        d.text((left+int(k/30*(right-left))-40,bottom+24),label,font=font(23),fill=MUTED)
    d.text((left,top-58),f'{totals[0]/mapped*100:.3f}%  to  {totals[-1]/mapped*100:.3f}%',font=font(30,True),fill=FG)
    d.text((70,925),'Matched function spans include pools; denominator: 85,132 mapped instruction bytes.',font=font(25),fill=MUTED)
    im.save(root/'matched-percent.png')
    chart, d = base('Bytes rebuilt from ordinary C', 'Exact accepted spans, including compiler literal pools and in-function alignment')
    for y,label,size in [(290,'Before: 25 functions',totals[0]),(570,'After: 55 functions',totals[-1])]:
        d.text((80,y-60),label,font=font(32,True),fill=FG)
        width=int(size/totals[-1]*1150)
        d.rectangle((80,y,80+width,y+82),fill=COLORS['code'])
        d.text((80,y+105),f'{size:,} bytes',font=font(36,True),fill=FG)
    d.text((80,835),f'+{totals[-1]-totals[0]:,} bytes / thirty new functions / complete ROM remains byte-identical',font=font(27),fill=FG)
    d.text((80,915),'Calls, globals, input polling, bounds checks, byte loops and transfer setup.',font=font(25),fill=MUTED)
    chart.save(root/'matched-bytes.png')
    encoder=subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pixel_format','rgb24',
        '-video_size','1600x1000','-framerate','30','-i','-','-an','-c:v','libvpx-vp9',
        '-threads','2','-b:v','700k','-crf','36','-r','30',str(root/'matching-progress.webm')],stdin=subprocess.PIPE)
    for frame in range(180):
        k = min(30, frame//5)
        picture=summary(25+k,totals[k],mapped,'Accepted replacement milestones')
        encoder.stdin.write(picture.tobytes())
    encoder.stdin.close()
    if encoder.wait():raise RuntimeError('clip encoder failed')
    if (root/'matching-progress.webm').stat().st_size>4000000:raise RuntimeError('clip exceeds review limit')
    (root/'NOTES.md').write_text('TXRA now rebuilds thirty more functions from ordinary C, including functions that call others and use globals. Compare before/ and after/ for the same-view totals; the charts show the gain across accepted replacements. The muted clip walks through the same progress using only our tool output. The percentage includes literal pools, so it is an approximate measure of instruction coverage.\n')
    (root/'captions.json').write_text(json.dumps({'matched-percent.png':'After: approximate matched code share across the thirty accepted replacements.',
        'matched-bytes.png':'Before and after: 582 to 2,388 matched bytes, including pools.',
        'matching-progress.webm':'Six-second muted progress walkthrough, 30 fps; metadata only.'},indent=2)+'\n')
    (root/'milestones.json').write_text(json.dumps([{'additional_matches':k,'functions':25+k,'bytes':n} for k,n in enumerate(totals)],indent=2)+'\n')
    print('Wrote matching charts, same-view status pictures, captions and a six-second clip.')

if __name__ == '__main__':main()

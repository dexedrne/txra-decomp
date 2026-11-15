#!/usr/bin/env python3
"""Render round-four discovery evidence using metadata only; never opens ROM."""
import argparse
import json
from pathlib import Path
import subprocess
from review_map import base, font, heat, FG, MUTED, COLORS


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory', type=Path)
    p.add_argument('--before-config', type=Path, required=True)
    p.add_argument('--before-functions', type=Path, required=True)
    args = p.parse_args(); root = args.directory; root.mkdir(parents=True, exist_ok=True)
    cfg = json.loads(Path('tools/rom.cfg').read_text())
    prior = json.loads(args.before_config.read_text())
    audit = json.loads(Path('docs/map/code-audit.json').read_text())
    summary = json.loads(Path('docs/map/round4-audit.json').read_text())
    coverage = json.loads(Path('docs/map/coverage.json').read_text())
    race = next(s for s in coverage['sessions'] if s['name']=='race')
    if race['frames'] != 12500 or any(s['stopped'] or any(s[k] for k in ('fallback_steps','unknown_targets','unsupported')) for s in coverage['sessions']):
        raise ValueError('review requires the full race and clean runtime statistics')
    if audit['counts']['proposal'] or len(json.loads(args.before_functions.read_text())['functions']) != len(json.loads(Path('docs/map/functions.json').read_text())['functions']):
        raise ValueError('this review layout describes a pass with no newly accepted function')
    fs = json.loads(Path('docs/map/functions.json').read_text())['functions']
    old = len(json.loads(args.before_functions.read_text())['functions']); n = len(fs)
    code = sum(b['size'] for b in cfg['mapping'] if b['type']=='code')
    unknown = sum(b['size'] for b in cfg['mapping'] if b['type']=='unknown')
    images = []
    for folder, config, label in [('before',prior,'Before: round 3'),('after',cfg,'After: round 4 audit')]:
        dest = root/folder; dest.mkdir(exist_ok=True)
        im = heat(config['mapping'], label, cfg['size']); im.save(dest/'rom-heat-strip.png'); images.append(im)
        (dest/'NOTES.md').write_text('TXRA code discovery, round four. Compare these same-view maps; this audit did not establish additional code. The colors show exact metadata classifications, with dark areas still unknown.\n')
        (dest/'captions.json').write_text(json.dumps({'rom-heat-strip.png':label+'; the same full-ROM view, metadata only.'},indent=2)+'\n')
    im, d = base('Function discovery: evidence checked', 'The function count stays unchanged when switch labels and false pointers are excluded')
    for y, label, value in [(270,'Before',old),(490,'After',n)]:
        d.text((70,y),label,font=font(30,True),fill=FG)
        d.rectangle((280,y,280+int(1000*value/max(old,n,1)),y+65),fill=COLORS['code'])
        d.text((1320,y+6),str(value),font=font(38,True),fill=FG)
    d.text((70,690),f'{sum(f["mode"]=="thumb" for f in fs)} THUMB / {sum(f["mode"]=="arm" for f in fs)} ARM entries; {code:,} code bytes',font=font(28),fill=FG)
    d.text((70,750),f'{unknown:,} bytes remain unknown. No additional function was accepted.',font=font(25),fill=MUTED)
    d.text((70,830),f'{len(summary["sessions"])} coverage sessions; full race: {race["frames"]:,} frames; zero fallback / unknown / unsupported.',font=font(23),fill=MUTED)
    d.text((70,905),'Metadata only. This audit does not prove every possible function or game path is known.',font=font(22),fill=MUTED)
    im.save(root/'functions-found.png')
    chart, d = base('What the candidate scan found', f'{audit["scanned_source_bytes"]:,} source bytes checked across table, data and unknown regions')
    labels = [('existing-entry','Existing function entries',COLORS['code']),
              ('internal-switch-target','Internal switch targets',COLORS['table']),
              ('rejected','Rejected / not proven',COLORS['data']),
              ('proposal','Additional function proposals',COLORS['compressed'])]
    maximum = max(audit['counts'].values())
    for row,(key,label,color) in enumerate(labels):
        y = 235+row*135; value = audit['counts'][key]
        d.text((65,y),label,font=font(26),fill=FG)
        if value:d.rectangle((550,y,550+int(800*value/maximum),y+48),fill=color)
        d.text((1400,y),str(value),font=font(30,True),fill=FG)
    d.text((65,805),'Every rejected candidate retains its reference offsets and reason in the audit.',font=font(24),fill=MUTED)
    d.text((65,860),'Pointer-shaped values in course, lookup and audio data do not establish executable code.',font=font(23),fill=MUTED)
    d.text((65,920),'Validation limits and unresolved transfers remain explicit; no new code was guessed.',font=font(23),fill=MUTED)
    chart.save(root/'candidate-audit.png')
    encoder = subprocess.Popen(['ffmpeg','-v','error','-y','-f','rawvideo','-pixel_format','rgb24',
        '-video_size','1600x1000','-framerate','30','-i','-','-an','-c:v','libvpx-vp9','-threads','2',
        '-b:v','900k','-crf','35','-r','30',str(root/'audit-status.webm')],stdin=subprocess.PIPE)
    for frame in range(180):
        if frame<60:picture=chart
        elif frame<120:picture=im
        else:picture=images[0] if frame<150 else images[1]
        encoder.stdin.write(picture.tobytes())
    encoder.stdin.close()
    if encoder.wait():raise RuntimeError('encoder failed')
    if (root/'audit-status.webm').stat().st_size>4000000:raise RuntimeError('review clip exceeds size limit')
    delta=sum(b['size'] for b in prior['mapping'] if b['type']=='unknown')-unknown
    (root/'NOTES.md').write_text(f'TXRA round four checks pointers and calls for code missed by the earlier map. No additional function passed review; a new pause-choice probe mapped {delta:,} more data bytes. Compare the printed unknown totals in before/ and after/, since the changes are too small to see clearly at this scale; the charts explain the candidate counts. The muted clip shows our metadata tools only, with no game footage.\n')
    (root/'captions.json').write_text(json.dumps({'functions-found.png':f'Before and after: {old} to {n} mapped function entries; no count inflated by switch labels.',
        'candidate-audit.png':'Actual scan results: existing entries, internal switch labels and rejected candidates.',
        'audit-status.webm':'Six seconds at 30 fps: candidate results, function counts and same-view byte maps.'},indent=2)+'\n')
    print('Wrote same-view maps, two evidence charts and a six-second muted metadata clip.')

if __name__ == '__main__':main()

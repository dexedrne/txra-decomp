"""Render the assigned angle/queue study using our matching metadata only."""
import argparse
import json
from pathlib import Path
import subprocess
from PIL import Image, ImageDraw, ImageFont


def font(size):
    paths = ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
             '/usr/share/fonts/Adwaita/AdwaitaSans-Regular.ttf']
    return ImageFont.truetype(next(p for p in paths if Path(p).exists()), size)


def panel(title, lines):
    im = Image.new('RGB', (1280, 800), '#101725')
    d = ImageDraw.Draw(im)
    d.text((55, 38), 'TXRA / MATCHING ROUND 9', font=font(22), fill='#b0bbce')
    d.text((55, 105), title, font=font(42), fill='#f2eedf')
    for i, line in enumerate(lines):
        d.text((55, 220 + i * 77), line, font=font(28), fill='#f2eedf')
    d.text((55, 745), 'Matching metadata only. No private game content.', font=font(21), fill='#b0bbce')
    return im


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('directory', type=Path)
    ap.add_argument('--baseline', required=True)
    args = ap.parse_args()
    root = args.directory
    root.mkdir(parents=True, exist_ok=True)
    old = json.loads(subprocess.check_output(['git', 'show', args.baseline + ':tools/rom.cfg'], text=True))
    new = json.loads(Path('tools/rom.cfg').read_text())
    mapped = json.loads(Path('progress.json').read_text())['code_bytes_mapped']
    frames = []
    for name, cfg in [('before', old), ('after', new)]:
        count = len(cfg['matches'])
        size = sum(m['size'] for m in cfg['matches'])
        im = panel('Verified C replacements', [f'Complete functions: {count}',
                   f'Matched bytes including pools: {size:,}',
                   f'Of mapped instruction bytes: {100*size/mapped:.3f}%',
                   'A near match is excluded from these totals.'])
        folder = root / name
        folder.mkdir(exist_ok=True)
        im.save(folder / 'matching-status.png')
        (folder / 'NOTES.md').write_text('TXRA matching totals, ' + name + ' this pass. Compare the same view in before/ and after/. Only complete verified replacements count.\n')
        (folder / 'captions.json').write_text(json.dumps({'matching-status.png': name.capitalize() + ': complete verified replacements; near matches excluded.'}, indent=2) + '\n')
        frames.append(im)
    nearest = json.loads(Path('docs/near-misses/func_08015DA8.json').read_text())
    distance = nearest.get('score', [7])[0]
    study = panel('Angle and queue study', [
        'Angle: already matched before this pass (88 bytes).',
        f'Queue: 11 to {distance} differing instructions.',
        'Queue length: 118 bytes; still an uninstalled draft.',
        'Remaining work: zero-path store and readback registers.',
        f'New complete matches: {len(new["matches"])-len(old["matches"])} / target 5.'])
    study.save(root / 'queue-study.png')
    frames.append(study)
    proc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo',
        '-pixel_format', 'rgb24', '-video_size', '1280x800', '-framerate', '30',
        '-i', '-', '-an', '-c:v', 'libvpx-vp9', '-threads', '2', '-b:v', '500k',
        '-crf', '36', '-r', '30', str(root / 'matching-study.webm')], stdin=subprocess.PIPE)
    for im in frames:
        for _ in range(60):
            proc.stdin.write(im.tobytes())
    proc.stdin.close()
    if proc.wait():
        raise RuntimeError('review encoding failed')
    if (root / 'matching-study.webm').stat().st_size > 4000000:
        raise RuntimeError('review clip exceeds limit')
    (root / 'NOTES.md').write_text('TXRA angle and queue matching study. The angle was already complete; the queue draft is closer but still excluded from the matching totals. Compare before/ and after/ for the same-view totals, then look at queue-study.png for the remaining gap. The muted six-second clip shows only our matching results. The five-new-match target is unfinished.\n')
    (root / 'captions.json').write_text(json.dumps({
        'queue-study.png': 'After: the queue draft is closer, but no new complete match is claimed.',
        'matching-study.webm': 'Before, after and queue study; six seconds, muted, 30 fps.'}, indent=2) + '\n')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Render sanitized owner comparisons; no decompiler exports or ROM bytes saved."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'recomp'))
import draft
import reloc
from measure_candidate import diagnostic_compile
import review_match1109c as review

TARGETS = [
    ('hud-owner-1110', '0800421C', 'HUD drawer', 0x08004422, 36),
    ('arm-16da8-1110', '08016DA8', 'Track-face renderer', 0x08016EF0, 96),
]


def media_record(path, **extra):
    return dict(bytes=path.stat().st_size,
                sha256=hashlib.sha256(path.read_bytes()).hexdigest(), **extra)


def clip(path, before, after):
    command = ['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'rawvideo',
               '-pix_fmt', 'rgb24', '-s', '1600x1000', '-r', '30', '-i', '-', '-an',
               '-frames:v', '120', '-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '38',
               '-deadline', 'good', '-cpu-used', '4', '-row-mt', '1', '-threads', '2', str(path)]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    try:
        for frame in range(120):
            picture = (before if frame < 60 else after).copy()
            draw = ImageDraw.Draw(picture)
            y = 316 + ((frame % 60) * 23 // 60) * 24
            draw.rectangle((36, y - 2, 1564, y + 22), outline=review.AMBER, width=2)
            process.stdin.write(picture.tobytes())
        process.stdin.close()
        assert process.wait() == 0
    finally:
        if process.poll() is None:
            process.kill()
            process.wait()
    info = json.loads(subprocess.check_output(
        ['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)]))
    assert len(info['streams']) == 1
    stream = info['streams'][0]
    assert stream['codec_type'] == 'video' and stream['r_frame_rate'] == '30/1'
    assert (stream['width'], stream['height']) == (1600, 1000)
    assert 3.9 < float(info['format']['duration']) < 4.1
    assert path.stat().st_size <= 4_000_000
    return media_record(path, seconds=float(info['format']['duration']), fps=30,
                        width=1600, height=1000, audio_streams=0)


def source_flow():
    picture = Image.new('RGB', (1600, 1000), review.BG)
    draw = ImageDraw.Draw(picture)
    draw.text((42, 28), 'TXRA / 11.10 / RENDERER SOURCE CHANGE',
              font=review.font(25, True), fill=review.MUTED)
    draw.text((42, 85), 'Same generated code; clearer near-path guards',
              font=review.font(37, True), fill=review.FG)
    draw.text((42, 150), '3,251 differing bytes / 108-byte frame / no replacement installed',
              font=review.font(26), fill=review.AMBER)
    groups = [
        ('before: early skips', [
            'for each of four face parts:',
            '    if depth is negative: skip',
            '    build the part geometry',
            '    project its four points',
            '    if no corner is visible: skip',
            '    expand and clamp the packet',
            '    if winding is positive: skip',
            '    write texture coordinates',
            '    finish the packet',
        ]),
        ('after: positive guards', [
            'for each of four face parts:',
            '    if depth is nonnegative:',
            '        build the part geometry',
            '        project its four points',
            '        if a corner is visible:',
            '            expand and clamp',
            '            if winding is nonpositive:',
            '                write texture coordinates',
            '                finish the packet',
        ]),
    ]
    for x, (title, lines) in zip((42, 820), groups):
        draw.text((x, 260), title, font=review.font(28, True), fill=review.AMBER)
        for index, line in enumerate(lines):
            y = 330 + index * 48
            font = review.font(22, mono=True)
            assert draw.textbbox((x, y), line, font=font)[2] < x + 740
            draw.text((x, y), line, font=font, fill=review.FG)
    draw.text((42, 875), 'This describes our C sources. It is not exported decompiler text.',
              font=review.font(26), fill=review.FG)
    draw.text((42, 930), 'The independent state checks pass; original byte equality is still missing.',
              font=review.font(24), fill=review.MUTED)
    return picture


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    output = parser.parse_args().directory
    output.mkdir(parents=True, exist_ok=True)
    (output / 'NOTES.md').write_text(
        'TXRA HUD and track-renderer code are reviewed here after looking at their original control flow. '
        'The HUD is closer by 67 bytes; the renderer uses clearer conditions but produces the same code as before. '
        'Compare each before and after pair at the same original code view, and use the renderer flow picture to see its source change. '
        'The four-second muted clips replay those comparisons; they are not gameplay recordings. '
        'Both pieces still differ from the cartridge, so no game replacement was installed.\n')
    captions, artifacts = {}, {}
    program = draft.Program()
    symbols = reloc.symbols(program)
    overview = Image.new('RGB', (1000, 660), review.BG)
    overview_draw = ImageDraw.Draw(overview)
    for group, (folder, address, name, focus, frame) in enumerate(TARGETS):
        images = []
        for after, label in ((False, 'baseline'), (True, 'candidate')):
            record = json.loads((Path('docs/near-misses') / folder / (label + '.json')).read_text())
            source = Path(record['source']).read_text()
            assert hashlib.sha256(source.encode()).hexdigest() == record['source_sha256']
            start, end = int(address, 16), int(record['target_end'], 16)
            actual, _ = diagnostic_compile(source, 'func_' + address, start, symbols, record['compiler'])
            assert hashlib.sha256(actual).hexdigest() == record['compiled_sha256']
            expected = program.rom[start - draft.BASE:end - draft.BASE]
            mode = 'arm' if record['compiler'] == 'arm' else 'thumb'
            rows = review.compare(expected, actual, start, mode)
            picture = review.picture(address, name, rows, focus, record, after, frame)
            draw = ImageDraw.Draw(picture)
            draw.rectangle((36, 20, 1564, 65), fill=review.BG)
            draw.text((42, 28), 'TXRA / MATCHING C / 11.10 / DECOMPILER-GUIDED PASS',
                      font=review.font(22, True), fill=review.MUTED)
            if address == '08016DA8' and after:
                draw.rectangle((36, 120, 1564, 163), fill=review.BG)
                draw.text((42, 126), 'after: positive near guards; generated code is unchanged from before',
                          font=review.font(23), fill=review.MUTED)
            filename = ('after-' if after else 'before-') + address + '.png'
            picture.save(output / filename)
            images.append(picture)
            captions[filename] = (('After: ' if after else 'Before: ') + name.lower()
                                  + f", {record['different_bytes']:,} bytes still differ; same original view."
                                  + (' Generated code unchanged.' if address == '08016DA8' else ''))
            artifacts[filename] = media_record(output / filename, width=1600, height=1000)
        filename = address + '.webm'
        artifacts[filename] = clip(output / filename, *images)
        captions[filename] = 'Four seconds, muted, 30 fps: before then after ' + name.lower() + '; still a nonmatch.'
        overview_draw.text((12, group * 330 + 3), address + ' / decoded clip frames, before then after',
                           font=review.font(17, True), fill=review.FG)
        for index in range(8):
            data = subprocess.check_output(['ffmpeg', '-v', 'error', '-ss', str(index * 0.5 + 0.25),
                                            '-i', str(output / filename), '-frames:v', '1', '-f',
                                            'image2pipe', '-vcodec', 'png', '-'])
            decoded = Image.open(io.BytesIO(data)).convert('RGB')
            assert decoded.size == (1600, 1000)
            assert max(decoded.getextrema()[0]) - min(decoded.getextrema()[0]) > 100
            overview.paste(decoded.resize((250, 156)), ((index % 4) * 250, group * 330 + 18 + (index // 4) * 156))
    for filename, picture, caption in [
        ('arm-source-flow.png', source_flow(), 'Before and after renderer source flow; compiled output stays identical.'),
        ('clip-overview.png', overview, 'Decoded frames every half second: HUD above, renderer below; before then after.'),
    ]:
        picture.save(output / filename)
        captions[filename] = caption
        artifacts[filename] = media_record(output / filename, width=picture.width, height=picture.height)
    (output / 'captions.json').write_text(json.dumps(captions, indent=2) + '\n')
    Path('docs/near-misses/review-1110.json').write_text(json.dumps(artifacts, indent=2) + '\n')
    print(json.dumps(artifacts, indent=2))


if __name__ == '__main__':
    main()

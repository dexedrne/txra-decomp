#!/usr/bin/env python3
"""Render frozen, sanitized block-search comparisons and muted review clips."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont
import llm_blocks as blocks
import draft
import reloc
import review_match1109c as review
from review_match1110 import clip, media_record

NAMES = {'0800421C': 'HUD drawer', '080064A4': 'Sound owner', '08016DA8': 'Track-face renderer'}
FRAMES = {'0800421C': 36, '080064A4': 108, '08016DA8': 96}

if not (review.FONT / 'NimbusSans-Regular.otf').exists():
    def portable_font(size, bold=False, mono=False):
        if mono:
            path = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono' + ('-Bold' if bold else '') + '.ttf'
        else:
            path = '/usr/share/fonts/truetype/noto/NotoSans-' + ('Bold' if bold else 'Regular') + '.ttf'
        return ImageFont.truetype(path, size)
    review.font = portable_font


def fitted(draw, xy, text, size, width, **options):
    font = review.font(size, **options)
    assert draw.textbbox(xy, text, font=font)[2] <= xy[0] + width, text
    draw.text(xy, text, font=font, fill=review.FG)


def summary(state, name_count, names_total):
    picture = Image.new('RGB', (1600, 1000), review.BG)
    draw = ImageDraw.Draw(picture)
    draw.text((42, 28), 'TXRA / 11.11 / BLOCK SEARCH', font=review.font(25, True), fill=review.MUTED)
    fitted(draw, (42, 85), 'Small C regions, whole-function measurements', 37, 1515, bold=True)
    fitted(draw, (42, 150), 'Only an exact replacement can pass the complete cartridge rebuild gate.', 25, 1515)
    for i, (address, record) in enumerate(state['targets'].items()):
        y = 245 + i * 155
        draw.rounded_rectangle((35, y - 15, 1565, y + 120), radius=8, fill=review.AGREE, outline=review.BORDER)
        fitted(draw, (58, y), address + ' / ' + NAMES[address], 29, 740, bold=True)
        draw.text((835, y), f"{record['before']:,} -> {record['best']:,} differing bytes",
                  font=review.font(28, True), fill=review.AMBER)
        fitted(draw, (58, y + 60), f"{record['compiled']} measured alternatives / {record['attempts']} proposed", 25, 740)
        fitted(draw, (835, y + 60), f"{record['improvements']} retained improvements / {record['profile']} profile", 25, 680)
    hud = state['targets']['0800421C']
    fitted(draw, (42, 760), f"HUD proof: {hud['compiled']} / 200 measured. Naming proposals: {name_count} / {names_total}.", 27, 1515)
    draw.text((42, 820), 'Installed replacements this round: ' + (', '.join(state['installed']) or 'none'),
              font=review.font(27, True), fill=review.AMBER)
    fitted(draw, (42, 890), 'Before/after pairs use the same original instruction window.', 24, 1515)
    fitted(draw, (42, 936), 'Compiler review only. The clips do not claim a gameplay or performance change.', 24, 1515)
    return picture


def frozen_profile(path):
    profile = json.loads(path.read_text())
    code = Path(profile['source']).read_text()
    if hashlib.sha256(code.encode()).hexdigest() != profile['source_sha256']:
        raise ValueError('source changed during review snapshot; retry after the current judgement')
    return profile, code


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    destination = parser.parse_args().directory.expanduser()
    state = json.loads(blocks.STATE.read_text())
    program = draft.Program()
    symbols = reloc.symbols(program)
    regions = json.loads(Path('docs/near-misses/regions-1111.json').read_text())
    names = json.loads(blocks.NAMES.read_text()) if blocks.NAMES.exists() else {}
    artifacts, captions, sources = {}, {}, {}
    # Publish only after every dimension, source identity and clip has passed.
    with tempfile.TemporaryDirectory(prefix='review-local1111-', dir='build') as folder:
        output = Path(folder)
        picture = summary(state, len(names), sum(m['name'].startswith('func_') for m in program.matched.values()))
        picture.save(output / 'search-status.png')
        artifacts['search-status.png'] = media_record(output / 'search-status.png', width=1600, height=1000)
        captions['search-status.png'] = 'Search snapshot: measured attempts, retained byte counts, and naming coverage; no guessed matches.'
        overview = Image.new('RGB', (1000, 990), review.BG)
        for group, (address, (stem, _, end, profile)) in enumerate(blocks.TARGETS.items()):
            directory = Path('docs/near-misses') / (stem + '-1111')
            images = []
            before, before_code = frozen_profile(directory / 'baseline.json')
            after, after_code = frozen_profile(directory / 'candidate.json')
            if after['source_sha256'] != state['targets'][address]['source_sha256']:
                raise ValueError('candidate adoption overlapped the status snapshot; retry')
            changed = before['compiled_sha256'] != after['compiled_sha256']
            focus = int(address, 16) + min(a for a, z in regions[address]['machine_spans'])
            start = int(address, 16)
            compiled = {}
            for label, record, code in (('baseline', before, before_code), ('candidate', after, after_code)):
                actual, _ = blocks.measure.diagnostic_compile(code, 'func_' + address, start, symbols, profile)
                assert hashlib.sha256(actual).hexdigest() == record['compiled_sha256']
                compiled[label] = actual
            if changed:
                first = next((i for i, (a, b) in enumerate(zip(compiled['baseline'], compiled['candidate'])) if a != b),
                             min(len(compiled['baseline']), len(compiled['candidate'])))
                width = 4 if profile == 'arm' else 2
                focus = start + max(0, min(first // width * width - 8, end - start - 160))
            sources[address] = dict(before_source_sha256=before['source_sha256'],
                                    after_source_sha256=after['source_sha256'],
                                    before_compiled_sha256=before['compiled_sha256'],
                                    after_compiled_sha256=after['compiled_sha256'], focus_address='%08X' % focus)
            for is_after, label in ((False, 'baseline'), (True, 'candidate')):
                record = after if is_after else before
                actual = compiled[label]
                want = program.rom[start - blocks.match.BASE:end - blocks.match.BASE]
                mode = 'arm' if profile == 'arm' else 'thumb'
                # Anchor each column to the same actual address window. Global
                # shape alignment can move the entire sound listing ahead of
                # this window and leave a misleading empty candidate column.
                left = [r for r in review.listing(want, start, mode) if r[0] >= focus]
                right = [r for r in review.listing(actual, start, mode) if r[0] >= focus]
                rows = [(x, y, x == y) for x, y in zip(left, right)]
                picture = review.picture(address, NAMES[address], rows, focus, record, is_after, FRAMES[address])
                draw = ImageDraw.Draw(picture)
                draw.rectangle((36, 20, 1564, 65), fill=review.BG)
                draw.text((42, 28), 'TXRA / 11.11 / LOCAL BLOCK SEARCH', font=review.font(22, True), fill=review.MUTED)
                if is_after and not changed:
                    draw.rectangle((36, 120, 1564, 163), fill=review.BG)
                    draw.text((42, 126), 'after: no improvement yet; the retained compiler output is unchanged',
                              font=review.font(23), fill=review.MUTED)
                filename = ('after-' if is_after else 'before-') + address + '.png'
                picture.save(output / filename)
                artifacts[filename] = media_record(output / filename, width=1600, height=1000)
                captions[filename] = (('After' if is_after else 'Before') + ': ' + NAMES[address] +
                    f", {record['different_bytes']:,} differing bytes, same original instruction view." +
                    (' Compiler output unchanged.' if is_after and not changed else ''))
                images.append(picture)
            filename = address + '.webm'
            artifacts[filename] = clip(output / filename, *images)
            captions[filename] = 'Four seconds, muted, 30 fps: ' + NAMES[address] + ' before then after compiler comparison; not gameplay.'
            for index in range(8):
                frame = subprocess.check_output(['ffmpeg', '-v', 'error', '-ss', str(index * .5 + .25),
                    '-i', str(output / filename), '-frames:v', '1', '-f', 'image2pipe', '-vcodec', 'png', '-'])
                thumbnail = Image.open(io.BytesIO(frame)).convert('RGB').resize((250, 156))
                overview.paste(thumbnail, ((index % 4) * 250, group * 330 + 18 + (index // 4) * 156))
            ImageDraw.Draw(overview).text((8, group * 330), address + ' / decoded frames',
                                         font=review.font(17, True), fill=review.FG)
        overview.save(output / 'clip-overview.png')
        artifacts['clip-overview.png'] = media_record(output / 'clip-overview.png', width=1000, height=990)
        captions['clip-overview.png'] = 'Decoded half-second samples from all three muted clips, before then after.'
        hud = state['targets']['0800421C']
        gain = hud['before'] - hud['best']
        result = f"The HUD is {gain} bytes closer so far" if gain else 'The HUD output is unchanged so far'
        (output / 'NOTES.md').write_text(
            'This is TXRA compiler recovery: the search now asks for small C changes and measures the whole function. '
            + result + '; the search continues, and the status picture shows this snapshot’s attempts and naming coverage. '
            'Compare each before/after pair at the same instruction view; unchanged outputs are labelled explicitly. '
            'The muted clips replay those compiler comparisons, not gameplay. '
            'Nearer candidates remain uninstalled until every byte and the complete rebuild agree.\n')
        (output / 'captions.json').write_text(json.dumps(captions, indent=2) + '\n')
        destination.mkdir(parents=True, exist_ok=True)
        for path in output.iterdir():
            # Artifacts are all small and live on the same home filesystem.
            path.replace(destination / path.name)
    blocks.atomic(Path('docs/near-misses/review-1111.json'), dict(
        snapshot=state['updated'], artifacts=artifacts, sources=sources,
        comparisons_only=True, gameplay_claimed=False))
    print('Published %d reviewed media files.' % len(artifacts))


if __name__ == '__main__':
    main()

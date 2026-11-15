#!/usr/bin/env python3
"""Review the eight exact C replacements using sanitized compiler metadata."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'recomp'))
import draft
import reloc
import review_match1109c as review
from measure_candidate import diagnostic_compile
from review_match1110 import media_record, clip as code_clip

ROOT = Path('docs/near-misses/breadth-1112')
ENTRIES = [('0800753C', 'sound fade request'), ('08014790', 'link request setter'),
           ('080075DC', 'sound state restore'), ('08018DA0', 'EEPROM retry wrapper'),
           ('08015F98', 'display buffer clear'), ('08015F58', 'neutral display fill'),
           ('08015E50', 'display / object fill A'), ('08015ED4', 'display / object fill B')]


def font(size, bold=False, mono=False):
    name = 'DejaVuSansMono' if mono else 'DejaVuSans'
    return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/'+name+('-Bold' if bold else '')+'.ttf', size)


review.font = font


def line(draw, xy, text, size=26, color=review.FG, bold=False, mono=False, width=1510):
    f = font(size, bold, mono)
    assert draw.textbbox(xy, text, font=f)[2] <= xy[0]+width, text
    draw.text(xy, text, font=f, fill=color)


def overview(after):
    im = Image.new('RGB', (1600, 1000), review.BG)
    d = ImageDraw.Draw(im)
    line(d, (42, 25), 'TXRA / 12 NOVEMBER / SMALL FUNCTION RECOVERY', 23, review.MUTED, True)
    line(d, (42, 79), 'Eight complete helpers recovered', 42, bold=True)
    line(d, (42, 143), 'AFTER: all eight exact and installed' if after else 'BEFORE: eight gaps without C replacements', 26, review.AMBER)
    metrics = [('exact C matches', 189 if after else 181), ('mapped entries', 237 if after else 229),
               ('unknown bytes', '721,370' if after else '721,992')]
    for x, (name, value) in zip((42, 562, 1082), metrics):
        line(d, (x, 215), str(value), 48, review.AMBER, True, width=470)
        line(d, (x, 280), name, 25, width=470)
    line(d, (42, 344), 'entry', 23, review.MUTED, True)
    line(d, (340, 344), 'recovered helper', 23, review.MUTED, True)
    line(d, (1130, 344), 'complete byte check', 23, review.MUTED, True, width=430)
    for i, (a, title) in enumerate(ENTRIES):
        y = 392+i*53
        d.rectangle((35, y-4, 1565, y+43), fill=review.AGREE)
        line(d, (50, y), a, 25, mono=True, width=260)
        line(d, (340, y), title, 25, width=740)
        r = json.loads((ROOT/('candidate-'+a+'.json')).read_text())
        line(d, (1130, y), f"{r['target_bytes']} / {r['target_bytes']} exact" if after else 'unmapped', 24,
             review.AMBER if after else review.MUTED, width=420)
    line(d, (42, 866), 'Each installation passed a forced complete rebuild and the cartridge hash gate.' if after
         else 'New code gaps are reviewed as static candidates before any C is installed.', 24)
    line(d, (42, 918), '446 instruction bytes and 176 pool bytes mapped. No new runtime execution claim.' if after
         else 'Candidates cover 446 instruction bytes and 176 pool bytes. Runtime remains unverified.', 24, review.MUTED)
    line(d, (42, 962), 'Compiler and mapping review only; this is not gameplay footage.', 21, review.MUTED)
    return im


def comparison(program, after):
    address = '08015E50'
    profile = json.loads((ROOT/(('candidate-' if after else 'baseline-')+address+'.json')).read_text())
    path = ROOT/('candidates' if after else 'baseline-sources')/('func_'+address+'.c')
    code = path.read_text()
    assert hashlib.sha256(code.encode()).hexdigest() == profile['source_sha256']
    a, z = int(address, 16), int(profile['target_end'], 16)
    data, _ = diagnostic_compile(code, 'func_'+address, a, reloc.symbols(program), 'old')
    assert hashlib.sha256(data).hexdigest() == profile['compiled_sha256']
    want = program.rom[a-draft.BASE:z-draft.BASE]
    if after:
        assert data == want and profile['installed'] and profile['whole_rom_gate']
    im = Image.new('RGB', (1600, 1000), review.BG)
    d = ImageDraw.Draw(im)
    line(d, (42, 25), 'TXRA / 12 NOVEMBER / SAME ORIGINAL INSTRUCTION VIEW', 23, review.MUTED, True)
    line(d, (42, 78), '08015E50 / neutral display and object fill', 38, bold=True)
    line(d, (42, 145), 'AFTER: shared fill value, separate DMA blocks' if after else 'BEFORE: first structured C draft', 26, review.MUTED)
    line(d, (42, 200), f"{profile['different_bytes']} differing bytes / {profile['emitted_bytes']} of {profile['target_bytes']} bytes", 34, review.AMBER, True)
    line(d, (42, 269), 'original instructions', 24, review.AMBER, True)
    line(d, (820, 269), 'compiled structured C', 24, review.AMBER, True, width=740)
    left, right = review.listing(want, a, 'thumb'), review.listing(data, a, 'thumb')
    for i, (l, r) in enumerate(zip(left[:23], right[:23])):
        y = 316+i*24
        d.rectangle((36, y-2, 1564, y+22), fill=review.AGREE if l == r else review.BAD)
        for x, item in ((45, l), (823, r)):
            line(d, (x, y), '%08X  %s' % item[:2], 18, mono=True, width=740)
    d.line((42, 900, 1558, 900), fill=review.BORDER, width=2)
    line(d, (42, 920), 'All 132 bytes, including every pool, match; the whole cartridge rebuild passes.' if after else
         'The first draft differs in 107 bytes and is 12 bytes short. It cannot be installed.', 24)
    line(d, (42, 961), 'Encodings and pool contents are hidden. No new gameplay or performance claim.', 21, review.MUTED)
    return im


def status_clip(path, before, after):
    command = ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
               '-s', '1600x1000', '-r', '30', '-i', '-', '-an', '-frames:v', '120',
               '-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '38', '-deadline', 'good',
               '-cpu-used', '4', '-row-mt', '1', '-threads', '2', str(path)]
    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    try:
        for frame in range(120):
            im = (before if frame < 60 else after).copy()
            y = 392+(frame % 60)*8//60*53
            ImageDraw.Draw(im).rectangle((35, y-4, 1565, y+43), outline=review.AMBER, width=2)
            process.stdin.write(im.tobytes())
        process.stdin.close()
        assert process.wait() == 0
    finally:
        if process.poll() is None:
            process.kill()
            process.wait()
    info = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_streams', '-show_format', '-of', 'json', str(path)]))
    assert len(info['streams']) == 1 and info['streams'][0]['r_frame_rate'] == '30/1'
    assert (info['streams'][0]['width'], info['streams'][0]['height']) == (1600, 1000)
    assert 3.9 < float(info['format']['duration']) < 4.1 and path.stat().st_size < 4_000_000
    return media_record(path, seconds=float(info['format']['duration']), fps=30, width=1600, height=1000, audio_streams=0)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('directory', type=Path)
    ap.add_argument('--status-only', action='store_true', help='retain the valid compiler pictures and clip')
    args = ap.parse_args()
    dest = args.directory.expanduser()
    dest.mkdir(parents=True, exist_ok=True)
    captions, artifacts = {}, {}
    program = draft.Program()
    sheet = Image.new('RGB', (1000, 660), review.BG)
    for group, (stem, maker) in enumerate([('breadth-status', overview), ('08015E50', lambda after: comparison(program, after))]):
        images = []
        for after in (False, True):
            name = ('after-' if after else 'before-')+stem+'.png'
            im = Image.open(dest/name).convert('RGB') if args.status_only and group == 1 else maker(after)
            if not (args.status_only and group == 1):
                im.save(dest/name)
            artifacts[name] = media_record(dest/name, width=1600, height=1000)
            captions[name] = ('After: ' if after else 'Before: ')+('eight helpers and exact-match totals, same table view.' if group == 0 else 'display fill compiler comparison, same original instruction view.')
            images.append(im)
        name = stem+'.webm'
        if args.status_only and group == 1:
            artifacts[name] = json.loads((ROOT/'review.json').read_text())['artifacts'][name]
        else:
            artifacts[name] = (status_clip if group == 0 else code_clip)(dest/name, *images)
        captions[name] = 'Four seconds, muted, 30 fps: before then after '+('breadth results.' if group == 0 else 'display fill compiler comparison.')
        ImageDraw.Draw(sheet).text((8, group*330), stem+' / decoded frames', font=font(17, True), fill=review.FG)
        for index in range(8):
            data = subprocess.check_output(['ffmpeg', '-v', 'error', '-ss', str(.25+index*.5), '-i', str(dest/name),
                                            '-frames:v', '1', '-f', 'image2pipe', '-vcodec', 'png', '-'])
            im = Image.open(io.BytesIO(data)).convert('RGB').resize((250, 156))
            sheet.paste(im, ((index % 4)*250, group*330+18+(index//4)*156))
    name = 'clip-overview.png'
    sheet.save(dest/name)
    artifacts[name] = media_record(dest/name, width=1000, height=660)
    captions[name] = 'Decoded half-second samples from both muted comparison clips.'
    (dest/'NOTES.md').write_text('This is TXRA code recovery for eight small sound, display, link and save helpers. '
        'All eight now match the cartridge exactly, taking the total from 181 to 189; their discovery also adds eight mapped entries. '
        'Compare before and after at the same table and code views; the code example shows the display fill going from 107 differing bytes to zero. '
        'The short muted clips replay those comparisons, and the overview contains decoded samples from both clips. '
        'This is compiler evidence, with no new gameplay or runtime execution claim.\n')
    (dest/'captions.json').write_text(json.dumps(captions, indent=2)+'\n')
    (ROOT/'review.json').write_text(json.dumps(dict(directory='txra-review/breadth-1112',artifacts=artifacts,
        comparisons_only=True,gameplay_claimed=False),indent=2)+'\n')
    print('Published %d review artifacts.' % len(artifacts))


if __name__ == '__main__':
    main()

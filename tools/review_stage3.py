#!/usr/bin/env python3
"""Encode an existing private stage-three session; inspect images before marking milestones."""
import argparse
import json
import subprocess
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('output', type=Path)
p.add_argument('--session', type=Path, default=Path('build/stage3-final'))
p.add_argument('--menu-picture', type=Path)
a = p.parse_args()
a.output.mkdir(parents=True, exist_ok=True)
caption_path = a.output / 'captions.json'
captions = json.loads(caption_path.read_text()) if caption_path.exists() else {}
def run(*args): subprocess.run(args, check=True)
def picture(frame, name, caption):
    # Raw frame zero is guest frame two. Recording is every other VBlank.
    run('ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pixel_format', 'bgra',
        '-video_size', '240x160', '-framerate', '16777216/561792', '-i',
        str(a.session / 'session.bgra'), '-vf',
        f'select=eq(n\\,{frame // 2 - 1}),scale=960:640:flags=neighbor',
        '-frames:v', '1', str(a.output / (name + '.png')))
    captions[name + '.png'] = caption

def clip(first, duration, name, caption):
    path = a.output / (name + '.webm')
    run('ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pixel_format', 'bgra',
        '-video_size', '240x160', '-framerate', '16777216/561792', '-ss',
        str(first * 280896 / 16777216), '-i', str(a.session / 'session.bgra'),
        '-t', str(duration), '-vf', 'scale=720:480:flags=neighbor', '-r', '30',
        '-c:v', 'libvpx-vp9', '-crf', '34', '-b:v', '0', '-deadline', 'good',
        '-cpu-used', '4', '-an', str(path))
    assert path.stat().st_size <= 4_000_000
    captions[path.name] = caption

picture(900, 'title', 'After: title screen from the stage three PC build.')
picture(2080, 'main-menu', 'After: garage menu at the same frame as the previous build.')
if a.menu_picture:
    run('ffmpeg', '-v', 'error', '-y', '-i', str(a.menu_picture), '-vf',
        'scale=960:640:flags=neighbor', str(a.output / 'menu-settled.png'))
    captions['menu-settled.png'] = 'After: idle main menu; the left money label matches the guest bitmap.'
picture(4000, 'race', 'After: race at the same frame as the previous build.')
picture(12000, 'results', 'After: the complete race ends in a loss.')
# Two excerpts retain the title and animated car menus in a single short clip.
path = a.output / 'title-menu.webm'
raw = str(a.session / 'session.bgra')
source = ['-f', 'rawvideo', '-pixel_format', 'bgra', '-video_size', '240x160',
          '-framerate', '16777216/561792']
run('ffmpeg', '-v', 'error', '-y', *source, '-ss', str(840 * 280896 / 16777216),
    '-i', raw, *source, '-ss', str(1940 * 280896 / 16777216), '-i', raw,
    '-filter_complex',
    '[0:v]trim=duration=2,setpts=PTS-STARTPTS,scale=720:480:flags=neighbor[a];'
    '[1:v]trim=duration=6,setpts=PTS-STARTPTS,scale=720:480:flags=neighbor[b];'
    '[a][b]concat=n=2:v=1:a=0[out]', '-map', '[out]', '-t', '8', '-r', '30',
    '-c:v', 'libvpx-vp9', '-crf', '34', '-b:v', '0', '-deadline', 'good',
    '-cpu-used', '4', '-an', str(path))
assert path.stat().st_size <= 4_000_000
captions[path.name] = 'After: title and name entry, then a cut to animated car and race menus.'
clip(3450, 8, 'race-driving', 'After: acceleration and two steering inputs during the race.')
clip(10800, 6, 'race-results', 'After: the race ends and the game displays its loss result.')
(a.output / 'captions.json').write_text(json.dumps(captions, indent=2) + '\n')
(a.output / 'NOTES.md').write_text(
    'TXRA stage three runs from the title through a complete race loss. '
    'Timing, sound mixing, screen effects and controller reconnection have changed; compare before/ with the matching menu and race pictures. '
    'The three clips show the title and moving menus, driving, and the race ending. '
    'The money label still looks clipped at the left edge and already matches the game’s own picture; save and reload verification is described in the ship note.\n')

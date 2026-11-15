#!/usr/bin/env python3
"""Replay the reviewed career route in both execution modes; keep outputs private."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def check(directory, golden):
    for route in golden['routes']:
        root = directory / route['name']
        expected = route['expected']
        assert sha(route['script']) == route['script_sha256'], 'Route input changed'
        for mode in ('native', 'reference'):
            stats = json.loads((root / f'{mode}.json').read_text())
            for key, value in expected.items():
                assert stats[key] == value, f'{route["name"]}/{mode}: {key} differs'
            for key in ('unsupported', 'unknown_targets'):
                assert stats[key] == 0, f'Unexpected {key}'
            assert not stats['stopped']
            if mode == 'native':
                assert stats['fallback_steps'] == 0, 'Record and review newly executed code'
            assert sha(root / f'{mode}.hashes') == route['frames_sha256'], 'Frame sequence differs'
            assert sha(root / f'{mode}.pcm') == route['pcm_sha256'], 'PCM differs'
            assert sha(directory / f'{mode}.sav') == golden['save_sha256'], 'Career save differs'
        subprocess.run(['python3', 'tools/compare_runtime.py', str(root)], check=True)
    print('Career route: every native/reference frame, PCM byte, final state and unchanged reload save passed')


def check_input_reader(binary, rom):
    with tempfile.TemporaryDirectory(prefix='input-reader-', dir='build') as temp:
        root = Path(temp)
        cases = [('257 events', '10 20 1\n' * 257, 0),
                 ('8192 events', '10 20 1\n' * 8192, 0),
                 ('capacity overflow', '10 20 1\n' * 8193, 2),
                 ('invalid mask', '10 20 400\n', 2),
                 ('empty interval', '10 10 1\n', 2),
                 ('malformed row', 'bad row\n', 2)]
        for name, text, expected in cases:
            script = root/'input.txt'
            script.write_text(text)
            result = subprocess.run([str(binary.resolve()), '--rom', str(rom.resolve()),
                                     '--headless', '--mute', '--benchmark', '--frames', '1',
                                     '--input-script', str(script), '--save', str(root/'fresh.sav'),
                                     '--stats', str(root/'run.json'), '--unknown-log', str(root/'unknown.log')],
                                    capture_output=True)
            assert result.returncode == expected, f'Input reader: {name} failed'
        print('6 input-reader boundary and rejection checks passed')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory', type=Path, help='new private output folder below build/')
    p.add_argument('--existing', action='store_true', help='check completed recordings')
    p.add_argument('--binary', type=Path, default=Path('build/txra-pc'))
    p.add_argument('--rom', type=Path, default=Path('baserom.gba'))
    a = p.parse_args()
    root = a.directory.resolve()
    if Path('build').resolve() not in root.parents:
        p.error('Recordings must stay below ignored build/.')
    check_input_reader(a.binary, a.rom)
    golden = json.loads(Path('tests/career-golden.json').read_text())
    if not a.existing:
        root.mkdir(parents=True, exist_ok=False)
        for route in golden['routes']:
            dest = root / route['name']
            dest.mkdir()
            for mode in ('native', 'reference'):
                command = [str(a.binary.resolve()), '--rom', str(a.rom.resolve()),
                           '--headless', '--mute', '--benchmark', '--frames', str(route['expected']['frames']),
                           '--input-script', route['script'], '--save', str(root / f'{mode}.sav'),
                           '--stats', str(dest / f'{mode}.json'), '--frame-hashes', str(dest / f'{mode}.hashes'),
                           '--audio-dump', str(dest / f'{mode}.pcm'), '--unknown-log', str(dest / f'{mode}-unknown.log')]
                if mode == 'reference':
                    command.append('--interpreter')
                with (dest / f'{mode}.log').open('w') as log:
                    subprocess.run(command, stdout=log, stderr=log, check=True)
                if route['name'] != 'reload':
                    shutil.copy2(root / f'{mode}.sav', dest / f'{mode}.sav')
    check(root, golden)


if __name__ == '__main__':
    main()

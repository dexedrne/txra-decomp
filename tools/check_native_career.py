#!/usr/bin/env python3
"""Record native-only career/reload against existing reviewed goldens; no reference run."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
from check_career import check_input_reader, sha


def main():
    if sys.flags.optimize:
        raise SystemExit('Run without Python optimization: golden assertions must remain enabled.')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('directory', type=Path)
    parser.add_argument('--binary', type=Path, required=True)
    parser.add_argument('--rom', type=Path, default=Path('baserom.gba'))
    args = parser.parse_args()
    root = args.directory.resolve()
    if Path('build').resolve() not in root.parents:
        parser.error('Recordings must stay below ignored build/.')
    root.mkdir(parents=True, exist_ok=False)
    check_input_reader(args.binary, args.rom)
    golden = json.loads(Path('tests/career-golden.json').read_text())
    results = {'execution': 'native-only', 'reference': 'existing reviewed goldens; not executed',
               'binary_sha256': sha(args.binary), 'routes': []}
    save = root / 'native.sav'
    for route in golden['routes']:
        assert sha(route['script']) == route['script_sha256'], 'Route input changed'
        dest = root / route['name']
        dest.mkdir()
        command = [str(args.binary.resolve()), '--rom', str(args.rom.resolve()),
                   '--headless', '--mute', '--benchmark', '--frames', str(route['expected']['frames']),
                   '--input-script', route['script'], '--save', str(save),
                   '--stats', str(dest / 'native.json'), '--frame-hashes', str(dest / 'native.hashes'),
                   '--audio-dump', str(dest / 'native.pcm'), '--unknown-log', str(dest / 'unknown.log')]
        with (dest / 'native.log').open('w') as log:
            subprocess.run(command, stdout=log, stderr=log, check=True)
        stats = json.loads((dest / 'native.json').read_text())
        for key, value in route['expected'].items():
            assert stats[key] == value, f'{route["name"]}: {key} differs'
        for key in ('fallback_steps', 'unknown_targets', 'unsupported'):
            assert stats[key] == 0, f'Unexpected {key}'
        assert stats['functions_compiled'] == 229
        assert not stats['stopped']
        hashes = {'frames_sha256': sha(dest / 'native.hashes'),
                  'pcm_sha256': sha(dest / 'native.pcm'), 'save_sha256': sha(save)}
        assert hashes['frames_sha256'] == route['frames_sha256']
        assert hashes['pcm_sha256'] == route['pcm_sha256']
        assert hashes['save_sha256'] == golden['save_sha256']
        results['routes'].append({'name': route['name'], 'stats': stats, **hashes})
        (root / 'verification.json').write_text(json.dumps(results, indent=2) + '\n')
        print(f'{route["name"]}: native frames, PCM, state/cycles/samples/save and counters passed', flush=True)


if __name__ == '__main__':
    main()

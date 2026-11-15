#!/usr/bin/env python3
"""Lock frame/audio behavior to a reviewed recording, with metadata only in git."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def check(root, golden):
    stats = json.loads((root / 'run.json').read_text())
    assert sha(Path(golden['input_script'])) == golden['input_sha256'], 'Input script changed'
    assert sha(root / 'frames.txt') == golden['frames_sha256'], 'Framebuffer regression'
    assert sha(root / 'audio.pcm') == golden['pcm_sha256'], 'Audio regression'
    assert len((root / 'frames.txt').read_text().splitlines()) == golden['frames']
    for key in ('frames', 'state_hash', 'audio_samples', 'audio_hash', 'cycles'):
        assert stats[key] == golden[key], f'{key} regression'
    for key in ('unsupported', 'fallback_steps', 'unknown_targets'):
        assert stats[key] == 0, f'Unexpected {key}'
    assert not stats['stopped']
    print(f"Accuracy: {stats['frames']} framebuffer hashes, every PCM byte, final state and sample clock passed")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--existing', type=Path, help='check already captured run.json, frames.txt, audio.pcm')
    p.add_argument('--binary', type=Path, default=Path('build/txra-pc'))
    p.add_argument('--rom', type=Path, default=Path('baserom.gba'))
    a = p.parse_args()
    golden = json.loads(Path('tests/runtime-golden.json').read_text())
    if a.existing:
        check(a.existing, golden)
        return
    with tempfile.TemporaryDirectory(prefix='accuracy-', dir='build') as temp:
        root = Path(temp)
        subprocess.run([str(a.binary.resolve()), '--rom', str(a.rom), '--headless', '--mute',
                        '--benchmark', '--frames', str(golden['frames']),
                        '--input-script', golden['input_script'], '--save', str(root / 'fresh.sav'),
                        '--stats', str(root / 'run.json'), '--frame-hashes', str(root / 'frames.txt'),
                        '--audio-dump', str(root / 'audio.pcm'), '--unknown-log', str(root / 'unknown.log')], check=True)
        check(root, golden)


if __name__ == '__main__':
    main()

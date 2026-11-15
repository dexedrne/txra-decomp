#!/usr/bin/env python3
"""Compare completed native/fallback runs, without storing any ROM-derived data in git."""
import argparse
import json
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('directory', type=Path)
a = p.parse_args()
root = a.directory
native = json.loads((root / 'native.json').read_text())
reference = json.loads((root / 'reference.json').read_text())
frames = (root / 'native.hashes').read_bytes()
assert frames == (root / 'reference.hashes').read_bytes(), 'Framebuffer mismatch: compare per-frame hashes'
assert len(frames.splitlines()) == native['frames'] == reference['frames']
for key in ('state_hash', 'cycles', 'audio_samples', 'audio_hash', 'unsupported', 'stopped'):
    assert native[key] == reference[key], f'{key} differs'
assert not native['unsupported'] and not native['stopped']
assert not native['fallback_steps'] and not native['unknown_targets'], 'Record and translate new targets'
assert native['audio_samples'] == native['cycles'] // 512, 'Sample clock drift'
assert (root / 'native.pcm').read_bytes() == (root / 'reference.pcm').read_bytes(), 'Audio mismatch'
result = {'frames_compared': native['frames'], 'state_matches': True, 'audio_matches': True,
          'sample_clock_matches': True, 'fallback_steps': 0, 'unknown_targets': 0}
(root / 'comparison.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))

#!/usr/bin/env python3
"""Run synthetic state tests against the complete, uninstalled sound C candidate."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


def main():
    here = Path(__file__).resolve().parent
    root = here.parents[2]
    config_path = root / 'tools/rom.cfg'
    before = config_path.read_bytes()
    config = json.loads(before)
    begin, end = 0x64A4, 0x7398
    assert not [m for m in config['matches'] if m['offset'] < end and begin < m['offset'] + m['size']], 'Owner overlaps an installed match'
    compiler = shutil.which('cc')
    if not compiler:
        raise SystemExit('A host C compiler is required; none was found')
    with tempfile.TemporaryDirectory(prefix='sound-owner-source-') as directory:
        binary = str(Path(directory) / 'check')
        subprocess.run([compiler, '-std=c11', '-O1', '-Wall', '-Wextra', '-Werror',
                        '-fsanitize=undefined', '-fno-sanitize-recover=all',
                        '-fno-pie', '-no-pie', str(here / 'test_sound_owner.c'),
                        '-Wl,--defsym,g_08333324=test_steps+4', '-o', binary], check=True)
        subprocess.run([binary], check=True)
    assert config_path.read_bytes() == before, 'Registry changed during source checks'
    print('Candidate SHA256:', hashlib.sha256((here / 'func_080064A4.c').read_bytes()).hexdigest())
    print('No registered overlap; local source checks only (no byte comparison); match count unchanged')


if __name__ == '__main__':
    main()

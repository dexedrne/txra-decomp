#!/usr/bin/env python3
"""Package the Linux PC executable as a reproducible archive; never includes the ROM or game data.

    python3 tools/package_pc.py              (after tools/build_pc.py or make recomp)

Writes build/release/txra-pc-linux-x86_64.tar.gz, SHA256SUMS and receipt.json. The
stripped executable is scanned against the player's ROM (counts only) and packaging
fails if it reproduces any ROM data. Outside a git checkout, set SOURCE_DATE_EPOCH and
TXRA_SOURCE_COMMIT so the archive date and receipt match the source revision.
"""
import argparse
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parent.parent
NAME = 'txra-pc-linux-x86_64'
ROM_SHA1 = '4197339d4add74bb40ed02a8fba5e58096afb487'


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def run(command):
    return subprocess.run(command, check=True, capture_output=True, text=True).stdout


def glibc_floor(executable):
    versions = set(re.findall(r'GLIBC_(\d+(?:\.\d+)+)', run(['objdump', '-T', str(executable)])))
    if not versions:
        raise SystemExit('No versioned glibc symbols found; is this a dynamically linked Linux build?')
    return max(versions, key=lambda v: tuple(map(int, v.split('.'))))


def needed_libraries(executable):
    return re.findall(r'\(NEEDED\)\s+Shared library: \[([^\]]+)\]', run(['readelf', '-d', str(executable)]))


def source_commit():
    if os.environ.get('TXRA_SOURCE_COMMIT'):
        return os.environ['TXRA_SOURCE_COMMIT']
    try:
        return run(['git', '-C', str(ROOT), 'rev-parse', '--short', 'HEAD']).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def source_date():
    if os.environ.get('SOURCE_DATE_EPOCH'):
        return int(os.environ['SOURCE_DATE_EPOCH'])
    try:
        return int(run(['git', '-C', str(ROOT), 'log', '-1', '--format=%ct']).strip())
    except (OSError, subprocess.CalledProcessError, ValueError):
        return 0


def write_archive(staging, archive, mtime):
    """Sorted entries, fixed owner/date/modes and a gzip header without a timestamp."""
    data = io.BytesIO()
    with tarfile.open(fileobj=data, mode='w', format=tarfile.USTAR_FORMAT) as tar:
        for path in [staging, *sorted(staging.rglob('*'))]:
            info = tar.gettarinfo(str(path), arcname=str(Path(NAME) / path.relative_to(staging)))
            info.uid = info.gid = 0
            info.uname = info.gname = ''
            info.mtime = mtime
            info.mode = 0o755 if path.is_dir() or os.access(path, os.X_OK) else 0o644
            if path.is_file():
                with path.open('rb') as f:
                    tar.addfile(info, f)
            else:
                tar.addfile(info)
    with archive.open('wb') as raw, gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0,
                                                   compresslevel=9) as out:
        out.write(data.getvalue())


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--binary', type=Path, default=ROOT / 'build/txra-pc')
    p.add_argument('--output-dir', type=Path, default=ROOT / 'build/release')
    p.add_argument('--rom', type=Path, default=ROOT / 'baserom.gba',
                   help='player ROM used only to verify the package reproduces none of its data')
    p.add_argument('--generated', type=Path, default=ROOT / 'build/generated.c')
    a = p.parse_args()
    binary = a.binary.resolve()
    header = binary.read_bytes()[:20] if binary.is_file() else b''
    if header[:4] != b'\x7fELF' or header[4] != 2 or header[18:20] != b'\x3e\x00':
        p.error(f'{binary} is not an x86-64 Linux executable; build it with tools/build_pc.py first.')
    rom = a.rom.resolve()
    if not rom.is_file() or hashlib.sha1(rom.read_bytes()).hexdigest() != ROM_SHA1:
        p.error('Supply the supported ROM with --rom so the package can be checked for ROM data.')
    for tool in ('strip', 'objdump', 'readelf'):
        if not shutil.which(tool):
            p.error(f'Missing packaging tool: {tool}')
    output = a.output_dir.resolve()
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.package-', dir=output) as temp:
        staging = Path(temp) / NAME
        staging.mkdir()
        staging.chmod(0o755)
        executable = staging / 'txra-pc'
        shutil.copyfile(binary, executable)
        subprocess.run(['strip', '--strip-all', str(executable)], check=True)
        executable.chmod(0o755)
        floor = glibc_floor(executable)
        readme = (ROOT / 'docs/release/README-PC-linux.txt').read_text().replace('@GLIBC@', floor)
        (staging / 'README-PC.txt').write_text(readme)
        for name in ('LICENSE', 'LICENSE.txt', 'LICENSE.md', 'COPYING'):
            if (ROOT / name).is_file():
                shutil.copyfile(ROOT / name, staging / name)
        files = sorted(path for path in staging.iterdir() if path.is_file())
        for path in files:
            if path.suffix.lower() in ('.gba', '.sav', '.bin') or hashlib.sha1(path.read_bytes()).hexdigest() == ROM_SHA1:
                raise SystemExit(f'Refusing to package {path.name}')
        scan_json = Path(temp) / 'scan.json'
        command = [sys.executable, str(ROOT / 'tools/scan_embedded_rom.py'), str(executable), '--rom', str(rom),
                   '--max-data-bytes', '0', '--json', str(scan_json)]
        if a.generated.is_file():
            command += ['--generated', str(a.generated)]
        if subprocess.run(command, stdout=subprocess.DEVNULL).returncode:
            raise SystemExit('The executable reproduces ROM data (see the scan above); nothing was packaged.')
        scan = json.loads(scan_json.read_text())
        (staging / 'SHA256SUMS').write_text(''.join(f'{sha256(path)}  {path.name}\n' for path in files))
        archive = output / f'{NAME}.tar.gz'
        partial = Path(temp) / archive.name
        write_archive(staging, partial, source_date())
        os.replace(partial, archive)
        digest = sha256(archive)
        (output / 'SHA256SUMS').write_text(f'{digest}  {archive.name}\n')
        target = scan['files'][0]
        receipt = {
            'package': archive.name,
            'size': archive.stat().st_size,
            'sha256': digest,
            'contents': {path.name: {'size': path.stat().st_size, 'sha256': sha256(path)}
                         for path in [*files, staging / 'SHA256SUMS']},
            'glibc_floor': floor,
            'needed_libraries': needed_libraries(executable),
            'built_with': {'compiler': run(['cc', '--version']).splitlines()[0],
                           'sdl2': run(['pkg-config', '--modversion', 'sdl2']).strip()},
            'source_commit': source_commit(),
            'source_date_epoch': source_date(),
            'rom_included': False,
            'rom_data_scan': {
                'window_bytes': scan['window'],
                'min_distinct_byte_values': scan['min_distinct'],
                'rom_data_bytes': scan['rom_data_bytes'],
                'data_windows_checked': target['data']['windows_checked'],
                'data_windows_found': target['data']['windows_found'],
                'rom_data_bytes_in_executable': target['data']['rom_bytes_covered'],
                'rom_code_bytes_in_executable': target['code']['rom_bytes_covered'],
                'generated_c': scan.get('generated'),
            },
        }
        (output / 'receipt.json').write_text(json.dumps(receipt, indent=1) + '\n')
    print(f'{archive} ({receipt["size"]} bytes) sha256 {digest}')
    print(f'glibc >= {floor}; needs {", ".join(receipt["needed_libraries"])}; ROM data bytes embedded: 0')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Package the Windows build (no ROM or game data) as a zip with checksums and a receipt.

Run after `python3 tools/build_pc.py --target windows ...`. Writes
<output>/txra-pc-windows-x86_64.zip, <output>/SHA256SUMS (for the zip) and
<output>/txra-pc-windows-x86_64.receipt.json. Inside the zip, one folder holds
txra-pc.exe, SDL2.dll, README-PC.txt, SDL2-LICENSE.txt, LICENSE (when the
repository has one) and SHA256SUMS for those files.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import time
import zipfile

NAME = 'txra-pc-windows-x86_64'
ROM_SHA1 = '4197339d4add74bb40ed02a8fba5e58096afb487'


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def tool_version(command):
    try:
        return subprocess.run(command, capture_output=True, text=True, check=True).stdout.splitlines()[0]
    except (OSError, subprocess.CalledProcessError, IndexError):
        return None


def sdl_version(header):
    text = header.read_text()
    parts = [re.search(rf'#define SDL_{k}\s+(\d+)', text).group(1) for k in ('MAJOR_VERSION', 'MINOR_VERSION', 'PATCHLEVEL')]
    return '.'.join(parts)


def pe_facts(exe):
    """DLL imports and subsystem from objdump, when available."""
    objdump = shutil.which('x86_64-w64-mingw32-objdump')
    if not objdump:
        return {}
    text = subprocess.run([objdump, '-p', str(exe)], capture_output=True, text=True, check=True).stdout
    subsystem = re.search(r'^Subsystem\s+\S+\s+\((.*)\)', text, re.M)
    stack = re.search(r'^SizeOfStackReserve\s+(\S+)', text, re.M)
    return {'dll_imports': sorted(set(re.findall(r'DLL Name: (\S+)', text)), key=str.lower),
            'subsystem': subsystem.group(1) if subsystem else None,
            'stack_reserve_bytes': int(stack.group(1), 16) if stack else None}


def main():
    root = Path(__file__).resolve().parent.parent
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--build', type=Path, default=root / 'build/windows', help='folder with txra-pc.exe and SDL2.dll')
    p.add_argument('--sdl2-root', type=Path, help='SDL2 SDK triplet folder used for the build (for its version)')
    p.add_argument('--output', type=Path, default=root / 'build/release/windows')
    p.add_argument('--commit', help='source commit recorded in the receipt')
    p.add_argument('--attach', action='append', default=[], metavar='KEY=FILE.json',
                   help='embed a JSON result (for example a ROM-bytes scan or test run) in the receipt')
    a = p.parse_args()
    build = a.build.resolve()
    exe, dll = build / 'txra-pc.exe', build / 'SDL2.dll'
    for path in (exe, dll):
        if not path.is_file():
            p.error(f'Missing {path.name}; run tools/build_pc.py --target windows first')
    sdk = a.sdl2_root or os.environ.get('TXRA_SDL2_WINDOWS_ROOT')
    sdl = sdl_version(Path(sdk) / 'include/SDL2/SDL_version.h') if sdk else None
    readme = (root / 'runtime/windows/README-PC.txt').read_text()
    readme = readme.replace('{rom_sha1}', ROM_SHA1).replace('{sdl_version}', sdl or '2')
    files = {'txra-pc.exe': exe.read_bytes(), 'SDL2.dll': dll.read_bytes(),
             'README-PC.txt': readme.replace('\r\n', '\n').replace('\n', '\r\n').encode()}
    if (build / 'SDL2-LICENSE.txt').is_file():
        files['SDL2-LICENSE.txt'] = (build / 'SDL2-LICENSE.txt').read_bytes()
    for name in ('LICENSE', 'LICENSE.txt', 'LICENSE.md'):
        if (root / name).is_file():
            files[name] = (root / name).read_bytes()
    sums = ''.join(f'{sha256(data)}  {name}\n' for name, data in sorted(files.items()))
    files['SHA256SUMS'] = sums.encode()

    # Reproducible archive: fixed order, timestamps and permissions.
    stamp = time.gmtime(int(os.environ.get('SOURCE_DATE_EPOCH', time.time())))[:6]
    stamp = max(stamp, (1980, 1, 1, 0, 0, 0))
    output = a.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    archive = output / f'{NAME}.zip'
    temporary = archive.with_suffix('.zip.tmp')
    with zipfile.ZipFile(temporary, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, data in sorted(files.items()):
            info = zipfile.ZipInfo(f'{NAME}/{name}', stamp)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, data)
    os.replace(temporary, archive)
    package = archive.read_bytes()
    (output / 'SHA256SUMS').write_text(f'{sha256(package)}  {archive.name}\n')

    receipt = {
        'package': archive.name,
        'bytes': len(package),
        'sha256': sha256(package),
        'source_commit': a.commit,
        'contents': {name: {'bytes': len(data), 'sha256': sha256(data)} for name, data in sorted(files.items())},
        'contains_rom_or_game_data': False,
        'required_rom_sha1': ROM_SHA1,
        'executable': pe_facts(exe),
        'toolchain': {'compiler': tool_version(['x86_64-w64-mingw32-gcc', '--version']),
                      'binutils': tool_version(['x86_64-w64-mingw32-ld', '--version']),
                      'sdl2': sdl},
    }
    for item in a.attach:
        key, _, path = item.partition('=')
        receipt[key] = json.loads(Path(path).read_text())
    (output / f'{NAME}.receipt.json').write_text(json.dumps(receipt, indent=1) + '\n')
    print(f'{archive} {len(package)} bytes sha256 {sha256(package)}')


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Build a desktop executable; the player's ROM remains a separate private input."""
import argparse
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def publish(source, destination, strip=None):
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(prefix='.txra-build-', dir=destination.parent, delete=False) as f:
        temporary = Path(f.name)
    try:
        shutil.copy2(source, temporary)
        if strip:
            subprocess.run([strip, '--strip-debug', str(temporary)], check=True)
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)


def main():
    root = Path(__file__).resolve().parent.parent
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('rom', type=Path, nargs='?', default=root / 'baserom.gba',
                   help='supported player-owned cartridge dump (default: baserom.gba)')
    p.add_argument('--target', choices=('native', 'windows'), default='native')
    p.add_argument('--output', type=Path)
    p.add_argument('--sdl2-root', type=Path, help='Windows SDL2 SDK triplet folder containing include/, lib/, bin/')
    a = p.parse_args()
    rom = a.rom.resolve()
    if not rom.is_file() or hashlib.sha1(rom.read_bytes()).hexdigest() != '4197339d4add74bb40ed02a8fba5e58096afb487':
        p.error('Supply the supported 4 MiB player-owned ROM (see README).')
    output = (a.output or Path('build/windows/txra-pc.exe' if a.target == 'windows' else 'build/txra-pc')).resolve()
    os.chdir(root)
    compiler = 'x86_64-w64-mingw32-gcc' if a.target == 'windows' else 'cc'
    dependencies = (compiler,) if a.target == 'windows' else ('make', compiler, 'pkg-config')
    for tool in dependencies:
        if not shutil.which(tool):
            p.error(f'Missing build dependency: {tool}')
    sdk = None
    if a.target == 'windows':
        sdk = a.sdl2_root or os.environ.get('TXRA_SDL2_WINDOWS_ROOT')
        if not sdk:
            candidates = sorted((root / 'build/toolchains').glob('SDL2-*/x86_64-w64-mingw32'))
            sdk = candidates[-1] if candidates else None
        if not sdk:
            p.error('Supply the SDL2 MinGW development SDK with --sdl2-root or TXRA_SDL2_WINDOWS_ROOT.')
        sdk = Path(sdk).resolve()
        for name in ('include/SDL2/SDL.h', 'lib/libSDL2.dll.a', 'bin/SDL2.dll'):
            if not (sdk / name).is_file():
                p.error(f'Incomplete Windows SDL2 SDK: missing {name}')
    else:
        subprocess.run(['pkg-config', '--exists', 'sdl2'], check=True)
    subprocess.run([sys.executable, 'recomp/generate.py', '--rom', str(rom)], check=True)
    if a.target == 'windows':
        directory = root / 'build/windows'
        directory.mkdir(parents=True, exist_ok=True)
        flags = ['-O2', '-std=c11', '-Wall', '-Wextra', '-Wno-misleading-indentation', '-Iruntime', '-DSDL_MAIN_HANDLED']
        subprocess.run([compiler, *flags, '-O1', '-c', 'build/generated.c', '-o', str(directory / 'generated.o')], check=True)
        built = directory / 'txra-pc.exe'
        subprocess.run([compiler, *flags, '-I' + str(sdk / 'include/SDL2'),
                        *map(str, sorted((root / 'runtime').glob('*.c'))), str(directory / 'generated.o'),
                        '-L' + str(sdk / 'lib'), '-lSDL2', '-o', str(built)], check=True)
        publish(sdk / 'bin/SDL2.dll', output.parent / 'SDL2.dll')
        license_path = sdk.parent / 'LICENSE.txt'
        if license_path.is_file():
            publish(license_path, output.parent / 'SDL2-LICENSE.txt')
        stripper = shutil.which('x86_64-w64-mingw32-strip')
    else:
        subprocess.run(['make', '--assume-old=build/generated.c', f'PYTHON={sys.executable}', 'recomp'], check=True)
        built = root / 'build/txra-pc'
        stripper = shutil.which('strip')
    publish(built, output, stripper)
    print(f'Built {output.name}. Run it with --rom /path/to/your/cartridge.gba')
    print('No ROM or extracted assets are packaged. ' +
          ('Keep the included SDL2.dll beside the Windows executable.' if sdk else 'SDL2 is a system runtime dependency.'))


if __name__ == '__main__':
    main()

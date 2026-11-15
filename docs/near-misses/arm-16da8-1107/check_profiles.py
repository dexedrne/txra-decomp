#!/usr/bin/env python3
"""Compile the one recovered candidate with the two existing ARM profiles.

Uses the installed compilers only. No search, ROM read, installation or generated
map update. Temporary objects are removed. Source-derived synthetic assembly
checks the original APCS admission path without substituting any private bytes.
Run with the existing project Python environment (capstone is required).
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from types import SimpleNamespace

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(HERE), str(ROOT/'tools'), str(ROOT/'recomp')]
from check_semantics import Arm, Memory, POOLS
import reloc
import rank_targets

START, END = 0x08016DA8, 0x08017E68
TOOLS = Path(os.environ.get('TXRA_TOOLS', Path.home()/'opt'))
ARM = str(TOOLS/'arm-gnu-toolchain-14.3.rel1-x86_64-arm-none-eabi/bin/arm-none-eabi-')
HISTORICAL = TOOLS/'agbcc/agbcc_arm'


def run(args):
    result = subprocess.run(list(map(str, args)), capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(result.stderr)
    return result


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def original_fixture(folder):
    text = (ROOT/'asm/program.s').read_text().split('func_08016DA8:')[1].split('func_08017E68:')[0]
    def replace_pool(match):
        address, count = (int(v, 16) for v in match.groups())
        assert count % 4 == 0
        return '.word ' + ', '.join(hex(POOLS[0x08000000+address+i]) for i in range(0, count, 4))
    text = re.sub(r'\.incbin "baserom.gba", (0x[0-9a-fA-F]+), (0x[0-9a-fA-F]+)', replace_pool, text)
    assert '.incbin' not in text  # Never let an assembler attempt a ROM read.
    source, obj, binary = folder/'original.s', folder/'original.o', folder/'original.bin'
    source.write_text('.syntax unified\n.text\n.arm\n.global func_08016DA8\nfunc_08016DA8:\n'+text)
    run([ARM+'as', '-mcpu=arm7tdmi', source, '-o', obj])
    run([ARM+'objcopy', '-O', 'binary', '-j', '.text', obj, binary])
    code = binary.read_bytes()
    assert len(code) == END-START
    # Every source instruction keeps its original offset after assembling all
    # branch-around-pool regions. Confirm label addresses independently via nm.
    labels = dict((name, int(offset, 16)) for offset, kind, name in
                  (line.split() for line in run([ARM+'nm', '-a', obj]).stdout.splitlines()
                   if len(line.split()) == 3))
    for name in re.findall(r'^(loc_[0-9A-F]+|data_[0-9A-F]+):', text, re.M):
        assert labels[name]+START == int(name.split('_')[1], 16)
    program = SimpleNamespace(rom=b'\0'*(START-0x08000000)+code,
        by_start={START: {'mode': 'arm', 'end': hex(END)}},
        insns={START: [SimpleNamespace(addr=a) for a in sorted(Arm(Memory()).code)]})
    reason = rank_targets.arm_leaf_rejection(program, START)
    assert reason is None, reason
    return {'extent_bytes_including_pools': len(code), 'instructions': len(program.insns[START]),
            'pool_bytes': len(POOLS)*4, 'admission_rejection': reason,
            'pool_bindings': 'target addresses verified on private host; synthetic memory contents'}


def compile_profile(profile, folder, candidate):
    source = HERE/candidate
    assembly, obj, binary = (folder/(profile+suffix) for suffix in ('.s', '.o', '.bin'))
    if profile == 'arm':
        preprocessed = folder/'candidate.i'
        run([ARM+'gcc', '-E', '-P', source, '-o', preprocessed])
        run([HISTORICAL, preprocessed, '-O2', '-mthumb-interwork', '-o', assembly])
        compiler = HISTORICAL
        flags = ['-O2', '-mthumb-interwork']
    else:
        flags = ['-O2', '-marm', '-mcpu=arm7tdmi', '-mno-thumb-interwork']
        run([ARM+'gcc', '-S', source, *flags, '-o', assembly])
        compiler = Path(ARM+'gcc')
    run([ARM+'as', '-mcpu=arm7tdmi', assembly, '-o', obj])
    run([ARM+'objcopy', '-O', 'binary', '-j', '.text', obj, binary])
    raw = binary.read_bytes()
    function = reloc.function_bytes(obj, raw, 'func_08016DA8', ARM+'objdump')
    table = {}
    for symbol in re.findall(r'extern u8 (g_[0-9A-F]{8})\[\];', source.read_text()):
        table[symbol] = (int(symbol[2:], 16), False)
    linked = reloc.link_bytes(obj, function, START, table, ARM+'objdump')
    # Independent linker agrees with the existing strict relocation helper.
    elf, linked_binary = folder/(profile+'.elf'), folder/(profile+'-linked.bin')
    run([ARM+'ld', '-Ttext='+hex(START), '--entry=func_08016DA8',
         *['--defsym='+name+'='+hex(value[0]) for name, value in table.items()], obj, '-o', elf])
    run([ARM+'objcopy', '-O', 'binary', '-j', '.text', elf, linked_binary])
    assert linked == linked_binary.read_bytes()
    assembly_text = assembly.read_text()
    calls = re.findall(r'^\s*bl\s+([^\n]+)', assembly_text, re.M)
    return {'candidate': candidate, 'profile': profile, 'flags': flags, 'compiler_sha256': sha(compiler),
            'source_sha256': sha(source), 'text_bytes': len(function),
            'target_extent_bytes': END-START, 'same_extent': len(function) == END-START,
            'out_of_line_calls': calls, 'strict_relocation_and_linker_agree': True,
            'address_linked_text_sha256': hashlib.sha256(linked).hexdigest(),
            'exact_match': False, 'rom_comparison_performed': False}


def main():
    with tempfile.TemporaryDirectory(prefix='txra-16da8-profiles-') as folder:
        folder = Path(folder)
        result = {'original_source_fixture': original_fixture(folder),
                  'profiles': [compile_profile(p, folder, candidate)
                               for candidate in ('func_08016DA8.c', 'func_08016DA8_match.c')
                               for p in ('arm', 'modern-arm')]}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()

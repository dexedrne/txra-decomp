#!/usr/bin/env python3
"""Resolve relocations of one standalone compiled function at its ROM address.

Calls (BL) to mapped functions, absolute words naming functions, globals spelled with
their address (gUnk_03001234), and local labels inside the function's own section
(switch tables) are resolved here so the bytes can be compared without a linker script.
Anything else is rejected rather than guessed.
"""
import re, struct, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'recomp'))

# Reviewed aliases: every name has at least two agreeing accessors in
# docs/MATCH4-LAYOUTS.md. Legacy address names remain available.
DATA_SYMBOLS = {'gSaveStaging': 0x03005FE0, 'gKeysHeld': 0x030014BC,
                'gOamShadow': 0x03005B40, 'gEepromGeometry': 0x03007B50}

def symbols(prog):
    """{name: (address, is_thumb_code)} for every mapped function and its provisional name."""
    table = {name: (address, False) for name, address in DATA_SYMBOLS.items()}
    for a, f in prog.by_start.items():
        thumb = f['mode'] == 'thumb'
        table['func_%08X' % a] = (a, thumb)
        if not thumb:
            # Existing runtime names deliberately prefer their Thumb veneers.
            # ARM callers need a distinct name for the underlying ARM entry.
            table['arm_func_%08X' % a] = (a, False)
        # THUMB callers reach runtime routines through THUMB entry veneers; prefer those.
        if thumb or prog.name(a) not in table: table[prog.name(a)] = (a, thumb)
    # Address-only names come from literals referenced by mapped instructions.
    # Retain the older spelling so already installed C continues to build.
    import draft
    for addr in prog.by_start:
        for value in draft.pool_words(prog, addr).values():
            if value is not None and draft.region(value) and (value & ~1) not in prog.by_start:
                for prefix in ('g_', 'gUnk_'):
                    table[prefix + '%08X' % value] = (value, False)
    return table

def resolve(sym, table):
    if sym in table: return table[sym]
    m = re.fullmatch(r'[A-Za-z_]\w*?_?([0-9A-Fa-f]{8})', sym)
    if m and re.fullmatch(r'(?:g_|gUnk_)[0-9A-Fa-f]{8}', sym):
        address = int(m.group(1), 16)
        if 0x02000000 <= address < 0x0E010000: return address, False
    raise ValueError('unknown symbol ' + sym)

def parse(text):
    """[(offset, type, symbol)] from `objdump -r` output for .text."""
    out, section = [], None
    for line in text.splitlines():
        m = re.match(r'RELOCATION RECORDS FOR \[(.+)\]', line)
        if m: section = m.group(1); continue
        m = re.match(r'^([0-9a-f]{8})\s+(R_ARM_\w+)\s+(\S+)\s*$', line)
        if m:
            if section != '.text': raise ValueError('relocation outside .text: ' + str(section))
            out.append((int(m.group(1), 16), m.group(2), m.group(3)))
    return out

def relocate(code, relocs, start, table):
    data = bytearray(code)
    for off, kind, sym in relocs:
        if off < 0 or off + 4 > len(data): raise ValueError('relocation past the end of the function')
        if kind in ('R_ARM_THM_CALL', 'R_ARM_THM_PC22'):
            target, thumb = resolve(sym, table)
            if not thumb: raise ValueError('BL to non-THUMB target ' + sym)
            hi, lo = struct.unpack_from('<HH', data, off)
            if hi & 0xF800 != 0xF000 or lo & 0xF800 != 0xF800:
                raise ValueError('invalid THUMB BL relocation')
            addend = ((hi & 0x7FF) << 12) | ((lo & 0x7FF) << 1)
            if addend & (1 << 22): addend -= 1 << 23
            # REL stores target - PC in the instruction; the standard -4
            # placeholder represents a zero symbol addend.
            d = target + addend + 4 - (start + off + 4)
            if d & 1 or not -(1 << 22) <= d < (1 << 22): raise ValueError('BL out of range ' + sym)
            struct.pack_into('<HH', data, off, 0xF000 | ((d >> 12) & 0x7FF), 0xF800 | ((d >> 1) & 0x7FF))
        elif kind == 'R_ARM_V4BX':
            # ARM7TDMI implements BX. This is a linker compatibility hint,
            # not a symbol addend; preserve the assembler's instruction.
            word = struct.unpack_from('<I', data, off)[0]
            if ((start | off) & 3 or sym != '*ABS*' or word & 0x0FFFFFF0 != 0x012FFF10
                    or word >> 28 == 15):
                raise ValueError('invalid ARM BX compatibility relocation')
        elif kind in ('R_ARM_JUMP24', 'R_ARM_CALL', 'R_ARM_PC24'):
            target, thumb = resolve(sym, table)
            word = struct.unpack_from('<I', data, off)[0]
            if thumb or target & 3:
                raise ValueError('ARM branch to non-ARM target ' + sym)
            if word & 0x0E000000 != 0x0A000000 or word >> 28 == 15:
                raise ValueError('invalid ARM branch relocation')
            if ((kind == 'R_ARM_CALL' and not word & 0x01000000)
                    or (kind == 'R_ARM_JUMP24' and word & 0x01000000)):
                raise ValueError('ARM branch relocation has wrong link bit')
            addend = (word & 0xFFFFFF) << 2
            if addend & (1 << 25):
                addend -= 1 << 26
            # ARM REL placeholders contain -8 for a zero symbol addend.
            distance = target + addend - (start + off)
            if (start + off) & 3 or distance & 3 or not -(1 << 25) <= distance < (1 << 25):
                raise ValueError('ARM branch out of range ' + sym)
            struct.pack_into('<I', data, off, (word & 0xFF000000) | ((distance >> 2) & 0xFFFFFF))
        elif kind == 'R_ARM_ABS32':
            addend = struct.unpack_from('<I', data, off)[0]
            if sym == '.text':
                value = start + addend
            elif sym.startswith('.'):
                raise ValueError('reference to section ' + sym + ' (separate data is not supported)')
            else:
                target, thumb = resolve(sym, table)
                value = target + addend + (1 if thumb and sym in table else 0)
            struct.pack_into('<I', data, off, value & 0xffffffff)
        else:
            raise ValueError('unsupported relocation ' + kind)
    return bytes(data)

def link_bytes(obj, code, start, table, objdump):
    """Bytes of `code` (the object's .text) with every relocation resolved at `start`."""
    text = subprocess.run([str(objdump), '-r', str(obj)], check=True, capture_output=True, text=True, timeout=60).stdout
    return relocate(code, parse(text), start, table)


def declarations(prog, addr):
    """Provisional address names for mapped literal references, without semantic guesses."""
    import draft
    values = set(draft.pool_words(prog, addr).values())
    return '\n'.join('extern u8 g_%08X[];' % v for v in sorted(v for v in values if v is not None)
                     if draft.region(v) and (v & ~1) not in prog.by_start)


def function_bytes(obj, code, name, objdump):
    """Exclude section alignment after the compiler's .size boundary."""
    listing = subprocess.run([str(objdump), '-t', str(obj)], check=True, capture_output=True, text=True, timeout=60).stdout
    for line in listing.splitlines():
        fields = line.split()
        if len(fields) >= 5 and fields[-1] == name and '.text' in fields:
            offset = int(fields[0], 16)
            size = int(fields[-2], 16)
            if offset != 0 or not 0 < size <= len(code):
                raise ValueError('invalid standalone function span ' + name)
            return code[:size]
    raise ValueError('missing function symbol ' + name)

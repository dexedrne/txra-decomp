#!/usr/bin/env python3
"""ROM-free differential check: compiled structured C vs textual ARM execution.

No lifted C is the oracle. Instructions are parsed from asm/program.s at run
time. Pool target addresses were verified on the private host. Memory contents
remain synthetic. This is not a byte-match or a real-state runtime test.
"""
import ctypes
import argparse
import hashlib
import json
import random
import re
import subprocess
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
MASK = 0xffffffff
POOLS = {
    0x08017198: 0x030001B8, 0x0801719C: 0x030057A0,
    0x080176B4: 0x03005F70, 0x080176B8: 0x030057A0,
    0x080176BC: 0x03005F80, 0x080176C0: 0x03002A18,
    0x080176C4: 0x03001B28, 0x080176C8: 0x03000DF8,
    0x080176CC: 0x03005F58, 0x080176D0: 0x030055F8,
    0x080176D4: 0x0804F330, 0x080176D8: 0x030021C4,
    0x08017AA0: 0x030021C4, 0x08017AA4: 0x03000670,
    0x08017E0C: 0x030021C4, 0x08017E10: 0x03000DE0,
    0x08017E14: 0x03000AD0, 0x08017E18: 0x03000ADC,
    0x08017E1C: 0x03000670,
}
REG = {**{f'r{i}': i for i in range(16)}, 'sb': 9, 'sl': 10,
       'fp': 11, 'ip': 12, 'sp': 13, 'lr': 14, 'pc': 15}


def signed(x, bits=32):
    x &= (1 << bits)-1
    return x-(1 << bits) if x >> (bits-1) else x


class Memory:
    def __init__(self):
        self.regions = {0x02000000: bytearray(0x40000),
                        0x03000000: bytearray(0x8000),
                        0x07F00000: bytearray(0x300000)}

    def region(self, a, width):
        for base, data in self.regions.items():
            if base <= a and a+width <= base+len(data):
                return data, a-base
        raise AssertionError(f'out of synthetic memory: {a:08x}/{width}')

    def read(self, a, width=4):
        data, off = self.region(a, width)
        assert a % width == 0, (hex(a), width)
        return int.from_bytes(data[off:off+width], 'little')

    def write(self, a, value, width=4):
        data, off = self.region(a, width)
        assert a % width == 0, (hex(a), width)
        data[off:off+width] = (value & ((1 << (width*8))-1)).to_bytes(width, 'little')


class Arm:
    def __init__(self, memory):
        text = (ROOT/'asm/program.s').read_text().split('func_08016DA8:')[1].split('func_08017E68:')[0]
        self.code = {}
        for line in text.splitlines():
            m = re.fullmatch(r'\s+(.*?) @ ([0-9A-F]{8})', line)
            if m:
                insn, address = m.groups()
                op, args = insn.split(' ', 1)
                self.code[int(address, 16)] = (op, args)
        self.mem = memory
        self.r = [0x12340000+i for i in range(16)]
        self.r[13] = 0x03007E00
        self.r[14] = 0xF0000000
        self.n = self.z = self.c = self.v = False
        self.visited = set()

    def value(self, arg):
        arg = arg.strip()
        if arg.startswith('#'):
            return int(arg[1:], 0) & MASK
        if ',' in arg:
            reg, shift = arg.split(',', 1)
            kind, count = shift.strip().split()
            value, count = self.value(reg), self.value(count)
            if kind == 'lsl': return (value << count) & MASK
            if kind == 'asr': return (signed(value) >> count) & MASK
            raise AssertionError(kind)
        return self.r[REG[arg]]

    def flags(self, a, b, subtract):
        result = (a-b if subtract else a+b) & MASK
        self.n, self.z = bool(result >> 31), result == 0
        self.c = a >= b if subtract else a+b > MASK
        self.v = bool(((a ^ b) if subtract else ~(a ^ b)) & (a ^ result) & 0x80000000)
        return result

    def run(self):
        pc = 0x08016DA8
        steps = 0
        while pc != 0xF0000000:
            steps += 1
            assert steps < 2000000, 'nonterminating fixture'
            self.visited.add(pc)
            op, args = self.code[pc]
            self.r[15] = pc+8
            next_pc = pc+4
            conditions = {'eq': self.z, 'ne': not self.z, 'lt': self.n != self.v,
                          'le': self.z or self.n != self.v, 'gt': not self.z and self.n == self.v,
                          'ge': self.n == self.v, 'mi': self.n, 'hi': self.c and not self.z}
            suffix = next((s for s in conditions if op.endswith(s)), None)
            if suffix:
                op = op[:-2]
                if not conditions[suffix]:
                    pc = next_pc
                    continue
            if op == 'b':
                next_pc = int(args.removeprefix('loc_'), 16)
            elif op == 'bx':
                next_pc = self.value(args)
            elif op == 'push' or op.startswith('ldm'):
                if op == 'push':
                    names = args.strip('{}').split(', ')
                    base = self.r[13]-4*len(names)
                    for i, reg in enumerate(names): self.mem.write(base+4*i, self.value(reg))
                    self.r[13] = base
                else:
                    base_reg, names = args.split(', {')
                    names = names.rstrip('}').split(', ')
                    base = self.value(base_reg)
                    if op == 'ldmda': base -= 4*(len(names)-1)
                    elif op == 'ldmdb': base -= 4*len(names)
                    else: assert op == 'ldm'
                    values = [self.mem.read(base+4*i) for i in range(len(names))]
                    for reg, val in zip(names, values): self.r[REG[reg]] = val
            elif op.startswith(('ldr', 'str')):
                dest, address = args.split(', [')
                address = address.rstrip(']')
                base, *offset = address.split(', ', 1)
                a = (self.value(base) + (self.value(offset[0]) if offset else 0)) & MASK
                width = 1 if op.endswith('b') else 2 if op.endswith(('h', 'sh')) else 4
                if op.startswith('ldr'):
                    value = POOLS[a] if base == 'pc' else self.mem.read(a, width)
                    if op == 'ldrsh': value = signed(value, 16) & MASK
                    self.r[REG[dest]] = value
                else:
                    self.mem.write(a, self.value(dest), width)
            else:
                parts = args.split(', ')
                dest, rest = parts[0], parts[1:]
                if op in ('cmp', 'cmn'):
                    self.flags(self.value(dest), self.value(', '.join(rest)), op == 'cmp')
                else:
                    a = self.value(rest[0])
                    b = self.value(', '.join(rest[1:])) if len(rest) > 1 and op != 'mla' else 0
                    if op == 'mov': result = self.value(', '.join(rest))
                    elif op == 'mvn': result = ~a
                    elif op == 'and': result = a & b
                    elif op == 'add': result = a+b
                    elif op == 'adds': result = self.flags(a, b, False)
                    elif op == 'sub': result = a-b
                    elif op == 'rsb': result = b-a
                    elif op == 'mul': result = a*b
                    elif op == 'mla': result = a*self.value(rest[1])+self.value(rest[2])
                    elif op == 'lsl': result = a << b
                    elif op in ('asr', 'asrs'):
                        result = signed(a) >> b
                        if op == 'asrs': self.n, self.z = result < 0, result == 0
                    else: raise AssertionError((hex(pc), op, args))
                    self.r[REG[dest]] = result & MASK
            pc = next_pc
        return steps


def build_library(directory, candidate):
    header = '''
extern unsigned char ewram[], iwram[], table[];
static __inline__ unsigned char *synthetic_address(unsigned int a) {
    if (a >= 0x07F00000u && a < 0x08200000u) return table + a-0x07F00000u;
    if (a >= 0x03000000u && a < 0x03008000u) return iwram + a-0x03000000u;
    if (a >= 0x02000000u && a < 0x02040000u) return ewram + a-0x02000000u;
    __builtin_trap();
}
#define MEM8(a) (*synthetic_address(a))
#define MEM16(a) (*(u16 *)synthetic_address(a))
#define MEM32(a) (*(u32 *)synthetic_address(a))
#define DEPTH_SCRATCH 0x030055F8u
#define SPECIAL_BASE 0x03000AD0u
#define SPECIAL_WIDTH 0x03000ADCu
'''
    (directory/'synthetic_memory.h').write_text(header)
    source = directory/'harness.c'
    source.write_text('#define TXRA_SYNTHETIC\n#include "'+candidate+'"\n'
                      '#include <stddef.h>\n'
                      'unsigned char ewram[0x40000],iwram[0x8000],table[0x300000];\n'
                      'typedef char point_size[(sizeof(TrackPoint)==28)?1:-1];\n'
                      'typedef char face_size[(sizeof(TrackFace)==56)?1:-1];\n'
                      'typedef char packet_size[(sizeof(TrackPacket)==32)?1:-1];\n'
                      'u32 probe_midpoint(u32 a,u32 b){return midpoint(a,b);}\n'
                      'u32 probe_point(u32 a){return point_address(a);}\n'
                      'u32 probe_winding(u32 a){return winding(a);}\n'
                      'void probe_clamp(void){near_expand_and_clamp();}\n'
                      'int probe_visible(u32 a){return visible(a);}\n'+
                      '\n'.join(f'typedef char offset_{record}_{field}[(offsetof({record},{field})=={offset})?1:-1];'
                                for record, fields in [
                                    ('TrackPoint', [('sx', 16), ('sy', 20), ('depth', 24)]),
                                    ('TrackFace', [('index', 4), ('u', 20), ('v', 36), ('count', 52)]),
                                    ('TrackPacket', [('x', 0), ('y', 8), ('u', 16), ('v', 20),
                                                     ('count', 24), ('kind', 26), ('next', 28)])]
                                for field, offset in fields)+'\n')
    library = directory/'candidate.so'
    subprocess.run(['gcc', '-std=gnu89', '-O2', '-Wall', '-Wextra', '-Werror',
                    '-fno-strict-aliasing', '-shared', '-fPIC', '-I'+str(HERE),
                    '-I'+str(directory), str(source), '-o', str(library)], check=True)
    return ctypes.CDLL(str(library))


def fixture(seed, mode, depths=None, kind=None, tick=None, screen=None, empty=False, faces=1):
    rng = random.Random(seed)
    m = Memory()
    # Distinct stale bytes expose rejected-packet writes and unwritten fields.
    m.regions[0x02000000][:] = b'\xa5'*0x40000
    m.regions[0x03000000][:] = b'\x5a'*0x8000
    tick = rng.randrange(0x100000000) if tick is None else tick
    m.write(0x030001B8, tick)
    m.write(0x030021C4, 0x02019EF0)
    m.write(0x03000DE0, 0)
    for i in range(256): m.write(0x03000670+4*i, 0x02018000 if i % 2 and not empty else 0)
    for slot in range(32): m.write(0x02033B70+1344*slot, 0, 2)
    for a in (0x03005F70, 0x03005F74, 0x03005F78): m.write(a, rng.randint(-500, 500))
    for a in (0x03005F80, 0x03005F84): m.write(a, rng.randint(-15, 15))
    m.write(0x03005F88, rng.randint(-1000, 2000))
    for a in (0x03002A18, 0x03001B28, 0x03000DF8, 0x03005F58):
        m.write(a, rng.choice([0, 4096, -4096, 2048, -127, 0x7fffffff]))
    # Synthetic reciprocal values deliberately vary across every index.
    table = m.regions[0x07F00000]
    pattern = b''.join(rng.choice([1, 128, 4096, 65536, 0xffffffff]).to_bytes(4, 'little') for _ in range(1024))
    table[:] = pattern * (len(table)//len(pattern))
    ring = (tick-29) & 31
    count = 1 if mode in ('near', 'far') else 7
    for n in range(count):
        f = 0x02033B70 + 1344*((ring+n*3) & 31)
        m.write(f, kind if kind is not None else rng.choice([1, 2, 3, 4, 9]), 2)
        for j in range(4):
            index = n*4+j
            p = 0x02014000+28*index
            m.write(f+4+4*j, index)
            for c in range(3): m.write(p+4*c, rng.choice([rng.randint(-2000, 2000), 0x7fffffff, 0x80000000]))
            for off in (16, 20): m.write(p+off, rng.choice([0, 119, 120, 159, 160, -1, -67, 187, 32767, -32768, rng.randint(-200, 300)]))
            if screen is not None:
                m.write(p+16, screen[0][j])
                m.write(p+20, screen[1][j])
            d = depths[j] if depths is not None else rng.choice([768, 1000, 40000]) if mode == 'far' else rng.choice([-1, 0, 1, 766, 767, 768, 0x80000000, 0x7fffffff])
            m.write(p+24, d)
            for off in (20, 36): m.write(f+off+4*j, rng.getrandbits(32))
        m.write(f+52, rng.randrange(65536), 2)
        for face in range(1, faces):
            for offset in range(0, 56, 2):
                m.write(f+56*face+offset, m.read(f+offset, 2), 2)
        m.write(f+56*faces, 0, 2)
    return m


def check_primitives(lib):
    """Fixed expected results, not another spelling of the candidate algorithm."""
    checks = 0
    lib.probe_midpoint.argtypes = [ctypes.c_uint, ctypes.c_uint]
    lib.probe_midpoint.restype = ctypes.c_uint
    for a, b, expected in [(0xffffffff, 1, 0), (0x7fffffff, 1, 0xc0000000),
                           (0xfffffffd, 0, 0xfffffffe),
                           (0x80000000, 0x80000000, 0), (3, 4, 3)]:
        assert lib.probe_midpoint(a, b) == expected
        checks += 1
    lib.probe_point.argtypes = [ctypes.c_uint]
    lib.probe_point.restype = ctypes.c_uint
    for index, expected in [(0, 0x02014000), (1, 0x0201401c),
                            (0xffffffff, 0x02013fe4), (0x40000000, 0x02014000)]:
        assert lib.probe_point(index) == expected
        checks += 1
    ram = (ctypes.c_ubyte*0x40000).in_dll(lib, 'ewram')
    iram = (ctypes.c_ubyte*0x8000).in_dll(lib, 'iwram')
    def put(a, value, width=2):
        buffer, offset = (ram, a-0x02000000) if a < 0x03000000 else (iram, a-0x03000000)
        buffer[offset:offset+width] = (value & ((1 << (width*8))-1)).to_bytes(width, 'little')
    packet = 0x02019ef0
    put(0x030021c4, packet, 4)
    lib.probe_winding.argtypes = [ctypes.c_uint]
    lib.probe_winding.restype = ctypes.c_uint
    for coords, expected in [(([10, 20, 20, 10], [10, 10, 20, 20]), 0xffffff9c),
                             (([10, 10, 20, 20], [10, 20, 20, 10]), 100),
                             (([0]*4, [0]*4), 0)]:
        for axis, values in enumerate(coords):
            for i, v in enumerate(values): put(packet+axis*8+i*2, v)
        assert lib.probe_winding(packet) == expected
        checks += 1
    # A visible x and visible y at DIFFERENT corners do not pass visibility.
    for x, y, expected in [([0, 200, 200, 200], [-1, 0, -1, -1], 0),
                           ([119]*4, [159]*4, 1), ([120]*4, [159]*4, 0),
                           ([119]*4, [160]*4, 0), ([-1]*4, [0]*4, 0)]:
        for i in range(4):
            put(packet+i*2, x[i]); put(packet+8+i*2, y[i])
        assert lib.probe_visible(packet) == expected
        checks += 1
    # Narrowing happens before signed clamps, and only corners 0/1 expand.
    for i, value in enumerate([32768, 32767, -67, 187]): put(packet+i*2, value)
    for i, value in enumerate([-32768, -175, -176, 336]): put(packet+8+i*2, value)
    lib.probe_clamp()
    expected = [186, -66, -66, 186, 334, -174, -174, 334]
    actual = [signed(int.from_bytes(bytes(ram[0x19ef0+2*i:0x19ef2+2*i]), 'little'), 16) for i in range(8)]
    assert actual == expected, actual
    checks += 1
    # Check the test executor's condition arithmetic independently too.
    arm = Arm(Memory())
    assert arm.flags(0x7fffffff, 0xffffffff, True) == 0x80000000
    assert arm.n and arm.v and not arm.c and not arm.z
    assert arm.flags(0xffffffff, 1, False) == 0
    assert arm.z and arm.c and not arm.n and not arm.v
    checks += 2
    return checks


def compare(lib, memory, label):
    symbols = {0x02000000: 'ewram', 0x03000000: 'iwram', 0x07F00000: 'table'}
    for base, data in memory.regions.items():
        ctypes.memmove((ctypes.c_ubyte*len(data)).in_dll(lib, symbols[base]), bytes(data), len(data))
    arm = Arm(memory)
    arm.run()
    lib.func_08016DA8()
    for base, expected in memory.regions.items():
        actual = bytes((ctypes.c_ubyte*len(expected)).in_dll(lib, symbols[base]))
        # Frame contents are compiler-dependent and not observable after return.
        spans = [(0, 0x7D00), (0x7E00, len(expected))] if base == 0x03000000 else [(0, len(expected))]
        differences = [i for lo, hi in spans for i in range(lo, hi) if actual[i] != expected[i]] if any(
            actual[lo:hi] != expected[lo:hi] for lo, hi in spans) else []
        if differences:
            i = differences[0]
            raise AssertionError(f'{label}: at {base+i:08x}: C {actual[i]:02x}, ARM {expected[i]:02x}')
    return arm.visited


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', default='func_08016DA8.c',
                        choices=['func_08016DA8.c', 'func_08016DA8_match.c',
                                 'func_08016DA8_projection.c'])
    candidate = parser.parse_args().candidate
    visited = set()
    count = 0
    with tempfile.TemporaryDirectory(prefix='txra-16da8-check-') as folder:
        lib = build_library(Path(folder), candidate)
        primitive_checks = check_primitives(lib)
        cases = []
        for i in range(48):
            for mode in ('near', 'far', 'mixed'):
                cases.append((f'{mode}-{i}', (i, mode), {}))
        for k in (1, 2, 3, 4, 9):
            for d in (-1, 0, 766, 767, 768, 0x7fffffff, 0x80000000):
                cases.append((f'boundary-{k}-{d}', (700+k, 'near'), {'depths': [d]*4, 'kind': k}))
        for tick in (0, 5, 6, 28, 29, 31, 32, 0xffffffff):
            cases.append((f'ring-{tick}', (99, 'mixed'), {'tick': tick}))
        for kind in (1, 2, 3, 4):
            for empty in (False, True):
                cases.append((f'direct-insert-{kind}-{empty}', (123, 'far'),
                              {'kind': kind, 'depths': [1000]*4, 'empty': empty,
                               'screen': ([10, 20, 20, 10], [10, 10, 20, 20])}))
        for mode in ('near', 'far'):
            for kind in (1, 3):
                cases.append((f'two-faces-{mode}-{kind}', (123, mode),
                              {'kind': kind, 'faces': 2,
                               'depths': [767 if mode == 'near' else 1000]*4,
                               'screen': ([10, 20, 20, 10], [10, 10, 20, 20])}))
        for label, args, kwargs in cases:
            visited.update(compare(lib, fixture(*args, **kwargs), label))
            count += 1
    all_code = set(Arm(Memory()).code)
    result = {'candidate': candidate, 'differential_fixtures': count, 'fixed_expected_checks': primitive_checks,
              'compile_time_size_checks': 3, 'compile_time_offset_checks': 14,
              'executed_instruction_addresses': len(visited),
              'instruction_addresses': len(all_code),
              'not_executed': [f'{a:08X}' for a in sorted(all_code-visited)],
              'source_sha256': hashlib.sha256((HERE/candidate).read_bytes()).hexdigest(),
              'assembly_sha256': hashlib.sha256((ROOT/'asm/program.s').read_bytes()).hexdigest(),
              'rom_used': False, 'byte_match_verified': False}
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()

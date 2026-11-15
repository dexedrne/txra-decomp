#!/usr/bin/env python3
"""Differential check: run two C sources of func_080064A4 on the same synthetic states.

Both sources are compiled unchanged for i386 (32-bit pointers), linked freestanding with
harness32.c, with every g_XXXXXXXX symbol placed at its GBA address.  Synthetic states are
generated from a seed (structured voices, command/event streams, envelopes, effects).  The
outputs (all mapped regions plus the ordered hook-call log) must be byte-identical.
No ROM bytes are read.  usage: diff32.py <reference.c> <candidate.c> [states] [seed] [--fix-pcm-step]

--fix-pcm-step applies one documented correction to the 11/11 reference before building it:
its rest-sample block stores the sample step to voice offset 0x40, while the original
instructions (08007314: str r0,[r4] with r4 = sp+76 = 0x030077A0 + 72*i) store it at 0x30.
"""
import hashlib, json, random, re, struct, subprocess, sys, tempfile
from pathlib import Path
HERE = Path(__file__).resolve().parent
REGIONS = [(0x02000000, 0x10000), (0x03000000, 0x8000), (0x04000000, 0x1000),
           (0x0801F000, 0x1000), (0x08332000, 0x92000)]

def build(src, folder, tag):
    text = Path(src).read_text()
    syms = sorted(set(re.findall(r'\bg_([0-9A-F]{8})\b', text)))
    flags = ['-m32', '-O1', '-fwrapv', '-fno-strict-aliasing', '-ffreestanding', '-fno-pic', '-fno-pie',
             '-fno-stack-protector', '-fno-asynchronous-unwind-tables', '-fno-builtin', '-w']
    subprocess.run(['gcc', *flags, '-c', src, '-o', folder / (tag + '.o')], check=True)
    subprocess.run(['gcc', *flags, '-c', HERE / 'harness32.c', '-o', folder / 'h.o'], check=True)
    exe = folder / (tag + '.elf')
    subprocess.run(['ld', '-m', 'elf_i386', '-static', '-nostdlib', '-Ttext=0x10000000', '-e', '_start',
                    *['--defsym=g_%s=0x%s' % (s, s) for s in syms if s not in ('08332E9C', '08332EA0')],
                    '--defsym=g_08332E9C=0x08332E9C', '--defsym=g_08332EA0=0x08332EA0',
                    folder / 'h.o', folder / (tag + '.o'), '-o', exe], check=True)
    return exe

class Mem:
    def __init__(self):
        self.r = {b: bytearray(n) for b, n in REGIONS}
    def put(self, addr, data):
        for b, n in REGIONS:
            if b <= addr and addr + len(data) <= b + n:
                self.r[b][addr - b:addr - b + len(data)] = data; return
        raise ValueError('unmapped %08X' % addr)
    def w32(self, a, v): self.put(a, struct.pack('<I', v & 0xFFFFFFFF))
    def w16(self, a, v): self.put(a, struct.pack('<H', v & 0xFFFF))
    def image(self, frames):
        return struct.pack('<I', frames) + b''.join(bytes(self.r[b]) for b, _ in REGIONS)

def state(rng):
    m = Mem()
    heap = [0x02000100]
    def alloc(n):
        a = heap[0]; heap[0] = (a + n + 3) & ~3; assert heap[0] < 0x0200F000; return a
    # fade table (0..256), frequency tables, sample steps, samples
    for k in range(9): m.w32(0x0801FF00 + 4 * k, 32 * k)
    for k in range(256 + 97): m.put(0x083C0FAC + k, bytes([rng.randrange(256)]))
    for k in range(-200, 100): m.w32(0x08333324 + 4 * k, rng.randrange(1 << 20))
    for k in range(16):
        m.w32(0x083B8698 + 16 * k + 4, rng.randrange(8, 4000))
    # envelopes: pairs, with 254 jumps and a 255 hold
    def envelope():
        n = rng.randrange(1, 6); vals = []
        for _ in range(n): vals += [rng.randrange(0, 254), rng.randrange(1, 4)]
        if rng.random() < 0.4: vals += [254, 2 * rng.randrange(0, n)]
        vals += [255, 0]
        a = alloc(2 * len(vals))
        for k, v in enumerate(vals): m.w16(a + 2 * k, v)
        return a, len(vals)
    insts = []
    for k in range(8):
        a = alloc(36)
        m.w32(a + 0, rng.randrange(256)); m.w32(a + 4, rng.randrange(65536)); m.w32(a + 8, rng.randrange(256))
        for off in (16, 24, 32):
            m.w32(a + off, envelope()[0] if rng.random() < 0.7 else 0)
        m.w32(0x083C19C0 + 4 * k, a); insts.append(a)
    durations = alloc(64)
    for k in range(16): m.w32(durations + 4 * k, rng.randrange(1, 4))
    m.w32(0x03007580, durations)
    def events():
        n = rng.randrange(1, 6); out = []
        for _ in range(n):
            out += [rng.choice([0x60] + list(range(0, 96))), rng.randrange(8), rng.randrange(16)]
        out += [0x65]
        a = alloc(len(out) + 4)
        m.put(a, bytes(out))
        return a, n
    def commands():
        out = []
        for _ in range(rng.randrange(0, 4)):
            c = rng.choice([0x67, 0x69, 0x60, 0x66])
            out += {0x67: [0x67, rng.randrange(16)], 0x69: [0x69, rng.randrange(1, 512)],
                    0x60: [0x60, 0, 0], 0x66: [0x66, rng.randrange(100)]}[c]
        ev, _ = events()
        if rng.random() < 0.15: out += [0x61]
        else: out += [0x64, ev, rng.randrange(-12, 13), rng.randrange(0, 3)]
        out += [0x61]
        a = alloc(4 * len(out))
        for k, v in enumerate(out): m.w32(a + 4 * k, v)
        return a
    for v in range(8):
        base = 0x03007770 + 72 * v
        f = [0] * 18
        f[0] = 1 if rng.random() < 0.8 else rng.randrange(3)
        f[1] = rng.randrange(2)
        f[2] = 0
        f[4] = rng.randrange(0, 3)
        f[5] = rng.randrange(96); f[6] = rng.randrange(65536); f[7] = rng.randrange(8)
        f[8] = commands() if rng.random() < 0.9 else 0
        if rng.random() < 0.6:
            ev, n = events(); f[9] = ev; f[3] = 3 * rng.randrange(n)
        f[10] = rng.randrange(-12, 13); f[11] = rng.randrange(0, 3)
        for k in (12, 14, 16):
            f[k] = 0; f[k + 1] = rng.randrange(1, 3)
        for k, val in enumerate(f): m.w32(base + 4 * k, val)
    for e in range(4):
        base = 0x03007590 + 12 * e
        if rng.random() < 0.7:
            recs = []
            for _ in range(rng.randrange(1, 4)):
                recs += [rng.randrange(1, 4)] + [rng.randrange(256) for _ in range(4)]
            if rng.random() < 0.3: recs += [254, 253, 0, 0, 0]
            recs += [255, 0, 0, 0, 0]
            a = alloc(2 * len(recs) + 8)
            for k, val in enumerate(recs): m.w16(a + 2 * k, val)
            m.w32(base, a); m.w32(base + 4, -5); m.w32(base + 8, rng.randrange(0, 2))
    m.w32(0x030079B4, rng.choice([0, 1, 1])); m.w32(0x03007400, rng.randrange(16))
    m.w32(0x030079B0, rng.randrange(8)); m.w32(0x03007570, 1 if rng.random() < 0.15 else 0)
    m.w32(0x03006A98, rng.randrange(2)); m.w32(0x03007574, rng.randrange(256))
    m.w32(0x03007404, rng.choice([0, 128, 256, 300])); m.w16(0x04000080, rng.randrange(65536))
    for k in range(352): m.put(0x03007410 + k, bytes([rng.randrange(256)]))
    return m

FIX_OLD = 'VOICE_arpeggio_cursor(i) = g_08333324[95 - VOICE_note(i)];'
FIX_NEW = 'VOICE_volume_cursor(i) = g_08333324[95 - VOICE_note(i)];'

def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    fix = '--fix-pcm-step' in sys.argv
    ref, cand = args[0], args[1]
    n = int(args[2]) if len(args) > 2 else 400
    seed = int(args[3]) if len(args) > 3 else 1115
    with tempfile.TemporaryDirectory(prefix='diff32-') as td:
        td = Path(td)
        ref_src = ref
        if fix:
            text = Path(ref).read_text()
            assert text.count(FIX_OLD) == 1
            ref_src = td / 'reference.c'
            ref_src.write_text(text.replace(FIX_OLD, FIX_NEW))
        a, b = build(ref_src, td, 'ref'), build(cand, td, 'cand')
        rng = random.Random(seed); same = 0; fails = []
        calls = 0
        for k in range(n):
            img = state(rng).image(rng.randrange(1, 5))
            ra = subprocess.run([str(a)], input=img, capture_output=True)
            rb = subprocess.run([str(b)], input=img, capture_output=True)
            if ra.returncode == 0 and ra.stdout == rb.stdout and rb.returncode == 0:
                same += 1
                calls += struct.unpack_from('<I', ra.stdout, len(ra.stdout) - 260)[0]
            else:
                fails.append((k, ra.returncode, rb.returncode, len(ra.stdout), len(rb.stdout)))
        print(json.dumps(dict(reference=str(ref), reference_sha256=hashlib.sha256(Path(ref).read_bytes()).hexdigest(), reference_fix_pcm_step=fix,
                              candidate=str(cand), candidate_sha256=hashlib.sha256(Path(cand).read_bytes()).hexdigest(),
                              states=n, seed=seed, identical=same, failures=fails[:10], logged_events=calls,
                              rom_used=False), indent=1))
        return 0 if same == n else 1

if __name__ == '__main__':
    sys.exit(main())

def debug(ref, cand, idx, seed=1):
    with tempfile.TemporaryDirectory(prefix='diff32-') as td:
        td = Path(td)
        a, b = build(ref, td, 'ref'), build(cand, td, 'cand')
        rng = random.Random(seed)
        for k in range(idx + 1):
            st = state(rng); fr = rng.randrange(1, 5)
        img = st.image(fr)
        ra = subprocess.run([str(a)], input=img, capture_output=True).stdout
        rb = subprocess.run([str(b)], input=img, capture_output=True).stdout
        pos = 0
        print('frames', fr)
        for base, size in REGIONS:
            x, y = ra[pos:pos + size], rb[pos:pos + size]
            for o in range(0, size, 4):
                if x[o:o+4] != y[o:o+4]:
                    print('%08X ref %s cand %s init %s' % (base + o, x[o:o+4].hex(), y[o:o+4].hex(), bytes(st.r[base][o:o+4]).hex()))
            pos += size
        print('log ref ', struct.unpack_from('<16I', ra, pos + 4))
        print('log cand', struct.unpack_from('<16I', rb, pos + 4))

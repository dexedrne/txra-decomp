#!/usr/bin/env python3
"""Readable pseudo-C drafts lifted from the recompiler's per-instruction semantic C.

Each mapped instruction is decoded by generate.decode exactly as the static
recompiler emits it; the resulting statement is parsed back into a small IR and
rendered with registers as locals, unused flags folded away, memory helpers as
typed loads/stores at known addresses, and calls by name. Drafts are build output.
"""
import json, re, struct, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import generate

BASE = 0x08000000
CONDS = ('eq', 'ne', 'cs', 'cc', 'mi', 'pl', 'vs', 'vc', 'hi', 'ls', 'ge', 'lt', 'gt', 'le', '', 'nv')
BIOS = {0: 'SoftReset', 1: 'RegisterRamReset', 2: 'Halt', 3: 'Stop', 4: 'IntrWait', 5: 'VBlankIntrWait', 6: 'Div',
        8: 'Sqrt', 9: 'ArcTan', 10: 'ArcTan2', 11: 'CpuSet', 12: 'CpuFastSet', 14: 'BgAffineSet', 15: 'ObjAffineSet',
        17: 'LZ77UnCompWram', 18: 'LZ77UnCompVram', 19: 'HuffUnComp', 20: 'RLUnCompWram', 21: 'RLUnCompVram'}
# Provisional runtime names from docs/COMPILER.md; everything else keeps its address name.
LIBRARY = {0x08000218: '__divsi3', 0x0800027C: '__udivsi3', 0x08018E1C: 'memcpy'}
SIZE_TYPE = {1: 'u8', 2: 'u16', 4: 'u32'}
TYPEDEFS = ('typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;\n'
            'typedef signed char s8; typedef signed short s16; typedef signed int s32;\n'
            'typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;\n')

def fname(addr):
    return LIBRARY.get(addr, 'func_%08X' % addr)

def hexv(v):
    return str(v) if v < 10 else '0x%X' % v

def regname(r):
    return {13: 'sp', 14: 'lr', 15: 'pc'}.get(r, 'r%d' % r)

def reglist(mask, extra=()):
    return '{' + ', '.join([regname(i) for i in range(16) if mask & (1 << i)] + list(extra)) + '}'

def hardware_names(root=Path('.')):
    """I/O register names from the docs table: {address: name}."""
    names = {}
    path = root / 'docs/HARDWARE.md'
    if path.exists():
        for a, n in re.findall(r'^\| ([0-9A-F]{8}) \| ([^|]+?) \|', path.read_text(), re.M):
            names[int(a, 16)] = re.sub(r'[^A-Za-z0-9_]+', '_', n.split(' ')[0]).strip('_')
    return names

def region(addr):
    top = addr >> 24
    return {2: 'EWRAM', 3: 'IWRAM', 4: 'I/O', 5: 'palette', 6: 'VRAM', 7: 'OAM', 8: 'ROM', 9: 'ROM', 13: 'EEPROM'}.get(top)

# ---------------------------------------------------------------- IR

class Insn:
    """One instruction: address, raw word, assembly text and a lifted IR tuple."""
    def __init__(self, addr, size, raw, asm, ir, cond=14, flags=False):
        self.addr, self.size, self.raw, self.asm, self.ir, self.cond, self.flags = addr, size, raw, asm, ir, cond, flags
    def __repr__(self):
        return '%08X %s' % (self.addr, self.asm)

def imm(v):
    return ('#', v & 0xffffffff)

ALU2 = ('and', 'eor', 'lsl', 'lsr', 'asr', 'adc', 'sbc', 'ror', 'tst', 'neg', 'cmp', 'cmn', 'orr', 'mul', 'bic', 'mvn')
SHIFTS = ('lsl', 'lsr', 'asr', 'ror')

def thumb_ir(stmt, pc, w):
    """Parse one generate.decode THUMB statement into (asm, ir, flags)."""
    m = re.fullmatch(r'thumb\(g,(\d+),(\d+),(\d+),(\d+),(\d+)\);', stmt)
    if m:
        G, op, x, y, z = map(int, m.groups())
        if G == 0:
            if op < 3:
                n = x if x or op == 0 else 32
                if op == 0 and x == 0:
                    return 'movs %s, %s' % (regname(z), regname(y)), ('mov', z, y), True
                return '%ss %s, %s, #%d' % (SHIFTS[op], regname(z), regname(y), n), ('alu', z, SHIFTS[op], y, imm(n)), True
            b = imm(x & 7) if x & 16 else x & 7
            o = 'sub' if x & 8 else 'add'
            if b == imm(0) and o == 'add':
                return 'adds %s, %s, #0' % (regname(z), regname(y)), ('mov', z, y), True
            return '%ss %s, %s, %s' % (o, regname(z), regname(y), '#%d' % (x & 7) if x & 16 else regname(x & 7)), ('alu', z, o, y, b), True
        if G == 1:
            name = ('mov', 'cmp', 'add', 'sub')[op]
            text = '%s%s %s, #%d' % (name, '' if op == 1 else 's', regname(x), y)
            if op == 0: return text, ('mov', x, imm(y)), True
            if op == 1: return text, ('cmp', x, imm(y)), True
            return text, ('alu', x, name, x, imm(y)), True
        if G == 2:
            name, rd, rs = ALU2[op], y, x
            text = '%s%s %s, %s' % (name, '' if name in ('tst', 'cmp', 'cmn') else 's', regname(rd), regname(rs))
            if name in ('tst', 'cmp', 'cmn'): return text, (name, rd, rs), True
            if name == 'neg': return text, ('alu', rd, 'sub', imm(0), rs), True
            if name == 'mvn': return text, ('alu', rd, 'mvn', rs, rs), True
            return text, ('alu', rd, name, rd, rs), True
        if G == 3:
            rd, rs = y, x
            if op == 0: return 'add %s, %s' % (regname(rd), regname(rs)), ('alu', rd, 'add', rd, rs), False
            if op == 1: return 'cmp %s, %s' % (regname(rd), regname(rs)), ('cmp', rd, rs), True
            if op == 2:
                if rd == 15: return 'mov pc, %s' % regname(rs), ('jump', rs), False
                return 'mov %s, %s' % (regname(rd), regname(rs)), ('mov', rd, rs), False
            return 'bx %s' % regname(rs), ('bx', rs), False
        if G == 4:
            name = ('str', 'strh', 'strb', 'ldrsb', 'ldr', 'ldrh', 'ldrb', 'ldrsh')[op]
            size = (4, 2, 1, 1, 4, 2, 1, 2)[op]
            text = '%s %s, [%s, %s]' % (name, regname(z), regname(y), regname(x))
            if op < 3: return text, ('store', z, size, y, x), False
            return text, ('load', z, size, op in (3, 7), y, x), False
        if G == 5:
            size = 1 if op & 2 else 4
            off = x if op & 2 else x * 4
            name = ('str', 'ldr', 'strb', 'ldrb')[op]
            text = '%s %s, [%s, #%d]' % (name, regname(z), regname(y), off)
            if op & 1: return text, ('load', z, size, False, y, imm(off)), False
            return text, ('store', z, size, y, imm(off)), False
        if G == 6:
            text = '%s %s, [%s, #%d]' % ('ldrh' if op else 'strh', regname(z), regname(y), x * 2)
            if op: return text, ('load', z, 2, False, y, imm(x * 2)), False
            return text, ('store', z, 2, y, imm(x * 2)), False
        if G == 7:
            text = '%s %s, [sp, #%d]' % ('ldr' if op else 'str', regname(x), y)
            if op: return text, ('load', x, 4, False, 13, imm(y)), False
            return text, ('store', x, 4, 13, imm(y)), False
        if G == 8:
            if op: return 'add %s, sp, #%d' % (regname(x), y), ('alu', x, 'add', 13, imm(y)), False
            return 'add %s, pc, #%d' % (regname(x), y), ('mov', x, imm(((pc + 4) & ~3) + y)), False
        if G == 9:
            return '%s sp, #%d' % ('sub' if op else 'add', x), ('sp', -x if op else x), False
        if G == 10:
            if op: return 'pop ' + reglist(x | (y << 15)), ('pop', x | (y << 15)), False
            return 'push ' + reglist(x | (y << 14)), ('push', x | (y << 14)), False
        if G == 11:
            return '%s %s!, %s' % ('ldmia' if op else 'stmia', regname(x), reglist(y)), ('ldm' if op else 'stm', x, y), False
    m = re.fullmatch(r'g->r\[(\d+)\]=rd32\(g,\(\(g->r\[15\]\+4\)&~3u\)\+(\d+)\);g->r\[15\]=\d+u;', stmt)
    if m:
        rd, off = map(int, m.groups())
        at = ((pc + 4) & ~3) + off
        return 'ldr %s, [pc, #%d] @ =0x%08X' % (regname(rd), off, at), ('pool', rd, at), False
    m = re.fullmatch(r'g->r\[14\]=0x([0-9a-f]+); g->r\[15\]=\d+u;', stmt)
    if m: return 'bl (high half)', ('blhi', int(m.group(1), 16)), False
    m = re.fullmatch(r'\{u32 dst=g->r\[14\]\+(\d+)u; g->r\[14\]=\d+u; branch\(g,dst,true\);\}', stmt)
    if m: return 'bl (low half)', ('bllo', int(m.group(1))), False
    m = re.fullmatch(r'g->r\[15\]=cond\(g,(\d+)\)\?(\d+)u:\d+u;', stmt)
    if m:
        c, t = int(m.group(1)), int(m.group(2)) & 0xffffffff
        return 'b%s 0x%08X' % (CONDS[c], t), ('b', t), False, c
    m = re.fullmatch(r'g->r\[15\]=\d+u; bios\(g,(\d+)\);', stmt)
    if m: return 'swi #0x%X' % int(m.group(1)), ('swi', int(m.group(1))), False
    m = re.fullmatch(r'g->r\[15\]=(-?\d+)u;', stmt)
    if m:
        t = int(m.group(1)) & 0xffffffff
        return 'b 0x%08X' % t, ('b', t), False
    return '.hword 0x%04X' % w, ('unknown', '.hword 0x%04X' % w), False

def arm_op2(I, field):
    if I:
        rot = (field >> 8) * 2
        v = ((field & 255) >> rot | (field & 255) << (32 - rot)) & 0xffffffff if rot else field & 255
        return imm(v), '#0x%X' % v
    rm, kind = field & 15, (field >> 5) & 3
    if field & 16:
        rs = field >> 8
        return ('shift', rm, SHIFTS[kind], rs), '%s, %s %s' % (regname(rm), SHIFTS[kind], regname(rs))
    n = (field >> 7) & 31
    if n == 0 and kind == 0: return rm, regname(rm)
    if n == 0: n = 32 if kind in (1, 2) else 0
    if n == 0 and kind == 3: return ('shift', rm, 'rrx', imm(1)), regname(rm) + ', rrx'
    return ('shift', rm, SHIFTS[kind], imm(n)), '%s, %s #%d' % (regname(rm), SHIFTS[kind], n)

ARMDP = ('and', 'eor', 'sub', 'rsb', 'add', 'adc', 'sbc', 'rsc', 'tst', 'teq', 'cmp', 'cmn', 'orr', 'mov', 'bic', 'mvn')

def arm_ir(stmt, pc, w):
    m = re.fullmatch(r'if\(cond\(g,(\d+)\)\)\{(.*)\}else g->r\[15\]=\d+u;', stmt)
    if not m: return '.word 0x%08X' % w, ('unknown', '.word 0x%08X' % w), False, 14
    c, body = int(m.group(1)), m.group(2)
    cs = CONDS[c]
    args = lambda s: list(map(int, re.findall(r'-?\d+', s.split('(', 1)[1])))
    if body.startswith('branch(g,reg(g,'):
        r = int(re.search(r'reg\(g,(\d+)\)', body).group(1))
        return 'bx%s %s' % (cs, regname(r)), ('bx', r), False, c
    if 'bios(g,' in body:
        n = int(re.search(r'bios\(g,(\d+)\)', body).group(1))
        return 'swi%s #0x%X' % (cs, n), ('swi', n), False, c
    mm = re.fullmatch(r'(g->r\[14\]=\d+u;)?g->r\[15\]=(\d+)u;(?:fn_\w+\(g\);)?', body)
    if mm:
        t = int(mm.group(2))
        if mm.group(1): return 'bl%s 0x%08X' % (cs, t), ('call', t), False, c
        return 'b%s 0x%08X' % (cs, t), ('b', t), False, c
    if body.startswith('arm_dp('):
        I, op, S, rn, rd, field, *_ = args(body)
        src, stext = arm_op2(I, field)
        name = ARMDP[op]
        if name in ('tst', 'teq', 'cmp', 'cmn'):
            return '%s%s %s, %s' % (name, cs, regname(rn), stext), ({'teq': 'teq'}.get(name, name), rn, src), True, c
        text = '%s%s%s %s, %s' % (name, cs, 's' if S else '', regname(rd), (regname(rn) + ', ' if name not in ('mov', 'mvn') else '') + stext)
        if rd == 15 and name == 'mov': return text, ('jump', src), False, c
        if name == 'mov': return text, ('mov', rd, src), bool(S), c
        if name == 'mvn': return text, ('alu', rd, 'mvn', src, src), bool(S), c
        if name == 'rsb': return text, ('alu', rd, 'sub', src, rn), bool(S), c
        if name == 'rsc': return text, ('alu', rd, 'sbc', src, rn), bool(S), c
        return text, ('alu', rd, name, rn, src), bool(S), c
    if body.startswith('arm_mem('):
        I, P, U, B, W, L, rn, rd, off = args(body)
        if I: o, otext = arm_op2(0, off)
        else: o, otext = imm(off), '#%d' % off
        if not U:
            o = ('neg', o) if not isinstance(o, tuple) or o[0] != '#' else imm(-off)
            otext = '-' + otext
        size = 1 if B else 4
        name = ('ldr' if L else 'str') + ('b' if B else '')
        text = '%s%s %s, [%s%s, %s%s' % (name, cs, regname(rd), regname(rn), '' if P else ']', otext, ']' + ('!' if W else '') if P else '')
        if not P or W: return text, ('unknown', text), False, c
        if L and not B and not I and rn == 15:
            return text, ('pool', rd, pc + 8 + (off if U else -off)), False, c
        if L: return text, ('load', rd, size, False, rn, o), False, c
        return text, ('store', rd, size, rn, o), False, c
    if body.startswith('arm_half('):
        P, U, I, W, L, rn, rd, off, sh = args(body)
        o = imm(off if U else -off) if I else rn
        name = ('str', 'ldrh', 'ldrsb', 'ldrsh')[sh] if L else 'strh'
        text = '%s%s %s, [%s, %s%s]' % (name, cs, regname(rd), regname(rn), '' if U else '-', '#%d' % off if I else regname(off & 15))
        if not I: o = off & 15
        if not P or W or (not I and not U): return text, ('unknown', text), False, c
        if L: return text, ('load', rd, (2, 1, 2)[sh - 1], sh != 1, rn, o), False, c
        return text, ('store', rd, 2, rn, o), False, c
    if body.startswith('arm_block('):
        P, U, S, W, L, rn, lst = args(body)
        if rn == 13 and W and L and U and not P: return 'pop%s %s' % (cs, reglist(lst)), ('pop', lst), False, c
        if rn == 13 and W and not L and not U and P: return 'push%s %s' % (cs, reglist(lst)), ('push', lst), False, c
        name = ('ldm' if L else 'stm') + ('i' if U else 'd') + ('b' if P else 'a')
        text = '%s%s %s%s, %s' % (name, cs, regname(rn), '!' if W else '', reglist(lst))
        if U and not P: return text, ('ldm' if L else 'stm', rn, lst), False, c
        return text, ('unknown', text), False, c
    if body.startswith('arm_mul('):
        acc, _u, A, S, rd, rn, rs, rm = args(body)
        if not acc and not A:
            return 'mul%s%s %s, %s, %s' % (cs, 's' if S else '', regname(rd), regname(rm), regname(rs)), ('alu', rd, 'mul', rm, rs), bool(S), c
        if not acc:
            text = 'mla%s%s %s, %s, %s, %s' % (cs, 's' if S else '', regname(rd), regname(rm), regname(rs), regname(rn))
            return text, ('mla', rd, rm, rs, rn), bool(S), c
        text = 'long multiply'
        return text, ('unknown', text), False, c
    text = re.sub(r'\(g,', '(', body.split(';')[0])
    return text, ('unknown', text), False, c

def decode_function(rom, f):
    """Return the IR instruction list for one mapped function, in address order."""
    thumb = f['mode'] == 'thumb'
    out = []
    for a, z in f['spans']:
        at, end = int(a, 16), int(z, 16)
        while at < end:
            if thumb:
                w = struct.unpack_from('<H', rom, at - BASE)[0]
                res = thumb_ir(generate.decode(w, True, at), at, w)
            else:
                w = struct.unpack_from('<I', rom, at - BASE)[0]
                res = arm_ir(generate.decode(w, False, at), at, w)
            asm, ir, flags = res[:3]
            cond = res[3] if len(res) > 3 else 14
            if ir[0] == 'bllo' and out and out[-1].ir[0] == 'blhi':
                hi = out.pop()
                target = (hi.ir[1] + ir[1]) & 0xffffffff
                out.append(Insn(hi.addr, 4, (w << 16) | hi.raw, 'bl 0x%08X' % target, ('call', target)))
            else:
                out.append(Insn(at, 2 if thumb else 4, w, asm, ir, cond, flags))
            at += 2 if thumb else 4
    return out

def disassemble_thumb(data, start):
    """Listing for raw THUMB bytes (compiled output or a ROM slice), using the same decoder."""
    lines, at, pending = [], 0, None
    while at + 1 < len(data):
        w = struct.unpack_from('<H', data, at)[0]
        asm, ir = thumb_ir(generate.decode(w, True, start + at), start + at, w)[:2]
        if ir[0] == 'blhi':
            pending = (at, w, ir[1])
        elif ir[0] == 'bllo' and pending and pending[0] == at - 2:
            lines[-1] = '%08X: %04X%04X bl 0x%08X' % (start + pending[0], pending[1], w, (pending[2] + ir[1]) & 0xffffffff)
            pending = None; at += 2; continue
        lines.append('%08X: %04X      %s' % (start + at, w, asm))
        at += 2
    return lines

# ---------------------------------------------------------------- program-wide facts

class Program:
    """Mapped functions plus call-graph and register-use facts used by drafts and the matcher."""
    def __init__(self, root=Path('.')):
        self.root = Path(root)
        self.rom = (self.root / 'baserom.gba').read_bytes()
        self.cfg = json.loads((self.root / 'tools/rom.cfg').read_text())
        self.functions = json.loads((self.root / 'docs/map/functions.json').read_text())['functions']
        self.by_start = {int(f['start'], 16): f for f in self.functions}
        self.hw = hardware_names(self.root)
        self.insns = {s: decode_function(self.rom, f) for s, f in self.by_start.items()}
        # Reviewed Thumb long branches (rom.cfg far_jumps) are gotos, not calls.
        far = {j['source']: j['target'] for j in self.cfg.get('far_jumps', [])}
        for ins in self.insns.values():
            for i in ins:
                if i.addr in far and i.ir == ('call', far[i.addr]):
                    i.ir = ('b', far[i.addr])
        self.callers = {s: set() for s in self.by_start}
        self.callees = {s: set() for s in self.by_start}
        self.pointed = set()
        for s, ins in self.insns.items():
            for i in ins:
                if i.ir[0] == 'call':
                    t = i.ir[1]
                    self.callees[s].add(t)
                    self.callers.setdefault(t, set()).add(s)
                if i.ir[0] == 'pool':
                    v = self.word(i.ir[2])
                    if v is not None and (v & ~1) in self.by_start: self.pointed.add(v & ~1)
        for t in json.loads((self.root / 'docs/map/indirect.json').read_text()).get('transfers', []):
            for x in t.get('targets', []) + ([t['target']] if t.get('target') else []):
                self.pointed.add(int(x, 16) & ~1)
        self.matched = {BASE + m['offset']: m for m in self.cfg['matches']}
        self._params, self._returns = {}, {}

    def word(self, addr):
        if BASE <= addr < BASE + len(self.rom) - 3:
            return struct.unpack_from('<I', self.rom, addr - BASE)[0]
        return None

    def name(self, addr):
        f = self.by_start.get(addr)
        if f is not None and f['mode'] == 'thumb':
            ins = self.insns[addr]
            if len(ins) >= 1 and ins[0].ir == ('bx', 15) and addr + 4 in self.by_start and self.by_start[addr + 4]['mode'] == 'arm':
                b = self.insns[addr + 4][0].ir if self.insns[addr + 4] else None
                if b and b[0] == 'b': return fname(b[1])
            if len(ins) == 1 and ins[0].ir[0] == 'bx' and ins[0].ir[1] < 13:
                return '_call_via_' + {10: 'sl', 11: 'fp', 12: 'ip'}.get(ins[0].ir[1], 'r%d' % ins[0].ir[1])
        return fname(addr)

    def size(self, addr):
        f = self.by_start[addr]
        return int(f['end'], 16) - addr

    def params(self, addr, depth=0):
        """Registers r0-r3 read before written along the function's instructions."""
        # ARM helpers and their interworking veneers share the same ABI.
        # The veneer itself only branches, so local read-before-write inference
        # cannot recover the arguments passed by its callers.
        runtime_params = {'__divsi3': 2, '__udivsi3': 2, 'memcpy': 3}
        if self.name(addr) in runtime_params:
            return runtime_params[self.name(addr)]
        if addr in self._params: return self._params[addr]
        if addr not in self.insns or depth > 8:
            return 4 if addr not in self.insns else 0
        self._params[addr] = 0
        written, used = set(), set()
        for i in self.insns[addr]:
            reads, writes = uses(i.ir, self, depth)
            for r in reads:
                if r < 4 and r not in written: used.add(r)
            written |= set(writes)
            if i.ir[0] in ('b',) and i.cond == 14: pass
        n = max(used) + 1 if used else 0
        self._params[addr] = n
        return n

    def returns(self, addr, depth=0):
        """True when a caller reads r0 after the call, or the function leaves a dead value in r0."""
        if addr in self._returns: return self._returns[addr]
        self._returns[addr] = False
        result = False
        for c in self.callers.get(addr, ()):
            ins = self.insns.get(c, [])
            for k, i in enumerate(ins):
                if i.ir == ('call', addr):
                    for j in ins[k + 1:]:
                        if j.ir[0] in ('b', 'bx', 'jump', 'pop', 'call'): break
                        reads, writes = uses(j.ir, self, 9)
                        if 0 in reads: result = True; break
                        if 0 in writes: break
            if result: break
        if not result and depth < 6: result = self.dead_r0(addr, depth)
        self._returns[addr] = result
        return result

    def dead_r0(self, addr, depth):
        """A write to r0 that nothing reads before a return is a return value."""
        ins = self.insns.get(addr, [])
        targets = {i.ir[1] for i in ins if i.ir[0] == 'b'}
        for k, i in enumerate(ins):
            after_pop = i.ir[0] == 'bx' and k and ins[k - 1].ir[0] == 'pop' and ins[k - 1].ir[1] & (1 << i.ir[1])
            if not ((i.ir[0] == 'bx' and i.ir[1] == 14) or (i.ir[0] == 'pop' and i.ir[1] & (1 << 15)) or after_pop):
                continue
            for j in range(k - (2 if after_pop else 1), -1, -1):
                x = ins[j]
                if x.ir[0] in ('b', 'bx', 'jump') or (j + 1 < len(ins) and ins[j + 1].addr in targets and j + 1 != k): break
                reads, writes = uses(x.ir, self, 9)
                if 0 in writes:
                    if x.ir[0] == 'call' and self.returns(x.ir[1], depth + 1): return True
                    if x.ir[0] not in ('call', 'pop', 'swi'): return True
                    break
                if 0 in reads: break
        return False

def operand_regs(o):
    if isinstance(o, int): return [o]
    if o[0] == 'shift': return [o[1]] + ([o[3]] if isinstance(o[3], int) else [])
    if o[0] == 'neg': return operand_regs(o[1])
    return []

def uses(ir, prog=None, depth=0):
    """(registers read, registers written) for one IR tuple."""
    k = ir[0]
    if k == 'mov': return operand_regs(ir[2]), [ir[1]]
    if k == 'alu': return operand_regs(ir[3]) + operand_regs(ir[4]) + ([ir[3]] if ir[2] in ('adc', 'sbc') and isinstance(ir[3], int) else []), [ir[1]]
    if k == 'mla': return list(ir[2:]), [ir[1]]
    if k in ('cmp', 'cmn', 'tst', 'teq'): return operand_regs(ir[1]) + operand_regs(ir[2]), []
    if k == 'load': return [ir[4]] + operand_regs(ir[5]), [ir[1]]
    if k == 'store': return [ir[1], ir[3]] + operand_regs(ir[4]), []
    if k == 'pool': return [], [ir[1]]
    if k == 'push': return [r for r in range(16) if ir[1] & (1 << r)], []
    if k == 'pop': return [], [r for r in range(16) if ir[1] & (1 << r)]
    if k == 'ldm': return [ir[1]], [ir[1]] + [r for r in range(8) if ir[2] & (1 << r)]
    if k == 'stm': return [ir[1]] + [r for r in range(8) if ir[2] & (1 << r)], [ir[1]]
    if k == 'call':
        n = prog.params(ir[1], depth + 1) if prog is not None else 4
        return list(range(n)), [0, 1, 2, 3, 12, 14]
    if k in ('bx', 'jump'): return operand_regs(ir[1]) if not isinstance(ir[1], int) else [ir[1]], []
    if k == 'swi': return [0, 1, 2], [0, 1, 3]
    return [], []

# ---------------------------------------------------------------- rendering

def is_imm(o): return isinstance(o, tuple) and o[0] == '#'

class Lifter:
    def __init__(self, prog, addr):
        self.prog, self.addr = prog, addr
        self.f = prog.by_start[addr]
        self.ins = prog.insns[addr]
        self.thumb = self.f['mode'] == 'thumb'
        self.labels = {i.ir[1] for i in self.ins if i.ir[0] == 'b' and self.contains(i.ir[1])}
        self.consts = {}
        self.locals = set()
        self.cur_def, self.used, self.const_defs = {}, set(), set()
        # High registers saved through low ones around push/pop are frame bookkeeping, not logic.
        self.skip = set()
        for k, i in enumerate(self.ins):
            hi_lo = lambda x, d, src: x.ir[0] == 'mov' and isinstance(x.ir[2], int) and (x.ir[2] >= 8) == src and (x.ir[1] >= 8) == d
            if i.ir[0] == 'push':
                j = k - 1
                while j >= 0 and hi_lo(self.ins[j], False, True) and i.ir[1] & (1 << self.ins[j].ir[1]): self.skip.add(j); j -= 1
            if i.ir[0] == 'pop' and not i.ir[1] & (1 << 15):
                j = k + 1
                while j < len(self.ins) and hi_lo(self.ins[j], True, False) and i.ir[1] & (1 << self.ins[j].ir[2]): self.skip.add(j); j += 1

    def contains(self, t):
        return any(int(a, 16) <= t < int(z, 16) for a, z in self.f['spans'])

    def val(self, o):
        if is_imm(o): return hexv(o[1])
        if isinstance(o, int):
            if o == 13: return 'sp'
            if o == 15: return 'pc'
            self.used.add(self.cur_def.get(o))
            return regname(o)
        if o[0] == 'shift':
            _, rm, kind, n = o
            amount = str(n[1]) if is_imm(n) else self.val(n)
            self.val(rm)
            if kind == 'lsl': return '(%s << %s)' % (regname(rm), amount)
            if kind == 'lsr': return '(%s >> %s)' % (regname(rm), amount)
            if kind == 'asr': return '((s32)%s >> %s)' % (regname(rm), amount)
            if kind == 'ror': return 'ROR(%s, %s)' % (regname(rm), amount)
            return 'RRX(%s)' % regname(rm)
        if o[0] == 'neg': return '-(%s)' % self.val(o[1])
        return '?'

    def constval(self, o):
        if is_imm(o): return o[1]
        if isinstance(o, int): return self.consts.get(o)
        return None

    def const_text(self, v, pool=False):
        if v is None: return None
        name = self.prog.hw.get(v)
        if name: return '0x%08X /* REG_%s */' % (v, name)
        if (v & ~1) in self.prog.by_start and v & 1 and self.prog.by_start[v & ~1]['mode'] == 'thumb':
            return '(u32)%s /* thumb */' % self.prog.name(v & ~1)
        if v in self.prog.by_start and self.prog.by_start[v]['mode'] == 'arm':
            return '(u32)%s /* ARM */' % self.prog.name(v)
        r = region(v) if pool and v >= 0x02000000 else None
        return ('0x%08X' % v if v >= 0x02000000 else hexv(v)) + (' /* %s */' % r if r else '')

    def address(self, base, off, size, signed=False, write=False):
        """Render a typed lvalue for [base + off]."""
        t = ('s' if signed else 'u') + str(size * 8)
        if base == 13 and is_imm(off):
            name = 'sp%02X' % off[1]
            self.locals.add(name)
            return name
        b = self.constval(base)
        o = self.constval(off) if is_imm(off) else None
        if b is not None and (is_imm(off)):
            a = (b + off[1]) & 0xffffffff
            name = self.prog.hw.get(a)
            vol = 'v' if (a >> 24) == 4 else ''
            note = ' /* REG_%s */' % name if name else (' /* %s */' % region(a) if region(a) else '')
            return '*(%s%s *)0x%08X%s' % (vol, t, a, note)
        if is_imm(off):
            if off[1] == 0: return '*(%s *)%s' % (t, self.val(base))
            return '*(%s *)(%s + %s)' % (t, self.val(base), hexv(off[1]) if off[1] < 0x80000000 else '-' + hexv(-off[1] & 0xffffffff))
        return '*(%s *)(%s + %s)' % (t, self.val(base), self.val(off))

    def call_text(self, target):
        n = self.prog.params(target)
        for r in range(n): self.used.add(self.cur_def.get(r))
        args = ', '.join('r%d' % r for r in range(n))
        return '%s(%s)' % (self.prog.name(target), args)

    def cond_text(self, setter, c):
        """C condition for branch code c given the flag-setting instruction."""
        if setter is None:
            return 'FLAGS_%s' % CONDS[c].upper()
        k = setter.ir[0]
        if k in ('cmp', 'cmn'):
            a, b = self.val(setter.ir[1]), self.val(setter.ir[2])
            if k == 'cmn': b = '-(%s)' % b
            ops = {0: '==', 1: '!=', 2: '>=', 3: '<', 8: '>', 9: '<=', 10: '>=', 11: '<', 12: '>', 13: '<='}
            if c in (10, 11, 12, 13):
                sa = a if is_imm(setter.ir[1]) else '(s32)' + a
                sb = b if is_imm(setter.ir[2]) and k == 'cmp' else '(s32)' + b
                return '%s %s %s' % (sa, ops[c], sb)
            if c in ops: return '%s %s %s' % (a, ops[c], b)
            if c in (4, 5): return '(s32)(%s - %s) %s 0' % (a, b, '<' if c == 4 else '>=')
        elif k == 'tst' or k == 'teq':
            e = '(%s %s %s)' % (self.val(setter.ir[1]), '&' if k == 'tst' else '^', self.val(setter.ir[2]))
            if c in (0, 1): return '%s %s 0' % (e, '==' if c == 0 else '!=')
            if c in (4, 5): return '(s32)%s %s 0' % (e, '<' if c == 4 else '>=')
        elif k in ('alu', 'mov', 'mla'):
            r = regname(setter.ir[1])
            if c in (0, 1): return '%s %s 0' % (r, '==' if c == 0 else '!=')
            if c in (4, 5, 10, 11): return '(s32)%s %s 0' % (r, '<' if c in (4, 11) else '>=')
            if c in (12, 13): return '(s32)%s %s 0' % (r, '>' if c == 12 else '<=')
        return 'FLAGS_%s /* from %08X */' % (CONDS[c].upper(), setter.addr)

    def statement(self, i, k, prev_setter):
        """Pseudo-C for one non-branch instruction, or None to omit it."""
        ir = i.ir
        op = ir[0]
        if op == 'mov':
            rd, src = ir[1], ir[2]
            if rd == 13: return 'sp = %s;' % self.val(src)
            self.consts[rd] = self.constval(src)
            return '%s = %s;' % (regname(rd), self.const_text(src[1]) if is_imm(src) else self.val(src))
        if op == 'pool':
            v = self.prog.word(ir[2])
            self.consts[ir[1]] = v
            return '%s = %s;' % (regname(ir[1]), self.const_text(v, pool=True) if v is not None else '*(u32 *)0x%08X' % ir[2])
        if op == 'mla':
            _, rd, rm, rs, rn = ir
            self.consts[rd] = None
            return '%s = %s * %s + %s;' % (regname(rd), self.val(rm), self.val(rs), self.val(rn))
        if op == 'alu':
            _, rd, o, a, b = ir
            ca, cb = self.constval(a), self.constval(b)
            if o == 'add' and a == 13 and is_imm(b):
                self.locals.add('sp%02X' % b[1]); self.consts[rd] = None
                return '%s = (u32)&sp%02X;' % (regname(rd), b[1])
            sym = {'add': '+', 'sub': '-', 'and': '&', 'eor': '^', 'orr': '|', 'mul': '*', 'lsl': '<<', 'lsr': '>>'}
            folded = None
            if ca is not None and cb is not None and o in ('add', 'sub', 'and', 'eor', 'orr', 'lsl', 'lsr', 'mul'):
                folded = eval('(%d %s %d) & 0xffffffff' % (ca, sym[o], cb if o not in ('lsl', 'lsr') else min(cb, 63)))
            self.consts[rd] = folded
            A, Bv = self.val(a), self.val(b)
            if o in SHIFTS and is_imm(b): Bv = str(b[1])
            if isinstance(b, tuple) and b[0] == 'shift': Bv = '(%s)' % Bv
            if o == 'mvn': text = '~%s' % Bv
            elif o == 'bic': text = '%s & ~%s' % (A, Bv)
            elif o == 'asr': text = '(s32)%s >> %s' % (A, Bv)
            elif o == 'ror': text = 'ROR(%s, %s)' % (A, Bv)
            elif o == 'adc': text = '%s + %s + FLAG_C' % (A, Bv)
            elif o == 'sbc': text = '%s - %s - !FLAG_C' % (A, Bv)
            elif o == 'sub' and is_imm(a) and a[1] == 0: text = '-%s' % Bv
            elif isinstance(a, int) and a == rd and o in sym: return '%s %s= %s;' % (regname(rd), sym[o], Bv)
            else: text = '%s %s %s' % (A, sym[o], Bv)
            return '%s = %s;' % (regname(rd), text)
        if op in ('cmp', 'cmn', 'tst', 'teq'):
            return None
        if op == 'load':
            _, rd, size, signed, base, off = ir
            lv = self.address(base, off, size, signed)
            self.consts[rd] = None
            return '%s = %s;' % (regname(rd), lv)
        if op == 'store':
            _, rs, size, base, off = ir
            v = self.val(rs)
            if size < 4 and not (base == 13): v = '(%s)%s' % (SIZE_TYPE[size], v)
            return '%s = %s;' % (self.address(base, off, size, write=True), v)
        if op == 'sp':
            return None
        if op == 'push':
            return None
        if op == 'pop':
            return None
        if op in ('ldm', 'stm'):
            regs = [r for r in range(8) if ir[2] & (1 << r)]
            b = regname(ir[1])
            parts = []
            for n, r in enumerate(regs):
                parts.append(('%s = *(u32 *)(%s + %d);' if op == 'ldm' else '*(u32 *)(%s + %d) = %s;') %
                             ((regname(r), b, 4 * n) if op == 'ldm' else (b, 4 * n, regname(r))))
            parts.append('%s += %d;' % (b, 4 * len(regs)))
            for r in regs: self.consts[r] = None
            self.consts[ir[1]] = None
            return ' '.join(parts)
        if op == 'call':
            for r in (0, 1, 2, 3, 12): self.consts[r] = None
            text = self.call_text(ir[1])
            return ('r0 = %s;' if self.prog.returns(ir[1]) else '%s;') % text
        if op == 'swi':
            self.consts[0] = self.consts[1] = self.consts[3] = None
            return '%s(); /* BIOS SWI 0x%X; r0-r3 as arguments */' % (BIOS.get(ir[1], 'Bios%X' % ir[1]), ir[1])
        return '/* %s */' % i.asm

    def lift(self):
        """List of (kind, payload) lines: ('label', addr), ('stmt', text), ('goto', addr, cond), ('return',)."""
        out = []
        setter = None
        pushed_lr = False
        rets = self.prog.returns(self.addr)
        for k, i in enumerate(self.ins):
            if i.addr in self.labels:
                out.append(('label', i.addr))
                self.consts = {}
                self.used |= set(self.cur_def.values()); self.cur_def = {}
            if k in self.skip: continue
            ir = i.ir
            if ir[0] == 'push' and ir[1] & (1 << 14): pushed_lr = True
            if ir[0] == 'b':
                t = ir[1]
                cond = None if i.cond == 14 else self.cond_text(setter, i.cond)
                self.used |= set(self.cur_def.values())
                if self.contains(t):
                    out.append(('goto', t, cond, i.cond, setter))
                else:
                    call = '%s(%s)' % (self.prog.name(t), ', '.join('r%d' % r for r in range(self.prog.params(t))))
                    text = ('return %s;' % call if rets else '%s; return; /* tail call */' % call)
                    out.append(('stmt', ('if (%s) { %s }' % (cond, text)) if cond else text))
                continue
            returning = (ir[0] == 'bx' and ir[1] == 14) or (ir[0] == 'pop' and ir[1] & (1 << 15))
            if ir[0] == 'pop' and not ir[1] & (1 << 15) and k + 1 < len(self.ins) and self.ins[k + 1].ir[0] == 'bx' \
                    and ir[1] & (1 << self.ins[k + 1].ir[1]) and pushed_lr:
                continue
            if ir[0] == 'bx' and k and self.ins[k - 1].ir[0] == 'pop' and self.ins[k - 1].ir[1] & (1 << ir[1]) and pushed_lr:
                returning = True
            if returning:
                if rets: self.used.add(self.cur_def.get(0))
                text = 'return r0;' if rets else 'return;'
                out.append(('stmt', ('if (%s) %s' % (self.cond_text(setter, i.cond), text)) if i.cond != 14 else text))
                continue
            if ir[0] == 'bx':
                via = '((void (*)(void))%s)(); return; /* indirect tail jump */' % regname(ir[1])
                out.append(('stmt', via))
                continue
            if ir[0] == 'jump':
                sw = next((s for s in self.switches() if int(s['source'], 16) <= i.addr < int(s['start'], 16)), None)
                if sw:
                    targets = ', '.join(t[2:] for t in sw['targets'][:24]) + (' ...' if len(sw['targets']) > 24 else '')
                    out.append(('stmt', 'switch (index) { /* jump table %s: %d cases -> %s */ }' % (sw['start'], len(sw['targets']), targets)))
                else:
                    out.append(('stmt', 'goto *%s; /* computed jump */' % self.val(ir[1])))
                continue
            prev = self.cur_def.get(ir[1]) if ir[0] == 'alu' else None
            text = self.statement(i, k, setter)
            written = uses(ir, self.prog)[1]
            for r in written: self.cur_def.pop(r, None)
            if ir[0] == 'alu' and ir[3] == ir[1] and is_imm(ir[4]) and prev is not None and prev == len(out) - 1 \
                    and self.consts.get(ir[1]) is not None and i.cond == 14:
                # Constant built in two steps (mov then shift/add): show the value once.
                out[-1] = ('stmt', '%s = %s;' % (regname(ir[1]), self.const_text(self.consts[ir[1]])))
                self.used.discard(prev); self.cur_def[ir[1]] = prev
                text = None
            elif ir[0] == 'alu' and ir[2] in ('lsr', 'asr') and is_imm(ir[4]) and ir[4][1] in (16, 24) and k and out \
                    and self.ins[k - 1].ir[:3] == ('alu', ir[3], 'lsl') and self.ins[k - 1].ir[4] == ir[4] \
                    and isinstance(self.ins[k - 1].ir[3], int) and i.addr not in self.labels:
                cast = ('u' if ir[2] == 'lsr' else 's') + str(32 - ir[4][1])
                src = self.ins[k - 1].ir[3]
                text = '%s = (%s)%s;' % (regname(ir[1]), cast, regname(src))
                if ir[1] == ir[3] and out[-1][0] == 'stmt' and len(out) - 1 not in self.const_defs: out.pop()
            if text is not None:
                if i.cond != 14: text = 'if (%s) { %s }' % (self.cond_text(setter, i.cond), text)
                out.append(('stmt', text))
                if ir[0] in ('pool', 'mov') and is_imm(ir[2] if ir[0] == 'mov' else ('#', 0)) and i.cond == 14:
                    self.cur_def[ir[1]] = len(out) - 1
                    self.const_defs.add(len(out) - 1)
            if i.flags:
                setter = i
            elif ir[0] in ('call', 'swi'):
                setter = None
        # Constants whose only uses were folded into absolute addresses add nothing to read.
        dead = self.const_defs - self.used
        return [l for n, l in enumerate(out) if n not in dead]

    def switches(self):
        if not hasattr(self.prog, '_switches'):
            self.prog._switches = json.loads((self.prog.root / 'docs/map/pointers.json').read_text()).get('switches', [])
        return self.prog._switches

def invert(c):
    return c ^ 1

def structure(lines, lifter, indent=1):
    """Fold single-entry forward skips into if-blocks and single-entry back edges into do/while."""
    refs = {}
    for l in lines:
        if l[0] == 'goto': refs[l[1]] = refs.get(l[1], 0) + 1
    out = []
    i = 0
    while i < len(lines):
        l = lines[i]
        if l[0] == 'goto' and l[2] is not None and refs.get(l[1], 0) == 1:
            j = next((n for n in range(i + 1, len(lines)) if lines[n][0] == 'label' and lines[n][1] == l[1]), None)
            if j is not None and self_contained(lines[i + 1:j], refs):
                body = structure(lines[i + 1:j], lifter, indent + 1)
                out.append(('if', lifter.cond_text(l[4], invert(l[3])), body))
                i = j + 1
                continue
        if l[0] == 'label' and refs.get(l[1], 0) == 1:
            j = next((n for n in range(i + 1, len(lines)) if lines[n][0] == 'goto' and lines[n][1] == l[1]), None)
            if j is not None and self_contained(lines[i + 1:j], refs):
                body = structure(lines[i + 1:j], lifter, indent + 1)
                cond = lines[j][2]
                out.append(('loop', cond, body))
                i = j + 1
                continue
        out.append(l)
        i += 1
    return out

def self_contained(block, refs):
    """No label in block is targeted from outside it and every goto inside targets a label inside."""
    inner = {l[1] for l in block if l[0] == 'label'}
    counts = {}
    for l in block:
        if l[0] == 'goto': counts[l[1]] = counts.get(l[1], 0) + 1
    if any(counts.get(t, 0) != refs.get(t, 0) for t in inner): return False
    return all(l[1] in inner for l in block if l[0] == 'goto')

def emit(nodes, indent=1):
    pad = '    ' * indent
    text = []
    for n in nodes:
        if n[0] == 'label': text.append('L_%08X:' % n[1])
        elif n[0] == 'stmt': text.append(pad + n[1])
        elif n[0] == 'goto': text.append(pad + ('if (%s) goto L_%08X;' % (n[2], n[1]) if n[2] else 'goto L_%08X;' % n[1]))
        elif n[0] == 'if':
            text.append(pad + 'if (%s) {' % n[1]); text += emit(n[2], indent + 1); text.append(pad + '}')
        elif n[0] == 'loop':
            text.append(pad + 'do {'); text += emit(n[2], indent + 1)
            text.append(pad + ('} while (%s);' % n[1] if n[1] else '} while (1);'))
    return text

def signature(prog, addr):
    n = prog.params(addr)
    ret = 'u32' if prog.returns(addr) else 'void'
    return '%s %s(%s)' % (ret, prog.name(addr) if prog.name(addr).startswith('func_') else 'func_%08X' % addr,
                          ', '.join('u32 r%d' % r for r in range(n)) or 'void')

def disassembly(prog, addr, pools=True):
    """Text listing with literal pool words resolved."""
    lines = []
    for i in prog.insns[addr]:
        raw = '%08X' % i.raw if i.size == 4 else '%04X' % i.raw
        extra = ''
        if i.ir[0] == 'pool':
            v = prog.word(i.ir[2])
            extra = ' (0x%08X)' % v if v is not None else ''
        if i.ir[0] == 'call': extra = ' <%s>' % prog.name(i.ir[1])
        lines.append('%08X: %-9s %s%s' % (i.addr, raw, i.asm, extra))
    return '\n'.join(lines)

def pool_words(prog, addr):
    """{pool address: word} for literals referenced by the function."""
    return {i.ir[2]: prog.word(i.ir[2]) for i in prog.insns[addr] if i.ir[0] == 'pool'}

def draft(prog, addr):
    """Full draft text for one function."""
    f = prog.by_start[addr]
    lifter = Lifter(prog, addr)
    lines = lifter.lift()
    body = emit(structure(lines, lifter))
    regs = sorted({int(m) for m in re.findall(r'\br(\d+)\b', '\n'.join(body))})
    params = prog.params(addr) if f['mode'] == 'thumb' else 4
    local_regs = [r for r in regs if r >= params]
    callers = sorted(prog.callers.get(addr, ()))
    head = ['/* %s  %s  %s mode, %d bytes of instructions (pools excluded)' % (prog.name(addr), f['start'], f['mode'], prog.size(addr)),
            ' * callers: %s' % (', '.join(prog.name(c) for c in callers[:12]) + (' ...' if len(callers) > 12 else '') if callers else 'none found (entry, pointer or interrupt target)'),
            ' * callees: %s' % (', '.join(prog.name(c) for c in sorted(prog.callees.get(addr, ()))) or 'none (leaf)'),
            ' * matched in C: %s' % ('yes' if addr in prog.matched else 'no'),
            ' * Lifted automatically from the static recompiler; r0-r3 are argument registers, flags are',
            ' * folded into conditions where a branch uses them. Not compilable as-is. */']
    sig = signature(prog, addr)
    out = head + [sig + ' {']
    if local_regs: out.append('    u32 %s;' % ', '.join('r%d' % r for r in local_regs))
    if lifter.locals: out.append('    u32 %s; /* stack slots */' % ', '.join(sorted(lifter.locals)))
    out += body + ['}', '']
    return '\n'.join(out)

def write_drafts(root=Path('.'), only=None):
    prog = Program(root)
    outdir = Path(root) / 'build/drafts'
    outdir.mkdir(parents=True, exist_ok=True)
    n = 0
    for addr in sorted(prog.by_start):
        if only is not None and addr not in only: continue
        (outdir / ('func_%08X.c' % addr)).write_text(draft(prog, addr))
        n += 1
    return n

if __name__ == '__main__':
    n = write_drafts()
    print('Wrote %d drafts to build/drafts' % n)

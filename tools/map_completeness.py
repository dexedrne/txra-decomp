#!/usr/bin/env python3
"""Map-completeness audit. Writes metadata (offsets, counts, reasons); never ROM bytes.

Questions answered, each from the current tools/rom.cfg, docs/map/functions.json,
splits.json and indirect.json:

1. Closure: does every direct branch, call, PC-relative literal and resolved
   indirect transfer in the mapped instructions land on mapped code (or on data)?
2. References from non-code bytes: which code-shaped pointers (odd ROM pointers,
   ARM-aligned ROM pointers, copied-RAM aliases) point at code, and do any point
   into unknown bytes?
3. Code-likeness of every unknown span compared with mapped code and mapped data:
   Thumb BL pairs that hit a known instruction start, ARM BL/B words that hit
   known ARM code, ARM always-condition density, and Thumb frame/return idioms.
4. The two-byte unknown gaps inside the program enclosure: are they aligners?
5. Copy sources: is every copied byte mapped?

A negative result is bounded evidence about references and code shape. It is not
a proof that no unreferenced byte sequence could ever be executed.
"""
import argparse
import bisect
import collections
import hashlib
import json
import struct
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB
from capstone.arm import (ARM_CC_AL, ARM_INS_ADD, ARM_INS_ADR, ARM_INS_B, ARM_INS_BL, ARM_INS_BX, ARM_INS_LDM,
                          ARM_INS_LDR, ARM_INS_MOV, ARM_INS_POP, ARM_OP_IMM, ARM_OP_MEM, ARM_OP_REG, ARM_REG_PC)

BASE = 0x08000000
PROGRAM_END = 0x18EC4          # end of the IRQ callback table; first rodata byte
RAM = ((0x02000000, 0x02040000), (0x03000000, 0x03008000))
IO_LIKE = ((0x04000000, 0x04000400), (0x05000000, 0x05000400), (0x06000000, 0x06018000),
           (0x07000000, 0x07000400))


def hx(v):
    return f'0x{v:08X}'


class Model:
    def __init__(self, rom, cfg, functions, splits, indirect):
        self.rom, self.cfg, self.functions, self.indirect = rom, cfg, functions, indirect
        self.size = len(rom)
        self.mapping = sorted(cfg['mapping'], key=lambda s: s['offset'])
        self.map_starts = [s['offset'] for s in self.mapping]
        self.mode = bytearray(self.size)       # 1 thumb, 2 arm instruction bytes
        self.pool = bytearray(self.size)       # literal/switch bytes from splits
        self.ins_start = {}                    # offset -> 'thumb'/'arm'
        self.spans = []
        for r in splits:
            a, z = int(r['start'], 16)-BASE, int(r['end'], 16)-BASE
            if r['kind'] == 'literal':
                self.pool[a:z] = b'\1'*(z-a)
            elif r['kind'] in ('arm', 'thumb'):
                self.mode[a:z] = bytes([1 if r['kind'] == 'thumb' else 2])*(z-a)
                self.spans.append((a, z, r['kind']))
        self.entries = {(int(f['start'], 16)-BASE, f['mode']) for f in functions}
        self.entry_offsets = {o for o, _ in self.entries}
        self.alias_entries = {}
        for f in functions:
            for alias in f.get('runtime_aliases', []):
                self.alias_entries[int(alias['start'], 16)] = (int(f['start'], 16)-BASE, f['mode'])
        self.copies = cfg.get('copies', [])
        self.decoded = []
        for a, z, kind in self.spans:
            cs = Cs(CS_ARCH_ARM, CS_MODE_THUMB if kind == 'thumb' else CS_MODE_ARM)
            cs.detail = True
            for ins in cs.disasm(rom[a:z], BASE+a):
                self.ins_start[ins.address-BASE] = kind
                self.decoded.append((kind, ins))

    def type_at(self, off):
        if not 0 <= off < self.size:
            return 'outside-rom'
        i = bisect.bisect_right(self.map_starts, off)-1
        return self.mapping[i]['type']

    def classify_rom_target(self, off, thumb):
        """Where does a code-shaped ROM address land?"""
        mode = 'thumb' if thumb else 'arm'
        if (off, mode) in self.entries:
            return 'function-entry'
        if self.ins_start.get(off) == mode:
            return 'internal-instruction'
        if self.mode[off] if 0 <= off < self.size else 0:
            return 'instruction-mode-conflict-or-interior'
        return 'non-code:'+self.type_at(off)

    def ram_aliases(self, value):
        """Unique copied-code alias offsets for a RAM address, with copy mode."""
        address = value & ~1
        out = set()
        for c in self.copies:
            if c['run'] <= address < c['run']+c['size']:
                out.add(c['load']-BASE+address-c['run'])
        return sorted(out)


def literal_value(m, address):
    off = address-BASE
    if 0 <= off <= m.size-4:
        return struct.unpack_from('<I', m.rom, off)[0]
    return None


def classify_value(m, v):
    """Classify a 32-bit literal value as a code/data/IO reference."""
    if BASE <= v < BASE+m.size:
        off = (v & ~1)-BASE
        if v & 1:
            return 'rom-odd', m.classify_rom_target(off, True), off
        if m.mode[off] == 2 or (off, 'arm') in m.entries:
            return 'rom-even-arm-code', m.classify_rom_target(off, False), off
        if m.mode[off] == 1:
            return 'rom-even-into-thumb-code', 'thumb-instruction-address', off
        return 'rom-data', 'data:'+m.type_at(off), off
    for lo, hi in RAM:
        if lo <= v < hi:
            aliases = m.ram_aliases(v)
            if not aliases:
                return 'ram', 'ram-not-copied-code', None
            thumb = bool(v & 1)
            results = sorted({m.classify_rom_target(a, thumb) for a in aliases})
            return 'ram-copied', '|'.join(results), aliases[0]
    for lo, hi in IO_LIKE:
        if lo <= v < hi:
            return 'hw', 'hardware', None
    return 'scalar', 'scalar', None


def closure(m):
    """Every transfer and literal reachable from the decoded mapped instructions."""
    edges = collections.Counter()
    problems = []
    literal_kinds = collections.Counter()
    literal_code_targets = collections.Counter()
    callers = collections.defaultdict(int)
    refs = collections.defaultdict(list)
    for kind, ins in m.decoded:
        at = ins.address-BASE
        ops = ins.operands
        if ins.id in (ARM_INS_B, ARM_INS_BL) and ops and ops[0].type == ARM_OP_IMM:
            target = ops[0].imm-BASE
            cls = m.classify_rom_target(target, kind == 'thumb')
            label = ('call' if ins.id == ARM_INS_BL else 'branch')+'->'+cls
            edges[label] += 1
            if ins.id == ARM_INS_BL:
                callers[target] += 1
            if (target, kind) in m.entries:
                refs[target].append((at, 'direct call' if ins.id == ARM_INS_BL else 'direct branch'))
            if cls.startswith('non-code') or cls.startswith('instruction-mode'):
                problems.append({'site': hx(ins.address), 'kind': label, 'target': hx(BASE+target)})
            continue
        lit = None
        if ins.id == ARM_INS_LDR and len(ops) > 1 and ops[1].type == ARM_OP_MEM and ops[1].mem.base == ARM_REG_PC:
            pc = (ins.address+4) & ~3 if kind == 'thumb' else ins.address+8
            lit = pc+ops[1].mem.disp
            # Only immediate-offset literal loads; register-indexed PC loads are switch reads.
            if ops[1].mem.index:
                continue
            v = literal_value(m, lit)
            if v is None:
                problems.append({'site': hx(ins.address), 'kind': 'literal outside ROM'})
                continue
            if not m.pool[lit-BASE] and not m.mode[lit-BASE]:
                problems.append({'site': hx(ins.address), 'kind': 'literal slot not in a mapped pool',
                                 'slot': hx(lit), 'slot_type': m.type_at(lit-BASE)})
            vk, vc, tgt = classify_value(m, v)
            literal_kinds[vk] += 1
            if vc == 'function-entry' and tgt is not None:
                refs[tgt].append((at, 'code literal'))
            elif vk == 'ram-copied' and 'function-entry' in vc:
                for alias in m.ram_aliases(v):
                    if (alias, 'thumb' if v & 1 else 'arm') in m.entries:
                        refs[alias].append((at, 'code literal (copied-RAM alias)'))
            if vk in ('rom-odd', 'rom-even-arm-code', 'ram-copied', 'rom-even-into-thumb-code'):
                literal_code_targets[vk+'->'+vc] += 1
                if 'non-code' in vc or 'conflict' in vc:
                    problems.append({'site': hx(ins.address), 'kind': 'literal '+vk+' -> '+vc,
                                     'value_target': hx(BASE+tgt) if tgt is not None else None})
        elif ins.id in (ARM_INS_ADR,) or (ins.id == ARM_INS_ADD and len(ops) == 3 and ops[1].type == ARM_OP_REG
                                          and ops[1].reg == ARM_REG_PC and ops[2].type == ARM_OP_IMM):
            pc = (ins.address+4) & ~3 if kind == 'thumb' else ins.address+8
            disp = ops[-1].imm if ops[-1].type == ARM_OP_IMM else 0
            target = pc+disp-BASE
            literal_kinds['pc-relative-address'] += 1
            if any((target, k) in m.entries for k in ('thumb', 'arm')):
                refs[target].append((at, 'code pc-relative address'))
            literal_code_targets['pc-relative-address->'+('pool' if 0 <= target < m.size and m.pool[target]
                                                          else m.classify_rom_target(target, kind == 'thumb')
                                                          if 0 <= target < m.size else 'outside')] += 1
    # Indirect transfers resolved by the inventory.
    indirect_rows = collections.Counter()
    unresolved = []
    for site in m.indirect['transfers']+m.indirect.get('veneer_calls', []):
        if site.get('kind') == 'return':
            indirect_rows['return'] += 1
            continue
        values = set(site.get('targets', []))
        if site.get('target'):
            values.add(site['target'])
        if not values:
            unresolved.append(site['source'])
            continue
        for value in values:
            v = int(value, 16)
            vk, vc, tgt = classify_value(m, v)
            if vk == 'rom-data' and site.get('confidence') == 'bounded switch':
                vk, vc = 'switch', m.classify_rom_target(v-BASE, site.get('mode') == 'thumb')
            if vk == 'rom-data' and v == BASE:
                vc = m.classify_rom_target(0, False)
            indirect_rows[vk+'->'+vc] += 1
            label = 'IRQ table' if 'IRQ table' in site.get('confidence', '') else 'resolved indirect'
            src = int(site['source'], 16)-BASE
            if vk == 'ram-copied':
                for alias in m.ram_aliases(v):
                    if (alias, 'thumb' if v & 1 else 'arm') in m.entries:
                        refs[alias].append((src, label))
            elif tgt is not None and vc == 'function-entry':
                refs[tgt].append((src, label))
            elif v == BASE:
                refs[0].append((src, label))
            if 'non-code' in vc:
                problems.append({'site': site['source'], 'kind': 'indirect target not mapped', 'target': value})
    veneer_callers = {}
    for site in unresolved:
        off = int(site, 16)-BASE
        veneer_callers[site] = {'direct_BL_callers': callers.get(off, 0),
                                'literal_or_data_pointer_refs': None}
    return {'decoded_instructions': len(m.decoded), 'direct_edges': dict(edges),
            'pc_literal_kinds': dict(literal_kinds), 'code_shaped_literals': dict(literal_code_targets),
            'indirect_targets': dict(indirect_rows), 'unresolved_indirect_sites': veneer_callers,
            'problems': problems, '_refs': refs}


def data_references(m, unresolved_sites):
    """Code-shaped words in every non-code byte (all alignments for odd pointers)."""
    rom = m.rom
    noncode = bytearray(m.size)
    for s in m.mapping:
        if s['type'] != 'code':
            noncode[s['offset']:s['offset']+s['size']] = b'\1'*s['size']
    odd = collections.Counter(); odd_unknown = []
    even_arm = collections.Counter(); ram = collections.Counter(); ram_rows = []
    pointer_refs_to = collections.Counter()
    entry_slots = collections.defaultdict(list)
    for p in range(0, m.size-3):
        if not (noncode[p] and noncode[p+3]):
            continue
        v = struct.unpack_from('<I', rom, p)[0]
        if BASE <= v < BASE+m.size and v & 1:
            off = (v & ~1)-BASE
            cls = m.classify_rom_target(off, True)
            odd[(cls, p % 4 == 0)] += 1
            pointer_refs_to[off] += 1
            if p % 4 == 0 and cls == 'function-entry':
                entry_slots[off].append(p)
            if cls == 'non-code:unknown':
                odd_unknown.append((p, off))
        elif p % 4 == 0 and BASE <= v < BASE+PROGRAM_END and not v & 3:
            off = v-BASE
            if m.mode[off] == 2:
                even_arm[m.classify_rom_target(off, False)] += 1
                pointer_refs_to[off] += 1
                if (off, 'arm') in m.entries and off:
                    entry_slots[off].append(p)
        elif p % 4 == 0 and any(lo <= v < hi for lo, hi in RAM):
            aliases = m.ram_aliases(v)
            if aliases:
                kinds = sorted({m.classify_rom_target(a, bool(v & 1)) for a in aliases})
                ram['|'.join(kinds)] += 1
                for alias in aliases:
                    if (alias, 'thumb' if v & 1 else 'arm') in m.entries:
                        entry_slots[alias].append(p)
                ram_rows.append({'slot': hx(BASE+p), 'slot_type': m.type_at(p), 'runtime_target': hx(v),
                                 'alias_classes': kinds,
                                 'entries': sorted(hx(BASE+a) for a in aliases if (a, 'thumb' if v & 1 else 'arm') in m.entries)})
    # Do odd pointers into unknown bytes start plausible Thumb code? Reuse the reviewed validator.
    from code_audit import validate_thumb
    pools = {p for p in range(m.size) if m.pool[p]}
    validated = collections.Counter(); proposals = []
    by_target = collections.defaultdict(list)
    for p, off in odd_unknown:
        by_target[off].append(p)
    for off, sources in sorted(by_target.items()):
        result = validate_thumb(rom, off, [{'kind': 'odd-ROM-pointer'}], pools, budget=4096)
        validated[result['reason'] if not result['valid'] else 'VALID'] += 1
        if result['valid']:
            proposals.append({'target': hx(BASE+off), 'sources': [hx(BASE+s) for s in sources[:8]],
                              'spans': [[hx(BASE+a), hx(BASE+z)] for a, z in result['spans']]})
    veneer_refs = {s: pointer_refs_to.get(int(s, 16)-BASE, 0) for s in unresolved_sites}
    return {'odd_rom_pointers': {f'{cls} ({"word" if aligned else "unaligned"})': n
                                 for (cls, aligned), n in sorted(odd.items())},
            'odd_pointer_targets_in_unknown': len(by_target),
            'odd_pointer_targets_in_unknown_validation': dict(validated),
            'odd_pointer_proposals': proposals,
            'aligned_rom_pointers_to_arm_code': dict(even_arm),
            'aligned_ram_pointers_to_copied_code': dict(ram),
            'aligned_ram_pointer_slots': ram_rows,
            'pointer_refs_to_unresolved_veneers': veneer_refs, '_entry_slots': entry_slots}


def code_features(m, a, z, known_arm_starts, events=None):
    """Counts only; no byte values are returned. Optional events collect idiom offsets."""
    rom = m.rom
    f = collections.Counter()
    a2 = a + (a & 1)
    for p in range(a2, z-1, 2):
        w = rom[p] | rom[p+1] << 8
        f['halfwords'] += 1
        hi = w & 0xFF00
        if w == 0x4770:
            f['thumb_bx_lr'] += 1
            if events is not None:
                events.append(('thumb-bx-lr', p))
        if hi == 0xB500:
            f['thumb_push_lr'] += 1
        elif hi == 0xBD00:
            f['thumb_pop_pc'] += 1
        elif hi == 0xBC00 and w & 0xFF and p+3 < z:
            w2 = rom[p+2] | rom[p+3] << 8
            if w2 & 0xFF87 == 0x4700 and (w2 >> 3) & 15 < 8 and w & (1 << ((w2 >> 3) & 7)):
                f['thumb_pop_bx_return'] += 1
                if events is not None:
                    events.append(('thumb-pop-bx', p))
        if w & 0xF800 == 0xF000 and p+3 < z:
            w2 = rom[p+2] | rom[p+3] << 8
            f['thumb_bl_prefix'] += 1
            if w2 & 0xF800 == 0xF800:
                f['thumb_bl_pair'] += 1
                off = ((w & 0x7FF) << 12) | ((w2 & 0x7FF) << 1)
                if off & 0x400000:
                    off -= 0x800000
                t = p+4+off
                if 0 <= t < m.size and m.ins_start.get(t) == 'thumb':
                    f['thumb_bl_hits_known_thumb'] += 1
                    if (t, 'thumb') in m.entries:
                        f['thumb_bl_hits_entry'] += 1
        if w & 0xF800 == 0x4800:
            lit = ((p+4) & ~3)+(w & 0xFF)*4
            if lit+4 <= m.size:
                v = struct.unpack_from('<I', rom, lit)[0]
                f['thumb_pc_loads'] += 1
                if (BASE <= v < BASE+m.size or any(lo <= v < hi for lo, hi in RAM+IO_LIKE)):
                    f['thumb_pc_loads_address_like'] += 1
    a4 = (a+3) & ~3
    run = []
    for p in range(a4, z-3, 4):
        w = struct.unpack_from('<I', rom, p)[0]
        f['words'] += 1
        always = w >> 28 == 0xE
        if always:
            f['arm_cond_always'] += 1
        run.append(always)
        if len(run) >= 16:
            if sum(run[-16:]) >= 12:
                f['arm_dense_16word_windows'] += 1
                if events is not None and (not events or events[-1][0] != 'arm-dense' or events[-1][1] < p-60):
                    events.append(('arm-dense', p-60))
        if w >> 25 & 7 == 5 and w >> 28 != 0xF:      # B/BL any condition
            off = w & 0xFFFFFF
            if off & 0x800000:
                off -= 0x1000000
            t = p+8+off*4
            if 0 <= t < m.size and t in known_arm_starts:
                f['arm_branch_hits_known_arm'] += 1
        if w & 0x0FFFFFF0 == 0x012FFF10:
            f['arm_bx'] += 1
        if w == 0xE12FFF1E:
            f['arm_bx_lr'] += 1
        if w & 0x0FFF8000 == 0x08BD8000:                  # LDMIA sp!,{...,pc}
            f['arm_pop_pc'] += 1
        if w & 0x0FFF0000 == 0x092D0000 and w & 0x4000:   # STMDB sp!,{...,lr}
            f['arm_push_lr'] += 1
    return f


def rates(f, nbytes):
    kb = max(nbytes, 1)/1024
    words = max(f['words'], 1)
    return {'bytes': nbytes,
            'thumb_bl_pair_coherence': round(f['thumb_bl_pair']/f['thumb_bl_prefix'], 4) if f['thumb_bl_prefix'] else None,
            'thumb_bl_hits_known_thumb': f['thumb_bl_hits_known_thumb'],
            'thumb_bl_hits_entry': f['thumb_bl_hits_entry'],
            'thumb_bl_hits_entry_per_kb': round(f['thumb_bl_hits_entry']/kb, 4),
            'thumb_push_lr': f['thumb_push_lr'], 'thumb_push_lr_per_kb': round(f['thumb_push_lr']/kb, 4),
            'thumb_pop_pc': f['thumb_pop_pc'],
            'thumb_bx_lr': f['thumb_bx_lr'], 'thumb_bx_lr_per_kb': round(f['thumb_bx_lr']/kb, 4),
            'thumb_pop_bx_return': f['thumb_pop_bx_return'],
            'thumb_return_idioms_per_kb': round((f['thumb_bx_lr']+f['thumb_pop_bx_return']+f['thumb_pop_pc'])/kb, 4),
            'thumb_pc_load_address_like_fraction': round(f['thumb_pc_loads_address_like']/f['thumb_pc_loads'], 4)
                if f['thumb_pc_loads'] else None,
            'arm_cond_always_fraction': round(f['arm_cond_always']/words, 4),
            'arm_dense_16word_windows': f['arm_dense_16word_windows'],
            'arm_branch_hits_known_arm': f['arm_branch_hits_known_arm'],
            'arm_push_lr': f['arm_push_lr'], 'arm_pop_pc': f['arm_pop_pc'],
            'arm_bx': f['arm_bx'], 'arm_bx_lr': f['arm_bx_lr']}


def likeness(m):
    known_arm = {o for o, k in m.ins_start.items() if k == 'arm'}
    groups = collections.defaultdict(collections.Counter); sizes = collections.Counter()
    spans = []; events = []
    for s in m.mapping:
        a, z = s['offset'], s['offset']+s['size']
        key = s['type'] + (':'+s['format'] if s['type'] == 'code' else '')
        ev = [] if s['type'] == 'unknown' else None
        f = code_features(m, a, z, known_arm, ev)
        groups[key].update(f); sizes[key] += z-a
        if s['type'] == 'unknown':
            spans.append((a, z, f))
            events.extend(ev)
    baseline = {k: rates(groups[k], sizes[k]) for k in sorted(groups)}
    # Flag any unknown span with code evidence that random data should essentially never produce.
    flagged = []
    for a, z, f in spans:
        n = z-a
        reasons = []
        if f['thumb_bl_hits_entry']:
            reasons.append('%d Thumb BL pair(s) hit a function entry' % f['thumb_bl_hits_entry'])
        if f['thumb_bl_hits_known_thumb'] >= 2:
            reasons.append('%d Thumb BL pairs hit known Thumb instructions' % f['thumb_bl_hits_known_thumb'])
        if f['arm_dense_16word_windows']:
            reasons.append('%d dense ARM-condition windows' % f['arm_dense_16word_windows'])
        if f['thumb_bx_lr'] or f['thumb_pop_bx_return']:
            reasons.append('%d Thumb return idiom(s)' % (f['thumb_bx_lr']+f['thumb_pop_bx_return']))
        if f['arm_branch_hits_known_arm']:
            reasons.append('%d ARM branch word(s) hit known ARM instructions' % f['arm_branch_hits_known_arm'])
        if f['words'] >= 8 and f['arm_cond_always'] / f['words'] >= 0.5:
            reasons.append('ARM always-condition fraction %.2f' % (f['arm_cond_always']/f['words']))
        if f['thumb_push_lr'] and (f['thumb_pop_pc'] or f['thumb_bx_lr']) and n <= 4096:
            reasons.append('Thumb push-lr with pop-pc/bx-lr in a %d-byte span' % n)
        if reasons:
            flagged.append({'start': hx(BASE+a), 'size': n, 'reasons': reasons, **rates(f, n)})
    hist = collections.Counter()
    for a, z, f in spans:
        n = z-a
        hist['<=4' if n <= 4 else '<=16' if n <= 16 else '<=64' if n <= 64 else '<=256' if n <= 256 else
             '<=1K' if n <= 1024 else '<=4K' if n <= 4096 else '<=16K' if n <= 16384 else '>16K'] += n
    # For every Thumb return idiom in unknown bytes, try each push-lr start up to 1 KiB before it
    # and the halfword starts after the previous return/terminal; report validator outcomes.
    from code_audit import validate_thumb
    pools = {p for p in range(m.size) if m.pool[p]}
    idiom_rows = []
    dense = [p for kind, p in events if kind == 'arm-dense']
    runs = []
    for p in dense:
        if runs and p <= runs[-1][1]:
            runs[-1][1] = max(runs[-1][1], p+64)
        else:
            runs.append([p, p+64])
    for a, z in runs:
        f = code_features(m, a, z, known_arm)
        idiom_rows.append({'kind': 'arm-condition-dense-run', 'start': hx(BASE+a), 'end': hx(BASE+z),
                           'span_type': m.type_at(a), 'arm_branch_hits_known_arm': f['arm_branch_hits_known_arm'],
                           'arm_bx': f['arm_bx'], 'arm_pop_pc': f['arm_pop_pc'], 'arm_push_lr': f['arm_push_lr'],
                           'distinct_byte_values': len(set(m.rom[a:z]))})
    for kind, p in events:
        if kind == 'arm-dense':
            continue
        tried = collections.Counter(); valid = []
        for start in range(max(0, p-1024), p+1, 2):
            w = m.rom[start] | m.rom[start+1] << 8
            # Framed routines start with PUSH {..,lr}; frameless leaves (BX LR) may start anywhere close.
            if w & 0xFF00 != 0xB500 and not (kind == 'thumb-bx-lr' and start >= p-256):
                continue
            r = validate_thumb(m.rom, start, [{'kind': 'return-idiom-backscan'}], pools, budget=4096)
            tried[r['reason'] if not r['valid'] else 'VALID'] += 1
            if r['valid'] and any(a <= p < z for a, z in r['spans']):
                valid.append({'start': hx(BASE+start), 'spans': [[hx(BASE+a), hx(BASE+z)] for a, z in r['spans']]})
        idiom_rows.append({'kind': kind, 'at': hx(BASE+p), 'starts_tried': sum(tried.values()),
                           'outcomes': dict(tried), 'valid_containing_starts': valid})
    neighbours = collections.Counter(); windows = collections.Counter()
    index = {s['offset']: i for i, s in enumerate(m.mapping)}
    for a, z, f in spans:
        i = index[a]
        pair = tuple(sorted({m.mapping[i-1]['type'] if i else 'start', m.mapping[i+1]['type'] if i+1 < len(m.mapping) else 'end'}))
        neighbours['+'.join(pair)] += z-a
        windows['%06X' % (a & ~0x3FFFF)] += z-a
    return {'baselines_by_mapping_type': baseline, 'unknown_spans': len(spans),
            'unknown_bytes_by_neighbour_types': dict(neighbours.most_common()),
            'unknown_bytes_by_256k_window_of_span_start': dict(sorted(windows.items())),
            'unknown_code_idioms': idiom_rows,
            'unknown_bytes_by_span_size': dict(hist), 'flagged_unknown_spans': flagged}


def entry_table(m, refs, slots, cfg):
    """Per entry: who references it, and is it reachable from reset through code-only edges?"""
    owners = collections.defaultdict(set)
    for f in m.functions:
        start = int(f['start'], 16)-BASE
        for a, z in f['spans']:
            for q in range(int(a, 16)-BASE, int(z, 16)-BASE):
                owners[q].add(start)
    # Installed exact owners also own the internal labels inside their extents.
    for mm in cfg.get('matches', []):
        for q in range(mm['offset'], mm['offset']+mm['size']):
            owners[q].add(mm['offset'])
    edges = collections.defaultdict(set)
    for target, rows in refs.items():
        for src, kind in rows:
            for owner in owners.get(src, ()):
                if owner != target:
                    edges[owner].add(target)
    # A span whose last instruction can fall through into another entry continues that body.
    by_end = {ins.address-BASE+ins.size: ins for _, ins in m.decoded}
    entry_set = {o for o, _ in m.entries}
    for f in m.functions:
        start = int(f['start'], 16)-BASE
        for a, z in f['spans']:
            end = int(z, 16)-BASE
            ins = by_end.get(end)
            if end not in entry_set or ins is None:
                continue
            ops = ins.operands
            terminal = ((ins.id == ARM_INS_B and ins.cc == ARM_CC_AL) or ins.id == ARM_INS_BX or
                        (ins.id in (ARM_INS_POP, ARM_INS_LDM) and any(o.type == ARM_OP_REG and o.reg == ARM_REG_PC for o in ops)) or
                        (ins.id == ARM_INS_MOV and ops and ops[0].type == ARM_OP_REG and ops[0].reg == ARM_REG_PC))
            if not terminal:
                edges[start].add(end)
    roots = {0}
    seen = set(); work = list(roots)
    while work:
        x = work.pop()
        if x in seen:
            continue
        seen.add(x)
        work.extend(edges.get(x, ()))
    try:
        audit = json.loads(Path('docs/map/round4-audit.json').read_text())
        unexecuted = {int(r['start'], 16)-BASE for r in audit['mapped_function_entries_unexecuted']}
    except (OSError, KeyError, ValueError):
        unexecuted = set()
    reviewed = {r['offset'] for r in cfg.get('reviewed_seeds', [])}
    matched = {mm['offset']: mm['offset']+mm['size'] for mm in cfg.get('matches', [])}
    covered = {}
    for a, z in matched.items():
        for f in m.functions:
            o = int(f['start'], 16)-BASE
            if a < o < z and o not in matched:
                covered[o] = a
    rows = []
    for f in m.functions:
        o = int(f['start'], 16)-BASE
        kinds = collections.Counter(k for _, k in refs.get(o, []))
        slot_types = collections.Counter(m.type_at(p) for p in slots.get(o, []))
        rows.append({'start': f['start'], 'mode': f['mode'], 'size': int(f['end'], 16)-int(f['start'], 16),
                     'status': 'exact C' if o in matched else ('inside installed owner '+hx(BASE+covered[o]) if o in covered else 'not matched'),
                     'code_references': dict(kinds), 'data_slot_references': dict(slot_types),
                     'reachable_from_reset_by_code_edges': o in seen,
                     'executed_in_recorded_coverage': (o not in unexecuted and o not in reviewed) if unexecuted else None})
    summary = collections.Counter()
    for r in rows:
        if r['reachable_from_reset_by_code_edges']:
            summary['reachable from reset through code references'] += 1
        elif r['data_slot_references']:
            summary['referenced only from data slots'] += 1
        elif r['code_references']:
            summary['referenced only from code that is itself unreached'] += 1
        else:
            summary['no reference (unreferenced library member or dead routine)'] += 1
    return {'summary': dict(summary), 'entries': rows}


def program_gaps(m):
    rows = []
    summary = collections.Counter()
    for i, s in enumerate(m.mapping):
        if s['type'] != 'unknown' or s['offset'] >= PROGRAM_END:
            continue
        a, n = s['offset'], s['size']
        prev = m.mapping[i-1]['type'] if i else None
        nxt = m.mapping[i+1]['type'] if i+1 < len(m.mapping) else None
        zero = all(b == 0 for b in m.rom[a:a+n])
        nop = n == 2 and m.rom[a:a+2] == b'\xc0\x46'
        after = a+n
        aligned_next = after % 4 == 0
        next_is_entry = any((after, k) in m.entries for k in ('thumb', 'arm'))
        prev_end = a  # previous instruction end
        prev_terminal = None
        if prev == 'code' and m.mode[a-2] == 1:
            w = m.rom[a-2] | m.rom[a-1] << 8
            prev_terminal = (w == 0x4770 or w & 0xFF00 == 0xBD00 or w & 0xF800 == 0xE000
                             or w & 0xFF87 == 0x4700)
        if n == 2 and aligned_next and zero and (nxt == 'table' or next_is_entry):
            why = 'zero halfword aligning the following ' + ('literal pool' if nxt == 'table' else 'function entry')
            summary['aligner-zero'] += 1
        elif n == 2 and aligned_next and nop:
            why = 'Thumb no-operation aligning the following ' + ('literal pool' if nxt == 'table' else 'entry')
            summary['aligner-nop'] += 1
        else:
            why = 'not a simple aligner'
            summary['other'] += 1
        rows.append({'start': hx(BASE+a), 'size': n, 'prev': prev, 'next': nxt,
                     'next_word_aligned': aligned_next, 'next_is_entry': next_is_entry,
                     'previous_halfword_ends_flow': prev_terminal, 'value_class': 'zero' if zero else ('nop' if nop else 'other'),
                     'classification': why})
    return {'count': len(rows), 'bytes': sum(r['size'] for r in rows), 'summary': dict(summary), 'gaps': rows}


def copy_coverage(m):
    out = []
    for c in m.copies:
        a = c['load']-BASE; z = a+c['size']
        types = collections.Counter()
        for p in range(a, z):
            types[m.type_at(p)] += 1
        out.append({'load': hx(c['load']), 'run': hx(c['run']), 'size': c['size'], 'by_type': dict(types)})
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    cfg = json.loads(Path('tools/rom.cfg').read_text())
    rom = Path('baserom.gba').read_bytes()
    if len(rom) != cfg['size'] or hashlib.sha1(rom).hexdigest() != cfg['sha1']:
        raise SystemExit('wrong private ROM')
    functions = json.loads(Path('docs/map/functions.json').read_text())['functions']
    splits = json.loads(Path('docs/map/splits.json').read_text())['regions']
    indirect = json.loads(Path('docs/map/indirect.json').read_text())
    m = Model(rom, cfg, functions, splits, indirect)
    c = closure(m)
    d = data_references(m, list(c['unresolved_indirect_sites']))
    for site, refs in d['pointer_refs_to_unresolved_veneers'].items():
        c['unresolved_indirect_sites'][site]['literal_or_data_pointer_refs'] = refs
    entries = entry_table(m, c.pop('_refs'), d.pop('_entry_slots'), cfg)
    counts = collections.Counter()
    for s in m.mapping:
        counts[s['type']] += s['size']
    result = {'complete': False, 'rom_sha1': cfg['sha1'],
              'input_mapping_sha256': hashlib.sha256(json.dumps(cfg['mapping'], sort_keys=True).encode()).hexdigest(),
              'functions': len(functions), 'mapping_bytes': dict(counts),
              'program_enclosure_end': hx(BASE+PROGRAM_END),
              'closure': c, 'data_references': d, 'entry_references': entries, 'code_likeness': likeness(m),
              'program_enclosure_gaps': program_gaps(m), 'copy_sources': copy_coverage(m),
              'caveat': 'Metadata only. Negative results bound referenced and code-shaped bytes; they do not prove '
                        'that no unreferenced sequence could execute.'}
    args.output.write_text(json.dumps(result, indent=1)+'\n')
    print(json.dumps({'problems': len(c['problems']), 'flagged_unknown_spans': len(result['code_likeness']['flagged_unknown_spans']),
                      'odd_pointer_proposals': len(d['odd_pointer_proposals']),
                      'program_gaps': result['program_enclosure_gaps']['summary'],
                      'entries': entries['summary']}))


if __name__ == '__main__':
    main()

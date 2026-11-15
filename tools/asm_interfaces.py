#!/usr/bin/env python3
"""Machine evidence for every mapped entry that is not an exact C replacement.

Writes docs/map/finish.json: one record per unmatched entry with its finishing class
(assembly-interface, fragment-of-owner, covered-by-installed-owner, C-candidate), the
measured instruction properties that justify it, and the owner/next step. Metadata only:
offsets, counts, mnemonics of instructions already listed in asm/, never ROM bytes.

Classes are *reviewed* (docs/asm-only.md and the round notes); this tool re-measures the
properties those reviews rely on and fails loudly when an entry no longer shows them.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path

from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB
from capstone.arm import (ARM_CC_AL, ARM_CC_INVALID, ARM_INS_B, ARM_INS_BL, ARM_INS_BX, ARM_INS_EOR,
                          ARM_INS_LDM, ARM_INS_MOV, ARM_INS_MRS, ARM_INS_MSR, ARM_INS_POP, ARM_INS_PUSH,
                          ARM_INS_STMDB, ARM_INS_STR, ARM_INS_SVC, ARM_OP_IMM, ARM_OP_MEM, ARM_OP_REG,
                          ARM_REG_LR, ARM_REG_PC, ARM_REG_R0, ARM_REG_R1, ARM_REG_R2, ARM_REG_R3, ARM_REG_SP)

BASE = 0x08000000
ABI_IN = {ARM_REG_R0, ARM_REG_R1, ARM_REG_R2, ARM_REG_R3, ARM_REG_SP, ARM_REG_LR, ARM_REG_PC}

# Reviewed classification of the 48 entries without their own exact replacement.
# (class, unit/owner, short reason)
REGISTER_CALL = 'register-call veneer (libgcc _call_via_rN)'
REVIEWED = {
    0x080000C0: ('assembly-interface', 'startup', 'reset: privileged mode changes, banked stacks, IRQ hook, BX to Thumb'),
    0x080000FC: ('assembly-interface', 'irq', 'IRQ dispatcher: SPSR save, mode switch, table dispatch'),
    0x080001F4: ('assembly-interface', 'irq', 'IRQ return tail: restores banked SPSR/mode'),
    0x08000218: ('assembly-interface', 'division-runtime', 'signed division helper (flag-coupled ARM runtime)'),
    0x0800027C: ('assembly-interface', 'division-runtime', 'unsigned division helper (carry-driven ARM runtime)'),
    0x080002CC: ('assembly-interface', 'renderer-private-abi', 'raster front end passing operands in r6-r11'),
    0x08000324: ('assembly-interface', 'renderer-private-abi', 'raster inner loop with preloaded high registers'),
    0x080005D8: ('assembly-interface', 'renderer-private-abi', 'textured raster front end calling 08000AA0 privately'),
    0x08000AA0: ('assembly-interface', 'renderer-private-abi', 'raster helper consuming live high registers and flags'),
    0x08000BF0: ('assembly-interface', 'renderer-private-abi', 'raster front end calling 080010B8 privately'),
    0x080010B8: ('assembly-interface', 'renderer-private-abi', 'raster helper with packed inputs in r4/r6/r11'),
    0x08001218: ('assembly-interface', 'renderer-private-abi', 'raster front end calling 080016E0 privately'),
    0x080016E0: ('assembly-interface', 'renderer-private-abi', 'raster inner loop with live r4/r6-r8/r11/r12'),
    0x08018A54: ('assembly-interface', 'bios-veneer', 'CpuFastSet SWI then return'),
    0x08018A58: ('assembly-interface', 'bios-veneer', 'CpuSet SWI then return'),
    0x08018E7C: ('assembly-interface', 'state-switch-veneer', 'Thumb BX PC into the ARM branch at 08018E80'),
    0x08018E84: ('assembly-interface', 'state-switch-veneer', 'Thumb BX PC into the ARM branch at 08018E88'),
    0x08003786: ('covered-by-installed-owner', '08002854', 'internal continuation inside installed func_08002854 (second scenery pass, reached by the far BL at 0800416A)'),
    0x080051FE: ('fragment-of-owner', '0800421C', 'shared epilogue releasing the 36-byte frame'),
    0x08006712: ('covered-by-installed-owner', '080064A4', 'mixer block inside installed func_080064A4 (reached by the far BL at 08007364)'),
    0x08006740: ('covered-by-installed-owner', '080064A4', 'voice preparation block inside installed func_080064A4 (far BL at 08006F46)'),
    0x08006776: ('covered-by-installed-owner', '080064A4', 'envelope body inside installed func_080064A4 (far BL at 08007358)'),
    0x0800735C: ('covered-by-installed-owner', '080064A4', 'voice-loop continuation inside installed func_080064A4 (far BLs at 0800672C/0800673C)'),
    0x08007368: ('covered-by-installed-owner', '080064A4', 'shared epilogue inside installed func_080064A4 (far BLs at 080066EC/08006700)'),
    0x08007B40: ('covered-by-installed-owner', '08007B28', 'internal entry inside installed func_08007B28'),
    0x080095C4: ('covered-by-installed-owner', '08008A88', 'shared epilogue inside installed func_08008A88'),
    0x0800D570: ('covered-by-installed-owner', '0800D51C', 'internal entry inside installed func_0800D51C'),
    0x0800D630: ('covered-by-installed-owner', '0800D51C', 'internal body inside installed func_0800D51C'),
    0x0800D960: ('covered-by-installed-owner', '0800D51C', 'shared tail inside installed func_0800D51C'),
}
# Complete owner extents including pools, as used by the exact-match checker (round notes 1112b/1112c/1111).
OWNER_END = {}
for _reg, _at in zip(('r0', 'r1', 'r2', 'r3', 'r4', 'r5', 'r6', 'r7', 'r8', 'sb', 'sl', 'fp', 'ip', 'sp'),
                     range(0x08018DE0, 0x08018E18, 4)):
    REVIEWED[_at] = ('assembly-interface', 'register-call-veneer', 'BX %s without setting LR (libgcc _call_via_%s)' % (_reg, _reg))


def decode(rom, f):
    mode = f['mode']
    cs = Cs(CS_ARCH_ARM, CS_MODE_THUMB if mode == 'thumb' else CS_MODE_ARM)
    cs.detail = True
    out = {}
    for a, z in f['spans']:
        a, z = int(a, 16)-BASE, int(z, 16)-BASE
        for ins in cs.disasm(rom[a:z], BASE+a):
            out[ins.address] = ins
    return out


def reg_lists(ins):
    return [o.reg for o in ins.operands if o.type == ARM_OP_REG]


def is_return(ins):
    regs = reg_lists(ins)
    return ((ins.id == ARM_INS_BX and ins.cc in (ARM_CC_AL, ARM_CC_INVALID)) or
            (ins.id in (ARM_INS_POP, ARM_INS_LDM) and ARM_REG_PC in regs) or
            (ins.id == ARM_INS_MOV and regs and regs[0] == ARM_REG_PC))


def reads_flags(ins):
    return ins.cc not in (ARM_CC_AL, ARM_CC_INVALID) or ins.mnemonic.startswith(('adc', 'sbc', 'rsc')) or 'rrx' in ins.op_str


def writes_flags(ins):
    return bool(ins.update_flags) or ins.mnemonic.startswith(('cmp', 'cmn', 'tst', 'teq')) or (
        ins.id == ARM_INS_MSR and 'f' in ins.op_str.split(',')[0])


def uses_defs(ins, prev):
    regs = reg_lists(ins)
    if ins.id in (ARM_INS_PUSH,) or (ins.id == ARM_INS_STMDB and regs and regs[0] == ARM_REG_SP):
        return {ARM_REG_SP}, {ARM_REG_SP}            # saves are not inputs
    if ins.id in (ARM_INS_POP,) or (ins.id == ARM_INS_LDM and regs and regs[0] == ARM_REG_SP and ARM_REG_PC in regs):
        return {ARM_REG_SP}, set(regs)
    if ins.id == ARM_INS_BL or (ins.id == ARM_INS_BX and prev is not None and prev.id == ARM_INS_MOV
                                and reg_lists(prev)[:2] == [ARM_REG_LR, ARM_REG_PC]):
        used = set(reg_lists(ins)) if ins.id == ARM_INS_BX else set()
        return used | {ARM_REG_R0, ARM_REG_R1, ARM_REG_R2, ARM_REG_R3}, {ARM_REG_R0, ARM_REG_R1, ARM_REG_R2, ARM_REG_R3, ARM_REG_LR}
    r, w = ins.regs_access()
    return set(r), set(w)


def measure(rom, f):
    insns = decode(rom, f)
    order = sorted(insns)
    nxt = {a: b for a, b in zip(order, order[1:])}
    prev = {b: insns[a] for a, b in zip(order, order[1:])}
    succ = {}
    for a in order:
        ins = insns[a]
        s = []
        if ins.id == ARM_INS_B and ins.operands and ins.operands[0].type == ARM_OP_IMM:
            t = ins.operands[0].imm
            if t in insns:
                s.append(t)
            if ins.cc not in (ARM_CC_AL, ARM_CC_INVALID) and a in nxt:
                s.append(nxt[a])
        elif is_return(ins) and not (ins.id == ARM_INS_BX and prev.get(a) is not None and prev[a].id == ARM_INS_MOV
                                    and reg_lists(prev[a])[:2] == [ARM_REG_LR, ARM_REG_PC]):
            pass
        elif a in nxt and nxt[a] == a+ins.size:
            s.append(nxt[a])
        succ[a] = s
    ud = {a: uses_defs(insns[a], prev.get(a)) for a in order}
    live = {a: set() for a in order}; flag_live = {a: False for a in order}
    changed = True
    while changed:
        changed = False
        for a in reversed(order):
            out = set(); fout = False
            for b in succ[a]:
                out |= live[b]; fout = fout or flag_live[b]
            u, d = ud[a]
            if is_return(insns[a]):
                u = u | {ARM_REG_R0, ARM_REG_R1}
            new = u | (out - d)
            fnew = reads_flags(insns[a]) or (fout and not writes_flags(insns[a]))
            if new != live[a] or fnew != flag_live[a]:
                live[a], flag_live[a] = new, fnew; changed = True
    entry = int(f['start'], 16)
    cs_name = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    live_in = sorted(cs_name.reg_name(r) for r in live.get(entry, set()) - ABI_IN)
    first = insns.get(entry)
    xor = 0
    for a in order[:-2]:
        i1, i2, i3 = insns[a], insns.get(nxt[a]), insns.get(nxt.get(nxt[a]))
        if i2 is None or i3 is None:
            continue
        if all(i.id == ARM_INS_EOR for i in (i1, i2, i3)):
            r1, r2, r3 = reg_lists(i1), reg_lists(i2), reg_lists(i3)
            if len(r1) >= 2 and len(r2) >= 2 and len(r3) >= 2 and r1[0] == r3[0] and r2[0] != r1[0] \
                    and set(r1[:3]) == set(r2[:3]) == set(r3[:3]):
                xor += 1
    below_sp = sum(1 for i in insns.values() if i.id == ARM_INS_STR and any(
        o.type == ARM_OP_MEM and o.mem.base == ARM_REG_SP and o.mem.disp < 0 for o in i.operands))
    lr_general = 0
    for a in order:
        i = insns[a]
        _, w = ud[a]
        if ARM_REG_LR in w and i.id != ARM_INS_BL and not (i.id == ARM_INS_MOV and reg_lists(i)[:2] == [ARM_REG_LR, ARM_REG_PC]) \
                and not (i.id in (ARM_INS_POP, ARM_INS_LDM)):
            lr_general += 1
    cond = sum(1 for i in insns.values() if i.cc not in (ARM_CC_AL, ARM_CC_INVALID) and i.id != ARM_INS_B)
    regs0 = reg_lists(first) if first else []
    frame = bool(first) and (first.id == ARM_INS_PUSH or (first.id == ARM_INS_STMDB and regs0 and regs0[0] == ARM_REG_SP)) \
        and ARM_REG_LR in regs0
    if not frame and first is not None and f['mode'] == 'arm':
        # APCS frames start with mov ip, sp; stmdb sp!, {..., fp, ip, lr, pc}
        second = insns.get(entry+4)
        frame = bool(second) and second.id in (ARM_INS_STMDB, ARM_INS_PUSH) and ARM_REG_LR in reg_lists(second)
    calls = sorted({hex(i.operands[0].imm) for i in insns.values() if i.id == ARM_INS_BL})
    return {
        'instructions': len(insns),
        'first_instruction': (first.mnemonic+' '+first.op_str).strip() if first else None,
        'swi': [i.operands[0].imm for i in insns.values() if i.id == ARM_INS_SVC and i.operands],
        'status_register_access': sum(1 for i in insns.values() if i.id in (ARM_INS_MRS, ARM_INS_MSR)),
        'non_abi_live_in_registers': live_in,
        'condition_flags_live_in': flag_live.get(entry, False),
        'xor_swaps': xor,
        'stores_below_sp': below_sp,
        'lr_written_as_general_register': lr_general,
        'conditional_non_branch_instructions': cond,
        'conventional_frame_at_entry': frame,
        'direct_calls': calls,
    }


def expected(cls, unit, props, entry):
    """The property each reviewed class relies on. Returns (ok, evidence sentence)."""
    p = props
    if unit == 'register-call-veneer':
        ok = p['instructions'] == 1 and p['first_instruction'].startswith('bx ') and not p['conventional_frame_at_entry']
        return ok, 'single %s; no frame, LR untouched, so the callee returns straight to the BL caller' % p['first_instruction']
    if unit == 'bios-veneer':
        ok = p['instructions'] == 2 and len(p['swi']) == 1
        return ok, 'SWI 0x%02X then return; agbcc has no intrinsic for the SWI opcode' % (p['swi'][0] if p['swi'] else -1)
    if unit == 'state-switch-veneer':
        ok = p['instructions'] == 1 and p['first_instruction'] == 'bx pc'
        return ok, 'bx pc switches to ARM at the next word; the paired ARM branch is installed separately'
    if unit == 'startup':
        ok = p['status_register_access'] >= 2
        return ok, '%d status-register writes (mode changes) and banked stack setup' % p['status_register_access']
    if unit == 'irq':
        ok = p['status_register_access'] >= 1
        return ok, '%d MRS/MSR instructions on SPSR/CPSR (exception state)' % p['status_register_access']
    if unit == 'division-runtime':
        ok = not p['conventional_frame_at_entry'] and p['conditional_non_branch_instructions'] >= 5
        return ok, ('no frame; %d conditionally executed non-branch instructions driven by shift/subtract flags%s'
                    % (p['conditional_non_branch_instructions'],
                       '; condition flags live across blocks' if p['condition_flags_live_in'] else ''))
    if unit == 'renderer-private-abi':
        marks = []
        if p['non_abi_live_in_registers']:
            marks.append('reads %s before defining them' % '/'.join(p['non_abi_live_in_registers']))
        if p['condition_flags_live_in']:
            marks.append('consumes incoming condition flags')
        if p['xor_swaps']:
            marks.append('%d XOR register swaps' % p['xor_swaps'])
        if p['stores_below_sp']:
            marks.append('%d stores below SP without allocation' % p['stores_below_sp'])
        if p['lr_written_as_general_register']:
            marks.append('LR used as a general register (%d writes)' % p['lr_written_as_general_register'])
        if p['conditional_non_branch_instructions']:
            marks.append('%d predicated non-branch instructions' % p['conditional_non_branch_instructions'])
        strong = bool(p['non_abi_live_in_registers'] or p['condition_flags_live_in'] or p['xor_swaps']
                      or p['stores_below_sp'] or p['lr_written_as_general_register'])
        return strong, '; '.join(marks)
    if cls == 'C-candidate':
        return p['conventional_frame_at_entry'], 'conventional compiler frame at entry; ordinary C target'
    if cls in ('fragment-of-owner', 'covered-by-installed-owner'):
        ok = not p['conventional_frame_at_entry'] or bool(p['non_abi_live_in_registers'])
        live = ('; reads %s before defining them' % '/'.join(p['non_abi_live_in_registers'])
                if p['non_abi_live_in_registers'] else '')
        return ok, 'no own prologue%s' % live if not p['conventional_frame_at_entry'] else 'internal label%s' % live
    return False, 'unreviewed'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', type=Path, default=Path('docs/map/finish.json'))
    ap.add_argument('--completeness', type=Path, help='map_completeness.py output for reference counts')
    args = ap.parse_args()
    cfg = json.loads(Path('tools/rom.cfg').read_text())
    rom = Path('baserom.gba').read_bytes()
    if len(rom) != cfg['size'] or hashlib.sha1(rom).hexdigest() != cfg['sha1']:
        raise SystemExit('wrong private ROM')
    functions = json.loads(Path('docs/map/functions.json').read_text())['functions']
    matched = {m['offset']+BASE for m in cfg['matches']}
    refs = {}
    if args.completeness:
        for e in json.loads(args.completeness.read_text())['entry_references']['entries']:
            refs[int(e['start'], 16)] = e
    rows = []; failures = []
    for f in functions:
        at = int(f['start'], 16)
        if at in matched:
            continue
        if at not in REVIEWED:
            failures.append(f['start']+' has no reviewed class')
            continue
        cls, unit, reason = REVIEWED[at]
        props = measure(rom, f)
        ok, evidence = expected(cls, unit, props, at)
        if not ok:
            failures.append('%s (%s/%s) no longer shows its defining property' % (f['start'], cls, unit))
        r = refs.get(at, {})
        extra = {}
        if at in OWNER_END:
            extra = {'owner_end_including_pools': hex(OWNER_END[at]), 'owner_bytes_including_pools': OWNER_END[at]-at}
        rows.append({'start': f['start'], 'end': f['end'], 'mode': f['mode'],
                     'instruction_bytes': int(f['end'], 16)-at, 'class': cls, 'unit': unit, **extra,
                     'reason': reason, 'measured_evidence': evidence, 'properties': props,
                     'code_references': r.get('code_references'), 'data_slot_references': r.get('data_slot_references'),
                     'reachable_from_reset_by_code_edges': r.get('reachable_from_reset_by_code_edges'),
                     'executed_in_recorded_coverage': r.get('executed_in_recorded_coverage')})
    # A front end that calls a helper whose entry reads non-ABI registers shares that private contract.
    by_start = {int(r['start'], 16): r for r in rows}
    for r in rows:
        if r['unit'] != 'renderer-private-abi':
            continue
        for call in r['properties']['direct_calls']:
            callee = by_start.get(int(call, 16))
            if callee and callee['properties']['non_abi_live_in_registers']:
                r['measured_evidence'] += '; calls %s, which reads %s on entry (private register contract)' % (
                    callee['start'], '/'.join(callee['properties']['non_abi_live_in_registers']))
    summary = collections.Counter(); size = collections.Counter()
    for r in rows:
        summary[r['class']] += 1; size[r['class']] += r['instruction_bytes']
    result = {'rom_sha1': cfg['sha1'], 'entries_total': len(functions), 'exact_c_entries': len(matched & {int(f['start'], 16) for f in functions}),
              'unmatched_by_class': dict(summary), 'unmatched_instruction_bytes_by_class': dict(size),
              'verification_failures': failures, 'entries': rows,
              'note': 'Assembly interfaces are counted as documented assembly, never as C. Classes are reviewed; '
                      'properties are re-measured from the ROM on every run.'}
    args.output.write_text(json.dumps(result, indent=1)+'\n')
    print(json.dumps({'unmatched_by_class': dict(summary), 'bytes': dict(size), 'failures': failures}))
    if failures:
        raise SystemExit(1)


if __name__ == '__main__':
    main()

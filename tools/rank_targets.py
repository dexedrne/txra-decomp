#!/usr/bin/env python3
"""Rank remaining entries using verified boundaries, coverage evidence and C dependencies.

Only metadata is printed. Missing dynamic call counts remain null; static caller
counts and the audit's executed/unexecuted evidence are separate columns.
"""
import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def coverage_evidence(directory):
    """Read optional entry counters, and the latest audit's negative entry evidence."""
    counts = {}
    coverage = json.loads((directory / 'coverage.json').read_text())
    # A session's semantic_entries is a total, never a per-function counter.
    for key, value in coverage.get('function_call_counts', {}).items():
        address = int(key, 16)
        if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
            counts[address] = value
    audits = sorted(directory.glob('round*-audit.json'),
                    key=lambda p: int(p.stem.split('-')[0][5:]))
    unexecuted = None
    if audits:
        audit = json.loads(audits[-1].read_text())
        if 'mapped_function_entries_unexecuted' in audit:
            unexecuted = {int(f['start'], 16) for f in audit['mapped_function_entries_unexecuted']}
    return counts, unexecuted


def high_register_live_in(prog, address):
    """Flag obvious non-ABI live-ins; prologue saves are not argument reads.

    This linear check is deliberately only a rejection hint. Passing it does
    not establish definition dominance across branches.
    """
    from code_audit import engine
    from capstone.arm import ARM_INS_MOV, ARM_INS_PUSH, ARM_REG_R8, ARM_REG_R9, ARM_REG_R10, ARM_REG_R11, ARM_REG_R12
    high = {ARM_REG_R8, ARM_REG_R9, ARM_REG_R10, ARM_REG_R11, ARM_REG_R12}
    defined = set()
    prologue = True
    cs = engine('thumb')
    for item in prog.insns[address]:
        offset = item.addr-0x08000000
        ins = next(cs.disasm(prog.rom[offset:offset+4], item.addr, count=1), None)
        if ins is None:
            continue
        reads, writes = map(set, ins.regs_access())
        save = (prologue and ins.id == ARM_INS_MOV and reads.intersection(high)
                and not writes.intersection(high))
        if ins.id != ARM_INS_PUSH and not save:
            prologue = False
        if not save and reads.intersection(high)-defined:
            reg = min(reads.intersection(high)-defined)
            return 'non-argument register %s read before definition; review enclosing function' % cs.reg_name(reg)
        defined.update(writes.intersection(high))
    return None


def arm_leaf_rejection(prog, address):
    """Conservative search admission, not byte-match or general ARM ABI validation."""
    from code_audit import engine
    from capstone import CS_GRP_CALL, CS_GRP_JUMP
    from capstone import arm as a
    cs = engine('arm')
    insns = {}
    end = int(prog.by_start[address]['end'], 16)
    for item in prog.insns[address]:
        offset = item.addr-0x08000000
        ins = next(cs.disasm(prog.rom[offset:offset+4], item.addr, count=1), None)
        if ins is None or ins.size != 4 or item.addr % 4 or not address <= item.addr <= end-4:
            return 'ARM: undecodable or out-of-body instruction'
        insns[item.addr] = ins
    ordered = sorted(insns.values(), key=lambda i: i.address)
    if len(ordered) < 6:
        return 'ARM: unsupported APCS leaf frame'
    first, push = ordered[:2]
    saved = {a.ARM_REG_R4,a.ARM_REG_R5,a.ARM_REG_R6,a.ARM_REG_R7,a.ARM_REG_R8,
             a.ARM_REG_R9,a.ARM_REG_R10,a.ARM_REG_FP,a.ARM_REG_IP,a.ARM_REG_LR,a.ARM_REG_PC}
    if not (first.address == address and first.id == a.ARM_INS_MOV and first.cc == a.ARM_CC_AL
            and [o.reg for o in first.operands] == [a.ARM_REG_IP,a.ARM_REG_SP]
            and push.address == address+4 and push.id == a.ARM_INS_PUSH and push.cc == a.ARM_CC_AL
            and {o.reg for o in push.operands} == saved):
        return 'ARM: unsupported APCS leaf frame'
    restore, ret = ordered[-2:]
    if not (restore.id == a.ARM_INS_LDMDB and restore.cc == a.ARM_CC_AL
            and not restore.writeback
            and restore.operands[0].reg == a.ARM_REG_FP
            and {o.reg for o in restore.operands[1:]} == (saved-{a.ARM_REG_IP,a.ARM_REG_PC})|{a.ARM_REG_SP}
            and ret.id == a.ARM_INS_BX and ret.cc == a.ARM_CC_AL
            and [o.reg for o in ret.operands] == [a.ARM_REG_LR]):
        return 'ARM: unsupported APCS restore'
    frame = None
    allocation = None
    for ins in ordered[2:8]:
        ops = ins.operands
        if (ins.id == a.ARM_INS_SUB and ins.cc == a.ARM_CC_AL and len(ops) == 3
                and ops[0].reg == a.ARM_REG_FP and ops[1].reg == a.ARM_REG_IP
                and ops[2].type == a.ARM_OP_IMM and ops[2].imm == 4):
            frame = ins.address
        if (ins.id == a.ARM_INS_SUB and ins.cc == a.ARM_CC_AL and len(ops) == 3
                and ops[0].reg == a.ARM_REG_SP and ops[1].reg == a.ARM_REG_SP
                and ops[2].type == a.ARM_OP_IMM and ops[2].imm >= 0 and ops[2].imm % 4 == 0):
            allocation = ins.address
    if frame is None:
        return 'ARM: unsupported APCS frame pointer'
    prologue_end = max(frame, allocation or frame)
    for index, ins in enumerate(i for i in ordered if i.address <= prologue_end):
        writes = set(ins.regs_access()[1])
        if (ins.address != address+4*index or ins.cc != a.ARM_CC_AL
                or ins.group(CS_GRP_JUMP) or ins.group(CS_GRP_CALL) or a.ARM_REG_PC in writes
                or (a.ARM_REG_IP in writes and ins.address != address)
                or (a.ARM_REG_FP in writes and ins.address != frame)
                or (a.ARM_REG_SP in writes and ins.address not in (push.address,allocation))):
            return 'ARM: unsupported or interrupted APCS prologue'
    flags = 'condition flags'
    restored = 'restored APCS frame'
    supported = {getattr(a, 'ARM_INS_'+name) for name in (
        'ADC ADD AND ASR B BIC BX CMN CMP EOR LDM LDMDA LDMDB LDR LDRB LDRH LDRSB LDRSH '
        'LSL LSR MLA MOV MUL MVN ORR POP PUSH ROR RRX RSB RSC SBC SMLAL SMULL STM '
        'STMDB STR STRB STRH SUB TEQ TST UMLAL UMULL').split()}
    initial = frozenset({a.ARM_REG_R0,a.ARM_REG_R1,a.ARM_REG_R2,a.ARM_REG_R3,a.ARM_REG_SP,a.ARM_REG_PC})
    states = {}
    work = [(address, initial)]
    returns = steps = 0
    while work:
        at, defined = work.pop()
        if at not in insns:
            return 'ARM: control flow outside declared instruction body'
        if at in states:
            defined = defined & states[at]
            if defined == states[at]:
                continue
        states[at] = defined
        steps += 1
        if steps > 8192:
            return 'ARM: leaf flow budget exceeded'
        ins = insns[at]
        if ins.id in (a.ARM_INS_MRS,a.ARM_INS_MSR,a.ARM_INS_SVC) or ins.usermode:
            return 'ARM: processor state or BIOS contract'
        if ins.group(CS_GRP_CALL):
            return 'ARM: calls require separate ABI review'
        if ins.id not in supported:
            return 'ARM: %s outside supported ARMv4T leaf subset' % ins.mnemonic
        reads, writes = map(set, ins.regs_access())
        if (ins.cc != a.ARM_CC_AL or a.ARM_REG_CPSR in reads) and flags not in defined:
            return 'ARM: incoming condition flags are not C arguments'
        if at == push.address:
            reads = {a.ARM_REG_SP}  # Saving caller values does not define them as C inputs.
        missing = reads-{a.ARM_REG_CPSR}-defined
        if missing:
            return 'ARM: non-argument live-in %s' % cs.reg_name(min(missing))
        if a.ARM_REG_FP in writes and at not in (frame,restore.address):
            return 'ARM: frame pointer overwritten'
        if a.ARM_REG_SP in writes and at not in (push.address,allocation,restore.address):
            return 'ARM: untracked stack write'
        if ins.id in (a.ARM_INS_STR,a.ARM_INS_STRB,a.ARM_INS_STRH):
            mem = ins.operands[1].mem
            if mem.base in (a.ARM_REG_FP,a.ARM_REG_SP):
                width = 1 if ins.id == a.ARM_INS_STRB else 2 if ins.id == a.ARM_INS_STRH else 4
                boundary = -4*(len(saved)-1) if mem.base == a.ARM_REG_FP else (
                    insns[allocation].operands[2].imm if allocation is not None else 0)
                if mem.index or (mem.disp < boundary+4*len(saved) and mem.disp+width > boundary):
                    return 'ARM: store may overwrite saved frame'
        if ins.id in (a.ARM_INS_STM,a.ARM_INS_STMDB) and ins.operands[0].reg in (a.ARM_REG_FP,a.ARM_REG_SP):
            return 'ARM: multiple store needs saved frame review'
        if a.ARM_REG_LR in writes:
            defined = defined-{restored}
        if ins.cc == a.ARM_CC_AL:
            defined = defined | writes
            if ins.update_flags or ins.id in (a.ARM_INS_CMP,a.ARM_INS_CMN,a.ARM_INS_TST,a.ARM_INS_TEQ):
                defined = defined | {flags}
        if at == restore.address:
            defined = defined | {restored}
        if ins.id == a.ARM_INS_BX:
            if at != ret.address:
                return 'ARM: unresolved control transfer'
            if restored not in defined:
                return 'ARM: return bypasses frame restore'
            returns += 1
            continue
        if ins.id == a.ARM_INS_B:
            if len(ins.operands) != 1 or ins.operands[0].type != a.ARM_OP_IMM:
                return 'ARM: unresolved branch'
            if ins.operands[0].imm <= prologue_end:
                return 'ARM: branch replays APCS prologue'
            work.append((ins.operands[0].imm, defined))
            if ins.cc == a.ARM_CC_AL:
                continue
        elif ins.group(CS_GRP_JUMP) or a.ARM_REG_PC in writes:
            return 'ARM: unresolved control transfer'
        work.append((at+4, defined))
    return None if returns else 'ARM: no proven leaf return'


def covering_owner(prog, address, function):
    """Name the installed replacement whose verified byte range holds every span of this entry.

    Internal labels reached by long BL transfers (for example 0800D570/0800D630/0800D960
    inside the installed 0800D51C owner) are already exact; they are not separate work.
    """
    end = int(function['end'], 16)
    spans = [(int(a, 16), int(z, 16)) for a, z in function.get('spans') or [(hex(address), hex(end))]]
    for start, m in prog.matched.items():
        if start != address and all(start <= a and z <= start + m['size'] for a, z in spans):
            return m.get('name', 'func_%08X' % start)
    return None


def rank(prog, counts, unexecuted):
    from code_audit import validate_thumb
    import draft
    rows = []
    for address, function in prog.by_start.items():
        if address in prog.matched:
            continue
        end = int(function['end'], 16)
        insns = prog.insns[address]
        calls = prog.callees.get(address, set())
        callers = prog.callers.get(address, set())
        reason = None
        owner = covering_owner(prog, address, function)
        if owner is not None:
            reason = 'covered by installed %s' % owner
        elif function['mode'] == 'arm':
            reason = arm_leaf_rejection(prog, address)
        elif function['mode'] != 'thumb':
            reason = 'unsupported instruction mode'
        elif not prog.name(address).startswith('func_'):
            reason = 'runtime helper'
        elif any(i.ir[0] in {'swi', 'unknown'} for i in insns):
            reason = 'BIOS veneer or undecoded instruction'
        else:
            unit = validate_thumb(prog.rom, address-draft.BASE,
                                  [{'kind': 'ranked-entry'}], budget=8192)
            if not unit['valid']:
                reason = unit['reason']
            elif any(draft.BASE + a < address or draft.BASE + z > end
                     for a, z in unit.get('spans', [])):
                reason = 'reachable body crosses mapped boundary'
        if reason is None and function['mode'] == 'thumb':
            reason = high_register_live_in(prog, address)
        matched_callees = len(calls.intersection(prog.matched))
        call_count = counts.get(address)
        executed = None if unexecuted is None else address not in unexecuted
        # Counts dominate only when real dynamic counters exist. Otherwise
        # prefer observed entries, then small bodies and recovered dependencies.
        difficulty = len(insns) + 8 * (len(calls)-matched_callees)
        value = (1 + len(callers) + 2*matched_callees) * (2 if executed else 1)
        if call_count is not None:
            value *= 1 + math.log2(1+call_count)
        rows.append({'address': '%08X' % address, 'mode': function['mode'],
                     'bytes': end-address, 'instructions': len(insns),
                     'call_count': call_count, 'observed_entry': executed,
                     'static_callers': len(callers), 'matched_callees': matched_callees,
                     'unmatched_callees': len(calls)-matched_callees,
                     'difficulty': difficulty, 'value': round(value, 3),
                     'priority': round(value/max(1, difficulty), 6),
                     'blocked_reason': reason})
    return sorted(rows, key=lambda r: (r['blocked_reason'] is not None,
                  -(r['call_count'] or 0), r['observed_entry'] is False,
                  -r['priority'], r['difficulty'], r['bytes'], r['address']))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json', action='store_true')
    parser.add_argument('--limit', type=int, default=0)
    parser.add_argument('--smallest-first', action='store_true', help='inspect small standalone bodies before value ordering')
    args = parser.parse_args()
    import sys
    sys.path[:0] = [str(ROOT/'recomp'), str(ROOT/'tools')]
    import draft
    rows = rank(draft.Program(), *coverage_evidence(ROOT/'docs/map'))
    if args.smallest_first:
        rows.sort(key=lambda r: (r['blocked_reason'] is not None, r['bytes'], -r['priority'], r['address']))
    if args.limit:
        rows = rows[:args.limit]
    if args.json:
        print(json.dumps(rows, indent=2))
    else:
        print('address   bytes  insns  dynamic calls  observed  callers  matched callees  difficulty  status')
        for r in rows:
            print('%s %5d %6d %14s %9s %8d %16d %11d  %s' %
                  (r['address'], r['bytes'], r['instructions'],
                   'unknown' if r['call_count'] is None else r['call_count'],
                   r['observed_entry'], r['static_callers'], r['matched_callees'],
                   r['difficulty'], r['blocked_reason'] or 'standalone candidate'))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

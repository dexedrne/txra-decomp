#!/usr/bin/env python3
"""Audit referenced THUMB entries. Output contains offsets and reasons, never bytes.

A passing static check is a proposal for review, not proof of runtime reachability.
No map is changed automatically. Re-run analyze with reviewed seeds, then recomp
and coverage before publishing code classifications.
"""
import argparse
from collections import defaultdict
from bisect import bisect_right
import hashlib
import json
from pathlib import Path
import struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB, CS_MODE_ARM, CS_GRP_JUMP, CS_GRP_CALL
from capstone.arm import *

BASE = 0x08000000


def engine(mode):
    cs = Cs(CS_ARCH_ARM, CS_MODE_THUMB if mode == 'thumb' else CS_MODE_ARM)
    cs.detail = True
    return cs


def pointer_candidates(rom, mapping, base=BASE):
    """Include byte-packed records, isolated slots and table runs."""
    refs = defaultdict(list)
    allowed = bytearray(len(rom))
    for block in mapping:
        if block['type'] in {'table', 'unknown', 'data'}:
            a = block['offset']; z = a + block['size']
            allowed[a:z] = b'\1' * (z-a)
    for block in mapping:
        if block['type'] not in {'table', 'unknown', 'data'}:
            continue
        a, z = block['offset'], block['offset'] + block['size']
        for p in range(a, min(z, len(rom)-3)):
            if not all(allowed[p:p+4]):
                continue
            value = struct.unpack_from('<I', rom, p)[0]
            target = (value & ~1) - base
            if value & 1 and 0 <= target < len(rom):
                refs[target].append({'source_offset': p, 'kind': 'odd-ROM-pointer',
                                     'source_type': block['type'], 'source_format': block.get('format','unspecified'), 'word_aligned': p % 4 == 0})
    return refs


def direct_candidates(rom, splits, base=BASE):
    """Decode only established instruction spans; never search data for BL bits."""
    refs = defaultdict(list)
    for block in splits:
        mode = block['kind']
        if mode not in {'arm', 'thumb'}:
            continue
        a, z = int(block['start'], 16) - base, int(block['end'], 16) - base
        for ins in engine(mode).disasm(rom[a:z], base + a):
            if ins.id == ARM_INS_BL and ins.operands[0].type == ARM_OP_IMM:
                target = ins.operands[0].imm - base
                if 0 <= target < len(rom):
                    refs[(target, mode)].append({'source_offset': ins.address - base, 'kind': 'direct-BL'})
    return refs


def validate_thumb(rom, start, references, forbidden=(), budget=8192, base=BASE):
    """Check all reachable paths, ARMv4T encoding and LR/stack return shape.

    Store instructions and conditional branches are allowed, unlike the old
    linear leaf heuristic. Reject unresolved dispatch, unbalanced stack, calls
    without saving LR, pools on paths and fallthrough into undecodable data.
    """
    if not references:
        return {'valid': False, 'reason': 'no reference'}
    if start % 2 or not 0 <= start < len(rom) - 1:
        return {'valid': False, 'reason': 'unaligned or outside ROM'}
    cs = engine('thumb'); work = [(start, 0, 0, True, None)]; seen = set(); widths = {}; occupied = {}; returns = 0
    blocked = set(forbidden)
    def fail(reason):
        return {'valid': False, 'reason': reason}
    while work:
        at, depth, saved_lr, lr_intact, popped = work.pop()
        state = (at, depth, saved_lr, lr_intact, popped)
        if state in seen:
            continue
        seen.add(state)
        if len(seen) > budget:
            return fail('validation budget exceeded')
        if at < 0 or at + 2 > len(rom) or any(p in blocked for p in range(at, at+2)):
            return fail('path leaves ROM or enters established literal/data pool')
        ins = next(cs.disasm(rom[at:at+4], base+at, count=1), None)
        if not ins:
            return fail('undecodable reachable instruction')
        # v4T THUMB has no wide instruction except the original BL pair.
        w = struct.unpack_from('<H', rom, at)[0]
        supported = (w < 0xb000 or w & 0xff00 == 0xb000 or w & 0xf600 == 0xb400
                     or w & 0xf000 == 0xc000 or (w & 0xf000 == 0xd000 and w & 0x0f00 != 0x0e00)
                     or w & 0xf800 == 0xe000 or (w & 0xf800 == 0xf000 and ins.id == ARM_INS_BL))
        if not supported:
            return fail('instruction outside supported ARMv4T subset')
        if (ins.size == 4 and (ins.id != ARM_INS_BL or w & 0xf800 != 0xf000)) or ins.mnemonic.startswith(('bkpt', 'udf', 'it', 'cbz', 'cbnz', 'blx', 'cps', 'rev', 'sx', 'ux')):
            return fail('instruction outside supported ARMv4T subset')
        if ins.size != 2 and ins.id != ARM_INS_BL:
            return fail('unsupported instruction width')
        if any(p in occupied and occupied[p] != at for p in range(at, at+ins.size)):
            return fail('branch enters instruction interior')
        if any(p in blocked for p in range(at, at+ins.size)):
            return fail('instruction overlaps established literal/data pool')
        if ins.id != ARM_INS_BL and ARM_REG_LR in ins.regs_access()[1]:
            return fail('untracked LR write')
        widths[at] = ins.size
        for p in range(at, at+ins.size):
            occupied[p] = at
        ops = ins.operands; nxt = at + ins.size; was_popped = popped; popped = None
        if saved_lr and ins.mnemonic.startswith('str'):
            for op in ops:
                if op.type == ARM_OP_MEM and op.mem.base == ARM_REG_SP:
                    if op.mem.index or abs((depth-op.mem.disp)-saved_lr) < 4:
                        return fail('store may overwrite saved return address')
        if ins.id == ARM_INS_PUSH:
            if any(op.reg == ARM_REG_LR for op in ops):
                if saved_lr:
                    return fail('nested LR save needs manual review')
                if not lr_intact:
                    return fail('saving overwritten LR needs manual review')
                saved_lr = depth + 4
            depth += 4 * len(ops)
        elif ins.id == ARM_INS_POP:
            old_depth = depth
            depth -= 4 * len(ops)
            if depth < 0:
                return fail('stack underflow')
            restored = None
            if saved_lr and depth < saved_lr <= old_depth:
                restored = ops[(old_depth-saved_lr)//4].reg
                saved_lr = 0
            if any(op.reg == ARM_REG_PC for op in ops):
                if depth or restored != ARM_REG_PC:
                    return fail('unbalanced or unsaved stack return')
                returns += 1; continue
            popped = restored
        elif ins.id in (ARM_INS_ADD, ARM_INS_SUB) and ops[0].type == ARM_OP_REG and ops[0].reg == ARM_REG_SP:
            if ops[-1].type != ARM_OP_IMM:
                return fail('dynamic stack adjustment')
            depth += ops[-1].imm * (1 if ins.id == ARM_INS_SUB else -1)
            if saved_lr > depth:
                saved_lr = 0
        elif ARM_REG_SP in ins.regs_access()[1]:
            return fail('untracked stack write')
        if depth < 0 or depth > 4096:
            return fail('invalid stack depth')
        if ins.id == ARM_INS_BL:
            target = ops[0].imm - base
            if not saved_lr or not 0 <= target < len(rom):
                return fail('call without saved LR or outside ROM')
            lr_intact = False
        elif ins.id == ARM_INS_BX:
            reg = ops[0].reg
            if depth == 0 and (reg == was_popped or (reg == ARM_REG_LR and lr_intact)):
                returns += 1; continue
            return fail('unresolved BX or unbalanced return')
        elif ins.id == ARM_INS_B:
            work.append((ops[0].imm-base, depth, saved_lr, lr_intact, popped))
            if ins.cc == ARM_CC_AL:
                continue
        elif ins.group(CS_GRP_JUMP) or ins.group(CS_GRP_CALL) or ARM_REG_PC in ins.regs_access()[1]:
            return fail('unresolved control transfer')
        if ins.id == ARM_INS_LDR and len(ops) > 1 and ops[1].type == ARM_OP_MEM and ops[1].mem.base == ARM_REG_PC:
            pool = ((base+at+4) & ~3) + ops[1].mem.disp - base
            if not 0 <= pool <= len(rom)-4:
                return fail('literal outside ROM')
            blocked.update(range(pool, pool+4))
            if any(p in blocked for p in occupied):
                return fail('literal overlaps reachable instruction')
        work.append((nxt, depth, saved_lr, lr_intact, popped))
    if not returns:
        return fail('no proven return (loop or tail transfer needs manual review)')
    spans = []
    for at, width in sorted(widths.items()):
        if spans and spans[-1][1] == at:
            spans[-1][1] += width
        else:
            spans.append([at, at+width])
    return {'valid': True, 'reason': 'referenced; all paths decode; balanced return; ARMv4T',
            'spans': spans, 'return_sites': returns}


def indirect_candidates(indirect, cfg):
    """Follow resolved BX/veneer targets, including unique copied-code aliases."""
    refs = defaultdict(list)
    unresolved = []
    for site in indirect.get('transfers', []) + indirect.get('veneer_calls', []):
        if site.get('kind') == 'return':
            continue
        values = set(site.get('targets', [])) | set(site.get('possible_targets_from_writes', []))
        if site.get('target'):
            values.add(site['target'])
        if not values:
            unresolved.append(site['source'])
        for value in sorted(values):
            raw = int(value, 16); address = raw & ~1
            aliases = {(c['load']+address-c['run'], c['mode']) for c in cfg.get('copies', [])
                       if c['run'] <= address < c['run']+c['size']}
            if cfg['base'] <= address < cfg['base']+cfg['size']:
                aliases = {(address, 'thumb' if raw & 1 or site.get('mode') == 'thumb' and site.get('confidence') == 'bounded switch' else 'arm')}
            if len(aliases) != 1:
                unresolved.append(site['source'])
                continue
            address, mode = aliases.pop()
            refs[address-cfg['base'], mode].append({'source_offset': int(site['source'],16)-cfg['base'],
                                                  'kind': 'resolved-indirect', 'runtime_target': value})
    return refs, sorted(set(unresolved))


def audit(rom, cfg, functions, splits, indirect=None):
    known = {(int(f['start'], 16)-cfg['base'], f['mode']) for f in functions}
    refs = {(at, 'thumb'): values for at, values in pointer_candidates(rom, cfg['mapping'], cfg['base']).items()}
    for key, values in direct_candidates(rom, splits, cfg['base']).items():
        refs.setdefault(key, []).extend(values)
    indirect_refs, unresolved = indirect_candidates(indirect or {}, cfg)
    for key, values in indirect_refs.items():
        refs.setdefault(key, []).extend(values)
    modes = {p:s['kind'] for s in splits if s['kind'] in {'arm','thumb'}
             for p in range(int(s['start'],16)-cfg['base'], int(s['end'],16)-cfg['base'])}
    switch_sources = {s['source'] for s in (indirect or {}).get('transfers',[]) if s.get('confidence') == 'bounded switch'}
    far_sources = {j['source']-cfg['base'] for j in cfg.get('far_jumps', [])}
    pools = {p for s in splits if s['kind'] == 'literal'
             for p in range(int(s['start'],16)-cfg['base'], int(s['end'],16)-cfg['base'])}
    partition = sorted(cfg['mapping'],key=lambda s:s['offset'])
    starts = [s['offset'] for s in partition]
    rows = []
    for (at, mode), references in sorted(refs.items()):
        if (at, mode) in known:
            result = {'status': 'existing-entry', 'reason': 'already in function inventory'}
        elif at in modes and modes[at] != mode:
            result = {'status':'rejected', 'reason':'pointer conflicts with established instruction mode'}
        elif references and all(r['kind']=='resolved-indirect' and f"0x{cfg['base']+r['source_offset']:08X}" in switch_sources for r in references):
            result = {'status':'internal-switch-target', 'reason':'bounded switch block inside an existing function; not a function call'}
        elif references and all(r['kind']=='direct-BL' and r['source_offset'] in far_sources for r in references):
            result = {'status':'internal-far-jump', 'reason':'reviewed Thumb long branch inside an existing function; not a function call'}
        elif mode != 'thumb':
            result = {'status': 'manual-review', 'reason': 'new ARM direct target requires ARM validator'}
        else:
            result = validate_thumb(rom, at, references, pools, base=cfg['base'])
            result['status'] = 'proposal' if result.pop('valid') else 'rejected'
        index = bisect_right(starts,at)-1
        block = partition[index] if index >= 0 else None
        context = ({'type':block['type'],'format':block.get('format','unspecified')}
                   if block and at < block['offset']+block['size'] else None)
        rows.append({'offset': at, 'mode': mode, 'target_classification':context, 'references': references, **result})
    return {'complete': False, 'rom_sha1': cfg['sha1'],
            'input_mapping_sha256': hashlib.sha256(json.dumps(cfg['mapping'],sort_keys=True).encode()).hexdigest(),
            'scanned_source_bytes': sum(s['size'] for s in cfg['mapping'] if s['type'] in {'table','unknown','data'}),
            'reference_counts': dict((kind,sum(r['kind']==kind for row in rows for r in row['references']))
                                     for kind in ('odd-ROM-pointer','direct-BL','resolved-indirect')),
            'candidates': rows,
            'unresolved_indirect_sites': unresolved,
            'counts': {s: sum(r['status'] == s for r in rows) for s in ('existing-entry', 'proposal', 'rejected', 'manual-review', 'internal-switch-target', 'internal-far-jump')},
            'caveat': 'Proposals require review and runtime coverage before seed/map acceptance. Rejections are retained with reasons.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', type=Path, default=Path('docs/map/code-audit.json'))
    args = p.parse_args()
    cfg = json.loads(Path('tools/rom.cfg').read_text())
    rom = Path('baserom.gba').read_bytes()
    if len(rom) != cfg['size'] or hashlib.sha1(rom).hexdigest() != cfg['sha1']:
        raise SystemExit('wrong ROM')
    result = audit(rom, cfg, json.loads(Path('docs/map/functions.json').read_text())['functions'],
                   json.loads(Path('docs/map/splits.json').read_text())['regions'],
                   json.loads(Path('docs/map/indirect.json').read_text()))
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result['counts']))

if __name__ == '__main__':
    main()

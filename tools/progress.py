#!/usr/bin/env python3
"""Report compiled mapped functions and explicitly reviewed execution milestones."""
import json, subprocess, hashlib
from pathlib import Path
def mapping_progress(cfg):
    size=cfg['size']; end=0; code=data=unknown=0
    for block in cfg.get('mapping', []):
        start=block['offset']; count=block['size']
        if block['type'] not in {'code','data','graphics','audio','compressed','table','text','fill','unknown'}:
            raise ValueError('unrecognized mapping type')
        if start != end or count<=0 or start+count>size:
            raise ValueError('mapping must partition the ROM without gaps or overlaps')
        end=start+count
        if block['type']=='code': code+=count
        elif block['type']=='unknown': unknown+=count
        else: data+=count
    if end and end!=size: raise ValueError('mapping does not cover the ROM')
    if not end: unknown=size
    return dict(rom_bytes=size, code_bytes_mapped=code, data_bytes_mapped=data, unknown_bytes=unknown)

def completion(fs, cfg, finish, unresolved=()):
    """'Complete' = exact C, or an internal label inside an installed exact owner, or a documented
    assembly interface. Assembly is reported separately and never counted as C."""
    starts = {int(f['start'], 16) for f in fs}
    base = cfg.get('base', 0x08000000)
    exact = sum(1 for m in cfg.get('matches', []) if m['offset']+base in starts)
    rows = finish.get('entries', [])
    by = lambda cls: [r for r in rows if r['class'] == cls]
    asm, covered, owners, fragments = (by('assembly-interface'), by('covered-by-installed-owner'),
                                      by('C-candidate'), by('fragment-of-owner'))
    unreferenced = {r['start'] for r in rows if not r.get('code_references') and not r.get('data_slot_references')
                    and r.get('code_references') is not None}
    done = exact + len(covered) + len(asm)
    return {
        'definition': 'complete entry = exact C replacement, internal label inside an installed exact owner, '
                      'or documented assembly interface (docs/map/finish.json); assembly is never counted as C',
        'entries_total': len(fs),
        'exact_c_entries': exact,
        'internal_labels_inside_exact_owners': len(covered),
        'documented_assembly_interfaces': len(asm),
        'assembly_interface_instruction_bytes': sum(r['instruction_bytes'] for r in asm),
        'complete_entries': done,
        'remaining_c_owners': [r['start'] for r in owners],
        'remaining_c_owner_bytes_including_pools': sum(r.get('owner_bytes_including_pools', 0) for r in owners),
        'remaining_fragments_inside_c_owners': len(fragments),
        'remaining_entries': len(owners) + len(fragments),
        'indirect_sites_unresolved_but_unreferenced': len(set(unresolved) & unreferenced),
    }

def main():
    fs=json.loads(Path('docs/map/functions.json').read_text())['functions']
    source=Path('build/generated.c'); emitted=Path('build/emitted.json')
    obj=Path('build/generated.o'); binary=Path('build/txra-pc')
    n=0
    if all(p.exists() for p in (source,emitted,obj,binary)) and obj.stat().st_mtime>=source.stat().st_mtime and binary.stat().st_mtime>=obj.stat().st_mtime:
        result=subprocess.run(['nm','--defined-only',str(obj)],capture_output=True,text=True,check=True)
        symbols={line.split()[-1] for line in result.stdout.splitlines() if line.split()}
        n=sum(f"fn_{int(f['start'],16):08x}_{int(f['mode']=='thumb')}" in symbols for f in fs)
    cfg=json.loads(Path('tools/rom.cfg').read_text())
    counts=mapping_progress(cfg)
    pointers=json.loads(Path('docs/map/pointers.json').read_text())
    indirect=json.loads(Path('docs/map/indirect.json').read_text())
    unresolved={t['source'] for t in indirect['transfers'] if t['kind']=='indirect' and t['target'] is None and not t.get('targets')}
    unresolved.update(t['source'] for t in indirect.get('veneer_calls',[]) if t['target'] is None)
    unresolved-=set(cfg.get('indirect_sources_observed', []))
    counts.update(functions_found=len(fs),functions_thumb=sum(f['mode']=='thumb' for f in fs),
                  functions_arm=sum(f['mode']=='arm' for f in fs),jump_tables=len(pointers['switches']),
                  indirect_targets_unresolved=len(unresolved))
    verified=Path('build/milestones.json')
    m=json.loads(verified.read_text()) if verified.exists() else {}
    verified_build=binary.exists() and m.get('build_sha256')==hashlib.sha256(binary.read_bytes()).hexdigest()
    progress={**counts,'functions_mapped':len(fs),'functions_recompiled':n,
              'boots':bool(n and verified_build and m.get('boots',False)),
              'reaches_title':bool(n and verified_build and m.get('reaches_title',False)),
              'playable':bool(n and verified_build and m.get('playable',False)),
              'full_race':bool(n and verified_build and m.get('full_race',False)),
              'saves':bool(n and verified_build and m.get('saves',False)),
              'evidence':m.get('evidence','No PC execution verified for this build yet.') if verified_build else 'No execution milestones reviewed for this exact executable yet.'}
    previous = json.loads(Path('progress.json').read_text()) if Path('progress.json').exists() else {}
    for key in ('match10_search', 'deep_hand_b', 'llm_attempts', 'llm_success_rate', 'llm_requests',
                'llm_answers_pending_judgement', 'deterministic_matches', 'hand_matches_added'):
        if key in previous: progress[key] = previous[key]
    matched_bytes = sum(m['size'] for m in cfg.get('matches', []))
    matched_count = len(cfg.get('matches', []))
    progress['functions_matched_c'] = {
        'count': matched_count, 'bytes_including_pools': matched_bytes,
        'percent_of_mapped_code': round(100 * matched_bytes / counts['code_bytes_mapped'], 3)
                                  if counts['code_bytes_mapped'] else 0}
    progress['functions_c_matched'] = matched_count
    finish_path = Path('docs/map/finish.json')
    if finish_path.exists():
        progress['completion'] = completion(fs, cfg, json.loads(finish_path.read_text()), unresolved)
    Path('progress.json').write_text(json.dumps(progress,indent=2)+'\n')
    print(json.dumps(progress))

if __name__ == '__main__': main()

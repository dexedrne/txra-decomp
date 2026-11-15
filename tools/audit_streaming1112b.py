#!/usr/bin/env python3
"""Reproduce complete streaming-owner boundaries and call/stack metadata.

No mapping or match registry is edited. The apparent call to 08003786 is a
long backward loop transfer within the owner; it is never an independent C ABI.
"""
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import sys

sys.path[:0]=[str(Path(__file__).resolve().parent),str(Path(__file__).resolve().parents[1]/'recomp')]
import draft
from code_audit import validate_thumb


def main():
    p=draft.Program()
    assert hashlib.sha1(p.rom).hexdigest()==p.cfg['sha1']
    entries=[0x08002854,0x08003786]
    insns=sorted((i for a in entries for i in p.insns[a]),key=lambda i:i.addr)
    spans=[(int(a,16),int(z,16)) for t in entries for a,z in p.by_start[t]['spans']]
    pools={k for a in entries for k in draft.pool_words(p,a)}
    forbidden={v-draft.BASE for q in pools for v in range(q,q+4)}
    validation=validate_thumb(p.rom,0x2854,[{'kind':'reviewed-existing-owner'}],forbidden,budget=20000)
    assert validation['valid'],validation
    independent={a for s,z in validation['spans'] for a in range(s+draft.BASE,z+draft.BASE)}
    established={a for s,z in spans for a in range(s,z)}
    assert independent==established,'recursive paths and mapped owner union differ'
    calls=[];internal=[]
    for i in insns:
        if i.ir[0]!='call':continue
        target=i.ir[1]
        record=dict(source='%08X'%i.addr,target='%08X'%target)
        if target in entries:
            assert i.addr==0x0800416A and target==0x08003786
            record.update(kind='long loop transfer',returns_to_next_instruction=False)
            internal.append(record)
        else:
            assert target in (0x08005F48,0x08005DD4)
            record.update(kind='normal helper call',arguments=5 if target==0x08005F48 else 4)
            calls.append(record)
    slots=Counter()
    for i in insns:
        if i.ir[0] in ('load','store') and i.ir[-2]==13 and isinstance(i.ir[-1],tuple) and i.ir[-1][0]=='#':
            slots[i.ir[-1][1]]+=1
    addressed=[i.addr for i in insns if i.ir[0]=='alu' and i.ir[2]=='add' and i.ir[3]==13]
    assert not addressed,'addressed local buffers need explicit recovery'
    assert max(pools)+4==0x0800418C and max(z for s,z in spans)==0x0800417E
    r=dict(entry='08002854',suggested_name='build_streamed_course_ring_slot',
           instruction_end_exclusive='0800417E',complete_end_exclusive='0800418C',complete_bytes=6456,
           instruction_bytes=sum(z-a for a,z in spans),instructions=len(insns),literal_words=len(pools),
           frame_bytes=268,static_balanced_return=True,static_path_union_matches_registry=True,
           existing_internal_entry='08003786',independent_function_count=1,new_functions_mapped=0,
           calls= calls,internal_transfers=internal,
           stack_slot_accesses={str(k):v for k,v in sorted(slots.items())},
           addressed_local_buffers=0,
           phases=[dict(start='08002854',end='080029F0',purpose='Select wrapped course window, select ring output slot, clear 24 point and quad active flags.'),
                   dict(start='080029F0',end='0800375A',purpose='Generate conditional edge and base geometry; structured recovery unfinished.'),
                   dict(start='0800375A',end='0800416E',purpose='Prepare and process two feature bytes; backward transfer repeats the existing frame.'),
                   dict(start='0800416E',end='0800417E',purpose='Release 268-byte frame, restore high and low registers, return to saved caller.')],
           caveats=['Static boundary and synthetic opening checks only; no gameplay reachability claim.',
                    'The generic draft call inference reports only four register arguments for 08005F48. Its installed C has a fifth signed y argument at caller sp+0; preserve it.',
                    'Only the recovered opening has a structured C hypothesis. No complete owner C or byte-distance claim is supplied.'])
    path=Path('docs/near-misses/breadth-1112b/streaming-owner.json.gz')
    with gzip.open(path,'wt') as stream:json.dump(r,stream,indent=2)
    print(json.dumps({k:r[k] for k in ('complete_bytes','instruction_bytes','instructions','literal_words','frame_bytes','static_balanced_return','new_functions_mapped')}))


if __name__=='__main__':main()

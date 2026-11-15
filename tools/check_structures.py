#!/usr/bin/env python3
"""Check all reverse blocks against guest CPU execution; never emit payloads."""
import hashlib
import json
import subprocess
from pathlib import Path
from structures import reverse_blocks, reverse_decode

def main():
    rom=Path('baserom.gba').read_bytes()
    cfg=json.loads(Path('tools/rom.cfg').read_text())
    if hashlib.sha1(rom).hexdigest()!=cfg['sha1']:raise ValueError('wrong private ROM')
    Path('build/map3').mkdir(parents=True,exist_ok=True)
    blocks=list(reverse_blocks(rom))
    if len(blocks)!=24:raise ValueError('expected 24 independently referenced reverse blocks')
    command=['cc','-O2','-std=c11','-Iruntime','tests/structure_reference.c',
             'runtime/cpu.c','runtime/memory.c','runtime/hardware.c','runtime/coverage.c',
             '-o','build/structure-reference']
    subprocess.run(command,check=True)
    result=subprocess.run(['build/structure-reference','baserom.gba'],
        input=''.join(f'{b["offset"]} {b["decompressed_size"]}\n' for b in blocks),
        capture_output=True,text=True,check=True)
    got=dict(map(int,line.split()) for line in result.stdout.splitlines())
    for block in blocks:
        decoded,_=reverse_decode(rom,block['offset'],block['decompressed_size'])
        value=2166136261
        for byte in decoded:value=((value^byte)*16777619)&0xffffffff
        if got[block['offset']]!=value:raise ValueError('guest/custom decoder mismatch')
    Path('build/map3/structure-reference.json').write_text(json.dumps(
        {'blocks_checked':len(blocks),'all_output_hashes_match':True,
         'method':'Independent guest CPU execution of 0801251C versus checked structural decoder'},indent=2)+'\n')
    print(f'{len(blocks)} complete reverse blocks match guest CPU output hashes')

if __name__=='__main__':main()

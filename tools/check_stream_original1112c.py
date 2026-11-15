#!/usr/bin/env python3
"""Compare complete streaming geometry against original instructions in memory."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR

sys.path[:0]=[str(Path(__file__).resolve().parent),str(Path(__file__).resolve().parents[1]/'recomp')]
import draft
import reloc
import measure_candidate as mc
from check_contact_original1112c import word
from check_hud_original1112c import SAVED,ARGS

START,END,RETURN=0x08002854,0x0800418C,0x0F000000


def initialize(case):
    iwram=bytearray(0x8000)
    ewram=bytearray([0x5a])*0x40000
    length=64
    position=[0,1,2,31,62,63][case%6]
    direction=(case//6)&1
    center=(position+28)%length if direction==0 else (position-1)%length
    for addr,value in [(0x2334,direction),(0x5f50,position),(0x2e4c,length),
                       (0x1b8,(case*7)&31),(0x6874,0x02000400),(0x5f48,0x6c6c)]:
        word(iwram,addr,value)
    scenery=(case//12)%20
    variant=case//240
    second_type=(scenery+7)%20 if variant and case&1 else scenery if case&1 else 0
    for i in range(length):
        a=0x400+i*28
        for off,value in [(0,i*64),(4,(i%7)*16),(8,i*96)]: word(ewram,a+off,value)
        word(ewram,a+12,(i*71+case*13)&16383,2)
        for j in range(3): ewram[a+14+j]=(case+i+j)%9
        ewram[a+17]=(case+i//(1+variant%3))%4
        ewram[a+19]=(case+i//2)%4
        ewram[a+20]=(case+i//(1+variant%2))%3
        ewram[a+21]=(case+i//3)%3
        ewram[a+22]=(case//24+variant)&1
        ewram[a+23]=0
        ewram[a+24]=0
    # The arch family refers to the preceding bridge and bank seam vertices.
    # Preserve that valid-state dependency instead of reading uninitialized stack.
    if 3<=scenery<=11 or 3<=second_type<=11:
        if center&1: center=(center+1)%length
        position=(center-28)%length if direction==0 else (center+1)%length
        word(iwram,0x5f50,position)
        ewram[0x400+center*28+22]=1
        ewram[0x400+center*28+21]=0
        ewram[0x400+((center-2)%length)*28+21]=1
    ewram[0x400+center*28+23]=scenery
    ewram[0x400+center*28+24]=second_type
    return bytes(iwram),bytes(ewram),scenery,direction


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('candidate',type=Path)
    ap.add_argument('receipt',type=Path)
    ap.add_argument('--cases',type=int,default=480)
    args=ap.parse_args()
    p=draft.Program()
    assert hashlib.sha1(p.rom).hexdigest()=='4197339d4add74bb40ed02a8fba5e58096afb487'
    code=args.candidate.read_text()
    actual,_=mc.diagnostic_compile(code,'func_08002854',START,reloc.symbols(p),'old')
    assert len(actual)<=END-START
    engines=[]
    for compiled in (False,True):
        uc=Uc(UC_ARCH_ARM,UC_MODE_THUMB)
        for base,size in [(0x02000000,0x40000),(0x03000000,0x8000),(0x08000000,0x400000)]: uc.mem_map(base,size)
        uc.mem_write(0x08000000,p.rom)
        if compiled: uc.mem_write(START,actual)
        engines.append(uc)
    traces=[[],[]]
    def observe(uc,address,size,slot):
        values=[uc.reg_read(r) for r in ARGS]
        if address==0x08005f48: values.append(int.from_bytes(uc.mem_read(uc.reg_read(UC_ARM_REG_SP),4),'little'))
        traces[slot].append([address,*values])
    for slot,uc in enumerate(engines):
        for entry in (0x08005dd4,0x08005f48): uc.hook_add(UC_HOOK_CODE,observe,slot,begin=entry,end=entry)
    calls=0
    types=set()
    directions=set()
    for case in range(args.cases):
        iwram,ewram,scenery,direction=initialize(case)
        types.add(scenery)
        directions.add(direction)
        outcomes=[]
        for slot,uc in enumerate(engines):
            traces[slot].clear()
            uc.mem_write(0x03000000,iwram)
            uc.mem_write(0x02000000,ewram)
            uc.reg_write(UC_ARM_REG_CPSR,0x3f)
            for i,r in enumerate(SAVED): uc.reg_write(r,0x45670000+i)
            uc.reg_write(UC_ARM_REG_SP,0x03007e00)
            uc.reg_write(UC_ARM_REG_LR,RETURN|1)
            uc.emu_start(START|1,RETURN,count=100000)
            assert uc.reg_read(UC_ARM_REG_PC)==RETURN,'instruction limit or bad return'
            assert uc.reg_read(UC_ARM_REG_SP)==0x03007e00
            assert [uc.reg_read(r) for r in SAVED]==[0x45670000+i for i in range(8)]
            outcomes.append(bytes(uc.mem_read(0x02000000,0x40000))+bytes(uc.mem_read(0x03000000,0x7000)))
        if outcomes[0]!=outcomes[1] or traces[0]!=traces[1]:
            location=next((i for i,(a,b) in enumerate(zip(*outcomes)) if a!=b),None)
            call=next((i for i,(a,b) in enumerate(zip(*traces)) if a!=b),None)
            address=hex(0x02000000+location) if location is not None and location<0x40000 else hex(0x03000000+location-0x40000) if location is not None else None
            details=dict(case=case,scenery=scenery,direction=direction,address=address,
                         call=call,original_calls=len(traces[0]),candidate_calls=len(traces[1]))
            args.receipt.write_text(json.dumps(dict(passed=case,failure=details,installation_authority=False),indent=2)+'\n')
            raise AssertionError('original streaming mismatch: '+json.dumps(details))
        calls+=len(traces[0])
    receipt=dict(candidate=args.candidate.as_posix(),source_sha256=hashlib.sha256(code.encode()).hexdigest(),
        compiled_sha256=hashlib.sha256(actual).hexdigest(),cases=args.cases,passed=args.cases,
        ordered_helper_calls_compared=calls,scenery_types=sorted(types),directions=sorted(directions),
        compared='all EWRAM, IWRAM below stack, helper arguments/order, callee-saved registers and stack restoration',
        original_instructions_executed=True,original_helpers_executed=True,helper_calls_mocked=False,
        private_rom_identity_verified=True,binary_artifacts_written=False,installation_authority=False,
        limitations='Bounded synthetic states with bridge/bank dependencies for arch types; original lookup data. No arbitrary malformed-state or gameplay claim.')
    args.receipt.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt))


if __name__=='__main__': main()

#!/usr/bin/env python3
"""Run the original and candidate HUD with the original helpers in memory.

States are synthetic; all lookup data and helper instructions are read from
the private ROM. Nothing read from the ROM is written to an artifact. This is
a bounded regression experiment, not an installation gate or gameplay proof.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

from unicorn import Uc,UC_ARCH_ARM,UC_MODE_THUMB,UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC,UC_ARM_REG_CPSR

sys.path[:0]=[str(Path(__file__).resolve().parent),str(Path(__file__).resolve().parents[1]/'recomp')]
import draft
import reloc
import measure_candidate as mc
from check_contact_original1112c import word

START,END,RETURN=0x0800421C,0x08005238,0x0F000000
SAVED=[UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]
ARGS=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3]


def initialize(seed):
    state=bytearray(0x8000)
    timers=[0,1,2,31,32,63,64,95,96,127,150]
    modes=[0,1,2,3,32,33]
    for a,v in [(0xac0,seed%29==0),(0x2330,timers[seed%11]),(0x5f54,timers[(seed//3)%11]),
                (0x1bc,modes[(seed//7)%6]),(0x4780,seed%8),(0x1b14,(seed//5)%3),
                (0x2a28,seed*31%12000),(0x1e50,(seed//11)%6)]: word(state,a,v,2)
    for a,v in [(0x21d4,2 if seed%7==0 else 1),(0x1b1c,seed&15),(0x21d8,seed&1),
                (0x61e4,seed%16),(0x6680,seed%8),(0x2a18,4096),(0x5f58,4096),
                (0x5f78,-4096),(0x5f88,4096)]: word(state,a,v)
    for i in range(8):
        word(state,0x46e2+i*4,100+i*16,2)
        a=0x1e60+i*100
        fields=[(0,(seed+i)%5!=0,2),(2,16+i%4,2),(4,(seed*3+i*17)%1024-512,4),
            (8,(seed+i*11)%128-64,4),(12,(seed*5+i*23)%1024-512,4),
            (28,seed+i,4),(32,seed%256,4),(36,seed*7%256,4),(40,(seed*47+i*211)%8000-2000,4),
            (48,198+(seed+i)%5,4),(64,43+(seed+i)%4,2),(68,(seed//13)&3,2),
            (82,seed%5,2),(98,(seed*3+i*7)%100,2)]
        for offset,v,size in fields: word(state,a+offset,v,size)
        for offset,v in [(0,(seed+i)%3==0),(4,100+(seed+i)%40),(8,70+(seed+i)%30),(12,(seed+i)%23)]:
            word(state,0xad0+i*16+offset,v)
        for offset,v in [(0,1 if seed%9==0 else (seed+i)%7),(4,i*8-32),(8,0),(12,193+i*3)]:
            word(state,0x67f0+i*16+offset,v)
        state[0x5790+i]=(seed+i)%10
    for i in range(128): state[0x5680+i*2]=i&1
    state[0xde8:0xdee]=b'A1 B2C'
    return bytes(state)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('candidate',type=Path)
    ap.add_argument('receipt',type=Path)
    ap.add_argument('--cases',type=int,default=192)
    args=ap.parse_args()
    p=draft.Program()
    assert hashlib.sha1(p.rom).hexdigest()=='4197339d4add74bb40ed02a8fba5e58096afb487'
    code=args.candidate.read_text()
    actual,_=mc.diagnostic_compile(code,'func_0800421C',START,reloc.symbols(p),'old')
    assert len(actual)<=END-START
    engines=[]
    for compiled in (False,True):
        uc=Uc(UC_ARCH_ARM,UC_MODE_THUMB)
        for base,size in [(0x02000000,0x40000),(0x03000000,0x8000),(0x04000000,0x1000),
                          (0x05000000,0x1000),(0x06000000,0x20000),(0x07000000,0x1000),
                          (0x08000000,0x400000)]: uc.mem_map(base,size)
        uc.mem_write(0x08000000,p.rom)
        if compiled: uc.mem_write(START,actual)
        engines.append(uc)
    traces=[[],[]]
    def observe(uc,address,size,slot):
        argc={0x08005cf4:5,0x0801533c:9,0x0801604c:2,0x080162f8:2}[address]
        values=[uc.reg_read(r) for r in ARGS[:argc]]
        if argc>4:
            stack=uc.reg_read(UC_ARM_REG_SP)
            values += [int.from_bytes(uc.mem_read(stack+i*4,4),'little') for i in range(argc-4)]
        traces[slot].append([address,*values])
    for slot,uc in enumerate(engines):
        for entry in (0x08005cf4,0x0801533c,0x0801604c,0x080162f8):
            uc.hook_add(UC_HOOK_CODE,observe,slot,begin=entry,end=entry)
    call_count=changed=0
    for seed in range(args.cases):
        state=initialize(seed)
        outcomes=[]
        for slot,uc in enumerate(engines):
            traces[slot].clear()
            uc.mem_write(0x03000000,state)
            uc.reg_write(UC_ARM_REG_CPSR,0x3f)
            for i,r in enumerate(SAVED): uc.reg_write(r,0x45670000+i)
            uc.reg_write(UC_ARM_REG_SP,0x03007e00)
            uc.reg_write(UC_ARM_REG_LR,RETURN|1)
            uc.emu_start(START|1,RETURN,count=100000)
            assert uc.reg_read(UC_ARM_REG_PC)==RETURN,'instruction limit or bad return'
            assert uc.reg_read(UC_ARM_REG_SP)==0x03007e00
            assert [uc.reg_read(r) for r in SAVED]==[0x45670000+i for i in range(8)]
            outcomes.append(bytes(uc.mem_read(0x03000000,0x7000)))
        if outcomes[0]!=outcomes[1] or traces[0]!=traces[1]:
            location=next((i for i,(a,b) in enumerate(zip(*outcomes)) if a!=b),None)
            call=next((i for i,(a,b) in enumerate(zip(*traces)) if a!=b),None)
            raise AssertionError('original instruction mismatch, case %d; address %s; call %s; values omitted'%(seed,hex(0x03000000+location) if location is not None else 'none',call))
        changed+=outcomes[0]!=state[:0x7000]
        call_count+=len(traces[0])
    receipt=dict(candidate=args.candidate.as_posix(),source_sha256=hashlib.sha256(code.encode()).hexdigest(),
        compiled_sha256=hashlib.sha256(actual).hexdigest(),cases=args.cases,passed=args.cases,
        state_changing_cases=changed,ordered_helper_calls_compared=call_count,
        original_instructions_executed=True,original_helpers_executed=True,helper_calls_mocked=False,
        compared='IWRAM below stack region, helper arguments/order, callee-saved registers and stack restoration',
        engine='Unicorn ARM/Thumb',private_rom_identity_verified=True,binary_artifacts_written=False,
        installation_authority=False,limitations='Bounded synthetic states, original lookup data. No gameplay or arbitrary malformed-state proof; byte equality and whole-ROM gates still required.')
    args.receipt.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt))


if __name__=='__main__': main()

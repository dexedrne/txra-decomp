#!/usr/bin/env python3
"""Synthetic ARM comparisons against original instructions, entirely in memory.

The private ROM is read only through its ignored link. No ROM, slice, emulator
snapshot or compiled binary is saved by this tool. Lookup data and state are
synthetic. This does not admit a byte-nonmatching replacement.
"""
import argparse
import hashlib
import json
from pathlib import Path
import random
import struct
import sys

from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM
from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R4, UC_ARM_REG_R5,
    UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R10,
    UC_ARM_REG_R11, UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_CPSR)

sys.path[:0] = [str(Path(__file__).resolve().parent),str(Path(__file__).resolve().parents[1]/'recomp')]
import draft
import measure_candidate as mc
import reloc

START, END, RETURN = 0x080181C0, 0x08018854, 0x0F000000
SAVED = [UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,
         UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11]


def word(mem, offset, value, size=4):
    mem[offset:offset+size] = (value & ((1 << (8*size))-1)).to_bytes(size,'little')


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('candidate',type=Path)
    ap.add_argument('receipt',type=Path)
    ap.add_argument('--cases',type=int,default=192)
    args=ap.parse_args()
    p=draft.Program()
    assert hashlib.sha1(p.rom).hexdigest()=='4197339d4add74bb40ed02a8fba5e58096afb487'
    code=args.candidate.read_text()
    actual,_=mc.diagnostic_compile(code,'func_080181C0',START,reloc.symbols(p),'arm')
    assert len(actual)<=END-START
    engines=[]
    table=bytearray(0x10000)
    for i in range(16384):
        x=i&8191
        s=x if x<4096 else 8192-x
        word(table,i*4,-s if i&8192 else s)
    cosine=table[4096*4:]+table[:4096*4]
    for compiled in (False,True):
        uc=Uc(UC_ARCH_ARM,UC_MODE_ARM)
        for base,size in [(0x02000000,0x40000),(0x03000000,0x8000),(0x08000000,0x400000)]:
            uc.mem_map(base,size)
        uc.mem_write(0x08000000,p.rom)
        if compiled:
            uc.mem_write(START,actual)
        uc.mem_write(0x083D2280,bytes(table))
        uc.mem_write(0x083C2280,bytes(cosine))
        uc.mem_write(0x080202E4,struct.pack('<8I',*[1<<i for i in range(8)]))
        uc.mem_write(0x08020B04,struct.pack('<8i',64,96,96,144,128,192,160,240))
        engines.append(uc)
    rng=random.Random(111203)
    changed=collisions=0
    for case in range(args.cases):
        state=bytearray(0x8000)
        for i in range(8):
            a=0x1e60+i*100
            active=0 if case%8==0 else int(i==0) if case%8==1 else int(rng.randrange(4)!=0)
            word(state,a,active,2)
            word(state,a+2,rng.randrange(4),2)
            word(state,a+4,i*12 if case%3==0 else rng.randrange(-1500,1501))
            word(state,a+12,i*8 if case%3==0 else rng.randrange(-1500,1501))
            word(state,a+32,rng.randrange(-32768,32768))
            word(state,a+40,rng.randrange(-1500,1501))
            for off in (58,60,62): word(state,a+off,rng.randrange(65536),2)
        for i in range(4): word(state,0x5f90+i*4,rng.randrange(128) if case&1 else 0)
        word(state,0x21cc,case%2,2)
        outcomes=[]
        for uc in engines:
            uc.mem_write(0x03000000,bytes(state))
            uc.reg_write(UC_ARM_REG_CPSR,0x1f)
            for i,reg in enumerate(SAVED): uc.reg_write(reg,0x45670000+i)
            uc.reg_write(UC_ARM_REG_SP,0x03007e00)
            uc.reg_write(UC_ARM_REG_LR,RETURN)
            uc.emu_start(START,RETURN,count=200000)
            assert uc.reg_read(UC_ARM_REG_PC)==RETURN, 'instruction limit or bad return'
            assert uc.reg_read(UC_ARM_REG_SP)==0x03007e00
            assert [uc.reg_read(r) for r in SAVED]==[0x45670000+i for i in range(8)]
            outcomes.append((uc.reg_read(UC_ARM_REG_R0),bytes(uc.mem_read(0x03000000,0x7000))))
        if outcomes[0]!=outcomes[1]:
            left,right=outcomes[0][1],outcomes[1][1]
            location=next((i for i,(a,b) in enumerate(zip(left,right)) if a!=b),None)
            raise AssertionError('original instruction mismatch in case %d at %s; values omitted'%(case,hex(0x03000000+location) if location is not None else 'return'))
        changed+=outcomes[0][1]!=bytes(state[:0x7000])
        collisions+=outcomes[0][0]!=0
    receipt=dict(candidate=args.candidate.as_posix(),source_sha256=hashlib.sha256(code.encode()).hexdigest(),
        compiled_sha256=hashlib.sha256(actual).hexdigest(),cases=args.cases,passed=args.cases,
        state_changing_cases=changed,nonzero_return_cases=collisions,original_instructions_executed=True,
        engine='Unicorn ARM',lookup_data='synthetic signed triangular wave, synthetic dimensions and masks',
        compared='return, IWRAM below stack region, all callee-saved registers and stack restoration',
        private_rom_identity_verified=True,binary_artifacts_written=False,installation_authority=False,
        limitations='Synthetic bounded state only; no gameplay or arbitrary malformed-state claim. Exact bytes and whole-ROM gates still required.')
    args.receipt.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt))


if __name__=='__main__': main()

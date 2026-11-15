#!/usr/bin/env python3
"""Check the recovered streaming opening against private original Thumb code.

This is an explicitly partial source recovery, never an installable function.
Original execution stops at the first geometry branch, 080029F0. The complete
owner continues through 0800417E, with its last pools ending at 0800418C.
"""
import argparse
import ctypes
import hashlib
import json
from pathlib import Path
import random
import struct
import subprocess
import tempfile
import unicorn
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_THUMB, UC_HOOK_CODE, UC_PROT_READ, UC_PROT_EXEC
from unicorn.arm_const import UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R6, UC_ARM_REG_R10, UC_ARM_REG_CPSR

SOURCE=Path('docs/near-misses/breadth-1112b/streaming-window.c')


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('receipt',type=Path)
    args=ap.parse_args()
    rom=Path('baserom.gba').read_bytes()
    assert hashlib.sha1(rom).hexdigest()=='4197339d4add74bb40ed02a8fba5e58096afb487'
    uc=Uc(UC_ARCH_ARM,UC_MODE_THUMB)
    uc.mem_map(0x02000000,0x40000);uc.mem_map(0x03000000,0x8000)
    uc.mem_map(0x08000000,len(rom));uc.mem_write(0x08000000,rom)
    uc.mem_protect(0x08000000,len(rom),UC_PROT_READ|UC_PROT_EXEC)
    visited=set()
    uc.hook_add(UC_HOOK_CODE,lambda u,a,n,unused:visited.add(a))
    rng=random.Random(2854)
    point_size,quad_size=32*24*28,32*24*56
    cases=wraps=reverse_cases=0
    with tempfile.TemporaryDirectory(prefix='streaming-window-',dir='build') as td:
        libpath=Path(td)/'window.so'
        subprocess.run(['cc','-shared','-fPIC','-O2','-Wall','-Wextra','-Werror','-std=c11',
                        str(SOURCE),'-o',str(libpath)],check=True,capture_output=True,text=True)
        lib=ctypes.CDLL(str(libpath.resolve()))
        lib.recover_streaming_window.argtypes=[ctypes.c_int32]*4+[ctypes.c_void_p]*3
        lib.recover_streaming_window.restype=None
        for case in range(1024):
            count=(32,33,64,127,512,1024)[case%6]
            position=case%count if case<64 else rng.randrange(count)
            reverse=(0,1,-1,2)[case%4]
            ring=case%32
            points=bytes(rng.randrange(256) for _ in range(point_size)) if case==0 else points
            quads=bytes(rng.randrange(256) for _ in range(quad_size)) if case==0 else quads
            uc.mem_write(0x02014000,points);uc.mem_write(0x02033B70,quads)
            for address,value in [(0x03002334,reverse),(0x03005F50,position),(0x03002E4C,count),(0x030001B8,ring)]:
                uc.mem_write(address,struct.pack('<i',value))
            uc.reg_write(UC_ARM_REG_CPSR,0x3F);uc.reg_write(UC_ARM_REG_SP,0x03007F00)
            uc.reg_write(UC_ARM_REG_LR,0x0203FFF1)
            uc.emu_start(0x08002855,0x080029F0,count=2000)
            assert uc.reg_read(UC_ARM_REG_PC)==0x080029F0,'opening did not reach geometry branch'
            sp=uc.reg_read(UC_ARM_REG_SP)
            assert sp==0x03007F00-32-268,'original frame shape changed'
            word=lambda off:struct.unpack('<i',uc.mem_read(sp+off,4))[0]
            slot=(uc.reg_read(UC_ARM_REG_R6)-0x02014000)//(24*28)
            expected=(word(12),word(16),word(20),ctypes.c_int32(uc.reg_read(UC_ARM_REG_R10)).value,word(8),slot)
            cp=ctypes.create_string_buffer(points,point_size);cq=ctypes.create_string_buffer(quads,quad_size)
            window=(ctypes.c_int32*6)()
            lib.recover_streaming_window(reverse,position,count,ring,cp,cq,window)
            actual=tuple(window[:5])+(window[5]&31,)
            assert actual==expected,'window differs in case %d'%case
            assert cp.raw==bytes(uc.mem_read(0x02014000,point_size)),'point clear differs'
            assert cq.raw==bytes(uc.mem_read(0x02033B70,quad_size)),'quad clear differs'
            cases+=1;wraps+=int(position+28>=count if not reverse else position==0);reverse_cases+=int(reverse!=0)
    r=dict(cases=cases,passed=cases,reverse_cases=reverse_cases,current_wrap_cases=wraps,
           original_instruction_addresses_visited=len(visited),original_instructions_executed=True,
           original_memory_readonly=True,unicorn_version=unicorn.__version__,source=str(SOURCE),
           source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
           tested_start='08002854',tested_end_exclusive='080029F0',complete_owner_end='0800418C',
           source_is_partial=True,installed=False,installation_authority=False,
           limitations='Only window selection and 24-record clears are checked. Geometry generation, continuation and complete-byte equality remain unfinished.')
    args.receipt.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))


if __name__=='__main__':main()

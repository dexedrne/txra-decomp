#!/usr/bin/env python3
"""Compare a complete contact C hypothesis with private original ARM execution.

The ROM is read through the ignored link and held in memory only. Inputs are
synthetic bounded states; no ROM bytes, table contents or extracted binaries
are written. This checker has no replacement-installation authority.
"""
import argparse
import ctypes
import hashlib
import json
from pathlib import Path
import random
import struct
import subprocess
import sys
import tempfile
import unicorn

sys.path[:0] = [str(Path(__file__).resolve().parent), str(Path(__file__).resolve().parents[1]/'recomp')]
import draft
from check_contact1112 import HARNESS, adjusted
from unicorn import Uc, UC_ARCH_ARM, UC_MODE_ARM, UC_HOOK_CODE, UC_PROT_READ, UC_PROT_EXEC
from unicorn.arm_const import UC_ARM_REG_SP, UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_CPSR

WRAPPER = r'''
int run_contact(unsigned char *cars, unsigned char *points, int *known, short flag) {
    int result;
    memcpy(g_03001E60,cars,sizeof(g_03001E60));
    memcpy(g_030057A0,points,sizeof(g_030057A0));
    memcpy(g_03005F90,known,sizeof(g_03005F90));
    g_030021CC=flag;
    result=candidate_contact();
    memcpy(cars,g_03001E60,sizeof(g_03001E60));
    memcpy(points,g_030057A0,sizeof(g_030057A0));
    memcpy(known,g_03005F90,sizeof(g_03005F90));
    return result;
}
'''


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('candidate', type=Path)
    ap.add_argument('receipt', type=Path)
    ap.add_argument('--cases', type=int, default=384)
    args = ap.parse_args()
    rom = Path('baserom.gba').read_bytes()
    assert hashlib.sha1(rom).hexdigest() == '4197339d4add74bb40ed02a8fba5e58096afb487'
    code = args.candidate.read_text()
    negative = code.replace('s1 = g_083D2280[a];', 's1 = (u16)g_083D2280[a];')
    assert negative != code, 'signed coefficient load is required for the negative control'
    source = draft.TYPEDEFS+'\n#include "types.h"\n'+HARNESS+adjusted(code, 'candidate_contact')+WRAPPER
    source += adjusted(negative, 'narrowed_contact')
    source += WRAPPER.replace('run_contact', 'run_narrowed').replace('candidate_contact', 'narrowed_contact')
    visited = set()
    uc = Uc(UC_ARCH_ARM, UC_MODE_ARM)
    uc.mem_map(0x02000000, 0x40000)
    uc.mem_map(0x03000000, 0x8000)
    uc.mem_map(0x08000000, len(rom))
    uc.mem_write(0x08000000, rom)
    uc.mem_protect(0x08000000, len(rom), UC_PROT_READ|UC_PROT_EXEC)
    uc.hook_add(UC_HOOK_CODE, lambda u, a, n, unused: visited.add(a))
    rng = random.Random(1112)
    results = dict(cases=args.cases, passed=0, state_changing_cases=0, contact_results=0,
                   cache_preserved_cases=0, cache_cleared_cases=0, rejected_narrowing_control_cases=0)
    with tempfile.TemporaryDirectory(prefix='contact-reference-', dir='build') as td:
        folder = Path(td)
        (folder/'candidate.c').write_text(source)
        subprocess.run(['cc', '-shared', '-fPIC', '-O1', '-std=c11', '-fwrapv', '-fno-strict-aliasing',
                        '-Isrc', str(folder/'candidate.c'), '-o', str(folder/'candidate.so')],
                       check=True, capture_output=True, text=True)
        lib = ctypes.CDLL(str((folder/'candidate.so').resolve()))
        lib.run_contact.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_short]
        lib.run_contact.restype = ctypes.c_int
        lib.run_narrowed.argtypes = lib.run_contact.argtypes
        lib.run_narrowed.restype = ctypes.c_int
        for name, address, count in [('g_083D2280',0x083D2280,16384),('g_083C2280',0x083C2280,16384),
                                     ('g_080202E4',0x080202E4,8),('g_08020B04',0x08020B04,8),('g_08020B08',0x08020B08,8)]:
            array = (ctypes.c_int32*count).in_dll(lib,name)
            ctypes.memmove(array,rom[address-0x08000000:address-0x08000000+count*4],count*4)
        for case in range(args.cases):
            cars = bytearray(800)
            points = bytes(rng.randrange(256) for _ in range(72))
            for i in range(8):
                a=i*100
                active = 0 if case%12==0 else int(i==0) if case%12==1 else int(rng.randrange(4)!=0)
                struct.pack_into('<hh',cars,a,active,rng.randrange(4))
                x,z = ((i*12,i*8) if case%3==0 else (rng.randrange(-1500,1501),rng.randrange(-1500,1501)))
                struct.pack_into('<i',cars,a+4,x)
                struct.pack_into('<i',cars,a+12,z)
                struct.pack_into('<i',cars,a+32,rng.randrange(-32768,32768))
                struct.pack_into('<i',cars,a+40,rng.randrange(-1500,1501))
                for off in (58,60,62):struct.pack_into('<h',cars,a+off,rng.randrange(-32768,32768))
            known=struct.pack('<4i',*[rng.randrange(128) if case&1 else 0 for _ in range(4)])
            flag=case%2
            uc.mem_write(0x03001E60,bytes(cars));uc.mem_write(0x030057A0,points)
            uc.mem_write(0x03005F90,known);uc.mem_write(0x030021CC,struct.pack('<h',flag))
            uc.reg_write(UC_ARM_REG_CPSR,0x1F)
            uc.reg_write(UC_ARM_REG_SP,0x03007F00);uc.reg_write(UC_ARM_REG_LR,0x0203FFF0)
            uc.emu_start(0x080181C0,0x0203FFF0,count=250000)
            assert uc.reg_read(UC_ARM_REG_PC)==0x0203FFF0,'original did not return within bound'
            expected_result=ctypes.c_int32(uc.reg_read(UC_ARM_REG_R0)).value
            expected=(bytes(uc.mem_read(0x03001E60,800)),bytes(uc.mem_read(0x030057A0,72)),bytes(uc.mem_read(0x03005F90,16)))
            c_cars=ctypes.create_string_buffer(bytes(cars),800)
            c_points=ctypes.create_string_buffer(points,72)
            c_known=ctypes.create_string_buffer(known,16)
            result=lib.run_contact(c_cars,c_points,c_known,flag)
            actual=(c_cars.raw,c_points.raw,c_known.raw)
            if result!=expected_result or actual!=expected:
                parts=[name for name,a,b in zip(('records','points','cache'),expected,actual) if a!=b]
                raise AssertionError('case %d differs: result=%s memory=%s'%(case,result!=expected_result,','.join(parts)))
            n_cars=ctypes.create_string_buffer(bytes(cars),800)
            n_points=ctypes.create_string_buffer(points,72)
            n_known=ctypes.create_string_buffer(known,16)
            bad=lib.run_narrowed(n_cars,n_points,n_known,flag)
            results['rejected_narrowing_control_cases']+=int(bad!=expected_result or (n_cars.raw,n_points.raw,n_known.raw)!=expected)
            results['passed']+=1
            results['state_changing_cases']+=int(expected!=(bytes(cars),points,known))
            results['contact_results']+=int(result!=0)
            results['cache_preserved_cases']+=int(expected[2]==known)
            results['cache_cleared_cases']+=int(known!=bytes(16) and expected[2]==bytes(16))
    assert results['rejected_narrowing_control_cases']>0, 'negative control did not exercise signed coefficient loss'
    results.update(candidate=str(args.candidate),candidate_sha256=hashlib.sha256(code.encode()).hexdigest(),unicorn_version=unicorn.__version__,
                   harness_sha256=hashlib.sha256(source.encode()).hexdigest(),
                   original_instructions_executed=True,original_instruction_addresses_visited=len(visited),
                   original_memory_readonly=True,installation_authority=False,
                   method='Original ARM instructions in Unicorn versus host-compiled complete C; actual private lookup tables; bounded synthetic RAM.',
                   limitations='No gameplay, arbitrary malformed-state or byte-equality claim. Original bytes and tables remain private and memory-only.')
    args.receipt.write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results))


if __name__=='__main__':main()

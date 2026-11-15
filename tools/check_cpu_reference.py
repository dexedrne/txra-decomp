import ctypes, random,struct
from unicorn import Uc,UC_ARCH_ARM,UC_MODE_ARM,UC_MODE_THUMB,UC_PROT_ALL
from unicorn.arm_const import *
random.seed(42)
lib=ctypes.CDLL('./build/cpu-reference.so');lib.execute.argtypes=[ctypes.POINTER(ctypes.c_uint32),ctypes.POINTER(ctypes.c_uint32),ctypes.c_uint32,ctypes.c_int]
uc=Uc(UC_ARCH_ARM,UC_MODE_ARM);uc.mem_map(0x2000000,0x40000)
registers=[UC_ARM_REG_R0,UC_ARM_REG_R1,UC_ARM_REG_R2,UC_ARM_REG_R3,UC_ARM_REG_R4,UC_ARM_REG_R5,UC_ARM_REG_R6,UC_ARM_REG_R7,UC_ARM_REG_R8,UC_ARM_REG_R9,UC_ARM_REG_R10,UC_ARM_REG_R11,UC_ARM_REG_R12,UC_ARM_REG_SP,UC_ARM_REG_LR,UC_ARM_REG_PC]
total=0
for t in (True,False):
 count=0
 for i in range(20000):
  r=[random.getrandbits(32) for _ in range(15)]+[0x2000000];p=random.randrange(16)<<28|0x1f|(32 if t else 0)
  if t:
   op=random.choice([random.randrange(0x4000),0x4000|random.randrange(0x400),0x4400|random.randrange(0x400),0xa000|random.randrange(0x1000)])
   if op&0xff00==0x4700:continue
  else:
   op=0xe0000000|random.getrandbits(26)
   if op&15==15 or ((op>>16)&15)==15 or ((op>>8)&15)==15 or (op>>12)&15==15 or (op&0xc000000)!=0 or op&0x90==0x90 or op&0x01900000==0x01000000:continue
  cr=(ctypes.c_uint32*16)(*r);cp=ctypes.c_uint32(p);lib.execute(cr,ctypes.byref(cp),op,t)
  uc.reg_write(UC_ARM_REG_CPSR,p)
  for rr,v in zip(registers,r):uc.reg_write(rr,v)
  uc.mem_write(0x2000000,struct.pack('<H' if t else '<I',op))
  uc.ctl_remove_cache(0x2000000,0x2000008)
  try:uc.emu_start(0x2000000|int(t),0,count=1)
  except Exception:continue
  ur=[uc.reg_read(rr) for rr in registers];up=uc.reg_read(UC_ARM_REG_CPSR)
  count+=1
  if list(cr)!=ur or cp.value&0xf000003f!=up&0xf000003f:
   print('MISMATCH',t,hex(op),'input',list(map(hex,r)),hex(p));print('ours',list(map(hex,cr)),hex(cp.value));print('ref ',list(map(hex,ur)),hex(up));raise SystemExit(1)
 else:print(f'{count} {"THUMB" if t else "ARM"} arithmetic vectors passed');total+=count
print(f'{total} reference comparisons passed')

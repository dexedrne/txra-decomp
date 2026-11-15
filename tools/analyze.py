#!/usr/bin/env python3
"""Conservative ARMv4T recursive disassembly; no extracted data is written."""
import json, struct, hashlib, collections, argparse, zlib
from pathlib import Path
from capstone import *
from capstone.arm import *
cfg=json.loads(Path('tools/rom.cfg').read_text()); b=Path('baserom.gba').read_bytes(); base=cfg['base']; limit=cfg['scan_end']
assert len(b)==cfg['size'] and hashlib.sha1(b).hexdigest()==cfg['sha1'], 'wrong ROM'
eng={m:Cs(CS_ARCH_ARM,CS_MODE_ARM if m=='arm' else CS_MODE_THUMB) for m in ('arm','thumb')}
for e in eng.values(): e.detail=True
parser=argparse.ArgumentParser()
parser.add_argument('--coverage', nargs='*', default=[])
args=parser.parse_args()
observed=[]
for path in args.coverage:
 trace=json.loads(Path(path).read_text())
 assert not trace['overflow'], 'incomplete coverage'
 assert trace.get('rom_crc32') == f'{zlib.crc32(b):08x}', 'coverage ROM fingerprint mismatch'
 for pc,thumb in trace['pcs']:
  if base<=pc<base+len(b): observed.append((pc-base,'thumb' if thumb else 'arm'))
  else:
   for copy in cfg['copies']:
    if copy['run']<=pc<copy['run']+copy['size']:
     observed.append((copy['load']-base+pc-copy['run'],'thumb' if thumb else 'arm'))
# A pointer alone is not code proof: require a bounded ARMv4T leaf ending in
# an explicit return. Prologues and direct calls remain separate evidence.
def leaf(o,m):
 for _ in range(96):
  if not 0xc0<=o<len(b)-4:return False
  ins=next(eng[m].disasm(b[o:o+4],base+o,count=1),None)
  if not ins or (m=='thumb' and ins.size!=2):return False
  if ins.id==ARM_INS_BX:return ins.operands[0].reg==ARM_REG_LR
  if ins.id==ARM_INS_POP:return any(op.type==ARM_OP_REG and op.reg==ARM_REG_PC for op in ins.operands)
  if ins.group(CS_GRP_JUMP) or ins.group(CS_GRP_CALL):return False
  if ins.mnemonic.startswith(('movw','movt','udf','svc','bkpt','str','stm')):return False
  o+=ins.size
 return False
jump_tables={}; code={}; occupied={}; literals=set(); funcs={}; edges=[]; indirect=[]; todo=collections.deque()
# Reviewed Thumb long branches: BL used as an intra-function jump (lr already
# saved, link value never used). They neither create an entry nor fall through.
far_jumps={j['source']-base:j['target']-base for j in cfg.get('far_jumps',[])}
supplement=json.loads(Path('recomp/observed.json').read_text())['functions']
confirmed_interiors=set()
for f in supplement:
 for a,z in f['spans']:confirmed_interiors.update(range(int(a,16)-base+4,int(z,16)-base,4))
def seed(o,m,why):
 if o in confirmed_interiors:
  todo.append((o,m));return
 if 0<=o<limit and o%(4 if m=='arm' else 2)==0:
  funcs.setdefault(o,{'mode':m,'evidence':why}); todo.append((o,m))
for o,m in cfg['seeds']: seed(o,m,'explicit entry/runtime seed')
for entry in cfg.get('reviewed_seeds', []):
 seed(entry['offset'],entry['mode'],entry['evidence'])
for f in supplement: seed(int(f['start'],16)-base,f['mode'],'executed IRQ epilogue; reviewed runtime coverage')
for o in (0x18854,0x18e80,0x18e88): seed(o,'arm','BX PC interworking veneer')
for copy in cfg.get('copies',[]):
 seed(copy['load']-base,copy['mode'],'DMA-copied IWRAM routine')
for o in range(0x18de0,0x18e1c,4): seed(o,'thumb','libgcc register-call veneer')
# Pointer candidates require a plausible save-register prologue; these remain candidates.
for p in range(0xc0,len(b)-3,4):
 v=struct.unpack_from('<I',b,p)[0]; o=(v&~1)-base
 if 0xc0<=o<limit:
  if v&1 and struct.unpack_from('<H',b,o)[0]&0xfe00==0xb400: seed(o,'thumb',f'ROM pointer at {base+p:08X} + PUSH prologue')
  elif not v&3 and struct.unpack_from('<I',b,o)[0]&0xffff0000==0xe92d0000: seed(o,'arm',f'ROM pointer at {base+p:08X} + STMDB prologue')
  elif (v&1 or not v&3) and leaf(o,'thumb' if v&1 else 'arm'):
   seed(o,'thumb' if v&1 else 'arm',f'ROM pointer at {base+p:08X} + bounded return leaf candidate')
# Consecutive Thumb pointers are table evidence even for leaf functions.
pointer_run=[]
for p in range(0xc0,len(b),4):
 v=struct.unpack_from('<I',b,p)[0]; target=(v&~1)-base
 if v&1 and 0x2000<=target<0x18e8c:
  pointer_run.append((p,target))
 else:
  if len(pointer_run)>=2:
   for where,target in pointer_run: seed(target,'thumb',f'consecutive pointer table at {base+where:08X}')
  pointer_run=[]
# Unreferenced functions exist after computed dispatches. Prologue-only discovery
# is lower confidence than a direct call and is explicitly marked in the report.
for o in range(0x2000,0x18a54,2):
 if struct.unpack_from('<H',b,o)[0]&0xff00==0xb500:
  seed(o,'thumb','PUSH with LR candidate (medium confidence)')
for o,m in cfg.get('dynamic_seeds',[]): seed(o,m,'executed guest PC (coverage)')
pending_observed=collections.deque(sorted(set(observed)))
# Drain the entire static closure first. Interleaving arbitrary observed PCs
# would split basic blocks and erase the local constants used to find pools.
while todo or pending_observed:
 if not todo:
  while pending_observed and not todo:
   at,mode=pending_observed.popleft()
   if at not in code: seed(at,mode,'executed guest PC (coverage)')
  if not todo:break
 o,m=todo.popleft(); regs={}
 for _ in range(30000):
  if o in code or o in occupied or o in literals or not 0<=o<limit: break
  ins=next(eng[m].disasm(b[o:o+4],base+o,count=1),None)
  if not ins or (m=='thumb' and ins.size==4 and ins.id!=ARM_INS_BL): break
  if m=='arm' and ins.mnemonic.startswith(('movw','movt')): break
  if any(x in occupied or x in literals for x in range(o,o+ins.size)): break
  code[o]=(m,ins)
  for x in range(o,o+ins.size): occupied[x]=o
  ops=ins.operands; loaded=None
  if ins.id==ARM_INS_LDR and len(ops)>1 and ops[1].type==ARM_OP_MEM and ops[1].mem.base==ARM_REG_PC:
   p=((ins.address+(8 if m=='arm' else 4)) & (~3 if m=='thumb' else ~0))+ops[1].mem.disp-base
   if 0<=p<len(b)-3:
    literals.update(range(p,p+4)); loaded=(ops[0].reg,struct.unpack_from('<I',b,p)[0])
  if ins.id in (ARM_INS_B,ARM_INS_BL) and ops and ops[0].type==ARM_OP_IMM:
   target=ops[0].imm-base; edges.append([o,target,'far-jump' if o in far_jumps else ins.mnemonic]); todo.append((target,m))
   if o in far_jumps:
    assert ins.id==ARM_INS_BL and m=='thumb' and far_jumps[o]==target, 'reviewed far jump changed'
    break
   if ins.id==ARM_INS_BL: funcs.setdefault(target,{'mode':m,'evidence':'direct BL'})
   if ins.id==ARM_INS_B and ins.cc==ARM_CC_AL: break
  if ins.id==ARM_INS_BX:
   previous=code.get(o-4)
   if m=='arm' and previous and previous[1].id==ARM_INS_MOV and previous[1].operands[0].reg==ARM_REG_LR and previous[1].operands[1].reg==ARM_REG_PC:
    todo.append((o+ins.size,m))
   reg=ops[0].reg; v=(ins.address+4 if reg==ARM_REG_PC and m=='thumb' else regs.get(reg))
   if v is not None: seed((v&~1)-base,'thumb' if v&1 else 'arm','literal load then BX')
   elif reg!=ARM_REG_LR: indirect.append(o)
   if ins.cc==ARM_CC_AL: break
  if ins.id in (ARM_INS_POP,ARM_INS_LDM) and any(op.type==ARM_OP_REG and op.reg==ARM_REG_PC for op in ops): break
  if m=='thumb' and ins.id==ARM_INS_MOV and ops[0].reg==ARM_REG_PC:
   # GCC bounded switch: CMP; BLS; B default; LSL #2; LDR pool;
   # ADD table base; LDR target; MOV PC. Entries are EVEN Thumb PCs.
   load=next((code[p][1] for p in range(o-6,o-12,-2) if p in code and code[p][1].id==ARM_INS_LDR and len(code[p][1].operands)>1 and code[p][1].operands[1].type==ARM_OP_MEM and code[p][1].operands[1].mem.base==ARM_REG_PC),None)
   bound=next((code[p][1].operands[1].imm for p in range(o-8,max(o-36,0),-2) if p in code and code[p][1].id==ARM_INS_CMP and code[p][1].operands[1].type==ARM_OP_IMM),None)
   if load is not None and bound is not None and 0<=bound<512:
    pool=((load.address+4)&~3)+load.operands[1].mem.disp-base
    table=struct.unpack_from('<I',b,pool)[0]-base
    if 0<=table<len(b)-(bound+1)*4:
     targets=[struct.unpack_from('<I',b,table+j*4)[0]-base for j in range(bound+1)]
     if all(0x2000<=t<0x18e8c and t%2==0 for t in targets):
      jump_tables[o]={'table':table,'targets':targets,'bound':bound,'mode':'thumb','confidence':'high; bounded GCC switch pattern'}
      literals.update(range(table,table+4*(bound+1)))
      for t in targets: todo.append((t,'thumb')); edges.append([o,t,'switch'])
  if ins.id in (ARM_INS_MOV,ARM_INS_LDM) and ops and ops[0].type==ARM_OP_REG and ops[0].reg==ARM_REG_PC: break
  try:
   for register in ins.regs_access()[1]: regs.pop(register,None)
  except Exception: regs={}
  if loaded is not None: regs[loaded[0]]=loaded[1]
  if ins.id==ARM_INS_BL: regs={}
  o+=ins.size
# Discard false candidate paths which trespassed on discovered literal words.
for o in list(code):
 if any(x in literals for x in range(o,o+code[o][1].size)): del code[o]
# Reviewed interior labels: far goto targets (Thumb emits a goto beyond 2 KiB as
# BL) inside an installed byte-matched owner. They stay code, but not entries,
# so the owner's extent runs through them.
for label in cfg.get('interior_labels',[]):
 owner=next(x for x in cfg['matches'] if x['name']==label['owner'])
 assert owner['offset']<label['offset']<owner['offset']+owner['size'], 'interior label outside its owner'
 assert label['offset'] in code and code[label['offset']][0]==label['mode'], 'interior label is not code'
 funcs.pop(label['offset'],None)
Path('build').mkdir(exist_ok=True)
report={'functions':{f'{base+o:08X}':v for o,v in sorted(funcs.items()) if o in code},'edges':edges,'indirect':[f'{base+o:08X}' for o in sorted(set(indirect))], 'instructions':len(code),'code_bytes':sum(i.size for m,i in code.values())}
Path('build/analysis.json').write_text(json.dumps(report,indent=2)+'\n')
# Always preserve every uncovered byte with incbin. Named boundaries drive the build.
labels={o:f'func_{base+o:08X}' for o in funcs if o in code}
for o,(m,i) in code.items():
 if i.id in (ARM_INS_B,ARM_INS_BL) and i.operands[0].type==ARM_OP_IMM:
  t=i.operands[0].imm-base
  if t in code: labels.setdefault(t,f'loc_{base+t:08X}')
segments=[]
for start,end,name in cfg['regions']:
 lines=['@ Generated by tools/analyze.py. Data stays in the private base ROM.','.syntax unified', '.section .text',f'.global region_{name}',f'region_{name}:']; o=start; mode=None
 while o<end:
  match=next((x for x in cfg.get('matches',[]) if x['offset']==o),None)
  if match:
   lines.extend([match['name']+':', f'    .incbin "build/leaves/{match["name"]}.bin"'])
   o+=match['size']; continue
  if o in code and o+code[o][1].size<=end:
   m,i=code[o]
   if mode!=m: lines.append('.arm' if m=='arm' else '.thumb'); mode=m
   if o in labels: lines.append(labels[o]+':')
   op=i.op_str
   if i.id in (ARM_INS_B,ARM_INS_BL) and i.operands[0].type==ARM_OP_IMM:
    t=i.operands[0].imm-base
    # Absolute address expression relative to the current section position.
    op=labels.get(t,f'. + ({t-o})')
   if m=='arm': op=op.replace('apsr','cpsr')
   if m=='thumb' and i.mnemonic=='add' and ', sp, ' in op and '#' not in op: op=op.split(',')[0]+', sp'
   lines.append(f'    {i.mnemonic} {op} @ {base+o:08X}')
   o+=i.size
  else:
   n=o+1
   while n<end and n not in code and n not in labels: n+=1
   lines.extend([f'data_{base+o:08X}:',f'    .incbin "baserom.gba", 0x{o:X}, 0x{n-o:X}']); o=n
 path=f'asm/{name}.s'; Path(path).write_text('\n'.join(lines)+'\n'); segments.append(path)
Path('asm/rom.s').write_text('.global _start\n_start:\n'+''.join(f'.include "{s}"\n' for s in segments))
print(f'{len(code)} instructions, {report["code_bytes"]} bytes, {len(report["functions"])} function candidates')

from inventory import write_inventory
write_inventory(b,cfg,code,funcs,literals,jump_tables)

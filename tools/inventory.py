"""Metadata only: function extents, pointer tables, copied code, I/O sites."""
import json, struct
from pathlib import Path
from capstone.arm import *
def write_inventory(b,cfg,code,funcs,literals,jump_tables):
 base=cfg['base']; root=Path('docs/map'); root.mkdir(parents=True,exist_ok=True)
 def save(name,obj):
  path=root/(name+'.json'); text=json.dumps(obj,indent=2)+'\n'
  if not path.exists() or path.read_text()!=text:path.write_text(text)
 def hx(v): return f'0x{v:08X}'
 def address(o): return hx(base+o)
 # A function extent is the union of locally reachable instruction spans. Calls
 # contribute their fallthrough, not the callee's body. Tail sharing is retained.
 functions=[]
 for o,f in sorted(funcs.items()):
  if o not in code:continue
  work=[o];visited=set()
  far={j['source']-base for j in cfg.get('far_jumps',[])}
  while work:
   p=work.pop()
   if p in visited or p not in code:continue
   if p!=o and p in funcs:continue
   visited.add(p);m,i=code[p];n=p+i.size;ops=i.operands
   if i.id==ARM_INS_B:
    if ops[0].type==ARM_OP_IMM: work.append(ops[0].imm-base)
    if i.cc!=ARM_CC_AL:work.append(n)
   elif i.id==ARM_INS_BL and p in far:work.append(ops[0].imm-base)
   elif i.id==ARM_INS_BX:
    prev=code.get(p-4)
    if i.cc!=ARM_CC_AL or (m=='arm' and prev and prev[1].id==ARM_INS_MOV and prev[1].operands[0].reg==ARM_REG_LR and prev[1].operands[1].reg==ARM_REG_PC):work.append(n)
   elif i.id in (ARM_INS_POP,ARM_INS_LDM) and any(x.type==ARM_OP_REG and x.reg==ARM_REG_PC for x in ops):pass
   elif i.id==ARM_INS_MOV and ops[0].reg==ARM_REG_PC:
    work.extend(jump_tables.get(p,{}).get("targets",[]))
   else:work.append(n)
  spans=[]
  for p in sorted(visited):
   end=p+code[p][1].size
   if spans and spans[-1][1]==p:spans[-1][1]=end
   else:spans.append([p,end])
  end=max(p+code[p][1].size for p in visited)
  runs=[{'start':hx(c['run']+o-(c['load']-base)),'copy_load':hx(c['load'])} for c in cfg.get('copies',[]) if c['load']-base<=o<c['load']-base+c['size']]
  evidence=f['evidence'];confidence='medium' if 'candidate' in evidence or 'prologue' in evidence else 'high'
  functions.append({'start':address(o),'end':address(end),'end_exclusive':True,'mode':f['mode'],'confidence':confidence,'evidence':evidence,'extent_kind':'reachable instructions; excludes pools; may share tails','spans':[[address(a),address(z)] for a,z in spans],'runtime_aliases':runs})
  reviewed=next((r for r in cfg.get('reviewed_seeds',[]) if r['offset']==o),None)
  if reviewed:
   functions[-1]['suggested_name']=reviewed['name']
   functions[-1]['execution_verified']=False
 save('functions',{'complete':False,'caveat':'Static candidate inventory. Computed transfers and leaf entries can remain unresolved. Ends are reachable extents, not linker symbol sizes.','functions':functions})
 # Full ROM partition, no binary bytes. The decoder's confidence does not prove reachability.
 splits=[]
 for o in range(len(b)):
  if o in code:
   m,i=code[o];kind=m
  elif o in literals: kind='literal'
  else:kind='unresolved'
  # continuation bytes inherit the instruction kind
  if splits and o<splits[-1]['_instruction_end']:continue
  n=o+(code[o][1].size if o in code else 1)
  if splits and splits[-1]['kind']==kind and splits[-1]['end']==address(o):
   splits[-1]['end']=address(n);splits[-1]['_instruction_end']=n
  else:splits.append({'start':address(o),'end':address(n),'kind':kind,'_instruction_end':n})
 for s in splits:s.pop('_instruction_end')
 save('splits',{'end_exclusive':True,'regions':splits})
 ram_targets={}
 for c in cfg.get('copies',[]):
  for o in code:
   if c['load']-base<=o<c['load']-base+c['size']:
    ram_targets[c['run']+o-(c['load']-base)]=o
 pointers=[]
 for p in range(0xc0,len(b)-3,4):
  v=struct.unpack_from('<I',b,p)[0];t=(v&~1)-base
  if (v&~1) in ram_targets:t=ram_targets[v&~1]
  if t in code and ((v&1 and code[t][0]=='thumb') or (not v&3 and code[t][0]=='arm')):
   pointers.append({'source':address(p),'target':address(t),'mode':code[t][0],'runtime_target':hx(v),'confidence':'candidate; ROM word points to decoded instruction'})
 tables=[];group=[]
 for p in pointers:
  if group and int(p['source'],16)!=int(group[-1]['source'],16)+4:
   if len(group)>1:tables.append({'start':group[0]['source'],'end':hx(int(group[-1]['source'],16)+4),'kind':'function-pointer or jump-table candidate','entries':group})
   group=[]
  group.append(p)
 if len(group)>1:tables.append({'start':group[0]['source'],'end':hx(int(group[-1]['source'],16)+4),'kind':'function-pointer or jump-table candidate','entries':group})
 save('pointers',{'switches':[{'source':address(o),'start':address(t['table']),'end':address(t['table']+len(t['targets'])*4),'targets':[address(x) for x in t['targets']],'mode':t['mode'],'confidence':t['confidence']} for o,t in sorted(jump_tables.items())],'tables':tables,'references':pointers})
 # Local constant propagation. Reset at every incoming branch and after control
 # transfer. Unknown writes kill constants; unresolved memory sites remain listed.
 targets={i.operands[0].imm-base for m,i in code.values() if i.id in (ARM_INS_B,ARM_INS_BL) and i.operands[0].type==ARM_OP_IMM}
 constants={}; loaded_from={}; call_sites=[]; io=[]; unresolved=[]; transfers=[];dma={};ramrefs=[]
 def val(op):
  if op.type==ARM_OP_IMM:return op.imm
  if op.type!=ARM_OP_REG:return None
  v=constants.get(op.reg)
  if v is None:return None
  if op.shift.type==ARM_SFT_LSL:v=(v<<op.shift.value)&0xffffffff
  elif op.shift.type==ARM_SFT_LSR:v=v>>op.shift.value
  elif op.shift.type==ARM_SFT_ASR:v=((v if v<0x80000000 else v-0x100000000)>>op.shift.value)&0xffffffff
  elif op.shift.type:return None
  return v
 for o,(m,i) in sorted(code.items()):
  if o in targets or o in funcs:constants={};loaded_from={}
  constants[ARM_REG_PC]=i.address+(8 if m=='arm' else 4)
  ops=i.operands;result=None;new_origin=None;dest=ops[0].reg if ops and ops[0].type==ARM_OP_REG else None
  for op in ops:
   if op.type!=ARM_OP_MEM:continue
   mem=op.mem;v=constants.get(mem.base)
   if mem.base==ARM_REG_PC and m=='thumb' and v is not None:v&=~3
   idx=constants.get(mem.index) if mem.index else 0
   if v is not None and idx is not None:
    addr=(v+(idx<<mem.lshift)+mem.disp)&0xffffffff
    action='write' if i.mnemonic.startswith(('str','stm')) else 'read'
    value=val(ops[0]) if action=='write' else None
    if action=='read' and dest is not None:new_origin=(dest,addr)
    rec={'instruction':address(o),'address':hx(addr),'access':action,'mnemonic':i.mnemonic,'value':hx(value) if value is not None else None,'confidence':'local constant propagation'}
    if 0x4000000<=addr<0x4000400 or 0xd000000<=addr<0xe000000:io.append(rec)
    if 0x2000000<=addr<0x4000000:ramrefs.append(rec)
    if action=='read' and i.id==ARM_INS_LDR and base<=addr<base+len(b)-3:result=struct.unpack_from('<I',b,addr-base)[0]
   elif mem.base!=ARM_REG_SP:unresolved.append({'instruction':address(o),'mnemonic':i.mnemonic,'base_register':i.reg_name(mem.base)})
  if i.id==ARM_INS_MOV and len(ops)>1:result=val(ops[1])
  if i.id in (ARM_INS_ADD,ARM_INS_SUB,ARM_INS_ORR,ARM_INS_AND,ARM_INS_BIC,ARM_INS_EOR,ARM_INS_MUL):
   a=val(ops[1]) if len(ops)>2 else val(ops[0]); z=val(ops[2]) if len(ops)>2 else val(ops[1])
   if a is not None and z is not None:
    result={ARM_INS_ADD:lambda:a+z,ARM_INS_SUB:lambda:a-z,ARM_INS_ORR:lambda:a|z,ARM_INS_AND:lambda:a&z,ARM_INS_BIC:lambda:a&~z,ARM_INS_EOR:lambda:a^z,ARM_INS_MUL:lambda:a*z}[i.id]()&0xffffffff
  if i.id in (ARM_INS_LSL,ARM_INS_LSR,ARM_INS_ASR) and len(ops)==3:
   a=val(ops[1]);z=val(ops[2])
   if a is not None and z is not None:
    if i.id==ARM_INS_LSL:result=(a<<z)&0xffffffff
    elif i.id==ARM_INS_LSR:result=a>>z
    else:result=((a if a<0x80000000 else a-0x100000000)>>z)&0xffffffff
  if i.id==ARM_INS_BX or (i.id==ARM_INS_MOV and dest==ARM_REG_PC):
   reg=ops[0].reg if i.id==ARM_INS_BX else ops[1].reg;v=constants.get(reg)
   prev=code.get(o-2);ret=reg==ARM_REG_LR or (prev and prev[1].id==ARM_INS_POP and any(x.reg==reg for x in prev[1].operands))
   transfers.append({'source':address(o),'mode':m,'kind':'return' if ret else 'indirect','register':i.reg_name(reg),'target':hx(v) if v is not None else None,'confidence':'bounded switch' if o in jump_tables else ('local constant' if v is not None else ('return pattern' if ret else 'unresolved')),'targets':[address(x) for x in jump_tables.get(o,{}).get('targets',[])],'pointer_slot':hx(loaded_from[reg]) if reg in loaded_from else None})
  if i.id==ARM_INS_BL and ops[0].type==ARM_OP_IMM:
   t=ops[0].imm-base
   if 0x18de0<=t<0x18e1c and t in code:
    reg=code[t][1].operands[0].reg;v=constants.get(reg)
    call_sites.append({'source':address(o),'veneer':address(t),'register':i.reg_name(reg),'target':hx(v) if v is not None else None,'confidence':'local constant' if v is not None else 'unresolved','pointer_slot':hx(loaded_from[reg]) if reg in loaded_from else None})
  try:_,writes=i.regs_access()
  except Exception:writes=[]
  for w in writes:constants.pop(w,None);loaded_from.pop(w,None)
  if new_origin is not None:loaded_from[new_origin[0]]=new_origin[1]
  if dest and result is not None:constants[dest]=result
  if i.id in (ARM_INS_BL,ARM_INS_B,ARM_INS_BX):constants={};loaded_from={}
 # Manually reviewed loop-invariant call slots; verify the ROM-side fact.
 for known in cfg.get('known_indirect_calls',[]):
  assert struct.unpack_from('<I',b,known['pointer_slot']-base)[0]==known['target']
  for call in call_sites:
   if call['source']==hx(known['source']):
    call.update(target=hx(known['target']),pointer_slot=hx(known['pointer_slot']),confidence='high; '+known['evidence'])
 # Cross-reference constant slot writes without claiming dynamic order/coverage.
 for call in call_sites:
  slot=call.get('pointer_slot')
  call['possible_targets_from_writes']=sorted({r['value'] for r in ramrefs if slot and r['address']==slot and r['access']=='write' and r['value'] and (int(r['value'],16)&~1 in ram_targets or ((int(r['value'],16)&~1)-base) in code)})
 for transfer in transfers:
  observed=sorted({call['target'] for call in call_sites if call['veneer']==transfer['source'] and call['target']})
  if observed:
   transfer['targets']=observed;transfer['confidence']='known callsite targets; static coverage not exhaustive'
  if transfer['source']=='0x080001F0':
   transfer['targets']=[hx(struct.unpack_from('<I',b,p)[0]) for p in range(0x18e8c,0x18ec4,4)]
   transfer['confidence']='high; fixed IRQ table, writable code could change dispatch'
 save('indirect',{'complete':False,'transfers':transfers,'veneer_calls':call_sites})
 literal_io=[{'source':address(p),'address':hx(struct.unpack_from('<I',b,p)[0])} for p in sorted(literals) if p%4==0 and p<len(b)-3 and 0x4000000<=struct.unpack_from('<I',b,p)[0]<0x4000400]
 save('hardware',{'literal_candidates':literal_io,'complete':False,'method':'Basic-block local constant propagation; unresolved bases deliberately retained. Width follows mnemonic. Conditional sites are potential accesses.','resolved_io':io,'unresolved_memory':unresolved,'resolved_ram':ramrefs})
 save('copies',{'copies':cfg.get('copies',[]),'caveat':'Transfers include startup IRQ, audio initialization and initializer via 08018E84. Copy ranges overlap and can include mixed code/data tails: preserve order and bytes, do not assume disjoint functions. No EWRAM executable copy proven.'})
 print(f'Inventory: {len(functions)} functions, {len(tables)} pointer-table candidates, {len(io)} resolved I/O sites, {sum(t["kind"]=="indirect" and t["target"] is None and not t.get("targets") for t in transfers)} unresolved indirect sites')

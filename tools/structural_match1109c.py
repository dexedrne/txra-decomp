"""Metadata-only layout and shape comparison; no original instruction data saved."""
import sys,re,json,difflib,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'tools'),str(ROOT/'recomp')]
import draft,reloc,measure_candidate as mc,diffhint
REGIONS={
'080181C0': [('entry and pair selection','080181C0','08018460'),('rotation','08018460','08018528'),('contact updates','08018528','080187DC'),('loop exits and return','080187DC','08018854')],
'08002854': [('entry and stream window','08002854','080029BC'),('bank geometry','080029BC','08002FDE'),('road walls and bridge','08002FDE','08003786'),('scenery continuation and return','08003786','0800418C')],
'0800421C': [('entry and opening overlay','0800421C','080042EC'),('sprite strips and text','080042EC','080047A4'),('gauges','080047A4','08004A88'),('map and flashes','08004A88','08004C96'),('projected effects','08004C96','08004FFA'),('smoke and return','08004FFA','08005238')],
'08016DA8': [('entry and geometry setup','08016DA8','08016EF0'),('subdivision cases','08016EF0','08017308'),('projection','08017308','08017470'),('near visibility and packets','08017470','08017AA8'),('direct path and return','08017AA8','08017E68')],
'080064A4': [('fade and sample update','080064A4','080065C2'),('sequence loop','080065C2','080066E4'),('voice entry and preparation','080066E4','0800677A'),('envelope updates','0800677A','08006D62'),('command loop','08006D62','08006ECC'),('events, note starts and return','08006ECC','08007398')],
}
def listing(data,a,mode):
 out=[]
 for row in diffhint.listing(data,a,mode):
  m=re.match(r'(\w{8}):\s*(.*)',row);addr=int(m[1],16);text=re.sub(r'^[0-9A-Fa-f]{4,8}\s+','',m[2])
  pool=text.startswith('.word ')
  width=4 if mode=='arm' or pool or text.startswith('bl ') else 2
  out.append(dict(address=addr,text=text,pool=pool,blob=data[addr-a:addr-a+width]))
 return out

def branch(row):return bool(re.match(r'b(?:l|x|eq|ne|gt|ge|lt|le|hi|ls|cs|cc|mi|pl|vs|vc)?\s',row['text']))
def shape(row):
 text=row['text']
 text=re.sub(r'\[pc, #[^]]+\]','[pc, pool]',text)
 text=re.sub(r'@ =0x[0-9A-Fa-f]+','@ pool',text)
 if branch(row) and not text.startswith('bl '):text=re.sub(r'0x08[0-9A-Fa-f]{6}', '<local destination>',text)
 return re.sub(r'\br(?:1[0-5]|[0-9])\b','REG',text)

def generate(profile_path,destination):
 record=json.loads(Path(profile_path).read_text());a=int(record['address'],16);e=int(record['target_end'],16)
 code=Path(record['source']).read_text();assert hashlib.sha256(code.encode()).hexdigest()==record['source_sha256']
 p=draft.Program();want=p.rom[a-draft.BASE:e-draft.BASE]
 got,frame=mc.diagnostic_compile(code,'func_'+record['address'],a,reloc.symbols(p),record['compiler'])
 assert hashlib.sha256(got).hexdigest()==record['compiled_sha256']
 mode='arm' if record['compiler']=='arm' else 'thumb'
 full_left,full_right=listing(want,a,mode),listing(got,a,mode)
 left=[r for r in full_left if not r['pool']];right=[r for r in full_right if not r['pool']]
 starts={a};original_addresses={r['address'] for r in left}
 for idx,row in enumerate(left):
  if branch(row):
   match=re.search(r'0x(08[0-9A-Fa-f]{6})',row['text'])
   if match and int(match[1],16) in original_addresses and not row['text'].startswith('bl '):starts.add(int(match[1],16))
   if not row['text'].startswith('bl ') and idx+1<len(left):starts.add(left[idx+1]['address'])
 counts=dict(identical_opcode_pairs=0,register_operand_pairs=0,pc_reference_pairs=0,branch_destination_pairs=0,unpaired_original_rows=0,unpaired_compiled_rows=0)
 matcher=difflib.SequenceMatcher(None,list(map(shape,left)),list(map(shape,right)),autojunk=False)
 for tag,aa,bb,cc,dd in matcher.get_opcodes():
  if tag!='equal':
   counts['unpaired_original_rows']+=bb-aa;counts['unpaired_compiled_rows']+=dd-cc;continue
  for x,y in zip(left[aa:bb],right[cc:dd]):
   key='identical_opcode_pairs' if x['blob']==y['blob'] else 'pc_reference_pairs' if '[pc,' in x['text'] else 'branch_destination_pairs' if branch(x) else 'register_operand_pairs'
   counts[key]+=1
 regions=[]
 for label,lo,hi in REGIONS[record['address']]:
  lo,hi=int(lo,16),int(hi,16)
  dif=sum(1 for addr in range(lo,hi) if addr-a>=len(got) or want[addr-a]!=got[addr-a])
  regions.append(dict(region=label,start=f'{lo:08X}',end=f'{hi:08X}',original_bytes=hi-lo,positional_different_bytes=dif,original_basic_blocks=sum(lo<=x<hi for x in starts),original_instruction_rows=sum(lo<=r['address']<hi for r in left),original_pool_words=sum(lo<=r['address']<hi and r['pool'] for r in full_left)))
 assert sum(r['positional_different_bytes'] for r in regions)==record['different_bytes'] # retained owners fit
 result=dict(address=record['address'],source_sha256=record['source_sha256'],compiled_sha256=record['compiled_sha256'],method='Original-address windows count positional differences, including pools/missing tail. Global instruction-shape alignment ignores register identities and local branch/PC displacements. Referenced pool words only. It is a heuristic layout aid, not causal attribution or semantic proof. Calls are not block boundaries; unconditional/conditional branches are.',original_local_frame={'0800421C':36,'08016DA8':96,'080064A4':108,'080181C0':72,'08002854':268}[record['address']],compiled_local_frame=frame,original_pool_words=sum(r['pool'] for r in full_left),compiled_pool_words=sum(r['pool'] for r in full_right),shape_alignment=counts,regions=regions)
 Path(destination).write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':generate(*sys.argv[1:])

#!/usr/bin/env python3
"""Compile real C, split its generated functions, verify every replacement byte."""
import os, json, subprocess, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import reloc
root=Path(os.environ.get('TXRA_TOOLS',Path.home()/'opt'))
arm=str(root/'arm-gnu-toolchain-14.3.rel1-x86_64-arm-none-eabi/bin/arm-none-eabi-')
cc=root/'agbcc/old_agbcc'
def run(args): subprocess.run(list(map(str,args)),check=True)
out=Path('build/leaves');out.mkdir(parents=True,exist_ok=True)
b=Path('baserom.gba').read_bytes()
cache={}
table=None
for m in json.loads(Path('tools/rom.cfg').read_text())['matches']:
 name=m['name']; source=m.get('source', 'src/leaves.c')
 compiler=m.get('compiler','old')
 if compiler not in ('old','standard','old-no-gcse','old-o1','standard-o1','modern-arm','old-no-interwork','arm'):raise ValueError('unknown compiler variant')
 key=(source,compiler)
 if key not in cache:
  run([arm+'gcc','-E','-P','-Isrc',source,'-o',out/'leaves.i'])
  if compiler=='modern-arm':
   run([arm+'gcc','-S','-x','c',out/'leaves.i','-O2','-marm','-mcpu=arm7tdmi','-mno-thumb-interwork','-o',out/'leaves.s'])
  else:
   run([cc.with_name('agbcc_arm') if compiler=='arm' else cc.with_name('agbcc') if compiler in ('standard','standard-o1') else cc,out/'leaves.i','-O1' if compiler.endswith('-o1') else '-O2','-mno-thumb-interwork' if compiler=='old-no-interwork' else '-mthumb-interwork',*(['-fno-gcse'] if compiler=='old-no-gcse' else []),'-o',out/'leaves.s'])
  cache[key]=(out/'leaves.s').read_text()
 s=cache[key]; start=s.index(name+':');end=re.search(r'\n\s*\.size\s+'+name+r',[^\n]*',s[start:]).end()+start
 text=('.syntax unified\n.text\n.arm\n' if compiler=='modern-arm' else '.syntax divided\n.text\n'+('.arm\n' if compiler=='arm' else '.thumb\n'))+s[start:end]+'\n'
 (out/(name+'.s')).write_text(text)
 run([arm+'as','-mcpu=arm7tdmi',out/(name+'.s'),'-o',out/(name+'.o')])
 run([arm+'objcopy','-O','binary','-j','.text',out/(name+'.o'),out/(name+'.bin')])
 actual=reloc.function_bytes(out/(name+'.o'), (out/(name+'.bin')).read_bytes(), name, arm+'objdump')
 (out/(name+'.bin')).write_bytes(actual)
 if 'R_ARM_' in subprocess.run([arm+'objdump','-r',str(out/(name+'.o'))],check=True,capture_output=True,text=True).stdout:
  # Calls, function pointers and switch tables resolve to their fixed ROM addresses.
  if table is None:
   import draft; table=reloc.symbols(draft.Program())
  actual=reloc.link_bytes(out/(name+'.o'),actual,0x08000000+m['offset'],table,arm+'objdump')
  (out/(name+'.bin')).write_bytes(actual)
 assert actual==b[m['offset']:m['offset']+m['size']],f'{name}: C does not match ({len(actual)} bytes)'
 print(f'{name}: C match ({len(actual)} bytes)')
(out/'verified').touch()

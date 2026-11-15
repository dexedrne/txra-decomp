"""Integration checks against the private ROM and the generated execution map."""
import hashlib,json,struct,unittest,subprocess,tempfile,sys,zlib
from pathlib import Path
BASE=0x08000000
class RomMapTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.rom=Path('baserom.gba').read_bytes()
 def read(self,name):return json.loads(Path('docs/map/'+name+'.json').read_text())
 def test_full_binary_identity(self):
  self.assertEqual(hashlib.sha1(self.rom).hexdigest(),'4197339d4add74bb40ed02a8fba5e58096afb487')
  self.assertEqual(Path('build/txra.gba').read_bytes(),self.rom)
 def test_header(self):
  self.assertEqual(len(self.rom),0x400000)
  self.assertEqual(self.rom[0xac:0xb0],b'BTZE')
  self.assertEqual(self.rom[0xb2],0x96)
  self.assertEqual((-sum(self.rom[0xa0:0xbd])-0x19)&255,self.rom[0xbd])
  word=struct.unpack_from('<I',self.rom)[0]
  self.assertEqual(8+((word&0xffffff)<<2),0xc0)
 def test_complete_nonoverlapping_partition(self):
  end=BASE
  for r in self.read('splits')['regions']:
   self.assertEqual(int(r['start'],16),end)
   end=int(r['end'],16)
   self.assertGreater(end,int(r['start'],16))
  self.assertEqual(end,BASE+len(self.rom))
 def test_function_extents(self):
  seen=set()
  for f in self.read('functions')['functions']:
   start=int(f['start'],16);end=int(f['end'],16)
   self.assertNotIn(start,seen);seen.add(start)
   self.assertEqual(start%(4 if f['mode']=='arm' else 2),0)
   self.assertLess(start,end)
   self.assertLessEqual(end,BASE+len(self.rom))
   self.assertTrue(any(int(a,16)==start for a,z in f['spans']))
   for a,z in f['spans']:self.assertTrue(start<=int(a,16)<int(z,16)<=end)
 def test_switch_table_targets(self):
  switches=self.read('pointers')['switches']
  self.assertEqual(len(switches),14)
  asm=Path('asm/program.s').read_text()
  matches=json.loads(Path('tools/rom.cfg').read_text())['matches']
  verified=set()
  for t in switches:
   start=int(t['start'],16)-BASE
   self.assertEqual(int(t['end'],16)-BASE,start+4*len(t['targets']))
   for i,target in enumerate(t['targets']):
    addr=int(target,16)
    self.assertEqual(struct.unpack_from('<I',self.rom,start+4*i)[0],addr)
    self.assertEqual(addr%2,0)
    owner=next((m for m in matches if m['offset']<=addr-BASE<m['offset']+m['size']),None)
    if owner is None:
     self.assertTrue(f'@ {addr:08X}' in asm,f'unemitted switch target {addr:08X}')
    else:
     target_bytes=Path('build/leaves/'+owner['name']+'.bin').read_bytes()
     target_offset=addr-BASE-owner['offset']
     self.assertEqual(target_bytes[target_offset:target_offset+2],self.rom[addr-BASE:addr-BASE+2])
    if owner is not None and owner['name'] not in verified:
     name=owner['name'];offset=owner['offset'];size=owner['size']
     self.assertTrue(f'.incbin "build/leaves/{name}.bin"' in asm,f'missing C body {name}')
     compiled=Path(f'build/leaves/{name}.bin').read_bytes()
     self.assertEqual(len(compiled),size)
     self.assertEqual(compiled,self.rom[offset:offset+size],f'switch owner {name}')
     verified.add(name)
 def test_coverage_descent_preserves_static_closure(self):
  # Existing executed PCs must not reorder recursive static discovery.
  script=Path('tools/analyze.py').resolve()
  cfg=json.loads(Path('tools/rom.cfg').read_text());cfg.pop('mapping',None)
  pcs=[]
  for f in self.read('functions')['functions']:
   for a,z in f['spans']:
    pcs.extend([pc,int(f['mode']=='thumb')] for pc in range(int(a,16),int(z,16),2 if f['mode']=='thumb' else 4))
  trace={'rom_crc32':f'{zlib.crc32(self.rom):08x}','overflow':False,'pcs':pcs,'branches':[],'reads':[],'transfers':[]}
  with tempfile.TemporaryDirectory(dir='build') as directory:
   root=Path(directory)
   for name in ('tools','asm','recomp'): (root/name).mkdir()
   (root/'baserom.gba').symlink_to(Path('baserom.gba').resolve())
   (root/'tools/rom.cfg').write_text(json.dumps(cfg))
   (root/'recomp/observed.json').write_text(Path('recomp/observed.json').read_text())
   (root/'trace.json').write_text(json.dumps(trace))
   subprocess.run([sys.executable,str(script)],cwd=root,check=True,capture_output=True)
   before={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for folder in ('asm','docs/map') for p in (root/folder).rglob('*') if p.is_file()}
   subprocess.run([sys.executable,str(script),'--coverage','trace.json'],cwd=root,check=True,capture_output=True)
   after={name:hashlib.sha256((root/name).read_bytes()).hexdigest() for name in before}
   self.assertEqual(before,after)
 def test_real_c_replacements(self):
  cfg=json.loads(Path('tools/rom.cfg').read_text())
  self.assertGreaterEqual(len(cfg['matches']),4)
  for f in cfg['matches']:
   self.assertEqual(Path('build/leaves/'+f['name']+'.bin').read_bytes(),self.rom[f['offset']:f['offset']+f['size']])
if __name__=='__main__':unittest.main()

"""Synthetic classifier and coverage tests; no ROM content in test fixtures."""
import importlib.util
import hashlib
import sys
import zlib
import json
from pathlib import Path
import struct
import subprocess
import tempfile
import unittest

def module(name):
    spec=importlib.util.spec_from_file_location(name,Path('tools')/(name+'.py'))
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

sys.path.insert(0,str(Path('tools').resolve()))
mapping=module('rom_map')
progress=module('progress')

class ClassifierTests(unittest.TestCase):
    def test_lz_exact_source_extent(self):
        stream=bytes([0x10,6,0,0,0x10,65,66,67,0,2,255])
        self.assertEqual(mapping.compressed_size(stream,0),(10,'bios-lz77'))
    def test_lz_invalid_back_reference(self):
        self.assertIsNone(mapping.compressed_size(bytes([0x10,3,0,0,128,0,0]),0))
    def test_rle_exact_extent(self):
        self.assertEqual(mapping.compressed_size(bytes([0x30,6,0,0,0x83,77]),0),(6,'bios-rle'))
    def test_truncated_and_overrun(self):
        for stream in (bytes([0x10,1,0,0]),bytes([0x30,2,0,0,128,7]),bytes([0x28,8,0,0,255])):
            self.assertIsNone(mapping.compressed_size(stream,0))
    def test_huffman_word_order_and_tree(self):
        stream=bytes([0x28,4,0,0,1,0xc0,65,66])+struct.pack('<I',0x50000000)
        self.assertEqual(mapping.compressed_size(stream,0),(12,'bios-huffman8'))
        self.assertIsNone(mapping.compressed_size(stream[:8],0))
    def test_fill_does_not_claim_interior_zero(self):
        rom=bytes(80)+b'x'+bytes([255])*64+b'x'+bytes(70)
        self.assertEqual(list(mapping.fill_runs(rom)),[(81,64,'ff'),(146,70,'terminal-zero')])
    def test_pcm_header_boundaries(self):
        rom=struct.pack('<HHIII',0,0x4000,16000*1024,8,16)+bytes(16)
        self.assertEqual(mapping.pcm_size(rom,0),32)
        self.assertIsNone(mapping.pcm_size(rom[:-1],0))
        self.assertIsNone(mapping.pcm_size(rom,4))
    def test_partition_priorities_and_counts(self):
        rom=bytes(1024)
        cfg={'copies':[]}
        trace={'reads':[[200,32]],'pcs':[[mapping.BASE+200,1]],'transfers':[]}
        splits=[{'start':hex(mapping.BASE+204),'end':hex(mapping.BASE+208),'kind':'literal'}]
        spans=mapping.classify(rom,cfg,splits,[trace])
        result=progress.mapping_progress({'size':len(rom),'mapping':spans})
        self.assertEqual(sum(result[k] for k in ('code_bytes_mapped','data_bytes_mapped','unknown_bytes')),len(rom))
        self.assertTrue(any(b['offset']==200 and b['type']=='code' for b in spans))
    def test_observed_read_bounds(self):
        with self.assertRaises(ValueError):
            mapping.classify(bytes(1024),{'copies':[]},[],[{'reads':[[1023,2]],'transfers':[],'pcs':[]}])
    def test_logger_reports_capacity_exhaustion(self):
        subprocess.run(['make','build/coverage-test'],check=True,stdout=subprocess.DEVNULL)
        with tempfile.TemporaryDirectory(dir='build') as directory:
            path=Path(directory)/'overflow.json'
            subprocess.run(['build/coverage-test',str(path),'overflow'],check=True)
            self.assertTrue(json.loads(path.read_text())['overflow'])
    def test_classifier_command_publishes_partition_and_summary(self):
        command=str(Path('tools/rom_map.py').resolve())
        with tempfile.TemporaryDirectory(dir='build') as directory:
            root=Path(directory);(root/'tools').mkdir();(root/'docs/map').mkdir(parents=True)
            rom=bytes([0x77])*4096
            cfg={'size':len(rom),'base':mapping.BASE,'sha1':hashlib.sha1(rom).hexdigest(),'copies':[]}
            (root/'baserom.gba').write_bytes(rom)
            (root/'tools/rom.cfg').write_text(json.dumps(cfg))
            (root/'docs/map/splits.json').write_text(json.dumps({'regions':[]}))
            (root/'docs/map/indirect.json').write_text(json.dumps({'transfers':[],'veneer_calls':[]}))
            trace={'rom_crc32':f'{zlib.crc32(rom):08x}','overflow':False,'pcs':[[mapping.BASE,0]],
                   'branches':[],'reads':[[200,8]],'transfers':[]}
            (root/'trace.json').write_text(json.dumps(trace))
            subprocess.run([sys.executable,command,'trace.json'],cwd=root,check=True,capture_output=True)
            cfg=json.loads((root/'tools/rom.cfg').read_text())
            result=progress.mapping_progress(cfg)
            self.assertEqual(result['code_bytes_mapped'],4)
            self.assertEqual(result['data_bytes_mapped'],196)
            self.assertEqual(json.loads((root/'docs/map/coverage.json').read_text())['rom_read_bytes'],8)
            trace['rom_crc32']='incorrect';(root/'trace.json').write_text(json.dumps(trace))
            self.assertNotEqual(subprocess.run([sys.executable,command,'trace.json'],cwd=root,capture_output=True).returncode,0)
    def test_custom_audio_descriptors(self):
        rom=bytearray([0x77])*0xc000
        struct.pack_into('<I',rom,0x7ad4,mapping.BASE+0x9000)
        struct.pack_into('<IIII',rom,0x9000,mapping.BASE+0xa000,128,0,0)
        struct.pack_into('<I',rom,0x62dc,mapping.BASE+0x9100)
        struct.pack_into('<IIIII',rom,0x9100,mapping.BASE+0xb000,4,0,0,0)
        spans=mapping.classify(rom,{'copies':[]},[],[])
        self.assertTrue(any(b['offset']==0xa000 and b['size']==128 and b['type']=='audio' for b in spans))
        self.assertTrue(any(b['offset']==0xb000 and b['size']==704 and b['type']=='audio' for b in spans))
    def test_progress_rejects_unknown_type(self):
        with self.assertRaises(ValueError):
            progress.mapping_progress({'size':8,'mapping':[{'offset':0,'size':8,'type':'typo'}]})
    def test_progress_rejects_overlap_and_gap(self):
        for start in (1,3):
            with self.assertRaises(ValueError):
                progress.mapping_progress({'size':8,'mapping':[{'offset':0,'size':2,'type':'code'},{'offset':start,'size':5,'type':'data'}]})
    def test_logger_pc_reads_targets_and_transfers(self):
        subprocess.run(['make','build/coverage-test'],check=True,stdout=subprocess.DEVNULL)
        with tempfile.TemporaryDirectory(dir='build') as directory:
            path=Path(directory)/'coverage.json'
            subprocess.run(['build/coverage-test',str(path)],check=True)
            trace=json.loads(path.read_text())
        self.assertFalse(trace['overflow'])
        for service, source, size in ((0x11,0x08000400,10),(0x14,0x08000500,6),(0x13,0x08000600,12)):
            self.assertTrue(any(t[0]==service and t[2]==source and t[4]==size for t in trace['transfers']))
        self.assertEqual(sorted(trace['pcs']),[[0x080000c0,0],[0x08002000,1],[0x0800d51c,1],[0x0801251c,1]])
        self.assertEqual(sorted(trace['entries']),[[0x0800d51c,4,0,0],[0x0801251c,0x08001000,0x02000000,65536]])
        self.assertEqual(trace['branches'],[[0x080000c0,0x08002001]])
        self.assertIn([256,8],trace['reads'])
        self.assertIn([512,8],trace['reads'])
        self.assertIn([768,2],trace['reads'])
        self.assertTrue(any(t[0]==11 and t[2:]==[0x08000100,0x02000000,8] for t in trace['transfers']))
        self.assertTrue(any(t[0]==2 and t[2:]==[0x08000200,0x02000020,8] for t in trace['transfers']))

class RefineUnknownTests(unittest.TestCase):
    """Synthetic partitions; the two reviewed rules may only relabel unknown bytes."""
    B=mapping.BASE
    def spans(self,*blocks):
        out=[];at=0
        for size,kind in blocks:
            out.append(dict(offset=at,size=size,type=kind,format='thumb' if kind=='code' else
                            'literal-pool-or-switch' if kind=='table' else 'unclassified'));at+=size
        return out
    def test_alignment_halfword_before_pool_and_entry(self):
        rom=bytearray(32); rom[6:8]=b'\xc0\x46'; rom[18:20]=b'\x01\x00'
        spans=self.spans((6,'code'),(2,'unknown'),(4,'table'),(6,'code'),(2,'unknown'),(12,'table'))
        splits=[{'start':hex(self.B),'end':hex(self.B+6),'kind':'thumb'},{'start':hex(self.B+8),'end':hex(self.B+12),'kind':'literal'},
                {'start':hex(self.B+12),'end':hex(self.B+18),'kind':'thumb'},{'start':hex(self.B+20),'end':hex(self.B+32),'kind':'literal'}]
        out=mapping.refine_spans(bytes(rom),spans,splits,[])
        kinds={(b['offset'],b['type'],b['format']) for b in out}
        self.assertIn((6,'fill','alignment-halfword'),kinds)
        self.assertIn((18,'unknown','unclassified'),kinds)   # nonzero, non-nop halfword stays unknown
        self.assertEqual(sum(b['size'] for b in out),len(rom))
    def test_unaligned_or_unmapped_neighbour_stays_unknown(self):
        rom=bytes(16)
        spans=self.spans((4,'unknown'),(2,'unknown'),(10,'code'))
        splits=[{'start':hex(self.B+6),'end':hex(self.B+16),'kind':'thumb'}]
        out=mapping.refine_spans(rom,spans,splits,[])
        self.assertEqual([b['type'] for b in out],['unknown','code'])
    def test_code_entry_pointer_array_needs_three_distinct_entries(self):
        funcs=[{'start':hex(self.B+0x40),'mode':'thumb','runtime_aliases':[]},
               {'start':hex(self.B+0x80),'mode':'arm','runtime_aliases':[{'start':'0x03000100'}]},
               {'start':hex(self.B+0xC0),'mode':'thumb','runtime_aliases':[]}]
        words=[self.B+0x41,0x03000100,self.B+0xC1,0x12345678,self.B+0x41,self.B+0x41,self.B+0x41]
        rom=struct.pack('<7I',*words)+bytes(4)
        spans=[dict(offset=0,size=4,type='data',format='observed-rom-read'),
               dict(offset=4,size=len(rom)-4,type='unknown',format='unclassified')]
        out=mapping.refine_spans(rom,spans,[],funcs)
        tables=[(b['offset'],b['size']) for b in out if b['format']=='code-entry-pointer-array']
        self.assertEqual(tables,[(4,8)])                    # observed slot keeps its read label
        self.assertFalse(any(b['type']=='table' and b['offset']>=16 for b in out))  # repeated single target rejected
        self.assertEqual(sum(b['size'] for b in out),len(rom))

if __name__=='__main__':unittest.main()

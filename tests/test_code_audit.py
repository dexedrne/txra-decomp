"""Synthetic instructions only; no cartridge-derived fixtures."""
import struct
import hashlib
import random
import json
import subprocess
import tempfile
import sys
from pathlib import Path
import unittest
sys.path.insert(0, str(Path('tools').resolve()))
import code_audit as audit


def words(*values):
    return struct.pack('<'+'H'*len(values), *values)


class CodeAuditTests(unittest.TestCase):
    def check_code(self, code, **kwargs):
        return audit.validate_thumb(code, 0, [{'source_offset': 100}], **kwargs)

    def test_leaf_with_store(self):
        self.assertTrue(self.check_code(words(0x6008, 0x4770))['valid'])

    def test_conditional_paths_and_stack_return(self):
        code = words(0xb510, 0x2800, 0xd000, 0x6008, 0xbd10)
        result = self.check_code(code)
        self.assertTrue(result['valid'], result)
        self.assertEqual(result['spans'], [[0, 10]])

    def test_register_return_after_pop(self):
        self.assertTrue(self.check_code(words(0xb510, 0xbc10, 0xbc01, 0x4700))['valid'])

    def test_stack_local_allocation(self):
        self.assertTrue(self.check_code(words(0xb500, 0xb082, 0xb002, 0xbd00))['valid'])

    def test_missing_reference(self):
        self.assertEqual(audit.validate_thumb(words(0x4770), 0, [])['reason'], 'no reference')

    def test_stack_underflow(self):
        self.assertEqual(self.check_code(words(0xbd00))['reason'], 'stack underflow')

    def test_unbalanced_bx(self):
        self.assertIn('unbalanced', self.check_code(words(0xb500, 0x4770))['reason'])

    def test_unresolved_bx(self):
        self.assertFalse(self.check_code(words(0x4700))['valid'])

    def test_random_data_is_bounded_and_always_has_a_disposition(self):
        rng = random.Random(1701)
        for _ in range(256):
            result = self.check_code(rng.randbytes(64),budget=16)
            self.assertIsInstance(result['valid'],bool)
            self.assertTrue(result['reason'])

    def test_no_undecodable_fallthrough(self):
        self.assertFalse(self.check_code(words(0x2000, 0xffff))['valid'])

    def test_reject_newer_instruction_set(self):
        for word in (0xbe00,0xb650,0xb100):
            self.assertFalse(self.check_code(words(word,0x4770))['valid'])

    def test_call_requires_saved_lr(self):
        self.assertIn('without saved LR', self.check_code(words(0xf000, 0xf800, 0x4770))['reason'])

    def test_overwritten_stack_return_is_rejected(self):
        code = words(0xb500, 0xb001, 0xb401, 0xbd00)
        self.assertFalse(self.check_code(code)['valid'])

    def test_stack_store_over_return_address_is_rejected(self):
        self.assertFalse(self.check_code(words(0xb500, 0x9000, 0xbd00))['valid'])

    def test_stack_store_into_local_is_valid(self):
        self.assertTrue(self.check_code(words(0xb500, 0xb081, 0x9000, 0xb001, 0xbd00))['valid'])

    def test_discarded_LR_after_call_cannot_return(self):
        code = words(0xb500, 0xf000, 0xf800, 0xb001, 0x4770)
        self.assertFalse(self.check_code(code)['valid'])

    def test_saved_call_and_return(self):
        self.assertTrue(self.check_code(words(0xb500, 0xf000, 0xf800, 0xbd00))['valid'])

    def test_literal_cannot_be_executed(self):
        self.assertFalse(self.check_code(words(0x4800, 0x2000, 0x4770, 0x0000))['valid'])

    def test_established_pool_is_rejected(self):
        self.assertFalse(self.check_code(words(0x4770), forbidden={0})['valid'])

    def test_unconditional_loop_not_function_proof(self):
        self.assertIn('no proven return', self.check_code(words(0xe7fe))['reason'])

    def test_budget_bound(self):
        self.assertIn('budget', self.check_code(words(0x2000, 0x2000, 0x4770), budget=1)['reason'])

    def test_packed_callback_records_and_final_slot(self):
        rom = bytearray(20)
        struct.pack_into('<I', rom, 2, audit.BASE+17)
        struct.pack_into('<I', rom, 12, audit.BASE+17)
        spans = [{'offset': 0, 'size': 6, 'type': 'unknown'},
                 {'offset': 6, 'size': 6, 'type': 'code'},
                 {'offset': 12, 'size': 4, 'type': 'table'},
                 {'offset': 16, 'size': 4, 'type': 'data'}]
        refs = audit.pointer_candidates(rom, spans)
        self.assertEqual([r['source_offset'] for r in refs[16]], [2,12])
        self.assertFalse(refs[16][0]['word_aligned'])

    def test_byte_packed_callback_slot(self):
        rom = b'x'+struct.pack('<I',audit.BASE+1)
        refs = audit.pointer_candidates(rom,[{'offset':0,'size':5,'type':'data'}])
        self.assertEqual(refs[0][0]['source_offset'],1)

    def test_pointer_crosses_classification_boundary(self):
        rom = struct.pack('<I', audit.BASE+1)
        spans = [{'offset':0,'size':2,'type':'data'}, {'offset':2,'size':2,'type':'unknown'}]
        self.assertEqual(list(audit.pointer_candidates(rom, spans)), [0])

    def test_leaf_cannot_replace_return_address(self):
        self.assertIn('LR write', self.check_code(words(0x4686, 0x4770))['reason'])

    def test_pointer_excludes_nonROM_even_and_code(self):
        rom = struct.pack('<IIII', audit.BASE+2, 0x03000001, audit.BASE+3, audit.BASE+3)
        spans = [{'offset': 0, 'size': 8, 'type': 'data'}, {'offset': 8, 'size': 8, 'type': 'code'}]
        self.assertEqual(dict(audit.pointer_candidates(rom, spans)), {})

    def test_direct_BL_only_in_known_code(self):
        rom = words(0xf000, 0xf802, 0xf000, 0xf800, 0x4770)
        splits = [{'start': hex(audit.BASE), 'end': hex(audit.BASE+4), 'kind': 'thumb'}]
        refs = audit.direct_candidates(rom, splits)
        self.assertEqual(list(refs), [(8,'thumb')])
        self.assertEqual(refs[8,'thumb'][0]['source_offset'], 0)

    def test_resolved_indirect_and_unique_RAM_alias(self):
        cfg = {'base':audit.BASE, 'size':100, 'copies':[{'load':audit.BASE+20,'run':0x03000000,'size':8,'mode':'thumb'}]}
        sites = {'transfers':[{'source':hex(audit.BASE+4),'target':'0x03000001'},
                               {'source':hex(audit.BASE+6),'target':None},
                               {'source':hex(audit.BASE+8),'target':None,'kind':'return'}]}
        refs, unresolved = audit.indirect_candidates(sites, cfg)
        self.assertEqual(list(refs), [(20,'thumb')])
        self.assertEqual(unresolved, [hex(audit.BASE+6)])

    def test_ambiguous_RAM_alias_remains_unresolved(self):
        copy = {'load':audit.BASE+20,'run':0x03000000,'size':8,'mode':'thumb'}
        cfg = {'base':audit.BASE,'size':100,'copies':[copy,dict(copy,load=audit.BASE+40)]}
        refs, unresolved = audit.indirect_candidates({'transfers':[{'source':'0x08000004','target':'0x03000001'}]},cfg)
        self.assertEqual(dict(refs), {})
        self.assertEqual(unresolved, ['0x08000004'])

    def test_switch_blocks_do_not_inflate_function_count(self):
        cfg = {'base':audit.BASE,'size':8,'sha1':'synthetic','mapping':[]}
        site = {'source':'0x08000004','target':None,'targets':['0x08000000'],
                'mode':'thumb','confidence':'bounded switch'}
        result = audit.audit(words(0x4770)*4,cfg,[],[],{'transfers':[site]})
        self.assertEqual(result['counts']['internal-switch-target'],1)
        self.assertEqual(result['counts']['proposal'],0)

    def test_odd_scalar_into_ARM_code_is_rejected(self):
        rom = struct.pack('<II',0xe12fff1e,audit.BASE+1)
        cfg = {'base':audit.BASE,'size':8,'sha1':'synthetic',
               'mapping':[{'offset':4,'size':4,'type':'table'}]}
        splits = [{'start':'0x08000000','end':'0x08000004','kind':'arm'}]
        result = audit.audit(rom,cfg,[],splits)
        self.assertIn('instruction mode',result['candidates'][0]['reason'])

    def test_metadata_audit_statuses_and_reasons(self):
        rom = words(0x4770, 0x4700) + struct.pack('<II', audit.BASE+1, audit.BASE+3)
        cfg = {'size': len(rom), 'base': audit.BASE, 'sha1': 'synthetic', 'mapping': [{'offset':4,'size':8,'type':'table'}]}
        result = audit.audit(rom, cfg, [], [])
        self.assertEqual(result['counts']['proposal'], 1)
        self.assertEqual(result['counts']['rejected'], 1)
        cfg['mapping'][0]['type'] = 'code'
        self.assertEqual(audit.audit(rom, cfg, [], [])['candidates'], [])

class AuditCommandTests(unittest.TestCase):
    def test_command_logs_proposal_and_rejection_and_refuses_wrong_ROM(self):
        command = str(Path('tools/code_audit.py').resolve())
        rom = words(0x4770,0x4700)+struct.pack('<II',audit.BASE+1,audit.BASE+3)
        with tempfile.TemporaryDirectory(dir='build') as directory:
            root = Path(directory); (root/'tools').mkdir(); (root/'docs/map').mkdir(parents=True)
            cfg = {'base':audit.BASE,'size':len(rom),'sha1':hashlib.sha1(rom).hexdigest(),
                   'mapping':[{'offset':4,'size':8,'type':'table'}]}
            (root/'baserom.gba').write_bytes(rom)
            (root/'tools/rom.cfg').write_text(json.dumps(cfg))
            for name, content in [('functions',{'functions':[]}),('splits',{'regions':[]}),('indirect',{})]:
                (root/f'docs/map/{name}.json').write_text(json.dumps(content))
            subprocess.run([sys.executable,command],cwd=root,check=True,capture_output=True)
            report = (root/'docs/map/code-audit.json').read_text()
            result = json.loads(report)
            self.assertEqual(result['counts']['proposal'],1)
            self.assertEqual(result['counts']['rejected'],1)
            self.assertTrue(all(row['reason'] for row in result['candidates']))
            self.assertEqual(json.loads((root/'tools/rom.cfg').read_text()),cfg)
            (root/'baserom.gba').write_bytes(bytes(len(rom)))
            run = subprocess.run([sys.executable,command],cwd=root,capture_output=True,text=True)
            self.assertNotEqual(run.returncode,0)
            self.assertIn('wrong ROM',run.stderr)
            self.assertEqual((root/'docs/map/code-audit.json').read_text(),report)

if __name__ == '__main__':
    unittest.main()

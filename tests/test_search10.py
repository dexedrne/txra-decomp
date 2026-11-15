"""Verify conservative operators and a real compiler/checkpoint round trip."""
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
import search10 as s


class Search10Tests(unittest.TestCase):
    def test_context_tracks_arm_compiler_replacement_and_absence(self):
        from unittest.mock import patch
        original=Path.read_bytes
        with tempfile.TemporaryDirectory() as td:
            compiler=Path(td)/'agbcc_arm';compiler.write_bytes(b'compiler-a')
            def read(path):return original(path) if path==compiler else b'unchanged-input'
            with patch.object(s.v.judge,'CC',Path(td)/'old_agbcc'),patch.object(Path,'read_bytes',read):
                a=s.fingerprint();compiler.write_bytes(b'compiler-b');b=s.fingerprint()
                self.assertNotEqual(a,b)
                compiler.unlink();missing=s.fingerprint()
                self.assertNotEqual(b,missing)
                self.assertEqual(missing,s.fingerprint())

    def test_first_compiler_batch_respects_target_instruction_state(self):
        from types import SimpleNamespace
        from unittest.mock import Mock,patch
        class BatchCaptured(Exception):pass
        for mode,expected in [('arm',('arm','modern-arm')),('thumb',s.v.profiles_for_mode('thumb'))]:
            with tempfile.TemporaryDirectory() as td:
                seen=[]
                def capture(worker,jobs):
                    seen.extend(job[3] for job in jobs)
                    raise BatchCaptured()
                pool=SimpleNamespace(map=capture);db=Mock();db.execute.return_value.fetchone.return_value=None
                prog=SimpleNamespace(by_start={0x08001000:{'mode':mode}})
                args=SimpleNamespace(output=Path(td)/'out',seed=1,seconds=60)
                with patch.object(s,'ROOT',Path(td)),patch.object(s.v,'seeds',return_value=['void f(void) {}']),patch.object(s.v,'comparison_end',return_value=0x08001008):
                    with self.assertRaises(BatchCaptured):s.search(pool,prog,{'address':'08001000','source':None},args,db,'test-context')
                self.assertEqual(tuple(seen),expected)

    def test_integer_address_operators_always_return_source(self):
        for op,source in s.extra_mutations('void f(void) {\nu32 cursor;\ncursor += 2;\n}'):
            self.assertIsInstance(source,str)
            if op=='address-pointer':self.assertNotIn('u32 *)cursor',source)

    def test_dependency_safe_reordering(self):
        good='void f(void) {\nu32 a;\nu32 b;\nu32 x;\nu32 y;\na = x;\nb = y;\n}'
        self.assertTrue(any(op=='independent-order' for op,_ in s.extra_mutations(good)))
        for bad in (good.replace('b = y','b = a'),good.replace('a = x','a = b'),good.replace('a = x','a = read()'),good.replace('a = x','a = *x')):
            self.assertFalse(any(op=='independent-order' for op,_ in s.extra_mutations(bad)))

    def test_deterministic_learned_first(self):
        src='void func_08001000(void) {\nu32 sum;\nu32 *p;\nsum = *p++;\n}'
        a=s.neighborhood(src,random.Random(12));b=s.neighborhood(src,random.Random(12))
        self.assertEqual(a,b)
        self.assertEqual(a[0][0],'separate-updates')

    def test_switch_rejects_modified_selector(self):
        src='if (a == 1) { a = 2; } if (a == 2) { x = 3; }'
        self.assertFalse(any(op=='if-switch' for op,_ in s.extra_mutations(src)))

    def test_real_compiler_resume_and_no_false_match(self):
        if len(s.choose_targets(s.v.draft.Program(),2))<2:
            self.skipTest('fewer than two unmatched retained drafts remain to search')
        with tempfile.TemporaryDirectory(dir=ROOT/'build',prefix='search10-test-') as td:
            out=Path(td)
            cmd=[sys.executable,'tools/search10.py','--count','2','--seconds','1','--output',str(out)]
            subprocess.run(cmd,cwd=ROOT,check=True,stdout=subprocess.DEVNULL,timeout=120)
            before={p.parent.name:json.loads(p.read_text()) for p in out.glob('*/result.json')}
            self.assertEqual(len(before),2)
            for row in before.values():
                self.assertFalse(row['exact']);self.assertGreaterEqual(row['seconds'],1)
                self.assertGreater(row['compiled']+row['cache_hits'],0)
            subprocess.run(cmd,cwd=ROOT,check=True,stdout=subprocess.DEVNULL,timeout=120)
            after={p.parent.name:json.loads(p.read_text()) for p in out.glob('*/result.json')}
            for a in before:
                self.assertEqual(before[a]['compiled'],after[a]['compiled'])
                self.assertEqual(before[a]['attempts'],after[a]['attempts'])
                self.assertEqual(before[a]['best_score'],after[a]['best_score'])

if __name__=='__main__':unittest.main()

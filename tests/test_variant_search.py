import sys
import unittest
from pathlib import Path
import random
sys.path[:0] = [str(Path(__file__).resolve().parents[1]/'tools')]
import variant_search as search


class VariantSearchTests(unittest.TestCase):
    def test_edit_distance_counts_insertions_once(self):
        self.assertEqual(search.edit_distance(['a','b','c'], ['a','x','b','c']), 1)
        self.assertEqual(search.edit_distance(['a'], ['b']), 1)
        self.assertEqual(search.edit_distance([], ['b']), 1)

    def test_instruction_addresses_and_encodings_do_not_affect_token(self):
        # mov r0,#1 and mov r0,#2: one differing instruction.
        self.assertEqual(search.score(b'\x01\x20\x70\x47',b'\x02\x20\x70\x47',0x08001000), (1,1))

    def test_arm_scoring_and_review_use_arm_instructions(self):
        want=bytes.fromhex('0100a0e31eff2fe1')  # mov r0,#1; bx lr
        got=bytes.fromhex('021082e21eff2fe1')   # add r1,r2,#2; bx lr
        self.assertEqual(len(search.instruction_tokens(want,0x08001000,mode='arm')),2)
        self.assertEqual(search.score(want,got,0x08001000,mode='arm'),(1,4))
        review=search.source_diff(want,got,0x08001000,mode='arm')
        self.assertIn('mov r0',review)
        self.assertIn('add r1',review)

    def test_arm_compiler_profiles_score_their_emitted_instruction_state(self):
        from unittest.mock import patch
        want=bytes.fromhex('0100a0e31eff2fe1')
        got=bytes.fromhex('021082e21eff2fe1')
        with patch.object(search,'SYMBOLS',{},create=True),patch.object(search.judge,'compile_candidate',return_value=(False,8,'',want.hex(),got.hex())):
            for profile in ('arm','modern-arm'):
                score,size,actual,error=search.compile_job((0x08001000,0x08001008,'',profile))
                self.assertIsNone(error)
                self.assertEqual((score,size,actual),((1,4),8,got))

    def test_declaration_and_parameter_neighborhoods(self):
        code='u32 func_08001000(u32 a, u32 b) {\n    u32 x, y;\n    x = a;\n    y = b;\n    return x + y;\n}\n'
        variants=list(search.mutations(code,random.Random(1)))
        self.assertTrue(any('register u32 x;' in x for x in variants))
        self.assertTrue(any('s16 x;' in x for x in variants))
        self.assertTrue(any('func_08001000(u16 a, u32 b)' in x for x in variants))
        self.assertTrue(any('u32 b, u32 a' in x for x in variants))

    def test_dependent_assignments_are_not_swapped(self):
        code='void func_08001000(void) {\n    u32 a,b;\n    a = 1;\n    b = a;\n}\n'
        self.assertFalse(any('b = a;\n    a = 1;' in x for x in search.mutations(code,random.Random(1))))

    def test_loop_and_compound_variants(self):
        code='void func_08001000(void) {\n    u32 n;\n    n = 4;\n    while (n != 0) { n -= 1; }\n}\n'
        variants=list(search.mutations(code,random.Random(1)))
        self.assertTrue(any('for (; n != 0;)' in x for x in variants))
        self.assertTrue(any('n = n - (1);' in x for x in variants))

    def test_compact_initializers_are_retained(self):
        code='void func_08001000(void){u32 x=4;u32 y=8;while(x){x--;}}'
        variants=list(search.mutations(code,random.Random(1)))
        self.assertTrue(any('register u32 x=4;' in x for x in variants))
        self.assertTrue(any('u32 x;\nx=4;' in x for x in variants))
        self.assertEqual(variants,list(search.mutations(code,random.Random(1))))

    def test_comparison_includes_pools_after_mapped_instructions(self):
        import draft
        p=draft.Program()
        a=0x08018AA4
        self.assertEqual(search.comparison_end(p,a),0x08018B24)
        self.assertGreater(search.comparison_end(p,a),int(p.by_start[a]['end'],16))

    def test_o1_winner_and_wrong_profile_are_distinguished(self):
        import draft
        import reloc
        p=draft.Program(); a=0x08018AA4
        search.SYMBOLS=reloc.symbols(p)
        search.ROM=p.rom
        code=(Path(__file__).resolve().parents[1]/'tools/search-drafts/func_08018AA4.c').read_text()
        end=search.comparison_end(p,a)
        self.assertEqual(search.compile_job((a,end,code,'standard-o1'))[0],(0,0))
        self.assertNotEqual(search.compile_job((a,end,code,'old'))[0],(0,0))

    def test_assembly_cache_retains_full_comparison(self):
        import draft
        import llm_match as judge
        import reloc
        from unittest.mock import patch
        p=draft.Program(); a=0x08014518
        code=judge.matched_sources(p)[a]
        cache={}
        with patch.object(judge,'run',wraps=judge.run) as calls:
            first=judge.compile_candidate(code,'func_%08X'%a,a,a+4096,reloc.symbols(p),cache=cache,rom=p.rom)
            count=calls.call_count
            second=judge.compile_candidate(code,'func_%08X'%a,a,a+4096,reloc.symbols(p),cache=cache,rom=p.rom)
            self.assertEqual(calls.call_count-count,2)
        self.assertEqual(first,second)
        self.assertTrue(second[0])
        self.assertEqual(len(cache),1)

    def test_for_while_and_guarded_do_forms(self):
        code='for (i=0; i<8; i++) { if (p[i]) { sum+=p[i]; } }'
        variants=list(search.loop_mutations(code))
        self.assertEqual(len(variants),1)
        self.assertIn('while (i<8)',variants[0])
        self.assertIn('i++;',variants[0])
        self.assertEqual(list(search.loop_mutations('for (i=0; i<8; i++) { continue; }')),[])
        self.assertEqual(list(search.loop_mutations('while (n) { n--; }')),['if (n) do { n--; } while (n);'])

    def test_profiles_follow_instruction_state(self):
        self.assertEqual(search.profiles_for_mode('arm'), ('arm', 'modern-arm'))
        self.assertIn('old-no-interwork', search.profiles_for_mode('thumb'))
        self.assertEqual(set(search.profiles_for_mode('thumb')) |
                         set(search.profiles_for_mode('arm')), set(search.PROFILES))

    def test_all_profiles_compile_known_exact(self):
        import llm_match as judge
        import reloc
        import draft
        p=draft.Program(); a=0x08014518
        code=judge.matched_sources(p)[a]
        for profile in search.profiles_for_mode('thumb'):
            result=judge.compile_candidate(code,'func_%08X'%a,a,a+4096,reloc.symbols(p),target_end=int(p.by_start[a]['end'],16),compiler=profile)
            self.assertTrue(result[0],profile)

if __name__ == '__main__':
    unittest.main()

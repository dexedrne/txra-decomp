import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
import matching_patterns as patterns

class LearnedNeighborhoodTests(unittest.TestCase):
    def test_entry_guard_preserves_zero_iterations(self):
        sources = [s for name,s in patterns.transformations('void f(void) { while (count) { count--; } }') if name == 'guarded-loop']
        self.assertTrue(any('if (count) do {' in s for s in sources))

    def test_cursor_preserves_type_and_avoids_duplicate_name(self):
        sources = list(patterns.transformations('u16 *p = base + offset;'))
        self.assertIn(('integer-cursor', 'u32 p_address = (u32)(base + offset);\nu16 *p = (u16 *)p_address;'), sources)
        self.assertFalse(any(n == 'integer-cursor' for n,s in patterns.transformations('u32 p_address; u16 *p = base;')))

    def test_store_order_is_reviewable(self):
        self.assertIn(('separate-updates', '*dst = value;\ndst++;'), list(patterns.transformations('*dst++ = value;')))

    def test_focus_rejects_unrelated_edit(self):
        before = 'u32 count = 0;\nu32 tail = sum;'
        self.assertFalse(patterns.touches_focus(before,before.replace('count = 0','count = 1'),'tail'))
        self.assertTrue(patterns.touches_focus(before,before.replace('tail = sum','tail = ~sum'),'tail'))
        self.assertTrue(patterns.touches_focus(before,before.replace('tail', 'register tail'),'tail'))

    def test_learned_stack_rewrite_reproduces_accepted_function(self):
        import variant_search as search
        import draft
        import reloc
        root = Path(__file__).resolve().parents[1]
        source = (root / 'tools/search-drafts/func_08018B24.c').read_text()
        # Restore the natural pointer seed that missed the addition's operand order.
        source = source.replace('    u32 offset;\n', '')
        source = source.replace('offset = *((u8 *)g_03007B50 + 8) * 2;\n    p = (u16 *)(offset + (u32)buffer);\n    p++;',
                                'p = buffer + *((u8 *)g_03007B50 + 8) + 1;')
        candidates = [s for n,s in patterns.transformations(source) if n == 'scaled-stack-address']
        self.assertEqual(len(candidates), 1)
        p = draft.Program(); a = 0x08018B24
        search.SYMBOLS = reloc.symbols(p); search.ROM = p.rom
        self.assertEqual(search.compile_job((a,search.comparison_end(p,a),candidates[0],'standard-o1'))[0], (0,0))

    def test_global_cursor_stays_inside_function(self):
        code = 'extern u32 g_03000100;\nu32 func_08001000(void) { u32 i; for(i=0;i<2;i++) { g_03000100 = i; } return 0; }'
        sources = [s for n,s in patterns.transformations(code) if n == 'explicit-global-cursor']
        self.assertEqual(len(sources), 1)
        self.assertIn('u32 *g_03000100_cursor;', sources[0])
        self.assertIn('(*g_03000100_cursor) = i;', sources[0])

class DirectReturnPatternTests(unittest.TestCase):
    def test_cleanup_prevents_direct_return(self):
        code = 's32 f(void) { s32 result; result = 1; goto done;\ndone: release(); return result; }'
        self.assertFalse(any(n == 'direct-short-return' for n,s in patterns.transformations(code)))

    def test_learned_angle_sequence_reproduces_complete_match(self):
        import variant_search as search
        import draft
        import reloc
        root = Path(__file__).resolve().parents[1]
        source = (root / 'docs/near-misses/func_08014614.c').read_text()
        direct = [s for n,s in patterns.transformations(source)
                  if n == 'direct-short-return' and 's32 result;' in s][0]
        grouped = [s for n,s in patterns.transformations(direct)
                   if n == 'distributed-offset' and 'b - (a + 16384)' in s][0]
        distributed = [s for n,s in patterns.transformations(grouped)
                       if n == 'distributed-offset' and 'b + 16384 - a' in s][0]
        p = draft.Program(); a = 0x08014614
        search.SYMBOLS = reloc.symbols(p); search.ROM = p.rom
        result = search.compile_job((a,search.comparison_end(p,a),distributed,'old'))
        self.assertEqual(result[0], (0,0))
        self.assertEqual(result[1], 88)

class DecoderPatternTests(unittest.TestCase):
    def test_backedge_with_another_exit_stays_manual(self):
        code = 'void f(void) {\nloop: if (ready) goto done; body(); if (a) goto done; if (b) goto loop; done: return; }'
        self.assertFalse(any(n == 'structured-backedge' for n,s in patterns.transformations(code)))

    def test_learned_decoder_sequence_reproduces_complete_match(self):
        import variant_search as search
        import draft
        import reloc
        root = Path(__file__).resolve().parents[1]
        source = (root / 'docs/match6-search/expanded/func_0801251C.c').read_text()
        for operation in ('structured-backedge','direct-mask-test','named-add-input'):
            source = next(s for n,s in patterns.transformations(source) if n == operation)
        p = draft.Program(); a = 0x0801251C
        search.SYMBOLS = reloc.symbols(p); search.ROM = p.rom
        result = search.compile_job((a,search.comparison_end(p,a),source,'old'))
        self.assertEqual(result[0], (0,0))
        self.assertEqual(result[1], 226)

class HalfwordDecoderPatternTests(unittest.TestCase):
    def test_decoder_patterns_transfer_to_the_halfword_sibling(self):
        import variant_search as search
        import draft
        import reloc
        root = Path(__file__).resolve().parents[1]
        source = (root / 'docs/match7-seeds/func_080123F0.c').read_text()
        for operation in ('structured-backedge','direct-mask-test',
                          'direct-mask-assignment','direct-mask-assignment','direct-zero-test'):
            source = next(s for n,s in patterns.transformations(source) if n == operation)
        p = draft.Program(); a = 0x080123F0
        search.SYMBOLS = reloc.symbols(p); search.ROM = p.rom
        result = search.compile_job((a,search.comparison_end(p,a),source,'old'))
        self.assertEqual(result[0], (0,0))
        self.assertEqual(result[1], 300)

if __name__ == '__main__': unittest.main()

import json
from pathlib import Path
import subprocess
import sys
import unittest
from unittest.mock import patch
import tempfile
sys.path.insert(0, str(Path('tools').resolve()))
import llm_match as m


class RoundThreeTests(unittest.TestCase):
    def test_hard_range_and_fragments(self):
        p = m.draft.Program()
        # Keep a known standalone fixture eligible as matching progresses.
        p.matched.pop(0x08014614, None)
        skipped = {}
        cs = m.candidates(p, skipped, hard=True)
        self.assertTrue(cs)
        self.assertTrue(all(8 <= len(p.insns[c.start]) <= 40 for c in cs))
        # Long-branch labels reached by reviewed far jumps (the HUD epilogue and
        # the sound owner's five labels) are part of their owners rather than
        # separate fragment entries.
        for a in (0x080051FE, 0x08006712, 0x08006740, 0x08006776, 0x0800735C, 0x08007368):
            self.assertNotIn(a, {c.start for c in cs})
            self.assertNotIn(a, skipped)

    def test_hard_cli_is_read_only_without_real_requests(self):
        before = {f: Path(f).read_bytes() for f in ('tools/rom.cfg', 'progress.json')}
        result = subprocess.run([sys.executable, 'tools/llm_match.py', '--hard', '--dry-run',
                                 '--limit', '1', '--retries', '1'], capture_output=True, text=True, timeout=120)
        self.assertEqual(result.returncode, 0, result.stderr)
        for f, content in before.items(): self.assertEqual(Path(f).read_bytes(), content)
        state = json.loads(Path('build/llm-dry-status.json').read_text())
        expected = min(1, len(m.candidates(m.draft.Program(), hard=True))) * 2
        self.assertEqual(state['requests'], expected)
        self.assertEqual(state['deterministic']['tried'], 0)

    def test_hard_dry_run_exercises_a_known_eligible_fixture(self):
        program = m.draft.Program()
        program.matched.pop(0x08014614, None)
        before = {f: Path(f).read_bytes() for f in ('tools/rom.cfg', 'progress.json')}
        with tempfile.TemporaryDirectory(dir='build') as td:
            status = Path(td) / 'status.json'
            with patch.object(m.draft, 'Program', return_value=program), \
                 patch.object(m, 'STATE', status), \
                 patch.object(m, 'LOG', Path(td) / 'dry.log'), \
                 patch.object(sys, 'argv', ['llm_match.py','--hard','--dry-run','--limit','1','--retries','1']):
                m.main()
                # main selects the dry-run state location explicitly.
                result = json.loads(m.STATE.read_text())
                self.assertEqual(result['requests'], 2)
                self.assertEqual(result['deterministic']['tried'], 0)
        for f, content in before.items():
            self.assertEqual(Path(f).read_bytes(), content)

    def test_retry_recovers_nearest_compiled_source(self):
        close, best = m.retry_context('close();\n', '\nByte distance: 2\ndiff A')
        regressed, best = m.retry_context('regression();\n', '\nByte distance: 8\ndiff B', best)
        self.assertIn('closest compiled attempt', regressed)
        self.assertIn('close();', regressed)
        failed, best = m.retry_context('invalid();\n', 'Compilation failed', best)
        self.assertIn('diff A', failed)
        improved, best = m.retry_context('improved();\n', '\nByte distance: 1\ndiff C', best)
        self.assertEqual(best[0], 1)
        self.assertNotIn('close();', improved)

    def test_distance_counts_missing_bytes(self):
        feedback = m.mismatch_feedback(0x08001000, '01207047', '0120')
        self.assertIn('Byte distance: 2', feedback)
        self.assertIn('target 4 bytes, compiled 2 bytes', feedback)

    def test_prompt_supplies_callee_signature_and_shared_layouts(self):
        p = m.draft.Program()
        a = 0x0801604C
        c = m.Candidate(a, int(p.by_start[a]['end'], 16), a + 128, True, False)
        prompt = m.build_prompt(p, c)
        self.assertIn('extern void func_0800761C(u32 a,u32 i);', prompt)
        self.assertIn('TxraRow28 *g_03006874;', prompt)
        self.assertIn('already included by the judge', prompt)
        self.assertIn('separate shift assignment', prompt)
        self.assertNotIn('extern u8 g_03006874[];', prompt)

    @unittest.skipUnless(m.toolchain_ready(), 'matching compiler unavailable')
    def test_standard_compiler_variant_is_verified(self):
        p = m.draft.Program()
        a = 0x08018A5C
        code = Path('src/generated/func_08018A5C.c').read_text()
        table = m.reloc.symbols(p)
        standard = m.compile_candidate(code, 'func_08018A5C', a, a + 72, table,
                                       target_end=a + 72, compiler='standard')
        self.assertTrue(standard[0])
        self.assertEqual(standard[1], 72)
        old = m.compile_candidate(code, 'func_08018A5C', a, a + 72, table, target_end=a + 72)
        self.assertFalse(old[0])
        with self.assertRaises(ValueError):
            m.compile_candidate(code, 'func_08018A5C', a, a + 72, table, compiler='unknown')


class CompilerOptionsTests(unittest.TestCase):
    @unittest.skipUnless(m.toolchain_ready(), 'matching compiler unavailable')
    def test_runtime_copy_has_separate_interworking_policy(self):
        a = 0x08018E1C
        code = Path('src/generated/func_08018E1C.c').read_text()
        chosen = m.compile_candidate(code, 'func_08018E1C', a, a + 94,
                                     target_end=a + 94, compiler='old-no-interwork')
        self.assertTrue(chosen[0])
        self.assertEqual(chosen[1], 94)
        default = m.compile_candidate(code, 'func_08018E1C', a, a + 128,
                                      target_end=a + 94)
        self.assertFalse(default[0])

    @unittest.skipUnless(m.toolchain_ready(), 'matching compiler unavailable')
    def test_dispatcher_includes_switch_table_and_final_literals(self):
        p = m.draft.Program()
        a = 0x08002500
        code = Path('src/generated/func_08002500.c').read_text()
        table = m.reloc.symbols(p)
        chosen = m.compile_candidate(code, 'func_08002500', a, a + 632, table,
                                     target_end=int(p.by_start[a]['end'], 16))
        self.assertTrue(chosen[0])
        self.assertEqual(chosen[1], 632)
        with self.assertRaisesRegex(ValueError, 'crosses next candidate boundary'):
            m.compile_candidate(code, 'func_08002500', a, a + 630, table,
                                target_end=int(p.by_start[a]['end'], 16))

    @unittest.skipUnless(m.toolchain_ready(), 'matching compiler unavailable')
    def test_library_copy_requires_noninterworking_return(self):
        p = m.draft.Program()
        a = 0x08018E1C
        code = Path('src/generated/func_08018E1C.c').read_text()
        table = m.reloc.symbols(p)
        chosen = m.compile_candidate(code, 'func_08018E1C', a, a + 96, table,
                                     target_end=a + 94, compiler='old-no-interwork')
        self.assertTrue(chosen[0])
        self.assertEqual(chosen[1], 94)
        default = m.compile_candidate(code, 'func_08018E1C', a, a + 100, table,
                                      target_end=a + 94)
        self.assertFalse(default[0])

    @unittest.skipUnless(m.toolchain_ready(), 'matching compiler unavailable')
    def test_clear_loop_requires_recorded_optimization_choice(self):
        p = m.draft.Program()
        a = 0x080146F4
        code = Path('src/generated/func_080146F4.c').read_text()
        table = m.reloc.symbols(p)
        chosen = m.compile_candidate(code, 'func_080146F4', a, a + 88, table,
                                     target_end=a + 88, compiler='old-no-gcse')
        self.assertTrue(chosen[0])
        default = m.compile_candidate(code, 'func_080146F4', a, a + 88, table, target_end=a + 88)
        self.assertFalse(default[0])


if __name__ == '__main__': unittest.main()

import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path('tools').resolve()))
import diffhint
import llm_match as m

class DiffHintTests(unittest.TestCase):
    def test_arm_listing_preserves_instruction_width_and_pool(self):
        import struct
        code = struct.pack('<III', 0xe59f0000, 0xe12fff1e, 0x03001234)
        lines = diffhint.listing(code, 0x08001000, mode='arm')
        self.assertEqual(len(lines), 3)
        self.assertIn('ldr', lines[0])
        self.assertIn('bx', lines[1])
        self.assertIn('.word 0x03001234 (literal pool)', lines[2])

    @unittest.skipUnless(m.toolchain_ready(), 'matching compiler unavailable')
    def test_cli_accepts_merged_compiler_profiles(self):
        import contextlib
        import io
        from unittest.mock import patch
        for address, profile in [('08018E1C', 'old-no-interwork'),
                                 ('08017E68', 'arm'), ('08018E88', 'modern-arm')]:
            with self.subTest(profile=profile):
                for override in ([], ['--compiler', profile]):
                    output = io.StringIO()
                    argv = ['diffhint.py', address, 'src/generated/func_%s.c' % address, *override]
                    with patch.object(sys, 'argv', argv), contextlib.redirect_stdout(output):
                        result = diffhint.main()
                    self.assertEqual(result, 0)
                    self.assertIn('Exact byte match.', output.getvalue())

    def test_config_update_preserves_other_sections(self):
        import json
        old = '{"matches": [], "mapping": [{"offset":0,"size":4}]}\n'
        new = m.config_with_matches(old, [{"name": "f", "size": 4}])
        self.assertTrue(new.endswith(', "mapping": [{"offset":0,"size":4}]}\n'))
        self.assertEqual(json.loads(new)['matches'][0]['size'], 4)

    def test_register_and_constant_mismatch(self):
        text = diffhint.hint(b'\x01\x20\x70\x47', b'\x02\x21\x70\x47', 0x08001000)
        self.assertIn('-08001000:', text)
        self.assertIn('+08001000:', text)
        self.assertIn('r0, #1', text)
        self.assertIn('r1, #2', text)

    def test_missing_tail_and_bounded_output(self):
        text = diffhint.hint(b'\x01\x20' * 40, b'\x70\x47', 0x08001000, 4)
        self.assertIn('target 80 bytes, compiled 2 bytes', text)
        self.assertIn('omitted', text)
        self.assertLess(len(text.splitlines()), 12)

    def test_pool_value_is_data(self):
        code = b'\x00\x48\x70\x47\x34\x12\x00\x03'
        self.assertIn('.word 0x03001234 (literal pool)', '\n'.join(diffhint.listing(code, 0x08001000)))
        self.assertIn('Exact byte match', diffhint.hint(code, code, 0x08001000))

    def test_retry_includes_complete_target_extent(self):
        from unittest.mock import patch
        c = m.Candidate(0x08001000, 0x08001008, 0x08001020, True, False)
        with patch.object(m, 'compile_candidate', return_value=(False, 2, '', '0120704700000000', '7047')) as compile:
            ok, feedback = m.try_install(None, {}, c, 'void x(void) {}', False)
        self.assertFalse(ok)
        self.assertEqual(compile.call_args.kwargs['target_end'], c.end)
        self.assertIn('target 8 bytes, compiled 2 bytes', feedback)

    def test_cli_keeps_a_literal_tail_when_trial_is_shorter(self):
        import contextlib
        import io
        from types import SimpleNamespace
        from unittest.mock import patch
        address = 0x08001000
        program = SimpleNamespace(by_start={address: {'mode': 'thumb', 'end': '0x08001004'}},
                                  matched={}, cfg={'scan_end': 0x2000})
        output = io.StringIO()
        argv = ['diffhint.py', '08001000', 'trial.c', '--compiler', 'old-no-gcse']
        with patch.object(sys, 'argv', argv), patch.object(diffhint.draft, 'Program', return_value=program), \
             patch.object(diffhint.draft, 'pool_words', return_value={address+4: 0x03001234}), \
             patch.object(m.reloc, 'symbols', return_value={}), patch.object(Path, 'read_text', return_value='void f(void) {}'), \
             patch.object(m, 'compile_candidate', return_value=(False, 2, '', '0048704734120003', '7047')) as compile, \
             contextlib.redirect_stdout(output):
            result = diffhint.main()
        self.assertEqual(result, 1)
        self.assertEqual(compile.call_args.kwargs['target_end'], address+8)
        self.assertEqual(compile.call_args.kwargs['compiler'], 'old-no-gcse')
        self.assertIn('target 8 bytes, compiled 2 bytes', output.getvalue())

    @unittest.skipUnless(m.toolchain_ready(), 'matching compiler unavailable')
    def test_cli_uses_the_installed_nondefault_profile(self):
        import contextlib
        import io
        from unittest.mock import patch
        output = io.StringIO()
        argv = ['diffhint.py', '080146F4', 'src/generated/func_080146F4.c']
        with patch.object(sys, 'argv', argv), contextlib.redirect_stdout(output):
            result = diffhint.main()
        self.assertEqual(result, 0)
        self.assertIn('Exact byte match.', output.getvalue())

    @unittest.skipUnless(m.toolchain_ready(), 'matching compiler unavailable')
    def test_curated_examples_reproduce_installed_spans(self):
        p = m.draft.Program()
        table = m.reloc.symbols(p)
        examples = list(Path('tools/fewshot').glob('*.c'))
        self.assertGreaterEqual(len(examples), 21)
        for path in examples:
            address = int(path.stem.split('_')[-1], 16)
            record = p.matched[address]
            with self.subTest(function=path.stem):
                result = m.compile_candidate(path.read_text(), path.stem, address,
                                             address + record['size'], table, target_end=address + record['size'], compiler=record.get('compiler', 'old'))
                self.assertTrue(result[0])
                self.assertEqual(result[1], record['size'])
                self.assertTrue(path.with_suffix('.md').exists())

    def test_ready_callees_are_prioritised_and_sizes_ordered(self):
        p = m.draft.Program()
        p.matched.pop(0x0801604C, None)
        p.matched[0x0800761C] = {}
        candidates = m.candidates(p)
        target = next(c for c in candidates if c.start == 0x0801604C)
        self.assertTrue(target.callees_matched)
        keys = [(not c.real, not c.callees_matched, c.size, c.start) for c in candidates]
        self.assertEqual(keys, sorted(keys))

    def test_prompt_loads_curated_notes_and_extern_globals(self):
        p = m.draft.Program()
        a = 0x0801604C
        c = m.Candidate(a, int(p.by_start[a]['end'], 16), a+128, True, False)
        prompt = m.build_prompt(p, c)
        self.assertIn('extern u8 g_03000DE4[];', prompt)
        self.assertIn('five-argument transfer', prompt)
        self.assertIn('func_0800761C', prompt)

class RelocationEdgeTests(unittest.TestCase):
    def test_negative_offsets_rejected(self):
        with self.assertRaises(ValueError):
            m.reloc.relocate(b'\0' * 4, [(-1, 'R_ARM_ABS32', 'g_03000000')], 0x08000000, {})

    def test_unknown_and_nonmemory_symbols_rejected(self):
        for name in ('mystery_03000000', 'g_00000010', 'g_DEADBEEF', 'func_08000000'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                m.reloc.resolve(name, {})

    def test_bl_symbol_addend(self):
        import struct
        # BL placeholder for symbol+2: encoded displacement is -2.
        code = struct.pack('<HH', 0xF7FF, 0xFFFF)
        actual = m.reloc.relocate(code, [(0, 'R_ARM_THM_CALL', 'func_08001000')],
                                  0x08000000, {'func_08001000': (0x08001000, True)})
        listing = m.draft.disassemble_thumb(actual, 0x08000000)
        self.assertIn('0x08001002', listing[0])
        with self.assertRaises(ValueError):
            m.reloc.relocate(b'\0'*4, [(0, 'R_ARM_THM_CALL', 'f')], 0x08000000, {'f': (0x08001000, True)})

    @unittest.skipUnless(m.toolchain_ready(), 'matching compiler unavailable')
    def test_excludes_section_padding_after_compiler_size(self):
        p = m.draft.Program()
        address = 0x0801474C
        code = Path('src/generated/func_0801474C.c').read_text()
        result = m.compile_candidate(code, 'func_0801474C', address, address+66, m.reloc.symbols(p), target_end=address+66)
        self.assertTrue(result[0])
        self.assertEqual(result[1], 66)

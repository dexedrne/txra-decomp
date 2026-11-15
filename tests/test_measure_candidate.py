"""Admission and private-data regressions for retained comparison evidence."""
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.path[:0] = ['tools', 'recomp']
import llm_match
import measure_candidate as measure


class EvidenceTests(unittest.TestCase):
    def test_encoding_columns_and_pool_contents_are_removed(self):
        listing = ('-08000000: F000F800 bl 0x08000004\n'
                   '+08000002: 1234    movs r0, #1\n'
                   ' 08000004: E1A00000  mov r0, r0\n'
                   ' 08000008: .word 0x12345678 (literal pool)')
        with patch.object(measure.diffhint, 'hint', return_value=listing):
            result = measure.sanitized_diff(b'', b'', 0x08000000, 'thumb')
        self.assertIn('bl 0x08000004', result)
        self.assertIn('movs r0, #1', result)
        for private_column in ('F000F800', '1234 ', 'E1A00000', '0x12345678'):
            self.assertNotIn(private_column, result)

    @unittest.skipUnless(llm_match.toolchain_ready(), 'historical compiler unavailable')
    def test_oversized_diagnostic_cannot_relax_checker_limit(self):
        # All-zero synthetic memory is deliberately unrelated to any cartridge.
        # The compiler emits a real C store; no instruction bytes are supplied.
        start, end = 0x08000000, 0x08000002
        program = SimpleNamespace(rom=bytes(64))
        code = 'void func_08000000(void) { *(volatile unsigned *)0x04000000 = 1; }\n'
        with tempfile.TemporaryDirectory() as td:
            source = Path(td) / 'candidate.c'
            source.write_text(code)
            with patch.object(measure.draft, 'Program', return_value=program), \
                    patch.object(measure.reloc, 'symbols', return_value={}), \
                    patch.object(measure.match, 'compile_candidate',
                                 wraps=llm_match.compile_candidate) as checker:
                result = measure.measure(source, start, end, 'old')
        self.assertEqual(checker.call_count, 1)
        self.assertEqual(checker.call_args.args[3], end)
        self.assertEqual(result['checker_limit'], '08000002')
        self.assertEqual(result['checker_rejection'], 'output crosses next candidate boundary')
        self.assertGreater(result['emitted_bytes'], result['target_bytes'])
        self.assertFalse(result['exact'])
        self.assertFalse(result['installed'])

    def test_other_checker_failures_are_not_reported_as_nonmatches(self):
        with tempfile.TemporaryDirectory() as td:
            source = Path(td) / 'candidate.c'
            source.write_text('void func_08000000(void) {}\n')
            with patch.object(measure.draft, 'Program', return_value=SimpleNamespace(rom=bytes(64))), \
                    patch.object(measure.reloc, 'symbols', return_value={}), \
                    patch.object(measure, 'diagnostic_compile', return_value=(bytes(4), 0)), \
                    patch.object(measure.match, 'compile_candidate',
                                 side_effect=ValueError('unknown symbol')):
                with self.assertRaisesRegex(ValueError, 'unknown symbol'):
                    measure.measure(source, 0x08000000, 0x08000010, 'old')


if __name__ == '__main__':
    unittest.main()

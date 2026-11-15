import struct
import sys
import unittest
from pathlib import Path

sys.path[:0] = ['tools', 'recomp']
import llm_match as match
import reloc


class ArmMarkerTests(unittest.TestCase):
    def test_bx_marker_preserves_original_instruction(self):
        for register in (0, 12, 14):
            instruction = struct.pack('<I', 0xE12FFF10 | register)
            self.assertEqual(reloc.relocate(instruction, [(0, 'R_ARM_V4BX', '*ABS*')],
                                            0x08001000, {}), instruction)

    def test_malformed_bx_marker_is_rejected(self):
        for instruction, offset, start, symbol in (
            (0, 0, 0x08001000, '*ABS*'),
            (0xE12FFF1E, 0, 0x08001002, '*ABS*'),
            (0xE12FFF1E, 0, 0x08001000, 'unknown'),
            (0xE12FFF1E, 1, 0x08001000, '*ABS*'),
        ):
            with self.subTest(offset=offset, start=start, symbol=symbol):
                with self.assertRaises(ValueError):
                    reloc.relocate(struct.pack('<I', instruction),
                                   [(offset, 'R_ARM_V4BX', symbol)], start, {})


@unittest.skipUnless(match.toolchain_ready() and match.CC.with_name('agbcc_arm').exists()
                     and Path('baserom.gba').exists(), 'ARM matching compiler or private ROM unavailable')
class ArmCompilerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.program = match.draft.Program()
        cls.symbols = reloc.symbols(cls.program)
        cls.source = Path('src/generated/func_08017E68.c').read_text()

    def compile(self, source, limit=0x08017F64):
        return match.compile_candidate(source, 'func_08017E68', 0x08017E68,
                                       limit, self.symbols, target_end=0x08017F64,
                                       compiler='arm')

    def test_complete_arm_body_and_pools_match(self):
        equal, size, emitted, expected, actual = self.compile(self.source)
        self.assertTrue(equal)
        self.assertEqual(size, 252)
        self.assertEqual(expected, actual)
        self.assertIn('bx', emitted)

    def test_changed_source_does_not_match(self):
        changed = self.source.replace('g_03005F4C = 0;', 'g_03005F4C = 1;')
        self.assertNotEqual(changed, self.source)
        self.assertFalse(self.compile(changed)[0])

    def test_arm_boundary_is_enforced(self):
        with self.assertRaises(ValueError):
            self.compile(self.source, 0x08017F60)


if __name__ == '__main__':
    unittest.main()

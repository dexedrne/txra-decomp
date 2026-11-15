"""ARM tail branches must retain their complete extent and resolve like the linker."""
import struct
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
import llm_match as match


class ArmBranchRelocations(unittest.TestCase):
    def resolve(self, word, start, target, kind='R_ARM_JUMP24', thumb=False):
        return struct.unpack('<I', match.reloc.relocate(
            struct.pack('<I', word), [(0, kind, 'target')], start,
            {'target': (target, thumb)}))[0]

    def test_backward_tail_branch(self):
        word = self.resolve(0xEAFFFFFE, 0x08018E88, 0x08018854)
        displacement = ((0x08018854 - 0x08018E88 - 8) >> 2) & 0xFFFFFF
        self.assertEqual(word, 0xEA000000 | displacement)

    def test_forward_call_preserves_condition_and_symbol_addend(self):
        # Placeholder -4 means symbol +4, relative to the ARM PC bias of eight.
        word = self.resolve(0x1BFFFFFF, 0x08001000, 0x08002000, 'R_ARM_CALL')
        self.assertEqual(word, 0x1B0003FF)

    def test_legacy_pc24_branch(self):
        self.assertEqual(self.resolve(0xEAFFFFFE, 0x08001000, 0x08001008,
                                      'R_ARM_PC24'), 0xEA000000)

    def test_arm7_bx_compatibility_hint_preserves_only_bx(self):
        code = struct.pack('<I', 0xE12FFF1E)
        self.assertEqual(match.reloc.relocate(code, [(0, 'R_ARM_V4BX', '*ABS*')],
                                             0x08001000, {}), code)
        with self.assertRaisesRegex(ValueError, 'compatibility'):
            match.reloc.relocate(b'\0' * 4, [(0, 'R_ARM_V4BX', '*ABS*')], 0x08001000, {})

    def test_rejects_wrong_instruction_or_link_bit(self):
        for word, kind in [(0, 'R_ARM_JUMP24'), (0xFAFFFFFE, 'R_ARM_CALL'),
                           (0xEBFFFFFE, 'R_ARM_JUMP24'), (0xEAFFFFFE, 'R_ARM_CALL')]:
            with self.subTest(word=word, kind=kind), self.assertRaises(ValueError):
                self.resolve(word, 0x08001000, 0x08002000, kind)

    def test_rejects_mode_alignment_and_range_errors(self):
        for start, target, thumb in [(0x08001000, 0x08002000, True),
                                     (0x08001002, 0x08002000, False),
                                     (0x08001000, 0x08002002, False),
                                     (0x08001000, 0x0C002000, False)]:
            with self.subTest(start=start, target=target), self.assertRaises(ValueError):
                self.resolve(0xEAFFFFFE, start, target, thumb=thumb)


@unittest.skipUnless(match.toolchain_ready(), 'matching compiler unavailable')
class ArmCompilerMatch(unittest.TestCase):
    SOURCE = '''
extern void arm_func_08018854(void);
void func_08018E88(void)
{
    arm_func_08018854();
}
'''

    def test_complete_tail_thunk_and_boundary(self):
        prog = match.draft.Program()
        start = 0x08018E88
        result = match.compile_candidate(self.SOURCE, 'func_08018E88', start, start + 4,
                                         match.reloc.symbols(prog), target_end=start + 4,
                                         compiler='modern-arm')
        self.assertTrue(result[0])
        self.assertEqual(result[1], 4)
        self.assertEqual(bytes.fromhex(result[4]), prog.rom[start-match.BASE:start-match.BASE+4])
        different = match.compile_candidate('u32 func_08018E88(u32 a) { return a + 1; }',
                                            'func_08018E88', start, start + 16,
                                            match.reloc.symbols(prog), compiler='modern-arm')
        self.assertFalse(different[0])
        with self.assertRaisesRegex(ValueError, 'boundary'):
            match.compile_candidate(self.SOURCE, 'func_08018E88', start, start + 2,
                                    match.reloc.symbols(prog), compiler='modern-arm')

    def test_tail_relocation_agrees_with_linker(self):
        with tempfile.TemporaryDirectory(dir=ROOT / 'build', prefix='arm-reference-') as tmp:
            folder = Path(tmp)
            source, obj = folder / 'tail.c', folder / 'tail.o'
            source.write_text(self.SOURCE)
            match.run([match.ARM + 'gcc', '-c', '-O2', '-marm', '-mcpu=arm7tdmi',
                       '-mno-thumb-interwork', source, '-o', obj])
            match.run([match.ARM + 'objcopy', '-O', 'binary', '-j', '.text', obj, folder / 'raw.bin'])
            raw = (folder / 'raw.bin').read_bytes()
            table = {'arm_func_08018854': (0x08018854, False)}
            relocated = match.reloc.link_bytes(obj, raw, 0x08018E88, table, match.ARM + 'objdump')
            match.run([match.ARM + 'ld', '-Ttext=0x08018E88', '--entry=func_08018E88',
                       '--defsym=arm_func_08018854=0x08018854', obj, '-o', folder / 'linked.elf'])
            match.run([match.ARM + 'objcopy', '-O', 'binary', '-j', '.text',
                       folder / 'linked.elf', folder / 'linked.bin'])
            self.assertEqual(relocated, (folder / 'linked.bin').read_bytes())

    def test_arm_alias_does_not_replace_thumb_runtime_alias(self):
        table = match.reloc.symbols(match.draft.Program())
        self.assertEqual(table['arm_func_08018854'], (0x08018854, False))
        self.assertEqual(table['func_08018854'], (0x08018E84, True))


if __name__ == '__main__':
    unittest.main()

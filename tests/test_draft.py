"""Lifted drafts and directly generated leaves, checked against the private ROM."""
import re
import sys
import unittest
from pathlib import Path
sys.path.insert(0, 'recomp')
sys.path.insert(0, 'tools')
import draft
import generate
import leafgen

PROG = draft.Program()

class DraftTests(unittest.TestCase):
    def test_division_veneer_draft_retains_call_arguments(self):
        text = draft.draft(PROG, 0x0800AC3C)
        self.assertIn('__divsi3(r0, r1)', text)
        self.assertIn('r1 = 0x64;', text)
        self.assertIn('r1 = 0xC;', text)
        self.assertNotIn('__divsi3()', text)

    def test_arm_multiply_add_keeps_accumulator_and_aliasing_reads(self):
        # Construct MLA r4,r4,r2,r1, with flags, from the ISA fields.
        word = 0xE0000090 | (1 << 21) | (1 << 20) | (4 << 16) | (1 << 12) | (2 << 8) | 4
        text, ir, flags, cond = draft.arm_ir(generate.decode(word, False, 0x08001000), 0x08001000, word)
        self.assertEqual(text, 'mlas r4, r4, r2, r1')
        self.assertEqual(draft.uses(ir), ([4, 2, 1], [4]))
        self.assertTrue(flags)
        self.assertEqual(cond, 14)
        lifter = draft.Lifter(PROG, 0x080147C0)
        insn = draft.Insn(0x08001000, 4, word, text, ir, cond, flags)
        self.assertEqual(lifter.statement(insn, 0, None), 'r4 = r4 * r2 + r1;')

    def test_arm_shifted_subtraction_and_address_preserve_precedence(self):
        lifter = draft.Lifter(PROG, 0x080147C0)
        ir = ('alu', 3, 'sub', ('shift', 3, 'lsl', draft.imm(3)), 3)
        insn = draft.Insn(0x08001000, 4, 0, '', ir)
        self.assertEqual(lifter.statement(insn, 0, None), 'r3 = (r3 << 3) - r3;')
        self.assertEqual(lifter.address(2, ('shift', 3, 'lsl', draft.imm(2)), 4),
                         '*(u32 *)(r2 + (r3 << 2))')

    def test_arm_literal_load_uses_pc_plus_eight_in_both_directions(self):
        for up in (0, 1):
            # LDR r4,[pc,+/-20].
            word = 0xE51F4014 | (up << 23)
            _, ir, _, _ = draft.arm_ir(generate.decode(word, False, 0x08001000), 0x08001000, word)
            self.assertEqual(ir, ('pool', 4, 0x08001008 + (20 if up else -20)))

    def test_every_recompiled_thumb_statement_is_lifted(self):
        for addr, f in PROG.by_start.items():
            if f['mode'] != 'thumb': continue
            for i in PROG.insns[addr]:
                if i.ir[0] == 'unknown':
                    # Only instructions the recompiler itself leaves unsupported may stay opaque.
                    self.assertIn('unsupported', generate.decode(i.raw, True, i.addr), i)

    def test_listing_agrees_with_raw_byte_disassembler(self):
        addr = 0x08015D78  # one span: no data between instructions
        listing = [l.split(None, 2)[2] for l in draft.disassembly(PROG, addr).splitlines()]
        raw = draft.disassemble_thumb(PROG.rom[addr - draft.BASE:addr - draft.BASE + PROG.size(addr)], addr)
        self.assertEqual([re.sub(r' \(0x[0-9A-F]+\)| <\w+>', '', l) for l in listing], [r.split(None, 2)[2] for r in raw])

    def test_known_drafts(self):
        text = draft.draft(PROG, 0x080147C0)
        self.assertIn('u32 func_080147C0(void) {', text)
        self.assertIn('r0 = *(vu32 *)0x04000128 /* REG_SIOCNT */;', text)
        self.assertNotIn('r0 = 0x04000128', text)  # constant used only as an address is folded away
        text = draft.draft(PROG, 0x0800D188)
        self.assertIn('void func_0800D188(u32 r0) {', text)
        self.assertIn('*(u32 *)0x030014A4 /* IWRAM */ = r1;', text)

    def test_flags_folded_and_structured(self):
        text = draft.draft(PROG, 0x08015200)
        self.assertIn('if (r3 < r0) {', text)
        self.assertIn('} while (r3 < r0);', text)
        self.assertNotIn('FLAGS_', text)
        text = draft.draft(PROG, 0x08005E84)
        self.assertIn('r4 = (u16)r6;', text)
        self.assertIn('r0 = func_08018B24(r0, r1);', text)
        self.assertIn('r0 = 0x200;', text)
        self.assertNotIn('r8 = r3', text)  # high-register save/restore is frame bookkeeping
        thumb_flags = [a for a, f in PROG.by_start.items() if f['mode'] == 'thumb' and 'FLAGS_' in draft.draft(PROG, a)]
        self.assertEqual(thumb_flags, [])

    def test_structure_requires_single_entry(self):
        lifter = draft.Lifter(PROG, 0x08015200)
        lines = [('goto', 0x10, 'x', 0, None), ('stmt', 'a;'), ('label', 0x10), ('stmt', 'b;')]
        self.assertEqual(draft.structure(lines, lifter)[0][0], 'if')
        shared = lines + [('goto', 0x10, None, 14, None)]
        self.assertEqual(draft.structure(shared, lifter)[0][0], 'goto')

    def test_write_drafts(self):
        n = draft.write_drafts(Path('.'), only={0x080147C0})
        self.assertEqual(n, 1)
        self.assertTrue(Path('build/drafts/func_080147C0.c').exists())

class LeafTests(unittest.TestCase):
    def test_known_matches_regenerated(self):
        self.assertIn('    return (*(vu32 *)0x04000128 & 0x30) >> 4;\n', leafgen.generate(PROG, 0x080147C0)[0])
        self.assertIn('void func_08015DA4(void)\n{\n}\n', leafgen.generate(PROG, 0x08015DA4))
        self.assertTrue(any('    *(u32 *)0x03002184 = 0;\n' in v for v in leafgen.generate(PROG, 0x08014518)))
        self.assertTrue(any('void func_0800D188(u32 a0)' in v for v in leafgen.generate(PROG, 0x0800D188)))

    def test_branching_functions_left_to_the_model(self):
        self.assertEqual(leafgen.generate(PROG, 0x08015200), [])

    def test_value_read_once(self):
        v = leafgen.generate(PROG, 0x08015D78)[0]
        self.assertEqual(v.count('0x04000130'), 1)

    def test_calls_and_signed_division(self):
        v = leafgen.generate(PROG, 0x08014250)[0]
        self.assertIn('extern void func_0800EDF4(u32, u32);', v)
        self.assertIn('    func_0800EDF4(a0, a1);\n', v)
        self.assertIn('(s32)a2 / 2', leafgen.generate(PROG, 0x08014420)[0])

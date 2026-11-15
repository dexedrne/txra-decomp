"""Synthetic instruction fixtures for the finishing audits; no cartridge bytes."""
import struct
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path('tools').resolve()))
import asm_interfaces  # noqa: E402
import map_completeness  # noqa: E402

B = 0x08000000


def thumb(*halfwords):
    return struct.pack('<%dH' % len(halfwords), *halfwords)


def fn(start, end, mode='thumb'):
    return {'start': '0x%08X' % (B+start), 'end': '0x%08X' % (B+end), 'mode': mode,
            'spans': [['0x%08X' % (B+start), '0x%08X' % (B+end)]]}


class AsmInterfaceTests(unittest.TestCase):
    def test_register_call_veneer(self):
        rom = thumb(0x4718, 0x46C0)                     # bx r3; nop
        props = asm_interfaces.measure(rom, fn(0, 2))
        ok, text = asm_interfaces.expected('assembly-interface', 'register-call-veneer', props, B)
        self.assertTrue(ok)
        self.assertIn('bx r3', text)

    def test_bios_veneer(self):
        rom = thumb(0xDF0B, 0x4770)                     # svc 0x0B; bx lr
        props = asm_interfaces.measure(rom, fn(0, 4))
        self.assertEqual(props['swi'], [0x0B])
        self.assertTrue(asm_interfaces.expected('assembly-interface', 'bios-veneer', props, B)[0])

    def test_ordinary_leaf_is_not_a_veneer_or_private_abi(self):
        rom = thumb(0x1840, 0x4770)                     # adds r0, r0, r1; bx lr
        props = asm_interfaces.measure(rom, fn(0, 4))
        self.assertFalse(asm_interfaces.expected('assembly-interface', 'register-call-veneer', props, B)[0])
        self.assertFalse(asm_interfaces.expected('assembly-interface', 'renderer-private-abi', props, B)[0])
        self.assertEqual(props['non_abi_live_in_registers'], [])

    def test_live_in_high_register_is_reported(self):
        rom = thumb(0x1C30, 0x4770)                     # adds r0, r6, #0; bx lr  (r6 read before definition)
        props = asm_interfaces.measure(rom, fn(0, 4))
        self.assertEqual(props['non_abi_live_in_registers'], ['r6'])
        self.assertTrue(asm_interfaces.expected('assembly-interface', 'renderer-private-abi', props, B)[0])

    def test_saved_registers_are_not_inputs(self):
        rom = thumb(0xB530, 0x2400, 0x1C20, 0xBC30, 0xBC02, 0x4708)   # push {r4,r5,lr}; movs r4,#0; adds r0,r4,#0; pop; pop {r1}; bx r1
        props = asm_interfaces.measure(rom, fn(0, 12))
        self.assertTrue(props['conventional_frame_at_entry'])
        self.assertEqual(props['non_abi_live_in_registers'], [])


class CodeFeatureTests(unittest.TestCase):
    class Model:
        def __init__(self, rom, entries):
            self.rom, self.size = rom, len(rom)
            self.entries = {(e, 'thumb') for e in entries}
            self.ins_start = {e: 'thumb' for e in entries}

    def test_bl_to_entry_and_returns_are_counted(self):
        # 0: bl +0 -> target 4 ; 4: push {lr}; 6: pop {r0}; 8: bx r0; 10: bx lr
        rom = thumb(0xF000, 0xF800, 0xB500, 0xBC01, 0x4700, 0x4770)
        m = self.Model(rom, [4])
        f = map_completeness.code_features(m, 0, len(rom), set())
        self.assertEqual(f['thumb_bl_hits_entry'], 1)
        self.assertEqual(f['thumb_pop_bx_return'], 1)
        self.assertEqual(f['thumb_bx_lr'], 1)
        self.assertEqual(f['thumb_push_lr'], 1)

    def test_negative_halfword_pairs_do_not_hit_entries(self):
        rom = thumb(*([0xF123, 0xFFF0] * 8))
        m = self.Model(rom, [0x40])
        f = map_completeness.code_features(m, 0, len(rom), set())
        self.assertEqual(f['thumb_bl_hits_entry'], 0)
        self.assertEqual(f['thumb_bx_lr'] + f['thumb_pop_bx_return'], 0)


if __name__ == '__main__':
    unittest.main()

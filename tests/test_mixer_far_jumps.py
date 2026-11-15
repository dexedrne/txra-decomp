import json
from pathlib import Path
import sys
import unittest

OWNER = 0x080064A4
# Thumb long branches inside the sound owner (source -> target). Each spans more
# than the 2 KiB unconditional-branch range; none is a call.
FAR_JUMPS = {
    0x080066EC: 0x08007368, 0x08006700: 0x08007368,
    0x0800672C: 0x0800735C, 0x0800673C: 0x0800735C,
    0x08006F46: 0x08006740, 0x08007358: 0x08006776,
    0x08007364: 0x08006712,
}
INTERIOR = (0x08006712, 0x08006740, 0x08006776, 0x0800735C, 0x08007368)


class MixerFarJumpTests(unittest.TestCase):
    def setUp(self):
        self.cfg = json.loads(Path('tools/rom.cfg').read_text())
        self.functions = json.loads(Path('docs/map/functions.json').read_text())['functions']

    def test_reviewed_far_jumps_belong_to_the_sound_owner(self):
        reviewed = {j['source']: j for j in self.cfg.get('far_jumps', []) if j['owner'] == OWNER}
        self.assertEqual({s: j['target'] for s, j in reviewed.items()}, FAR_JUMPS)
        for source, target in FAR_JUMPS.items():
            self.assertGreater(abs(target - (source + 4)), 2048, 'a local B would reach it')

    def test_interior_labels_are_not_registry_entries(self):
        starts = {int(f['start'], 16) for f in self.functions}
        for address in INTERIOR:
            self.assertNotIn(address, starts)
        owner = next(f for f in self.functions if int(f['start'], 16) == OWNER)
        self.assertEqual(owner['end'], '0x08007378')
        for address in INTERIOR:
            self.assertTrue(any(int(a, 16) <= address < int(z, 16) for a, z in owner['spans']),
                            f'{address:08X} outside the owner extent')

    def test_generated_listing_includes_the_installed_owner(self):
        # The owner is exact C (src/generated/func_080064A4.c): the listing includes
        # its verified leaf, so the far-jump targets are interior addresses of that
        # leaf rather than labels or separate functions.
        listing = Path('asm/program.s').read_text()
        self.assertIn('func_080064A4:\n    .incbin "build/leaves/func_080064A4.bin"\n', listing)
        for address in INTERIOR:
            self.assertNotIn(f'func_{address:08X}', listing)
            self.assertNotIn(f'loc_{address:08X}:', listing)

    def test_lifter_treats_far_jumps_as_gotos(self):
        sys.path.insert(0, str(Path('recomp').resolve()))
        import draft
        program = draft.Program()
        self.assertFalse(program.callees[OWNER] & set(INTERIOR))
        jumps = {i.addr: i.ir for i in program.insns[OWNER] if i.addr in FAR_JUMPS}
        self.assertEqual(jumps, {s: ('b', t) for s, t in FAR_JUMPS.items()})


if __name__ == '__main__':
    unittest.main()

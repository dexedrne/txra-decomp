"""Gap discovery uses synthetic instructions, never cartridge-derived fixtures."""
import struct
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path('tools').resolve()))
from code_gap_audit import scan


class GapAuditTests(unittest.TestCase):
    def inspect(self, words, kind='unknown', splits=(), start=0, end=None):
        rom = struct.pack('<'+'H'*len(words), *words)
        cfg = dict(base=0x08000000, mapping=[dict(offset=0, size=len(rom), type=kind)])
        return scan(rom, cfg, splits, start=start, end=len(rom) if end is None else end)

    def test_leaf_after_alignment_excludes_alignment(self):
        result = self.inspect([0, 0x2103, 0x6001, 0x4770])
        self.assertEqual([c['offset'] for c in result['candidates']], [2])
        self.assertFalse(result['candidates'][0]['execution_verified'])
        self.assertIn('unreferenced', result['candidates'][0]['reason'])

    def test_framed_leaf_inside_gap(self):
        result = self.inspect([0xFFFF, 0xFFFF, 0xB081, 0x2102, 0x9100, 0xB001, 0x4770])
        self.assertEqual([c['offset'] for c in result['candidates']], [4])

    def test_data_partition_is_not_scanned(self):
        self.assertEqual(self.inspect([0x2103, 0x6001, 0x4770], kind='data')['tested'], 0)

    def test_existing_body_is_not_adopted_through_fallthrough(self):
        splits = [dict(start='0x08000004', end='0x08000008', kind='thumb')]
        self.assertFalse(self.inspect([0x2103, 0x6001, 0x6001, 0x4770], splits=splits)['candidates'])

    def test_literal_path_is_rejected(self):
        splits = [dict(start='0x08000004', end='0x08000008', kind='literal')]
        self.assertFalse(self.inspect([0x2103, 0x6001, 0x6001, 0x4770], splits=splits)['candidates'])

    def test_scan_bounds_and_invalid_frame(self):
        self.assertEqual(self.inspect([0xB081, 0x2103, 0x4770])['candidates'], [])
        self.assertEqual(self.inspect([0x2103, 0x6001, 0x4770], start=8)['tested'], 0)


if __name__ == '__main__':
    unittest.main()

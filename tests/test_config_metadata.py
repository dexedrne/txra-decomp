"""Matching updates must retain reviewed mapping and indirect-call evidence."""
import json
import unittest
from collections import Counter
from pathlib import Path


class ConfigMetadataTests(unittest.TestCase):
    def test_partition_agrees_with_reviewed_coverage(self):
        cfg = json.loads(Path('tools/rom.cfg').read_text())
        report = json.loads(Path('docs/map/coverage.json').read_text())
        self.assertEqual(cfg['sha1'], report['rom_sha1'])
        self.assertIn('mapping', cfg)
        counts = Counter()
        end = 0
        for block in cfg['mapping']:
            self.assertEqual(block['offset'], end)
            self.assertGreater(block['size'], 0)
            end += block['size']
            counts[block['type']] += block['size']
        self.assertEqual(end, cfg['size'])
        self.assertEqual(dict(counts), report['classified_bytes'])

    def test_reviewed_veneer_call_has_a_regeneratable_config_entry(self):
        cfg = json.loads(Path('tools/rom.cfg').read_text())
        report = json.loads(Path('docs/map/indirect.json').read_text())
        call = next(c for c in report['veneer_calls'] if c['source'] == '0x080065CC')
        entry = next((c for c in cfg.get('known_indirect_calls', [])
                      if c['source'] == int(call['source'], 16)), None)
        self.assertIsNotNone(entry, 'reviewed call would disappear on regeneration')
        self.assertEqual(entry['target'], int(call['target'], 16))
        self.assertEqual(entry['pointer_slot'], int(call['pointer_slot'], 16))

    def test_reviewed_far_jump_keeps_the_hud_epilogue_in_its_owner(self):
        cfg = json.loads(Path('tools/rom.cfg').read_text())
        jump = next(j for j in cfg.get('far_jumps', []) if j['source'] == 0x08004232)
        self.assertEqual((jump['target'], jump['owner']), (0x080051FE, 0x0800421C))
        functions = json.loads(Path('docs/map/functions.json').read_text())['functions']
        self.assertNotIn('0x080051FE', {f['start'] for f in functions})
        owner = next(f for f in functions if f['start'] == '0x0800421C')
        self.assertEqual(owner['end'], '0x0800520E')
        self.assertTrue(any(int(a, 16) <= 0x080051FE < int(z, 16) for a, z in owner['spans']))

    def test_reviewed_far_jumps_fold_epilogue_and_tail_labels_into_matched_owners(self):
        cfg = json.loads(Path('tools/rom.cfg').read_text())
        functions = json.loads(Path('docs/map/functions.json').read_text())['functions']
        starts = {f['start'] for f in functions}
        jumps = {j['source']: j for j in cfg.get('far_jumps', [])}
        for source, target, owner in ((0x08008B08, 0x080095C4, 'func_08008A88'),
                                      (0x08008C76, 0x080095C4, 'func_08008A88'),
                                      (0x0800E3DC, 0x0800D960, 'func_0800D51C')):
            self.assertEqual(jumps[source]['target'], target)
            match = next(m for m in cfg['matches'] if m['name'] == owner)
            low, high = cfg['base'] + match['offset'], cfg['base'] + match['offset'] + match['size']
            self.assertEqual(jumps[source]['owner'], low)
            self.assertTrue(low < source < high and low < target < high,
                            'far jump must stay inside its installed exact owner')
            self.assertNotIn(f'0x{target:08X}', starts, 'far-jump label listed as an entry')
            entry = next(f for f in functions
                         if any(int(a, 16) <= source < int(z, 16) for a, z in f['spans']))
            self.assertTrue(any(int(a, 16) <= target < int(z, 16) for a, z in entry['spans']),
                            'registry extent does not run through the far-jump label')

    def test_interior_labels_stay_inside_their_matched_owner(self):
        cfg = json.loads(Path('tools/rom.cfg').read_text())
        functions = json.loads(Path('docs/map/functions.json').read_text())['functions']
        starts = {int(f['start'], 16) - cfg['base']: f for f in functions}
        for label in cfg.get('interior_labels', []):
            owner = next(m for m in cfg['matches'] if m['name'] == label['owner'])
            self.assertLess(owner['offset'], label['offset'])
            self.assertLess(label['offset'], owner['offset'] + owner['size'])
            self.assertNotIn(label['offset'], starts, 'interior label listed as an entry')
            entry = starts[owner['offset']]
            address = cfg['base'] + label['offset']
            self.assertTrue(any(int(a, 16) <= address < int(z, 16) for a, z in entry['spans']),
                            'owner extent does not run through its interior label')

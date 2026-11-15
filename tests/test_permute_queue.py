import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'tools'))
import permute_queue as q


class PermuteQueueTests(unittest.TestCase):
    def setUp(self):
        self.functions = [dict(start='%08X' % a, end='%08X' % (a + 16), mode='arm')
                          for a in (0x08001000, 0x08001008, 0x08002000, 0x08003000)]
        self.config = {'matches': [{'offset': 0x1000, 'size': 16}]}

    def test_excludes_matches_and_covered_entries_for_every_input_order(self):
        for candidates in (None, ['08001008', '08003000', '08001000', '08002000']):
            self.assertEqual([r['address'] for r in q.queue(self.config, self.functions, candidates)],
                             ['08002000', '08003000'])
        # A new match is picked up on the next round without editing the target list.
        self.config['matches'].append({'offset': 0x2000, 'size': 16})
        self.assertEqual([r['address'] for r in q.queue(self.config, self.functions)], ['08003000'])

    def test_lowest_score_across_snapshots_ranks_before_untried(self):
        scores = q.best_scores([{'08003000': 800, '08001000': 0},
                               [{'address': '08003000', 'best_score': 606}]])
        rows = q.queue(self.config, self.functions, scores=scores)
        self.assertEqual([r['address'] for r in rows], ['08003000', '08002000'])
        self.assertEqual(rows[0]['best_score'], [606])
        self.assertIsNone(rows[1]['best_score'])

    def test_ties_use_byte_score_then_size_then_address(self):
        scores = q.best_scores([{'08002000': [4, 10], '08003000': {'score': [4, 9]}}])
        rows = q.queue(self.config, self.functions, scores=scores)
        self.assertEqual([r['address'] for r in rows], ['08003000', '08002000'])

    def test_rejects_unknown_targets_and_invalid_scores(self):
        with self.assertRaises(ValueError):
            q.queue(self.config, self.functions, ['08009999'])
        for value in (-1, float('inf'), True, '606'):
            with self.assertRaises(ValueError):
                q.best_scores([{'08003000': value}])

    def test_current_inventory_never_queues_any_installed_match(self):
        config = json.loads((ROOT / 'tools/rom.cfg').read_text())
        functions = json.loads((ROOT / 'docs/map/functions.json').read_text())['functions']
        rows = q.queue(config, functions)
        matched = {'%08X' % (q.BASE + m['offset']) for m in config['matches']}
        self.assertFalse(matched.intersection(r['address'] for r in rows))
        # Every queued address also lies outside all installed bodies.
        for row in rows:
            a = int(row['address'], 16)
            self.assertFalse(any(q.BASE + m['offset'] <= a < q.BASE + m['offset'] + m['size']
                                 for m in config['matches']))


if __name__ == '__main__':
    unittest.main()

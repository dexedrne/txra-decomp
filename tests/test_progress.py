"""Progress must reflect the current config even when saved counters are stale."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class ProgressTests(unittest.TestCase):
    def test_recompute_matches_preserves_search_counters(self):
        script = Path('tools/progress.py').resolve()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'tools').mkdir()
            (root / 'docs/map').mkdir(parents=True)
            cfg = {'size': 100, 'mapping': [{'offset': 0, 'size': 100, 'type': 'code'}],
                   'matches': [{'offset': 0, 'size': 10}, {'offset': 20, 'size': 15}]}
            (root / 'tools/rom.cfg').write_text(json.dumps(cfg))
            for name, value in {'functions': {'functions': []}, 'pointers': {'switches': []},
                                'indirect': {'transfers': []}}.items():
                (root / f'docs/map/{name}.json').write_text(json.dumps(value))
            previous = {'functions_matched_c': {'count': 999}, 'functions_c_matched': 999,
                        'llm_attempts': 3662, 'llm_requests': 3425,
                        'match10_search': {'targets_completed': 15},
                        'deep_hand_b': {'exact_replacements_added': 1}}
            (root / 'progress.json').write_text(json.dumps(previous))
            subprocess.run([sys.executable, str(script)], cwd=root, check=True, capture_output=True)
            result = json.loads((root / 'progress.json').read_text())
            self.assertEqual(result['functions_matched_c'], {
                'count': 2, 'bytes_including_pools': 25, 'percent_of_mapped_code': 25.0})
            self.assertEqual(result['functions_c_matched'], 2)
            for key in ('llm_attempts', 'llm_requests', 'match10_search', 'deep_hand_b'):
                self.assertEqual(result[key], previous[key])


class CompletionTests(unittest.TestCase):
    def test_assembly_is_counted_separately_from_c(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location('progress', Path('tools/progress.py'))
        progress = importlib.util.module_from_spec(spec); spec.loader.exec_module(progress)
        fs = [{'start': '0x%08X' % (0x08000000+o)} for o in (0, 0x10, 0x20, 0x30, 0x40, 0x50)]
        cfg = {'base': 0x08000000, 'matches': [{'offset': 0, 'size': 16}, {'offset': 0x20, 'size': 4}]}
        finish = {'entries': [
            {'start': '0x08000010', 'class': 'assembly-interface', 'instruction_bytes': 2,
             'code_references': {}, 'data_slot_references': {}},
            {'start': '0x08000030', 'class': 'covered-by-installed-owner', 'instruction_bytes': 8},
            {'start': '0x08000040', 'class': 'C-candidate', 'instruction_bytes': 40, 'owner_bytes_including_pools': 48},
            {'start': '0x08000050', 'class': 'fragment-of-owner', 'instruction_bytes': 6}]}
        out = progress.completion(fs, cfg, finish, {'0x08000010'})
        self.assertEqual(out['exact_c_entries'], 2)
        self.assertEqual(out['documented_assembly_interfaces'], 1)
        self.assertEqual(out['complete_entries'], 4)
        self.assertEqual(out['remaining_entries'], 2)
        self.assertEqual(out['remaining_c_owner_bytes_including_pools'], 48)
        self.assertEqual(out['indirect_sites_unresolved_but_unreferenced'], 1)

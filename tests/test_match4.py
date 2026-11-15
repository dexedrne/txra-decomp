import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0, str(Path('tools').resolve()))
import diffhint
import llm_match as m
import rank_targets
import reloc


class RoundFourTests(unittest.TestCase):
    def test_diff_localizes_changes_and_missing_bytes(self):
        text = diffhint.hint(bytes.fromhex('01207047'), bytes.fromhex('02207047'), 0x08001000)
        self.assertIn('exact prefix 0 bytes, exact suffix 3 bytes', text)
        text = diffhint.hint(bytes.fromhex('01207047'), bytes.fromhex('0120'), 0x08001000)
        self.assertIn('0x08001002', text)
        self.assertIn('Length differs by -2 bytes', text)

    def test_register_only_diff_keeps_constants_significant(self):
        self.assertIn('Instruction shapes', diffhint.hint(bytes.fromhex('01207047'), bytes.fromhex('01217047'), 0x08001000))
        self.assertNotIn('Instruction shapes', diffhint.hint(bytes.fromhex('01207047'), bytes.fromhex('02217047'), 0x08001000))

    def test_missing_dynamic_counts_are_not_session_totals(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root/'coverage.json').write_text(json.dumps({'sessions': [{'semantic_entries': 99}]}))
            self.assertEqual(rank_targets.coverage_evidence(root), ({}, None))
            (root/'coverage.json').write_text(json.dumps({'function_call_counts': {'0x08001000': 37}}))
            (root/'round9-audit.json').write_text(json.dumps({'mapped_function_entries_unexecuted': [{'start': '0x08001000'}]}))
            (root/'round10-audit.json').write_text(json.dumps({'mapped_function_entries_unexecuted': [{'start': '0x08002000'}]}))
            self.assertEqual(rank_targets.coverage_evidence(root), ({0x08001000: 37}, {0x08002000}))

    def test_rank_excludes_matches_and_flags_epilogues(self):
        p = m.draft.Program()
        actual = rank_targets.rank(p, {}, set())
        self.assertTrue(all(int(r['address'], 16) not in p.matched for r in actual))
        # Test ranking against a stable standalone fixture even after it lands.
        p.matched.pop(0x08014614, None)
        # 08015128 is matched C (an uninitialised local), but still exercises
        # the high-register live-in hint.
        p.matched.pop(0x08015128, None)
        rows = rank_targets.rank(p, {0x08014614: 100}, set())
        by_address = {r['address']: r for r in rows}
        self.assertNotIn('08013B38', by_address)
        self.assertEqual(rows[0]['address'], '08014614')
        # A stable blocked entry: the ARM IRQ epilogue. Long-branch labels such as
        # 08007368 and 080051FE are now interior labels of their owner, not ranked entries.
        self.assertIsNotNone(by_address['080001F4']['blocked_reason'])
        self.assertNotIn('08007368', by_address)
        self.assertNotIn('080051FE', by_address)
        self.assertIsNone(by_address['08014614']['blocked_reason'])
        self.assertIn('read before definition', by_address['08015128']['blocked_reason'])
        # Internal labels of the installed garage loop owner are exact already.
        # 0800D960 and 08007B40 are no longer entries at all (far jump / interior label).
        for label in ('0800D570', '0800D630'):
            self.assertEqual(by_address[label]['blocked_reason'], 'covered by installed func_0800D51C')
        # The second scenery pass of the installed road stream owner.
        self.assertEqual(by_address['08003786']['blocked_reason'], 'covered by installed func_08002854')
        for label in ('0800D960', '08007B40', '080095C4'):
            self.assertNotIn(label, by_address)

    def test_aliases_resolve_to_reviewed_address_identity(self):
        table = reloc.symbols(m.draft.Program())
        for name, address in reloc.DATA_SYMBOLS.items():
            self.assertEqual(reloc.resolve(name, table), (address, False))
            self.assertEqual(reloc.resolve('g_%08X' % address, table), (address, False))

    def test_hard_prompt_explains_boundary_and_local_retry(self):
        p = m.draft.Program()
        a = 0x08014614
        c = m.Candidate(a, a+84, a+88, True, False)
        c.hard = True
        prompt = m.build_prompt(p, c)
        self.assertIn('Hard-mode recovery', prompt)
        self.assertIn('Never invent parameters', prompt)
        self.assertIn('Integer address arithmetic', prompt)


if __name__ == '__main__':
    unittest.main()

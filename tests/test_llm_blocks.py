"""Search control-plane regressions and real historical-profile/semantic checks.

Synthetic proposer answers in these tests are never search/proof attempts.
"""
import hashlib
import json
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

sys.path[:0] = ['tools', 'recomp']
import llm_blocks as b


class RegionTests(unittest.TestCase):
    def test_service_keeps_requests_serial_and_unloads_only_permitted_previous_model(self):
        calls = []
        primary, secondary = b.match.MODELS[:2]

        def request(path, payload=None, timeout=None):
            calls.append((path, payload))
            if path == '/api/ps':
                return {'models': [{'name': primary}]}
            return {'response': 'answer'}

        with tempfile.TemporaryDirectory() as folder, \
                patch.object(b.match.Path, 'home', return_value=Path(folder)), \
                patch.object(b.match, 'request', side_effect=request):
            self.assertEqual(b.match.ask('prompt', secondary, max_wait=0, num_predict=6144), 'answer')
        self.assertEqual(calls[1], ('/api/generate', {'model': primary, 'keep_alive': 0}))
        self.assertEqual(calls[2][1]['model'], secondary)
        self.assertEqual(calls[2][1]['options']['num_predict'], 6144)

    def test_service_never_evicts_or_requests_while_unrelated_model_is_loaded(self):
        with tempfile.TemporaryDirectory() as folder, \
                patch.object(b.match.Path, 'home', return_value=Path(folder)), \
                patch.object(b.match, 'request', return_value={'models': [{'name': 'unrelated-work'}]}) as request:
            with self.assertRaises(b.match.Unavailable):
                b.match.ask('prompt', b.match.MODELS[0], max_wait=0)
        self.assertEqual(request.call_count, 1)

    def test_regions_never_cut_control_pairs_or_for_headers(self):
        code = '''void func_08000000(void) {
    int i;
    if (x) { a(); } else if (y) b(); else c();
    for (i = 0; i < 4; i++) { x += i; }
    do { x--; } while (x);
    while (y) y--;
    x = call("; }", 'x');
}'''
        regions = b.regions(code, 'func_08000000')
        texts = [r['text'] for r in regions]
        self.assertIn('if (x) { a(); } else if (y) b(); else c();', texts)
        self.assertIn('for (i = 0; i < 4; i++) { x += i; }', texts)
        self.assertIn('do { x--; } while (x);', texts)
        self.assertIn('x = call("; }", \'x\');', texts)
        self.assertNotIn('if (x) { a(); }', texts)
        self.assertTrue(all(r['last_line'] - r['first_line'] < 40 for r in regions))

    def test_statement_macros_without_semicolons(self):
        code = '#define STEP(x) \\\n    if (x) { x--; }\nvoid f(void) { STEP(x) STEP(y) z++; }'
        self.assertIn('STEP(x)', [r['text'] for r in b.regions(code, 'f')])

    def test_multiline_and_compact_definition_extraction(self):
        code = 'int a(void) {return 0;}\nstatic unsigned\nother(int value)\n{ return value; }'
        a, _, z = b.function_span(code, 'other')
        self.assertEqual(code[a:z], 'static unsigned\nother(int value)\n{ return value; }')

    def test_rank_rotates_after_worst_and_uses_source_mapping(self):
        code = 'void f(void) {\n x++;\n y++;\n}'
        want, actual = bytes(4), bytes([1, 2, 3, 4])
        locations = [(2, 0, 3), (3, 3, 4)]
        first = b.rank_regions(code, 'f', locations, want, actual, {})
        self.assertEqual(first[0]['different_bytes'], 4)
        visits = {first[0]['identity']: 1}
        second = b.rank_regions(code, 'f', locations, want, actual, visits)
        self.assertNotEqual(first[0]['identity'], second[0]['identity'])

    def test_safety_rejects_non_c_mutations_and_new_effects(self):
        original = 'x = x + 1;'
        for code in ('asm("nop");', '__asm__("nop");', '#define x 1\nx++;',
                     'volatile int a; x++;', 'x = 0xE1A00000;', 'pad = x;',
                     '__builtin_memcpy(x,x,x);', 'new_call();', 'goto other;',
                     'static int x; x++;', 'x = x + 2;'):
            with self.subTest(code=code), self.assertRaises(ValueError):
                b.safe_region(original, code)
        self.assertEqual(b.safe_region(original, '{ int n; n = x; x = n + 1; }'),
                         '{ int n; n = x; x = n + 1; }')

    def test_response_parser_requires_explicit_c_or_json(self):
        self.assertEqual(b.alternatives('Some prose x++;'), [])
        self.assertEqual(b.alternatives('```c\nx++;\n```\n```c\n++x;\n```'), ['x++;\n', '++x;\n'])
        self.assertEqual(b.alternatives('{"alternatives":["a;","b;","c;","d;"]}'),
                         ['a;', 'b;', 'c;', 'd;'])
        self.assertEqual(b.alternatives('{"alternatives":["a;","b;","unterminated'), ['a;', 'b;'])
        self.assertEqual(b.json_array('Some wrapper {"proposals":[{"name":"a"}]} trailing'), [{'name': 'a'}])

    def test_context_follows_type_and_macro_dependencies(self):
        code = '''typedef struct { u32 value; } Node;
extern Node gData;
extern void helper(Node *, u32);
extern int gUnused;
#define APPLY(x) helper(&gData, x)
#define UNUSED(x) x++
void f(void) {
 u32 needed;
 u32 unused;
 APPLY(needed);
}'''
        region = next(r for r in b.regions(code, 'f') if r['text'] == 'APPLY(needed);')
        globals_, locals_ = b.region_declarations(code, 'f', region)
        self.assertIn('typedef struct { u32 value; } Node;', globals_)
        self.assertIn('extern Node gData;', globals_)
        self.assertIn('extern void helper(Node *, u32);', globals_)
        self.assertIn('#define APPLY(x)', globals_)
        self.assertIn('needed', locals_)
        self.assertNotIn('unused', locals_)
        self.assertNotIn('gUnused', globals_)
        self.assertNotIn('UNUSED', globals_)

    def test_sanitized_listings_never_include_instruction_encodings(self):
        rows = ['08000000: E1A00000  mov r0, r0',
                '08000004: .word 0x12345678 (literal pool)']
        with patch.object(b.diffhint, 'listing', return_value=rows):
            listing = b.sanitized_listing(b'', 0x08000000, 'arm', 0x08000000, 0x08000008)
        self.assertIn('mov r0, r0', listing)
        self.assertNotIn('E1A00000', listing)
        self.assertNotIn('12345678', listing)


class CheckpointTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.patches = [patch.object(b, name, self.root / file) for name, file in (
            ('STATE', 'state.json'), ('LOG', 'events.log'), ('PENDING', 'pending.json'))]
        for p in self.patches:
            p.start()
        self.code = 'void func_0800421C(void) { x = x + 1; }'
        self.source = self.root / 'func_0800421C.c'
        self.source.write_text(self.code)
        region = next(r for r in b.regions(self.code, 'func_0800421C') if r['text'] == 'x = x + 1;')
        self.record = dict(source=str(self.source), source_sha256=b.sha(self.code), before=100, best=100,
                           attempts=0, compiled=0, improvements=0, visits={}, seen=[], feedback=[],
                           profile='old', end='08005238')
        self.state = dict(attempts=0, targets={'0800421C': self.record}, installed=[])
        self.pending = dict(address='0800421C', model='synthetic-test', base_source=self.code,
                            base_sha256=b.sha(self.code), region=region,
                            choices=['x += 1;', '++x;', 'x++;', '{ x = x + 1; }'], next=0, batch=1)
        b.atomic(b.PENDING, self.pending)

    def tearDown(self):
        for p in reversed(self.patches):
            p.stop()
        self.tmp.cleanup()

    def result(self, value, rejection=None):
        return dict(different_bytes=value, exact=False, checker_rejection=rejection,
                    emitted_bytes=100, target_bytes=100, compiler='old')

    def test_strict_improvement_and_semantics_gate(self):
        results = [self.result(99), self.result(99), self.result(101), self.result(98)]

        def measure(*args, **kwargs):
            if len(args) == 5:
                return self.result(99)
            return results.pop(0)

        # Fourth trial would improve its byte count, but its changed behavior
        # must not replace the first accepted trial.
        semantic = [{}, {}, {}, RuntimeError('fixture behavior changed')]
        with patch.object(b.measure, 'measure', side_effect=measure), \
                patch.object(b, 'semantic_check', side_effect=semantic), \
                patch.object(b.match, 'install') as install:
            b.judge_pending(self.state, object())
        self.assertEqual(self.record['best'], 99)
        self.assertIn('x += 1;', self.source.read_text())
        self.assertEqual(self.record['compiled'], 4)
        self.assertEqual(self.record['improvements'], 1)
        self.assertEqual(self.state['attempts'], 4)
        self.assertFalse(b.PENDING.exists())
        install.assert_not_called()
        events = [json.loads(line) for line in b.LOG.read_text().splitlines()]
        self.assertEqual(len(events), 4)
        self.assertEqual([e['retained'] for e in events], [True, False, False, False])
        self.assertFalse(events[-1]['semantics_passed'])

    def test_owner_boundary_cannot_be_enlarged(self):
        with patch.object(b.measure, 'measure', return_value=self.result(1, 'output crosses next candidate boundary')), \
                patch.object(b, 'semantic_check', return_value={}), \
                patch.object(b.match, 'install') as install:
            b.judge_pending(self.state, object())
        self.assertEqual(self.record['best'], 100)
        self.assertEqual(self.source.read_text(), self.code)
        install.assert_not_called()

    def test_recovery_advances_cursor_without_double_judging(self):
        self.state['last_judged'] = [1, 1]
        b.recover_pending(self.state)
        self.assertEqual(json.loads(b.PENDING.read_text())['next'], 2)

    def test_bounded_pass_resumes_remaining_choices(self):
        with patch.object(b.measure, 'measure', return_value=self.result(101)), \
                patch.object(b, 'semantic_check', return_value={}):
            b.judge_pending(self.state, object(), max_judged=2)
            self.assertEqual(json.loads(b.PENDING.read_text())['next'], 2)
            self.assertEqual(self.record['compiled'], 2)
            b.judge_pending(self.state, object(), max_judged=4)
        self.assertEqual(self.record['compiled'], 4)
        self.assertFalse(b.PENDING.exists())

    def test_compile_errors_are_logged_but_do_not_count_toward_proof(self):
        with patch.object(b.measure, 'measure', side_effect=ValueError('syntax failed')):
            b.judge_pending(self.state, object())
        self.assertEqual(self.record['compiled'], 0)
        self.assertEqual(self.state['attempts'], 4)

    def test_whitespace_and_comment_only_answers_do_not_count_toward_proof(self):
        self.pending['choices'] = ['x=x+1;', 'x = x + 1; /* unchanged */']
        b.atomic(b.PENDING, self.pending)
        with patch.object(b.measure, 'measure') as measure:
            b.judge_pending(self.state, object())
        measure.assert_not_called()
        self.assertEqual(self.record['compiled'], 0)
        self.assertEqual(self.source.read_text(), self.code)

    def test_hud_proof_requires_200_measured_alternatives(self):
        self.state['next_target'] = 0
        self.record.update(attempts=250, compiled=199)
        self.assertEqual(b.next_target(self.state, 200, 40), '0800421C')
        self.record['compiled'] = 200
        self.assertEqual(b.next_target(self.state, 200, 40), '080064A4')

    def test_install_calls_existing_full_rom_gates_only_for_exact_owner(self):
        result = self.result(1)
        with patch.object(b.match, 'install') as install:
            self.assertFalse(b.try_install(None, '0800421C', self.code, result))
            result.update(exact=True, different_bytes=0, emitted_bytes=99)
            self.assertFalse(b.try_install(None, '0800421C', self.code, result))
            result['emitted_bytes'] = 100
            self.assertTrue(b.try_install(None, '0800421C', self.code, result))
        install.assert_called_once_with(self.code, 'func_0800421C', 0x0800421C, 100, 'old')

    def test_signal_during_service_wait_saves_clean_stop(self):
        with self.assertRaises(b.StopRequested):
            b.stop(signal.SIGTERM, None)

    def test_external_source_edit_is_preserved(self):
        changed = self.code.replace('x = x + 1;', 'owner_change();')
        self.source.write_text(changed)
        with self.assertRaisesRegex(ValueError, 'source changed'):
            b.judge_pending(self.state, object())
        self.assertEqual(self.source.read_text(), changed)
        self.assertEqual(self.state['attempts'], 0)

    def test_native_fixture_crash_is_bounded_and_scratch_is_removed(self):
        folders = []

        def execute(command, **kwargs):
            folders.append(Path(command[-1]))
            self.assertEqual(kwargs['timeout'], 100)
            return subprocess.CompletedProcess(command, -11, '', '')

        with patch.object(b.subprocess, 'run', side_effect=execute):
            with self.assertRaisesRegex(RuntimeError, 'terminated'):
                b.semantic_check('0800421C', self.source)
        self.assertTrue(folders)
        self.assertFalse(folders[0].exists())

    def test_interrupted_adoption_recovers_only_frozen_reproduced_evidence(self):
        changed = self.code.replace('x = x + 1;', 'x += 1;')
        self.source.write_text(changed)
        b.atomic(self.root / 'candidate.json', dict(source_sha256=b.sha(changed),
                 compiled_sha256='frozen-compiled-hash', different_bytes=99))
        b.atomic(self.root / 'candidate-checks.json', dict(source_sha256=b.sha(changed)))
        reproduced = dict(compiled_sha256='frozen-compiled-hash', different_bytes=99, checker_rejection=None)
        with patch.object(b, 'TARGETS', {'0800421C': b.TARGETS['0800421C']}), \
                patch.object(b.measure, 'measure', return_value=reproduced), \
                patch.object(b, 'semantic_check', return_value={}):
            b.prepare(self.state)
        self.assertEqual(self.record['best'], 99)
        self.assertEqual(self.record['source_sha256'], b.sha(changed))
        self.assertEqual(self.record['compiled'], 0)
        self.assertEqual(self.state['attempts'], 0)

    def test_naming_normalizes_identifier_and_preserves_exact_address(self):
        program = SimpleNamespace(matched={0x08000000: {'name': 'func_08000000', 'size': 4}},
                                  by_start={0x08000000: {'mode': 'arm'}}, rom=bytes(4))
        response = json.dumps({'proposals': [dict(address='08000000', name='DispatchSlotState',
                              description='Dispatches the slot state. Extra explanation.', confidence='medium')]})
        state = {}
        with patch.object(b, 'NAMES', self.root / 'names.json'), \
                patch.object(b, 'matched_source', return_value='void func_08000000(void) {}'), \
                patch.object(b, 'sanitized_listing', return_value='synthetic listing'), \
                patch.object(b, 'render_names'), \
                patch.object(b.match, 'ask', return_value=response), \
                patch.object(b, 'response_diagnostic'):
            b.name_batch(state, program, b.match.MODELS[0])
            proposal = json.loads(b.NAMES.read_text())['08000000']
        self.assertEqual(proposal['name'], 'dispatch_slot_state')
        self.assertEqual(proposal['description'], 'Dispatches the slot state.')
        self.assertEqual(state['names_proposed'], 1)

    def test_naming_rejects_address_aliases_before_case_normalization(self):
        program = SimpleNamespace(matched={0x080020B8: {'name': 'func_080020B8', 'size': 4}},
                                  by_start={0x080020B8: {'mode': 'thumb'}}, rom=bytes(0x20C0))
        response = json.dumps({'proposals': [dict(address='080020B8', name='func_080020B8',
                              description='Dispatches the slot state.', confidence='medium')]})
        state = {}
        with patch.object(b, 'NAMES', self.root / 'names.json'), \
                patch.object(b, 'matched_source', return_value='void func_080020B8(void) {}'), \
                patch.object(b, 'sanitized_listing', return_value='synthetic listing'), \
                patch.object(b, 'render_names'), \
                patch.object(b.match, 'ask', return_value=response), \
                patch.object(b, 'response_diagnostic'):
            b.name_batch(state, program, b.match.MODELS[0])
        self.assertEqual(state['names_proposed'], 0)


@unittest.skipUnless(b.match.toolchain_ready() and Path('baserom.gba').exists(), 'private compiler/ROM unavailable')
class HistoricalIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.program = b.draft.Program()
        cls.table = b.reloc.symbols(cls.program)

    def test_verified_source_maps_and_bounded_prompts_for_all_profiles(self):
        for address, (stem, previous, end, profile) in b.TARGETS.items():
            with self.subTest(address=address):
                source = Path('docs/near-misses') / previous / ('func_' + address + '.c')
                code, start = source.read_text(), int(address, 16)
                actual, _ = b.measure.diagnostic_compile(code, 'func_' + address, start, self.table, profile)
                locations = b.source_locations(code, 'func_' + address, profile, start, self.table, actual)
                want = self.program.rom[start - b.match.BASE:end - b.match.BASE]
                ranked = b.rank_regions(code, 'func_' + address, locations, want, actual, {})
                self.assertTrue(ranked)
                bounded = next(r for r in ranked if len(b.prompt_for(code, 'func_' + address, r,
                    want, actual, start, profile, [])) <= 18000)
                self.assertLessEqual(bounded['last_line'] - bounded['first_line'] + 1, 40)
                self.assertTrue(bounded['different_bytes'])

    def test_mapping_refuses_debug_profile_that_changes_code(self):
        code = 'void func_08000000(void) {}'
        with self.assertRaisesRegex(ValueError, 'debug output changed code'):
            b.source_locations(code, 'func_08000000', 'old', 0x08000000, {}, b'')

    def test_new_temporaries_receive_required_c89_scope(self):
        original = '*(u32 *)0x04000000 = 1;'
        replacement = 'u32 temporary; temporary = 1; *(u32 *)0x04000000 = temporary;'
        prefix = 'void func_08000000(void) { *(u32 *)0x04000000 = 1; '
        with self.assertRaises(subprocess.CalledProcessError):
            b.measure.diagnostic_compile(prefix + replacement + '}', 'func_08000000', 0x08000000, {}, 'old')
        normalized = b.safe_region(original, replacement)
        self.assertTrue(normalized.startswith('{'))
        actual, _ = b.measure.diagnostic_compile(prefix + normalized + '}', 'func_08000000', 0x08000000, {}, 'old')
        self.assertTrue(actual)

    def test_existing_hud_fixtures_reject_changed_behavior(self):
        source = Path('docs/near-misses/hud-owner-1110/func_0800421C.c').read_text()
        self.assertIn('g_03006680++;', source)
        with tempfile.TemporaryDirectory() as folder:
            candidate = Path(folder) / 'candidate.c'
            candidate.write_text(source.replace('g_03006680++;', 'g_03006680--;', 1))
            with self.assertRaisesRegex(RuntimeError, 'HUD regression seed'):
                b.semantic_check('0800421C', candidate)

    def test_naming_extracts_all_registered_address_definitions(self):
        for address, record in self.program.matched.items():
            with self.subTest(address=record['name']):
                code = b.matched_source(self.program, address)
                self.assertIn(record['name'], code)
                self.assertIn('{', code)
                self.assertIn('}', code)


if __name__ == '__main__':
    unittest.main()

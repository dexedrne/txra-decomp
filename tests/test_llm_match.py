import importlib.util
import json
import struct
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

spec = importlib.util.spec_from_file_location('llm_match', Path('tools/llm_match.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
draft, leafgen, reloc = m.draft, m.leafgen, m.reloc
PROG = draft.Program()
needs_compiler = unittest.skipUnless(m.toolchain_ready(), 'matching compiler not installed (tools/setup.sh)')

class Args:
    def __init__(self, **kw):
        self.models, self.retries, self.dry_run, self.max_wait = ','.join(m.MODELS), 2, False, 0
        self.__dict__.update(kw)

class FakeJudge:
    """Stands in for the compiler: a source 'matches' when it contains the expected text."""
    def __init__(self, good):
        self.good, self.calls, self.installed = good, [], []
    def compile(self, code, name, start, limit, table=None, target_end=None):
        self.calls.append(code)
        ok = self.good in code
        rom = PROG.rom[start - m.BASE:start - m.BASE + 4].hex()
        return ok, PROG.size(start), '', rom, rom if ok else '00' * 4
    def install(self, code, name, start, size):
        self.installed.append((name, start, size))

class Patched:
    """Swap module attributes for the duration of a test."""
    def __init__(self, **kw): self.kw, self.old = kw, {}
    def __enter__(self):
        for k, v in self.kw.items(): self.old[k] = getattr(m, k); setattr(m, k, v)
    def __exit__(self, *exc):
        for k, v in self.old.items(): setattr(m, k, v)

def candidate(addr):
    return next(c for c in m.candidates(PROG) if c.start == addr)

class MatchingLoopTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.patch = Patched(STATE=Path(self.tmp.name) / 'status.json', LOG=Path(self.tmp.name) / 'log.txt',
                             PENDING=Path(self.tmp.name) / 'pending', update_progress=lambda status: None,
                             propose_names=lambda *a: None)
        self.patch.__enter__()
        PROG.matched = {m.BASE + x['offset']: x for x in PROG.cfg['matches']}
        # Fixed trial fixtures remain usable after they are matched in the project.
        for address in (0x08015D68, 0x08015D78): PROG.matched.pop(address, None)

    def tearDown(self):
        self.patch.__exit__()
        self.tmp.cleanup()
        PROG.matched = {m.BASE + x['offset']: x for x in PROG.cfg['matches']}

    def test_entries_inside_matched_functions_are_not_candidates(self):
        skipped = {}
        starts = {c.start for c in m.candidates(PROG, skipped)}
        for m0 in PROG.matched.values():
            a, e = m.BASE + m0['offset'], m.BASE + m0['offset'] + m0['size']
            inner = [x for x in PROG.by_start if a < x < e]
            for x in inner:
                self.assertNotIn(x, starts)

    def test_commit_message_reports_real_counts(self):
        before = {'llm_attempts': 3908, 'llm_matched': 0, 'deterministic_matches': 5}
        self.assertEqual(m.commit_message({'llm_attempts': 3950, 'llm_matched': 0, 'deterministic_matches': 5}, before),
                         'Local model loop: 42 attempts, 0 matched')
        self.assertEqual(m.commit_message({'llm_attempts': 3909, 'llm_matched': 1, 'deterministic_matches': 5}, before),
                         'Local model loop: 1 attempt, 1 matched')
        self.assertEqual(m.commit_message({'llm_attempts': 7, 'llm_success_rate': 0.0}),
                         'Local model loop: 7 attempts, 0 matched')

    def test_response_extraction(self):
        self.assertEqual(m.extract_c('```c\nvoid func_08015DA4(void) {}\n```', 'func_08015DA4'), 'void func_08015DA4(void) {}\n')
        for bad in ('#include <x>\nvoid func_08015DA4(void) {}', 'void func_08015DA4(void) { asm("nop"); }', 'void other(void) {}'):
            with self.assertRaises(ValueError):
                m.extract_c(bad, 'func_08015DA4')
        # Repeated prelude typedefs would be redefinitions for the old compiler; they are dropped.
        code = m.extract_c('```c\ntypedef unsigned short u16;\nu16 func_08015DA4(void) { return 1; }\n```', 'func_08015DA4')
        self.assertNotIn('typedef', code)

    def test_candidates_put_real_functions_first_and_skip_fragments(self):
        skipped = {}
        cs = m.candidates(PROG, skipped)
        self.assertTrue(cs)
        firsts = [c.real for c in cs]
        self.assertEqual(firsts, sorted(firsts, reverse=True))
        self.assertTrue(all(c.start not in PROG.matched for c in cs))
        self.assertTrue(all(c.size <= m.MAX_SIZE and c.end <= c.following for c in cs))
        self.assertIn('runtime library routine', skipped.values())
        for a, why in skipped.items():
            if why == 'short fragment between data':
                self.assertFalse(PROG.callers.get(a))
        real = [c.size for c in cs if c.real]
        self.assertLess(real[0], real[-1])

    def test_prompt_contains_draft_listing_and_types(self):
        c = candidate(0x08015D78)
        prompt = m.build_prompt(PROG, c)
        for piece in ('Lifted draft', 'Target THUMB listing', 'u8 u16 u32 s8 s16 s32', '*(vu16 *)0x04000128', '-O2 -mthumb-interwork', c.name, 'KEYINPUT',
                      'Already matched C', 'func_0801604C'):
            self.assertIn(piece, prompt)

    def test_fake_model_mismatch_then_match_is_installed(self):
        c = candidate(0x08015D68)
        answers = iter(['```c\nvoid func_08015D68(void) { }\n```', '```c\nvoid func_08015D68(void) { *(vu16 *)0x04000004 &= 0xFF; }\n```'])
        prompts = []
        judge = FakeJudge('&= 0xFF')
        with Patched(ask=lambda prompt, model, max_wait=None: (prompts.append(prompt), next(answers))[1],
                     compile_candidate=judge.compile, install=judge.install):
            status = m.load_status()
            m.model_pass(PROG, {}, [c], status, Args(models=m.MODELS[0]), judge=True)
        self.assertEqual(judge.installed, [(c.name, c.start, PROG.size(c.start))])
        self.assertEqual((status['attempts'], status['matched'], status['requests']), (2, 1, 2))
        self.assertIn('differs', prompts[1])
        self.assertIn('Previous C:', prompts[1])
        self.assertIn('void func_08015D68(void) { }', prompts[1])
        self.assertEqual(status['by_model'][m.MODELS[0]], {'attempts': 2, 'matched': 1})

    def test_second_opinion_model_runs_after_primary_fails(self):
        c = candidate(0x08015D68)
        used = []
        judge = FakeJudge('never')
        with Patched(ask=lambda prompt, model, max_wait=None: (used.append(model), '```c\nvoid func_08015D68(void) {}\n```')[1],
                     compile_candidate=judge.compile, install=judge.install):
            status = m.load_status()
            m.model_pass(PROG, {}, [c], status, Args(retries=1), judge=True)
        self.assertEqual(used, list(m.MODELS))
        self.assertEqual(judge.installed, [])
        self.assertEqual(status['attempts'], 2)

    def test_without_compiler_answers_are_queued_not_installed(self):
        c = candidate(0x08015D68)
        judge = FakeJudge('anything')
        with Patched(ask=lambda prompt, model, max_wait=None: '```c\nvoid func_08015D68(void) { *(vu16 *)0x04000004 &= 0xFF; }\n```',
                     compile_candidate=judge.compile, install=judge.install):
            status = m.load_status()
            m.model_pass(PROG, {}, [c], status, Args(), judge=False)
            # A second run resumes rather than asking again.
            m.model_pass(PROG, {}, [c], status, Args(), judge=False)
        self.assertEqual(judge.calls, [])
        self.assertEqual(status['attempts'], 0)
        self.assertEqual(status['requests'], 2)
        record = json.loads((m.PENDING / (c.name + '.json')).read_text())
        self.assertEqual([a['source'] for a in record['answers']], ['model:' + x for x in m.MODELS])
        self.assertEqual(record['answers'][0]['syntax'], 'ok')

    def test_judge_pending_installs_queued_match(self):
        c = candidate(0x08015D68)
        m.queue(c, 'model:' + m.MODELS[0], 'void func_08015D68(void) { }\n', None)
        m.queue(c, 'model:' + m.MODELS[1], 'void func_08015D68(void) { *(vu16 *)0x04000004 &= 0xFF; }\n', None)
        judge = FakeJudge('&= 0xFF')
        with Patched(compile_candidate=judge.compile, install=judge.install):
            status = m.load_status()
            m.judge_pending(PROG, {}, status)
        self.assertEqual(len(judge.installed), 1)
        self.assertEqual((status['attempts'], status['matched']), (2, 1))
        self.assertEqual(m.pending_count(), 0)

    def test_deterministic_pass_installs_without_the_model(self):
        c = candidate(0x08015D68)
        judge = FakeJudge('0xFF & *(vu16 *)0x04000004')
        def no_model(*a, **k): raise AssertionError('model must not be asked')
        with Patched(compile_candidate=judge.compile, install=judge.install, ask=no_model):
            status = m.load_status()
            m.deterministic_pass(PROG, {}, [c], status, True, False)
        self.assertEqual(len(judge.installed), 1)
        self.assertEqual(status['deterministic']['matched'], 1)

    def test_service_outage_stops_bounded_pass(self):
        c = candidate(0x08015D68)
        def down(prompt, model, max_wait=None): raise m.Unavailable('connection refused')
        with Patched(ask=down):
            status = m.load_status()
            self.assertFalse(m.model_pass(PROG, {}, [c], status, Args(), judge=True))
        self.assertEqual(status['requests'], 0)

    def test_fake_model_cli_run_does_not_install(self):
        before = Path('tools/rom.cfg').read_bytes()
        progress = Path('progress.json').read_bytes()
        result = subprocess.run([sys.executable, 'tools/llm_match.py', '--dry-run', '--limit', '1', '--retries', '2'],
                                capture_output=True, text=True, timeout=120)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(before, Path('tools/rom.cfg').read_bytes())
        self.assertEqual(progress, Path('progress.json').read_bytes())
        status = json.loads(Path('build/llm-dry-status.json').read_text())
        self.assertEqual(status['requests'], 4 if m.toolchain_ready() else 2)

    @needs_compiler
    def test_real_compiler_exact_match_and_mismatch(self):
        start = 0x08015DA4
        equal, size, *_ = m.compile_candidate('void func_08015DA4(void) {}', 'func_08015DA4', start, start + 8)
        self.assertTrue(equal)
        self.assertEqual(size, 2)
        equal, *_ = m.compile_candidate('int func_08015DA4(void) { return 1; }', 'func_08015DA4', start, start + 8)
        self.assertFalse(equal)

    @needs_compiler
    def test_real_compiler_matches_generated_leaves(self):
        table = reloc.symbols(PROG)
        for addr in (0x080147C0, 0x08014518, 0x08015DA4):
            results = [m.compile_candidate(v, 'func_%08X' % addr, addr, addr + 64, table)[0] for v in leafgen.generate(PROG, addr)]
            self.assertIn(True, results, hex(addr))

    @needs_compiler
    def test_boundary_rejected(self):
        with self.assertRaises(ValueError):
            m.compile_candidate('int func_08015DA4(void) { return 1; }', 'func_08015DA4', 0x08015DA4, 0x08015DA6)

class RelocationTests(unittest.TestCase):
    table = reloc.symbols(PROG)

    def test_bl_reencodes_rom_call(self):
        site = next(i for ins in PROG.insns.values() for i in ins if i.ir[0] == 'call' and PROG.by_start.get(i.ir[1], {}).get('mode') == 'thumb')
        code = reloc.relocate(b'\xff\xf7\xfe\xff', [(0, 'R_ARM_THM_CALL', 'func_%08X' % site.ir[1])], site.addr, self.table)
        self.assertEqual(code, PROG.rom[site.addr - m.BASE:site.addr - m.BASE + 4])

    def test_runtime_names_resolve_to_thumb_entries(self):
        self.assertEqual(self.table['__divsi3'], (0x08018E7C, True))
        self.assertEqual(self.table['_call_via_r3'], (0x08018DEC, True))

    def test_absolute_words(self):
        word = lambda b: struct.unpack('<I', b)[0]
        self.assertEqual(word(reloc.relocate(b'\0\0\0\0', [(0, 'R_ARM_ABS32', 'func_08015DA4')], 0x08000000, self.table)), 0x08015DA5)
        self.assertEqual(word(reloc.relocate(b'\x04\0\0\0', [(0, 'R_ARM_ABS32', 'gUnk_03001234')], 0x08000000, self.table)), 0x03001238)
        self.assertEqual(word(reloc.relocate(b'\x10\0\0\0', [(0, 'R_ARM_ABS32', '.text')], 0x08001000, self.table)), 0x08001010)
        for bad in ([(0, 'R_ARM_ABS32', '.rodata')], [(0, 'R_ARM_THM_JUMP11', 'func_08015DA4')], [(0, 'R_ARM_ABS32', 'mystery')]):
            with self.assertRaises(ValueError):
                reloc.relocate(b'\0\0\0\0', bad, 0x08000000, self.table)

    def test_parse_objdump_records(self):
        text = ('RELOCATION RECORDS FOR [.text]:\nOFFSET   TYPE              VALUE\n'
                '00000004 R_ARM_THM_CALL    func_08015DA4\n0000000c R_ARM_ABS32       .text\n')
        self.assertEqual(reloc.parse(text), [(4, 'R_ARM_THM_CALL', 'func_08015DA4'), (12, 'R_ARM_ABS32', '.text')])
        with self.assertRaises(ValueError):
            reloc.parse('RELOCATION RECORDS FOR [.data]:\n00000000 R_ARM_ABS32       x\n')

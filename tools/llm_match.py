#!/usr/bin/env python3
"""Match THUMB functions against the private ROM: deterministic C first, then a local model fed
the lifted draft. Only byte-identical compiler output is installed, and only after a forced full
rebuild passes the SHA-1 check. Without the matching compiler, answers queue for later judging."""
import argparse
import datetime
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parent.parent
os.chdir(ROOT)
sys.path.insert(0, str(ROOT / 'recomp'))
sys.path.insert(0, str(ROOT / 'tools'))
import draft
import leafgen
import reloc
import diffhint

BASE = 0x08000000
MODELS = tuple(m for m in os.environ.get('TXRA_MODELS', 'kat-coder-v2.5:iq3s,qwen3.6-35b-a3b:iq3s').split(',') if m)
URL = os.environ.get('TXRA_OLLAMA_URL', 'http://127.0.0.1:11434').rstrip('/')
TOOLS = Path(os.environ.get('TXRA_TOOLS', Path.home() / 'opt'))
ARM = str(TOOLS / 'arm-gnu-toolchain-14.3.rel1-x86_64-arm-none-eabi/bin/arm-none-eabi-')
CC = TOOLS / 'agbcc/old_agbcc'
STATE = Path('build/llm-status.json')
LOG = Path('build/llm-match.log')
PENDING = Path('build/llm-pending')
MAX_SIZE = 320          # instruction bytes; larger functions do not fit the model context with their draft
PRELUDE = draft.TYPEDEFS + '#include "types.h"\n'

def run(args, **kwargs):
    return subprocess.run([str(x) for x in args], check=True, capture_output=True, text=True, timeout=60, **kwargs)

def log(message):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open('a') as f:
        f.write(datetime.datetime.now().isoformat(timespec='seconds') + ' ' + message + '\n')
    print(message, flush=True)

def save_status(status):
    STATE.parent.mkdir(parents=True, exist_ok=True)
    tmp = STATE.with_suffix('.tmp')
    tmp.write_text(json.dumps(status, indent=2) + '\n')
    tmp.replace(STATE)

def load_status():
    status = json.loads(STATE.read_text()) if STATE.exists() else {}
    for key, value in (('attempts', 0), ('matched', 0), ('requests', 0), ('by_size', {}), ('by_model', {}),
                       ('daily', {}), ('deterministic', {'tried': 0, 'matched': 0})):
        status.setdefault(key, value)
    status['current_function'] = None
    return status

def toolchain_ready():
    return CC.exists() and all(Path(ARM + t).exists() for t in ('gcc', 'as', 'objcopy', 'objdump'))

# ---------------------------------------------------------------- model service

class Unavailable(Exception):
    pass

def request(path, payload=None, timeout=120):
    data = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(URL + path, data=data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.load(response)

def ask(prompt, model, max_wait=None, poll=60, num_predict=2048, response_format=None, num_ctx=16384):
    """One request at a time, never while an unrelated model is loaded; wait out outages."""
    waited = 0
    while True:
        try:
            lock = Path.home() / '.cache' / 'txra-ollama.lock'
            lock.parent.mkdir(parents=True, exist_ok=True)
            with lock.open('w') as held:
                fcntl.flock(held, fcntl.LOCK_EX)
                ps = request('/api/ps', timeout=10)
                others = [x.get('name') or x.get('model') for x in ps.get('models', [])
                          if x.get('name', '') not in MODELS and x.get('model', '') not in MODELS]
                if others:
                    reason = 'another model is loaded (' + ', '.join(map(str, others)) + ')'
                else:
                    # The shared machine keeps only one permitted model loaded
                    # at a time. Never evict unrelated work to make room.
                    loaded = {x.get('name') or x.get('model') for x in ps.get('models', [])}
                    for previous in sorted(loaded - {model}):
                        unloaded = request('/api/generate', {'model': previous, 'keep_alive': 0}, timeout=120)
                        if unloaded.get('error'):
                            raise ValueError(str(unloaded['error']))
                    payload = {'model': model, 'prompt': prompt, 'stream': False, 'think': False,
                                     'options': {'num_ctx': num_ctx, 'num_predict': num_predict, 'temperature': 0.3},
                                     'keep_alive': '5m'}
                    if response_format is not None:
                        payload['format'] = response_format
                    result = request('/api/generate', payload, timeout=900)
                    if result.get('error') or not result.get('response'):
                        raise ValueError(str(result.get('error', 'empty response')))
                    log('Model response (%s): %s tokens, %d response characters, %d thinking characters, stop=%s.' % (
                        model, result.get('eval_count', '?'), len(result['response']),
                        len(result.get('thinking', '')), result.get('done_reason', '?')))
                    return result['response']
        except (OSError, ValueError, urllib.error.URLError, json.JSONDecodeError) as exc:
            reason = str(exc)
        if max_wait is not None and waited >= max_wait:
            raise Unavailable(reason)
        log('Model service busy or unavailable (%s); waiting %d seconds.' % (reason[:200], poll))
        time.sleep(poll)
        waited += poll

# ---------------------------------------------------------------- candidates

class Candidate:
    def __init__(self, start, end, following, real, from_matched):
        self.start, self.end, self.following, self.real, self.from_matched = start, end, following, real, from_matched
        self.name = 'func_%08X' % start
        self.size = end - start
        self.hard = False

def candidates(prog, skipped=None, hard=False):
    """Unmatched THUMB functions, most valuable first: real (called or referenced) functions,
    smallest first, prioritising callers whose direct callees are all matched. Data-wedged fragments are skipped."""
    cfg = prog.cfg
    starts = sorted(prog.by_start)
    seeds = {BASE + s for s, _ in cfg['seeds']}
    out = []
    skipped = {} if skipped is None else skipped
    # A matched routine can cover later mapped entries (far-jump targets, moved blocks).
    covered = [(start, start + m.get('size', 0)) for start, m in prog.matched.items()]
    for a, f in sorted(prog.by_start.items()):
        if f['mode'] != 'thumb' or a in prog.matched: continue
        if any(s < a < e for s, e in covered):
            skipped[a] = 'inside a matched function'
            continue
        end = int(f['end'], 16)
        following = next((x for x in starts if x > a), BASE + cfg['scan_end'])
        callers = prog.callers.get(a, set())
        real = bool(callers) or a in prog.pointed or a in seeds
        ops = {i.ir[0] for i in prog.insns[a]}
        reason = None
        if not prog.name(a).startswith('func_'): reason = 'runtime library routine'
        elif end > following: reason = 'extent overlaps the next function'
        elif end - a <= 4 and not real: reason = 'short fragment between data'
        elif end - a > MAX_SIZE: reason = 'too large for one model request'
        elif ops & {'swi', 'unknown'}: reason = 'needs BIOS call or undecoded instruction'
        elif hard and not 8 <= len(prog.insns[a]) <= 40: reason = 'outside hard range of 8–40 instructions'
        if reason is None and hard:
            from code_audit import validate_thumb
            unit = validate_thumb(prog.rom, a - BASE, [{'kind': 'matching-candidate'}], budget=2048)
            if not unit['valid'] or any(BASE + z > end or BASE + x < a for x, z in unit.get('spans', [])):
                reason = 'hard mode requires a complete balanced standalone function'
        if reason:
            skipped[a] = reason
            continue
        candidate = Candidate(a, end, following, real, any(c in prog.matched for c in callers))
        calls = prog.callees.get(a, set())
        candidate.hard = hard
        candidate.callees_matched = bool(calls) and all(c in prog.matched for c in calls)
        out.append(candidate)
    def value(c):
        return (not c.real, not c.callees_matched, c.size, c.start)
    return sorted(out, key=value)

# ---------------------------------------------------------------- prompt

def matched_sources(prog):
    """{address: C text of the matched function} from the installed sources."""
    out, files = {}, {}
    for addr, m in prog.matched.items():
        path = Path(m.get('source', 'src/leaves.c'))
        if path not in files: files[path] = path.read_text() if path.exists() else ''
        text = files[path]
        match = re.search(r'(?m)^[^\n;{}#]*\b' + re.escape(m['name']) + r'\s*\([^)]*\)\s*\{', text)
        if not match: continue
        depth, at = 0, match.end() - 1
        while at < len(text):
            depth += {'{': 1, '}': -1}.get(text[at], 0)
            at += 1
            if depth == 0: break
        # Examples are shown preprocessed: the model is told not to write macros.
        out[addr] = re.sub(r'\bWORD\(', '*(vu32 *)(', text[match.start():at].strip())
    return out

def declaration(prog, addr, sources):
    if addr in sources:
        return sources[addr].split('{', 1)[0].strip() + ';'
    n = prog.params(addr)
    return '%s %s(%s);' % ('u32' if prog.returns(addr) else 'void', prog.name(addr), ', '.join(['u32'] * n) or 'void')

def build_prompt(prog, c):
    sources = matched_sources(prog)
    callees = sorted(prog.callees.get(c.start, ()))
    related = [a for a in sources if a in callees or c.start in prog.callees.get(a, ())]
    nearest = sorted((a for a in sources if a not in related), key=lambda a: abs(a - c.start))
    curated = sorted((ROOT / 'tools/fewshot').glob('*.c'),
                     key=lambda path: (int(path.stem.split('_')[-1], 16) not in related,
                                       abs(int(path.stem.split('_')[-1], 16) - c.start)))[:6]
    examples = '\n\n'.join(path.read_text() + '\n/* ' + path.with_suffix('.md').read_text().strip() + ' */' for path in curated if path.with_suffix('.md').exists())
    example_addrs = [a for a in related + nearest if prog.matched[a].get('compiler', 'old') == 'old'][:2]
    examples += '\n\n' + '\n\n'.join(sources[a] for a in example_addrs)
    hardware = sorted({v for v in draft.pool_words(prog, c.start).values() if v is not None and v in prog.hw})
    externs = '\n'.join('extern ' + declaration(prog, a, sources) for a in callees) or '(none)'
    layouts = '\n'.join(line for line in (ROOT / 'src/types.h').read_text().splitlines()
                        if not line.startswith('#'))
    typed_globals = set(re.findall(r'\bg_[0-9A-F]{8}\b', '\n'.join(
        line for line in layouts.splitlines() if line.startswith('extern '))))
    globals_text = '\n'.join(line for line in reloc.declarations(prog, c.start).splitlines()
                             if not typed_globals.intersection(re.findall(r'\bg_[0-9A-F]{8}\b', line)))
    return ('Task: recover the original C source of one function from a Game Boy Advance game. The old GCC 2.95-based '
            'agbcc compiler (cc1, flags -O2 -mthumb-interwork, THUMB code) must reproduce the target bytes exactly.\n'
            'Rules: answer with one ```c block containing ' + c.name + ' and any extern declarations it needs. C89 only: '
            'declare variables at the top of a block, no // comments, no #include, #define, asm or __attribute__. These '
            'typedefs already exist: u8 u16 u32 s8 s16 s32 vu8 vu16 vu32. Use address-named extern globals '
            '(g_XXXXXXXX), and the supplied function declarations. Hardware may use literal addresses, '
            'for example *(vu16 *)0x04000128.\n'
            'The draft is exact in meaning but uses machine registers r0-r12. Turn registers into typed variables and '
            'gotos into if/while/for, choosing types and statement order so the compiler emits the same instructions, '
            'registers and order as the target listing. Preserve signed versus unsigned temporaries; a separate '
            'shift assignment can allocate differently from a shift nested inside subtraction. Typed records '
            'can preserve base addresses that byte-pointer arithmetic folds into offset literals. register-qualified '
            'locals can keep repeated call arguments in high registers. A for loop, a guarded do/while, '
            'and a while loop can allocate differently despite equivalent bounds. Keep independent retry '
            'checks separate; combining them with logical OR can change allocation. Place pointer/count '
            'updates in their original order and scope. Integer address arithmetic and typed pointer arithmetic '
            'can preserve different temporaries even when the addresses are identical. A guarded do/while '
            'can preserve a saved count that a while loop consumes directly. Do not add artificial side effects.\n\n' +
            ('Hard-mode recovery: work from the complete listing and supplied callee signatures. First establish '
             'the control-flow skeleton, access widths and stack layout. Treat the lifted draft as provisional '
             'where a mapped entry reads saved high registers before initializing them. Never invent parameters '
             'to hide an internal entry or count a prefix as a complete function. On retry, keep matching regions '
             'and explain the single source-level change in a C comment.\n' if c.hard else '') +
            'Signature guess: ' + draft.signature(prog, c.start) + '\n'
            'Shared recovered type layouts (already included by the judge):\n```c\n' + layouts + '\n```\n'
            'Declarations of called functions:\n' + externs + '\n' +
            'Known literal addresses (additional byte arrays; shared typed globals above take precedence):\n' + globals_text + '\n' +
            ('Hardware registers: ' + ', '.join('0x%08X %s' % (a, prog.hw[a]) for a in hardware) + '\n' if hardware else '') +
            '\nLifted draft:\n```c\n' + draft.draft(prog, c.start) + '```\n\n'
            'Target THUMB listing (literal pool values in parentheses):\n' + draft.disassembly(prog, c.start) + '\n\n' +
            ('Already matched C from this game (same compiler and flags):\n```c\n' + examples + '\n```\n' if examples else ''))

TYPEDEF_LINE = re.compile(r'^\s*typedef\s+(?:unsigned|signed|volatile)[^;]*\b(?:u8|u16|u32|s8|s16|s32|vu8|vu16|vu32)\s*;\s*$', re.M)

def extract_c(answer, name):
    blocks = re.findall(r'```(?:c)?\s*\n(.*?)```', answer, re.S | re.I)
    code = max(blocks, key=lambda b: name in b) if blocks else answer
    code = TYPEDEF_LINE.sub('', code)
    if len(code) > 12000 or re.search(r'^\s*#|\b(?:asm|__asm__|__attribute__|__attribute|include)\b', code, re.M):
        raise ValueError('unsafe or unsupported C')
    if not re.search(r'\b' + re.escape(name) + r'\s*\(', code):
        raise ValueError('missing required function')
    return code.strip() + '\n'

def syntax_check(code):
    """Cheap host-compiler parse used only when the matching compiler is absent; never a match."""
    host = shutil.which('cc') or shutil.which('gcc')
    if not host: return None
    with tempfile.TemporaryDirectory(prefix='txra-syntax-') as td:
        path = Path(td) / 'trial.c'
        path.write_text(PRELUDE + code)
        r = subprocess.run([host, '-fsyntax-only', '-std=gnu89', '-w', '-Isrc', str(path)], capture_output=True, text=True, timeout=60)
        return None if r.returncode == 0 else r.stderr.replace(str(path), 'trial.c')[:800]

# ---------------------------------------------------------------- judge

def compile_candidate(code, name, start, limit, table=None, target_end=None, compiler='old', cache=None, rom=None):
    """Compile, relocate and compare. Optional cache requires fixed ROM/symbol snapshots."""
    if compiler in ('arm', 'modern-arm') and start & 3:
        raise ValueError('ARM function start is not word aligned')
    Path('build').mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='txra-match-', dir='build') as td:
        d = Path(td)
        (d / 'trial.c').write_text(code if 'typedef unsigned char u8;' in code else PRELUDE + code)
        run([ARM + 'gcc', '-E', '-P', '-Isrc', d/'trial.c', '-o', d/'trial.i'])
        if compiler not in ('old', 'standard', 'old-no-gcse', 'old-o1', 'standard-o1', 'modern-arm', 'old-no-interwork', 'arm'):
            raise ValueError('unknown compiler variant')
        arm_mode = compiler in ('arm', 'modern-arm')
        if compiler == 'modern-arm':
            run([ARM + 'gcc', '-S', '-x', 'c', d/'trial.i', '-O2', '-marm', '-mcpu=arm7tdmi',
                 '-mno-thumb-interwork', '-o', d/'trial.s'])
        else:
            cc = CC.with_name('agbcc_arm') if compiler == 'arm' else CC.with_name('agbcc') if compiler in ('standard', 'standard-o1') else CC
            flags = ['-fno-gcse'] if compiler == 'old-no-gcse' else []
            run([cc, d/'trial.i', '-O1' if compiler.endswith('-o1') else '-O2', '-mno-thumb-interwork' if compiler == 'old-no-interwork' else '-mthumb-interwork', *flags, '-o', d/'trial.s'])
        assembly = (d/'trial.s').read_text()
        match = re.search(r'(?m)^' + re.escape(name) + r':', assembly)
        if not match:
            raise ValueError('function not emitted')
        tail = assembly[match.start():]
        finish = re.search(r'\n\s*\.size\s+' + re.escape(name) + r',[^\n]*', tail)
        if not finish:
            raise ValueError('function size missing')
        cache_key = (name, start, limit, target_end, compiler, tail[:finish.end()])
        if cache is not None and cache_key in cache:
            return cache[cache_key]
        preamble = '.syntax unified\n.text\n.arm\n' if compiler == 'modern-arm' else '.syntax divided\n.text\n' + ('.arm\n' if arm_mode else '.thumb\n')
        (d/'one.s').write_text(preamble + tail[:finish.end()] + '\n')
        run([ARM + 'as', '-mcpu=arm7tdmi', d/'one.s', '-o', d/'one.o'])
        run([ARM + 'objcopy', '-O', 'binary', '-j', '.text', d/'one.o', d/'one.bin'])
        actual = reloc.function_bytes(d/'one.o', (d/'one.bin').read_bytes(), name, ARM + 'objdump')
        relocs = reloc.parse(run([ARM + 'objdump', '-r', d/'one.o']).stdout)
        if relocs:
            if table is None: raise ValueError('relocations need the symbol table')
            actual = reloc.relocate(actual, relocs, start, table)
        if not actual or start + len(actual) > limit:
            raise ValueError('output crosses next candidate boundary')
        span = max(len(actual), (target_end or start) - start)
        rom = (Path('baserom.gba').read_bytes() if rom is None else rom)[start-BASE:start-BASE+span]
        if arm_mode:
            from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
            emitted = '\n'.join('%08X: %s %s' % (i.address, i.mnemonic, i.op_str)
                                for i in Cs(CS_ARCH_ARM, CS_MODE_ARM).disasm(actual, start))
        else:
            emitted = '\n'.join(draft.disassemble_thumb(actual, start))
        result = actual == rom, len(actual), emitted, rom.hex(), actual.hex()
        if cache is not None:
            if len(cache) >= 4096: cache.pop(next(iter(cache)))
            cache[cache_key] = result
        return result

def mismatch_feedback(start, expected_hex, actual_hex):
    expected, actual = bytes.fromhex(expected_hex), bytes.fromhex(actual_hex)
    distance = sum(a != b for a, b in zip(expected, actual)) + abs(len(expected) - len(actual))
    return ('\nByte distance: %d\n' % distance + diffhint.hint(expected, actual, start) +
            '\nRevise the previous C to close these differences. If only a few instructions differ, '
            'keep the matching control flow and change one type, initializer, expression or declaration at a time. '
            'Use the first differing offset and exact prefix/suffix to localize the edit. Do not rewrite an '
            'already matching loop to repair an unrelated pool or prologue difference.')


def retry_context(code, feedback, best=None):
    """Retain the nearest compiled source when a later retry regresses or fails to compile."""
    found = re.search(r'Byte distance: (\d+)', feedback)
    score = int(found.group(1)) if found else None
    current = '\nPrevious C:\n```c\n' + code + '```\n' + feedback
    if score is not None and (best is None or score <= best[0]):
        best = (score, current)
    if best is not None and (score is None or score > best[0]):
        current += '\nReturn to the closest compiled attempt below; the latest change regressed.\n' + best[1]
    return current, best

NEAR = Path("build/nearmiss")

def load_near(name):
    """Closest compiled attempt kept across passes (about 5,000 tries had forgotten every near miss between passes)."""
    try:
        d = json.loads((NEAR / (name + ".json")).read_text())
        return int(d["score"]), d["text"]
    except Exception:
        return None

def save_near(name, best):
    if best is None: return
    NEAR.mkdir(parents=True, exist_ok=True)
    (NEAR / (name + ".json")).write_text(json.dumps({"score": best[0], "text": best[1]}))

def config_with_matches(text, matches):
    """Update only the matches array; retain the large mapping's reviewed formatting."""
    key = re.search(r'"matches"\s*:\s*', text)
    if key is None: raise ValueError('configuration has no matches array')
    _, end = json.JSONDecoder().raw_decode(text, key.end())
    return text[:key.end()] + json.dumps(matches, indent=2).replace('\n', '\n  ') + text[end:]


def install(code, name, start, size, compiler='old'):
    cfg_path = Path('tools/rom.cfg')
    old = cfg_path.read_text()
    cfg = json.loads(old)
    source = Path('src/generated') / (name + '.c')
    source.parent.mkdir(parents=True, exist_ok=True)
    if source.exists():
        raise ValueError('source already exists')
    try:
        source.write_text('/* Byte-verified C; address name retained pending semantic review. */\n' +
                          (code if 'typedef unsigned char u8;' in code else PRELUDE + code))
        cfg['matches'].append({'name': name, 'offset': start-BASE, 'size': size, 'source': str(source)})
        if compiler not in ('old', 'standard', 'old-no-gcse', 'old-o1', 'standard-o1', 'modern-arm', 'old-no-interwork', 'arm'):
            raise ValueError('unknown compiler variant')
        if compiler != 'old': cfg['matches'][-1]['compiler'] = compiler
        cfg_path.write_text(config_with_matches(old, cfg['matches']))
        subprocess.run(['make', '-B', 'all'], check=True, capture_output=True, text=True)
    except Exception:
        cfg_path.write_text(old)
        source.unlink(missing_ok=True)
        # Restore generated assembly and artifacts after any failed trial.
        subprocess.run(['make', '-B', 'all'], check=True, capture_output=True, text=True)
        raise

def propose_names(prog, code, start, model, max_wait):
    try:
        proposal = ask('Suggest a descriptive function name and parameter names for this matched C. Explain the evidence and '
                       'uncertainty. Do not invent game semantics.\n' + code + '\n' + draft.disassembly(prog, start), model, max_wait)
    except Unavailable:
        return
    names = Path('docs/map/name-proposals.json')
    records = json.loads(names.read_text()) if names.exists() else []
    identifiers = re.findall(r'\b[a-zA-Z_][a-zA-Z_0-9]{2,40}\b', proposal)[:20]
    records.append({'address': hex(start), 'proposed_identifiers': identifiers, 'status': 'unreviewed; address name retained'})
    names.write_text(json.dumps(records, indent=2) + '\n')

# ---------------------------------------------------------------- bookkeeping

def update_progress(status):
    p = Path('progress.json')
    progress = json.loads(p.read_text())
    cfg = json.loads(Path('tools/rom.cfg').read_text())
    fs = json.loads(Path('docs/map/functions.json').read_text())['functions']
    code_bytes = sum(int(b, 16)-int(a, 16) for f in fs for a,b in f['spans'])
    matched_bytes = sum(m['size'] for m in cfg['matches'])
    progress['functions_matched_c'] = {'count': len(cfg['matches']), 'bytes_including_pools': matched_bytes,
                                       'percent_of_mapped_code': round(100*matched_bytes/code_bytes, 3) if code_bytes else 0}
    progress['functions_c_matched'] = len(cfg['matches'])
    # Attempts are model answers the matching compiler has judged; queued answers are counted separately.
    progress['llm_attempts'] = status['attempts']
    progress['llm_matched'] = status['matched']
    progress['llm_success_rate'] = round(status['matched'] / status['attempts'], 4) if status['attempts'] else None
    progress['llm_requests'] = status['requests']
    progress['llm_answers_pending_judgement'] = pending_count()
    progress['deterministic_matches'] = status['deterministic']['matched']
    p.write_text(json.dumps(progress, indent=2) + '\n')

def commit_message(current, previous=None):
    """One-line message for a loop progress commit, counting attempts and installed matches since PREVIOUS.

    Both arguments are progress.json dictionaries; PREVIOUS is the committed copy (None for a first commit).
    Never claims matches that did not happen: an attempts-only pass says "0 matched"."""
    def counts(p):
        p = p or {}
        matched = p.get('llm_matched')
        if matched is None:
            matched = round((p.get('llm_success_rate') or 0) * p.get('llm_attempts', 0))
        return p.get('llm_attempts', 0), matched + p.get('deterministic_matches', 0)
    attempts, matched = counts(current)
    if previous is not None:
        before_attempts, before_matched = counts(previous)
        attempts, matched = attempts - before_attempts, matched - before_matched
    return 'Local model loop: %d attempt%s, %d matched' % (attempts, '' if attempts == 1 else 's', max(matched, 0))

def committed_progress(ref='HEAD'):
    try:
        return json.loads(subprocess.run(['git', 'show', ref + ':progress.json'], check=True,
                                         capture_output=True, text=True).stdout)
    except (subprocess.CalledProcessError, ValueError):
        return None

def pending_path(name):
    return PENDING / (name + '.json')

def pending_count():
    n = 0
    for path in PENDING.glob('*.json') if PENDING.exists() else ():
        n += sum(1 for a in json.loads(path.read_text())['answers'] if not a.get('judged') and a['source'] != 'deterministic')
    return n

def queue(c, source, code, syntax, prompt_hash=None):
    PENDING.mkdir(parents=True, exist_ok=True)
    path = pending_path(c.name)
    record = json.loads(path.read_text()) if path.exists() else {'name': c.name, 'start': hex(c.start), 'end': hex(c.end),
                                                                   'limit': hex(c.following), 'answers': []}
    if any(a['code'] == code and a['source'] == source for a in record['answers']): return
    record['answers'].append({'source': source, 'code': code, 'syntax': syntax or 'ok', 'judged': False,
                              'prompt_sha1': prompt_hash, 'time': datetime.datetime.now().isoformat(timespec='seconds')})
    path.write_text(json.dumps(record, indent=2) + '\n')

def record_attempt(status, c, model, matched):
    status['attempts'] += 1
    stats = status['by_size'].setdefault(str(c.size), {'attempts': 0, 'matched': 0, 'success_rate': 0})
    stats['attempts'] += 1
    m = status['by_model'].setdefault(model, {'attempts': 0, 'matched': 0})
    m['attempts'] += 1
    if matched:
        status['matched'] += 1; stats['matched'] += 1; m['matched'] += 1
        today = datetime.date.today().isoformat()
        status['daily'][today] = status['daily'].get(today, 0) + 1
    stats['success_rate'] = round(stats['matched'] / stats['attempts'], 4)

def try_install(prog, table, c, code, dry_run):
    """Judge one source; install it when byte-identical. Returns (matched, feedback)."""
    try:
        equal, size, emitted, expected, actual = compile_candidate(code, c.name, c.start, c.following, table, target_end=c.end)
    except (ValueError, subprocess.SubprocessError) as exc:
        detail = exc.stderr if isinstance(exc, subprocess.CalledProcessError) and exc.stderr else str(exc)
        return False, '\nCompilation or validation failed: ' + str(detail)[:1000]
    if equal and c.start + size >= c.end:
        if dry_run:
            log(c.name + ' fake trial matched; not installed')
            return True, ''
        try:
            install(code, c.name, c.start, size)
        except (ValueError, subprocess.SubprocessError) as exc:
            return False, '\nStandalone bytes matched but the full rebuild failed: ' + str(exc)[:300]
        prog.matched[c.start] = {'name': c.name, 'offset': c.start - BASE, 'size': size, 'source': 'src/generated/%s.c' % c.name}
        log(c.name + ' matched and full ROM verified')
        return True, ''
    if equal:
        return False, '\nThe output matched only the first %d of %d target bytes; the function continues.' % (size, c.end - c.start)
    return False, mismatch_feedback(c.start, expected, actual)

# ---------------------------------------------------------------- passes

def deterministic_pass(prog, table, batch, status, judge, dry_run):
    for c in batch:
        if c.start in prog.matched: continue
        variants = leafgen.generate(prog, c.start)
        for code in variants:
            if not judge:
                queue(c, 'deterministic', code, syntax_check(code))
                continue
            status['deterministic']['tried'] += 1
            ok, _ = try_install(prog, table, c, code, dry_run)
            if ok:
                status['deterministic']['matched'] += 0 if dry_run else 1
                if not dry_run: update_progress(status)
                break
        save_status(status)

def model_pass(prog, table, batch, status, args, judge):
    models = [m for m in args.models.split(',') if m]
    for model in models:
        if model not in MODELS: raise SystemExit('model not allowed: ' + model)
    done = set()
    # Outer loop over models keeps the service from swapping models between requests.
    for turn, model in enumerate(models):
        for c in batch:
            if c.start in prog.matched or c.start in done: continue
            path = pending_path(c.name)
            if not judge and path.exists() and any(a['source'] == 'model:' + model for a in json.loads(path.read_text())['answers']):
                continue
            prompt = build_prompt(prog, c)
            phash = hashlib.sha1(prompt.encode()).hexdigest()[:12]
            best = load_near(c.name) if judge else None
            feedback = ('\nA previous pass left this closest compiled attempt; start from it and change as little as possible.\n' + best[1]) if best else ''
            status['current_function'] = c.name; save_status(status)
            tries = args.retries if judge else 2
            for attempt in range(tries):
                hint = ('try explicit temporaries', 'try signed versus unsigned types', 'try a different loop shape',
                        'try alternative statement order')[attempt % 4]
                if args.dry_run:
                    answer = '```c\nvoid %s(void) {}\n```' % c.name
                    status['requests'] += 1
                else:
                    try:
                        answer = ask(prompt + feedback + ('\nOn this attempt, ' + hint + '.' if attempt else ''), model, args.max_wait)
                    except Unavailable as exc:
                        log('Stopping this pass: model service unavailable for %s seconds (%s).' % (args.max_wait, exc))
                        return False
                    status['requests'] += 1
                try:
                    code = extract_c(answer, c.name)
                except ValueError as exc:
                    feedback = '\nYour previous answer was rejected: %s. Answer with one ```c block.' % exc
                    if judge: record_attempt(status, c, model, False)
                    save_status(status)
                    continue
                if not judge:
                    syntax = syntax_check(code)
                    if not args.dry_run: queue(c, 'model:' + model, code, syntax, phash)
                    status.setdefault('collected', 0)
                    status['collected'] += 1
                    save_status(status)
                    log('%s: %s answer queued for judging (%s)' % (c.name, model, 'parses' if not syntax else 'syntax errors'))
                    if not syntax: break
                    feedback = '\nYour previous answer does not compile as C89:\n' + syntax + '\nFix it.'
                    continue
                ok, feedback = try_install(prog, table, c, code, args.dry_run)
                if not ok:
                    feedback, best = retry_context(code, feedback, best)
                    if judge: save_near(c.name, best)
                record_attempt(status, c, model, ok and not args.dry_run)
                save_status(status)
                if ok:
                    done.add(c.start)
                    if not args.dry_run:
                        update_progress(status)
                        propose_names(prog, code, c.start, model, args.max_wait)
                    break
            log('%s: %s trials complete' % (c.name, model))
            if not args.dry_run: update_progress(status)
    return True

def judge_pending(prog, table, status):
    if not PENDING.exists(): return
    by_start = {c.start: c for c in candidates(prog)}
    for path in sorted(PENDING.glob('*.json')):
        record = json.loads(path.read_text())
        start = int(record['start'], 16)
        c = by_start.get(start)
        for a in record['answers']:
            if a.get('judged'): continue
            if c is None or start in prog.matched:
                a['judged'] = True; a['result'] = 'skipped: already matched or no longer a candidate'; continue
            ok, feedback = try_install(prog, table, c, a['code'], False)
            a['judged'] = True
            a['result'] = 'match' if ok else feedback.strip()[:300]
            if a['source'] == 'deterministic':
                status['deterministic']['tried'] += 1; status['deterministic']['matched'] += int(ok)
            else:
                record_attempt(status, c, a['source'].split(':', 1)[-1], ok)
            save_status(status)
        path.write_text(json.dumps(record, indent=2) + '\n')
    update_progress(status)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--forever', action='store_true')
    parser.add_argument('--dry-run', action='store_true', help='use a deterministic fake model; never install')
    parser.add_argument('--retries', type=int, default=4, help='compiler-judged guesses per function and model')
    parser.add_argument('--limit', type=int, default=1, help='number of functions to try per pass')
    parser.add_argument('--models', default=','.join(MODELS), help='comma-separated, in order; the second is a second opinion')
    parser.add_argument('--max-wait', type=int, default=None, help='give up a pass after this many seconds of service outage')
    parser.add_argument('--deterministic-only', action='store_true', help='only emit C for recognised leaves')
    parser.add_argument('--judge-pending', action='store_true', help='judge queued answers with the matching compiler')
    parser.add_argument('--list', action='store_true', help='print the candidate order and exit')
    parser.add_argument('--commit-message', action='store_true',
                        help='print the progress commit message (attempts and matches since HEAD) and exit')
    parser.add_argument('--hard', action='store_true', help='send 8–40 instruction functions directly to the model, with callee signatures')
    args = parser.parse_args()
    if args.retries < 1 or args.limit < 1:
        parser.error('retries and limit must be positive')
    if args.hard and args.deterministic_only:
        parser.error('--hard sends model requests; it cannot be combined with --deterministic-only')
    if args.commit_message:
        print(commit_message(json.loads(Path('progress.json').read_text()), committed_progress()))
        return
    Path('build').mkdir(exist_ok=True)
    global STATE
    if args.dry_run: STATE = Path('build/llm-dry-status.json'); STATE.unlink(missing_ok=True)
    status = load_status()
    prog = draft.Program()
    table = reloc.symbols(prog)
    judge = toolchain_ready()
    if args.list:
        skipped = {}
        for c in candidates(prog, skipped, hard=args.hard):
            print('%s %4d bytes real=%d from_matched=%d deterministic=%d' % (c.name, c.size, c.real, c.from_matched,
                                                                          bool(leafgen.generate(prog, c.start, 1))))
        for a, why in sorted(skipped.items()): print('skip func_%08X: %s' % (a, why))
        return
    if args.judge_pending:
        if not judge: raise SystemExit('the matching compiler is not installed; run tools/setup.sh first')
        judge_pending(prog, table, status)
        return
    if not judge and not args.dry_run:
        log('Matching compiler not found under %s: answers are queued in %s for --judge-pending; nothing is installed.' % (TOOLS, PENDING))
    seen = set()
    while True:
        options = [c for c in candidates(prog, hard=args.hard) if c.start not in seen]
        if not options:
            if not args.forever: break
            seen.clear(); log('Pass complete; waiting before retrying candidates.'); time.sleep(60); continue
        batch = options[:args.limit]
        seen.update(c.start for c in batch)
        if not args.dry_run and not args.hard: deterministic_pass(prog, table, batch, status, judge, False)
        if not args.deterministic_only:
            if not model_pass(prog, table, batch, status, args, judge) and not args.forever: break
        if not args.dry_run: update_progress(status)
        if not args.forever: break
    status['current_function'] = None; save_status(status)

if __name__ == '__main__': main()

#!/usr/bin/env python3
"""Resumable, serial block mutation search; only full-ROM-verified matches install.

No cartridge bytes or compiler binaries are retained. Response diagnostics stay
in ignored build scratch. Source
line mapping uses a separate debug compilation, verified against the pinned
non-debug profile before its locations can influence region selection. Positional
byte attribution is a layout heuristic, not a claim about semantic equivalence.
"""
import argparse
import contextlib
import datetime
import fcntl
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import re
import signal
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / 'tools'), str(ROOT / 'recomp')]
import diffhint
import draft
import llm_match as match
import measure_candidate as measure
import reloc

TARGETS = {
    '0800421C': ('hud-owner', 'hud-owner-1110', 0x08005238, 'old'),
    '080064A4': ('sound-owner', 'sound-owner-1109d', 0x08007398, 'old'),
    '08016DA8': ('arm-16da8', 'arm-16da8-1110', 0x08017E68, 'arm'),
}
STATE = Path('build/llm-blocks-status.json')
LOG = Path('build/llm-blocks.log')
PENDING = Path('build/llm-blocks-pending.json')
NAMES = Path('build/llm-blocks-names.json')
CONTEXT_TOKENS = 16384
PROMPT_CHARACTER_LIMIT = 18000
TOKEN = re.compile(r'/\*.*?\*/|//[^\n]*|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'|'
                   r'^[ \t]*\#(?:[^\n]*\\\n)*[^\n]*|[A-Za-z_]\w*|\d[\w.]*|\S', re.S | re.M)
FORBIDDEN = re.compile(r'\b(?:asm|__asm|__asm__|__attribute__|__attribute|__builtin_\w*|'
                       r'volatile|vu8|vu16|vu32|__LINE__|__FILE__)\b|^\s*#', re.M)


class StopRequested(BaseException):
    pass


def stop(signum, frame):
    raise StopRequested()


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def atomic(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, indent=2) + '\n')
    temporary.replace(path)


def log(event, **fields):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open('a') as output:
        output.write(json.dumps(dict(time=now(), event=event, **fields), sort_keys=True) + '\n')


def save(state):
    state['updated'] = now()
    atomic(STATE, state)


def owner_notes():
    path = Path('OWNER-NOTES.md')
    return path.read_text() if path.exists() else ''


def owner_alive(state):
    try:
        process = Path('/proc') / str(state.get('pid'))
        return bool(state.get('running') and process.joinpath('cwd').resolve() == ROOT and
                    process.joinpath('stat').read_text().split()[21] == state.get('process_start_ticks'))
    except OSError:
        return False


def tokens(code):
    return [(m.group(), m.start(), m.end()) for m in TOKEN.finditer(code)
            if not m.group().startswith(('/*', '//', '#'))]


def function_span(code, name):
    """Find an entire function including compact and multiline signatures."""
    ts = tokens(code)
    for i, (word, begin, _) in enumerate(ts):
        if word != name or i + 1 == len(ts) or ts[i + 1][0] != '(':
            continue
        j = paired(ts, i + 1)
        if j + 1 == len(ts) or ts[j + 1][0] != '{':
            continue
        end = paired(ts, j + 1)
        first = i
        while first and ts[first - 1][0] not in (';', '}', '{'):
            first -= 1
        return ts[first][1], ts[j + 1][1], ts[end][2]
    raise ValueError('function definition not found: ' + name)


def paired(ts, index):
    opening = ts[index][0]
    closing = {'(': ')', '{': '}', '[': ']'}[opening]
    depth = 0
    for i in range(index, len(ts)):
        depth += ts[i][0] == opening
        depth -= ts[i][0] == closing
        if depth == 0:
            return i
    raise ValueError('unbalanced C delimiter')


def regions(code, name, max_lines=40):
    """Collect complete statements, controls and adjacent statement groups.

    This is a bounded C89 statement scanner, not a C type parser. The compiler
    remains the syntax authority. It never splits a control header, for clause,
    string, macro call or an if/else pair. Declarations remain in their scope.
    """
    _, opening, _ = function_span(code, name)
    ts = tokens(code)
    root = next(i for i, t in enumerate(ts) if t[1] == opening)
    spans = set()
    block_macros = set(re.findall(r'^\s*#define\s+(\w+)\([^)]*\)\s*(?:\\\n\s*)?(?:if\b|do\b|\{)', code, re.M))

    def add(first, last):
        a, b = ts[first][1], ts[last - 1][2]
        if code.count('\n', a, b) < max_lines:
            spans.add((a, b))

    def compound(i):
        end = paired(ts, i)
        items = []
        j = i + 1
        while j < end:
            k = statement(j)
            if k <= j or k > end:
                raise ValueError('unrecognized C statement boundary at line %d: %s' % (
                    code.count('\n', 0, ts[j][1]) + 1, code[ts[j][1]:ts[k - 1][2]][:100]))
            add(j, k)
            items.append((j, k))
            j = k
        # Only group siblings, so a mutation cannot break an enclosing control.
        for index, (first, _) in enumerate(items):
            for _, last in items[index + 1:index + 5]:
                add(first, last)
        return end + 1

    def statement(i):
        word = ts[i][0]
        if word in block_macros and ts[i + 1][0] == '(':
            end = paired(ts, i + 1) + 1
            return end + (ts[end][0] == ';')
        if word == '{':
            return compound(i)
        if word in ('if', 'for', 'while', 'switch'):
            if ts[i + 1][0] != '(':
                raise ValueError('missing control header')
            end = statement(paired(ts, i + 1) + 1)
            if word == 'if' and ts[end][0] == 'else':
                end = statement(end + 1)
            return end
        if word == 'do':
            end = statement(i + 1)
            if ts[end][0] != 'while':
                raise ValueError('missing do/while tail')
            return paired(ts, end + 1) + 2
        if word in ('case', 'default') or (i + 1 < len(ts) and ts[i + 1][0] == ':'):
            # Labels stay outside selected regions; the following complete
            # statement and subsequent siblings are independently selectable.
            end = i
            while ts[end][0] != ':':
                end += 1
            return end + 1
        j = i
        while j < len(ts):
            if ts[j][0] in ('(', '[', '{'):
                j = paired(ts, j) + 1
            elif ts[j][0] == ';':
                return j + 1
            else:
                j += 1
        raise ValueError('unterminated C statement')

    compound(root)
    output = []
    for a, b in sorted(spans):
        text = code[a:b]
        # Declarations and labels alone cannot usefully account for code.
        if re.match(r'^(?:case\b|default\s*:|\w+\s*:$)', text) or text == ';':
            continue
        output.append(dict(begin=a, end=b, first_line=code.count('\n', 0, a) + 1,
                           last_line=code.count('\n', 0, b) + 1, text=text,
                           identity=sha(text)))
    return output


def source_locations(code, name, profile, start, table, expected_output):
    """Verified debug-only build supplies exact source line -> machine spans."""
    with tempfile.TemporaryDirectory(prefix='blocks-map-', dir='build') as folder:
        p = Path(folder)
        prelude = '' if 'typedef unsigned char u8;' in code else match.PRELUDE
        (p / 'trial.c').write_text(prelude + '#line 1 "candidate.c"\n' + code)
        match.run([match.ARM + 'gcc', '-E', '-Isrc', p / 'trial.c', '-o', p / 'trial.i'])
        compiler = match.CC.with_name('agbcc_arm') if profile == 'arm' else match.CC
        match.run([compiler, p / 'trial.i', '-O2', '-mthumb-interwork', '-g', '-o', p / 'trial.s'])
        match.run([match.ARM + 'as', '-mcpu=arm7tdmi', p / 'trial.s', '-o', p / 'trial.o'])
        match.run([match.ARM + 'objcopy', '-O', 'binary', '-j', '.text', p / 'trial.o', p / 'trial.bin'])
        actual = reloc.function_bytes(p / 'trial.o', (p / 'trial.bin').read_bytes(), name, match.ARM + 'objdump')
        entries = reloc.parse(match.run([match.ARM + 'objdump', '-r', '-j', '.text', p / 'trial.o']).stdout)
        actual = reloc.relocate(actual, entries, start, table) if entries else actual
        if actual != expected_output:
            raise ValueError('debug output changed code; source mapping refused')
        listing = match.run([match.ARM + 'objdump', '--dwarf=decodedline', p / 'trial.o']).stdout
        locations = [(int(m[1]), int(m[2], 0)) for m in re.finditer(
            r'(?m)^candidate\.c\s+(\d+)\s+(0x[0-9a-f]+|0)\s', listing)]
        if not locations:
            raise ValueError('compiler supplied no source map')
        return [(line, offset, locations[i + 1][1] if i + 1 < len(locations) else len(actual))
                for i, (line, offset) in enumerate(locations)]


def rank_regions(code, name, locations, want, actual, visits, max_lines=40):
    ranked = []
    for region in regions(code, name, max_lines=max_lines):
        spans = [(a, b) for line, a, b in locations
                 if region['first_line'] <= line <= region['last_line'] and b > a]
        offsets = {i for a, b in spans for i in range(a, b)}
        different = sum(i >= len(want) or i >= len(actual) or want[i] != actual[i] for i in offsets)
        if not different:
            continue
        region['different_bytes'] = different
        region['machine_spans'] = spans
        region['visits'] = visits.get(region['identity'], 0)
        ranked.append(region)
    # Visit every differing region before returning to the worst; an accepted
    # improvement resets the visit cycle because its layout has changed.
    return sorted(ranked, key=lambda r: (r['visits'], -r['different_bytes'],
                                        r['last_line'] - r['first_line'], r['begin']))


def safe_region(original, replacement):
    if not replacement.strip() or len(replacement) > 12000 or replacement.count('\n') >= 40:
        raise ValueError('replacement must be one nonempty region of at most 40 lines')
    clean = lambda text: re.sub(r'/\*.*?\*/|//[^\n]*', '', text, flags=re.S)
    new, old = clean(replacement), clean(original)
    if re.match(r'^\s*(?:register\s+)?(?:const\s+)?(?:u8|u16|u32|s8|s16|s32|int|unsigned|[A-Z]\w+)\b\s*[*\w]', new):
        # Most regions follow executable statements. Give new temporaries C89
        # block scope without altering proposed expressions or their ordering.
        replacement = '{\n' + replacement.strip() + '\n}'
        if replacement.count('\n') >= 40:
            raise ValueError('C89 scope wrapper would exceed the 40-line limit')
        new = clean(replacement)
    if FORBIDDEN.search(new) or re.search(r'\b(?:pad\w*|nop|incbin)\b', new, re.I):
        raise ValueError('unsupported assembly, preprocessor, volatile, builtin or padding')
    # Literal changes are not needed for equivalent spellings. This also rejects
    # raw opcode arrays, address patches and disguised byte/padding injection.
    constants = lambda text: set(re.findall(r'(?<![\w.])(?:0[xX][\da-fA-F]+|\d+)[uUlL]*|\'(?:\\.|[^\'\\])*\'|"(?:\\.|[^"\\])*"', text))
    if constants(new) - constants(old):
        raise ValueError('new literal constants are outside the permitted spelling search')
    if re.search(r'\b(?:static|extern|typedef)\b', new):
        raise ValueError('replacement may not introduce persistent objects or type declarations')
    if re.search(r'\[[^\]]*\]\s*=\s*\{', new):
        raise ValueError('raw aggregate initializer is outside the spelling search')
    # Prohibit introducing additional calls, IO macros and goto targets. The
    # semantic fixtures below remain necessary for all other behavior changes.
    calls = lambda text: set(re.findall(r'\b(\w+)\s*\(', text)) - {'if', 'for', 'while', 'switch', 'sizeof'}
    if calls(new) - calls(old):
        raise ValueError('replacement introduces a call or function-like macro')
    jumps = lambda text: set(re.findall(r'\bgoto\s+(\w+)', text))
    if jumps(new) - jumps(old):
        raise ValueError('replacement introduces an unstructured jump')
    if len(tokens(new)) > 4 * len(tokens(old)) + 40:
        raise ValueError('replacement is outside the local mutation budget')
    return replacement.strip()


def alternatives(answer):
    """Accept a JSON array/object or four explicit C fences, never prose as C."""
    text = answer.strip()
    fenced_json = re.search(r'```json\s*\n(.*?)```', text, re.S | re.I)
    try:
        value = json.loads(fenced_json[1] if fenced_json else text)
        if isinstance(value, dict):
            value = value.get('alternatives')
        if isinstance(value, list) and all(isinstance(v, str) for v in value):
            return value[:4]
    except (ValueError, TypeError):
        pass
    # A token limit can cut off the fourth JSON string. Preserve only complete
    # strings; never repair or invent the missing C. The next region still gets
    # a fresh request for four alternatives.
    array = re.search(r'"alternatives"\s*:\s*\[', text)
    if array:
        choices, at = [], array.end()
        while len(choices) < 4:
            while at < len(text) and text[at] in ' \r\n\t,':
                at += 1
            try:
                value, end = json.JSONDecoder().raw_decode(text, at)
            except ValueError:
                break
            if not isinstance(value, str):
                break
            choices.append(value)
            at = end
        if choices:
            return choices
    return re.findall(r'```(?:c(?:89|99)?)?[ \t]*\r?\n(.*?)```', text, re.S | re.I)[:4]


def response_diagnostic(answer, kind, batch):
    folder = Path('build/llm-blocks-responses')
    folder.mkdir(exist_ok=True)
    (folder / ('%s-%06d.txt' % (kind, batch))).write_text(answer)


def json_array(answer):
    """Find a structured answer even when a model wraps it in prose/thoughts."""
    decoder = json.JSONDecoder()
    for found in re.finditer(r'\[', answer):
        try:
            value, _ = decoder.raw_decode(answer[found.start():])
            if isinstance(value, list) and value and all(isinstance(p, dict) for p in value):
                return value
        except ValueError:
            continue
    raise ValueError('no complete JSON array in response')


def sanitized_listing(data, start, mode, low, high):
    rows = []
    for line in diffhint.listing(data, start, mode):
        address = int(line.split(':', 1)[0], 16)
        if low <= address < high:
            line = re.sub(r'^(\w+:\s*)[0-9a-fA-F]{4,8}\s+', r'\1', line)
            line = re.sub(r'\.word 0x[0-9A-Fa-f]+ \(literal pool\)', '.word <literal pool>', line)
            rows.append(line)
    return '\n'.join(rows)


def region_declarations(code, name, region):
    """Keep referenced declarations, types, helpers and macro dependencies.

    Address names tokenize expensively. Sending every unrelated record layout
    and a large unused sound macro can consume most of the output allowance.
    Only context is filtered; the compiled candidate always uses the full source.
    """
    _, opening, _ = function_span(code, name)
    shared = (ROOT / 'src/types.h').read_text()
    prefix = shared + '\n' + code[:opening]
    identifiers = lambda text: set(re.findall(r'\b[A-Za-z_]\w*\b', text))
    needed = identifiers(region['text'])
    definitions = {}
    for found in TOKEN.finditer(prefix):
        text = found.group().lstrip()
        macro = re.match(r'#\s*define\s+(\w+)', text)
        if macro:
            # The target branch precedes the synthetic fixture branch.
            definitions.setdefault(macro[1], text)
    ts = tokens(prefix)
    pieces = []
    first, i = 0, 0
    while i < len(ts):
        word = ts[i][0]
        if word == '{':
            end = paired(ts, i)
            is_type = ts[first][0] in ('typedef', 'struct', 'enum', 'union')
            if not is_type:
                text = prefix[ts[first][1]:ts[end][2]]
                header = text.split('{', 1)[0]
                function = re.search(r'(\w+)\s*\(', header)
                if function:
                    pieces.append(({function[1]}, text))
                first = end + 1
            i = end + 1
        elif word == ';':
            text = prefix[ts[first][1]:ts[i][2]]
            if ts[first][0] == 'typedef':
                names = {ts[i - 1][0]}
            else:
                names = set(re.findall(r'\b(?:g_\w+|g[A-Z]\w*|func_\w+|arm_func_\w+)\b', text))
                function = re.search(r'(\w+)\s*\(', text)
                if function:
                    names.add(function[1])
            pieces.append((names, text))
            first = i + 1
            i += 1
        else:
            i += 1
    declarations = [line for line in code[opening + 1:].splitlines()
                    if re.match(r'\s*(?:register\s+)?(?:u8|u16|u32|s8|s16|s32|int|unsigned|'
                                r'[A-Z]\w+)\s+[*\w]', line)]
    selected, macros, locals_ = set(), set(), set()
    changed = True
    while changed:
        changed = False
        for key, text in definitions.items():
            if key in needed and key not in macros:
                macros.add(key)
                needed.update(identifiers(text))
                changed = True
        for index, (names, text) in enumerate(pieces):
            if names & needed and index not in selected:
                selected.add(index)
                needed.update(identifiers(text))
                changed = True
        for index, text in enumerate(declarations):
            # Match variable tokens, never a common type token on its own.
            names = identifiers(re.sub(r'^\s*(?:register\s+)?\w+\s+', '', text))
            if names & needed and index not in locals_:
                locals_.add(index)
                needed.update(identifiers(text))
                changed = True
    compact = lambda text: re.sub(r'\n\s*\n', '\n', re.sub(r'/\*.*?\*/', '', text, flags=re.S))
    global_text = '\n'.join(text for i, (_, text) in enumerate(pieces) if i in selected)
    macro_text = '\n'.join(text for key, text in definitions.items() if key in macros)
    return compact(global_text + '\n' + macro_text), '\n'.join(
        text for i, text in enumerate(declarations) if i in locals_)


def prompt_for(code, name, region, want, actual, start, profile, feedback):
    global_text, declarations = region_declarations(code, name, region)
    idioms = json.loads((ROOT / 'tools/matching_patterns.json').read_text())
    idioms = '\n'.join(str(p['mismatch']) + ' => ' + str(p['transformation']) for p in idioms)
    fewshot = sorted((ROOT / 'tools/fewshot').glob('*.c'),
                     key=lambda p: abs(int(p.stem.split('_')[-1], 16) - start))[:2]
    examples = '\n'.join(p.read_text() + '\n' + (p.with_suffix('.md').read_text()
                         if p.with_suffix('.md').exists() else '') for p in fewshot)
    low = start + min(a for a, _ in region['machine_spans'])
    high = start + max(b for _, b in region['machine_spans'])
    mode = 'arm' if profile == 'arm' else 'thumb'
    return (f'Recover equivalent C89 spellings of ONE region in {name}. Compiler profile: '
            f'{profile}, -O2 -mthumb-interwork, {mode}. Return a JSON object with key alternatives: '
            'exactly four C source strings, each only a replacement region of at most 40 lines. '
            'No markdown fences, explanation, comments, function wrapper or new '
            'global declarations. Preserve all behavior, memory access widths, helper calls and their order. '
            'No assembly, raw bytes, padding, builtins, new literal constants, volatile, preprocessor '
            'directives, register bindings or artificial effects. Existing macros may be used unchanged. '
            'New temporaries must be declared at the start of a new inner block. Work on loop form, '
            'temporary lifetime, expression grouping, signedness or branch layout. Each alternative '
            'must differ from the original and each other. Make only one local change per alternative. '
            'Do not repeat spellings already rejected below. '
            'The source map attributes positional byte differences; shifted instructions can affect the mapping.\n'
            f'Region lines {region["first_line"]}-{region["last_line"]}; '
            f'{region["different_bytes"]} attributed differing bytes.\n'
            'Types u8/u16/u32 and s8/s16/s32 are unsigned/signed integers of the named bit width.\n'
            'Referenced types, globals, helpers and macros:\n' + global_text + '\n'
            'Local declarations (retain their scope; do not replace these globally):\n' + declarations + '\n'
            'Current region:\n```c\n' + region['text'] + '\n```\n'
            'Target disassembly for the mapped window:\n' + sanitized_listing(want, start, mode, low, high) + '\n'
            'Current disassembly for that window:\n' + sanitized_listing(actual, start, mode, low, high) + '\n'
            'House idioms:\n' + idioms + '\nFew-shot examples:\n' + examples + '\n'
            'Recent attempt feedback:\n' + '\n'.join(feedback[-8:]))


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def semantic_check(address, source):
    """Run fixtures in a bounded worker, including native ARM-candidate calls.

    A model can accidentally propose a nonterminating loop or invalid pointer.
    Keeping native fixtures outside the search process preserves its checkpoint
    even on a crash. The worker's alarm bounds native calls as well as Python.
    """
    with tempfile.TemporaryDirectory(prefix='blocks-fixtures-', dir='build') as folder:
        command = [sys.executable, str(Path(__file__).resolve()), '--check-source', address,
                   str(Path(source).resolve()), str(Path(folder).resolve())]
        result = subprocess.run(command, capture_output=True, text=True, timeout=100)
    if result.returncode:
        detail = (result.stderr.strip() or 'fixture worker terminated (%d)' % result.returncode)[-1500:]
        raise RuntimeError(detail.replace(str(ROOT), '<checkout>'))
    return json.loads(result.stdout)


def semantic_worker(address, source):
    if address in ('0800421C', '080064A4'):
        folder = 'hud-owner-1109' if address == '0800421C' else 'sound-owner-1109'
        return load_module(ROOT / 'docs/near-misses' / folder / 'check_source.py',
                           'block_check_' + address).check(source)
    # The ARM fixture loader resolves its selected source through HERE while
    # its independent instruction oracle stays rooted at the original checkout.
    module = load_module(ROOT / 'docs/near-misses/arm-16da8-1107/check_semantics.py', 'block_arm_check')
    with tempfile.TemporaryDirectory(prefix='blocks-arm-', dir='build') as folder:
        module.HERE = Path(folder).resolve()
        (module.HERE / 'func_08016DA8.c').symlink_to(Path(source).resolve())
        previous = sys.argv
        try:
            sys.argv = ['check_semantics.py', '--candidate', 'func_08016DA8.c']
            output = io.StringIO()
            with contextlib.redirect_stdout(output):
                module.main()
            return json.loads(output.getvalue())
        finally:
            sys.argv = previous


def verify_environment():
    if subprocess.check_output(['git', 'branch', '--show-current'], text=True).strip() != 'work/local-1111':
        raise ValueError('this search is pinned to work/local-1111')
    if hashlib.sha1(Path('baserom.gba').read_bytes()).hexdigest() != '4197339d4add74bb40ed02a8fba5e58096afb487':
        raise ValueError('private ROM identity mismatch')
    if not match.toolchain_ready() or not match.CC.with_name('agbcc_arm').exists():
        raise ValueError('historical compiler profiles unavailable')
    if os.statvfs('.').f_bavail * os.statvfs('.').f_frsize < 20 * 1024 ** 3:
        raise ValueError('less than the required 20 GiB storage reserve')


def prepare(state):
    state.setdefault('schema', 1)
    state.setdefault('attempts', 0)
    state.setdefault('requests', 0)
    state.setdefault('targets', {})
    state.setdefault('installed', [])
    state.setdefault('batch', 0)
    state.setdefault('next_target', 0)
    state.setdefault('owner_notes_sha256', sha(owner_notes()))
    for address, (stem, previous, end, profile) in TARGETS.items():
        if address in state['targets']:
            record = state['targets'][address]
            if sha(Path(record['source']).read_text()) != record['source_sha256']:
                # Recover a hard interruption after source adoption but before
                # its status write. Only frozen, independently reproduced
                # evidence authorizes recovery; arbitrary external edits fail.
                directory = Path(record['source']).parent
                profile_path, checks_path = directory / 'candidate.json', directory / 'candidate-checks.json'
                frozen = json.loads(profile_path.read_text())
                frozen_checks = json.loads(checks_path.read_text())
                current_sha = sha(Path(record['source']).read_text())
                if (current_sha != frozen['source_sha256'] or current_sha != frozen_checks['source_sha256'] or
                        frozen['different_bytes'] >= record['best']):
                    raise ValueError('retained candidate changed outside checkpoint: ' + address)
                reproduced = measure.measure(record['source'], int(address, 16), end, profile)
                semantic_check(address, Path(record['source']))
                if reproduced['compiled_sha256'] != frozen['compiled_sha256'] or reproduced['checker_rejection']:
                    raise ValueError('interrupted candidate failed recovery: ' + address)
                record.update(source_sha256=current_sha, best=reproduced['different_bytes'], visits={})
                record['improvements'] += 1
                save(state)
                log('recovered_candidate', address=address, different_bytes=record['best'])
            continue
        directory = Path('docs/near-misses') / (stem + '-1111')
        directory.mkdir(parents=True, exist_ok=True)
        source = directory / ('func_' + address + '.c')
        previous_source = Path('docs/near-misses') / previous / source.name
        # Never overwrite an untracked source left by an interrupted preparation.
        if not source.exists():
            source.write_text(previous_source.read_text())
        result = measure.measure(source, int(address, 16), end, profile, directory / 'candidate')
        checks = semantic_check(address, source)
        atomic(directory / 'candidate-checks.json', checks)
        baseline = dict(result, source=str(previous_source))
        atomic(directory / 'baseline.json', baseline)
        atomic(directory / 'baseline-checks.json', checks)
        state['targets'][address] = dict(source=str(source), source_sha256=result['source_sha256'],
                                        before=result['different_bytes'], best=result['different_bytes'],
                                        attempts=0, compiled=0, improvements=0, visits={}, seen=[], feedback=[],
                                        profile=profile, end='%08X' % end)
        save(state)
        log('baseline', address=address, different_bytes=result['different_bytes'], profile=profile)
    return state


def next_target(state, proof, rotation):
    hud = state['targets']['0800421C']
    if hud['compiled'] < proof and '0800421C' not in state['installed']:
        return '0800421C'
    addresses = list(TARGETS)
    # Following proof, start at sound then ARM, then return to HUD.
    sequence = [addresses[1], addresses[2], addresses[0]]
    while True:
        address = sequence[state['next_target'] % len(sequence)]
        if address not in state['installed']:
            return address
        state['next_target'] += 1
        if len(state['installed']) == len(TARGETS):
            return None


def new_batch(state, program, address, model):
    record = state['targets'][address]
    source = Path(record['source'])
    code = source.read_text()
    if sha(code) != record['source_sha256']:
        raise ValueError('retained source changed outside its checkpoint: ' + address)
    start, end = int(address, 16), int(record['end'], 16)
    table = reloc.symbols(program)
    actual, _ = measure.diagnostic_compile(code, 'func_' + address, start, table, record['profile'])
    want = program.rom[start - match.BASE:end - match.BASE]
    locations = source_locations(code, 'func_' + address, record['profile'], start, table, actual)
    # Sixteen original lines leave room for four actual mutations rather than
    # four long repetitions. Replacements may still use the brief's 40 lines.
    ranked = rank_regions(code, 'func_' + address, locations, want, actual, record['visits'], max_lines=16)
    if not ranked:
        raise ValueError('no differing mapped source region: ' + address)
    for region in ranked:
        prompt = prompt_for(code, 'func_' + address, region, want, actual, start, record['profile'], record['feedback'])
        # Keep room in the 16k context for all four alternatives. Expanded
        # statement macros can cover far more code than their few source lines.
        # Select the worst region that fits, keeping both listings complete.
        if len(prompt) <= PROMPT_CHARACTER_LIMIT:
            break
    else:
        raise ValueError('no complete mapped region fits the bounded model context')
    state['current'] = dict(address=address, model=model, first_line=region['first_line'],
                            last_line=region['last_line'], stage='waiting for model')
    save(state)
    schema = {'type': 'object', 'properties': {'alternatives': {
        'type': 'array', 'items': {'type': 'string'}, 'minItems': 4, 'maxItems': 4}}, 'required': ['alternatives']}
    answer = match.ask(prompt, model, max_wait=None, poll=60,
                       num_predict=6144 if CONTEXT_TOKENS == 16384 else 2048,
                       num_ctx=CONTEXT_TOKENS, response_format=schema)
    response_diagnostic(answer, 'blocks', state['batch'] + 1)
    choices = alternatives(answer)
    state['requests'] += 1
    state['batch'] += 1
    record['visits'][region['identity']] = record['visits'].get(region['identity'], 0) + 1
    if len(choices) != 4:
        log('response_incomplete', address=address, model=model, alternatives=len(choices),
            reason='expected four C alternatives')
        record['feedback'].append('Last response had %d alternatives; provide exactly four C strings.' % len(choices))
        record['feedback'] = record['feedback'][-12:]
        state['invalid_responses'] = state.get('invalid_responses', 0) + 1
        save(state)
        if not choices:
            return
    pending = dict(address=address, model=model, base_source=code, base_sha256=sha(code),
                   region=region, choices=choices, next=0, batch=state['batch'])
    atomic(PENDING, pending)
    save(state)


def try_install(program, address, code, result):
    if not result['exact'] or result['checker_rejection'] or result['emitted_bytes'] != result['target_bytes']:
        return False
    # The existing installer recompiles EVERY registered replacement and checks
    # the whole-ROM SHA-1. Any failed gate rolls source/config back itself.
    match.install(code, 'func_' + address, int(address, 16), result['emitted_bytes'], result['compiler'])
    if program is not None:
        program.cfg = json.loads(Path('tools/rom.cfg').read_text())
        program.matched = {match.BASE + m['offset']: m for m in program.cfg['matches']}
        try:
            refresh_counts()
        except (ValueError, OSError, subprocess.SubprocessError) as exc:
            # Installation has already passed its gates. Keep that fact even if
            # an unrelated bookkeeping command fails, and expose the problem.
            log('bookkeeping_error', address=address, reason=type(exc).__name__)
    return True


def refresh_counts():
    subprocess.run([sys.executable, 'tools/progress.py'], capture_output=True, text=True, check=True, timeout=120)
    progress = json.loads(Path('progress.json').read_text())
    matched = progress['functions_matched_c']
    count, total = matched['count'], progress['functions_mapped']
    code, code_total = matched['bytes_including_pools'], progress['code_bytes_mapped']
    text = Path('README.md').read_text()
    content = ('<!-- progress:start -->\n'
               f'**{count} of {total} functions** match the original compiler output byte for byte '
               f'({100 * count / total:.1f}% of functions), covering **{100 * code / code_total:.1f}% '
               f'of the game code** ({code:,} of {code_total:,} bytes).\n\n'
               'Uninstalled candidates and their byte-distance scores do not count as exact matches.\n'
               '<!-- progress:end -->')
    updated, changed = re.subn(r'<!-- progress:start -->.*?<!-- progress:end -->', content, text, flags=re.S)
    if changed != 1:
        raise ValueError('README progress block missing or ambiguous')
    Path('README.md').write_text(updated)


def judge_pending(state, program, max_judged=0):
    pending = json.loads(PENDING.read_text())
    address = pending['address']
    record = state['targets'][address]
    directory = Path(record['source']).parent
    region = pending['region']
    base = pending['base_source']
    for index in range(pending['next'], len(pending['choices'])):
        if sha(Path(record['source']).read_text()) != record['source_sha256']:
            raise ValueError('retained source changed while a model request was pending: ' + address)
        if max_judged and sum(t['compiled'] for t in state['targets'].values()) >= max_judged:
            return
        choice = pending['choices'][index]
        raw_choice = choice
        before, result, checks = record['best'], None, None
        reason, retained = None, False
        old_mask = None
        identity = None
        scope_wrapper = False
        state['current'] = dict(address=address, model=pending['model'], stage='judging',
                                batch=pending['batch'], alternative=index + 1,
                                first_line=region['first_line'], last_line=region['last_line'])
        save(state)
        try:
            choice = safe_region(region['text'], choice)
            scope_wrapper = choice.startswith('{') and not raw_choice.lstrip().startswith('{')
            trial = base[:region['begin']] + choice + base[region['end']:]
            identity = sha(trial)
            token_identity = sha(' '.join(t[0] for t in tokens(trial)))
            base_tokens = sha(' '.join(t[0] for t in tokens(base)))
            token_seen = record.setdefault('token_seen', [])
            if (identity == pending['base_sha256'] or identity in record['seen'] or
                    token_identity == base_tokens or token_identity in token_seen):
                reason = 'duplicate source; not compiled again'
            else:
                token_seen.append(token_identity)
                with tempfile.TemporaryDirectory(prefix='blocks-judge-', dir='build') as folder:
                    path = Path(folder) / ('func_' + address + '.c')
                    path.write_text(trial)
                    result = measure.measure(path, int(address, 16), int(record['end'], 16), record['profile'])
                    record['compiled'] += 1
                    # Check even regressing compiled variants to expose and
                    # report invalid behavior instead of treating it as distance.
                    checks = semantic_check(address, path)
                    if result['checker_rejection']:
                        reason = result['checker_rejection']
                    elif result['different_bytes'] >= before:
                        reason = 'no strict whole-function byte-distance improvement'
                    else:
                        # Finish source/evidence/checkpoint adoption before a
                        # requested stop. Compilation and remote waits remain
                        # interruptible; the short adoption transaction does not.
                        old_mask = signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGTERM, signal.SIGINT})
                        # Freeze all evidence before changing the retained source.
                        measure.measure(path, int(address, 16), int(record['end'], 16),
                                        record['profile'], directory / 'candidate')
                        result['source'] = record['source']
                        result['installed'] = False
                        atomic(directory / 'candidate.json', result)
                        atomic(directory / 'candidate-checks.json', checks)
                        # Retained revisions are plain C, never object payloads.
                        history = directory / 'improvements'
                        history.mkdir(exist_ok=True)
                        revision = history / ('%06d-%d.c' % (state['attempts'] + 1, result['different_bytes']))
                        revision.write_text(trial)
                        Path(record['source']).write_text(trial)
                        record['best'] = result['different_bytes']
                        record['source_sha256'] = identity
                        record['improvements'] += 1
                        record['visits'] = {}
                        retained = True
                        if try_install(program, address, trial, result):
                            state['installed'].append(address)
                            result['installed'] = True
                            atomic(directory / 'candidate.json', result)
                record['seen'].append(identity)
        except (ValueError, RuntimeError, AssertionError, subprocess.SubprocessError) as exc:
            # Model responses and compiler stderr stay local; never embed a
            # printed opcode or host path in committed receipts.
            detail = (exc.stderr or str(exc)) if isinstance(exc, subprocess.CalledProcessError) else str(exc)
            detail = re.sub(re.escape(str(Path.home())) + r'/[^\s:\'"\]]+', '<local>',
                            detail.replace(str(ROOT), '<checkout>'))
            diagnostic = [line.strip() for line in detail.splitlines()
                          if any(word in line.lower() for word in ('error', 'undeclared', 'warning', 'regression', 'assertion'))]
            reason = type(exc).__name__ + ': ' + ('; '.join(diagnostic[:2]) or detail[-500:])[:500]
        state['attempts'] += 1
        record['attempts'] += 1
        entry = dict(attempt=state['attempts'], address=address, model=pending['model'],
                     batch=pending['batch'], alternative=index + 1,
                     region=[region['first_line'], region['last_line']], region_sha256=region['identity'],
                     bytes_before=before, bytes_after=result['different_bytes'] if result else None,
                     compiled=result is not None, semantics_passed=checks is not None,
                     retained=retained, reason=reason, source_sha256=identity,
                     tool_sha256=state.get('tool_sha256'), c89_scope_wrapper=scope_wrapper)
        log('attempt', **entry)
        record['feedback'].append('Region %d-%d alternative %d (%s): %s -> %s; %s' % (
            region['first_line'], region['last_line'], index + 1, sha(choice)[:12], before,
            entry['bytes_after'], 'retained' if retained else str(reason)[-220:]))
        record['feedback'] = record['feedback'][-12:]
        # Checkpoint status first, then pending cursor. A crash between them is
        # reconciled by the batch/alternative receipt on resume (see recover).
        state['last_judged'] = [pending['batch'], index]
        save(state)
        pending['next'] = index + 1
        atomic(PENDING, pending)
        if old_mask is not None:
            signal.pthread_sigmask(signal.SIG_SETMASK, old_mask)
    PENDING.unlink()


def recover_pending(state):
    if not PENDING.exists():
        return
    pending = json.loads(PENDING.read_text())
    last = state.get('last_judged')
    if last and last[0] == pending['batch']:
        pending['next'] = max(pending['next'], last[1] + 1)
        atomic(PENDING, pending)


def matched_source(program, address):
    record = program.matched[address]
    text = Path(record.get('source', 'src/leaves.c')).read_text()
    # Some exact entries are registered against a compilation unit consisting
    # of quoted includes. Read the matching source, without preprocessing away
    # the useful address-named C or accidentally selecting a prototype.
    if not re.search(r'\b' + re.escape(record['name']) + r'\s*\(', text):
        parent = Path(record.get('source', 'src/leaves.c')).parent
        for include in re.findall(r'^\s*#include\s+"([^"\n]+)"', text, re.M):
            included = parent / include
            if included.exists() and re.search(r'\b' + re.escape(record['name']) + r'\s*\(', included.read_text()):
                text = included.read_text()
                break
    a, _, b = function_span(text, record['name'])
    return text[a:b]


def render_names(records, program):
    lines = ['# Matched function naming proposals, 11 November', '',
             'Unreviewed local proposals only; source symbols are unchanged. Confidence describes '
             'the proposed description, not proof of game semantics. Every proposal uses the matched C '
             'and its disassembly; evidence excerpts are explicitly marked for larger functions. '
             'Address suffixes distinguish repeated proposals without adding a new semantic claim.', '',
             '| Address | Current name | Proposed name | Description | Confidence |',
             '| --- | --- | --- | --- | --- |']
    for address, record in sorted(program.matched.items()):
        if not record['name'].startswith('func_'):
            continue
        proposal = records.get('%08X' % address)
        if not proposal:
            fields = ['%08X' % address, record['name'], 'pending', 'Awaiting local service.', 'pending']
        else:
            description = proposal['description'] + (' (excerpt evidence)' if proposal.get('evidence') == 'excerpts' else '')
            fields = ['%08X' % address, record['name'], proposal['name'], description, proposal['confidence']]
        lines.append('| ' + ' | '.join(str(v).replace('|', '/').replace('\n', ' ') for v in fields) + ' |')
    Path('docs/names-1111.md').write_text('\n'.join(lines) + '\n')


def name_batch(state, program, model, count=1):
    records = json.loads(NAMES.read_text()) if NAMES.exists() else {}
    visits = state.setdefault('naming_visits', {})
    addresses = sorted([a for a, m in program.matched.items()
                        if m['name'].startswith('func_') and '%08X' % a not in records],
                       key=lambda a: (visits.get('%08X' % a, 0), a))[:count]
    if not addresses:
        render_names(records, program)
        return False
    evidence = []
    for address in addresses:
        source = matched_source(program, address)
        mode = program.by_start[address]['mode']
        m = program.matched[address]
        data = program.rom[address - match.BASE:address - match.BASE + m['size']]
        listing = sanitized_listing(data, address, mode, address, address + len(data))
        partial = len(source) + len(listing) > (18000 if CONTEXT_TOKENS == 16384 else 7000)
        if partial:
            head, tail = (6500, 1500) if CONTEXT_TOKENS == 16384 else (2500, 500)
            source = source[:head] + '\n/* middle omitted */\n' + source[-tail:]
            listing = listing[:head] + '\n... middle omitted ...\n' + listing[-tail:]
        evidence.append(dict(address='%08X' % address, current_name=m['name'], c=source,
                             disassembly=listing, evidence='excerpts' if partial else 'complete'))
        if sum(len(str(e)) for e in evidence) > 23000:
            break
    prompt = ('Propose short descriptive snake_case C function names for these byte-matched functions. '
              'This is a vehicle racing game. Prefer generic slot, table, flag and dispatch descriptions '
              'when the meaning of state is not established. '
              'Use only the supplied C and disassembly. No place names or brand names. Describe observable behavior; do not invent '
              'game semantics. Return ONLY a JSON object with a proposals array, one object per address, keys: address, name, '
              'description (one short sentence), confidence (low/medium/high). Name the supplied outer function, '
              'never one of its callees. Preserve its exact supplied address. Use a descriptive name, never func_XXXXXXXX. '
              'No renaming is performed.\n' +
              json.dumps(evidence))
    state['current'] = dict(stage='naming', addresses=[e['address'] for e in evidence], model=model)
    save(state)
    schema = {'type': 'object', 'properties': {'proposals': {'type': 'array', 'items': {
        'type': 'object', 'properties': {key: {'type': 'string'} for key in
        ('address', 'name', 'description', 'confidence')}, 'required': ['address', 'name', 'description', 'confidence']}}},
        'required': ['proposals']}
    schema['properties']['proposals']['items']['properties']['confidence']['enum'] = ['low', 'medium', 'high']
    response = match.ask(prompt, model, max_wait=None, poll=60, response_format=schema, num_ctx=CONTEXT_TOKENS)
    state['naming_requests'] = state.get('naming_requests', 0) + 1
    response_diagnostic(response, 'names', state['naming_requests'])
    for e in evidence:
        visits[e['address']] = visits.get(e['address'], 0) + 1
    try:
        proposals = json_array(response)
        allowed = {e['address']: e['evidence'] for e in evidence}
        if not isinstance(proposals, list):
            raise ValueError('expected naming array')
        for p in proposals:
            address = str(p.get('address', '')).removeprefix('0x').upper()
            # Formatting a proposed identifier is not a new semantic proposal.
            name = p.get('name', '')
            if re.fullmatch(r'func[0-9a-f]{8}', name.replace('_', ''), re.I):
                continue
            name = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', name)
            name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name).lower()
            if address not in allowed or not re.fullmatch(r'[a-z][a-z_0-9]{2,55}', name) or re.fullmatch(r'func_[0-9a-f]{8}', name):
                continue
            description = p.get('description', '')
            if not isinstance(description, str) or len(description) < 3:
                continue
            description = re.split(r'(?<=[.!?])\s+', ' '.join(description.split()))[0]
            if len(description) > 240:
                description = description[:237].rsplit(' ', 1)[0] + '...'
            if p.get('confidence') not in ('low', 'medium', 'high'):
                continue
            confidence = 'low' if allowed[address] == 'excerpts' else p['confidence']
            records[address] = dict(name=name, description=description, confidence=confidence,
                                    evidence=allowed[address], model=model)
        atomic(NAMES, records)
    except (ValueError, TypeError, AttributeError):
        log('naming_response_rejected', model=model)
    render_names(records, program)
    state['names_proposed'] = len(records)
    save(state)
    log('naming', total=len(records), model=model)
    return True


def main(argv=None):
    global CONTEXT_TOKENS, PROMPT_CHARACTER_LIMIT
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare', action='store_true', help='verify and retain all baselines without service requests')
    parser.add_argument('--names-only', action='store_true')
    parser.add_argument('--status', action='store_true', help='read the running checkpoint without acquiring its lock')
    parser.add_argument('--stop', action='store_true', help='signal only the checkpoint owner after PID/start-time verification')
    parser.add_argument('--max-judged', type=int, default=0, help='total successfully measured alternatives; zero means unattended')
    parser.add_argument('--hud-proof', type=int, default=200)
    parser.add_argument('--rotation-attempts', type=int, default=40)
    parser.add_argument('--names-every', type=int, default=4, help='one naming batch after N mutation batches; zero disables')
    parser.add_argument('--context-tokens', type=int, choices=(8192, 16384), default=16384,
                        help='smaller requests for a service under memory pressure; never changes compiler profiles')
    args = parser.parse_args(argv)
    CONTEXT_TOKENS = args.context_tokens
    PROMPT_CHARACTER_LIMIT = 18000 if CONTEXT_TOKENS == 16384 else 9000
    if args.hud_proof < 200 or args.rotation_attempts < 4 or args.names_every < 0:
        parser.error('HUD proof must be at least 200; rotation at least four; names interval nonnegative')
    os.chdir(ROOT)
    if args.status or args.stop:
        if not STATE.exists():
            parser.error('no checkpoint exists')
        state = json.loads(STATE.read_text())
        if args.stop:
            pid = state.get('pid')
            if not owner_alive(state):
                parser.error('checkpoint owner is not running or its PID identity changed; no signal sent')
            os.kill(pid, signal.SIGTERM)
            print('Stop requested for checkpoint owner PID %d.' % pid)
        else:
            summary = {k: state.get(k) for k in ('pid', 'running', 'updated', 'current', 'service',
                       'attempts', 'requests', 'names_proposed', 'installed', 'error')}
            summary['process_alive'] = owner_alive(state)
            print(json.dumps(summary, indent=2))
            for address, record in state.get('targets', {}).items():
                print('%s: %d -> %d differing bytes; %d measured, %d proposed' % (
                    address, record['before'], record['best'], record['compiled'], record['attempts']))
        return 0
    Path('build').mkdir(exist_ok=True)
    signal.signal(signal.SIGTERM, stop)
    signal.signal(signal.SIGINT, stop)
    with Path('build/llm-blocks.lock').open('w') as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            parser.error('a block search already owns this checkout')
        state = json.loads(STATE.read_text()) if STATE.exists() else {}
        try:
            verify_environment()
            state = prepare(state)
            recover_pending(state)
            state.update(pid=os.getpid(), process_start_ticks=Path('/proc/self/stat').read_text().split()[21],
                         running=True, started=now(), stopped=None,
                         tool_sha256=sha(Path(__file__).read_text()), context_tokens=CONTEXT_TOKENS)
            state.pop('error', None)
            save(state)
            program = draft.Program()
            render_names(json.loads(NAMES.read_text()) if NAMES.exists() else {}, program)
            # Existing service helper retains its shared lock and etiquette.
            # Redirect its retry notices into this runner's structured log.
            def service_log(message):
                state['service'] = dict(time=now(), message=message)
                save(state)
                log('service', message=message)
            match.log = service_log
            if args.prepare:
                return 0
            while True:
                if sha(owner_notes()) != state['owner_notes_sha256']:
                    state['needs_owner_note_review'] = True
                    log('paused_for_owner_notes', reason='new owner notes require human task review')
                    break
                if args.names_only:
                    if not name_batch(state, program, match.MODELS[0]):
                        break
                    continue
                if args.max_judged and sum(t['compiled'] for t in state['targets'].values()) >= args.max_judged:
                    break
                address = next_target(state, args.hud_proof, args.rotation_attempts)
                if address is None:
                    break
                target = state['targets'][address]
                previous_attempts = target['compiled']
                if not PENDING.exists():
                    # Primary first, with one second-opinion batch after eight
                    # primary batches. Consecutive primary requests stay warm.
                    model = match.MODELS[1] if len(match.MODELS) > 1 and state['batch'] % 9 == 8 else match.MODELS[0]
                    new_batch(state, program, address, model)
                if sha(owner_notes()) != state['owner_notes_sha256']:
                    state['needs_owner_note_review'] = True
                    log('paused_for_owner_notes', reason='new notes arrived during the request; pending alternatives preserved')
                    break
                if PENDING.exists():
                    judge_pending(state, program, args.max_judged)
                if target['compiled'] > previous_attempts and state['targets']['0800421C']['compiled'] >= args.hud_proof:
                    rotation = state.setdefault('rotation_progress', {})
                    rotation[address] = rotation.get(address, 0) + target['compiled'] - previous_attempts
                    if rotation[address] >= args.rotation_attempts:
                        rotation[address] = 0
                        state['next_target'] += 1
                if args.names_every and state['batch'] and state['batch'] % args.names_every == 0:
                    for _ in range(4):
                        if not name_batch(state, program, match.MODELS[0]):
                            break
                save(state)
        except StopRequested:
            log('stopped', reason='signal; pending batch preserved')
        except Exception as exc:
            state['error'] = type(exc).__name__ + ': ' + str(exc).replace(str(ROOT), '<checkout>')[:500]
            log('error', reason=state['error'])
            return 1
        finally:
            state.update(running=False, stopped=now())
            save(state)
    return 0


if __name__ == '__main__':
    if len(sys.argv) == 5 and sys.argv[1] == '--check-source':
        os.chdir(ROOT)
        tempfile.tempdir = sys.argv[4]
        signal.alarm(90)
        print(json.dumps(semantic_worker(sys.argv[2], Path(sys.argv[3]))))
    else:
        sys.exit(main())

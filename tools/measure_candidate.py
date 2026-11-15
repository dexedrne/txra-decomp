#!/usr/bin/env python3
"""Measure a complete C owner without installing it or retaining binary data.

The normal checker always receives the exact owner end as its output limit.
Oversized compiler output is separately measured as a rejected diagnostic; it
never receives a larger checker boundary. All temporary compiler files vanish.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'recomp'))
import draft
import diffhint
import llm_match as match
import reloc
import variant_search


def digest(data):
    return hashlib.sha256(data).hexdigest()


def diagnostic_compile(code, name, start, table, profile):
    """Compile C only; this routine has no admission or installation authority."""
    if profile not in ('old', 'arm'):
        raise ValueError('this pass uses only the existing historical profiles')
    if re.search(r'\b(?:asm|__asm__)\s*\(', code):
        raise ValueError('structured C only')
    compiler = match.CC.with_name('agbcc_arm') if profile == 'arm' else match.CC
    with tempfile.TemporaryDirectory(prefix='measure-', dir='build') as td:
        folder = Path(td)
        source = code if 'typedef unsigned char u8;' in code else match.PRELUDE + code
        (folder / 'trial.c').write_text(source)
        match.run([match.ARM + 'gcc', '-E', '-P', '-Isrc', folder / 'trial.c',
                   '-o', folder / 'trial.i'])
        match.run([compiler, folder / 'trial.i', '-O2', '-mthumb-interwork',
                   '-o', folder / 'trial.s'])
        assembly = (folder / 'trial.s').read_text()
        begin = re.search(r'(?m)^' + re.escape(name) + ':', assembly).start()
        tail = assembly[begin:]
        end = re.search(r'\n\s*\.size\s+' + re.escape(name) + r',[^\n]*', tail).end()
        preamble = '.syntax divided\n.text\n' + ('.arm\n' if profile == 'arm' else '.thumb\n')
        (folder / 'one.s').write_text(preamble + tail[:end] + '\n')
        match.run([match.ARM + 'as', '-mcpu=arm7tdmi', folder / 'one.s', '-o', folder / 'one.o'])
        match.run([match.ARM + 'objcopy', '-O', 'binary', '-j', '.text',
                   folder / 'one.o', folder / 'one.bin'])
        obj = folder / 'one.o'
        actual = reloc.function_bytes(obj, (folder / 'one.bin').read_bytes(), name,
                                      match.ARM + 'objdump')
        entries = reloc.parse(match.run([match.ARM + 'objdump', '-r', obj]).stdout)
        actual = reloc.relocate(actual, entries, start, table) if entries else actual
        frame = re.search(r'frame = (\d+)', assembly)
        if frame is None and profile == 'old':
            frame = re.search(r'add\s+sp, sp, #-(\d+)', assembly)
        return actual, int(frame[1]) if frame else None


def sanitized_diff(want, actual, start, mode):
    text = diffhint.hint(want, actual, start, rows=100000, mode=mode)
    # Thumb BL listings use one space after an eight-digit encoding; ordinary
    # Thumb/ARM rows use wider spacing. Remove both, including diff +/- rows.
    text = re.sub(r'(?m)^([ +\-]?\w{8}:\s*)[0-9A-Fa-f]{4,8}\s+', r'\1', text)
    return re.sub(r'\.word 0x[0-9A-Fa-f]+ \(literal pool\)',
                  '.word <literal pool>', text) + '\n'


def measure(source, start, end, profile, destination=None):
    Path('build').mkdir(exist_ok=True)
    source = Path(source)
    code = source.read_text()
    program = draft.Program()
    table = reloc.symbols(program)
    name = 'func_%08X' % start
    actual, frame = diagnostic_compile(code, name, start, table, profile)
    expected = program.rom[start - match.BASE:end - match.BASE]
    rejection = None
    try:
        checked = match.compile_candidate(code, name, start, end, table,
                                          target_end=end, compiler=profile, rom=program.rom)
        assert checked[4] == actual.hex()
        assert checked[3] == expected.hex()
        equal = checked[0]
    except ValueError as exc:
        if str(exc) != 'output crosses next candidate boundary':
            raise
        assert start + len(actual) > end
        rejection = str(exc)
        equal = False
    mode = 'arm' if profile == 'arm' else 'thumb'
    score = variant_search.score(expected, actual, start, mode)
    compiler = match.CC.with_name('agbcc_arm') if profile == 'arm' else match.CC
    result = dict(address='%08X' % start, target_end='%08X' % end, compiler=profile,
                  flags=['-O2', '-mthumb-interwork'], source=source.as_posix(),
                  source_sha256=digest(code.encode()), compiler_sha256=digest(compiler.read_bytes()),
                  emitted_bytes=len(actual), target_bytes=len(expected), local_frame_bytes=frame,
                  instruction_distance=score[0], different_bytes=score[1], exact=equal,
                  compiled_sha256=digest(actual), checker_limit='%08X' % end,
                  checker_rejection=rejection, installed=False)
    if destination is not None:
        destination = Path(destination)
        destination.with_suffix('.json').write_text(json.dumps(result, indent=2) + '\n')
        destination.with_suffix('.diff.txt').write_text(sanitized_diff(expected, actual, start, mode))
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('start', type=lambda value: int(value, 16))
    parser.add_argument('end', type=lambda value: int(value, 16))
    parser.add_argument('profile', choices=('old', 'arm'))
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    print(json.dumps(measure(args.source, args.start, args.end, args.profile, args.destination), indent=2))


if __name__ == '__main__':
    main()

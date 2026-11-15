"""Queue lifetime grids; compile ordinary C and retain measured comparisons."""
import concurrent.futures as futures
import itertools
import json
import os
from pathlib import Path
import time
import variant_search as vs

ROOT = Path(__file__).resolve().parents[1]


def candidates():
    seed = (ROOT / 'docs/match7-search/queue_work/func_08015DA8.c').read_text()
    start = seed.index('        work = offset')
    end = seed.index('        cursor +=')
    # Separate pseudo-register creation from the eventual memory loads. Reusing
    # a loaded value for the next address changes interference/coalescing.
    for address, load, count, mask, read in itertools.product(
        ['work = offset + destbase;',
         'work = destbase; work += offset;',
         'dest = destbase; work = offset + dest;',
         'count = destbase; work = offset + count;',
         'count = destbase; dest = offset + count;',
         'dest = offset + destbase;'],
        ['dest = *(u32 *)work;', 'dest = *(u32 *)dest;',
         'work = *(u32 *)work; dest = work;',
         'count = *(u32 *)work; dest = count;'],
        ['work = base; work += 8; { u32 addend = work; work = offset + addend; } count = *(u32 *)work;',
         'count = base; count += 8; work = offset + count; count = *(u32 *)work;',
         'count = base; count += 8; count = offset + count; count = *(u32 *)count;',
         'work = base; work += 8; count = offset + work; count = *(u32 *)count;',
         '{ u32 addr = base; addr += 8; work = offset + addr; } count = *(u32 *)work;'],
        ['count >>= 2; work = 0x84000000; count |= work;',
         'count >>= 2; source = 0x84000000; count |= source;',
         'count >>= 2; dest = 0x84000000; count |= dest;',
         'work = count >> 2; count = 0x84000000; count |= work;',
         'count = (count >> 2) | 0x84000000;'],
        ['dma[2];', 'work = dma[2];', 'dest = dma[2];', 'count = dma[2];']):
        # Avoid malformed address hypotheses that read an uninitialized local.
        if '*(u32 *)dest' in load:
            valid = 'dest = offset +' in address
        else:
            valid = 'work =' in address or 'work +=' in address
        if not valid:
            continue
        body = '\n        '.join([address, load, count, 'dma[0] = source;',
                                   'dma[1] = dest;', mask, 'dma[2] = count;', read]) + '\n'
        yield seed[:start] + '        ' + body + seed[end:]


def coalescing():
    seed = (ROOT / 'docs/match7-search/queue_work/func_08015DA8.c').read_text()
    start = seed.index('        work = offset')
    end = seed.index('        cursor +=')
    body = '''        count = destbase;
        work = offset + count;
        dest = *(u32 *)work;
        work = base; work += 8;
        { u32 addend = work; work = offset + addend; }
        count = *(u32 *)work;
        dma[0] = source;
        dma[1] = dest;
        count >>= 2;
        work = 0x84000000;
        count |= work;
        dma[2] = count;
        work = dma[2];
'''
    seed = seed[:start] + body + seed[end:]
    for order, hints, location, dtype, ctype in itertools.product(
        itertools.permutations(['work', 'dest', 'count', 'source']),
        range(16), ['outer', 'inner', 'aftercheck'], ['u32', 's32', 'u32 *'],
        ['u32', 's32']):
        c = seed.replace('    u32 work;\n', '').replace('        u32 dest, count;\n', '')
        c = c.replace('u32 source = *(u32 *)cursor;', 'source = *(u32 *)cursor;')
        types = dict(work='u32', dest=dtype, count=ctype, source='u32')
        declarations = '\n'.join(('register ' if hints & (1 << n) else '') +
                                 types[name] + ' ' + name + ';' for n, name in enumerate(order))
        if location == 'outer':
            c = c.replace('    do {', declarations + '\n    do {')
        elif location == 'inner':
            c = c.replace('    do {', '    do {\n' + declarations)
        else:
            # Keep source in scope for its zero test.
            declarations = '\n'.join(x for x in declarations.splitlines() if ' source;' not in x)
            c = c.replace('    do {', '    do { u32 source;')
            c = c.replace('        count = destbase;', declarations + '\n        count = destbase;')
        if dtype == 'u32 *':
            c = c.replace('dest = *(u32 *)work;', 'dest = (u32 *)*(u32 *)work;').replace('dma[1] = dest;', 'dma[1] = (u32)dest;')
        yield c


def tails():
    seed = (ROOT / 'docs/match7-search/queue_work/func_08015DA8.c').read_text()
    for name, read, form, addr, mask in itertools.product(
        ['dest', 'work', 'count', 'source'], ['', 'work', 'dest', 'count', 'source'],
        ['zero', 'return', 'expression'], ['original', 'named'],
        ['original', 'inverted', 'separate']):
        c = seed.replace('    u32 work;', '    u32 work, dest, count, source;')
        c = c.replace('u32 source =', 'source =').replace('        u32 dest, count;\n', '')
        c = c.replace('        dma[2];', '        ' + (read + ' = ' if read else '') + 'dma[2];')
        if addr == 'named':
            c = c.replace('work = offset + destbase;', 'count = destbase; work = offset + count;')
        if mask == 'inverted':
            c = c.replace('count |= work;', 'count = work | count;')
        if mask == 'separate':
            c = c.replace('count >>= 2; work = 0x84000000; count |= work;', 'work = count >> 2; count = 0x84000000; count |= work;')
        if form == 'expression':
            tail = '*(u32 *)base = (' + name + ' = 0); *(u32 *)endmarker = ' + name + ';'
        else:
            tail = name + ' = 0; *(u32 *)base = ' + name + '; *(u32 *)endmarker = ' + name + ';'
        if form == 'return':
            c = c.replace('void func_08015DA8', 'u32 func_08015DA8')
            tail += ' return ' + name + ';'
        c = c.replace('*(u32 *)base = 0;\n    *(u32 *)endmarker = 0;', tail)
        yield c


def helpers():
    seed = (ROOT / 'docs/match7-search/queue_work/func_08015DA8.c').read_text()
    start = seed.index('        work = offset')
    end = seed.index('        cursor +=')
    original = seed[start:end]
    for order, ret, addr, read in itertools.product(
        itertools.permutations(['source', 'offset', 'destbase', 'base', 'dma']),
        ['void', 'u32'], ['original', 'named'], ['', 'work', 'dest', 'count']):
        params = ', '.join(('vu32 *' if x == 'dma' else 'u32 ') + x for x in order)
        args = ', '.join(order)
        body = 'u32 work, dest, count;\n' + original
        if addr == 'named':
            body = body.replace('work = offset + destbase;', 'count = destbase; work = offset + count;')
        body = body.replace('        dma[2];', '        ' + (read + ' = ' if read else '') + 'dma[2];')
        if ret == 'u32':
            body += 'return count;\n'
        helper = 'static inline ' + ret + ' transfer(' + params + ') {\n' + body + '}\n'
        yield helper + seed[:start] + '        transfer(' + args + ');\n' + seed[end:]


def pointer_work():
    seed = (ROOT / 'docs/match7-search/queue_work/func_08015DA8.c').read_text()
    for typ, desttyp, counttyp, read, addr in itertools.product(
        ['u8 *', 'void *', 's32', 'u32'], ['u32', 's32', 'void *'],
        ['u32', 's32'], ['', 'work', 'dest', 'count'], ['original', 'named']):
        c = seed.replace('u32 work;', typ + ' work;').replace('u32 dest, count;', desttyp + ' dest; ' + counttyp + ' count;')
        if '*' in typ:
            c = c.replace('work = offset + destbase;', 'work = offset + (' + typ + ')destbase;')
            c = c.replace('work = base;', 'work = (' + typ + ')base;')
            c = c.replace('u32 addend = work;', typ + ' addend = work;')
            c = c.replace('work = 0x84000000;', 'work = (' + typ + ')0x84000000;')
            c = c.replace('count |= work;', 'count |= (u32)work;')
        if '*' in desttyp:
            c = c.replace('dest = *(u32 *)work;', 'dest = (void *)*(u32 *)work;')
            c = c.replace('dma[1] = dest;', 'dma[1] = (u32)dest;')
        if counttyp == 's32':
            c = c.replace('count >>= 2;', 'count = (u32)count >> 2;')
        if addr == 'named':
            c = c.replace('work = offset + ', 'work = offset + ', 1)
            old = 'work = offset + ' + ('(' + typ + ')' if '*' in typ else '') + 'destbase;'
            c = c.replace(old, '{ ' + typ + ' input = (' + typ + ')destbase; work = offset + input; }')
        c = c.replace('        dma[2];', '        ' + (read + ' = (' + (typ if read == 'work' else desttyp if read == 'dest' else counttyp) + ')' if read else '') + 'dma[2];')
        yield c


def setup_reuse():
    seed = (ROOT / 'docs/match7-search/queue_work/func_08015DA8.c').read_text()
    setup = ['u32 i = 0;', 'u32 base = (u32)g_030061F0;',
             'u32 endmarker = (u32)&g_030067E4;',
             'vu32 *dma = (vu32 *)0x040000D4;', 'u32 cursor = base;',
             'u32 offset = 0;', 'u32 destbase = base + 4;']
    for bits, read, hint in itertools.product(range(1, 128), ['', 'work', 'count'], ['', 'dest', 'source']):
        c = seed.replace('    u32 work;', '').replace('u32 dest, count;', 'u32 count;')
        declarations = 'u32 work, dest, i, base, endmarker, cursor, offset, destbase; vu32 *dma;'
        c = c.replace('    u32 i = 0;', declarations + '\n    u32 i = 0;')
        for i, item in enumerate(setup):
            lhs, rhs = item[:-1].split(' = ')
            name = lhs.split()[-1].lstrip('*')
            replacement = name + ' = ' + rhs + ';'
            if bits & (1 << i):
                value = '(u32)' + rhs if name == 'dma' else rhs
                cast = '(vu32 *)' if name == 'dma' else ''
                replacement = 'dest = ' + value + '; ' + name + ' = ' + cast + 'dest;'
            c = c.replace(item, replacement)
        c = c.replace('        dma[2];', '        ' + (read + ' = ' if read else '') + 'dma[2];')
        if hint == 'dest':
            c = c.replace('u32 work, dest, i,', 'register u32 dest; u32 work, i,')
        if hint == 'source':
            c = c.replace('u32 source =', 'register u32 source =')
        yield c


def dead_parameters():
    # Every incoming value is overwritten before any use. This tests pseudo
    # creation and parameter preference without depending on extra ABI inputs.
    seeds = [(ROOT / x).read_text() for x in [
        'docs/match7-search/queue_work/func_08015DA8.c',
        'docs/match9-search/queue-setup-reuse/func_08015DA8.c']]
    for seed, count, read in itertools.product(seeds, range(1, 5), ['', 'work', 'count']):
        for names in itertools.permutations(['source', 'dest', 'work', 'count'], count):
            # Split joint declarations before removing the parameter locals.
            c = vs.split_declarations(seed)
            for name in names:
                c = vs.re.sub(r'\bu32 ' + name + r'\s*;', '', c)
                if name == 'source':
                    c = c.replace('u32 source =', 'source =')
            c = c.replace('func_08015DA8(void)', 'func_08015DA8(' + ', '.join('u32 ' + n for n in names) + ')')
            c = vs.re.sub(r'(?m)^\s*(?:(?:work|count) = )?dma\[2\];',
                          '\n        ' + (read + ' = ' if read else '') + 'dma[2];', c)
            yield c


def zero_branch():
    seed = (ROOT / 'docs/match7-search/queue_work/func_08015DA8.c').read_text()
    for decl, zero, read, mask in itertools.product(['inner', 'outer'],
        ['source', '0', 'work', 'count'], ['', 'work', 'dest', 'count'],
        ['original', 'inverse', 'separate']):
        c = seed.replace('    u32 work;', '    u32 work, dest;').replace('u32 dest, count;', 'u32 count;')
        if decl == 'outer':
            c = c.replace('    u32 work, dest;', '    u32 work, dest, count;').replace('        u32 count;', '')
        pre = '' if zero in ['source', '0'] else zero + ' = 0; '
        c = c.replace('if (!source) { *(u32 *)base = source; break; }',
                      'if (!source) { ' + pre + 'dest = ' + zero + '; *(u32 *)base = dest; break; }')
        c = c.replace('        dma[2];', '        ' + (read + ' = ' if read else '') + 'dma[2];')
        if mask == 'inverse':
            c = c.replace('count |= work;', 'count = work | count;')
        if mask == 'separate':
            c = c.replace('count >>= 2; work = 0x84000000; count |= work;',
                          'work = count >> 2; count = 0x84000000; count |= work;')
        yield c


def control():
    paths = ['docs/match7-search/queue_work/func_08015DA8.c',
             'docs/match9-search/queue-lifetimes/func_08015DA8.c',
             'docs/match9-search/queue-setup-reuse/func_08015DA8.c']
    for path, loop, signed, exitform, tail in itertools.product(paths,
        ['do', 'while', 'for', 'goto', 'infinite'], [False, True],
        ['break', 'goto', 'else'], ['ordinary', 'return-zero']):
        c = (ROOT / path).read_text()
        if signed:
            c = c.replace('u32 i = 0;', 's32 i = 0;')
            c = c.replace('dest, i, base', 'dest, base').replace('    i = 0;', '    s32 i;\n    i = 0;')
        if loop == 'while':
            c = c.replace('    do {', '    while (i <= 96) {').replace('} while (i <= 96);', '}')
        if loop == 'for':
            c = c.replace('    do {', '    for (; i <= 96; i++) {').replace('        i++;', '').replace('} while (i <= 96);', '}')
        if loop == 'goto':
            c = c.replace('    do {', 'again: {').replace('} while (i <= 96);', '} if (i <= 96) goto again;')
        if loop == 'infinite':
            c = c.replace('    do {', '    for (;;) {').replace('} while (i <= 96);', 'if (i > 96) break; }')
        if exitform == 'goto':
            c = c.replace('break;', 'goto done;').replace('    *(u32 *)base = 0;', 'done: *(u32 *)base = 0;')
        if exitform == 'else':
            c = c.replace('break; }', 'break; } else {').replace('        cursor += 12;', '        }\n        cursor += 12;')
        if tail == 'return-zero':
            c = c.replace('void func_08015DA8', 'u32 func_08015DA8').replace('*(u32 *)endmarker = 0;', '*(u32 *)endmarker = 0; return 0;')
        yield c


def main():
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--jobs', type=int, default=4)
    ap.add_argument('--profiles', nargs='+', default=['old'])
    ap.add_argument('--grid', choices=['lifetimes', 'coalescing', 'tails', 'helpers', 'pointer-work', 'setup-reuse', 'dead-parameters', 'control', 'zero-branch'], default='lifetimes')
    args = ap.parse_args()
    prog = vs.draft.Program()
    address = 0x08015DA8
    end = vs.comparison_end(prog, address)
    output = ROOT / ('docs/match9-search/queue-' + args.grid)
    output.mkdir(parents=True, exist_ok=True)
    sources = list(dict.fromkeys({'lifetimes': candidates, 'coalescing': coalescing, 'tails': tails, 'helpers': helpers, 'pointer-work': pointer_work, 'setup-reuse': setup_reuse, 'dead-parameters': dead_parameters, 'control': control, 'zero-branch': zero_branch}[args.grid]()))
    jobs = [(address, end, s, p) for s in sources for p in args.profiles]
    best = None
    tried = errors = 0
    started = time.monotonic()
    with futures.ProcessPoolExecutor(max_workers=args.jobs, initializer=vs.init_worker,
                                     initargs=(vs.reloc.symbols(prog),)) as pool:
        for lo in range(0, len(jobs), args.jobs * 2):
            wave = jobs[lo:lo + args.jobs * 2]
            for job, result in zip(wave, pool.map(vs.compile_job, wave)):
                tried += 1
                sc, size, got, error = result
                if error:
                    errors += 1
                    continue
                if best is None or sc < best[0]:
                    best = sc, size, job[2], job[3], got
                    print(f'trials={tried} score={sc} profile={job[3]}', flush=True)
                    (output / 'func_08015DA8.c').write_text(job[2])
                if got == prog.rom[address-vs.draft.BASE:end-vs.draft.BASE]:
                    break
            if best and best[0] == (0, 0):
                break
    record = dict(address='08015DA8', planned_jobs=len(jobs), attempts=tried,
                  compile_errors=errors, seconds=round(time.monotonic()-started, 2),
                  exact=bool(best and best[0] == (0, 0)))
    if best:
        sc, size, source, profile, got = best
        record.update(score=sc, size=size, compiler=profile)
        (output / 'func_08015DA8.diff.txt').write_text(vs.source_diff(
            prog.rom[address-vs.draft.BASE:end-vs.draft.BASE], got, address) + '\n')
    (output / 'results.json').write_text(json.dumps(record, indent=2) + '\n')


if __name__ == '__main__':
    main()

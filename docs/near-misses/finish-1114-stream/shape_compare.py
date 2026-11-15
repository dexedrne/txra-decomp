#!/usr/bin/env python3
"""Text-only comparison of the original disassembly (asm/program.s) with compiled
assembly (old_agbcc .s output). Canonicalises both syntaxes; no ROM bytes used.
Usage: shape_compare.py asm/program.s trial.s [ops | FIRST LAST]; NOSP=1 ignores sp offsets."""
import difflib, re, sys

REG = {'sb': 'r9', 'sl': 'r10', 'fp': 'r11', 'ip': 'r12'}
SUFFIX_OPS = {'adds', 'subs', 'movs', 'lsls', 'lsrs', 'asrs', 'ands', 'orrs', 'eors', 'muls',
              'mvns', 'negs', 'bics', 'adcs', 'sbcs', 'rors', 'rsbs'}
BR = re.compile(r'^b(eq|ne|cs|cc|hs|lo|mi|pl|vs|vc|hi|ls|ge|lt|gt|le|al)?$')


def num(t):
    t = t.strip().lstrip('#')
    return int(t, 0)


def reg(t):
    t = t.strip()
    return REG.get(t, t)


def canon(op, args):
    op = op.lower()
    if op in SUFFIX_OPS:
        op = op[:-1]
    if op == 'rsb':
        op = 'neg'
        args = args[:2]
    if BR.match(op):
        return (op, 'L')
    if op == 'bl':
        return (op, args[0].strip())
    if op in ('push', 'pop'):
        return (op, ','.join(reg(r) for r in re.findall(r'[a-z0-9]+', args[0] if len(args) == 1 else ','.join(args))))
    a = ','.join(args)
    # memory operand
    m = re.match(r'\s*(\w+)\s*,\s*\[(.*)\]\s*$', a)
    if m and op.startswith(('ldr', 'str')):
        rt = reg(m.group(1))
        inner = [x.strip() for x in m.group(2).split(',')]
        if inner[0] == 'pc':
            return (op, rt, '=P')
        base = reg(inner[0])
        off = inner[1] if len(inner) > 1 else '#0'
        off = str(num(off)) if off.startswith('#') else reg(off)
        return (op, rt, '[%s,%s]' % (base, off))
    if op == 'ldr' and re.match(r'\s*\w+\s*,\s*\.L', a):
        return (op, reg(args[0]), '=P')
    ops = []
    for x in args:
        x = x.strip()
        if x.startswith('#'):
            ops.append(str(num(x)))
        else:
            ops.append(reg(x))
    if op == 'add' and ops[:2] == ['sp', 'sp'] and len(ops) == 3:
        return ('spadj', str(-int(ops[2])))
    if op == 'sub' and ops[0] == 'sp' and len(ops) == 2:
        return ('spadj', ops[1])
    if op == 'add' and ops[0] == 'sp' and len(ops) == 2:
        return ('spadj', str(-int(ops[1])))
    if op in ('add', 'sub') and len(ops) == 3 and ops[0] == ops[1] and ops[2].lstrip('-').isdigit() and int(ops[2]) > 7:
        ops = [ops[0], ops[2]]
    if op in ('add', 'sub') and len(ops) == 3 and ops[0] == ops[1] and ops[2].lstrip('-').isdigit():
        ops = [ops[0], ops[2]]
    if op in ('and', 'orr', 'eor', 'mul', 'bic', 'adc', 'sbc', 'lsl', 'lsr', 'asr', 'ror', 'mvn', 'neg', 'cmp', 'cmn', 'tst') and len(ops) == 3 and ops[0] == ops[1] and not ops[2].lstrip('-').isdigit():
        ops = [ops[0], ops[2]]
    HI = ('r8', 'r9', 'r10', 'r11', 'r12', 'sp', 'lr', 'pc')
    if op == 'add' and len(ops) == 3 and ops[0] == ops[1] and (ops[0] in HI or ops[2] in HI):
        ops = [ops[0], ops[2]]
    if op == 'mul' and len(ops) == 3 and ops[0] == ops[2]:
        ops = [ops[0], ops[1]]
    return tuple([op] + ops)


def split_args(s):
    out, depth, cur = [], 0, ''
    for ch in s:
        if ch in '[{':
            depth += 1
        if ch in ']}':
            depth -= 1
        if ch == ',' and depth == 0:
            out.append(cur)
            cur = ''
        else:
            cur += ch
    if cur.strip():
        out.append(cur)
    return out


def parse_orig(path, start='func_08002854', stop='func_0800418C'):
    rows, on = [], False
    for line in open(path):
        if line.startswith(start + ':'):
            on = True
            continue
        if on and line.startswith(stop + ':'):
            break
        if not on:
            continue
        s = line.split('@')[0].strip()
        addr = line.split('@')[1].strip() if '@' in line else ''
        if not s or s.endswith(':') or s.startswith('.thumb'):
            continue
        if s.startswith('.incbin'):
            n = int(s.split(',')[-1], 0)
            for _ in range(n // 4):
                rows.append((('.word',), 'pool'))
            continue
        op, _, rest = s.partition(' ')
        rows.append((canon(op, split_args(rest)), addr))
    return rows


def parse_comp(path, name='func_08002854'):
    rows, on = [], False
    for line in open(path):
        if line.startswith(name + ':'):
            on = True
            continue
        if not on:
            continue
        if line.strip().startswith('.size') or line.startswith('.Lfe'):
            break
        s = line.split('@')[0].strip()
        if not s or s.endswith(':') or s.startswith(('.align', '.thumb', '.code', '.type', '.globl')):
            continue
        if s.startswith('.word'):
            rows.append((('.word',), 'pool'))
            continue
        op, _, rest = s.replace('\t', ' ', 1).partition(' ')
        rows.append((canon(op, split_args(rest.replace('\t', ' '))), ''))
    return rows


import os
def shape(t):
    t = tuple(re.sub(r'\br\d+\b', 'R', x) for x in t)
    if os.environ.get('NOSP'):
        t = tuple(re.sub(r'\[sp,\d+\]', '[sp,S]', x) for x in t)
        if t and t[0] == 'spadj':
            t = ('spadj',)
    return t


def main():
    orig = parse_orig(sys.argv[1])
    comp = parse_comp(sys.argv[2])
    a = [' '.join(r[0]) for r in orig]
    b = [' '.join(r[0]) for r in comp]
    sa = [' '.join(shape(r[0])) for r in orig]
    sb = [' '.join(shape(r[0])) for r in comp]
    full = difflib.SequenceMatcher(None, a, b, autojunk=False)
    shp = difflib.SequenceMatcher(None, sa, sb, autojunk=False)
    fm = sum(x.size for x in full.get_matching_blocks())
    sm = sum(x.size for x in shp.get_matching_blocks())
    prefix = 0
    while prefix < min(len(a), len(b)) and a[prefix] == b[prefix]:
        prefix += 1
    sprefix = 0
    while sprefix < min(len(sa), len(sb)) and sa[sprefix] == sb[sprefix]:
        sprefix += 1
    print('orig rows %d comp rows %d | full-match %d shape-match %d | exact prefix %d (%s) shape prefix %d (%s)' % (
        len(a), len(b), fm, sm, prefix, orig[prefix][1] if prefix < len(orig) else 'end',
        sprefix, orig[sprefix][1] if sprefix < len(orig) else 'end'))
    if len(sys.argv) > 3 and sys.argv[3] == 'ops':
        for tag, i1, i2, j1, j2 in shp.get_opcodes():
            if tag == 'equal':
                continue
            print('%s orig %d-%d (%s) | comp %d-%d' % (tag, i1, i2, orig[i1][1] if i1 < len(orig) else 'end', j1, j2))
            for t in range(max(i2 - i1, j2 - j1)):
                left = '%-34s' % a[i1 + t] if i1 + t < i2 else ' ' * 34
                right = b[j1 + t] if j1 + t < j2 else ''
                print('    %s | %s' % (left, right))
        return
    lo = int(sys.argv[3]) if len(sys.argv) > 3 else None
    if lo is not None:
        hi = int(sys.argv[4]) if len(sys.argv) > 4 else lo + 40
        for tag, i1, i2, j1, j2 in shp.get_opcodes():
            if i2 < lo or i1 > hi:
                continue
            for k in range(max(i1, lo), min(i2, hi)) if tag == 'equal' else []:
                j = j1 + (k - i1)
                mark = ' ' if a[k] == b[j] else '~'
                print('%s %5d %-10s %-34s | %s' % (mark, k, orig[k][1], a[k], b[j]))
            if tag != 'equal':
                n = max(i2 - i1, j2 - j1)
                for t in range(n):
                    left = '%5d %-10s %-34s' % (i1 + t, orig[i1 + t][1], a[i1 + t]) if i1 + t < i2 else ' ' * 52
                    right = b[j1 + t] if j1 + t < j2 else ''
                    print('%s %s | %s' % (tag[0].upper(), left, right))


if __name__ == '__main__':
    main()

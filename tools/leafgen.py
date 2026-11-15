#!/usr/bin/env python3
"""Emit C directly for straight-line THUMB functions recognised from their lifted IR.

Covers empty functions, constant returns, getters/setters at fixed or argument-relative
addresses, and other branch-free leaves (optionally calling other functions). Output is
a short list of plausible source variants; the matching compiler decides which, if any,
reproduces the ROM. Nothing here is trusted without that byte comparison.
"""
import itertools, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / 'recomp'))
import draft

PRELUDE = draft.TYPEDEFS
CASTS = {('lsr', 16): 'u16', ('asr', 16): 's16', ('lsr', 24): 'u8', ('asr', 24): 's8'}
BINOPS = {'add': '+', 'sub': '-', 'and': '&', 'eor': '^', 'orr': '|', 'mul': '*', 'lsl': '<<', 'lsr': '>>', 'asr': '>>', 'bic': '& ~'}

class Unsupported(Exception):
    pass

def is_const(e): return e[0] == 'const'

def simplify(e):
    """Fold constants and recognise shift pairs as narrowing casts."""
    if e[0] == 'bin':
        _, op, a, b = e
        if is_const(a) and is_const(b) and op in ('add', 'sub', 'and', 'eor', 'orr', 'mul', 'lsl', 'lsr', 'bic'):
            x, y = a[1], b[1]
            v = {'add': x + y, 'sub': x - y, 'and': x & y, 'eor': x ^ y, 'orr': x | y, 'mul': x * y,
                 'lsl': x << min(y, 63), 'lsr': x >> min(y, 63), 'bic': x & ~y}[op]
            return ('const', v & 0xffffffff)
        if op in ('lsr', 'asr') and is_const(b) and a[0] == 'bin' and a[1] == 'lsl' and a[3] == b and (op, b[1]) in CASTS:
            return ('cast', CASTS[op, b[1]], a[2])
        if op == 'add' and is_const(b) and b[1] == 0: return a
        # Signed division by a power of two: (x + (x >> 31 logical)) >> 1, or with a rounding mask.
        if op == 'asr' and is_const(b) and a[0] == 'bin' and a[1] == 'add':
            x, bias = a[2], a[3]
            if b[1] == 1 and bias == ('bin', 'lsr', x, ('const', 31)): return ('div', x, 2)
            if bias[0] == 'bin' and bias[1] == 'lsr' and bias[2] == ('bin', 'asr', x, ('const', 31)) and bias[3] == ('const', 32 - b[1]):
                return ('div', x, 1 << b[1])
    return e

def address(base, off):
    """Keep constant base + offset apart so a global-symbol spelling stays possible."""
    if is_const(off) and off[1] == 0: return base
    if is_const(base) and is_const(off): return ('bin', 'add', base, off)
    return simplify(('bin', 'add', base, off))

def offset_global(e):
    return e[0] == 'bin' and e[1] == 'add' and is_const(e[2]) and is_const(e[3])

def walk(e):
    yield e
    for x in e[1:]:
        if isinstance(x, tuple) and x and isinstance(x[0], str): yield from walk(x)
        if isinstance(x, list):
            for a in x: yield from walk(a)

def pure(e):
    if e[0] in ('load', 'ret'): return False
    if e[0] == 'bin': return pure(e[2]) and pure(e[3])
    if e[0] in ('cast', 'not', 'neg', 'div'): return pure(e[2] if e[0] == 'cast' else e[1])
    return True

class Leaf:
    """Symbolic evaluation of one straight-line function."""
    def __init__(self, prog, addr):
        self.prog, self.addr = prog, addr
        f = prog.by_start[addr]
        if f['mode'] != 'thumb': raise Unsupported('ARM mode')
        self.ins = prog.insns[addr]
        self.nparams = prog.params(addr)
        self.returns = prog.returns(addr)
        self.regs = {r: ('arg', r) for r in range(self.nparams)}
        self.stmts = []     # ('store', size, addr, value) | ('call', target, args, temp) | ('tmp', name, expr)
        self.temps = 0
        self.calls = set()
        self.ret = None
        self.evaluate()

    def get(self, r):
        if isinstance(r, tuple): return ('const', r[1])
        if r not in self.regs: raise Unsupported('reads r%d before writing it' % r)
        return self.regs[r]

    def live_after(self, k, r):
        for i in self.ins[k + 1:]:
            reads, writes = draft.uses(i.ir, self.prog)
            if i.ir[0] == 'bx' and i.ir[1] == 14 or i.ir[0] == 'pop' and i.ir[1] & (1 << 15):
                return r == 0 and self.returns
            if r in reads: return True
            if r in writes: return False
        return r == 0 and self.returns

    def settle(self, k):
        """Before a side effect, give any still-needed memory read or call result a name."""
        for r in sorted(self.regs):
            e = self.regs[r]
            if not pure(e) and e[0] != 'tmp' and self.live_after(k - 1, r):
                self.name_value(e)

    def name_value(self, e):
        name = 't%d' % self.temps; self.temps += 1
        self.stmts.append(('tmp', name, e))
        for q, x in self.regs.items():
            if x == e: self.regs[q] = ('tmp', name)
        return ('tmp', name)

    def read(self, r, k):
        """A memory-derived value read here and again later is one read in the ROM: name it."""
        e = self.get(r)
        if not isinstance(r, tuple) and not pure(e) and e[0] != 'tmp':
            writes = draft.uses(self.ins[k].ir, self.prog)[1]
            if r not in writes and self.live_after(k, r): return self.name_value(e)
            if r in writes and any(q != r and x == e and self.live_after(k, q) for q, x in self.regs.items()): return self.name_value(e)
        return e

    def evaluate(self):
        seen_return = False
        for k, i in enumerate(self.ins):
            if seen_return: raise Unsupported('code after return')
            ir = i.ir
            op = ir[0]
            if i.cond != 14: raise Unsupported('conditional')
            if op in ('push',): continue
            if op == 'pop':
                if ir[1] & (1 << 15): seen_return = True
                continue
            if op == 'bx':
                if ir[1] == 14 or (k and self.ins[k - 1].ir[0] == 'pop' and self.ins[k - 1].ir[1] & (1 << ir[1])):
                    seen_return = True; continue
                raise Unsupported('indirect branch')
            if op == 'mov':
                if ir[1] >= 8 or (isinstance(ir[2], int) and ir[2] >= 8):
                    if k + 1 < len(self.ins) and self.ins[k + 1].ir[0] in ('push', 'pop') or k and self.ins[k - 1].ir[0] == 'pop':
                        continue
                    raise Unsupported('high register value')
                self.regs[ir[1]] = self.read(ir[2], k) if not draft.is_imm(ir[2]) else ('const', ir[2][1])
            elif op == 'pool':
                v = self.prog.word(ir[2])
                if v is None: raise Unsupported('pool outside ROM')
                self.regs[ir[1]] = ('const', v)
            elif op == 'alu':
                _, rd, o, a, b = ir
                if o not in BINOPS and o != 'mvn': raise Unsupported('alu ' + o)
                if a == 13: raise Unsupported('stack address')
                if o == 'mvn': self.regs[rd] = ('not', self.read(b, k))
                elif o == 'sub' and draft.is_imm(a) and a[1] == 0: self.regs[rd] = ('neg', self.read(b, k))
                else: self.regs[rd] = simplify(('bin', o, self.read(a, k), self.read(b, k)))
            elif op == 'load':
                _, rd, size, signed, base, off = ir
                if base == 13: raise Unsupported('stack slot')
                self.regs[rd] = ('load', size, signed, address(self.read(base, k), self.read(off, k)))
            elif op == 'store':
                _, rs, size, base, off = ir
                if base == 13: raise Unsupported('stack slot')
                value, where = self.read(rs, k), address(self.read(base, k), self.read(off, k))
                self.settle(k)
                value, where = self.refresh(value), self.refresh(where)
                self.stmts.append(('store', size, where, value))
            elif op == 'call':
                t = ir[1]
                n = self.prog.params(t)
                args = [self.get(r) for r in range(n)]
                self.settle(k)
                args = [self.refresh(a) for a in args]
                self.calls.add(t)
                temp = None
                for r in (0, 1, 2, 3, 12): self.regs.pop(r, None)
                if self.prog.returns(t):
                    if self.live_after(k, 0):
                        temp = 't%d' % self.temps; self.temps += 1
                        self.regs[0] = ('tmp', temp)
                self.stmts.append(('call', t, args, temp))
            else:
                raise Unsupported(op)
        if not seen_return: raise Unsupported('no return')
        if self.returns:
            if 0 not in self.regs: raise Unsupported('return value not computed')
            self.ret = self.regs[0]

    def refresh(self, e):
        # A register may have been renamed to a temporary by settle().
        for name, x in [(s[1], s[2]) for s in self.stmts if s[0] == 'tmp']:
            if e == x: return ('tmp', name)
        return e

class Style:
    def __init__(self, volatile, symbols, param_types, return_type):
        self.volatile, self.symbols, self.param_types, self.return_type = volatile, symbols, param_types, return_type

def render(e, st, externs):
    k = e[0]
    if k == 'const':
        v = e[1]
        if (v & ~1) in st.prog.by_start and st.prog.by_start[v & ~1]['mode'] == 'thumb' and v & 1:
            externs.add(v & ~1); return '(u32)%s' % st.prog.name(v & ~1)
        return '0x%X' % v if v > 9 else str(v)
    if k == 'arg': return 'a%d' % e[1]
    if k == 'tmp': return e[1]
    if k == 'cast': return '(%s)%s' % (e[1], wrap(e[2], st, externs))
    if k == 'not': return '~' + wrap(e[1], st, externs)
    if k == 'neg': return '-' + wrap(e[1], st, externs)
    if k == 'div': return '(s32)%s / %d' % (wrap(e[1], st, externs), e[2])
    if k == 'bin':
        _, op, a, b = e
        if op == 'asr': return '(s32)%s >> %s' % (wrap(a, st, externs), wrap(b, st, externs))
        return '%s %s %s' % (wrap(a, st, externs), BINOPS[op], wrap(b, st, externs))
    if k == 'load':
        return lvalue(e[1], e[2], e[3], st, externs)
    raise Unsupported(k)

def wrap(e, st, externs):
    t = render(e, st, externs)
    return t if e[0] in ('const', 'arg', 'tmp', 'load') else '(%s)' % t

def lvalue(size, signed, where, st, externs):
    t = ('s' if signed else 'u') + str(size * 8)
    base, off = where, None
    if where[0] == 'bin' and where[1] == 'add' and is_const(where[3]): base, off = where[2], where[3][1]
    if is_const(where):
        a = where[1]
        if (a >> 24) == 4 or st.volatile: t = 'v' + t
        if st.symbols and draft.region(a):
            st.data.add(a)
            return '*(%s *)g_%08X' % (t, a)
        return '*(%s *)0x%08X' % (t, a)
    if is_const(base) and off is not None:
        a = base[1]
        vol = 'v' if (a >> 24) == 4 or st.volatile else ''
        if st.symbols and draft.region(a):
            st.data.add(a)
            return '*(%s%s *)(g_%08X + %d)' % (vol, t, a, off)
        return '*(%s%s *)0x%08X' % (vol, t, (a + off) & 0xffffffff)
    vol = 'v' if st.volatile else ''
    return '*(%s%s *)(%s)' % (vol, t, render(where, st, externs))

def generate(prog, addr, limit=8):
    """Plausible complete C sources (prelude excluded) for a straight-line function, or []."""
    try:
        leaf = Leaf(prog, addr)
    except (Unsupported, RecursionError):
        return []
    name = 'func_%08X' % addr
    casts = {}
    def scan(e):
        if e[0] == 'cast' and e[2][0] == 'arg': casts.setdefault(e[2][1], e[1])
        for x in e[1:]:
            if isinstance(x, tuple) and x and isinstance(x[0], str): scan(x)
    for s in leaf.stmts:
        for x in s[2:]:
            if isinstance(x, tuple): scan(x)
            if isinstance(x, list): [scan(a) for a in x]
    if leaf.ret is not None: scan(leaf.ret)
    exprs = [x for s in leaf.stmts for x in s[1:] if isinstance(x, (tuple, list))] + ([leaf.ret] if leaf.ret else [])
    has_offset_globals = any(offset_global(n) for e in exprs for n in walk(('list', e) if isinstance(e, list) else e) if isinstance(n, tuple))
    ret_options = ['u32']
    if leaf.ret is not None and leaf.ret[0] == 'cast': ret_options = [leaf.ret[1], 'u32']
    elif leaf.ret is not None and leaf.ret[0] == 'load' and leaf.ret[1] < 4:
        ret_options = [('s' if leaf.ret[2] else 'u') + str(leaf.ret[1] * 8), 'u32']
    if leaf.ret is not None and leaf.ret[0] == 'load':
        ret_options.append('void')  # a hardware register read back as a statement
    out = []
    for volatile, symbols, narrow, rt in itertools.product((True, False), (False, True),
                                                            (True, False) if casts else (False,), ret_options):
        st = Style(volatile, symbols, {n: (casts[n] if narrow and n in casts else 'u32') for n in range(leaf.nparams)}, rt)
        st.prog, st.data = prog, set()
        externs = set(leaf.calls)
        body = []
        def expr(e):
            return render(strip(e), st, externs)
        def strip(e):
            if narrow and e[0] == 'cast' and e[2][0] == 'arg' and casts.get(e[2][1]) == e[1]: return e[2]
            if e[0] in ('bin',): return ('bin', e[1], strip(e[2]), strip(e[3]))
            if e[0] == 'load': return ('load', e[1], e[2], strip(e[3]))
            if e[0] in ('not', 'neg'): return (e[0], strip(e[1]))
            if e[0] == 'div': return ('div', strip(e[1]), e[2])
            if e[0] == 'cast': return ('cast', e[1], strip(e[2]))
            return e
        temps = []
        for s in leaf.stmts:
            if s[0] == 'tmp':
                temps.append(s[1]); body.append('    %s = %s;' % (s[1], expr(s[2])))
            elif s[0] == 'store':
                v = expr(s[3])
                body.append('    %s = %s;' % (lvalue(s[1], False, strip(s[2]), st, externs), v))
            elif s[0] == 'call':
                call = '%s(%s)' % (prog.name(s[1]), ', '.join(expr(a) for a in s[2]))
                if s[3]: temps.append(s[3]); body.append('    %s = %s;' % (s[3], call))
                else: body.append('    %s;' % call)
        if leaf.ret is not None:
            r = leaf.ret
            if r[0] == 'cast' and r[1] == rt: r = r[2]
            body.append(('    %s;' if rt == 'void' else '    return %s;') % expr(r))
        params = ', '.join('%s a%d' % (st.param_types[n], n) for n in range(leaf.nparams)) or 'void'
        head = []
        for t in sorted(externs):
            n = prog.params(t)
            head.append('extern %s %s(%s);' % ('u32' if prog.returns(t) else 'void', prog.name(t),
                                               ', '.join(['u32'] * n) or 'void'))
        for a in sorted(st.data): head.append('extern u8 g_%08X[];' % a)
        decl = ['    u32 %s;' % ', '.join(temps)] if temps else []
        sig = '%s %s(%s)' % (rt if leaf.ret is not None else 'void', name, params)
        if rt == 'void' and leaf.ret is not None and not st.volatile: continue
        text = '\n'.join(head + [sig, '{'] + decl + body + ['}', ''])
        if text not in out: out.append(text)
        if len(out) >= limit: break
    return out

if __name__ == '__main__':
    prog = draft.Program()
    for a in sys.argv[1:]:
        for v in generate(prog, int(a, 16)):
            print(v)

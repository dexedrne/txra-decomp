#!/usr/bin/env python3
"""Write candidate sources: replace the projection loop body of g6.c with given text.
    import mk; mk.write(name, body, decls=None, pre_func='', fscope='')"""
import re
from pathlib import Path
BASE = Path(__file__).resolve().parents[2] / 'finish4-1115/renderer/c/g6.c'
OUT = Path(__file__).resolve().parent / 'c'
HEAD = '                        for (i = 0; i < 4; i++) {\n'
def build(body, pre_func='', fscope='', loop_head=None, base=None):
    b = (base or BASE.read_text())
    s0 = b.index(HEAD); s1 = b.index('\n                        }', s0 + len(HEAD))
    ind = ' ' * 28
    lines = [l.strip() for l in body.strip('\n').split('\n')]
    text = b[:s0] + (loop_head or HEAD) + '\n'.join(ind + l if l else '' for l in lines) + b[s1:]
    if pre_func:
        text = text.replace('void func_08016DA8(void)\n', pre_func + '\nvoid func_08016DA8(void)\n')
    if fscope:
        text = text.replace('    Point *pts = gPoints;\n', '    Point *pts = gPoints;\n' + fscope)
    return text
def write(name, body, **kw):
    OUT.mkdir(exist_ok=True)
    (OUT / (name + '.c')).write_text(build(body, **kw))

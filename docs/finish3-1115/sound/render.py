#!/usr/bin/env python3
"""Render every combination of a choice template into a folder.  usage: render.py <tpl> <outdir>"""
import sys, re, itertools
from pathlib import Path
PAT = re.compile(r'«(\w+)((?:@[^«»@]*)*)»', re.S)
tpl = Path(sys.argv[1]).read_text(); out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
pts = {}
for m in PAT.finditer(tpl):
    pts.setdefault(m.group(1), len(m.group(2).split('@')[1:]))
names = sorted(pts)
for c in itertools.product(*[range(pts[n]) for n in names]):
    ch = dict(zip(names, c))
    s = PAT.sub(lambda m: m.group(2).split('@')[1:][ch[m.group(1)]].replace('\\n', '\n'), tpl)
    for k, v in re.findall(r'/\*SUB:(\w+)=(\w+)\*/', s):
        s = s.replace(k, v)
    (out / ('v_' + '_'.join('%s%d' % (n, ch[n]) for n in names) + '.c')).write_text(s)

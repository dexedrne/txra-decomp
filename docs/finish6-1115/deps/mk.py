#!/usr/bin/env python3
"""mk.py BASE.c BODY.txt OUT.c [DECL] : replace the projection-loop body of an h7x2-style source
(the block between 'for (i = 0; i < 4; i++) {' and its closing brace) with BODY; DECL (optional)
replaces the function-scope 's32 tx, k, ty;' line."""
import sys, re
base, body, out = sys.argv[1:4]
t = open(base).read()
b = open(body).read()
s = t.index('for (i = 0; i < 4; i++) {')
s = t.index('\n', s) + 1
depth = 1; j = s
while depth:
    c = t[j]
    if c == '{': depth += 1
    elif c == '}': depth -= 1
    j += 1
e = t.rindex('\n', s, j - 1) + 1
t = t[:s] + b.rstrip('\n') + '\n' + t[e:]
if len(sys.argv) > 4:
    t = t.replace('    s32 tx, k, ty;\n', '    ' + sys.argv[4] + '\n')
open(out, 'w').write(t)

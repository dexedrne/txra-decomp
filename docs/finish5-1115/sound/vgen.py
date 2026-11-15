#!/usr/bin/env python3
"""Variant generator (worker only).  A spec file holds blocks:

    @@ name
    <<<   (or <<<- to drop the final newline of both texts)
    old text (exact, must occur once in the running source)
    ===
    new text
    >>>
    ... more <<< === >>> pairs ...

Each `@@ name` block starts again from the base source.  A block named with a leading `+`
(e.g. `@@ +name`) starts from the previous block's result instead (chained edits).
usage: vgen.py <base.c> <spec> <outdir>   -> writes <outdir>/<name>.c, prints the names."""
import sys, os, re
base = open(sys.argv[1]).read()
spec = open(sys.argv[2]).read()
out = sys.argv[3]
os.makedirs(out, exist_ok=True)
prev = base
for blk in re.split(r'(?m)^@@ ', spec)[1:]:
    head, _, body = blk.partition('\n')
    name = head.strip()
    chain = name.startswith('+')
    name = name.lstrip('+')
    src = prev if chain else base
    ok = True
    for m in re.finditer(r'(?ms)^<<<(-?)\n(.*?)^===\n(.*?)^>>>\n', body):
        old, new = m.group(2), m.group(3)
        if m.group(1):  # '<<<-': strip the final newline of both texts (in-line edits)
            old, new = old[:-1], new[:-1]
        n = src.count(old)
        if n != 1:
            print('SKIP %s: pattern occurs %d times: %r' % (name, n, old[:70]), file=sys.stderr)
            ok = False
            break
        src = src.replace(old, new)
    if not ok:
        continue
    open(os.path.join(out, name + '.c'), 'w').write(src)
    prev = src
    print(os.path.join(out, name + '.c'))

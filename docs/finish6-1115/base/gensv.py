#!/usr/bin/env python3
"""Saved-y variants of rendA h7x2.c (the 08016C18/080164D0 sibling idiom `saved_y = y;`).
    python3 gensv.py OUTDIR
sv is a function-scope variable that the direct path also uses for one point-to-packet copy, so
CSE makes it the canonical register of the dy/sv class (it lives past the loop block)."""
import sys, itertools
from pathlib import Path
src = Path('docs/finish5-1115/rendA/c/h7x2.c').read_text()
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
T = "                            t = dy * g_03000DF8 - tz * g_03005F58;\n                            ty = dy * g_03005F58 + tz * g_03000DF8;\n"
assert T in src
SLOTS = {
 'x1': ("                gCurPacket->x[1] = pts[b].sx;\n", "                sv = pts[b].sx;\n                gCurPacket->x[1] = sv;\n"),
 'y2': ("                gCurPacket->y[2] = pts[c].sy;\n", "                sv = pts[c].sy;\n                gCurPacket->y[2] = sv;\n"),
 'x3': ("                gCurPacket->x[3] = pts[d].sx;\n", "                sv = pts[d].sx;\n                gCurPacket->x[3] = sv;\n"),
 'y3': ("                gCurPacket->y[3] = pts[d].sy;\n", "                sv = pts[d].sy;\n                gCurPacket->y[3] = sv;\n"),
}
I = '                            '
PLACE = {
 # where `sv = dy;` goes
 'pA': lambda s: s.replace(T, I + 'sv = dy;\n' + T.replace('dy *', 'sv *')),
 'pB': lambda s: s.replace(I + 'dy -= gCamera.y;\n', I + 'dy -= gCamera.y;\n' + I + 'sv = dy;\n').replace(T, T.replace('dy *', 'sv *')),
 'pC': lambda s: s.replace(I + 'tz = (dx', I + 'sv = dy;\n' + I + 'tz = (dx').replace(T, T.replace('dy *', 'sv *')),
 'pD': lambda s: s.replace(I + 'tx = dx * g_03002A18;\n', I + 'sv = dy;\n' + I + 'tx = dx * g_03002A18;\n').replace(T, T.replace('dy *', 'sv *')),
}
n = 0
for sl, (a, b) in SLOTS.items():
    for pl, f in PLACE.items():
        s = src.replace('    s32 tx, k, ty;\n', '    s32 tx, k, ty, sv;\n')
        assert a in s
        s = s.replace(a, b)
        s = f(s)
        assert 'sv = dy;' in s and 'sv * g_03000DF8' in s
        s = s.replace('/* 08016DA8 renderer experiment (11/15 finish 5, rendA), NOT a match.',
                      '/* 08016DA8 renderer experiment (finish 6, base), NOT a match. h7x2 + saved copy sv (slot %s, place %s).' % (sl, pl), 1)
        (out / ('sv_%s_%s.c' % (sl, pl))).write_text(s); n += 1
print(n)

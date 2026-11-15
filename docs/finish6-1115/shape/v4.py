# Batch 4: final tx in its own function-scope variable shared with the direct path (global and,
# after combine folds the direct-path copy, single-set, so `tx2 = tx - k` is a birthing insn),
# with and without DF8 in another shared variable.
import runpy, itertools
from pathlib import Path
v1 = runpy.run_path(str(Path(__file__).resolve().parent / 'v1.py'))
L, BASE, DIRECT = v1['L'], v1['BASE'], v1['DIRECT']
DIRECT = dict(DIRECT)
DIRECT['x1'] = ('                gCurPacket->x[1] = pts[b].sx;', '                %s = pts[b].sx;\n                gCurPacket->x[1] = %s;')
def D(var, slot):
    old, new = DIRECT[slot]
    return (old, new % (var, var))
def body(df8, late):
    b = BASE
    if late:
        b = b.replace('tx -= k;\n', '').replace('dx = gOffset.x + (tx >> 12);', 'q = tx - k;\ndx = gOffset.x + (q >> 12);')
    else:
        b = b.replace('tx -= k;\n', 'q = tx - k;\n').replace('dx = gOffset.x + (tx >> 12);', 'dx = gOffset.x + (q >> 12);')
    if df8:
        b = b.replace('t = dy * g_03000DF8 - tz * g_03005F58;\nty = dy * g_03005F58 + tz * g_03000DF8;',
                      'w = g_03000DF8;\nt = dy * w - tz * g_03005F58;\nty = dy * g_03005F58 + tz * w;')
    return b
V = {}
slots = ['x1', 'y2', 'x3', 'y3']
for qs in slots:
    for late in (0, 1):
        V['q_%s_%d' % (qs, late)] = dict(decl='    s32 q;', loop=L(body(False, late)), rep=[D('q', qs)])
        for ws in slots:
            if ws == qs: continue
            V['qw_%s_%s_%d' % (qs, ws, late)] = dict(decl='    s32 q, w;', loop=L(body(True, late)), rep=[D('q', qs), D('w', ws)])
VARIANTS = V

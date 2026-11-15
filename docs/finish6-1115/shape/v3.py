# Batch 3: birthing final tx (u = tx - k, u single-set) on h7x2 and on the DF8-global family.
import runpy
from pathlib import Path
v1 = runpy.run_path(str(Path(__file__).resolve().parent / 'v1.py'))
L, BASE, D = v1['L'], v1['BASE'], v1['D']
def U(b, form):
    if form == 'u1':   # u = tx - k
        b = b.replace('tx -= k;\n', 'u = tx - k;\n')
    elif form == 'u2':  # tx stays the product, u computed late
        b = b.replace('tx -= k;\n', '')
        b = b.replace('dx = gOffset.x + (tx >> 12);', 'u = tx - k;\ndx = gOffset.x + (u >> 12);')
    return b.replace('dx = gOffset.x + (tx >> 12);', 'dx = gOffset.x + (u >> 12);')
V = {}
DF8 = BASE.replace('t = dy * g_03000DF8 - tz * g_03005F58;\nty = dy * g_03005F58 + tz * g_03000DF8;',
                   'w = g_03000DF8;\nt = dy * w - tz * g_03005F58;\nty = dy * g_03005F58 + tz * w;')
F58 = BASE.replace('t = dy * g_03000DF8 - tz * g_03005F58;\nty = dy * g_03005F58 + tz * g_03000DF8;',
                   'w = g_03005F58;\nt = dy * g_03000DF8 - tz * w;\nty = dy * w + tz * g_03000DF8;')
for form in ('u1', 'u2'):
    V['h_%s' % form] = dict(loop=L(U(BASE, form), decls='s32 dx, dy, dz, tz, f, sy, t, u;'))
    for slot in ('y2', 'x3', 'y3'):
        V['d8_%s_%s' % (form, slot)] = dict(decl='    s32 w;', loop=L(U(DF8, form), decls='s32 dx, dy, dz, tz, f, sy, t, u;'), rep=[D('w', slot)])
        V['f58_%s_%s' % (form, slot)] = dict(decl='    s32 w;', loop=L(U(F58, form), decls='s32 dx, dy, dz, tz, f, sy, t, u;'), rep=[D('w', slot)])
VARIANTS = V

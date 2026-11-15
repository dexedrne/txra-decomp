# Batch 1: copies in the race region, loop shapes, inline helper, statement order.
I = ' ' * 24
J = ' ' * 28
def L(body, hdr='for (i = 0; i < 4; i++) {', decls='s32 dx, dy, dz, tz, f, sy, t;', pre_loop=''):
    lines = [I[:-4] + '{']
    if pre_loop: lines.append(I + pre_loop)
    lines.append(I + hdr)
    lines.append(J + decls)
    lines += [J + s for s in body.strip().split('\n')]
    lines.append(I + '}')
    lines.append(I[:-4] + '}')
    return '\n'.join(lines)
BASE = """dx = gScratch[i].x;
dx -= gCamera.x;
dy = -gScratch[i].y;
dy -= gCamera.y;
dz = gScratch[i].z - gCamera.z;
tx = dx * g_03002A18;
k = dz * g_03001B28;
tx -= k;
tz = (dx * g_03001B28 + dz * g_03002A18) >> 12;
t = dy * g_03000DF8 - tz * g_03005F58;
ty = dy * g_03005F58 + tz * g_03000DF8;
dx = gOffset.x + (tx >> 12);
sy = gOffset.y + (ty >> 12);
dy = gOffset.z + (t >> 12);
g_030055F8[i].x = dy;
dy >>= 1;
f = g_0804F330[dy + 0x10000];
gCurPacket->x[i] = (((dx << 3) * f) >> 16) + 60;
gCurPacket->y[i] = (((sy << 3) * f) >> 15) + 80;"""
DIRECT = {
 'y2': ('                gCurPacket->y[2] = pts[c].sy;', '                %s = pts[c].sy;\n                gCurPacket->y[2] = %s;'),
 'x3': ('                gCurPacket->x[3] = pts[d].sx;', '                %s = pts[d].sx;\n                gCurPacket->x[3] = %s;'),
 'y3': ('                gCurPacket->y[3] = pts[d].sy;', '                %s = pts[d].sy;\n                gCurPacket->y[3] = %s;'),
}
def D(var, slot):
    old, new = DIRECT[slot]
    return (old, new % (var, var))
V = {}
V['base'] = dict(loop=L(BASE))
# --- copies of the y chain into a function-scope variable w (direct-path copy keeps w global)
for slot in ('y2', 'x3', 'y3'):
    body = BASE.replace('dy -= gCamera.y;\n', 'dy -= gCamera.y;\nw = dy;\n').replace(
        't = dy * g_03000DF8', 't = w * g_03000DF8').replace('ty = dy * g_03005F58', 'ty = w * g_03005F58')
    V['cw_' + slot] = dict(decl='    s32 w;', loop=L(body), rep=[D('w', slot)])
    body2 = BASE.replace('dy -= gCamera.y;\n', 'dy -= gCamera.y;\nw = dy;\n').replace('t = dy * g_03000DF8', 't = w * g_03000DF8')
    V['cwt_' + slot] = dict(decl='    s32 w;', loop=L(body2), rep=[D('w', slot)])
    # y chain in w itself, dy only for the depth
    body3 = BASE.replace('dy = -gScratch[i].y;\ndy -= gCamera.y;', 'w = -gScratch[i].y;\nw -= gCamera.y;').replace(
        't = dy * g_03000DF8', 't = w * g_03000DF8').replace('ty = dy * g_03005F58', 'ty = w * g_03005F58')
    V['cwy_' + slot] = dict(decl='    s32 w;', loop=L(body3), rep=[D('w', slot)])
    # DF8 in a function-scope variable
    body4 = BASE.replace('t = dy * g_03000DF8 - tz * g_03005F58;\nty = dy * g_03005F58 + tz * g_03000DF8;',
                         'w = g_03000DF8;\nt = dy * w - tz * g_03005F58;\nty = dy * g_03005F58 + tz * w;')
    V['cdf8_' + slot] = dict(decl='    s32 w;', loop=L(body4), rep=[D('w', slot)])
    # y chain local y, copied into a function-scope dy that also carries the depth
    body5 = BASE.replace('dy = -gScratch[i].y;\ndy -= gCamera.y;', 'y = -gScratch[i].y;\ny -= gCamera.y;\nw = y;').replace(
        't = dy * g_03000DF8', 't = w * g_03000DF8').replace('ty = dy * g_03005F58', 'ty = w * g_03005F58').replace(
        'dy = gOffset.z', 'w = gOffset.z').replace('g_030055F8[i].x = dy;\ndy >>= 1;\nf = g_0804F330[dy + 0x10000];',
        'g_030055F8[i].x = w;\nw >>= 1;\nf = g_0804F330[w + 0x10000];')
    V['cyw_' + slot] = dict(decl='    s32 w;', loop=L(body5, decls='s32 dx, y, dz, tz, f, sy, t;'), rep=[D('w', slot)])
# --- loop shapes
V['l_le3'] = dict(loop=L(BASE, hdr='for (i = 0; i <= 3; i++) {'))
V['l_do'] = dict(loop=L(BASE + '\ni++;', hdr='i = 0; do {').replace(I + '}\n' + I[:-4] + '}', I + '} while (i < 4);\n' + I[:-4] + '}'))
V['l_do2'] = dict(loop=L(BASE, hdr='i = 0; do {').replace(I + '}\n' + I[:-4] + '}', I + '} while (++i < 4);\n' + I[:-4] + '}'))
V['l_while'] = dict(loop=L(BASE + '\ni++;', hdr='i = 0; while (i < 4) {'))
ptr = BASE.replace('gScratch[i].x', 's->x').replace('gScratch[i].y', 's->y').replace('gScratch[i].z', 's->z')
V['l_ptr'] = dict(loop=L(ptr, hdr='for (i = 0, s = gScratch; i < 4; i++, s++) {'), decl='    Vec3 *s;')
V['l_ptr2'] = dict(loop=L(ptr + '\ni++;', hdr='for (s = gScratch, i = 0; s < &gScratch[4]; s++) {'), decl='    Vec3 *s;')
V['l_ptrloc'] = dict(loop=L(ptr, hdr='for (i = 0; i < 4; i++) {', decls='s32 dx, dy, dz, tz, f, sy, t; Vec3 *s = &gScratch[i];'))
dptr = ptr.replace('g_030055F8[i].x = dy;', 'o->x = dy;')
V['l_ptr3'] = dict(loop=L(dptr + '\no++;', hdr='for (i = 0, s = gScratch, o = g_030055F8; i < 4; i++, s++) {'), decl='    Vec3 *s, *o;')
# --- statement order: depth before the screen x/y
dfirst = BASE.replace("""dx = gOffset.x + (tx >> 12);
sy = gOffset.y + (ty >> 12);
dy = gOffset.z + (t >> 12);
g_030055F8[i].x = dy;
dy >>= 1;
f = g_0804F330[dy + 0x10000];""", """dy = gOffset.z + (t >> 12);
g_030055F8[i].x = dy;
dy >>= 1;
f = g_0804F330[dy + 0x10000];
dx = gOffset.x + (tx >> 12);
sy = gOffset.y + (ty >> 12);""")
V['o_dfirst'] = dict(loop=L(dfirst))
dfirst2 = BASE.replace("""dx = gOffset.x + (tx >> 12);
sy = gOffset.y + (ty >> 12);
dy = gOffset.z + (t >> 12);
g_030055F8[i].x = dy;""", """dy = gOffset.z + (t >> 12);
g_030055F8[i].x = dy;
dx = gOffset.x + (tx >> 12);
sy = gOffset.y + (ty >> 12);""")
V['o_dfirst2'] = dict(loop=L(dfirst2))
V['o_ty_first'] = dict(loop=L(BASE.replace('t = dy * g_03000DF8 - tz * g_03005F58;\nty = dy * g_03005F58 + tz * g_03000DF8;',
                                           'ty = dy * g_03005F58 + tz * g_03000DF8;\nt = dy * g_03000DF8 - tz * g_03005F58;')))
# --- inline helper (all temporaries local to the helper)
helper = """static inline void project(s32 i)
{
    s32 dx, dy, dz, tx, k, tz, ty, f, sy, t;
""" + '\n'.join('    ' + s for s in BASE.split('\n')) + "\n}\n"
V['i_proj'] = dict(pre=helper, loop=L('project(i);', decls=''))
helper2 = helper.replace('static inline void project(s32 i)\n{\n    s32 dx, dy, dz, tx, k, tz, ty, f, sy, t;',
                         'static inline void project(Vec3 *s, s32 i)\n{\n    s32 dx, dy, dz, tx, k, tz, ty, f, sy, t;').replace(
                         'gScratch[i].x', 's->x').replace('gScratch[i].y', 's->y').replace('gScratch[i].z', 's->z')
V['i_projp'] = dict(pre=helper2, loop=L('project(&gScratch[i], i);', decls=''))
VARIANTS = V

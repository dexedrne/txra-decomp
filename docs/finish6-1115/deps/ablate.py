#!/usr/bin/env python3
"""ablate.py OUTDIR : one-edit ablations of the installed renderer source (src/generated/func_08016DA8.c).
Score them with batch.py on a worker; receipts/ablations.txt holds the official-compiler results."""
import sys, os
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
base = open('src/generated/func_08016DA8.c').read()
I = ' ' * 28
def v(name, *pairs):
    t = base
    for a, b in pairs:
        assert t.count(a) == 1, (name, a)
        t = t.replace(a, b)
    open(os.path.join(OUT, name + '.c'), 'w').write(t)
v('ab1_dy_one_stmt', (I + 'dy = -gScratch[i].y;\n' + I + 'dy -= gCamera.y;\n', I + 'dy = -gScratch[i].y - gCamera.y;\n'))
v('ab2_shift_late', ('dy = (saved_y * g_03000DF8 - tz * g_03005F58) >> 12;', 'dy = saved_y * g_03000DF8 - tz * g_03005F58;'),
                    ('dy += gOffset.z;', 'dy = gOffset.z + (dy >> 12);'))
v('ab3_no_copy', ('s32 dx, dy, dz, tx, ty, tz, f, sy, saved_y;', 's32 dx, dy, dz, tx, ty, tz, f, sy, t;'),
                 (I + 'saved_y = dy;\n', ''),
                 ('dy = (saved_y * g_03000DF8 - tz * g_03005F58) >> 12;', 't = (dy * g_03000DF8 - tz * g_03005F58) >> 12;'),
                 ('ty = saved_y * g_03005F58', 'ty = dy * g_03005F58'),
                 ('dy += gOffset.z;', 'dy = t + gOffset.z;'))
v('ab4_tx_in_place', ('tx = dx * g_03002A18 - dz * g_03001B28;', 'tx = dx * g_03002A18;\n' + I + 'tx -= dz * g_03001B28;'))
v('ab5_copy_after_tz', (I + 'saved_y = dy;\n' + I + 'tz = (dx * g_03001B28 + dz * g_03002A18) >> 12;\n',
                        I + 'tz = (dx * g_03001B28 + dz * g_03002A18) >> 12;\n' + I + 'saved_y = dy;\n'))
v('ab6_off_first', ('dy += gOffset.z;', 'dy = gOffset.z + dy;'))
v('ab7_dx_one_stmt', (I + 'dx = gScratch[i].x;\n' + I + 'dx -= gCamera.x;\n', I + 'dx = gScratch[i].x - gCamera.x;\n'))
v('ab8_ty_first', (I + 'dy = (saved_y * g_03000DF8 - tz * g_03005F58) >> 12;\n' + I + 'ty = saved_y * g_03005F58 + tz * g_03000DF8;\n',
                   I + 'ty = saved_y * g_03005F58 + tz * g_03000DF8;\n' + I + 'dy = (saved_y * g_03000DF8 - tz * g_03005F58) >> 12;\n'))

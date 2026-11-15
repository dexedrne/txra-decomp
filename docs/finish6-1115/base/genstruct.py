#!/usr/bin/env python3
"""Struct/base groupings of the renderer's globals on the exact source sib1.c (finish 6, base lane).
    python3 genstruct.py OUTDIR
Each variant regroups globals that sit close together into one struct (same addresses), so loads
can share a base register; the measurement shows which groupings keep the cartridge's bytes."""
import sys
from pathlib import Path
src = Path('docs/finish6-1115/base/c/sib1.c').read_text()
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
def rep(s, a, b, n=1):
    assert s.count(a) == n, (a, s.count(a)); return s.replace(a, b)
V = {}
# S1: depth array = .z of the 12-byte rows at 0x030055F0 (as 080164D0 / 080162F8 write it)
s = rep(src, 'extern Vec3 g_030055F8[];\n', 'extern Vec3 g_030055F0[];\n')
V['s1_depth55F0z'] = rep(s, 'g_030055F8[i].x = y;', 'g_030055F0[i].z = y;')
# S2: one view struct at 0x03005F58 holding the pitch sine, the camera and the offset
VIEW = 'typedef struct { s32 sinp; s32 pad0[5]; Vec3 cam; s32 pad1; Vec3 off; } View;\n'
s = rep(src, 'extern Vec3 g_03005F70;\nextern Vec3 g_03005F80;\n', VIEW + 'extern View g_03005F58;\n')
s = rep(s, 'extern s32 g_03002A18, g_03001B28, g_03005F58, g_03000DF8;', 'extern s32 g_03002A18, g_03001B28, g_03000DF8;')
s = rep(s, '#define gCamera g_03005F70\n#define gOffset g_03005F80\n', '#define gCamera g_03005F58.cam\n#define gOffset g_03005F58.off\n')
V['s2_viewF58'] = rep(s, '* g_03005F58', '* g_03005F58.sinp', 2)
# S3: one struct at 0x03000DE0 holding the special-sprite count and the pitch cosine
s = rep(src, 'extern s32 g_03000DE0;\n', 'typedef struct { s32 count; s32 pad0[5]; s32 cosp; } Misc;\nextern Misc g_03000DE0;\n')
s = rep(s, 'extern s32 g_03002A18, g_03001B28, g_03005F58, g_03000DF8;', 'extern s32 g_03002A18, g_03001B28, g_03005F58;')
s = rep(s, '* g_03000DF8', '* g_03000DE0.cosp', 2)
s = rep(s, 's32 n = g_03000DE0;', 's32 n = g_03000DE0.count;')
V['s3_miscDE0'] = rep(s, 'g_03000DE0 = n + 1;', 'g_03000DE0.count = n + 1;')
# S4: camera and offset in one struct at 0x03005F70
s = rep(src, 'extern Vec3 g_03005F70;\nextern Vec3 g_03005F80;\n',
        'typedef struct { Vec3 cam; s32 pad; Vec3 off; } CamOff;\nextern CamOff g_03005F70;\n')
V['s4_camoffF70'] = rep(s, '#define gCamera g_03005F70\n#define gOffset g_03005F80\n', '#define gCamera g_03005F70.cam\n#define gOffset g_03005F70.off\n')
# S5: S2 + S3
s = V['s2_viewF58']
s = rep(s, 'extern s32 g_03000DE0;\n', 'typedef struct { s32 count; s32 pad0[5]; s32 cosp; } Misc;\nextern Misc g_03000DE0;\n')
s = rep(s, 'extern s32 g_03002A18, g_03001B28, g_03000DF8;', 'extern s32 g_03002A18, g_03001B28;')
s = rep(s, '* g_03000DF8', '* g_03000DE0.cosp', 2)
s = rep(s, 's32 n = g_03000DE0;', 's32 n = g_03000DE0.count;')
V['s5_view_misc'] = rep(s, 'g_03000DE0 = n + 1;', 'g_03000DE0.count = n + 1;')
# S6: pitch cosine and sine as a two-member array view is impossible (DF8 and F58 are 0x5160 apart); camera as s32[3]
s = rep(src, 'extern Vec3 g_03005F70;\n', 'extern s32 g_03005F70[3];\n')
s = rep(s, 'gCamera.x', 'gCamera[0]'); s = rep(s, 'gCamera.y', 'gCamera[1]')
V['s6_cam_array'] = rep(s, 'gCamera.z', 'gCamera[2]')
for k, v in V.items():
    (out / (k + '.c')).write_text(v.replace('/* 08016DA8 renderer experiment (finish 6, base)', '/* 08016DA8 renderer experiment (finish 6, base, struct variant %s)' % k, 1))
print(len(V))

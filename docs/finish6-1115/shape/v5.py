# Batch 5: integer-cast addresses (alias analysis sees no base) for the depth array and friends,
# with the camera/offset z values hoisted in the source.
import runpy
from pathlib import Path
v1 = runpy.run_path(str(Path(__file__).resolve().parent / 'v1.py'))
L, BASE = v1['L'], v1['BASE']
CASTS = {
 'dep': ('extern Vec3 g_030055F8[];', '#define g_030055F8 ((Vec3 *)0x030055F8)'),
 'off': ('extern Vec3 g_03005F80;', '#define g_03005F80 (*(Vec3 *)0x03005F80)'),
 'cam': ('extern Vec3 g_03005F70;', '#define g_03005F70 (*(Vec3 *)0x03005F70)'),
 'tab': ('extern s32 g_0804F330[];', '#define g_0804F330 ((s32 *)0x0804F330)'),
}
HZ = BASE.replace('dz = gScratch[i].z - gCamera.z;', 'dz = gScratch[i].z - cz;').replace('dy = gOffset.z + (t >> 12);', 'dy = gOffset.z + (t >> 12);'.replace('gOffset.z', 'oz'))
V = {}
import itertools
for r in range(1, 5):
    for combo in itertools.combinations(sorted(CASTS), r):
        rep = [CASTS[c] for c in combo]
        n = '_'.join(combo)
        V['a_' + n] = dict(loop=L(BASE), rep=list(rep))
        V['h_' + n] = dict(loop=L(HZ, decls='s32 dx, dy, dz, tz, f, sy, t;', pre_loop='s32 cz = gCamera.z, oz = gOffset.z;'), rep=list(rep))
        V['hf_' + n] = dict(decl='    s32 cz, oz;', loop=L(HZ, pre_loop='cz = gCamera.z; oz = gOffset.z;'), rep=list(rep))
V['h_none'] = dict(loop=L(HZ, pre_loop='s32 cz = gCamera.z, oz = gOffset.z;'))
VARIANTS = V

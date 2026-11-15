/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
/* Car model vertex projection: rotates a model point by the car's two angle
 * pairs (stored in the four trig globals), moves it into camera space,
 * rotates by the camera angles and writes depth and screen x/y. The same
 * statements as the ARM point-grid routine 08016C18 and Thumb 080164D0:
 * the first rotation reuses xx (the copied x), saved_y and zz, which is
 * what gives the original's spill set (frame 60, five untouched slots). */
extern TxraRecord g_03001E60[];
extern TxraTriple g_03005F80, g_03005F70, g_030057A0[], g_030055F0[];
extern s32 g_083D2280[], g_083C2280[], g_0804F330[];
extern s32 g_03005FC8, g_03005B30, g_03002E5C, g_030061E0;
extern s32 g_03002A18, g_03001B28, g_03000DF8, g_03005F58;
void func_080162F8(s32 point, s32 slot)
{
    s32 ox, oy, oz, dx, dy, dz;
    s32 x, y, z, xx, zz, saved_y;
    s32 factor;
    ox = g_03005F80.field_00;
    oy = g_03005F80.field_04;
    oz = g_03005F80.field_08;
    dx = g_03005F70.field_00 - g_03001E60[slot].field_04;
    dy = g_03005F70.field_04 - g_03001E60[slot].field_08;
    dz = g_03005F70.field_08 - g_03001E60[slot].field_0c;
    g_03005FC8 = g_083D2280[g_03001E60[slot].field_24];
    g_03005B30 = g_083C2280[g_03001E60[slot].field_24];
    g_03002E5C = g_083D2280[g_03001E60[slot].field_20];
    g_030061E0 = g_083C2280[g_03001E60[slot].field_20];
    x = g_030057A0[point].field_00;
    y = -g_030057A0[point].field_04;
    z = g_030057A0[point].field_08;
    xx = x;
    saved_y = (y * g_03005FC8 - z * g_03005B30) >> 12;
    zz = (y * g_03005B30 + z * g_03005FC8) >> 12;
    x = (xx * g_03002E5C - zz * g_030061E0) >> 12;
    z = (xx * g_030061E0 + zz * g_03002E5C) >> 12;
    x -= dx;
    y = saved_y - dy;
    z -= dz;
    xx = (x * g_03002A18 - z * g_03001B28) >> 12;
    saved_y = y;
    zz = (x * g_03001B28 + z * g_03002A18) >> 12;
    y = (saved_y * g_03000DF8 - zz * g_03005F58) >> 12;
    z = (saved_y * g_03005F58 + zz * g_03000DF8) >> 12;
    x = xx + ox;
    z += oy;
    y += oz;
    g_030055F0[point].field_08 = y;
    x <<= 3;
    z <<= 3;
    y >>= 1;
    factor = g_0804F330[y + 0x10000];
    g_030055F0[point].field_00 = ((x * factor) >> 15) + 120;
    g_030055F0[point].field_04 = ((z * factor) >> 15) + 80;
}

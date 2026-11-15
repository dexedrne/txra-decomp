/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
typedef struct { s32 x,y,z; } DeepVector;
extern DeepVector g_030057A0[],g_03005F70,g_03005F80,g_030055F0[];
extern s32 g_03002A18,g_03001B28,g_03000DF8,g_03005F58,g_0804F330[];
void func_080164D0(u32 index)
{
    s32 x,y,z;
    s32 xx,zz,saved_y;
    s32 factor;
    x = g_030057A0[index].x - g_03005F70.x;
    y = g_030057A0[index].y - g_03005F70.y;
    z = g_030057A0[index].z - g_03005F70.z;
    xx = (x * g_03002A18 - z * g_03001B28) >> 12;
    saved_y = y;
    zz = (x * g_03001B28 + z * g_03002A18) >> 12;
    y = (saved_y * g_03000DF8 - zz * g_03005F58) >> 12;
    z = (saved_y * g_03005F58 + zz * g_03000DF8) >> 12;
    x = xx + g_03005F80.x;
    z += g_03005F80.y;
    y += g_03005F80.z;
    g_030055F0[index].z = y;
    x <<= 3;
    z <<= 3;
    y >>= 1;
    factor = g_0804F330[y+0x10000];
    g_030055F0[index].x = ((x*factor)>>16)+60;
    g_030055F0[index].y = ((z*factor)>>15)+80;
}

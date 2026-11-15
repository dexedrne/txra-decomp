/* Byte-verified C; address name retained pending semantic review.
 * Stat scaling for one racer from the setup bytes at g_03000B60. The ten
 * stats are a two-dimensional s16 array, so each field address is
 * index * 20 + (base + offset) as in the original; the product is one
 * function-level temporary loaded, shifted and divided in place; the
 * last two factors use block temporaries so fold cannot reassociate the
 * - 4 and local allocation alternates r0/r1 like the original. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
typedef struct { s16 v[14]; } TxraCurve28;
extern s16 g_030046E0[][10];
extern TxraCurve28 g_080205C4[];
extern TxraRecord g_03001E60[];
extern u8 g_03000B60[];
/* field += field * 32 * (coefficient * factor) / 100 / 32, with the
 * product held in one function-level temporary p. */
#define BUMP(field, coefficient, factor) \
    { p = (field); p <<= 5; p *= (coefficient) * (factor); p /= 100; p /= 32; (field) += p; }
void func_0800A940(s32 index)
{
    s32 model = g_03001E60[index].field_02 - 16;
    s32 first, second, third, p;
    if (g_03000B60[17] != 0) g_03001E60[index].field_5a = 6 - g_03000B60[17] * 2;
    first = g_03000B60[15] - 1;
    first += (g_03000B60[14] - 1) * 3;
    BUMP(g_030046E0[index][0], g_080205C4[model].v[0], first);
    BUMP(g_030046E0[index][2], g_080205C4[model].v[1], first);
    BUMP(g_030046E0[index][4], g_080205C4[model].v[2], first);
    BUMP(g_030046E0[index][6], g_080205C4[model].v[3], first);
    BUMP(g_030046E0[index][8], g_080205C4[model].v[4], first);
    second = g_03000B60[16] - 1;
    BUMP(g_030046E0[index][1], g_080205C4[model].v[5], second);
    BUMP(g_030046E0[index][3], g_080205C4[model].v[6], second);
    BUMP(g_030046E0[index][5], g_080205C4[model].v[7], second);
    BUMP(g_030046E0[index][7], g_080205C4[model].v[8], second);
    BUMP(g_030046E0[index][9], g_080205C4[model].v[9], second);
    BUMP(g_03001E60[index].field_60, g_080205C4[model].v[10], second);
    third = g_03000B60[18] + g_03000B60[19] * 2;
    { s32 t = third - 4; third = g_03000B60[20] + t; }
    BUMP(g_03001E60[index].field_58, g_080205C4[model].v[11], third);
    { s32 f = g_03000B60[19] - 1; BUMP(g_03001E60[index].field_56, g_080205C4[model].v[12], f); }
}

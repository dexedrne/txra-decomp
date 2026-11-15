/* Byte-verified C; address name retained pending semantic review.
 * Stat scaling by the racer's grade (record halfword 0x62), the sibling of
 * 0800A940 with the same update macro. The first read goes through p
 * before the divide (the original's copy), and the /16 and /64 factors are
 * two separate variables, which gives the original's global allocation
 * order (factor in r8 after the row, index and base registers). */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
typedef struct { s16 v[14]; } TxraCurve28;
extern s16 g_030046E0[][10];
extern TxraCurve28 g_080205C4[];
extern TxraRecord g_03001E60[];
/* field += field * 32 * (coefficient * factor) / 100 / 32, with the
 * product held in one function-level temporary p (as in 0800A940). */
#define BUMP(field, coefficient, factor) \
    { p = (field); p <<= 5; p *= (coefficient) * (factor); p /= 100; p /= 32; (field) += p; }
void func_0800AC3C(s32 index)
{
    s32 grade, p;
    s32 level, speed;
    p = g_03001E60[index].field_62;
    grade = p / 32;
    g_03001E60[index].field_5a = 6 - grade;
    level = g_03001E60[index].field_62 / 16;
    BUMP(g_030046E0[index][0], g_080205C4[grade].v[0], level);
    BUMP(g_030046E0[index][2], g_080205C4[grade].v[1], level);
    BUMP(g_030046E0[index][4], g_080205C4[grade].v[2], level);
    BUMP(g_030046E0[index][6], g_080205C4[grade].v[3], level);
    BUMP(g_030046E0[index][8], g_080205C4[grade].v[4], level);
    speed = g_03001E60[index].field_62 / 64;
    BUMP(g_030046E0[index][1], g_080205C4[grade].v[5], speed);
    BUMP(g_030046E0[index][3], g_080205C4[grade].v[6], speed);
    BUMP(g_030046E0[index][5], g_080205C4[grade].v[7], speed);
    BUMP(g_030046E0[index][7], g_080205C4[grade].v[8], speed);
    BUMP(g_030046E0[index][9], g_080205C4[grade].v[9], speed);
    BUMP(g_03001E60[index].field_60, g_080205C4[grade].v[10], speed);
    { s32 f = (s16)(g_03001E60[index].field_62 / 12); BUMP(g_03001E60[index].field_58, g_080205C4[grade].v[11], f); }
    { s32 f = g_03001E60[index].field_62 / 32; BUMP(g_03001E60[index].field_56, g_080205C4[grade].v[12], f); }
}

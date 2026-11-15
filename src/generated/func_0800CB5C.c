/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
/* Per-car drive update (reading of the fields is provisional): acceleration
 * from a per-car gear table, automatic shifting or button shifting for the
 * player, speed clamps, movement along the heading plus a sideways slide,
 * slide decay with heading recovery, and a small speed decay. The table lookups mask their angle even
 * though the heading was already masked; combine folds the double mask into
 * the index, which places the AND after the table base as in the ROM. */
typedef struct {
    s16 field_00, field_02;
    u32 field_04, field_08, field_0c;
    s32 field_10, field_14, field_18, field_1c;
    s32 field_20, field_24, field_28;
    s32 field_2c, field_30;
    s32 field_34;
    s16 field_38;
    s16 field_3a, field_3c, field_3e;
    u8 unknown_40[2];
    s16 field_42, field_44;
    u8 unknown_46[2];
    s16 field_48;
    u8 unknown_4a[2];
    s16 field_4c, field_4e, field_50, field_52;
    u8 unknown_54[6];
    s16 field_5a;
    s16 field_5c;
    s16 field_5e, field_60;
    s16 field_62;
} CarState;
extern CarState g_03001E60[];
extern s16 g_030046E0[][5][2];
extern s16 g_03002A1C, g_03005F54;
extern u16 g_030001BC, g_0300218C;
extern s32 g_083D2280[], g_083C2280[];
extern s32 func_08014614(s32, s32);
#define SIN(a) g_083D2280[(a) & 16383]
#define COS(a) g_083C2280[(a) & 16383]
void func_0800CB5C(s32 slot)
{
    s32 old_x, old_z;
    s32 heading, step, diff;
    g_03001E60[slot].field_2c = 0;
    old_x = g_03001E60[slot].field_04;
    old_z = g_03001E60[slot].field_0c;
    if ((g_03001E60[slot].field_44 & 1) && !(g_03001E60[slot].field_44 & 2))
        g_03001E60[slot].field_2c = g_030046E0[slot][g_03001E60[slot].field_52][0];
    if (g_03001E60[slot].field_44 & 2)
        g_03001E60[slot].field_2c = -512;
    g_03001E60[slot].field_28 += g_03001E60[slot].field_2c >> 3;
    if (slot != 0 || !g_03002A1C || g_03005F54 || (g_030001BC & 32)) {
        if (g_03001E60[slot].field_28 > g_030046E0[slot][g_03001E60[slot].field_52][1]) {
            if (g_03001E60[slot].field_52 <= 3) {
                if (g_03001E60[slot].field_5c > g_03001E60[slot].field_5a) {
                    g_03001E60[slot].field_52++;
                    g_03001E60[slot].field_5c = 0;
                } else {
                    g_03001E60[slot].field_5c++;
                    g_03001E60[slot].field_28 -= 64;
                }
            }
        } else if (g_03001E60[slot].field_52 > 0
                   && g_03001E60[slot].field_28 < g_030046E0[slot][g_03001E60[slot].field_52 - 1][1] - 8) {
            g_03001E60[slot].field_52--;
        }
    } else {
        if (g_03001E60[0].field_28 > g_030046E0[0][g_03001E60[0].field_52][1] + g_030046E0[0][g_03001E60[0].field_52][0]
            && g_03001E60[0].field_52 <= 3)
            g_03001E60[0].field_28 -= g_030046E0[0][g_03001E60[0].field_52][0];
        if ((g_0300218C & 256) && g_03001E60[slot].field_52 <= 3) g_03001E60[slot].field_52++;
        if ((g_0300218C & 512) && g_03001E60[slot].field_52 > 0) g_03001E60[slot].field_52--;
    }
    if (g_03001E60[slot].field_28 < -512) g_03001E60[slot].field_28 = -512;
    if (g_03001E60[slot].field_28 > g_03001E60[slot].field_60) g_03001E60[slot].field_28 = g_03001E60[slot].field_60;
    step = g_03001E60[slot].field_28 >> 3;
    heading = ((g_03001E60[slot].field_34 >> 3) + 12288) & 16383;
    g_03001E60[slot].field_04 = old_x + (step * SIN(heading) >> 12);
    g_03001E60[slot].field_0c = old_z + (step * COS(heading) >> 12);
    step = g_03001E60[slot].field_3c >> 3;
    heading = (g_03001E60[slot].field_3a + 12288) & 16383;
    g_03001E60[slot].field_04 += step * SIN(heading) >> 12;
    g_03001E60[slot].field_0c += step * COS(heading) >> 12;
    if (g_03001E60[slot].field_3c > 0) {
        g_03001E60[slot].field_3c -= 256;
        if (g_03001E60[slot].field_3c < 0) g_03001E60[slot].field_3c = 0;
    }
    if (g_03001E60[slot].field_3c < 0) {
        g_03001E60[slot].field_3c += 256;
        if (g_03001E60[slot].field_3c > 0) g_03001E60[slot].field_3c = 0;
    }
    if (g_03001E60[slot].field_3c) {
        diff = func_08014614(g_03001E60[slot].field_20, g_03001E60[slot].field_3e);
        if (diff > 8191) diff -= 16384;
        diff >>= 1;
        g_03001E60[slot].field_20 = (g_03001E60[slot].field_20 + diff) & 16383;
    }
    if (g_03001E60[slot].field_3c > 192 && g_03001E60[slot].field_28 > 1600) g_03001E60[slot].field_28 -= 64;
    if (g_03001E60[slot].field_28 > 6) g_03001E60[slot].field_28 -= 6;
    else if (g_03001E60[slot].field_28 > 0) g_03001E60[slot].field_28--;
    else if (g_03001E60[slot].field_28 < -4) g_03001E60[slot].field_28 += 4;
    else if (g_03001E60[slot].field_28 < 0) g_03001E60[slot].field_28++;
}

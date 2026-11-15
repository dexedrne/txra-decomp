/* Byte-verified C; address name retained pending semantic review.
 * Steering, heading and camera update for one racer. Each block takes its
 * own record pointer (block 1's lives in a call-clobbered register, the
 * later one across calls), the first access in each block is a direct
 * index so the record base is loaded before the multiply, the two flag
 * tests are nested ifs (fold would merge them into one mask), and one
 * diff variable carries the angle differences, the decay step and the tilt. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern TxraRecord g_03001E60[];
extern TxraRow28 *g_03006874;
extern s32 func_08014614(s32, s32);
extern void func_0801604C(u32, u32);
extern s32 g_030021D4;
extern s16 g_030021CC;
extern TxraTriple g_03002E40;
void func_0800C3C4(s32 slot)
{
    TxraRecord *a, *b, *c, *q, *t;
    s32 steer, diff;
    if (g_03001E60[slot].field_40 > 0) g_03001E60[slot].field_40--;
    a = &g_03001E60[slot];
    steer = g_03001E60[slot].field_30;
    if (a->field_44 & 32) {
        if (steer > a->field_56) steer = a->field_56 - 350;
        if (steer > 0) steer -= 250;
        steer -= a->field_54;
        if (steer < -a->field_58 && g_03001E60[slot].field_28 > 1920) {
            g_03001E60[slot].field_28 -= 64;
            steer = -a->field_58;
            if (slot == 0 && g_03001E60[0].field_40 == 0) {
                func_0801604C(14, 1);
                g_03001E60[0].field_40 = 64;
                if (g_03001E60[0].field_3c == 0) {
                    g_03001E60[0].field_3c = 16;
                    g_03001E60[0].field_3a = (g_03001E60[0].field_20 - 4096) & 16383;
                    g_03001E60[0].field_3e = g_03001E60[0].field_20 & 16383;
                }
            }
        }
    }
    if (g_03001E60[slot].field_44 & 16) {
        b = &g_03001E60[slot];
        if (steer < -b->field_56) steer = 350 - b->field_56;
        if (steer < 0) steer += 250;
        steer += b->field_54;
        if (steer > b->field_58 && g_03001E60[slot].field_28 > 1920) {
            g_03001E60[slot].field_28 -= 64;
            steer = b->field_58;
            if (slot == 0 && g_03001E60[0].field_40 == 0) {
                func_0801604C(14, 1);
                g_03001E60[0].field_40 = 64;
                if (g_03001E60[0].field_3c == 0) {
                    g_03001E60[0].field_3c = 16;
                    g_03001E60[0].field_3a = (g_03001E60[0].field_20 + 4096) & 16383;
                    g_03001E60[0].field_3e = g_03001E60[0].field_20 & 16383;
                }
            }
        }
    }
    if (!(g_03001E60[slot].field_44 & 32)) if (!(g_03001E60[slot].field_44 & 16)) {
        c = &g_03001E60[slot];
        if (steer < -c->field_56) steer = -c->field_56;
        if (steer > c->field_56) steer = c->field_56;
        diff = steer >> 2;
        if (steer) steer -= diff;
    }
    g_03001E60[slot].field_30 = steer;
    q = &g_03001E60[slot];
    if (steer < -q->field_56) steer = -q->field_56;
    if (steer > q->field_56) steer = q->field_56;
    if (g_03001E60[slot].field_28 < 0) {
        steer = -steer;
        steer >>= 1;
        g_03001E60[slot].field_20 = (g_03001E60[slot].field_20 - (steer >> 3)) & 16383;
    }
    if (g_03001E60[slot].field_28 > 0) {
        steer >>= 1;
        g_03001E60[slot].field_20 = (g_03001E60[slot].field_20 - (steer >> 3)) & 16383;
    }
    diff = func_08014614(g_03001E60[slot].field_20, (g_03006874[q->field_38].field_0c + 4096) & 16383);
    if (diff > 8191) diff -= 8192;
    if (diff < -3600) g_03001E60[slot].field_20 = g_03006874[q->field_38].field_0c + 7694;
    if (diff > 3600) g_03001E60[slot].field_20 = g_03006874[q->field_38].field_0c + 498;
    g_03001E60[slot].field_20 &= 16383;
    diff = func_08014614(g_03001E60[slot].field_34 >> 3, g_03001E60[slot].field_20);
    if (diff > 8191) diff -= 16384;
    diff <<= 3;
    g_03001E60[slot].field_34 = (g_03001E60[slot].field_34 + diff) & 131071;
    diff = 0;
    if (steer > 400) diff = (((steer - 400) >> 1) * g_03001E60[slot].field_28) >> 14;
    if (steer < -400) diff = (((steer + 400) >> 1) * g_03001E60[slot].field_28) >> 14;
    t = &g_03001E60[slot];
    if (diff > t->field_4e) t->field_4e++;
    if (diff < t->field_4e) t->field_4e--;
    if (g_030021D4 == 1 && g_030021CC == 0) {
        diff = func_08014614((8192 - (g_03001E60[slot].field_34 >> 3)) & 16383, g_03002E40.field_04) & 16383;
        if (diff > 8191) diff -= 16384;
        if ((u32)(diff + 4) > 8) {
            diff >>= 2;
            if (diff < -60) diff = -60;
            if (diff > 60) diff = 60;
            g_03002E40.field_04 -= diff;
        } else {
            if (diff < 0) g_03002E40.field_04++;
            if (diff > 0) g_03002E40.field_04--;
        }
        diff = func_08014614((4096 - g_03002E40.field_04) & 16383, g_03006874[g_03001E60[slot].field_38].field_0c & 16383);
        if (diff > 8191) diff -= 16384;
        if (diff < -768) g_03002E40.field_04 = 3328 - g_03006874[g_03001E60[slot].field_38].field_0c;
        if (diff > 768) g_03002E40.field_04 = 4864 - g_03006874[g_03001E60[slot].field_38].field_0c;
        g_03002E40.field_04 &= 16383;
    }
    if (g_030021D4 == 0) g_03002E40.field_04 = (8192 - g_03001E60[slot].field_20) & 16383;
}

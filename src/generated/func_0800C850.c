/* Byte-verified C; address name retained pending semantic review.
 * Track-position update for one racer record. Same template as the matched
 * neighbour 0800C9C4: record fields indexed directly, the x address taken
 * before the row base is read, and the row address as at * 28 + base. The
 * unused wrap of next + 1 (after) is the original's dead add: flow keeps
 * the add because the compare still reads it, and jump later drops the
 * empty conditional. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern TxraRecord g_03001E60[];
extern s32 g_03002E4C;
extern s16 g_030021CC;
extern TxraRow28 *g_03006874;
extern s32 g_083D2280[], g_083C2280[];
extern s32 g_030001B8, g_03002334, g_03005F50;
extern void func_08002854(void);
void func_0800C850(s32 index)
{
    s32 at = g_03001E60[index].field_38;
    s32 prev = at - 1;
    s32 next, after;
    TxraRow28 *a, *base;
    s32 *xaddr;
    s32 x, z, angle, side, ahead, sine;
    if (prev < 0) prev += g_03002E4C;
    next = at + 1;
    if (next >= g_03002E4C) next = 0;
    after = next + 1;
    if (after >= g_03002E4C) after = 0;
    xaddr = &g_03001E60[index].field_04;
    base = g_03006874;
    a = (TxraRow28 *)(at * 28 + (u32)base);
    x = *xaddr - a->field_00;
    z = g_03001E60[index].field_0c - a->field_08;
    angle = (4096 - a->field_0c) & 16383;
    sine = g_083D2280[angle];
    side = (x * sine - z * g_083C2280[angle]) >> 12;
    ahead = (x * g_083C2280[angle] + z * sine) >> 12;
    g_03001E60[index].field_42 = (side + 0x300) >> 4;
    if (ahead > 0x1FF) {
        at = next;
        if (index == 0 && g_030021CC == 0) {
            g_030001B8 = (g_030001B8 + 1) & 31;
            g_03002334 = index;
            g_03005F50 = at;
            func_08002854();
        }
    }
    if (ahead < 0) {
        if (index == 0 && g_030021CC == 0) {
            if (at == next) g_030001B8 -= 2;
            else g_030001B8 -= 1;
            g_030001B8 &= 31;
            g_03002334 = 1;
        }
        at = prev;
        if (index == 0 && g_030021CC == 0) {
            g_03005F50 = at;
            func_08002854();
        }
    }
    g_03001E60[index].field_38 = at;
}

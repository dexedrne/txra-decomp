/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern TxraRecord g_03001E60[];
extern s32 g_030021D4;
extern TxraRow28 *g_03006874;
extern u16 g_03000B54;
extern u16 g_03002C30[];
extern void func_0801604C(u32, u32);
void func_0800841C(s32 index)
{
    s32 mode, i, v;
    s32 w;
    if (g_030021D4 == 0) return;
    mode = 0;
    v = g_03001E60[index].field_42;
    if (v <= 31) {
        w = g_03006874[g_03001E60[index].field_38].field_0e;
        if (w == 2) mode = 1;
        if (w == 6) mode = 2;
    }
    if (v >= 32 && v <= 63) {
        w = g_03006874[g_03001E60[index].field_38].field_0f;
        if (w == 2) mode = 1;
        if (w == 4) mode = 1;
    }
    if (v > 63) {
        w = g_03006874[g_03001E60[index].field_38].field_10;
        if (w == 2) mode = 1;
        if (w == 6) mode = 2;
    }
    if (mode == 0) {
        for (i = 0; i < 40; i++) g_03002C30[i + 192] = g_03002C30[i];
        if (g_03000B54 == 32) func_0801604C(31, 0);
    }
    if (mode == 1) {
        for (i = 0; i < 40; i++) {
            s32 r, g;
            w = g_03002C30[i];
            r = w & 31; g = (w >> 5) & 31;
            w = (w >> 10) & 31;
            r -= 4; if (r < 0) r = 0;
            g -= 4; if (g < 0) g = 0;
            w -= 4; if (w < 0) w = 0;
            g_03002C30[i + 192] = r + (g << 5) + (w << 10);
        }
        if (g_03000B54 == 31 && g_03006874[g_03001E60[index].field_38].field_16 != 0) func_0801604C(32, 0);
    }
    if (mode == 2) {
        for (i = 0; i < 40; i++) {
            s32 r, g;
            w = g_03002C30[i];
            r = w & 31; g = (w >> 5) & 31;
            w = (w >> 10) & 31;
            r += 2; if (r > 31) r = 31;
            g += 2; if (g > 31) g = 31;
            if (w > 31) w = 31;
            g_03002C30[i + 192] = r + (g << 5) + (w << 10);
        }
    }
}

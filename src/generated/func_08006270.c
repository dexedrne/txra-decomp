/* Byte-verified C; address name retained pending semantic review.
 * Sound stream mixer for one channel. The first loop reads the channel's
 * sample index through a pointer and the record table through a second
 * pointer to its +16 limit word; the mixing temporary v is one function-level
 * variable shared by the two halving loops. */
#ifndef TXRA_BASIC_TYPES
#define TXRA_BASIC_TYPES
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#endif
#include "types.h"
extern u32 g_030079D0[], g_03006A88[], g_03006890[], g_030075E8[];
extern s32 g_03006A98, g_03006A80;
extern u32 g_0300757C;
extern s8 g_03007600[];
void func_08006270(s32 ch)
{
    s8 *src;
    s32 buf, i, v;
    u32 pos;
    src = (s8 *)g_03006A88[ch];
    if (src) {
        if (g_03006890[ch] == 0) {
            if (g_030075E8[ch] == 0) {
                src = 0;
                g_03006A88[ch] = (u32)src;
            } else {
                g_03006A88[ch] = g_083B8378[g_030079D0[ch]].field_00;
                g_03006890[ch] = g_083B8378[g_030079D0[ch]].field_04 - 1;
                src = (s8 *)g_03006A88[ch];
            }
        } else {
            g_03006890[ch]--;
        }
    }
    buf = (g_03006A98 + 1) & 1;
    if (ch == 0) {
        if (src == 0) return;
        pos = g_0300757C;
        for (i = 0; i < 176; i++) {
            g_03007600[buf * 176 + i] = src[(s32)pos >> 4];
            {
                u32 *index = &g_030079D0[ch];
                u32 *limits = (u32 *)((u8 *)g_083B8378 + 16);
                pos += g_03006A80;
                if (pos >= *(u32 *)((u8 *)limits + *index * 20)) pos = 0;
            }
        }
        g_0300757C = pos;
        g_03006890[ch] = 4;
    } else if (src) {
        for (i = 0; i < 176; i++) {
            v = g_03007600[buf * 176 + i] + *src;
            src++;
            v >>= 1;
            g_03007600[buf * 176 + i] = v;
        }
    } else {
        for (i = 0; i < 176; i++) {
            v = g_03007600[buf * 176 + i];
            v >>= 1;
            g_03007600[buf * 176 + i] = v;
        }
    }
    g_03006A88[ch] = (u32)src;
}

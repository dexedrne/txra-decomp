/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern volatile u32 g_03005FC0;
extern u16 g_02003C00[], g_0832F29C[];
/* Blend blit of a 120x48 halfword block: a source halfword with an empty
 * low or high byte keeps that byte of the destination. The volatile read
 * of g_03005FC0 is in the original; the two always-zero terms built from it
 * are folded only by combine, after CSE, so height and the source base carry
 * no constant equivalence and get the original register priorities. */
void func_08014104(void)
{
    u32 tick;
    u32 width;
    s32 height;
    u32 destbase;
    u32 sourcebase;
    s32 y;
    s32 x;
    tick = g_03005FC0;
    width = 120;
    height = 48 + ((u8)tick >> 8);
    destbase = (u32)g_02003C00;
    sourcebase = (u32)g_0832F29C + ((u16)tick >> 16);
    y = 0;
    do {
        for (x = 0; x < (s32)width; x++) {
            u16 *dest = (u16 *)(destbase + y * 240);
            u16 *source = (u16 *)(sourcebase + y * 240);
            u32 value = source[x];
            if (value) {
                if (!(value & 0xFF))
                    dest[x] = (dest[x] & 0xFF) + value;
                else if (!(value & 0xFF00))
                    dest[x] = (dest[x] & 0xFF00) + value;
                else
                    dest[x] = value;
            }
        }
        y++;
    } while (y < height);
}

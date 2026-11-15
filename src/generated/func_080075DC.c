/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern u32 g_03007570, g_030079B0, g_030079B4, g_030079C8, g_030079C4;
extern u32 g_03006A88[2];
void func_080075DC(void)
{
    if (g_03007570) {
        g_030079B0 = g_030079C8;
        g_030079B4 = g_030079C4;
        g_03007570 = 0;
    }
    g_03006A88[0] = 0;
    g_03006A88[1] = 0;
}

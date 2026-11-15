/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern s32 g_030001C8;
extern u8 g_030079F0[2];
extern u32 g_03001B1C;
void func_08014790(u8 request)
{
    if (g_030001C8 <= 1) {
        g_030079F0[0] = 0;
        if (request == 0)
            g_030079F0[1] = g_03001B1C;
        g_030079F0[0] = request;
    }
}

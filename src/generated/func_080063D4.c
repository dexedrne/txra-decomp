/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern u32 g_03006A98;
extern u32 g_03007410[2][44], g_03007600[2][44];
void func_080063D4(void)
{
    u32 active, next;
    s32 i;
    u32 *p;
    active = g_03006A98;
    active++;
    active &= 1;
    g_03006A98 = active;
    *(vu32 *)0x04000100 = 0;
    *(vu32 *)0x040000C4 = 0;
    *(vu32 *)0x040000C0 = 0x040000A0;
    *(vu32 *)0x040000BC = (u32)g_03007410[active];
    *(vu32 *)0x04000100 = 0x0080F9C4;
    *(vu32 *)0x040000C4 = 0xBE400000;
    *(vu32 *)0x040000C4;
    *(vu32 *)0x04000104 = 0;
    *(vu32 *)0x040000D0 = 0;
    *(vu32 *)0x040000CC = 0x040000A4;
    *(vu32 *)0x040000C8 = (u32)g_03007600[active];
    *(vu32 *)0x04000104 = 0x0080F99D;
    *(vu32 *)0x040000D0 = 0xBE400000;
    *(vu32 *)0x040000D0;
    next = (active + 1) & 1;
    p = g_03007410[next];
    for (i = 0; i < 44; i++) *p++ = 0;
    p = g_03007600[next];
    for (i = 0; i < 44; i++) *p++ = 0;
}

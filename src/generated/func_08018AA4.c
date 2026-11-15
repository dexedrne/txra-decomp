/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
void func_08018AA4(u32 source, u32 dest, u16 count)
{
    u16 ime = *(vu16 *)0x04000208;
    u16 wait;
    *(vu16 *)0x04000208 = 0;
    wait = *(vu16 *)0x04000204;
    wait &= 0xF8FF;
    wait |= gEepromGeometry->wait_control;
    *(vu16 *)0x04000204 = wait;
    *(vu32 *)0x040000D4 = source;
    *(vu32 *)0x040000D8 = dest;
    *(vu32 *)0x040000DC = count | 0x80000000;
    while (*(vu16 *)0x040000DE & 0x8000) {}
    *(vu16 *)0x04000208 = ime;
}

/* Byte-verified C; address name retained pending semantic review. */
#ifndef TXRA_BASIC_TYPES
#define TXRA_BASIC_TYPES
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#endif
void func_08005D9C(u32 x, s32 y, u16 value, u32 page)
{
    u16 *base = (u16 *)0x06000000;
    if (page == 0) base = (u16 *)0x0600A000;
    if (x <= 119 && y >= 0 && y <= 159) *(u16 *)((u32)(base + x) + y * 240) = value;
}

/* Matched automatically; the address name is kept until reviewed. */
#ifndef TXRA_BASIC_TYPES
#define TXRA_BASIC_TYPES
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#endif
void func_08005EE0(void)
{
    u32 r0;
    u32 r1;
    u32 r2;
    u32 r3;
    r1 = 0x03000670;
    r2 = 0;
    r3 = 255;
    r3 = r3 << 2;
    r0 = r1 + r3;
    do {
        *(vu32 *)r0 = r2;
        r0 -= 4;
    } while ((s32)r0 >= (s32)r1);
}

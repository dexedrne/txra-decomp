/* Matched automatically; the address name is kept until reviewed. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
extern u32 func_08018BE8(u32, u32, u32);
u16 func_08018BD4(u16 a0, u32 a1)
{
    u32 t0;
    t0 = func_08018BE8(a0, a1, 1);
    return t0;
}

/* Matched automatically; the address name is kept until reviewed. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
void func_08014BF8(void)
{
    u32 r1;
    u8 r0;
    r1 = 0x03007A30;
    r0 = *(vu8 *)r1;
    if (r0 != 0)
    {
        *(vu8 *)(r1 + 8) = 1;
    }
}

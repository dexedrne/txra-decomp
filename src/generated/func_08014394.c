/* Matched automatically; the address name is kept until reviewed. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
void func_08014394(void)
{
    u32 r0;
    u32 *r2;
    u32 *r3;
    u32 r1;
    r3 = (u32 *)0x02000000;
    r2 = (u32 *)0x02010000;
    r1 = 0x2000;
    do {
        r0 = *r3++;
        *r2++ = r0;
        r1--;
    } while (r1 != 0);
}

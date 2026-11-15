/* Matched automatically; the address name is kept until reviewed. */
#ifndef TXRA_BASIC_TYPES
#define TXRA_BASIC_TYPES
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#endif
u32 func_08005C7C(void)
{
    u32 r0;
    u32 r1;
    u32 r2;
    u32 r3;
    u32 r4;
    u32 r5;
    u32 r6;

    r4 = 0;
    *(vu32 *)0x030014B8 = r4;
    *(vu32 *)0x03005F40 = r4;
    *(vu32 *)0x03000AC4 = r4;
    r6 = 0x030014B8;
    r5 = 0x03005F40;
    r2 = 0x03000AC4;
    r3 = 0x03000B60;
    r1 = 3;
    do {
        r0 = *(u8 *)r3;
        if (r0 == 0) {
            goto _L_08005CD4;
        }
        r4 += 1;
        r0 = *(u8 *)(r3 + 2);
        r0 -= 0x10;
        r0 = (u8)r0;
        if (r0 <= 5) {
            r0 = *(u32 *)r6;
            r0 += 1;
            *(u32 *)r6 = r0;
        }
        r0 = *(u8 *)(r3 + 2);
        r0 -= 0x16;
        r0 = (u8)r0;
        if (r0 <= 4) {
            r0 = *(u32 *)r5;
            r0 += 1;
            *(u32 *)r5 = r0;
        }
        r0 = *(u8 *)(r3 + 2);
        r0 -= 0x1B;
        r0 = (u8)r0;
        if (r0 > 4) {
            goto _L_08005CD4;
        }
        r0 = *(u32 *)r2;
        r0 += 1;
        *(u32 *)r2 = r0;
_L_08005CD4:
        r3 += 0x20;
        r1 -= 1;
    } while ((s32)r1 >= 0);
    r0 = r4;
    return r0;
}

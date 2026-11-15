/* Matched automatically; the address name is kept until reviewed. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
void func_08007510(u32 r0) {
    u32 r4;
    u32 r5;
    vu32 *r3;
    vu32 *r2;
    s32 r1;

    r4 = r0;
    r5 = 0;
    r3 = (vu32 *)0x03006A88;
    r2 = (vu32 *)0x030079D0;
    r1 = 1;
    do {
        if (*(u32 *)r2 == r4) {
            *(u32 *)r3 = r5;
        }
        r3++;
        r2++;
        r1--;
    } while (r1 >= 0);
}

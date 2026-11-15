/* Matched automatically; the address name is kept until reviewed. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
void func_0800ED28(u32 r0) {
    u32 r1;
    u32 r2;
    u32 r3;
    u32 r4;
    u32 r5;
    u32 r6;
    u32 r7;

    r3 = r0;
    r2 = 0x03005784;
    r0 = *(u32 *)0x03000B50;
    r0 += 1;
    r0 <<= 5;
    r1 = *(u32 *)r2;
    r1 += r0;
    r5 = 0x3FFF;
    r1 &= r5;
    *(u32 *)r2 = r1;
    r6 = 0x03005FC4;
    r0 = 0x2A28;
    *(u32 *)r6 = r0;
    if (r3 == 0x1E) {
        r0 = 0x600;
        *(u32 *)r2 = r0;
        r0 = 0x2C80;
        *(u32 *)r6 = r0;
    }
    if (r3 == 0x1F) {
        r0 = 0x2600;
        *(u32 *)r2 = r0;
        r0 = 0x2C80;
        *(u32 *)r6 = r0;
    }
    if (r3 == 0x20) {
        r0 = 0x1800;
        *(u32 *)r2 = r0;
        r0 = 0x27D0;
        *(u32 *)r6 = r0;
    }
    if (r3 == 0x21) {
        r0 = 0x1000;
        *(u32 *)r2 = r0;
        r0 = 0x2C80;
        *(u32 *)r6 = r0;
    }
    r0 = *(u32 *)r2;
    r0 &= r5;
    r4 = 0x03002E40;
    r1 = *(u32 *)(r4 + 4);
    r1 &= r5;
    r0 = func_08014614(r0, r1);
    r1 = r0;
    r7 = 0x1FFF;
    if ((s32)r1 > (s32)r7) {
        r0 = 0xFFFFC000;
        r1 += r0;
    }
    r1 = (s32)r1 >> 2;
    r0 = *(u32 *)(r4 + 4);
    r0 -= r1;
    r0 &= r5;
    *(u32 *)(r4 + 4) = r0;
    r0 = *(u32 *)r6;
    r0 &= r5;
    r1 = *(u32 *)(r4 + 8);
    r1 &= r5;
    r0 = func_08014614(r0, r1);
    r1 = r0;
    if ((s32)r1 > (s32)r7) {
        r0 = 0xFFFFC000;
        r1 += r0;
    }
    r1 = (s32)r1 >> 2;
    r0 = *(u32 *)(r4 + 8);
    r0 -= r1;
    r0 &= r5;
    *(u32 *)(r4 + 8) = r0;
}

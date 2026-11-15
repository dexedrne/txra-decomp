/* Matched automatically; the address name is kept until reviewed. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
void func_08009D38(void) {
    u32 r0;
    u32 r1;
    u32 r2;
    u32 r4;
    u32 r5;
    vu8 *r3;

    r0 = 0x03002190;
    r5 = 0;
    r1 = 0xFC;
    *(vu8 *)r0 = (u8)r1;
    r1 = *(u32 *)0x030066D4;
    *(vu8 *)(r0 + 1) = (u8)r1;
    r2 = 0x03000A70;
    *(vu32 *)(r0 + 4) = r2;
    r1 = 1;
    *(vu8 *)(r0 + 8) = (u8)r1;
    *(vu8 *)(r0 + 9) = (u8)r1;
    r3 = (vu8 *)0x03005790;
    r1 = *r3;
    r1 += 0x30;
    *(vu8 *)r2 = (u8)r1;
    r1 = *(r3 + 1);
    r1 += 0x30;
    *(vu8 *)(r2 + 1) = (u8)r1;
    r4 = 0x2E;
    *(vu8 *)(r2 + 2) = (u8)r4;
    r1 = *(r3 + 2);
    r1 += 0x30;
    *(vu8 *)(r2 + 3) = (u8)r1;
    r1 = *(r3 + 3);
    r1 += 0x30;
    *(vu8 *)(r2 + 4) = (u8)r1;
    *(vu8 *)(r2 + 5) = (u8)r4;
    r1 = *(r3 + 4);
    r1 += 0x30;
    *(vu8 *)(r2 + 6) = (u8)r1;
    *(vu8 *)(r2 + 7) = (u8)r5;
    func_080154AC(r0);
}

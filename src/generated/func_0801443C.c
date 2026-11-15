/* Matched automatically; the address name is kept until reviewed. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
u32 func_0801443C(u32 r0, u32 r1, u32 r2) {
    u32 r3;
    u32 r0_local;
    u32 r2_local;

    r3 = 0x040000D4;
    *(vu32 *)r3 = r1;
    *(vu32 *)(r3 + 4) = r0;

    r0_local = r2 >> 31;
    r2_local = r2 + r0_local;
    r2_local = (s32)r2_local >> 1;

    r0_local = 0x80;
    r0_local = r0_local << 24;
    r2_local |= r0_local;

    *(vu32 *)(r3 + 8) = r2_local;

    return *(vu32 *)(r3 + 8);
}

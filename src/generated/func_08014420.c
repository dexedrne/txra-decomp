/* Matched automatically; the address name is kept until reviewed. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
u32 func_08014420(u32 r0, u32 r1, u32 r2) {
    u32 r3;
    u32 r0_local;
    u32 r2_local;
    u32 r0_shifted;

    r3 = 0x040000D4;
    *(vu32 *)r3 = r0;
    *(vu32 *)(r3 + 4) = r1;

    r0_shifted = r2 >> 31;
    r2_local = r2 + r0_shifted;
    r2_local = (s32)r2_local >> 1;

    r0_local = 0x80000000;
    r2_local |= r0_local;

    *(vu32 *)(r3 + 8) = r2_local;
    
    return *(vu32 *)(r3 + 8);
}

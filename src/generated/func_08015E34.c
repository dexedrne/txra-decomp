/* Matched automatically; the address name is kept until reviewed. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
void func_08015E34(void) {
    u32 r0;
    s32 r1;
    u32 r2;
    s32 r3;
    r1 = 0;
    r3 = 0x1FF;
    r2 = 0xC0;
    r0 = 0x03005B40;
    do {
        *(vu16 *)r0 = (vu16)r2;
        r0 += 8;
        r1 += 4;
    } while ((s32)r1 <= (s32)r3);
}

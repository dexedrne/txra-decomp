/* Matched automatically; the address name is kept until reviewed. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
void func_080141EC(u32 r0)
{
    u32 r1;
    u32 r2;
    u32 r3;
    if (r0 != 0) {
        return;
    }
    r1 = 0x030021E0;
    r2 = 0;
    r3 = 159;
    r3 <<= 1;
    r0 = r1 + r3;
    do {
        *(vu16 *)r0 = (u16)r2;
        r0 -= 2;
    } while ((s32)r0 >= (s32)r1);
}

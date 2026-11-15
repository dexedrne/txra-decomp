/* Matched automatically; the address name is kept until reviewed. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
void func_08014408(void)
{
    u32 r0;
    u32 *r1;
    r1 = (u32 *)0x03005F5C;
    r0 = *(vu16 *)0x03005F5C;
    r0 -= 1;
    *(vu16 *)0x03005F5C = (u16)r0;
    r0 <<= 16;
    if ((s32)r0 < 0) {
        r0 = 0;
        *(vu16 *)0x03005F5C = (u16)r0;
    }
}

/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
extern u32 g_03005FC0;
void func_080161E8(void)
{
    if (g_03005FC0 == 0) *(vu16 *)0x04000000 = 0x1444;
    else *(vu16 *)0x04000000 = 0x1454;
}

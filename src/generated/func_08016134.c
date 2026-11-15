/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
extern u32 g_03005FC0;
extern void func_080160C4(u32, u32, u32, u32, u32);
void func_08016134(u32 source)
{
    if (g_03005FC0 == 0) func_080160C4(3, source, 0x0600A000, 0x9600, 32);
    else func_080160C4(3, source, 0x06000000, 0x9600, 32);
}

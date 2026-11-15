/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
extern u8 g_03002E30[];
extern s16 g_03005F5C;
extern u32 g_030014B4;
void func_080143CC(void)
{
    g_03002E30[g_03005F5C] = g_030014B4;
    g_03005F5C++;
    if (g_03005F5C > 15) g_03005F5C = 15;
    g_03002E30[g_03005F5C] = 0;
}

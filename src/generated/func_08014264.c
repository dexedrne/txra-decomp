/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
extern u8 g_03000B60[];
extern u32 g_03000B58, g_03000AC8, g_03005FD4;
void func_08014264(u32 slot)
{
    if (slot == 0) g_03000B60[g_03000B58 * 32] = 0;
    if (slot == 1) g_03000B60[g_03000AC8 * 32] = 0;
    if (slot == 2) g_03000B60[g_03005FD4 * 32] = 0;
}

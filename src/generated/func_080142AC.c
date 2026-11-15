/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
extern u8 g_03000B60[];
extern u32 g_03000B58, g_03000AC8, g_03005FD4;
void func_080142AC(u32 slot)
{
    u8 *source = g_03000B60;
    u8 *dest;
    u32 i;
    u8 t;
    if (slot == 0) dest = source + g_03000B58 * 32;
    if (slot == 1) dest = source + g_03000AC8 * 32;
    if (slot == 2) dest = source + g_03005FD4 * 32;
    for (i = 0; i <= 31; i++) {
        t = *source;
        *source = *dest;
        *dest = t;
        dest++;
        source++;
    }
}

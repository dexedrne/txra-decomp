/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
extern u8 g_03005FE0[];
extern u32 func_08005E84(void);
u32 func_08014208(void)
{
    u32 result = 0;
    s32 i;
    if (func_08005E84() != 0) return 0;
    if (g_03005FE0[0] == 0x54 && g_03005FE0[1] == 0x58 && g_03005FE0[2] == 0x52 && g_03005FE0[3] == 0x43) {
        i = 5;
        do { i++; } while (i <= 4095);
        result = 1;
    }
    return result;
}

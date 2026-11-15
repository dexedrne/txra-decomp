/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
extern u8 g_0202B7C0[];
extern s32 g_03001B20, g_03005FCC;
extern u32 g_03005FC0;
extern void func_080160C4(u32, void *, u32, u32, u32);
void func_08016174(void)
{
    u8 *source = g_0202B7C0;
    s32 length;
    if (g_03001B20 != 0) length = g_03001B20 & 63;
    else length = g_03005FCC;
    if (length > 55) length = 55;
    if (g_03005FC0 == 0) func_080160C4(3, source, 0x0600BB30, (length + 81) * 240, 32);
    else func_080160C4(3, source, 0x06001B30, (length + 81) * 240, 32);
}

/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
extern u16 g_0827A384[];
extern u32 g_03005F48;
extern s32 g_03001E54;
void func_08015CBC(void)
{
    u16 *table = g_0827A384;
    s32 i = 0;
    u16 value = *table;
    goto check;
again:
    g_03005F48 = 0x6C6C;
    i++;
    if (i > 191) return;
    value = *(u16 *)(i * 2 + (u32)table);
check:
    if (value != 0) goto again;
    g_03001E54 = i;
}

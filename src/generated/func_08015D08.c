/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
extern u8 g_03002A30[], g_03000BE0[];
extern u32 g_0300667C, g_03002184;
extern void func_08015DA8(void), func_080064A4(void);
void func_08015D08(void)
{
    vu32 *dma = (vu32 *)0x040000D4;
    dma[0] = (u32)g_03002A30;
    dma[1] = 0x05000000;
    dma[2] = 0x84000080;
    dma[2];
    dma[0] = (u32)g_03000BE0;
    dma[1] = 0x05000200;
    dma[2] = 0x84000080;
    dma[2];
    if (g_0300667C != 0) { func_08015DA8(); g_0300667C = 0; }
    if (g_03002184 == 0) func_080064A4();
}

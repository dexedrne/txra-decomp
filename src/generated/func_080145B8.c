/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
extern s16 g_03005788;
extern u8 g_0828B2E8[], g_03002A30[];
extern void func_0800A8A0(u32, void *, void *, u32, u32);
void func_080145B8(void)
{
    if (g_03005788 == 0) {
        vu32 *dma = (vu32 *)0x040000D4;
        dma[0] = (u32)g_0828B2E8;
        dma[1] = (u32)g_03002A30;
        dma[2] = 0x84000080;
        dma[2];
    } else {
        func_0800A8A0(3, g_0828B2E8, g_03002A30, 512, 32);
        g_03005788--;
    }
}

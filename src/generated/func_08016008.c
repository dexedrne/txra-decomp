/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
extern u8 g_08269B84[];
extern void func_080160C4(u32, void *, u32, u32, u32);
void func_08016008(void)
{
    vu32 *dma;
    u32 zero;
    func_080160C4(3, g_08269B84, 0x0600A000, 0x8700, 32);
    zero = 0;
    dma = (vu32 *)0x040000D4;
    dma[0] = (u32)&zero;
    dma[1] = 0x06012700;
    dma[2] = 0x850003C0;
    dma[2];
}

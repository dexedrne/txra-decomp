/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
extern s16 g_03005788;
extern u8 g_0831C89C[],g_03002A30[],g_08321BDC[],g_082B3D9C[];
extern void func_0800A8A0(u32,void *,void *,s32,u32);
void func_08013DB4(void)
{
    if (!g_03005788) {
        vu32 *dma=(vu32 *)0x040000D4;
        u8 *dest;
        dma[0]=(u32)g_0831C89C;
        dest=g_03002A30;
        dma[1]=(u32)dest;
        dma[2]=0x84000080;
        dma[2];
        dma[0]=(u32)g_08321BDC;
        dma[1]=(u32)(dest+320);
        dma[2]=0x84000020;
        dma[2];
        dma[0]=(u32)g_082B3D9C;
        dma[1]=(u32)(dest+464);
        dma[2]=0x8400000c;
        dma[2];
    } else {
        func_0800A8A0(3,g_0831C89C,g_03002A30,512,32);
        func_0800A8A0(3,g_08321BDC,g_03002A30+320,128,32);
        func_0800A8A0(3,g_082B3D9C,g_03002A30+464,48,32);
        g_03005788--;
    }
}

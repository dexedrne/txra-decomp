extern u32 g_030014A8, g_03002188, g_030061E4, g_030067E4, g_030061F0, g_03001B24, g_03000DF0, g_03006680, g_03005FC0;
extern u32 g_03002E58, g_030066D4, g_03001B18;
extern s16 g_03005788;
extern u16 g_0300218C;
extern u16 g_030021E0[];
extern u8 g_03002A30[], g_03000BE0[], g_0802581C[], g_08025864[], g_08323C5C[];
extern void func_08005EE0(void), func_08015E20(void), func_08015E34(void), func_08018E84(void);
extern void func_08015200(void), func_08015D78(void), func_080161E8(void), func_08014524(void);
extern void func_08016134(u32), func_080154AC(u8 *), func_0801251C(u8 *, u32, u32), func_0801604C(u32, u32);
#define DMA_CLEAR(dest) { vu32 *dma = (vu32 *)0x040000D4; zero = 0; dma[0] = (u32)&zero; dma[1] = (u32)(dest); dma[2] = 0x85000080; dma[2]; }
void func_08012CC8(void)
{
    vu32 zero;
    s32 i;
    func_08005EE0();
    g_030014A8 = 0;
    for (i = 159; i >= 0; i--) g_030021E0[i] = 0;
    DMA_CLEAR(g_03002A30);
    DMA_CLEAR(g_03000BE0);
    func_08015E20();
    func_08015E20();
    *(vu16 *)0x04000000 = 0;
    *(vu16 *)0x0400000C = 0xC083;
    func_08018E84();
    g_030014A8 = 0;
    DMA_CLEAR(g_03002A30);
    DMA_CLEAR(g_03000BE0);
    func_08015E20();
    func_08015E34();
    g_03002188 = 0;
    g_030061E4 = 64;
    g_030067E4 = 0;
    g_030061F0 = 0;
    g_03001B24 = 0;
    g_03000DF0 = 0;
    g_03006680 = 0;
    g_03005FC0 = 0;
    func_08015200();
    g_03005788 = 31;
    i = 0;
    for (;;) {
        func_08015D78();
        func_08015E20();
        func_080161E8();
        func_08014524();
        func_08016134(0x02000000);
        g_03002E58 = 0;
        g_030066D4 = 36;
        g_03001B18 = 2;
        func_080154AC(g_0802581C);
        g_03002E58 = 0;
        g_030066D4 = 120;
        g_03001B18 = 0;
        func_080154AC(g_08025864);
        if (i == 0) func_0801251C(g_08323C5C, 0x02000000, 0x9600);
        if (g_03005788 == 0 && ((g_0300218C & 1) || (g_0300218C & 8))) break;
        g_03005FC0 = (g_03005FC0 + 1) & 1;
        if (++i > 255) i = 64;
    }
    func_0801604C(2, 1);
    DMA_CLEAR(g_03002A30);
    DMA_CLEAR(g_03000BE0);
    func_08015E20();
}

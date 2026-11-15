/* Unmatched deep-j draft (273 normalized lines: loop-invariant choices); excluded from the ROM build. */
extern u32 g_030001C4, g_030014A8, g_03002188, g_030061E4, g_030067E4, g_030061F0, g_03001B24, g_03000DF0, g_03006680, g_03005FC0;
extern u32 g_03005F50, g_03000B50, g_03000DE0, g_030021C4, g_03000DFC;
extern s16 g_030014B0;
extern u16 g_0300218C, g_030014BC;
extern u16 g_030021E0[];
extern u8 g_03002A30[], g_03000BE0[], g_03002DB0[], g_03002C00[], g_03000B60[];
extern u8 g_0827A584[], g_082C770C[], g_0827A384[], g_082B3D9C[];
extern TxraRecord g_03001E60[];
extern TxraTriple g_03002320, g_03005F70, g_03002E40;
extern void func_08015CBC(void), func_08005EE0(void), func_08015E20(void), func_08015E34(void), func_08018E84(void);
extern void func_08015200(void), func_08015D78(void), func_08016264(void), func_08005EF8(void), func_080085E0(void);
extern void func_08016134(u32), func_08002778(u32);
extern void func_080086C0(u32, s32), func_08008780(u32, s32), func_0800D2F4(u32, s32), func_08008838(u32, s32);
#define DMA_SET(src, dest, cnt) { vu32 *dma = (vu32 *)0x040000D4; dma[0] = (u32)(src); dma[1] = (u32)(dest); dma[2] = (u32)(cnt); dma[2]; }
#define DMA_CLEAR(dest) { vu32 tmp = 0; DMA_SET(&tmp, dest, 0x85000080); }
void func_0800B4D8(void)
{
    s32 j;
    s32 slot;
    func_08015CBC();
    g_030001C4 = 60;
    { vu32 tmp = 0; DMA_SET(&tmp, 0x02000000, 0x85010000); }
    g_030014A8 = 0;
    DMA_CLEAR(g_03002A30);
    DMA_CLEAR(g_03000BE0);
    func_08015E20();
    func_08015E20();
    *(vu16 *)0x04000000 = 0;
    *(vu16 *)0x0400000C = 0xC083;
    *(vu16 *)0x04000050 = 0x1641;
    *(vu16 *)0x04000052 = 0x0808;
    *(vu16 *)0x04000054 = 1;
    func_08018E84();
    g_030014A8 = 0;
    DMA_CLEAR(g_03002A30);
    DMA_CLEAR(g_03000BE0);
    func_08015E20();
    for (j = 0; j < 160; j++) g_030021E0[j] = 0;
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
    g_03005F50 = 0;
    for (j = 0; j <= 7; j++) g_03001E60[j].field_00 = 0;
    func_08005EE0();
    g_030014B0 = 0;
    g_03001E60[0].field_00 = 1;
    g_03001E60[0].field_04 = 0;
    g_03001E60[0].field_08 = 0;
    g_03001E60[0].field_0c = 0;
    g_03001E60[0].field_34 = 0;
    g_03001E60[0].field_20 = 0;
    g_03001E60[0].field_24 = 0;
    g_03001E60[0].field_38 = 0;
    g_03001E60[0].field_02 = 15;
    g_03002320.field_00 = 0;
    g_03002320.field_04 = 0;
    g_03002320.field_08 = 800;
    g_03005F70.field_00 = 0;
    g_03005F70.field_04 = 128;
    g_03005F70.field_08 = 0;
    g_03002E40.field_08 = 0x2DAC;
    g_03002E40.field_04 = 0x2000;
    DMA_SET(g_0827A584, g_03000BE0, 0x84000050);
    DMA_SET(g_082C770C, g_03000BE0 + 320, 0x8400001C);
    g_03000B50 = 0;
    while (1) {
        func_08015D78();
        func_08015E20();
        DMA_SET(g_0827A384, g_03002A30, 0x84000050);
        DMA_SET(g_03002DB0, g_03002A30 + 384, 0x84000014);
        DMA_SET(g_082B3D9C, g_03002C00, 0x8400000C);
        func_08015E34();
        g_03002188 = 0;
        g_030061E4 = 368;
        g_030067E4 = 0;
        g_030061F0 = 0;
        g_03001B24 = 0;
        g_03000DF0 = 0;
        g_03006680 = 0;
        g_03000DE0 = 0;
        func_08016264();
        func_08015200();
        if (g_03005FC0 == 0) *(vu16 *)0x04000000 = 0x1444;
        else *(vu16 *)0x04000000 = 0x1454;
        func_08016134(0x02010000);
        g_030021C4 = 0x02019EF0;
        func_08002778(1);
        g_03000DFC = g_03005FC0 == 0 ? 0x0600A000 : 0x06000000;
        func_08005EF8();
        if (g_030014BC & 32) g_03002E40.field_04 = (g_03002E40.field_04 - 64) & 0x3FFF;
        if (g_030014BC & 16) g_03002E40.field_04 = (g_03002E40.field_04 + 64) & 0x3FFF;
        if (g_030014BC & 64) g_03005F70.field_04--;
        if (g_030014BC & 128) g_03005F70.field_04++;
        if (g_030014BC & 512) g_03002320.field_08 -= 8;
        if (g_030014BC & 256) g_03002320.field_08 += 8;
        if (g_0300218C & 1) {
            g_03001E60[0].field_02 = (g_03001E60[0].field_02 + 1) & 31;
            func_080085E0();
            slot = g_03001E60[0].field_02 - 16;
            func_080086C0(slot, g_03000B60[21] - 1);
            func_08008780(slot, g_03000B60[22] - 1);
            func_0800D2F4(slot, g_03000B60[24] - 1);
            func_08008838(slot, g_03000B60[19] - 1);
        }
        if (g_0300218C & 2) {
            g_03001E60[0].field_02 = (g_03001E60[0].field_02 - 1) & 31;
            func_080085E0();
            slot = g_03001E60[0].field_02 - 16;
            func_080086C0(slot, g_03000B60[21] - 1);
            func_08008780(slot, g_03000B60[22] - 1);
            func_0800D2F4(slot, g_03000B60[24] - 1);
            func_08008838(slot, g_03000B60[19] - 1);
        }
        if (g_0300218C & 8) break;
        g_03005FC0 = (g_03005FC0 + 1) & 1;
    }
}

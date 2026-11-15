/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern u32 g_030014A8, g_03002188, g_030061E4, g_030067E4, g_030061F0, g_03001B24, g_03000DF0, g_03006680, g_03005FC0;
extern u32 g_03002E58, g_030066D4, g_03001B18, g_030014A4;
extern s32 g_030014B4;
extern s16 g_03005788, g_03006684;
extern u16 g_0300218C;
extern u16 g_030021E0[], g_030001E0[];
extern u8 g_03002A30[], g_03000BE0[], g_03000DE8[], g_080258AC[], g_0828FD84[], g_0828B4E8[];
extern void func_08005EE0(void), func_08015E20(void), func_08015E34(void), func_08018E84(void);
extern void func_08015200(void), func_08015D78(void), func_080161E8(void), func_08013CF4(void), func_0800418C(void);
extern void func_08014458(void), func_08014104(void);
extern void func_08016134(u32), func_080154AC(u8 *), func_0801251C(u8 *, u32, u32), func_0801604C(u32, u32);
extern void func_080160C4(u32, u32, u32, u32, u32);
#define DMA_SET(src, dest, cnt) { vu32 *dma = (vu32 *)0x040000D4; dma[0] = (u32)(src); dma[1] = (u32)(dest); dma[2] = (u32)(cnt); dma[2]; }
#define DMA_CLEAR(dest) { vu32 tmp = 0; DMA_SET(&tmp, dest, 0x85000080); }
void func_080130BC(void)
{
    s32 i;
    s32 j;
    func_08005EE0();
    g_030014A8 = 0;
    for (j = 0; j < 160; j++) g_030021E0[j] = 0;
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
    for (j = 0; j <= 7; j++) g_03000DE8[j] = 32;
    g_03000DE8[8] = 0;
    g_030014B4 = 0;
    g_03006684 = 0;
    i = 0;
    while (1) {
        func_08015D78();
        func_08015E20();
        func_080161E8();
        func_08013CF4();
        func_08015E34();
        g_03002188 = 0;
        g_030061E4 = 64;
        g_030067E4 = 0;
        g_030061F0 = 0;
        g_03001B24 = 0;
        g_03000DF0 = 0;
        g_03006680 = 0;
        func_0800418C();
        func_08015200();
        func_08016134(0x02000000);
        g_03002E58 = 0;
        g_030066D4 = 36;
        g_03001B18 = 2;
        func_080154AC(g_080258AC);
        func_08014458();
        if (i == 0) {
            func_0801251C(g_0828FD84, 0x02009600, 0x9600);
            func_080160C4(3, 0x02009600, 0x02000000, 0x9600, 32);
            func_0801251C(g_0828B4E8, 0x02009600, 0xF5A0);
            func_080160C4(3, 0x02009600, 0x02000000, 0x1B30, 32);
            func_08014104();
        }
        if (g_03005788 == 0) {
            if (g_0300218C & 32) {
                g_030014B4--;
                if (g_030014B4 == 25) g_030014B4 = 38;
                if (g_030014B4 == 12) g_030014B4 = 25;
                if (g_030014B4 == -1) g_030014B4 = 12;
                func_0801604C(1, 1);
            }
            if (g_0300218C & 16) {
                g_030014B4++;
                if (g_030014B4 == 13) g_030014B4 = 0;
                if (g_030014B4 == 26) g_030014B4 = 13;
                if (g_030014B4 == 39) g_030014B4 = 26;
                func_0801604C(1, 1);
            }
            if (g_0300218C & 64) {
                g_030014B4 -= 13;
                if (g_030014B4 < 0) g_030014B4 += 39;
                func_0801604C(1, 1);
            }
            if (g_0300218C & 128) {
                g_030014B4 += 13;
                if (g_030014B4 > 38) g_030014B4 -= 39;
                func_0801604C(1, 1);
            }
            if ((g_0300218C & 1) || (g_0300218C & 8)) {
                func_0801604C(2, 1);
                if (g_030014B4 >= 0 && g_030014B4 <= 12) {
                    g_03000DE8[g_03006684] = g_030014B4 + 65;
                    if (g_03006684 <= 4) g_03006684++;
                }
                if (g_030014B4 >= 13 && g_030014B4 <= 25) {
                    g_03000DE8[g_03006684] = g_030014B4 + 65;
                    if (g_03006684 <= 4) g_03006684++;
                }
                if (g_030014B4 >= 26 && g_030014B4 <= 35) {
                    g_03000DE8[g_03006684] = g_030014B4 + 22;
                    if (g_03006684 <= 4) g_03006684++;
                }
                if (g_030014B4 == 36) {
                    g_03000DE8[g_03006684] = 32;
                    if (g_03006684 <= 4) g_03006684++;
                }
                if (g_030014B4 == 37) {
                    if (g_03006684 == 5) {
                        if (g_03000DE8[g_03006684] != 32) g_03000DE8[g_03006684] = 32;
                        else g_03006684--;
                    } else {
                        g_03000DE8[g_03006684] = 32;
                        if (g_03006684 > 0) g_03006684--;
                    }
                }
                if (g_030014B4 == 38) break;
            }
        }
        g_03005FC0 = (g_03005FC0 + 1) & 1;
        if (++i > 255) i = 64;
    }
    i = 0;
    for (j = 0; j <= 5; j++) if (g_03000DE8[j] != 32) i++;
    if (i == 0) {
        g_03000DE8[0] = 'P'; g_03000DE8[1] = 'L'; g_03000DE8[2] = 'A';
        g_03000DE8[3] = 'Y'; g_03000DE8[4] = 'E'; g_03000DE8[5] = 'R';
    }
    if (g_03000DE8[0] == 'N' && g_03000DE8[1] == 'I' && g_03000DE8[2] == 'G' &&
        g_03000DE8[3] == 'S' && g_03000DE8[4] == 'P' && g_03000DE8[5] == '8')
        for (j = 0; j <= 5; j++) g_030001E0[j] = 1;
    if (g_03000DE8[0] == 'J' && g_03000DE8[1] == 'O' && g_03000DE8[2] == 'N' &&
        g_03000DE8[3] == 'S' && g_03000DE8[4] == 'A' && g_03000DE8[5] == 'U')
        g_030014A4 = 250000;
    DMA_CLEAR(g_03002A30);
    DMA_CLEAR(g_03000BE0);
    func_08015E20();
}

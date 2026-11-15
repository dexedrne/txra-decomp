/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern u32 g_030014A8, g_03002188, g_030061E4, g_030067E4, g_030061F0, g_03001B24, g_03000DF0, g_03006680, g_03005FC0;
extern s32 g_03002E58;
extern u32 g_030066D4, g_03001B18, g_03001B1C, g_03006870;
extern s32 g_030014B4;
extern s16 g_03005788;
extern u16 g_0300218C;
extern u16 g_030021E0[];
extern u8 g_03002A30[], g_03000BE0[], g_0828FD84[], g_0828B4E8[];
extern u8 g_080258F4[], g_080259CC[], g_08025A14[], g_08025A5C[], g_08025CE4[], g_08025D2C[], g_0802593C[], g_08025984[];
extern void func_08005EE0(void), func_08015E20(void), func_08015E34(void), func_08018E84(void);
extern void func_08015200(void), func_08015D78(void), func_080161E8(void), func_08013CF4(void);
extern void func_08016134(u32), func_080154AC(u8 *), func_0801251C(u8 *, u32, u32), func_0801604C(u32, u32);
extern void func_080160C4(u32, u32, u32, u32, u32), func_08016078(u32);
extern s32 func_08013B38(void), func_08013C08(void);
#define DMA_SET(src, dest, cnt) { vu32 *dma = (vu32 *)0x040000D4; dma[0] = (u32)(src); dma[1] = (u32)(dest); dma[2] = (u32)(cnt); dma[2]; }
#define DMA_CLEAR(dest) { vu32 tmp = 0; DMA_SET(&tmp, dest, 0x85000080); }
#define TEXT(x, y, attr, s) { g_03002E58 = (x); g_030066D4 = (y); g_03001B18 = (attr); func_080154AC(s); }
s32 func_08013594(s32 mode)
{
    s32 i;
    s32 j;
    s32 next;
    s32 result;
    next = mode;
    func_08016078(0);
restart:
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
    g_030014B4 = 0;
    i = 0;
    do {
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
        func_08015200();
        func_08016134(0x02000000);
        switch (mode) {
        case 0:
            TEXT(0, 64, 2, g_080258F4);
            if (g_030014B4 != 0 || (g_03001B1C & 15) <= 7) TEXT(-32, 96, 0, g_0802593C);
            if (g_030014B4 != 1 || (g_03001B1C & 15) <= 7) TEXT(32, 96, 0, g_08025984);
            break;
        case 1:
            TEXT(0, 64, 2, g_080259CC);
            break;
        case 8:
            TEXT(0, 64, 2, g_08025CE4);
            break;
        case 9:
            TEXT(0, 64, 2, g_08025D2C);
            break;
        case 2:
            TEXT(0, 64, 2, g_08025A14);
            if (g_030014B4 != 0 || (g_03001B1C & 15) <= 7) TEXT(-32, 96, 0, g_0802593C);
            if (g_030014B4 != 1 || (g_03001B1C & 15) <= 7) TEXT(32, 96, 0, g_08025984);
            break;
        case 3:
            TEXT(0, 64, 2, g_08025A5C);
            break;
        }
        if (i == 0) {
            func_0801251C(g_0828FD84, 0x02009600, 0x9600);
            func_080160C4(3, 0x02009600, 0x02000000, 0x9600, 32);
            func_0801251C(g_0828B4E8, 0x02009600, 0xF5A0);
            func_080160C4(3, 0x02009600, 0x02000000, 0x1B30, 32);
        }
        if (g_03005788 == 0) {
            switch (mode) {
            case 0:
                if (g_0300218C & 32) {
                    if (g_030014B4 != 0) g_030014B4--;
                    func_0801604C(1, 1);
                }
                if (g_0300218C & 16) {
                    if (g_030014B4 != 1) g_030014B4++;
                    func_0801604C(1, 1);
                }
                if (g_0300218C & 1) {
                    if (g_030014B4 == 0) next = 1;
                    if (g_030014B4 == 1) next = 6;
                    func_0801604C(2, 1);
                }
                break;
            case 1:
                if (i == 118) {
                    result = func_08013B38();
                    if (g_03006870 == 0) func_08016078(0);
                    if (result) next = 8;
                }
                if (i == 120) next = 4;
                break;
            case 8:
                if (i > 64) next = 6;
                break;
            case 9:
                if (i > 64) next = 7;
                break;
            case 2:
                if (g_0300218C & 32) {
                    if (g_030014B4 != 0) g_030014B4--;
                    func_0801604C(1, 1);
                }
                if (g_0300218C & 16) {
                    if (g_030014B4 != 1) g_030014B4++;
                    func_0801604C(1, 1);
                }
                if (g_0300218C & 1) {
                    if (g_030014B4 == 0) next = 3;
                    if (g_030014B4 == 1) next = 7;
                    func_0801604C(2, 1);
                }
                break;
            case 3:
                if (i == 118) {
                    result = func_08013C08();
                    if (result) next = 9;
                }
                if (i == 120) next = 5;
                break;
            }
        }
        g_03005FC0 = (g_03005FC0 + 1) & 1;
        if (++i > 255) i = 64;
    } while (mode == next);
    if (next == 1) { mode = 1; goto restart; }
    if (next == 3) { mode = 3; goto restart; }
    if (next == 8) { mode = 8; goto restart; }
    if (next == 9) { mode = 9; goto restart; }
    DMA_CLEAR(g_03002A30);
    DMA_CLEAR(g_03000BE0);
    func_08015E20();
    func_08016078(2);
    return next;
}

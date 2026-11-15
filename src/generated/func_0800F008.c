/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern u32 g_030014A8, g_03002188, g_030061E4, g_030067E4, g_030061F0, g_03001B24, g_03000DF0, g_03006680, g_03005FC0;
extern u16 g_0300218C;
extern u16 g_030021E0[];
extern u8 g_03002A30[], g_03000BE0[];
extern u8 g_0827C110[], g_0827A984[], g_082825D0[], g_0827C310[], g_08283C6C[], g_082827D0[];
extern void func_08015E20(void), func_08015E34(void), func_08018E84(void);
extern void func_08015200(void), func_08015D78(void), func_080161E8(void);
extern void func_08016134(u32), func_0801251C(u8 *, u32, u32), func_08016210(u32, u32, u32, u32, u32);
#define DMA_SET(src, dest, cnt) { vu32 *dma = (vu32 *)0x040000D4; dma[0] = (u32)(src); dma[1] = (u32)(dest); dma[2] = (u32)(cnt); dma[2]; }
#define DMA_CLEAR(dest) { vu32 tmp = 0; DMA_SET(&tmp, dest, 0x85000080); }
#define DMA_COPY(src, dest) DMA_SET(src, dest, 0x84000080)
s32 func_0800F008(s32 scene)
{
    s32 i, j, state;
    g_030014A8 = 0;
    DMA_CLEAR(g_03002A30);
    DMA_CLEAR(g_03000BE0);
    func_08015E20();
    func_08016210(3, 0x02000000, 0x9600, 0x200, 32);
    func_08016210(3, 0x06000000, 0x9600, 0x200, 32);
    func_08016210(3, 0x0600A000, 0x9600, 0x200, 32);
restart_video:
    func_08015E20();
    *(vu16 *)0x04000000 = 0;
    *(vu16 *)0x0400000C = 0xC083;
    func_08018E84();
restart:
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
    state = 0;
    i = 0;
    do {
        func_08015D78();
        func_08015E20();
        switch (scene) {
        case 0:
            if (i == 0) DMA_CLEAR(g_03002A30) else DMA_COPY(g_0827C110, g_03002A30);
            func_080161E8();
            if (i == 0) func_0801251C(g_0827A984, 0x02000000, 0x9600);
            func_08016134(0x02000000);
            g_03005FC0 = (g_03005FC0 + 1) & 1;
            break;
        case 1:
            if (i == 0) DMA_CLEAR(g_03002A30) else DMA_COPY(g_082825D0, g_03002A30);
            func_080161E8();
            if (i == 0) func_0801251C(g_0827C310, 0x02000000, 0x9600);
            func_08016134(0x02000000);
            g_03005FC0 = (g_03005FC0 + 1) & 1;
            break;
        case 2:
            if (i == 0) DMA_CLEAR(g_03002A30) else DMA_COPY(g_08283C6C, g_03002A30);
            func_080161E8();
            if (i == 0) func_0801251C(g_082827D0, 0x02000000, 0x9600);
            func_08016134(0x02000000);
            g_03005FC0 = (g_03005FC0 + 1) & 1;
            if ((g_0300218C & 8) || (g_0300218C & 1)) {
                if (i > 32) i = 240;
            }
            break;
        }
        if (i < 240) {
            i++;
        } else {
            switch (scene) {
            case 0: scene = 1; state = 1; break;
            case 1: scene = 2; state = 1; break;
            case 3: scene = 2; state = 1; break;
            case 2: state = 3; break;
            }
        }
        if (state == 1) goto restart_video;
        if (state == 2) goto restart;
    } while (state != 3);
    return scene;
}

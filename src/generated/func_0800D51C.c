/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
/* Garage/shop screen loop. Sets up the screen, then runs the menu: cursor
 * movement, confirm/cancel per screen type, and the screen-change dispatch.
 * The mapped entries 0800D570, 0800D630 and 0800D960 are the reload and
 * restart labels and a loop-exit block that loop.c moved next to the jump
 * table; the far gotos back to them are the BL instructions in the ROM.
 * The record-zeroing lines are chained assignments (outer address first). */
typedef struct {
    u16 type, count;
    u8 unknown_04[10];
    u16 back_action, back_screen;
    u16 next[5];
    u16 action[6];
    u8 *text;
} Screen;
typedef struct { u8 unknown_00[2]; u8 model; u8 unknown_03[22]; u8 colour; u8 unknown_1a[6]; } CarEntry;
extern Screen g_08175B04[];
extern TxraRecord g_03001E60[];
extern TxraTriple g_03002320, g_03005F70, g_03002E40;
extern CarEntry g_03000B60[];
extern s16 g_080200E4[][16];
extern u8 g_03002E30[];
extern s16 g_030001E0[];
extern s32 g_03000010, g_030001C4, g_030014A8, g_03005FCC, g_03001B20, g_030001CC, g_03005FC0;
extern s32 g_03002188, g_030061E4, g_030067E4, g_030061F0, g_03001B24, g_03000DF0, g_03006680;
extern s32 g_03005784, g_03005FC4, g_030001C0, g_03002180, g_030014B4, g_030001B0, g_030021C4, g_03000DFC;
extern s32 g_03000B58, g_03000AC8, g_03005FD4, g_03000B50, g_03002E58, g_030066D4, g_03001B18;
extern s32 g_030014B8, g_03005F40, g_03000AC4;
extern s16 g_03005788, g_03005F60, g_030014B0, g_03005F5C, g_03001B14, g_03001E50;
extern u16 g_0300218C;
extern void func_08015E20(void), func_08015E34(void), func_08018E84(void), func_08015200(void);
extern void func_08005EE0(void), func_080141EC(s32), func_0801251C(u32, u32, u32);
extern s32 func_0801418C(s32, s32);
extern void func_0800EDF4(s32, s32), func_080085E0(void), func_08014394(void), func_08012600(s32);
extern void func_08015D78(void), func_08005238(s32), func_080145B8(void), func_080161E8(void);
extern void func_08016134(u32), func_08013FAC(s32), func_08016174(void), func_08016264(void);
extern void func_08002500(s32), func_08005EF8(void), func_08015250(s32), func_080154AC(u8 *);
extern void func_0800F2D0(s32), func_0800ED28(s32), func_0801604C(s32, s32), func_080143CC(void);
extern void func_0800E498(s32), func_08014408(void), func_080130BC(void);
extern s32 func_08005C7C(void), func_08010A50(s32), func_08014208(void), func_08013594(s32);
extern void func_08016210(s32, s32, u32, s32, s32);

#define DMA_SET(src, dest, cnt) { vu32 *dma = (vu32 *)0x040000D4; dma[0] = (u32)(src); dma[1] = (u32)(dest); dma[2] = (u32)(cnt); dma[2]; }
#define DMA_CLEAR(dest) { vu32 tmp = 0; DMA_SET(&tmp, dest, 0x85000080); }
#define NOT_CANCEL(v) \
    v = 0; \
    switch (scr) { \
    case 11: case 17: case 18: \
    case 36: case 37: case 38: case 39: case 40: case 41: case 42: case 43: case 44: case 45: case 46: case 47: case 48: \
    case 75: case 76: case 77: case 101: case 102: case 103: case 127: case 128: case 129: \
        v = 1; \
    } \
    if (!v) { g_030001C0 = 0; g_03002180 = 0; }
#define DENIED(v, n) \
    if (g_030014B4 == 0 && (n <= 1 || g_030014B8 <= 0)) v = 1; \
    if (g_030014B4 == 1 && (n <= 1 || g_03005F40 <= 0)) v = 1; \
    if (g_030014B4 == 2 && (n <= 1 || g_03000AC4 <= 0)) v = 1;

s32 func_0800D51C(s32 scr)
{
    s32 v, n, i;
    g_03000010 = 0;
    g_030001C4 = 76;
    g_030014A8 = 0;
    DMA_CLEAR(0x03002A30)
    DMA_CLEAR(0x03000BE0)
    func_08015E20();
    g_03005FCC = 0;
    g_03001B20 = 0;
    g_030001CC = scr;
    g_03005788 = 31;
reload:
    func_08015E20();
    *(vu16 *)0x04000000 = 0;
    *(vu16 *)0x0400000C = 0xC083;
    func_08018E84();
    g_030014A8 = 0;
    DMA_CLEAR(0x03002A30)
    DMA_CLEAR(0x03000BE0)
    func_08015E20();
    func_080141EC(0);
    g_03005FC0 = 0;
    func_08015E34();
    g_03002188 = 0;
    g_030061E4 = 64;
    g_030067E4 = 0;
    g_030061F0 = 0;
    g_03001B24 = 0;
    g_03000DF0 = 0;
    g_03006680 = 0;
    func_08015200();
    g_03002320.field_00 = 0;
    g_03002320.field_04 = 0;
    g_03002320.field_08 = 1000;
    g_03005F70.field_00 = 0;
    g_03005F70.field_08 = 0;
    g_03005784 = g_03002E40.field_04 = 0;
    g_03005FC4 = g_03002E40.field_08 = 0x2A28;
    g_03001E60[7].field_04 = g_03001E60[0].field_04 = 0;
    g_03001E60[7].field_08 = g_03001E60[0].field_08 = 0;
    g_03001E60[7].field_0c = g_03001E60[0].field_0c = 0;
    g_03001E60[7].field_20 = g_03001E60[0].field_20 = 0;
    g_03001E60[7].field_24 = g_03001E60[0].field_24 = 0;
restart:
    if (g_08175B04[scr].type == 0) g_03005788 = 31;
    g_030001C0 = 0;
    g_03002180 = 0;
    scr = g_030001CC;
    g_03005FCC = 64;
    g_03001B20 = 0;
    g_03005F60 = 0;
    func_08005EE0();
    g_03000010 = 0;
    g_030014B4 = 0;
    func_0801251C(0x0828B4E8, 0x0201A6F0, 0xF5A0);
    func_0801251C(0x0828FD84, 0x02029C90, 0x9600);
    if (g_08175B04[scr].type == 0) func_0801251C(0x08283E6C, 0x0201A6F0, 0x9600);
    g_030014B0 = 0;
    g_030014B4 = g_03002E30[g_03005F5C];
    switch (scr) {
    case 36: case 46:
        g_030014B0 = 7;
        g_03001E60[7].field_02 = 16;
        break;
    case 37: case 47:
        g_030014B0 = 7;
        g_03001E60[7].field_02 = 22;
        break;
    case 38: case 48:
        g_030014B0 = 7;
        g_03001E60[7].field_02 = 27;
        break;
    case 39: case 42: case 75: case 101: case 127:
        g_030014B0 = 7;
        g_03000B58 = func_0801418C(0, 0);
        g_03001E60[7].field_02 = g_03000B60[g_03000B58].model;
        break;
    case 40: case 43: case 76: case 102: case 128:
        g_030014B0 = 7;
        g_03000AC8 = func_0801418C(1, 0);
        g_03001E60[7].field_02 = g_03000B60[g_03000AC8].model;
        break;
    case 41: case 44: case 77: case 103: case 129:
        g_030014B0 = 7;
        g_03005FD4 = func_0801418C(2, 0);
        g_03001E60[7].field_02 = g_03000B60[g_03005FD4].model;
        break;
    case 26: case 65: case 91: case 117: g_030014B4 = g_03000B60[0].unknown_03[11] - 1; break;
    case 27: case 66: case 92: case 118: g_030014B4 = g_03000B60[0].unknown_03[12] - 1; break;
    case 22: case 61: case 87: case 113: g_030014B4 = g_03000B60[0].unknown_03[13] - 1; break;
    case 23: case 62: case 88: case 114: g_030014B4 = g_03000B60[0].unknown_03[14] - 1; break;
    case 24: case 63: case 89: case 115: g_030014B4 = g_03000B60[0].unknown_03[15] - 1; break;
    case 25: case 64: case 90: case 116: g_030014B4 = g_03000B60[0].unknown_03[16] - 1; break;
    case 30: case 69: case 95: case 121: g_030014B4 = g_03000B60[0].unknown_03[18] - 1; break;
    case 31: case 70: case 96: case 122: g_030014B4 = g_03000B60[0].unknown_03[19] - 1; break;
    case 32: case 71: case 97: case 123: g_030014B4 = g_03000B60[0].unknown_03[20] - 1; break;
    case 33: case 72: case 98: case 124: g_030014B4 = g_03000B60[0].unknown_03[21] - 1; break;
    case 14: case 57: case 83: case 109: g_030014B4 = g_03000B60[0].unknown_03[17] - 1; break;
    case 7: case 52: case 78: case 104: g_030014B4 = 1; break;
    }
    v = -1;
    if (scr == 39 || scr == 42 || scr == 75 || scr == 101 || scr == 127) v = g_03000B58;
    if (scr == 40 || scr == 43 || scr == 76 || scr == 102 || scr == 128) v = g_03000AC8;
    if (scr == 41 || scr == 44 || scr == 77 || scr == 103 || scr == 129) v = g_03005FD4;
    if (scr >= 36 && scr <= 38) v = 99;
    if (v != -1) {
        if (v == 99) {
            func_0800EDF4(g_080200E4[g_03001E60[7].field_02 - 16][2], g_080200E4[g_03001E60[7].field_02 - 16][0]);
            func_080085E0();
            func_08014394();
        } else {
            func_0800EDF4(g_080200E4[g_03000B60[v].model - 16][g_03000B60[v].colour + 2],
                          g_080200E4[g_03000B60[v].model - 16][0]);
            func_080085E0();
            func_08014394();
            func_08012600(scr);
        }
    } else {
        func_0800EDF4(g_080200E4[g_03001E60[0].field_02 - 16][g_03000B60[0].colour + 2],
                      g_080200E4[g_03001E60[0].field_02 - 16][0]);
        func_080085E0();
        func_08014394();
        func_08012600(scr);
    }
    do {
        if (g_03001B20) g_03005F70.field_04 = (g_03001B20 & 63) * 3 - 38;
        else g_03005F70.field_04 = g_03005FCC * 3 - 38;
        func_08015D78();
        i = 1;
        if (g_03005FCC != 0 || g_03001B20 != 0) i = 0;
        if (g_03005788 != 0) i = 1;
        if (i == 1) func_080141EC(0);
        func_08015E20();
        g_03000B50 = 0;
        func_08015E34();
        g_03002188 = 0;
        g_030061E4 = 64;
        g_030067E4 = 0;
        g_030061F0 = 0;
        g_03001B24 = 0;
        g_03000DF0 = 0;
        g_03006680 = 0;
        func_08005238(scr);
        func_08015200();
        switch (g_08175B04[scr].type) {
        case 0:
            func_080145B8();
            func_080161E8();
            func_08016134(0x0201A6F0);
            g_03005FC0 = (g_03005FC0 + 1) & 1;
            g_030014A8 = 0;
            break;
        case 1:
        case 2:
            func_08013FAC(scr);
            func_080161E8();
            g_030001B0 = g_08175B04[scr].count;
            func_08016174();
            if (scr == 45 && g_03005FCC == 0 && g_03001B20 == 0) {
                u32 vram = 0x0600BE00;
                if (g_03005FC0 & 1) vram = 0x06001E00;
                for (i = 0; i <= 71; i++)
                    DMA_SET(0x08302120 + i * 240, vram + 64 + i * 240, 0x8400001C);
            }
            g_030014A8 = 1;
            func_08016264();
            g_030021C4 = 0x02019EF0;
            func_08002500(scr);
            g_03000DFC = g_03005FC0 == 0 ? 0x0600A000 : 0x06000000;
            func_08005EF8();
            func_08015250(g_030001B0);
            if (g_03005FCC == 0 && g_03001B20 == 0) {
                g_03002E58 = 0;
                g_030066D4 = 4;
                g_03001B18 = 2;
                if (g_08175B04[scr].text) func_080154AC(g_08175B04[scr].text);
            }
            if (g_03001B20 == 0 && g_03005FCC == 0) {
                g_03002E58 = 0;
                g_030066D4 = 151;
                g_03001B18 = 1;
                if (scr == 11) g_030066D4 = 135;
                if ((scr >= 17 && scr <= 19) || scr == 45 || scr == 60 || scr == 86 || scr == 112) g_030066D4 -= 56;
                if (g_08175B04[g_08175B04[scr].next[g_030014B4]].text) func_080154AC(g_08175B04[g_08175B04[scr].next[g_030014B4]].text);
            }
            if (g_03001B20 == 0 && g_03005FCC == 0 && g_03005F60 == 0) func_0800F2D0(scr);
            func_0800ED28(scr);
            g_03005FC0 = (g_03005FC0 + 1) & 1;
            break;
        }
        switch (g_08175B04[scr].type) {
        case 0:
            if (g_0300218C & 8) {
                g_030001CC = g_08175B04[scr].next[g_030014B4];
                g_03000010 = g_08175B04[scr].action[g_030014B4];
                g_03001B20 = 64;
                func_0801604C(2, 1);
            }
            break;
        case 1:
            if (g_03005FCC != 0) {
                g_03005FCC -= (g_03000B50 + 1) * 2;
                if (g_03005FCC < 0) g_03005FCC = 0;
            }
            if (g_03001B20 != 0) g_03001B20 += (g_03000B50 + 1) * 2;
            if ((g_0300218C & 32) && g_030014B4 > 0) {
                g_030014B4--;
                func_0801604C(1, 1);
            }
            if ((g_0300218C & 16) && g_030014B4 < g_08175B04[scr].count - 1) {
                g_030014B4++;
                func_0801604C(1, 1);
            }
            if ((g_0300218C & 1) && g_03005FCC == 0 && g_03001B20 == 0) {
                g_030001CC = g_08175B04[scr].next[g_030014B4];
                g_03000010 = g_08175B04[scr].action[g_030014B4];
                g_03001B20 = 129;
                func_0801604C(2, 1);
                func_080143CC();
            }
            break;
        case 2:
            if (g_03005FCC != 0) {
                g_03005FCC -= (g_03000B50 + 1) * 2;
                if (g_03005FCC < 0) g_03005FCC = 0;
            }
            if (g_03001B20 != 0) g_03001B20 += (g_03000B50 + 1) * 2;
            func_0800E498(scr);
            if ((g_0300218C & 32) && g_03005FCC == 0 && g_03001B20 == 0 && g_03005F60 == 0) {
                NOT_CANCEL(v)
                if (g_030014B4 > 0) {
                    g_030014B4--;
                    func_0801604C(1, 1);
                }
            }
            if ((g_0300218C & 16) && g_03005FCC == 0 && g_03001B20 == 0 && g_03005F60 == 0) {
                NOT_CANCEL(v)
                if (g_030014B4 < g_08175B04[scr].count - 1) {
                    g_030014B4++;
                    func_0801604C(1, 1);
                }
            }
            if ((g_0300218C & 1) && g_03005FCC == 0 && g_03001B20 == 0 && g_03005F60 == 0) {
                if (scr == 7) g_03001B14 = 0;
                if (scr == 52) g_03001B14 = 1;
                if (scr == 78) g_03001B14 = 2;
                if (scr == 104) g_03001B14 = 3;
                if (scr >= 46 && scr <= 48) {
                    g_030001C0 = 0;
                    g_03002180 = 0;
                }
                if (g_08175B04[scr].action[g_030014B4] <= 199) {
                    v = 0;
                    if (scr == 17) {
                        n = func_08005C7C();
                        if (n > 3) v = 1;
                    }
                    if (scr == 18) {
                        n = func_08005C7C();
                        DENIED(v, n)
                    }
                    if (scr == 19 || scr == 60 || scr == 86 || scr == 112) {
                        n = func_08005C7C();
                        DENIED(v, n)
                    }
                    if (!v) {
                        g_030001CC = g_08175B04[scr].next[g_030014B4];
                        g_03000010 = g_08175B04[scr].action[g_030014B4];
                        g_03001B20 = 129;
                        func_0801604C(2, 1);
                        func_080143CC();
                    }
                } else if (g_030014B4 == 1 && (scr == 7 || scr == 52 || scr == 78 || scr == 104)) {
                    if (g_030001E0[g_03001E50] != 0) {
                        g_03000010 = 3;
                        g_03001B20 = 129;
                        func_0801604C(2, 1);
                        func_080143CC();
                    }
                } else {
                    g_030001CC = func_08010A50(scr);
                }
            }
            if ((g_0300218C & 2) && g_03005FCC == 0 && g_03001B20 == 0) {
                g_03000010 = g_08175B04[scr].back_action;
                g_030001CC = g_08175B04[scr].back_screen;
                g_03001B20 = 257;
                func_08014408();
                func_0801604C(4, 1);
            }
            break;
        }
        if ((g_03001B20 & 127) > 63) {
            if (g_03000010 == 1) goto restart;
            if (g_03000010 == 2) goto reload;
            if (g_03000010 == 3) goto fin;
            if (g_03000010 == 4) {
                if (func_08014208() && func_08013594(0) == 4) {
                    g_030001CC = 1;
                    goto restart;
                }
                func_080130BC();
                goto restart;
            }
            if (g_03000010 == 5) break;
        }
    } while (1);
    func_08013594(2);
    goto restart;
fin:
    for (i = 0; i < 2; i++) {
        func_08015E20();
        g_030014A8 = 0;
        DMA_CLEAR(0x03002A30)
        DMA_CLEAR(0x03000BE0)
        func_08016210(3, 0, 0x06000000, 0x9600, 32);
        func_08016210(3, 0, 0x0600A000, 0x9600, 32);
    }
    return scr;
}

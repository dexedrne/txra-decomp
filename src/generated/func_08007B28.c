/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
/* Race main: course and sprite setup (track table and length chosen by
 * g_03001E50), a 32-step pre-roll of the track streamer,
 * per-mode placement of the player car (g_03001B14 = 0..3), then the frame
 * loop that runs the race until 08008A88 reports a finish (3-6, returned) or
 * a restart (99, the far jump back to `restart`, which is the mapped entry
 * 08007B40 and appears in the ROM as a BL). g_030021A0 receives copies of
 * g_03000B50 between the frame stages. loop.c stores the pre-roll counter's
 * final value (32), which CSE reuses for a later constant 32, and
 * `g_030001B8++; g_030001B8 &= 31` stays two statements so the address copy
 * is hoisted in the first loop pass. */
extern s16 g_030066D0, g_03001E50, g_03001B14, g_03002330, g_03005F54, g_030001BC, g_03000AC0, g_030021CC;
extern u16 g_03005780, g_03004780, g_03005788;
extern s16 g_03002A20[];
extern u32 g_030001C4, g_03001E54, g_030014A8, g_03002188, g_030061E4, g_030067E4, g_030061F0, g_03001B24;
extern u32 g_03000DF0, g_03006680, g_03005FC0, g_03002E4C, g_03000018, g_030001B8, g_03005F50, g_03002334;
extern s32 g_03001E5C;
extern u32 g_03002E50, g_03000B50, g_03000DE0, g_030021C4, g_03000DFC;
extern u32 g_030021A0[];
extern u8 g_03005790[], g_03000B60[];
extern u16 g_030021E0[];
extern u8 g_03002A30[], g_03000BE0[];
extern u8 g_08292DCC[], g_082939CC[], g_082949CC[], g_082AD3CC[], g_082AD7CC[];
extern TxraRow28 g_080CF330[], g_080E0B4C[], g_0812ADCC[], g_08148CF8[], g_080FC468[], g_0811216C[];
extern s16 g_080200E4[][16];
extern TxraRecord g_03001E60[];
extern TxraTriple g_03002320, g_03005F70, g_03002E40;
extern void func_08015CBC(void), func_08016210(s32, s32, u32, s32, s32), func_08015E20(void), func_08015E34(void);
extern void func_08018E84(void), func_08015200(void), func_08014C5C(void), func_08002854(void);
extern void func_0800D1A0(void), func_08005EE0(void), func_080160C4(s32, u8 *, u32, s32, s32);
extern void func_0800AF4C(s32), func_0800A00C(void), func_0800B254(void);
extern void func_080085E0(void), func_0800D3B4(void), func_0800A62C(void), func_0801604C(s32, s32);
extern void func_0800EDF4(s32, s32), func_08015D78(void), func_0800A68C(void), func_08016264(void);
extern void func_0800421C(void), func_08009F84(void), func_08014CE4(u32), func_08005F20(void), func_08005F34(void);
extern void func_08002778(u32), func_080095E4(void), func_08009D94(void), func_08005EF8(void);
extern void func_0800A17C(void), func_0800D214(void), func_0800BBD4(s32), func_0800D4BC(void), func_0800B908(void);
extern void func_0800841C(s32), func_080098DC(void), func_08005F0C(void);
extern s32 func_08008A88(void);
#define DMA_SET(src, dest, cnt) { vu32 *dma = (vu32 *)0x040000D4; dma[0] = (u32)(src); dma[1] = (u32)(dest); dma[2] = (u32)(cnt); dma[2]; }
#define DMA_CLEAR(dest) { vu32 tmp = 0; DMA_SET(&tmp, dest, 0x85000080); }
/* Put the player record on track row n, interpolated towards row n + 1 by
 * g_03002E50 sixteenths, facing along the row three ahead. */
#define PLACE_ON_ROW(rec, index) { \
    s32 n = (index); \
    TxraRow28 *base = g_03006874; \
    TxraRow28 *row = (TxraRow28 *)(n * 28 + (u32)base); \
    TxraRow28 *next = row + 1; \
    (rec)->field_04 = row->field_00 + ((u32)(next->field_00 - row->field_00) * g_03002E50 >> 4); \
    (rec)->field_08 = -(row->field_04 + ((u32)(next->field_04 - row->field_04) * g_03002E50 >> 4)); \
    (rec)->field_0c = row->field_08 + ((u32)(next->field_08 - row->field_08) * g_03002E50 >> 4); \
    row += 3; \
    (rec)->field_34 = ((row->field_0c + 4096) & 16383) << 3; \
    (rec)->field_20 = (rec)->field_34 >> 3; }
s32 func_08007B28(void)
{
    s32 j;
    s32 result;
    g_030066D0 = 0;
    g_030001C4 = 60;
restart:
    func_08015CBC();
    func_08016210(3, 0, 0x02000000, 0x40000, 32);
    func_08016210(3, g_03001E54 + (g_03001E54 << 8), 0x06000000, 0x9600, 16);
    func_08016210(3, g_03001E54 + (g_03001E54 << 8), 0x0600A000, 0x9600, 16);
    g_030014A8 = 0;
    DMA_CLEAR(g_03002A30);
    DMA_CLEAR(g_03000BE0);
    for (j = 0; j < 160; j++) g_030021E0[j] = 0;
    func_08015E20();
    func_08015E20();
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
    switch (g_03001E50) {
    case 0: g_03006874 = g_080CF330; g_03002E4C = 0xA01; g_03000018 = 1; break;
    case 1: g_03006874 = g_080E0B4C; g_03002E4C = 0xFC1; g_03000018 = 1; break;
    case 2: g_03006874 = g_0812ADCC; g_03002E4C = 0x111D; g_03000018 = 3; break;
    case 3: g_03006874 = g_08148CF8; g_03002E4C = 0x19A5; g_03000018 = 3; break;
    case 4: g_03006874 = g_080FC468; g_03002E4C = 0xC77; g_03000018 = 2; break;
    case 5: g_03006874 = g_0811216C; g_03002E4C = 0xE28; g_03000018 = 2; break;
    }
    func_08014C5C();
    g_030001B8 = 0;
    g_03005F50 = g_03002E4C - 32;
    for (j = 0; j < 32; j++) {
        g_03002334 = 0;
        if (++g_03005F50 >= g_03002E4C) g_03005F50 = 0;
        g_030001B8++;
        g_030001B8 &= 31;
        func_08002854();
    }
    g_030001BC = 0;
    g_03001E5C = -204;
    g_03002330 = 0;
    g_03005F54 = 0;
    g_03005F50 = 0;
    func_0800D1A0();
    func_08005EE0();
    g_03000AC0 = 0;
    g_030021CC = 0;
    g_03005780 = 0;
    func_080160C4(3, g_08292DCC, 0x06014000, 0x1000, 32);
    func_080160C4(3, g_082939CC, 0x06014C00, 0x1000, 32);
    func_080160C4(3, g_082949CC, 0x06015C00, 0x500, 32);
    func_080160C4(3, g_082AD3CC, 0x06016100, 0x400, 32);
    func_080160C4(3, g_082AD7CC, 0x06016500, 0x400, 32);
    if (g_03001B14 == 2) {
        g_03002330 = 151;
        g_03005F54 = 0;
        g_03001E60[0].field_00 = 1;
        PLACE_ON_ROW(&g_03001E60[0], g_03005F50);
        g_03001E60[0].field_24 = 0;
        g_03001E60[0].field_38 = 0;
        g_03001E60[0].field_4c = 0;
        g_03001E60[0].field_48 = 48;
        g_03001E60[0].field_28 = 0;
        g_03001E60[0].field_52 = 0;
        g_03001E60[0].field_44 = 0;
        g_03001E60[0].field_4e = 0;
        g_03001E60[0].field_42 = 48;
        g_03001E60[0].field_5c = 0;
        g_03001E60[0].field_3c = 0;
        g_03001E60[0].field_40 = 0;
        func_0800AF4C(0);
        g_03005790[0] = 0;
        g_03005790[1] = 0;
        g_03005790[2] = 0;
        g_03005790[3] = 0;
        g_03005790[4] = 0;
        g_03005780 = 0;
    }
    if (g_03001B14 == 0) {
        g_03002330 = 0;
        g_03005F54 = 32;
        g_03005F50 = 0;
        g_03001E60[0].field_00 = 1;
        PLACE_ON_ROW(&g_03001E60[0], g_03005F50);
        g_03001E60[0].field_24 = 0;
        g_03001E60[0].field_38 = 0;
        g_03001E60[0].field_4c = 0;
        g_03001E60[0].field_48 = 48;
        g_03001E60[0].field_28 = 1920;
        g_03001E60[0].field_52 = 3;
        g_03001E60[0].field_44 = 0;
        g_03001E60[0].field_4e = 0;
        g_03001E60[0].field_42 = 48;
        g_03001E60[0].field_5c = 0;
        g_03001E60[0].field_3c = 0;
        g_03001E60[0].field_40 = 0;
        func_0800AF4C(0);
        func_0800A00C();
    }
    if (g_03001B14 == 1) {
        g_03002330 = 151;
        g_03005F54 = 0;
        g_030001BC = 36;
        g_03005F50 = 0;
        g_03001E60[0].field_00 = 1;
        PLACE_ON_ROW(&g_03001E60[0], g_03005F50);
        g_03001E60[0].field_24 = 0;
        g_03001E60[0].field_38 = 0;
        g_03001E60[0].field_4c = 0;
        g_03001E60[0].field_48 = 48;
        g_03001E60[0].field_28 = 1600;
        g_03001E60[0].field_52 = 3;
        g_03001E60[0].field_44 = 0;
        g_03001E60[0].field_4e = 0;
        g_03001E60[0].field_42 = 48;
        g_03001E60[0].field_3c = 0;
        g_03001E60[0].field_40 = 0;
        func_0800B254();
        g_03002A20[0] = g_03001E60[0].field_38;
        g_03002A20[2] = g_03001E60[g_030001BC & 7].field_38;
        g_03004780 = 4;
        func_0800AF4C(0);
    }
    if (g_03001B14 == 3) {
        g_03002330 = 0;
        g_03005F54 = 32;
        g_03005F50 = 0;
        g_03001E60[0].field_00 = 1;
        PLACE_ON_ROW(&g_03001E60[0], g_03005F50);
        g_03001E60[0].field_24 = 0;
        g_03001E60[0].field_38 = 0;
        g_03001E60[0].field_4c = 0;
        g_03001E60[0].field_48 = 48;
        g_03001E60[0].field_28 = 0;
        g_03001E60[0].field_52 = 0;
        g_03001E60[0].field_44 = 0;
        g_03001E60[0].field_4e = 0;
        g_03001E60[0].field_42 = 48;
        g_03001E60[0].field_5c = 0;
        g_03001E60[0].field_3c = 0;
        g_03001E60[0].field_40 = 0;
        func_0800AF4C(0);
    }
    g_03002320.field_00 = 0;
    g_03002320.field_04 = -8;
    g_03002320.field_08 = 1100;
    g_03005F70.field_00 = 0;
    g_03005F70.field_04 = 0;
    g_03005F70.field_08 = 0;
    g_03002E40.field_08 = 0x2ED8;
    g_03002E40.field_04 = (8192 - g_03001E60[0].field_20) & 16383;
    func_080085E0();
    func_0800D3B4();
    func_0800A62C();
    func_0801604C(31, 0);
    func_0800EDF4(g_080200E4[g_03001E60[0].field_02 - 16][g_03000B60[25] + 2], g_080200E4[g_03001E60[0].field_02 - 16][0]);
    func_08014C5C();
    g_03005788 = 31;
    g_03000B50 = -60;
    while (1) {
        func_08015D78();
    wait:
        func_08015E20();
        if (g_03000B50 <= 3) goto wait;
        g_03000B50 = 0;
        func_0800A68C();
        func_08015E34();
        g_03002188 = 0;
        g_030061E4 = 328;
        g_030067E4 = 0;
        g_030061F0 = 0;
        g_03001B24 = 0;
        g_03000DF0 = 0;
        g_03006680 = 0;
        g_03000DE0 = 0;
        func_08016264();
        func_0800421C();
        func_08015200();
        g_030021A0[0] = g_03000B50;
        func_08009F84();
        if (g_03005FC0 == 0) *(vu16 *)0x04000000 = 0x1444;
        else *(vu16 *)0x04000000 = 0x1454;
        func_08014CE4((u16)g_03005FC0);
        g_030021A0[1] = g_03000B50;
        g_030021C4 = 0x02019EF0;
        func_08005F20();
        g_030021A0[2] = g_03000B50;
        func_08005F34();
        g_030021A0[3] = g_03000B50;
        func_08002778(0);
        g_030021A0[4] = g_03000B50;
        func_080095E4();
        func_08009D94();
        g_030021A0[5] = g_03000B50;
        g_03000DFC = g_03005FC0 == 0 ? 0x0600A000 : 0x06000000;
        func_08005EF8();
        g_030021A0[6] = g_03000B50;
        func_0800A17C();
        func_0800D214();
        g_030021A0[7] = g_03000B50;
        if (g_03000AC0 == 0) {
            func_0800BBD4(0);
            if (g_03000AC0 == 0) {
                func_0800D4BC();
                if (g_03000AC0 == 0) func_0800B908();
            }
        }
        func_0800841C(0);
        func_080098DC();
        func_0800A62C();
        result = func_08008A88();
        if (result == 3) break;
        if (result == 4) break;
        if (result == 5) break;
        if (result == 6) break;
        if (result == 99) goto restart;
        if (g_03000AC0 == 0) func_08005F0C();
        g_03005FC0 = (g_03005FC0 + 1) & 1;
        g_030021A0[0] = g_03000B50;
        g_030021A0[1] = *(vu16 *)0x04000006;
    }
    return result;
}

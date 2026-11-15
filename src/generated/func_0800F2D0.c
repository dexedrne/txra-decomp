/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
/* Menu help/info panel for the highlighted control: per-state texts, class
 * notes gated by unlock bits, model names, rank and record-time lines and
 * the money readout. The repeated blocks are macros; text addresses stay
 * numeric until their tables are mapped. */
extern TxraRecord g_03001E60[];
extern s32 g_08178F04[][34];
extern u8 *g_08178704[][4];
extern u8 g_03000B60[];
extern u8 g_0802260C[];
extern u8 g_03000A70[];
extern u8 g_03005FA0[][5];
extern u8 g_03005680[][2];
extern s32 g_030014B4, g_03002E58, g_030066D4, g_03001B18, g_030001C0, g_030014A4;
extern s32 g_03006870, g_03000DE4, g_030021D4;
extern s16 g_03001B10, g_03002A1C, g_03001E50;
extern void func_0801084C(u32);
extern void func_08010910(s32, s32, s32, s32);
extern void func_080154AC(void *);
extern void func_08012600(s32);

#define TEXT(st, addr) if (g_030014B4 == st) func_0801084C(addr);
#define LINE(st, addr) if (g_030014B4 == st) func_080154AC((void *)addr);
#define NOTE(st, byte, bit, k) \
    if (g_030014B4 == st && !(g_03000B60[byte] & bit)) { \
        shown = 1; \
        func_08010910(8, 80, 9, g_08178F04[g_03001E60[0].field_02 - 16][k]); \
        func_080154AC(g_0802260C); \
    }
#define MODEL(m, addr) if (g_03001E60[7].field_02 == m) func_0801084C(addr);
#define MODELS \
    MODEL(16, 0x08024FF4) MODEL(17, 0x08024F64) MODEL(18, 0x08024FAC) MODEL(19, 0x0802503C) \
    MODEL(20, 0x08025084) MODEL(21, 0x080250CC) MODEL(22, 0x08025114) MODEL(23, 0x0802515C) \
    MODEL(24, 0x080251A4) MODEL(25, 0x080251EC) MODEL(26, 0x08025234) MODEL(27, 0x0802527C) \
    MODEL(28, 0x080252C4) MODEL(29, 0x0802530C) MODEL(30, 0x08025354) MODEL(31, 0x0802539C)
#define RANK(lo, addr) if (g_03001B10 >= lo && g_03001B10 <= lo + 5) func_080154AC((void *)addr);

void func_0800F2D0(s32 key)
{
    s32 shown = 0;
    g_03002E58 = 0;
    g_030066D4 = 80;
    g_03001B18 = 1;
    if (key == 26) {
        TEXT(0, 0x08023CD4) TEXT(1, 0x08023D1C) TEXT(2, 0x08023D64)
        NOTE(1, 3, 2, 1) NOTE(2, 3, 4, 2)
    }
    if (key == 27) {
        TEXT(0, 0x08023DF4) TEXT(1, 0x08023E3C) TEXT(2, 0x08023E84)
        NOTE(1, 4, 2, 3) NOTE(2, 4, 4, 4)
    }
    if (key == 22) {
        TEXT(0, 0x08023F5C) TEXT(1, 0x08023FA4) TEXT(2, 0x08023FEC)
        NOTE(1, 5, 2, 5) NOTE(2, 5, 4, 6)
    }
    if (key == 23) {
        TEXT(0, 0x08024034) TEXT(1, 0x0802407C) TEXT(2, 0x080240C4)
        NOTE(1, 6, 2, 7) NOTE(2, 6, 4, 8)
    }
    if (key == 24) {
        TEXT(0, 0x0802419C) TEXT(1, 0x080241E4) TEXT(2, 0x0802422C)
        NOTE(1, 7, 2, 9) NOTE(2, 7, 4, 10)
    }
    if (key == 25 || key == 64 || key == 90 || key == 116) {
        func_08012600(key);
        TEXT(0, 0x080244FC) TEXT(1, 0x08024544) TEXT(2, 0x0802458C) TEXT(3, 0x080245D4) TEXT(4, 0x0802461C)
        if (key <= 51) {
            NOTE(1, 8, 2, 11) NOTE(2, 8, 4, 12) NOTE(3, 8, 8, 13) NOTE(4, 8, 16, 14)
        }
    }
    if (key == 30 || key == 69 || key == 95 || key == 121) {
        func_08012600(key);
        TEXT(0, 0x08024814) TEXT(1, 0x0802485C) TEXT(2, 0x080248A4) TEXT(3, 0x080248EC) TEXT(4, 0x08024934)
        if (key <= 51) {
            NOTE(1, 10, 2, 17) NOTE(2, 10, 4, 18) NOTE(3, 10, 8, 19) NOTE(4, 10, 16, 20)
        }
    }
    if (key == 31 || key == 70 || key == 96 || key == 122) {
        func_08012600(key);
        TEXT(0, 0x0802497C) TEXT(1, 0x080249C4) TEXT(2, 0x08024A0C) TEXT(3, 0x08024A54) TEXT(4, 0x08024A9C)
        if (key <= 51) {
            NOTE(1, 11, 2, 21) NOTE(2, 11, 4, 22) NOTE(3, 11, 8, 23) NOTE(4, 11, 16, 24)
        }
    }
    if (key == 32 || key == 71 || key == 97 || key == 123) {
        TEXT(0, 0x08024AE4) TEXT(1, 0x08024B2C) TEXT(2, 0x08024B74) TEXT(3, 0x08024BBC) TEXT(4, 0x08024C04)
        if (key <= 51) {
            NOTE(1, 12, 2, 29) NOTE(2, 12, 4, 30) NOTE(3, 12, 8, 31) NOTE(4, 12, 16, 32)
        }
    }
    if (key == 33 || key == 72 || key == 98 || key == 124) {
        func_08012600(key);
        TEXT(0, 0x08024C4C) TEXT(1, 0x08024C94) TEXT(2, 0x08024CDC) TEXT(3, 0x08024D24) TEXT(4, 0x08024D6C)
        if (key <= 51) {
            NOTE(1, 13, 2, 25) NOTE(2, 13, 4, 26) NOTE(3, 13, 8, 27) NOTE(4, 13, 16, 28)
        }
    }
    if (key == 14) {
        TEXT(0, 0x0802473C) TEXT(1, 0x08024784) TEXT(2, 0x080247CC)
        NOTE(1, 9, 2, 15) NOTE(2, 9, 4, 16)
    }
    if (key == 11) {
        g_03001B18 = 1;
        g_03002E58 = 0;
        g_030066D4 = 64;
        RANK(0, 0x0802C974) RANK(6, 0x0802C9BC) RANK(12, 0x0802CA04) RANK(18, 0x0802CA4C)
        RANK(24, 0x0802CA94) RANK(30, 0x0802CADC) RANK(36, 0x0802CB24) RANK(42, 0x0802CB6C)
        RANK(48, 0x0802CBB4) RANK(54, 0x0802CBFC) RANK(60, 0x0802CC44) RANK(66, 0x0802CC8C)
        RANK(72, 0x0802CCD4) RANK(78, 0x0802CD1C) RANK(84, 0x0802CD64) RANK(90, 0x0802CDAC)
        if (g_03001B10 >= 96 && g_03001B10 <= 127) func_080154AC((void *)0x0802CDF4);
        g_03002E58 = 0;
        g_030066D4 = 72;
        func_080154AC(g_08178704[g_03001B10][0]);
        g_03002E58 = 0;
        g_030066D4 = 80;
        func_080154AC(g_08178704[g_03001B10][1]);
        if (g_03005680[g_03001B10][0]) {
            g_03002E58 = 0;
            g_030066D4 = 88;
            g_03001B18 = 0;
            func_080154AC((void *)0x08025AA4);
        }
        g_03001B18 = 1;
        func_0801084C((u32)g_08178704[g_03001B10][3]);
    }
    if (key >= 46 && key <= 48) {
        g_03002E58 = 0;
        g_030066D4 = 64;
        MODELS
        func_080154AC(g_0802260C);
        func_08010910(8, 80, 9, g_08178F04[g_03001E60[7].field_02 - 16][0]);
        shown = 1;
        g_03002E58 = 0;
        g_030066D4 = 96;
        LINE(0, 0x08023C44) LINE(1, 0x080232FC) LINE(2, 0x08023C8C)
    }
    switch (key) {
    case 36: case 37: case 38: case 39: case 40: case 41: case 42: case 43: case 44:
    case 75: case 76: case 77: case 101: case 102: case 103: case 127: case 128: case 129:
        g_03002E58 = 0;
        g_030066D4 = 64;
        MODELS
        if (key >= 36 && key <= 38) {
            func_080154AC(g_0802260C);
            func_08010910(8, 80, 9, g_08178F04[g_03001E60[7].field_02 - 16][0]);
            shown = 1;
        }
        if (key >= 39 && key <= 41) {
            func_080154AC(g_0802260C);
            func_08010910(8, 80, 9, g_08178F04[g_03001E60[7].field_02 - 16][0] * 60 / 100);
            shown = 1;
        }
        break;
    }
    if ((key >= 17 && key <= 19) || key == 45 || key == 60 || key == 86 || key == 112) {
        g_03002E58 = 0;
        g_030066D4 = 64;
        g_03001B18 = 1;
        TEXT(0, 0x08025B34) TEXT(1, 0x08025B7C) TEXT(2, 0x08025BC4)
    }
    if (key == 6) {
        g_03002E58 = 0;
        g_030066D4 = 56;
        g_03001B18 = 0;
        if (g_030014B4 == 0) {
            if (g_03006870 == 0) func_080154AC((void *)0x08022534);
            else func_080154AC((void *)0x080224EC);
        }
        if (g_030014B4 == 1) {
            if (g_03000DE4 == 0) func_080154AC((void *)0x080224A4);
            else func_080154AC((void *)0x0802245C);
        }
        if (g_030014B4 == 2) {
            if (g_030021D4 == 0) func_080154AC((void *)0x08022414);
            else func_080154AC((void *)0x080223CC);
        }
        if (g_030014B4 == 3) {
            s32 rec;
            g_03002E58 = 0;
            g_030066D4 = 40;
            g_03001B18 = 0;
            rec = g_030001C0 >> 7;
            if (g_030001C0 >= 0 && g_030001C0 <= 127) func_080154AC((void *)0x080253E4);
            if (g_030001C0 >= 128 && g_030001C0 <= 255) func_080154AC((void *)0x0802542C);
            if (g_030001C0 >= 256 && g_030001C0 <= 383) func_080154AC((void *)0x08025474);
            if (g_030001C0 >= 384 && g_030001C0 <= 511) func_080154AC((void *)0x080254BC);
            if (g_030001C0 >= 512 && g_030001C0 <= 639) func_080154AC((void *)0x08025504);
            if (g_030001C0 >= 640 && g_030001C0 <= 767) func_080154AC((void *)0x0802554C);
            if (++g_030001C0 > 767) g_030001C0 = 0;
            g_03002190.field_00 = 252;
            g_03002190.field_04 = g_03000A70;
            g_03002E58 = 0;
            g_030066D4 = 64;
            g_03000A70[0] = g_03005FA0[rec][0] + 48;
            g_03000A70[1] = g_03005FA0[rec][1] + 48;
            g_03000A70[2] = '.';
            g_03000A70[3] = g_03005FA0[rec][2] + 48;
            g_03000A70[4] = g_03005FA0[rec][3] + 48;
            g_03000A70[5] = '.';
            g_03000A70[6] = g_03005FA0[rec][4] + 48;
            g_03000A70[7] = 0;
            func_080154AC(&g_03002190);
        }
        if (g_030014B4 == 4) {
            if (g_03002A1C == 0) func_080154AC((void *)0x0802233C);
            else func_080154AC((void *)0x08022384);
        }
        g_03002E58 = 0;
        g_030066D4 = 151;
        g_03001B18 = 1;
        LINE(0, 0x08023464) LINE(1, 0x08023614) LINE(2, 0x080233D4) LINE(3, 0x080234F4) LINE(4, 0x080234AC)
    }
    if (key == 7 || key == 52 || key == 104 || key == 78) {
        g_03002E58 = -66;
        g_030066D4 = 58;
        g_03001B18 = 0;
        if (g_03001E50 == 0) func_080154AC((void *)0x080253E4);
        if (g_03001E50 == 1) func_080154AC((void *)0x0802542C);
        if (g_03001E50 == 2) func_080154AC((void *)0x08025474);
        if (g_03001E50 == 3) func_080154AC((void *)0x080254BC);
        if (g_03001E50 == 4) func_080154AC((void *)0x08025504);
        if (g_03001E50 == 5) func_080154AC((void *)0x0802554C);
    }
    if (key == 11) {
        func_08010910(252, 122, 17, g_03001B10 + 1);
    } else if (key != 45 && key != 6 && key != 7 && key != 52 && key != 78 && key != 104) {
        if (!shown) {
            g_03002E58 = 8;
            g_030066D4 = 64;
            g_03001B18 = 1;
            func_080154AC((void *)0x080225C4);
            g_03002E58 = 8;
            g_030066D4 = 72;
            g_03001B18 = 1;
            if (g_030014A4 <= 99999) func_08010910(8, 72, 1, g_030014A4);
            if (g_030014A4 > 99999) func_08010910(4, 72, 1, g_030014A4);
        } else {
            g_03002E58 = 8;
            g_030066D4 = 16;
            g_03001B18 = 1;
            func_080154AC((void *)0x0802257C);
            g_03002E58 = 8;
            g_030066D4 = 30;
            g_03001B18 = 1;
            if (g_030014A4 <= 99999) func_08010910(8, 56, 1, g_030014A4);
            if (g_030014A4 > 99999) func_08010910(4, 56, 1, g_030014A4);
        }
    }
}

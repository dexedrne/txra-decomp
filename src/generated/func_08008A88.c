/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
/* Pause and result menus during a race (state g_03000AC0, cursor
 * g_03006688). Three passes: cancel/back keys (mask 10), the confirm key
 * (bit 0), then drawing the current menu with the selected line blinking.
 * Returns a code to the race loop (3-6 end the race, 99 restarts it,
 * 0-2 keep it running); every exit funnels through `done`, so
 * the result stays in a register and the copy to r0 is shared with the
 * epilogue at 080095C4. Cases 8 and 9 of the confirm pass are written out
 * separately and only their tails are merged by cross-jumping. */
extern u16 g_0300218C;
extern s16 g_03000AC0, g_03006688, g_03001B14, g_03005788, g_03005F54;
extern u32 g_03000DF4, g_030021D4, g_030014AC, g_03005B38, g_03000DE4, g_03006870;
extern u16 g_030021D0;
extern u32 g_03005FC0, g_03002E58, g_030066D4, g_03001B18, g_03001B1C, g_030014C0, g_030014A4;
extern TxraRecord g_03001E60[];
extern u8 g_0830CDE0[];
extern u8 g_08023584[], g_080235CC[], g_080228DC[], g_0802365C[], g_080224A4[], g_0802245C[];
extern u8 g_08022534[], g_080224EC[], g_08022414[], g_080223CC[], g_08025594[], g_0802566C[];
extern u8 g_080256B4[], g_080255DC[], g_08025AEC[], g_08025624[], g_08022774[], g_080256FC[];
extern u8 g_08025744[], g_080227BC[], g_08022804[];
extern void func_0801604C(s32, s32), func_0800BBD4(s32), func_0800D37C(void), func_0800A5C4(void);
extern void func_0800D290(void), func_0800D4B0(void), func_08016078(s32), func_08018A54(void *, void *, u32);
extern void func_080154AC(u8 *), func_08010910(s32, s32, s32, s32), func_08009D38(void);
#define TEXT_AT(y, size) { g_03002E58 = 0; g_030066D4 = (y); g_03001B18 = (size); }
#define BLINK_OFF(k) (g_03006688 != (k) || (g_03001B1C & 31) <= 15)
s32 func_08008A88(void)
{
    s32 result = 0;
    if (g_0300218C & 10) {
        switch (g_03000AC0) {
        case 0:
            if (g_0300218C & 2) {
                result = 1;
                goto done;
            }
            g_03000AC0 = 1;
            g_03000DF4 = g_030021D4;
            g_03006688 = 0;
            result = 1;
            func_0801604C(4, 1);
            func_0801604C(0, 0);
            break;
        case 1:
            g_030021D4 = g_03000DF4;
            func_0800BBD4(0);
            g_03000AC0 = 0;
            result = 1;
            func_0801604C(4, 1);
            func_0800D37C();
            break;
        case 2:
            g_03000AC0 = 1;
            g_03006688 = 1;
            result = 1;
            func_0801604C(4, 1);
            break;
        case 3:
            g_03000AC0 = 5;
            g_03006688 = 0;
            result = 1;
            func_0801604C(4, 1);
            if (g_030014AC) g_03000AC0 = 11;
            if (g_03001B14 == 0 && g_03005B38) {
                result = 6;
                g_03005B38 = 0;
                g_03000AC0 = 0;
            }
            break;
        case 4:
            g_03000AC0 = 5;
            g_03006688 = 0;
            result = 1;
            func_0801604C(4, 1);
            break;
        case 11:
            g_03000AC0 = 5;
            g_03006688 = 0;
            result = 1;
            func_0801604C(4, 1);
            g_030014AC = 0;
            break;
        case 5:
            g_03000AC0 = 0;
            result = 1;
            func_0801604C(4, 1);
            if (g_03001B14 == 0) func_0800A5C4();
            g_03001E60[0].field_4c = 0;
            func_0800D290();
            func_0800D37C();
            g_03005788 = 31;
            g_03005F54 = 32;
            break;
        case 6:
        case 7:
            g_03000AC0 = 0;
            result = 4;
            func_0801604C(4, 1);
            break;
        case 8:
        case 9:
            g_03000AC0 = 0;
            result = 99;
            func_0801604C(4, 1);
            break;
        case 10:
            g_03000AC0 = 0;
            result = 5;
            func_0801604C(4, 1);
            break;
        }
    }
    if (result) goto done;
    if (g_03000AC0 && (g_0300218C & 1)) {
        switch (g_03000AC0) {
        case 1:
            if (g_03006688 == 0) {
                g_030021D4 = g_03000DF4;
                func_0800BBD4(0);
                g_03000AC0 = 0;
                result = 2;
                func_0800D37C();
            }
            if (g_03006688 == 1) {
                g_03000AC0 = 2;
                g_03006688 = 0;
                result = 1;
            }
            if (g_03006688 == 2) {
                g_03000AC0 = 0;
                result = 3;
            }
            func_0801604C(2, 1);
            break;
        case 2:
            if (g_03006688 == 0) g_03000DE4 ^= 1;
            if (g_03006688 == 1) {
                g_03006870 ^= 1;
                if (g_030021D0 == 1) func_08016078(1);
                if (g_030021D0 == 3) func_08016078(3);
                if (g_030021D0 == 4) func_08016078(4);
                if (g_030021D0 == 8) func_08016078(8);
                if (g_030021D0 == 9) func_08016078(9);
                if (g_030021D0 == 5) func_08016078(5);
            }
            if (g_03006688 == 2) g_03000DF4 ^= 1;
            func_0801604C(2, 1);
            break;
        case 3:
            g_03000AC0 = 5;
            g_03006688 = 0;
            result = 1;
            func_0801604C(4, 1);
            if (g_030014AC) g_03000AC0 = 11;
            if (g_03001B14 == 0 && g_03005B38) {
                result = 6;
                g_03005B38 = 0;
                g_03000AC0 = 0;
            }
            break;
        case 4:
            g_03000AC0 = 5;
            g_03006688 = 0;
            result = 1;
            func_0801604C(4, 1);
            break;
        case 11:
            g_03000AC0 = 5;
            g_03006688 = 0;
            result = 1;
            func_0801604C(4, 1);
            g_030014AC = 0;
            break;
        case 5:
            if (g_03006688 == 0) {
                g_03005788 = 31;
                g_03000AC0 = 0;
                result = 2;
                g_03005F54 = 32;
                func_0800D290();
                func_0800D37C();
                g_03001E60[0].field_4c = 0;
                if (g_03001B14 == 0) func_0800A5C4();
            }
            if (g_03006688 == 1) {
                g_03000AC0 = 0;
                result = 3;
            }
            func_0801604C(2, 1);
            break;
        case 6:
        case 7:
            g_03000AC0 = 0;
            result = 4;
            func_0801604C(2, 1);
            break;
        case 8:
            if (g_03006688 == 0) {
                g_03000AC0 = 0;
                result = 99;
                func_0800D4B0();
                func_0800D37C();
            }
            if (g_03006688 == 1) {
                g_03000AC0 = 0;
                result = 3;
            }
            func_0801604C(2, 1);
            break;
        case 9:
            if (g_03006688 == 0) {
                g_03000AC0 = 0;
                result = 99;
                func_0800D4B0();
                func_0800D37C();
            }
            if (g_03006688 == 1) {
                g_03000AC0 = 0;
                result = 3;
            }
            func_0801604C(2, 1);
            break;
        case 10:
            g_03000AC0 = 0;
            result = 5;
            func_0801604C(2, 1);
            break;
        }
    }
    if (result) goto done;
    if (g_03000AC0) {
        if (g_03005FC0 == 0) func_08018A54(g_0830CDE0, (void *)0x0600C580, 0x12C0);
        if (g_03005FC0 != 0) func_08018A54(g_0830CDE0, (void *)0x06002580, 0x12C0);
    }
    switch (g_03000AC0) {
    case 1:
        if ((g_0300218C & 64) && g_03006688 != 0) {
            g_03006688--;
            func_0801604C(1, 1);
        }
        if ((g_0300218C & 128) && g_03006688 != 2) {
            g_03006688++;
            func_0801604C(1, 1);
        }
        TEXT_AT(48, 2);
        func_080154AC(g_08023584);
        TEXT_AT(76, 1);
        if (BLINK_OFF(0)) func_080154AC(g_080235CC);
        TEXT_AT(84, 1);
        if (BLINK_OFF(1)) func_080154AC(g_080228DC);
        TEXT_AT(92, 1);
        if (BLINK_OFF(2)) func_080154AC(g_0802365C);
        break;
    case 2:
        if ((g_0300218C & 64) && g_03006688 != 0) {
            g_03006688--;
            func_0801604C(1, 1);
        }
        if ((g_0300218C & 128) && g_03006688 != 2) {
            g_03006688++;
            func_0801604C(1, 1);
        }
        TEXT_AT(48, 2);
        func_080154AC(g_080228DC);
        TEXT_AT(76, 1);
        if (BLINK_OFF(0)) {
            if (g_03000DE4 == 0) func_080154AC(g_080224A4);
            else func_080154AC(g_0802245C);
        }
        TEXT_AT(84, 1);
        if (BLINK_OFF(1)) {
            if (g_03006870 == 0) func_080154AC(g_08022534);
            else func_080154AC(g_080224EC);
        }
        TEXT_AT(92, 1);
        if (BLINK_OFF(2)) {
            if (g_03000DF4 == 0) func_080154AC(g_08022414);
            else func_080154AC(g_080223CC);
        }
        break;
    case 3:
        TEXT_AT(48, 2);
        func_080154AC(g_08025594);
        TEXT_AT(72, 1);
        func_080154AC(g_0802566C);
        func_08010910(252, 80, 1, g_030014C0);
        TEXT_AT(92, 1);
        func_080154AC(g_080256B4);
        func_08010910(252, 100, 1, g_030014A4);
        break;
    case 4:
        TEXT_AT(48, 2);
        func_080154AC(g_080255DC);
        TEXT_AT(72, 1);
        func_080154AC(g_0802566C);
        func_08010910(252, 80, 1, g_030014C0);
        TEXT_AT(92, 1);
        func_080154AC(g_080256B4);
        func_08010910(252, 100, 1, g_030014A4);
        break;
    case 11:
        TEXT_AT(64, 2);
        func_080154AC(g_08025AEC);
        break;
    case 5:
        if ((g_0300218C & 64) && g_03006688 != 0) {
            g_03006688--;
            func_0801604C(1, 1);
        }
        if ((g_0300218C & 128) && g_03006688 != 1) {
            g_03006688++;
            func_0801604C(1, 1);
        }
        TEXT_AT(48, 2);
        func_080154AC(g_08025624);
        TEXT_AT(80, 1);
        if (BLINK_OFF(0)) func_080154AC(g_08022774);
        TEXT_AT(88, 1);
        if (BLINK_OFF(1)) func_080154AC(g_0802365C);
        break;
    case 6:
        TEXT_AT(62, 2);
        func_080154AC(g_080256FC);
        TEXT_AT(80, 0);
        func_08009D38();
        break;
    case 7:
        TEXT_AT(62, 2);
        func_080154AC(g_08025744);
        TEXT_AT(80, 0);
        func_08009D38();
        break;
    case 8:
        if ((g_0300218C & 64) && g_03006688 != 0) {
            g_03006688--;
            func_0801604C(1, 1);
        }
        if ((g_0300218C & 128) && g_03006688 != 1) {
            g_03006688++;
            func_0801604C(1, 1);
        }
        TEXT_AT(48, 2);
        func_080154AC(g_08025594);
        TEXT_AT(80, 1);
        if (BLINK_OFF(0)) func_080154AC(g_080227BC);
        TEXT_AT(88, 1);
        if (BLINK_OFF(1)) func_080154AC(g_0802365C);
        break;
    case 9:
        if ((g_0300218C & 64) && g_03006688 != 0) {
            g_03006688--;
            func_0801604C(1, 1);
        }
        if ((g_0300218C & 128) && g_03006688 != 1) {
            g_03006688++;
            func_0801604C(1, 1);
        }
        TEXT_AT(48, 2);
        func_080154AC(g_080255DC);
        TEXT_AT(80, 1);
        if (BLINK_OFF(0)) func_080154AC(g_08022804);
        TEXT_AT(88, 1);
        if (BLINK_OFF(1)) func_080154AC(g_0802365C);
        break;
    case 10:
        TEXT_AT(64, 2);
        func_080154AC(g_08025594);
        break;
    }
done:
    return result;
}

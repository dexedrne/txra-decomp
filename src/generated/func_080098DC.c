/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
/* Per-frame race event handler. A running result timer (g_030021CC) picks
 * the outcome per mode when it reaches zero; in mode 0 a nearby rival in
 * slots 4-7 can be challenged; in mode 2 the checkpoint bits advance and the
 * five clock digits (g_03005790, limits 9/9/5/9/9) tick by two.
 * Each outcome branch keeps its own call-and-clear tail: CSE then reuses the
 * known-zero timer register for g_030001BC, and jump optimisation merges the
 * identical tails the way the original does. */
extern s16 g_030021CC, g_03001B14, g_03005F7C, g_03004DD4, g_03000AC0, g_030001BC, g_030066D0;
extern s16 g_03001E50, g_03005F54, g_03002A1C, g_03004780, g_03002330, g_03002A20[];
extern u16 g_030014BC, g_03005780;
extern u32 g_03005F50, g_03002E4C, g_030021D4;
extern u8 g_03005FA0[], g_03005790[];
extern TxraRecord g_03001E60[];
extern void func_0801604C(s32, s32), func_08016078(s32);
extern s32 func_0800D1B8(void);
#define LOCK_ON() { \
    g_030001BC &= 7; \
    g_03002A20[0] = g_03001E60[0].field_38; \
    g_03002A20[2] = g_03001E60[g_030001BC].field_38; \
    func_08016078(9); }
void func_080098DC(void)
{
    s32 i;
    if (g_030021CC) {
        g_030021CC--;
        if (!g_030021CC) {
            switch (g_03001B14) {
            case 0:
                if (g_03005F7C > g_03004DD4) {
                    g_03000AC0 = 3;
                    func_0801604C(0, 0);
                    g_030001BC = 0;
                    return;
                }
                g_03000AC0 = 4;
                func_0801604C(0, 0);
                g_030001BC = 0;
                return;
            case 1:
                if (g_03005F7C > g_03004DD4) {
                    if ((u16)g_030066D0 == 49) {
                        g_03000AC0 = 10;
                        func_0801604C(0, 0);
                        g_030001BC = 0;
                        g_030066D0++;
                        return;
                    }
                    g_03000AC0 = 8;
                    func_0801604C(0, 0);
                    g_030001BC = 0;
                    g_030066D0++;
                    return;
                } else {
                    g_03000AC0 = 9;
                    func_0801604C(0, 0);
                    g_030001BC = 0;
                    return;
                }
            case 2:
                if (!func_0800D1B8()) {
                    g_03000AC0 = 7;
                    func_08016078(7);
                    func_0801604C(0, 0);
                } else {
                    g_03000AC0 = 6;
                    func_08016078(6);
                    func_0801604C(0, 0);
                    for (i = 0; i <= 4; i++)
                        g_03005FA0[i + g_03001E50 * 5] = g_03005790[i];
                }
                return;
            }
        }
    }
    if (!g_03001B14) {
        if (!g_03005F54 && g_030001BC <= 2 && !g_03000AC0 && !g_030021CC) {
            g_030001BC = 0;
            for (i = 4; i <= 7; i++) {
                TxraRecord *other = &g_03001E60[i];
                if (other->field_00
                    && other->field_38 >= g_03001E60[0].field_38
                    && other->field_38 <= g_03001E60[0].field_38 + 8
                    && other->field_42 < g_03001E60[0].field_42 + 8
                    && other->field_42 > g_03001E60[0].field_42 - 8) {
                    g_030001BC = 1;
                    g_03004780 = i;
                    if ((!g_03002A1C && (g_030014BC & 256)) || (g_03002A1C == 1 && (g_030014BC & 64))) {
                        g_030001BC = i | 32;
                        g_03002330 = 192;
                        func_08016078(5);
                    }
                }
            }
        }
        if (!g_03001B14 && (g_030001BC & 32) && !g_03000AC0 && !g_030021CC && (u16)g_03002330 == 1)
            LOCK_ON();
    }
    if ((u16)g_03001B14 == 1 && (g_030001BC & 32) && !g_03000AC0 && !g_030021CC && (u16)g_03002330 == 1)
        LOCK_ON();
    if (g_03001B14 == 2 && !g_03000AC0 && !g_030021CC) {
        if ((g_03005780 & 31) == 31 && g_03005F50 && g_03005F50 <= 3) {
            g_030021CC = 48;
            g_03001E60[0].field_4c = 2;
            g_030021D4 = 1;
            return;
        }
        if (g_03005F50 - 256 <= 255) g_03005780 = (g_03005780 | 1) & 253;
        if (g_03005F50 - 512 <= 255 && (g_03005780 & 1)) g_03005780 = (g_03005780 | 2) & 251;
        if (g_03005F50 - 768 <= 255 && (g_03005780 & 2)) g_03005780 = (g_03005780 | 4) & 247;
        if (g_03005F50 - 1024 <= 255 && (g_03005780 & 4)) g_03005780 = (g_03005780 | 8) & 239;
        if (g_03005F50 >= g_03002E4C - 256 && (g_03005780 & 8)) g_03005780 = (g_03005780 | 16) & 223;
        if (!g_03002330) {
            g_03005790[4] += 2;
            if ((s8)g_03005790[4] <= 9) return;
            g_03005790[4] = 0;
            g_03005790[3]++;
            if ((s8)g_03005790[3] <= 9) return;
            g_03005790[3] = 0;
            g_03005790[2]++;
            if ((s8)g_03005790[2] <= 5) return;
            g_03005790[2] = 0;
            g_03005790[1]++;
            if ((s8)g_03005790[1] <= 9) return;
            g_03005790[1] = 0;
            g_03005790[0]++;
            if ((s8)g_03005790[0] <= 9) return;
            g_03005790[0] = 9;
            g_03005790[1] = 9;
            g_03005790[2] = 9;
            g_03005790[3] = 9;
            g_03005790[4] = 9;
        }
    }
}

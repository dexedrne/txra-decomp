/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
/* Shop/garage confirm handler for the highlighted control: cycles colours,
 * selects or buys tuning parts against the price table (unlock bits in
 * g_03000B60), buys, sells and swaps cars, steps settings, and plays the
 * confirm sound. Returns the next control id. The original reads m in the
 * second colour branch without setting it; that is kept. */
extern TxraRecord g_03001E60[];
extern s32 g_08178F04[][34];
extern s16 g_080200E4[][16];
extern u8 g_03000B60[];
extern s32 g_030014B4, g_030014A4, g_03002180, g_03000010, g_03001B20;
extern s32 g_030014B8, g_03005F40, g_03000AC4, g_03000B58, g_03000AC8, g_03005FD4;
extern s32 g_03006870, g_03000DE4, g_030021D4;
extern s16 g_03001B10, g_03005F60, g_03001E50, g_03002A1C;
extern void func_0800EDF4(s32, s32);
extern void func_08014364(void);
extern void func_0801238C(void);
extern void func_08014408(void);
extern void func_08005C7C(void);
extern void func_08014264(s32);
extern void func_08014300(void);
extern void func_080142AC(s32);
extern void func_08016078(s32);
extern void func_0801604C(s32, s32);

#define PRICE(k) g_08178F04[g_03001E60[0].field_02 - 16][k]
#define SELECT(sel) \
    if (g_030014B4 == 0 && g_03000B60[sel] != 1) { \
        done = 1; \
        g_03000B60[sel] = 1; \
    }
#define BUY(st, flag, k, sel) \
    if (g_030014B4 == st) { \
        if (key <= 51 && !(g_03000B60[flag] & (1 << st)) && g_030014A4 >= PRICE(k)) { \
            done = 1; \
            g_030014A4 -= PRICE(k); \
            g_03000B60[flag] |= 1 << st; \
            g_03000B60[sel] = st + 1; \
        } else if (g_03000B60[flag] & (1 << st)) { \
            done = 1; \
            g_03000B60[sel] = st + 1; \
        } \
    }
#define PART2(k1, k2, k3, k4, flag, p, sel) \
    if (key == k1 || key == k2 || key == k3 || key == k4) { \
        SELECT(sel) BUY(1, flag, p, sel) BUY(2, flag, p + 1, sel) \
    }
#define PART4(k1, k2, k3, k4, flag, p, sel) \
    if (key == k1 || key == k2 || key == k3 || key == k4) { \
        SELECT(sel) BUY(1, flag, p, sel) BUY(2, flag, p + 1, sel) BUY(3, flag, p + 2, sel) BUY(4, flag, p + 3, sel) \
    }
#define CAR_PRICE g_08178F04[g_03001E60[7].field_02 - 16][0]
#define PICK_CAR \
    if (g_030014B4 == 0) { done = 1; g_03005F60 = 1; } \
    if (g_030014B4 == 1 && g_030014A4 >= CAR_PRICE) { \
        done = 1; \
        g_030014A4 -= CAR_PRICE; \
        ret = 1; \
        g_03000010 = 1; \
        g_03001B20 = 129; \
        g_03000B60[2] = g_03001E60[0].field_02 = g_03001E60[7].field_02; \
    } \
    if (g_030014B4 == 2) { done = 1; g_03005F60 = 1; }
#define NEW_CAR \
    if (g_030014B4 == 0) { done = 1; g_03005F60 = 1; } \
    if (g_030014B4 == 1 && g_030014A4 >= CAR_PRICE) { \
        done = 1; \
        g_030014A4 -= CAR_PRICE; \
        func_08014364(); \
        func_0801238C(); \
        ret = 17; \
        g_03000010 = 1; \
        g_03001B20 = 129; \
        func_08014408(); \
    } \
    if (g_030014B4 == 2) { done = 1; g_03005F60 = 1; }
#define SELL_CAR(count, slot) \
    if (g_030014B4 == 0) { func_08005C7C(); if (count > 1) { done = 1; g_03005F60 = 1; } } \
    if (g_030014B4 == 1) { \
        done = 1; \
        g_030014A4 += CAR_PRICE * 60 / 100; \
        func_08014264(slot); \
        func_08014300(); \
        g_03001E60[7].field_02 = g_03001E60[0].field_02 = g_03000B60[2]; \
        ret = 18; \
        g_03000010 = 1; \
        g_03001B20 = 129; \
        func_08014408(); \
    } \
    if (g_030014B4 == 2) { func_08005C7C(); if (count > 1) { done = 1; g_03005F60 = 1; } }
#define SWAP_CAR(k1, k2, k3, k4, count, slot, var) \
    if (key == k1 || key == k2 || key == k3 || key == k4) { \
        if (g_030014B4 == 0) { func_08005C7C(); if (count > 1) { done = 1; g_03005F60 = 1; } } \
        if (g_030014B4 == 1) { \
            done = 1; \
            func_080142AC(slot); \
            g_03001E60[7].field_02 = g_03001E60[0].field_02 = g_03000B60[2]; \
            if (key == k1) ret = 19; \
            if (key == k2) ret = 60; \
            if (key == k3) ret = 86; \
            if (key == k4) ret = 112; \
            g_03000010 = 1; \
            g_03001B20 = 129; \
            var = 0; \
            func_08014408(); \
        } \
        if (g_030014B4 == 2) { func_08005C7C(); if (count > 1) { done = 1; g_03005F60 = 1; } } \
    }

s32 func_08010A50(s32 key)
{
    s32 done = 0;
    s32 ret = key;
    s32 m;
    if (key == 16 || key == 59 || key == 85 || key == 111) {
        if (g_030014B4 == 0) {
            done = 1;
            m = g_03001E60[0].field_02 - 16;
            g_03000B60[25]++;
            if (g_03000B60[25] >= g_080200E4[m][1]) g_03000B60[25] = 0;
            func_0800EDF4(g_080200E4[m][g_03000B60[25] + 2], g_080200E4[m][0]);
        }
        if (g_030014B4 == 1) {
            done = 1;
            g_03000B60[25] = 0;
            func_0800EDF4(g_080200E4[m][g_03000B60[25] + 2], g_080200E4[m][0]);
        }
    }
    PART2(26, 65, 91, 117, 3, 1, 14)
    PART2(27, 66, 92, 118, 4, 3, 15)
    PART2(22, 61, 87, 113, 5, 5, 16)
    PART2(23, 62, 88, 114, 6, 7, 17)
    PART2(24, 63, 89, 115, 7, 9, 18)
    PART4(25, 64, 90, 116, 8, 11, 19)
    PART4(30, 69, 95, 121, 10, 17, 21)
    PART4(31, 70, 96, 122, 11, 21, 22)
    PART4(32, 71, 97, 123, 12, 29, 23)
    PART4(33, 72, 98, 124, 13, 25, 24)
    PART2(14, 57, 83, 109, 9, 15, 20)
    if (key == 11) {
        if (g_030014B4 == 0) {
            done = 1;
            g_03002180 = 0;
            g_03001B10 = (g_03001B10 - 1) & 127;
        }
        if (g_030014B4 == 1) {
            done = 1;
            g_03002180 = 0;
            g_03001B10 = (g_03001B10 + 1) & 127;
        }
    }
    if (key == 46) { PICK_CAR }
    if (key == 47) { PICK_CAR }
    if (key == 48) { PICK_CAR }
    if (key == 36) { NEW_CAR }
    if (key == 37) { NEW_CAR }
    if (key == 38) { NEW_CAR }
    if (key == 39) { SELL_CAR(g_030014B8, 0) }
    if (key == 40) { SELL_CAR(g_03005F40, 1) }
    if (key == 41) { SELL_CAR(g_03000AC4, 2) }
    SWAP_CAR(42, 75, 101, 127, g_030014B8, 0, g_03000B58)
    SWAP_CAR(43, 76, 102, 128, g_03005F40, 1, g_03000AC8)
    SWAP_CAR(44, 77, 103, 129, g_03000AC4, 2, g_03005FD4)
    if (key == 7 || key == 52 || key == 78 || key == 104) {
        if (g_030014B4 == 0) {
            done = 1;
            if (--g_03001E50 < 0) g_03001E50 = 5;
        }
        if (g_030014B4 == 2) {
            done = 1;
            if (++g_03001E50 > 5) g_03001E50 = 0;
        }
    }
    if (key == 6) {
        if (g_030014B4 == 0) {
            done = 1;
            g_03006870 ^= 1;
            if (g_03006870 == 1) func_08016078(2);
            else func_08016078(0);
        }
        if (g_030014B4 == 1) {
            done = 1;
            g_03000DE4 ^= 1;
        }
        if (g_030014B4 == 2) {
            done = 1;
            g_030021D4 ^= 1;
        }
        if (g_030014B4 == 4) {
            done = 1;
            g_03002A1C ^= 1;
        }
    }
    if (done) {
        if (done == 1) func_0801604C(2, 1);
    }
    return ret;
}

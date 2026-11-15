/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
/* Car-select input: when the 32-frame highlight pulse hits frame 16, a
 * touched control steps the player's or the rival's model within its class
 * (16-21, 22-26, 27-31) or cycles one of three lineup slots. The repeated
 * bodies are written as macros; entry field names are offset-style guesses. */
typedef struct { u8 unknown_00[2]; u8 model; u8 unknown_03[22]; u8 colour; u8 unknown_1a[6]; } CarEntry;
extern TxraRecord g_03001E60[];
extern TxraTriple g_03002320;
extern CarEntry g_03000B60[];
extern s16 g_080200E4[][16];
extern s16 g_03005F60;
extern s32 g_030014B4, g_030001C0, g_03002180;
extern s32 g_03000B58, g_03000AC8, g_03005FD4;
extern void func_08014250(s32, s32);
extern void func_08012600(s32);
extern s32 func_0800EC70(s32, s32);
extern s32 func_0800ECCC(s32, s32);

#define PLAYER_MODEL(lo, hi) \
    if (g_030014B4 == 0) { \
        if (--g_03001E60[7].field_02 < lo) g_03001E60[7].field_02 = hi; \
        g_03001E60[0].field_02 = g_03001E60[7].field_02; \
        func_08014250(g_080200E4[g_03001E60[0].field_02 - 16][g_03000B60[0].colour + 2], \
                      g_080200E4[g_03001E60[0].field_02 - 16][0]); \
        g_030001C0 = 0; \
        g_03002180 = 0; \
    } \
    if (g_030014B4 == 2) { \
        if (++g_03001E60[7].field_02 > hi) g_03001E60[7].field_02 = lo; \
        g_03001E60[0].field_02 = g_03001E60[7].field_02; \
        func_08014250(g_080200E4[g_03001E60[0].field_02 - 16][g_03000B60[0].colour + 2], \
                      g_080200E4[g_03001E60[0].field_02 - 16][0]); \
        g_030001C0 = 0; \
        g_03002180 = 0; \
    }

#define RIVAL_MODEL(lo, hi) \
    if (g_030014B4 == 0) { \
        if (--g_03001E60[7].field_02 < lo) g_03001E60[7].field_02 = hi; \
        func_08014250(g_080200E4[g_03001E60[7].field_02 - 16][2], \
                      g_080200E4[g_03001E60[7].field_02 - 16][0]); \
        g_030001C0 = 0; \
        g_03002180 = 0; \
    } \
    if (g_030014B4 == 2) { \
        if (++g_03001E60[7].field_02 > hi) g_03001E60[7].field_02 = lo; \
        func_08014250(g_080200E4[g_03001E60[7].field_02 - 16][2], \
                      g_080200E4[g_03001E60[7].field_02 - 16][0]); \
        g_030001C0 = 0; \
        g_03002180 = 0; \
    }

#define LINEUP(slot, var) \
    if (g_030014B4 == 0) { \
        var = func_0800EC70(slot, var); \
        g_03001E60[7].field_02 = g_03000B60[var].model; \
        func_08014250(g_080200E4[g_03000B60[var].model - 16][g_03000B60[var].colour + 2], \
                      g_080200E4[g_03000B60[var].model - 16][0]); \
        func_08012600(key); \
        g_030001C0 = 0; \
        g_03002180 = 0; \
    } \
    if (g_030014B4 == 2) { \
        var = func_0800ECCC(slot, var); \
        g_03001E60[7].field_02 = g_03000B60[var].model; \
        func_08014250(g_080200E4[g_03000B60[var].model - 16][g_03000B60[var].colour + 2], \
                      g_080200E4[g_03000B60[var].model - 16][0]); \
        func_08012600(key); \
        g_030001C0 = 0; \
        g_03002180 = 0; \
    }

void func_0800E498(s32 key)
{
    if (g_03005F60 == 0) return;
    if (++g_03005F60 > 31) {
        g_03005F60 = 0;
        g_03002320.field_08 = 1000;
    }
    if (g_03005F60 <= 15) g_03002320.field_08 = (g_03005F60 << 8) + 1000;
    else g_03002320.field_08 = ((31 - g_03005F60) << 8) + 1000;
    if (g_03005F60 != 16) return;
    switch (key) {
    case 46: PLAYER_MODEL(16, 21) break;
    case 47: PLAYER_MODEL(22, 26) break;
    case 48: PLAYER_MODEL(27, 31) break;
    case 36: RIVAL_MODEL(16, 21) break;
    case 37: RIVAL_MODEL(22, 26) break;
    case 38: RIVAL_MODEL(27, 31) break;
    case 39: case 42: case 75: case 101: case 127: LINEUP(0, g_03000B58) break;
    case 40: case 43: case 76: case 102: case 128: LINEUP(1, g_03000AC8) break;
    case 41: case 44: case 77: case 103: case 129: LINEUP(2, g_03005FD4) break;
    }
}

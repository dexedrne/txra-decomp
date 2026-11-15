/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
typedef struct {
    u8 unknown_00[0x14];
    s32 state;
    u8 unknown_18[4];
    s32 sample;
    s32 enabled;
    u8 unknown_24[0xC];
    s32 step;
    u8 unknown_34[4];
    s32 pos;
    u32 length;
    u8 unknown_40[8];
} Voice;
typedef struct { s8 *data; s32 unknown_04; s32 loop; s32 unknown_0c; } Sample;
extern Voice g_03007770[];
extern Sample g_083B8698[];
extern s8 g_083334A8[];
extern s32 g_03006A98;
extern s8 g_03007410[];
void func_080076F4(s32 n)
{
    s32 sum;
    s32 pos0, pos1, pos2, pos3;
    s8 *data0, *data1, *data2, *data3;
    s32 step0, step1, step2, step3;
    s32 buf, buf1, i, nextbuf;
    pos0 = g_03007770[n].pos;
    step0 = g_03007770[n].step;
    pos1 = g_03007770[n + 1].pos;
    step1 = g_03007770[n + 1].step;
    pos2 = g_03007770[n + 2].pos;
    step2 = g_03007770[n + 2].step;
    pos3 = g_03007770[n + 3].pos;
    step3 = g_03007770[n + 3].step;
    data0 = g_083B8698[g_03007770[n].sample].data;
    data1 = g_083B8698[g_03007770[n + 1].sample].data;
    data2 = g_083B8698[g_03007770[n + 2].sample].data;
    data3 = g_083B8698[g_03007770[n + 3].sample].data;
    if (g_03007770[n].state == 0x60 || g_03007770[n].enabled == 0 || pos0 == -1) {
        step0 = 0;
        data0 = g_083334A8;
        pos0 = -1;
    }
    if (g_03007770[n + 1].state == 0x60 || g_03007770[n + 1].enabled == 0 || pos1 == -1) {
        step1 = 0;
        data1 = g_083334A8;
        pos1 = -1;
    }
    if (g_03007770[n + 2].state == 0x60 || g_03007770[n + 2].enabled == 0 || pos2 == -1) {
        step2 = 0;
        data2 = g_083334A8;
        pos2 = -1;
    }
    if (g_03007770[n + 3].state == 0x60 || g_03007770[n + 3].enabled == 0 || pos3 == -1) {
        step3 = 0;
        data3 = g_083334A8;
        pos3 = -1;
    }
    buf = (g_03006A98 + 1) & 1;
    i = 0;
    buf1 = buf * 176;
    if (buf == i) buf1 = i;
    nextbuf = buf1 + 1;
    for (i = 0; i <= 175; i += 2) {
        { s32 part;
        part = data0[pos0 >> 14] + data3[pos3 >> 14];
        sum = part + (data2[pos2 >> 14] + data1[pos1 >> 14]);
        sum >>= 2;
        g_03007410[i + buf1] = sum;
        }
        pos1 += step1;
        pos2 += step2;
        pos0 += step0;
        pos3 += step3;
        { s32 part;
        part = data0[pos0 >> 14] + data3[pos3 >> 14];
        sum = part + (data2[pos2 >> 14] + data1[pos1 >> 14]);
        sum >>= 2;
        g_03007410[i + nextbuf] = sum;
        }
        pos0 += step0;
        pos1 += step1;
        pos2 += step2;
        pos3 += step3;
    }
    if ((u32)pos0 >= g_03007770[n].length) {
        if (g_083B8698[g_03007770[n].sample].loop == 1) pos0 = -1;
        else pos0 = 0;
    }
    if ((u32)pos1 >= g_03007770[n + 1].length) {
        if (g_083B8698[g_03007770[n + 1].sample].loop == 1) pos1 = -1;
        else pos1 = 0;
    }
    if ((u32)pos2 >= g_03007770[n + 2].length) {
        if (g_083B8698[g_03007770[n + 2].sample].loop == 1) pos2 = -1;
        else pos2 = 0;
    }
    if ((u32)pos3 >= g_03007770[n + 3].length) {
        if (g_083B8698[g_03007770[n + 3].sample].loop == 1) pos3 = -1;
        else pos3 = 0;
    }
    g_03007770[n].pos = pos0;
    g_03007770[n + 1].pos = pos1;
    g_03007770[n + 2].pos = pos2;
    g_03007770[n + 3].pos = pos3;
}

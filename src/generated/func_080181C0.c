/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
/* Car contact owner 080181C0..08018854 (ARM, APCS frame of 72 bytes): rotates
 * six probe points of car i into car j's frame and tests them against car j's
 * model box. The probe array, the box tables and the heading mask are written so
 * that loop strength reduction, the two loop passes and register allocation make
 * the original's choices (see docs/FINISH3-1115-contact.md). */
extern s32 g_03001E6C[][25];
extern s32 g_03001E64[][25];
extern TxraRecord g_03001E60[];
extern TxraTriple g_030057A0[];
extern s32 g_03005F90[], g_080202E4[], g_08020B04[], g_08020B08[];
extern s32 g_083D2280[], g_083C2280[];
extern s16 g_030021CC;
s32 func_080181C0(void)
{
    s32 j;
    s32 i;
    s32 angle;
    s32 width;
    s32 height;
    s32 mask;
    s32 result;
    s32 known;
    s32 k;
    s32 model;
    u32 a;
    TxraTriple *p;
    u8 *wt;
    u8 *ht;
    p = g_030057A0;
    wt = (u8 *)g_08020B04;
    ht = (u8 *)g_08020B08;
    result = 0;
    mask = 0;
    i = 0;
    angle = (-g_03001E60[0].field_20) & 0x3FFF;
    do {
        if (g_03001E60[i].field_00) {
            j = 0;
            do {
                known = 0;
                if (g_03005F90[0] == i + j * 16 || g_03005F90[0] == j + i * 16) known = 1;
                if (g_03005F90[1] == i + j * 16 || g_03005F90[1] == j + i * 16) known = 1;
                if (g_03005F90[2] == i + j * 16 || g_03005F90[2] == j + i * 16) known = 1;
                if (g_03005F90[3] == i + j * 16 || g_03005F90[3] == j + i * 16) known = 1;
                if (mask & g_080202E4[i]) goto next_pair;
                if (mask & g_080202E4[j]) goto next_pair;
                if (g_03001E60[j].field_00 && j != i) {
                    p[0].field_00 = -64;
                    p[0].field_08 = -192;
                    p[1].field_00 = 64;
                    p[1].field_08 = -192;
                    p[2].field_00 = -64;
                    p[3].field_00 = 64;
                    p[4].field_00 = -64;
                    p[4].field_08 = 0;
                    p[5].field_00 = 64;
                    p[5].field_08 = 0;
                    p[2].field_08 = 192;
                    p[3].field_08 = 192;
                    model = g_03001E60[j].field_02 * 8;
                    width = *(s32 *)(wt + model);
                    height = *(s32 *)(ht + model);
                    a = g_03001E60[j].field_20;

                    for (k = 0; k <= 5; k++) {
                        s32 x;
                        s32 z;
                        s32 xx;
                        s32 zz;
                        x = p[k].field_00;
                        z = p[k].field_08;
                        xx = ((x * g_083D2280[a << 18 >> 18] - z * g_083C2280[a << 18 >> 18]) >> 12) + (g_03001E60[j].field_04 - g_03001E60[i].field_04);
                        zz = ((x * g_083C2280[a << 18 >> 18] + z * g_083D2280[a << 18 >> 18]) >> 12) + (g_03001E60[j].field_0c - g_03001E60[i].field_0c);
                        p[k].field_00 = (xx * g_083D2280[angle] - zz * g_083C2280[angle]) >> 12;
                        p[k].field_08 = (xx * g_083C2280[angle] + zz * g_083D2280[angle]) >> 12;
                    }
                    for (k = 0; k <= 5; k++) {
                        if (g_030057A0[k].field_00 > -width && g_030057A0[k].field_00 < width
                         && g_030057A0[k].field_08 > -height && g_030057A0[k].field_08 < height) {
                            if (!known) {
                                g_03001E60[i].field_3c = g_03001E60[j].field_28 + 560;
                                g_03001E60[j].field_3c = g_03001E60[i].field_28 + 560;
                                g_03001E60[i].field_3e = g_03001E60[i].field_20;
                                g_03001E60[j].field_3e = g_03001E60[j].field_20;
                                g_03001E60[i].field_3a = g_03001E60[j].field_20 & ~0xC000;
                                g_03001E60[j].field_3a = g_03001E60[i].field_20 & ~0xC000;
                                if (g_030057A0[k].field_00 > 32) {
                                    g_03001E60[i].field_3a = (g_03001E60[i].field_3a - 256) & ~0xC000;
                                    g_03001E60[i].field_3e = (g_03001E60[i].field_3e - 256) & ~0xC000;
                                    g_03001E60[j].field_3a = (g_03001E60[j].field_3a + 256) & ~0xC000;
                                    g_03001E60[j].field_3e = (g_03001E60[j].field_3e + 256) & ~0xC000;
                                }
                                if (g_030057A0[k].field_00 < -32) {
                                    g_03001E60[i].field_3a = (g_03001E60[i].field_3a + 256) & ~0xC000;
                                    g_03001E60[i].field_3e = (g_03001E60[i].field_3e + 256) & ~0xC000;
                                    g_03001E60[j].field_3a = (g_03001E60[j].field_3a - 256) & ~0xC000;
                                    g_03001E60[j].field_3e = (g_03001E60[j].field_3e - 256) & ~0xC000;
                                }
                                if (g_03001E60[i].field_3c < 0) {
                                    if (i != 0) g_03001E60[i].field_3c *= 4;
                                }
                                if (g_03001E60[j].field_3c < 0) {
                                    if (j != 0) g_03001E60[j].field_3c *= 4;
                                }
                                {
                                    s32 speed = g_03001E60[i].field_28;
                                    s32 other = g_03001E60[j].field_28;
                                    g_03001E60[j].field_28 = speed >> 1;
                                    g_03001E60[i].field_28 = other >> 1;
                                }
                                if (!g_030021CC) {
                                    if (i == 0 || j == 0) result = 1;
                                }
                                mask |= g_080202E4[i];
                                if (known) goto next_pair;
                                for (k = 0; k <= 3; k++) {
                                    if (g_03005F90[k] == 0) g_03005F90[k] = i + j * 16;
                                }
                                goto next_pair;
                            }
                            mask |= g_080202E4[i];
                            goto next_pair;
                        }
                    }
                }
next_pair:
                j++;
            } while (j <= 7);
        }
        i++;
    } while (i <= 7);
    if (!mask) {
        for (j = 0; j < 4; j++) g_03005F90[j] = 0;
    }
    return result;
}

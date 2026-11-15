/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
/* Seven roadside marker quads around the next track row: each point is
 * offset along the row heading, projected by 080164D0 and queued by depth.
 * Table indices are written inline (base loads first) and every case ends
 * with its own position add, which cross-jumping merges. Quad layout as in
 * the 08013E74 draft. */
typedef struct DeepQuad { u16 x[4]; s16 y[4]; u8 u[4], v[4]; u16 count, kind; struct DeepQuad *next; } DeepQuad;
extern DeepQuad *g_030021C4, *g_03000670[];
extern u16 g_03001B14;
extern u32 g_03005F50, g_03002E4C;
extern TxraTriple g_030057A0[], g_030055F0[];
extern s32 g_083D2280[], g_083C2280[];
extern void func_080164D0(s32);
void func_080095E4(void)
{
    s32 i, x, z, a, h, depth;
    if (g_03001B14 != 2) return;
    if (g_03005F50 > 2 && g_03005F50 < g_03002E4C - 32) return;
    for (i = 0; i <= 6; i++) {
        switch (i) {
        case 0:
            x = g_083D2280[(g_03006874[1].field_0c + 0x1000) & 0x3FFF] * 768 >> 12;
            z = g_083C2280[(g_03006874[1].field_0c + 0x1000) & 0x3FFF] * 768 >> 12;
            x += g_03006874[1].field_00;
            z += g_03006874[1].field_08;
            break;
        case 1:
            x = g_083D2280[(g_03006874[1].field_0c + 0x1000) & 0x3FFF] * 512 >> 12;
            z = g_083C2280[(g_03006874[1].field_0c + 0x1000) & 0x3FFF] * 512 >> 12;
            x += g_03006874[1].field_00;
            z += g_03006874[1].field_08;
            break;
        case 2:
            x = g_083D2280[(g_03006874[1].field_0c + 0x1000) & 0x3FFF] * 256 >> 12;
            z = g_083C2280[(g_03006874[1].field_0c + 0x1000) & 0x3FFF] * 256 >> 12;
            x += g_03006874[1].field_00;
            z += g_03006874[1].field_08;
            break;
        case 3:
            x = g_03006874[1].field_00;
            z = g_03006874[1].field_08;
            break;
        case 4:
            x = g_083D2280[(g_03006874[1].field_0c + 0x3000) & 0x3FFF] * 256 >> 12;
            z = g_083C2280[(g_03006874[1].field_0c + 0x3000) & 0x3FFF] * 256 >> 12;
            x += g_03006874[1].field_00;
            z += g_03006874[1].field_08;
            break;
        case 5:
            x = g_083D2280[(g_03006874[1].field_0c + 0x3000) & 0x3FFF] * 512 >> 12;
            z = g_083C2280[(g_03006874[1].field_0c + 0x3000) & 0x3FFF] * 512 >> 12;
            x += g_03006874[1].field_00;
            z += g_03006874[1].field_08;
            break;
        case 6:
            x = g_083D2280[(g_03006874[1].field_0c + 0x3000) & 0x3FFF] * 768 >> 12;
            z = g_083C2280[(g_03006874[1].field_0c + 0x3000) & 0x3FFF] * 768 >> 12;
            x += g_03006874[1].field_00;
            z += g_03006874[1].field_08;
            break;
        }
        g_030057A0[0].field_00 = x;
        g_030057A0[0].field_04 = g_03006874[1].field_04 + 64;
        g_030057A0[0].field_08 = z;
        func_080164D0(0);
        g_030057A0[1].field_00 = x;
        g_030057A0[1].field_04 = g_03006874[1].field_04;
        g_030057A0[1].field_08 = z;
        func_080164D0(1);
        h = g_030055F0[1].field_04 - g_030055F0[0].field_04;
        g_030021C4->x[0] = g_030055F0[0].field_00;
        g_030021C4->y[0] = g_030055F0[0].field_04;
        g_030021C4->x[1] = g_030055F0[0].field_00 + (h >> 1);
        g_030021C4->y[1] = g_030055F0[0].field_04;
        g_030021C4->x[2] = g_030055F0[0].field_00 + (h >> 1);
        g_030021C4->y[2] = g_030055F0[1].field_04;
        g_030021C4->x[3] = g_030055F0[0].field_00;
        g_030021C4->y[3] = g_030055F0[1].field_04;
        if ((g_030021C4->x[0] < 120 && g_030021C4->y[0] >= 0 && g_030021C4->y[0] < 160)
         || (g_030021C4->x[1] < 120 && g_030021C4->y[1] >= 0 && g_030021C4->y[1] < 160)
         || (g_030021C4->x[2] < 120 && g_030021C4->y[2] >= 0 && g_030021C4->y[2] < 160)
         || (g_030021C4->x[3] < 120 && g_030021C4->y[3] >= 0 && g_030021C4->y[3] < 160)) {
            g_030021C4->u[0] = 24;
            g_030021C4->v[0] = 0;
            g_030021C4->u[1] = 32;
            g_030021C4->v[1] = 0;
            g_030021C4->u[2] = 32;
            g_030021C4->v[2] = 15;
            g_030021C4->u[3] = 24;
            g_030021C4->v[3] = 15;
            depth = g_030055F0[0].field_08 >> 6;
            depth += 8;
            if (depth >= 0 && depth <= 255) {
                DeepQuad *q = g_030021C4;
                q->count = 8;
                q->kind = 1;
                if (!g_03000670[depth]) {
                    q->next = 0;
                    g_03000670[depth] = q;
                    g_030021C4 = q + 1;
                } else {
                    q->next = g_03000670[depth];
                    g_03000670[depth] = q;
                    g_030021C4 = q + 1;
                }
            }
        }
    }
}

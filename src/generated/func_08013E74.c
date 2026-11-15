/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
/* Three rows of sixteen textured quads, each two pixels wide, whose vertical
 * offsets follow a 32-entry wave table (phase k advances four entries per
 * quad). The texture column cycles through six frames. Each quad is
 * appended to the shared quad list. */
typedef struct WaveQuad {
    u16 x[4];
    s16 y[4];
    u8 u[4], v[4];
    u16 count, kind;
    struct WaveQuad *next;
} WaveQuad;
extern u32 g_03001B1C;
extern s32 g_030021D8;
extern s32 g_08020784[];
extern WaveQuad *g_030021C4, *g_03000670[];
void func_08013E74(void)
{
    s32 row, u, t, y, v, top, rel;
    u32 k;
    y = 44;
    k = g_03001B1C & 31;
    for (row = 0; row <= 2; row++) {
        top = 64;
        if (row == 0) y = -12;
        if (row == 1) y = 44;
        if (row == 2) y = 100;
        u = 0;
        rel = row - 1;
        for (; u <= 31; u += 2) {
            s32 *a, *b;
            WaveQuad *q;
            g_030021C4->x[0] = y;
            a = &g_08020784[k];
            g_030021C4->y[0] = (*a >> 1) + top;
            g_030021C4->x[1] = y + 2;
            b = &g_08020784[(k + 4) & 31];
            g_030021C4->y[1] = (*b >> 1) + top;
            g_030021C4->x[2] = y + 2;
            g_030021C4->y[2] = (*b >> 1) + (39 + top);
            g_030021C4->x[3] = y;
            g_030021C4->y[3] = (*a >> 1) + (39 + top);
            v = 0;
            t = g_030021D8 + rel;
            if (t < 0) t += 6;
            if (t > 5) t -= 6;
            if (t > 2) { v = 40; t -= 3; }
            t *= 36;
            t += u;
            g_030021C4->u[0] = t; g_030021C4->v[0] = v;
            g_030021C4->u[1] = t + 2; g_030021C4->v[1] = v;
            g_030021C4->u[2] = t + 2; g_030021C4->v[2] = v + 39;
            g_030021C4->u[3] = t; g_030021C4->v[3] = v + 39;
            q = g_030021C4;
            q->count = 11;
            q->kind = 3;
            if (!g_03000670[0]) {
                q->next = 0;
                g_03000670[0] = q;
            } else {
                q->next = g_03000670[0];
                g_03000670[0] = q;
            }
            g_030021C4 = q + 1;
            y += 2;
            k = (k + 4) & 31;
        }
    }
}

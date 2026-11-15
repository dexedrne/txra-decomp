/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
/* Track-edge clamp: rotate a record's position into its segment frame,
 * clamp the lateral offset to +/-850 (reflecting the heading off the wall),
 * then rotate back. The reflected angle and (0x1000 - d) reuse one
 * temporary, and 0x1000 - t + 0x1000 stays two statements, as in the ROM. */
extern TxraRecord g_03001E60[];
extern s32 g_083D2280[], g_083C2280[];
extern s16 g_030021CC;
extern s32 func_08014614(s32, s32);
extern void func_0801604C(s32, s32);
void func_0800CEEC(s32 idx)
{
    s32 seg;
    s32 lon;
    s32 angle;
    s32 lat;
    s32 dx;
    s32 dz;
    s32 d;
    s32 t;
    u32 heading;
    seg = g_03001E60[idx].field_38;
    dx = g_03001E60[idx].field_04 - g_03006874[seg].field_00;
    dz = g_03001E60[idx].field_0c - g_03006874[seg].field_08;
    heading = g_03006874[seg].field_0c;
    angle = (0x1000 - heading) & 0x3FFF;
    lat = (dx * g_083D2280[angle] - dz * g_083C2280[angle]) >> 12;
    lon = (dx * g_083C2280[angle] + dz * g_083D2280[angle]) >> 12;
    if (lat < -850 || lat > 850) {
        if (lat < -850) {
            lat = -840;
            t = func_08014614((g_03006874[seg].field_0c + 0x2000) & 0x3FFF, g_03001E60[idx].field_20) & 0x3FFF;
            if (t > 0x1FFF) t -= 0x2000;
            if (t > 0x1000) { t = 0x1000 - t; t += 0x1000; }
            d = t;
            t = 0x1000 - d;
            g_03001E60[idx].field_3c = t / 6 + 256;
            g_03001E60[idx].field_3a = g_03006874[seg].field_0c & 0x3FFF;
            g_03001E60[idx].field_3e = (g_03001E60[idx].field_20 - (d >> 2)) & 0x3FFF;
            g_03001E60[idx].field_30 = 0;
            g_03001E60[idx].field_28 = (g_03001E60[idx].field_28 * d) >> 12;
            if (idx == 0 && g_030021CC == 0) func_0801604C(28, 1);
        }
        if (lat > 850) {
            lat = 840;
            t = func_08014614(g_03006874[seg].field_0c & 0x3FFF, g_03001E60[idx].field_20) & 0x3FFF;
            if (t > 0x1FFF) t -= 0x2000;
            if (t > 0x1000) { t = 0x1000 - t; t += 0x1000; }
            d = t;
            t = 0x1000 - d;
            g_03001E60[idx].field_3c = t / 6 + 256;
            g_03001E60[idx].field_3a = (g_03006874[seg].field_0c + 0x2000) & 0x3FFF;
            g_03001E60[idx].field_3e = (g_03001E60[idx].field_20 + (d >> 2)) & 0x3FFF;
            g_03001E60[idx].field_30 = 0;
            g_03001E60[idx].field_28 = (g_03001E60[idx].field_28 * d) >> 12;
            if (idx == 0 && g_030021CC == 0) func_0801604C(28, 1);
        }
        dx = (lat * g_083D2280[(0x4000 - angle) & 0x3FFF] - lon * g_083C2280[(0x4000 - angle) & 0x3FFF]) >> 12;
        dz = (lat * g_083C2280[(0x4000 - angle) & 0x3FFF] + lon * g_083D2280[(0x4000 - angle) & 0x3FFF]) >> 12;
        g_03001E60[idx].field_04 = dx + g_03006874[seg].field_00;
        g_03001E60[idx].field_0c = dz + g_03006874[seg].field_08;
    }
}

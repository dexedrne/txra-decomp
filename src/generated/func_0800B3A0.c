/* Byte-verified C; address name retained pending semantic review.
 * Point plot into the mode-4 frame. Both parity branches read, mask and
 * store the pixel pair through one function-level variable v, so v is a
 * global pseudo and the odd branch's address and row offset get the
 * original r0/r1 instead of local-alloc's fixed three-quantity order. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern void func_08005F0C(void);
extern u32 g_03005FC0;
extern s16 g_03001E50;
extern s32 g_03002E4C;
extern const s32 g_0804F330[];
void func_0800B3A0(void)
{
    u32 screen;
    s32 mode, xs, zs, shift;
    s32 i;
    u32 v;
    func_08005F0C();
    { u32 flag = g_03005FC0; screen = 0x06000000; if (flag == 0) screen = 0x0600A000; }
    mode = g_03001E50;
    if (mode == 0) { zs = 7200; xs = zs; shift = 1; }
    if (mode == 1) { zs = 5120; xs = zs; shift = 1; }
    if (mode == 2) { xs = 7200; zs = 5120; shift = 0; }
    if (mode == 3) { xs = 8000; zs = 7000; shift = 1; }
    if (mode == 4) { zs = 7000; xs = zs; shift = 4; }
    if (mode == 5) { xs = 6400; zs = 4500; shift = 1; }
    for (i = 0; i < g_03002E4C; i += 8) {
        s32 x, y;
        TxraRow28 *row = (TxraRow28 *)(i * 28 + (u32)g_03006874);
        x = -row->field_00;
        y = row->field_08;
        x = (x * g_0804F330[xs + 0x10000]) >> 19;
        y = (y * g_0804F330[zs + 0x10000]) >> 19;
        x = x + (32 + shift);
        y += 120;
        if ((u32)(x - 1) <= 238 && y > 0 && y <= 159) {
            if (x & 1) {
                v = *((u16 *)screen + (x >> 1) + y * 120); v &= 0xFF; *((u16 *)screen + (x >> 1) + y * 120) = v;
            } else {
                v = *((u16 *)screen + (x >> 1) + y * 120); v &= 0xFF00; *((u16 *)screen + (x >> 1) + y * 120) = v;
            }
        }
    }
}

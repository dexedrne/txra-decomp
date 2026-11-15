/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
/* Transparent 8-bit blit between 256-byte rows at 0x02000000, optionally
 * mirrored. Masks are written in both halves of the source-parity test and
 * the destination row is formed inside each branch so loop.c hoists 1 and 255
 * into the inner preheader; the two writes share one store. */
void func_08008914(s32 x, s32 y, s32 width, s32 height, s32 dx, s32 dy, s32 flip, s32 ox, s32 oy)
{
    s32 sx, sy;
    u16 *p;
    u32 v;
    x += ox;
    y += oy;
    if (!flip) {
        for (sy = y; sy < y + height; sy++) {
            for (sx = x; sx < x + width; sx++) {
                u16 *src = (u16 *)(0x02000000 + (sy << 8));
                u32 pixel = src[sx >> 1];
                if (sx & 1) pixel = (pixel >> 8) & 255;
                else pixel &= 255;
                if (!(dx & 1)) {
                    if (pixel) {
                        u32 dst = (dy << 8) + 0x02000000;
                        p = (u16 *)((dx >> 1) * 2 + dst);
                        v = *p & 0xFF00;
                        goto store;
                    }
                } else {
                    if (pixel) {
                        u32 dst = (dy << 8) + 0x02000000;
                        p = (u16 *)((dx >> 1) * 2 + dst);
                        v = *p & 255;
                        pixel <<= 8;
                    store:
                        *p = v | pixel;
                    }
                }
                dx++;
            }
            dx -= width;
            dy++;
        }
    } else {
        for (sy = y; sy < y + height; sy++) {
            for (sx = x + width - 1; sx >= x; sx--) {
                u16 *src = (u16 *)(0x02000000 + (sy << 8));
                u32 pixel = src[sx >> 1];
                if (sx & 1) pixel = (pixel >> 8) & 255;
                else pixel &= 255;
                if (!(dx & 1)) {
                    if (pixel) {
                        u32 dst = (dy << 8) + 0x02000000;
                        p = (u16 *)((dx >> 1) * 2 + dst);
                        v = *p & 0xFF00;
                        goto store2;
                    }
                } else {
                    if (pixel) {
                        u32 dst = (dy << 8) + 0x02000000;
                        p = (u16 *)((dx >> 1) * 2 + dst);
                        v = *p & 255;
                        pixel <<= 8;
                    store2:
                        *p = v | pixel;
                    }
                }
                dx++;
            }
            dx -= width;
            dy++;
        }
    }
}

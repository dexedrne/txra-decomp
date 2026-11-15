/* Unmatched source hypothesis from deep slice e; excluded from the ROM build. */
void func_08008914(s32 x, s32 y, s32 width, s32 height, s32 dx, s32 dy, s32 flip, s32 ox, s32 oy)
{
    s32 sy, sx;
    x += ox;
    y += oy;
    if (!flip) {
        for (sy = y; sy < y + height; sy++) {
            for (sx = x; sx < x + width; sx++) {
                u16 *src = (u16 *)(0x02000000 + (sy << 8));
                u16 *dst = (u16 *)(0x02000000 + (dy << 8));
                u32 pixel = src[sx >> 1];
                if (sx & 1) pixel >>= 8;
                pixel &= 255;
                if (!(dx & 1)) {
                    if (pixel) dst[dx >> 1] = (dst[dx >> 1] & 0xFF00) | pixel;
                } else {
                    if (pixel) dst[dx >> 1] = (dst[dx >> 1] & 0xFF) | (pixel << 8);
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
                u16 *dst = (u16 *)(0x02000000 + (dy << 8));
                u32 pixel = src[sx >> 1];
                if (sx & 1) pixel >>= 8;
                pixel &= 255;
                if (!(dx & 1)) {
                    if (pixel) dst[dx >> 1] = (dst[dx >> 1] & 0xFF00) | pixel;
                } else {
                    if (pixel) dst[dx >> 1] = (dst[dx >> 1] & 0xFF) | (pixel << 8);
                }
                dx++;
            }
            dx -= width;
            dy++;
        }
    }
}

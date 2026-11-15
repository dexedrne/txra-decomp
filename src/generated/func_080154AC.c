/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
/* Text layout with word wrap: finds the record, measures each line with
 * the font width table, breaks at the last space when the line passes 238
 * pixels, centres it and draws the glyphs. The draw loop has its own index
 * `j` (copied from `start`): with a short live range it outranks the
 * hoisted y+8 and font address and takes r8, and `start` then shares r8.
 * The measure loop is a while (1) with the empty-text exit first, which
 * expand_end_loop rolls to the bottom (two copies of lw = w; end = i). */
extern u32 g_030021D8, g_03002E58, g_030066D4, g_03001B18;
extern s32 g_08021BBC[][160];
extern u8 g_082ADBCC[], g_082B3DCC[], g_082B55CC[];
extern u8 func_080157A0(u32);
extern void func_08015C2C(s32, s32, u8 *);
void func_080154AC(TxraTextRecord *rec)
{
    s32 x, y;
    s32 first;
    u8 *text;
    s32 i, end, state, start, j;
    s32 fixed = 0;
    s32 w, lw;
    u8 c;
    u8 *glyph;
    x = g_030021D8;
    while (x != 0) {
        if (rec->field_08 == 0xFE) x--;
        rec++;
    }
    x = rec->field_00;
    y = rec->field_01;
    first = x;
    if (x == 0xFC) {
        x = 0;
        y = g_030066D4;
    } else if (x == 0xFF) {
        x = g_03002E58;
    } else {
        g_03002E58 = x;
        g_030066D4 = y;
        fixed = 1;
    }
    while (1) {
        text = rec->field_04;
        i = 0;
        end = 0;
        start = 0;
        goto line;
        do {
            if (state == 2) {
                x = 0;
                if (g_03001B18 == 0) y += 16;
                if (g_03001B18 == 1) y += 8;
                if (g_03001B18 == 2) y += 16;
            }
        line:
            w = x;
            lw = 0;
            while (1) {
                if (text[i] == 0) {
                    lw = w;
                    end = i;
                    state = 1;
                    break;
                }
                c = func_080157A0(text[i]);
                if (c == 0) {
                    end = i + 1;
                    lw = w;
                    w = lw + g_08021BBC[g_03001B18][c];
                } else {
                    w += g_08021BBC[g_03001B18][c];
                }
                if (w > 238) {
                    if (first <= 249) {
                        end = i;
                        state = 2;
                        break;
                    }
                    i = end;
                    state = 2;
                    break;
                }
                i++;
            }
            x = 120 - (lw - x) / 2;
            x += g_03002E58;
            if (x < 0) x = 0;
            if (fixed == 1) x = g_03002E58;
            for (j = start; j < end; j++) {
                c = func_080157A0(text[j]);
                if (g_03001B18 == 0) {
                    glyph = g_082ADBCC + c * 256;
                    func_08015C2C(x, y, glyph);
                    func_08015C2C(x + 8, y, glyph + 64);
                    func_08015C2C(x, y + 8, glyph + 128);
                    func_08015C2C(x + 8, y + 8, glyph + 192);
                    x += g_08021BBC[g_03001B18][c];
                }
                if (g_03001B18 == 1) {
                    glyph = g_082B3DCC + c * 64;
                    func_08015C2C(x, y, glyph);
                    x += g_08021BBC[g_03001B18][c];
                }
                if (g_03001B18 == 2) {
                    glyph = g_082B55CC + c * 256;
                    func_08015C2C(x, y, glyph);
                    func_08015C2C(x + 8, y, glyph + 64);
                    func_08015C2C(x, y + 8, glyph + 128);
                    func_08015C2C(x + 8, y + 8, glyph + 192);
                    x += g_08021BBC[g_03001B18][c];
                }
            }
            start = end;
        } while (state != 1);
        if (rec->field_08 != 0xFD) break;
        rec++;
        x = 0;
        if (g_03001B18 == 0) y += 16;
        if (g_03001B18 == 1) y += 8;
        if (g_03001B18 == 2) y += 16;
    }
    g_03002E58 = x;
    g_030066D4 = y;
}

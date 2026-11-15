#include "gba.h"
#include <stdlib.h>
#include <string.h>
#ifdef _WIN32
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#endif
static unsigned voff(u32 a) {
    unsigned o = a & 0x1ffff;
    return o >= 0x18000 ? o - 0x8000 : o;
}
static uint8_t *ptr(GBA *g, u32 a) {
    switch (a >> 24) {
    case 2:
        return &g->ewram[a & 0x3ffff];
    case 3:
        return &g->iwram[a & 0x7fff];
    case 4:
        return &g->io[a & 0x3ff];
    case 5:
        return &g->pal[a & 0x3ff];
    case 6:
        return &g->vram[voff(a)];
    case 7:
        return &g->oam[a & 0x3ff];
    case 8:
    case 9:
    case 10:
    case 11:
    case 12:
        return &g->rom[a & 0x3fffff];
    default:
        return NULL;
    }
}
static unsigned ee_read(GBA *g) {
    if (!g->ee_read)
        return 1;
    unsigned pos = g->ee_out++;
    if (pos < 4)
        return 0;
    if (pos >= 68) {
        g->ee_read = 0;
        return 1;
    }
    unsigned bit = pos - 4, addr = g->ee_read - 1;
    return (g->eeprom[(addr * 8 + (bit >> 3)) & 8191] >> (7 - (bit & 7))) & 1;
}
static void ee_write(GBA *g, unsigned b) {
    if (g->ee_bits < sizeof(g->ee_cmd))
        g->ee_cmd[g->ee_bits++] = b & 1;
    if (!g->ee_len)
        return;
    if (g->ee_bits == g->ee_len) {
        unsigned ab = g->ee_len == 9 || g->ee_len == 73 ? 6 : 14, addr = 0;
        for (unsigned i = 0; i < ab; i++)
            addr = (addr << 1) | g->ee_cmd[2 + i];
        addr &= 1023;
        if (g->ee_cmd[1]) {
            g->ee_read = addr + 1;
            g->ee_out = 0;
        } else {
            for (unsigned i = 0; i < 64; i++) {
                unsigned at = (addr * 8 + i / 8) & 8191, mask = 1u << (7 - (i & 7));
                g->eeprom[at] = (g->eeprom[at] & ~mask) | (g->ee_cmd[2 + ab + i] ? mask : 0);
            }
            g->save_dirty = true;
        }
        g->ee_bits = 0;
        g->ee_len = 0;
    }
}
uint8_t rd8(GBA *g, u32 a) {
    if (g->coverage) coverage_read(g, a);
    if ((a >> 24) == 13)
        return ee_read(g);
    if ((a & 0xfffffff0) == 0x04000100) {
        unsigned i = (a & 15) / 4, o = a & 3;
        if (o < 2)
            return g->timer_value[i] >> (8 * o);
    }
    uint8_t *p = ptr(g, a);
    return p ? *p : 0;
}
uint16_t rd16(GBA *g, u32 a) {
    if ((a >> 24) == 13)
        return ee_read(g);
    u32 v = rd8(g, a & ~1u) | rd8(g, (a & ~1u) + 1) << 8;
    return a & 1 ? (v >> 8) | (v << 8) : v;
}
u32 rd32(GBA *g, u32 a) {
    u32 aligned = a & ~3u, v = rd8(g, aligned) | ((u32)rd8(g, aligned + 1) << 8) |
                               ((u32)rd8(g, aligned + 2) << 16) | ((u32)rd8(g, aligned + 3) << 24);
    unsigned s = (a & 3) * 8;
    return s ? (v >> s) | (v << (32 - s)) : v;
}
static void raw16(GBA *g, unsigned o, unsigned v) {
    g->io[o] = v;
    g->io[o + 1] = v >> 8;
}
void wr8(GBA *g, u32 a, u32 v) {
    unsigned region = a >> 24;
    if (region == 13) {
        ee_write(g, v);
        return;
    }
    if (region >= 8)
        return;
    if (region == 5 || region == 6) {
        if (region == 6 && voff(a) >= 0x10000)
            return;
        uint8_t *p = ptr(g, a & ~1u);
        p[0] = p[1] = v;
        return;
    }
    if (region == 7)
        return;
    if (region == 4) {
        unsigned aligned = a & ~1u, o = a & 0x3fe;
        // Read back the programmed latch, not the timer's moving counter.
        unsigned old = g->io[o] | g->io[o + 1] << 8;
        if ((a & 0x3fe) == 0x202) old = 0; // IF is write-one-to-clear.
        wr16(g, aligned, (a & 1) ? (old & 255) | ((v & 255) << 8)
                                 : (old & 0xff00) | (v & 255));
        return;
    }
    uint8_t *p = ptr(g, a);
    if (p) *p = v;
}
void wr16(GBA *g, u32 a, u32 v) {
    a &= ~1u;
    if ((a >> 24) == 13) {
        ee_write(g, v);
        return;
    }
    if ((a >> 24) >= 8)
        return;
    if ((a >> 24) == 4) {
        unsigned o = a & 0x3ff;
        if (o == 0x202) {
            raw16(g, o, rd16(g, 0x04000202) & ~v);
            return;
        }
        if (o == 0x130 || o == 6)
            return;
        if (o >= 0x100 && o < 0x110) {
            unsigned i = (o - 0x100) / 4;
            if (!(o & 2)) {
                g->timer_reload[i] = v;
                if (!(g->io[(o & ~3) + 2] & 128))
                    g->timer_value[i] = v;
            } else if ((v & 128) && !(g->io[o] & 128)) {
                g->timer_value[i] = g->timer_reload[i];
                g->timer_frac[i] = 0;
            }
        }
        if (o == 0x82) {
            if (v & (1 << 11))
                g->fifo_size[0] = g->fifo_head[0] = 0;
            if (v & (1 << 15))
                g->fifo_size[1] = g->fifo_head[1] = 0;
            v &= ~0x8800;
        }
        if (o == 0x128)
            v &= ~0x80u;
        raw16(g, o, v);
        if ((o >= 0x28 && o <= 0x2e) || (o >= 0x38 && o <= 0x3e)) {
            unsigned bg = (o - 0x28) / 16, base = 0x28 + bg * 16;
            if (o & 4) g->affine_y[bg] = (int32_t)(rd32(g, 0x04000000 + base + 4) << 4) >> 4;
            else g->affine_x[bg] = (int32_t)(rd32(g, 0x04000000 + base) << 4) >> 4;
        }
        if (o >= 0x60 && o <= 0x84)
            sound_write(g, o, v);
        if (o >= 0xba && o <= 0xde && (o - 0xba) % 12 == 0 && (v & 0x8000) && !g->dma_active) {
            unsigned ch = (o - 0xba) / 12;
            g->dma_src[ch] = rd32(g, 0x040000b0 + 12 * ch);
            g->dma_dst[ch] = rd32(g, 0x040000b4 + 12 * ch);
            if (!(v & 0x3000))
                dma_event(g, 0);
        }
        return;
    }
    uint8_t *p = ptr(g, a);
    if (p) {
        p[0] = v;
        p[1] = v >> 8;
    }
}
void wr32(GBA *g, u32 a, u32 v) {
    a &= ~3u;
    if (a == 0x040000a0 || a == 0x040000a4) {
        unsigned i = (a >> 2) & 1;
        for (unsigned b = 0; b < 4; b++)
            if (g->fifo_size[i] < 32) {
                g->fifo[i][(g->fifo_head[i] + g->fifo_size[i]) & 31] = v >> (b * 8);
                g->fifo_size[i]++;
            }
        return;
    }
    wr16(g, a, v & 65535);
    wr16(g, a + 2, v >> 16);
}
void dma_event(GBA *g, unsigned event) {
    if (g->dma_active)
        return;
    g->dma_active = true;
    for (unsigned ch = 0; ch < 4; ch++) {
        unsigned base = 0xb0 + ch * 12, c = rd16(g, 0x04000000 + base + 10), timing = (c >> 12) & 3;
        if (!(c & 0x8000)) continue;
        if (event >= 4) {
            if (timing != 3 || (ch != 1 && ch != 2) ||
                g->dma_dst[ch] != 0x040000a0u + (event - 4) * 4) continue;
        } else if (timing != event) continue;
        u32 n = rd16(g, 0x04000000 + base + 8), src = g->dma_src[ch], dst = g->dma_dst[ch];
        bool fifo = timing == 3 && (ch == 1 || ch == 2);
        if (fifo)
            n = 4;
        if (!n)
            n = ch == 3 ? 65536 : 16384;
        unsigned stride = (c & 0x400) || fifo ? 4 : 2, sm = (c >> 7) & 3, dm = (c >> 5) & 3;
        src &= ~(stride - 1u);
        dst &= ~(stride - 1u);
        if (src >> 24 == 13) {
            g->ee_out = 0;
        }
        if (dst >> 24 == 13) {
            g->ee_len = n;
            g->ee_bits = 0;
        }
        if (g->coverage) {
            u32 low = sm == 1 ? src - (n - 1) * stride : src;
            coverage_transfer(g, 2, low, dst, (sm == 2 ? 1 : n) * stride);
        }
        for (u32 i = 0; i < n; i++) {
            if (stride == 4)
                wr32(g, dst, rd32(g, src));
            else
                wr16(g, dst, rd16(g, src));
            src += sm == 2 ? 0 : sm == 1 ? 0 - stride : stride;
            dst += fifo || dm == 2 ? 0 : dm == 1 ? 0 - stride : stride;
        }
        g->dma_src[ch] = src;
        g->dma_dst[ch] = dm == 3 ? rd32(g, 0x04000000 + base + 4) : dst;
        g->dma_count++;
        if (c & 0x4000)
            raw16(g, 0x202, rd16(g, 0x04000202) | (1u << (8 + ch)));
        if (!(c & 0x200) || !timing)
            raw16(g, base + 10, c & ~0x8000u);
    }
    g->dma_active = false;
}
void eeprom_flush(GBA *g) {
    if (!g->save_dirty || !g->save_path)
        return;
    size_t length = strlen(g->save_path) + 5;
    char *temporary = malloc(length);
    if (!temporary)
        return;
    snprintf(temporary, length, "%s.tmp", g->save_path);
    FILE *f = fopen(temporary, "wb");
    if (f) {
        bool complete = fwrite(g->eeprom, 1, sizeof(g->eeprom), f) == sizeof(g->eeprom);
        if (fclose(f))
            complete = false;
#ifdef _WIN32
        /* C rename cannot replace an existing Windows save. MoveFileEx keeps
         * the old image intact if publishing the completed temporary fails. */
        bool published = complete && MoveFileExA(temporary, g->save_path,
                                                MOVEFILE_REPLACE_EXISTING | MOVEFILE_WRITE_THROUGH);
#else
        bool published = complete && rename(temporary, g->save_path) == 0;
#endif
        if (published) {
            g->save_dirty = false;
            g->save_writes++;
        }
        else
            perror("Save write");
    } else
        perror("Save write");
    free(temporary);
}

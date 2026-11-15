#include "gba.h"
#include <string.h>
/* Timer prescalers are exactly 1, 64, 256 and 1024 guest clocks. Keep
 * quotient/remainder arithmetic unsigned, including the overflow deadline. */
static const unsigned timer_shift[] = {0, 6, 8, 10};
static unsigned io16(GBA *g, unsigned a) {
    return g->io[a] | g->io[a + 1] << 8;
}
static void set16(GBA *g, unsigned a, unsigned v) {
    g->io[a] = v;
    g->io[a + 1] = v >> 8;
}
static void request(GBA *g, unsigned bit) {
    set16(g, 0x202, io16(g, 0x202) | (1u << bit));
}
void irq_check(GBA *g) {
    unsigned pending = io16(g, 0x200) & io16(g, 0x202);
    if (pending)
        g->halted = false;
    if (!pending || !(io16(g, 0x208) & 1) || (g->cpsr & 128) || g->in_irq)
        return;
    g->bank_sp[g->cpsr & 31] = g->r[13];
    g->bank_lr[g->cpsr & 31] = g->r[14];
    for (unsigned i = 0; i < 16; i++)
        g->irq_regs[i] = g->r[i];
    g->irq_cpsr = g->cpsr;
    g->spsr = g->cpsr;
    g->cpsr = (g->cpsr & ~63u) | 0x92;
    g->in_irq = true;
    g->r[13] = g->bank_sp[0x12];
    if (!g->r[13])
        g->r[13] = 0x03007fa0;
    g->r[14] = 0x138;
    g->r[0] = 0x04000000;
    branch(g, rd32(g, 0x03007ffc), false);
}
static void hardware_step(GBA *g, unsigned cycles) {
    g->cycles += cycles;
    bool overflow[4] = {0};
    for (unsigned i = 0; i < 4; i++) {
        unsigned ctrl = io16(g, 0x102 + i * 4);
        if (!(ctrl & 128))
            continue;
        unsigned inc;
        if ((ctrl & 4) && i)
            inc = overflow[i - 1];
        else {
            unsigned shift = timer_shift[ctrl & 3];
            g->timer_frac[i] += cycles;
            inc = g->timer_frac[i] >> shift;
            g->timer_frac[i] &= (1u << shift) - 1;
        }
        g->timer_value[i] += inc;
        if (g->timer_value[i] > 65535) {
            g->timer_value[i] = g->timer_reload[i] + (g->timer_value[i] - 65536);
            overflow[i] = true;
            if (ctrl & 64)
                request(g, 3 + i);
            unsigned sound = io16(g, 0x82);
            for (unsigned f = 0; f < 2; f++)
                if (((sound >> (10 + f * 4)) & 1) == i) {
                    if (g->fifo_size[f]) {
                        g->fifo_sample[f] = g->fifo[f][g->fifo_head[f]];
                        g->fifo_head[f] = (g->fifo_head[f] + 1) & 31;
                        g->fifo_size[f]--;
                    }
                    if (g->fifo_size[f] <= 16)
                        dma_event(g, 4 + f);
                }
        }
    }
    audio_tick(g, cycles);
    unsigned prev = g->line_cycles;
    g->line_cycles += cycles;
    if (prev < 1008 && g->line_cycles >= 1008) {
        if (g->line < 160) {
            scanline(g);
            for (unsigned bg = 0; bg < 2; bg++) {
                g->affine_x[bg] += (int16_t)io16(g, 0x22 + bg * 16);
                g->affine_y[bg] += (int16_t)io16(g, 0x26 + bg * 16);
            }
        }
        unsigned st = io16(g, 4) | 2;
        set16(g, 4, st);
        if (st & 16)
            request(g, 1);
        if (g->line < 160)
            dma_event(g, 2);
    }
    if (g->line_cycles >= 1232) {
        g->line_cycles -= 1232;
        g->line = (g->line + 1) % 228;
        set16(g, 6, g->line);
        if (!g->line) for (unsigned bg = 0; bg < 2; bg++) {
            g->affine_x[bg] = (int32_t)(rd32(g, 0x04000028 + bg * 16) << 4) >> 4;
            g->affine_y[bg] = (int32_t)(rd32(g, 0x0400002c + bg * 16) << 4) >> 4;
        }
        unsigned st = io16(g, 4) & ~7u;
        if (g->line >= 160 && g->line < 227)
            st |= 1;
        if (g->line == (st >> 8))
            st |= 4;
        set16(g, 4, st);
        if ((st & 4) && (st & 32))
            request(g, 2);
        if (g->line == 160) {
            if (st & 8)
                request(g, 0);
            dma_event(g, 1);
            g->frame++;
        }
    }
}
// Split at every observable edge, including timer reloads and the audio sample clock.
// This also makes halted/batched execution equivalent to single-clock stepping.
void hardware_advance(GBA *g, unsigned cycles) {
    while (cycles) {
        unsigned next = g->line_cycles < 1008 ? 1008 : 1232;
        unsigned step = next - g->line_cycles;
        unsigned audio = 512 - g->audio_cycles;
        if (step > audio) step = audio;
        for (unsigned i = 0; i < 4; i++) {
            unsigned ctrl = io16(g, 0x102 + i * 4);
            if (!(ctrl & 128) || (i && (ctrl & 4))) continue;
            unsigned until = ((65536 - g->timer_value[i]) << timer_shift[ctrl & 3]) - g->timer_frac[i];
            if (step > until) step = until;
        }
        if (step > cycles) step = cycles;
        hardware_step(g, step);
        cycles -= step;
    }
}
static unsigned color(GBA *g, unsigned idx) {
    idx &= 511;
    return g->pal[idx * 2] | g->pal[idx * 2 + 1] << 8;
}
static uint32_t rgb(unsigned c) {
    unsigned r = c & 31, gg = (c >> 5) & 31, b = (c >> 10) & 31;
    return 0xff000000u | ((r * 255 / 31) << 16) | ((gg * 255 / 31) << 8) | (b * 255 / 31);
}
static unsigned blend(unsigned a, unsigned b, unsigned x, unsigned y) {
    unsigned v = 0;
    for (unsigned i = 0; i < 3; i++) {
        unsigned c = (((a >> (i * 5)) & 31) * x + ((b >> (i * 5)) & 31) * y) >> 4;
        if (c > 31)
            c = 31;
        v |= c << (i * 5);
    }
    return v;
}
static bool within(unsigned value, unsigned range) {
    unsigned first = range >> 8, last = range & 255;
    return first <= last ? value >= first && value < last : value >= first || value < last;
}
static unsigned window_mask(GBA *g, unsigned x, bool obj) {
    unsigned dc = io16(g, 0);
    if (!(dc & 0xe000)) return 63;
    for (unsigned w = 0; w < 2; w++)
        if ((dc & (0x2000u << w)) && within(x, io16(g, 0x40 + w * 2)) &&
            within(g->line, io16(g, 0x44 + w * 2)))
            return (io16(g, 0x48) >> (w * 8)) & 63;
    return (io16(g, 0x4a) >> ((obj && (dc & 0x8000)) ? 8 : 0)) & 63;
}
void scanline(GBA *g) {
    unsigned line = g->line, dc = io16(g, 0), mode = dc & 7;
    unsigned bg[240], front[240], back[240], kind[240], backkind[240], priority[240];
    bool semi[240], objwin[240] = {0};
    unsigned mask[240];
    for (unsigned x = 0; x < 240; x++) mask[x] = window_mask(g, x, false);
    for (unsigned x = 0; x < 240; x++) {
        bg[x] = color(g, 0);
        front[x] = bg[x];
        kind[x] = 5;
        back[x] = bg[x];
        backkind[x] = 5;
        priority[x] = 4;
        semi[x] = false;
    }
    if (dc & 128) {
        for (unsigned x = 0; x < 240; x++)
            g->pixels[line * 240 + x] = 0xffffffff;
        return;
    }
    if ((dc & 0x400) && (mode >= 3 && mode <= 5)) {
        int16_t pa = io16(g, 0x20), pc = io16(g, 0x24);
        int32_t rx = g->affine_x[0], ry = g->affine_y[0];
        for (unsigned x = 0; x < 240; x++) {
            int sx = (rx + pa * (int)x) >> 8,
                sy = (ry + pc * (int)x) >> 8;
            unsigned w = mode == 5 ? 160 : 240, h = mode == 5 ? 128 : 160;
            if (sx < 0 || sy < 0 || sx >= (int)w || sy >= (int)h)
                continue;
            unsigned page = (mode != 3 && (dc & 16)) ? 0xa000 : 0, idx = sy * w + sx;
            unsigned c;
            if (mode == 4) {
                unsigned p = g->vram[page + idx];
                if (!p)
                    continue;
                c = color(g, p);
            } else {
                idx = page + idx * 2;
                c = g->vram[idx] | g->vram[idx + 1] << 8;
            }
            bg[x] = front[x] = c;
            kind[x] = 2;
            priority[x] = io16(g, 0xc) & 3;
        }
    }
    if (dc & 0x1000) {
        static const unsigned sizes[3][4][2] = {{{8, 8}, {16, 16}, {32, 32}, {64, 64}},
                                                {{16, 8}, {32, 8}, {32, 16}, {64, 32}},
                                                {{8, 16}, {8, 32}, {16, 32}, {32, 64}}};
        // Reverse OAM order gives the lower object index precedence at equal priority.
        for (unsigned pass = 0; pass < 2; pass++) {
        for (int obj = 127; obj >= 0; obj--) {
            unsigned o = obj * 8, a = g->oam[o] | g->oam[o + 1] << 8,
                     b = g->oam[o + 2] | g->oam[o + 3] << 8, c = g->oam[o + 4] | g->oam[o + 5] << 8,
                     shape = a >> 14;
            if (shape == 3 || (!(a & 256) && (a & 512)))
                continue;
            unsigned sw = sizes[shape][b >> 14][0], sh = sizes[shape][b >> 14][1], dw = sw, dh = sh;
            if ((a & 0x300) == 0x300) {
                dw *= 2;
                dh *= 2;
            }
            int oy = a & 255, ox = b & 511;
            if (ox >= 256)
                ox -= 512;
            if (oy >= 160)
                oy -= 256;
            int row = (int)line - oy;
            if (row < 0 || row >= (int)dh)
                continue;
            unsigned objmode = (a >> 10) & 3;
            if (objmode == 3 || (objmode == 2) != (pass == 0)) continue;
            for (unsigned xx = 0; xx < dw; xx++) {
                int screen = ox + xx;
                if (screen < 0 || screen >= 240)
                    continue;
                int tx = xx, ty = row;
                if (a & 256) {
                    unsigned mi = (b >> 9) & 31;
                    int16_t ma = (int16_t)(g->oam[mi * 32 + 6] | g->oam[mi * 32 + 7] << 8),
                            mb = (int16_t)(g->oam[mi * 32 + 14] | g->oam[mi * 32 + 15] << 8),
                            mc = (int16_t)(g->oam[mi * 32 + 22] | g->oam[mi * 32 + 23] << 8),
                            md = (int16_t)(g->oam[mi * 32 + 30] | g->oam[mi * 32 + 31] << 8);
                    tx = ((ma * ((int)xx - (int)dw / 2) + mb * (row - (int)dh / 2)) >> 8) + sw / 2;
                    ty = ((mc * ((int)xx - (int)dw / 2) + md * (row - (int)dh / 2)) >> 8) + sh / 2;
                } else {
                    if (b & 0x1000)
                        tx = sw - 1 - tx;
                    if (b & 0x2000)
                        ty = sh - 1 - ty;
                }
                if (tx < 0 || ty < 0 || tx >= (int)sw || ty >= (int)sh)
                    continue;
                bool eight = a & 0x2000;
                unsigned tile = c & 1023;
                if (eight)
                    tile &= ~1u;
                unsigned stride = (dc & 64) ? (sw / 8) * (eight ? 2 : 1) : 32;
                tile += (ty / 8) * stride + (tx / 8) * (eight ? 2 : 1);
                if (mode >= 3 && tile < 512)
                    continue;
                unsigned address =
                    0x10000 + tile * 32 + (ty & 7) * (eight ? 8 : 4) + (tx & 7) / (eight ? 1 : 2);
                if (address >= 0x18000)
                    continue;
                unsigned idx = g->vram[address];
                if (!eight)
                    idx = (idx >> ((tx & 1) * 4)) & 15;
                if (!idx)
                    continue;
                if (!pass) { objwin[screen] = true; continue; }
                if (!(mask[screen] & 16)) continue;
                unsigned col = color(g, 256 + idx + (eight ? 0 : (c >> 12) * 16)),
                         pri = (c >> 10) & 3;
                if (pri <= priority[screen]) {
                    if (kind[screen] != 4) {
                        back[screen] = front[screen];
                        backkind[screen] = kind[screen];
                    }
                    front[screen] = col;
                    kind[screen] = 4;
                    priority[screen] = pri;
                    semi[screen] = ((a >> 10) & 3) == 1;
                }
            }
        }
        if (!pass) for (unsigned x = 0; x < 240; x++) {
            mask[x] = window_mask(g, x, objwin[x]);
            if (!(mask[x] & (1u << kind[x]))) {
                front[x] = back[x] = color(g, 0);
                kind[x] = backkind[x] = 5;
                priority[x] = 4;
            }
        }
        }
    }
    // Background masks also apply when OBJ rendering is disabled.
    for (unsigned x = 0; x < 240; x++) if (kind[x] != 4 && !(mask[x] & (1u << kind[x]))) {
        front[x] = back[x] = color(g, 0); kind[x] = backkind[x] = 5;
    }
    unsigned bc = io16(g, 0x50), effect = (bc >> 6) & 3, alpha = io16(g, 0x52), eva = alpha & 31,
             evb = (alpha >> 8) & 31, y = io16(g, 0x54) & 31;
    if (eva > 16)
        eva = 16;
    if (evb > 16)
        evb = 16;
    if (y > 16)
        y = 16;
    for (unsigned x = 0; x < 240; x++) {
        unsigned c = front[x];
        if ((mask[x] & 32) && (effect == 1 || semi[x]) && (bc & (1u << (backkind[x] + 8))) &&
            ((bc & (1u << kind[x])) || semi[x]))
            c = blend(c, back[x], eva, evb);
        else if ((mask[x] & 32) && (bc & (1u << kind[x])) && effect >= 2)
            c = blend(c, effect == 2 ? 0x7fff : 0, 16 - y, y);
        g->pixels[line * 240 + x] = rgb(c);
    }
}
void sound_write(GBA *g, unsigned o, unsigned v) {
    if (o == 0x84 && !(v & 128)) {
        for (unsigned i = 0; i < 4; i++)
            g->psg_on[i] = false;
        return;
    }
    static const unsigned control[] = {0x64, 0x6c, 0x74, 0x7c},
                          envelope[] = {0x62, 0x68, 0x72, 0x78};
    for (unsigned i = 0; i < 4; i++)
        if (o == control[i] && (v & 0x8000)) {
            unsigned env = io16(g, envelope[i]);
            g->psg_on[i] = i == 2 ? (io16(g, 0x70) & 128) != 0 : (env & 0xf800) != 0;
            g->psg_length[i] = i == 2 ? 256 - (env & 255) : 64 - (env & 63);
            g->psg_volume[i] = env >> 12;
            g->psg_env[i] = 0;
            g->audio_phase[i] = 0;
            if (i == 3)
                g->noise = 0x7fff;
        }
}
void audio_tick(GBA *g, unsigned cycles) {
    g->audio_cycles += cycles;
    while (g->audio_cycles >= 512) {
        g->audio_cycles -= 512;
        int left = 0, right = 0;
        g->audio_samples++;
        if (io16(g, 0x84) & 128) {
            unsigned routing = io16(g, 0x80), mix = io16(g, 0x82), active = 0;
            static const unsigned control[] = {0x64, 0x6c, 0x74, 0x7c},
                                  envelope[] = {0x62, 0x68, 0x72, 0x78};
            for (unsigned ch = 0; ch < 4; ch++) {
                unsigned env = io16(g, envelope[ch]), ctrl = io16(g, control[ch]);
                if (g->audio_samples % 128 == 0 && g->psg_on[ch] && (ctrl & 0x4000) &&
                    g->psg_length[ch] && !--g->psg_length[ch])
                    g->psg_on[ch] = false;
                if (ch != 2 && g->audio_samples % 512 == 0) {
                    unsigned period = (env >> 8) & 7;
                    if (period && ++g->psg_env[ch] >= period) {
                        g->psg_env[ch] = 0;
                        if ((env & 0x800) && g->psg_volume[ch] < 15)
                            g->psg_volume[ch]++;
                        else if (!(env & 0x800) && g->psg_volume[ch])
                            g->psg_volume[ch]--;
                    }
                }
                if (!g->psg_on[ch])
                    continue;
                active |= 1u << ch;
                float hz;
                int value;
                if (ch < 2) {
                    hz = 131072.0f / (2048 - (ctrl & 2047));
                    g->audio_phase[ch] += hz / 32768.0f;
                    g->audio_phase[ch] -= (int)g->audio_phase[ch];
                    static const float duty[] = {.125f, .25f, .5f, .75f};
                    value = (g->audio_phase[ch] < duty[(env >> 6) & 3] ? 1 : -1) *
                            (int)g->psg_volume[ch] * 80;
                } else if (ch == 2) {
                    hz = 2097152.0f / (2048 - (ctrl & 2047));
                    g->audio_phase[ch] += hz / 32768.0f;
                    unsigned pos = (unsigned)g->audio_phase[ch];
                    g->audio_phase[ch] -= pos & ~31u;
                    pos &= 31;
                    unsigned wave = g->io[0x90 + pos / 2], v = (wave >> ((pos & 1) ? 0 : 4)) & 15,
                             volume = (env >> 13) & 3;
                    value = ((int)v * 2 - 15) * 80;
                    if (env & 0x8000)
                        value = value * 3 / 4;
                    else if (!volume)
                        value = 0;
                    else
                        value >>= volume - 1;
                } else {
                    unsigned div = ctrl & 7, shift = (ctrl >> 4) & 15;
                    hz = 524288.0f / (div ? div : .5f) / (1u << (shift + 1));
                    g->audio_phase[ch] += hz / 32768.0f;
                    while (g->audio_phase[ch] >= 1) {
                        unsigned feedback = (g->noise ^ (g->noise >> 1)) & 1;
                        g->noise = (g->noise >> 1) | (feedback << 14);
                        if (ctrl & 8)
                            g->noise = (g->noise & ~64u) | (feedback << 6);
                        g->audio_phase[ch] -= 1;
                    }
                    value = (g->noise & 1 ? -1 : 1) * (int)g->psg_volume[ch] * 80;
                }
                unsigned ratio = mix & 3;
                value = value * (ratio == 2 ? 4 : ratio == 1 ? 2 : 1) / 4;
                if (routing & (1u << (8 + ch))) right += value * (int)((routing & 7) + 1) / 8;
                if (routing & (1u << (12 + ch))) left += value * (int)(((routing >> 4) & 7) + 1) / 8;
            }
            g->io[0x84] = (g->io[0x84] & 0xf0) | active;
            for (unsigned i = 0; i < 2; i++) {
                int value = g->fifo_sample[i] * ((mix & (4u << i)) ? 48 : 24);
                if (mix & (0x100u << (i * 4))) right += value;
                if (mix & (0x200u << (i * 4))) left += value;
            }
        }
        int stereo[] = {left, right};
        for (unsigned i = 0; i < 2; i++) {
            int sample = stereo[i];
            if (sample > 32767) sample = 32767;
            if (sample < -32768) sample = -32768;
            if (g->audio_len < 4096) g->audio[g->audio_len++] = sample;
            g->audio_hash = (g->audio_hash ^ (uint16_t)sample) * 1099511628211ULL;
        }
    }
}

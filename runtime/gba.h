#ifndef TXRA_GBA_H
#define TXRA_GBA_H
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
typedef uint32_t u32;
typedef struct GBA {
    struct Coverage *coverage;
    u32 r[16], cpsr, spsr, bank_sp[32], bank_lr[32];
    uint8_t rom[0x400000], ewram[0x40000], iwram[0x8000], io[0x400], pal[0x400], vram[0x18000],
        oam[0x400];
    uint8_t eeprom[8192];
    unsigned ee_bits, ee_len, ee_out, ee_read;
    uint8_t ee_cmd[128];
    bool save_dirty;
    uint64_t cycles, instructions, compiled_steps, fallback_steps;
    unsigned line_cycles, frame, line;
    int quota;
    bool stopped, in_irq, halted, trace;
    u32 irq_regs[16], irq_cpsr;
    unsigned unknown_count, unsupported;
    u32 timer_reload[4], timer_value[4], timer_frac[4];
    u32 dma_src[4], dma_dst[4];
    bool dma_active;
    unsigned dma_count;
    int32_t affine_x[2], affine_y[2];
    uint32_t pixels[240 * 160];
    FILE *unknown;
    const char *save_path;
    int8_t fifo[2][32];
    unsigned fifo_size[2], fifo_head[2];
    int8_t fifo_sample[2];
    float audio_phase[4];
    uint32_t noise;
    bool psg_on[4];
    unsigned psg_length[4], psg_volume[4], psg_env[4], audio_samples;
    int16_t audio[4096];
    unsigned audio_len, audio_cycles;
    uint64_t audio_hash;
    unsigned save_writes;
} GBA;
bool coverage_start(GBA *);
void coverage_pc(GBA *);
void coverage_bios_source(GBA *, unsigned);
void coverage_branch(GBA *, u32, bool);
void coverage_read(GBA *, u32);
void coverage_transfer(GBA *, unsigned, u32, u32, u32);
bool coverage_finish(GBA *, const char *);
uint8_t rd8(GBA *, u32);
uint16_t rd16(GBA *, u32);
u32 rd32(GBA *, u32);
void wr8(GBA *, u32, u32);
void wr16(GBA *, u32, u32);
void wr32(GBA *, u32, u32);
void branch(GBA *, u32, bool);
void bios(GBA *, unsigned);
bool tick(GBA *);
void arm_dp(GBA *, unsigned, unsigned, unsigned, unsigned, unsigned, u32, unsigned, unsigned);
void arm_mem(GBA *, unsigned, unsigned, unsigned, unsigned, unsigned, unsigned, u32, unsigned,
             unsigned);
void arm_half(GBA *, unsigned, unsigned, unsigned, unsigned, unsigned, unsigned, unsigned, u32,
              unsigned);
void arm_block(GBA *, unsigned, unsigned, unsigned, unsigned, unsigned, unsigned, unsigned);
void arm_mul(GBA *, unsigned, unsigned, unsigned, unsigned, unsigned, unsigned, unsigned, unsigned);
void arm_status(GBA *, unsigned, unsigned, unsigned, u32);
void thumb(GBA *, unsigned, unsigned, unsigned, unsigned, int);
void fallback(GBA *);
void dispatch(GBA *);
bool generated_dispatch(GBA *);
void hardware_advance(GBA *, unsigned);
void scanline(GBA *);
void irq_check(GBA *);
void sound_write(GBA *, unsigned, unsigned);
void dma_event(GBA *, unsigned);
void audio_tick(GBA *, unsigned);
void eeprom_flush(GBA *);
extern const unsigned recompiled_function_count;
extern const u32 recompiled_rom_crc;
static inline u32 reg(GBA *g, unsigned n) {
    return n == 15 ? g->r[15] + ((g->cpsr & 32) ? 4 : 8) : g->r[n];
}
static inline bool cond(GBA *g, unsigned c) {
    unsigned n = g->cpsr >> 31, z = (g->cpsr >> 30) & 1, v = (g->cpsr >> 28) & 1,
             k = (g->cpsr >> 29) & 1;
    switch (c) {
    case 0:
        return z;
    case 1:
        return !z;
    case 2:
        return k;
    case 3:
        return !k;
    case 4:
        return n;
    case 5:
        return !n;
    case 6:
        return v;
    case 7:
        return !v;
    case 8:
        return k && !z;
    case 9:
        return !k || z;
    case 10:
        return n == v;
    case 11:
        return n != v;
    case 12:
        return !z && n == v;
    case 13:
        return z || n != v;
    case 14:
        return true;
    default:
        return false;
    }
}
#endif

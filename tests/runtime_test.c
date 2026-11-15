#include "gba.h"
#include <assert.h>
#include <stdlib.h>
#include <string.h>
static unsigned tests;
#define CHECK(x)                                                                                   \
    do {                                                                                           \
        assert(x);                                                                                 \
        tests++;                                                                                   \
    } while (0)
bool generated_dispatch(GBA *g) {
    (void)g;
    return false;
}
const unsigned recompiled_function_count = 0;
int main(void) {
    GBA *g = calloc(1, sizeof(*g));
    g->cpsr = 0x1f;
    g->r[15] = 0x08000000;
    g->r[0] = 0xffffffff;
    g->r[1] = 1;
    arm_dp(g, 0, 4, 1, 0, 2, 1, 0, 0);
    CHECK(g->r[2] == 0);
    CHECK((g->cpsr & 0xf0000000) == 0x60000000);
    g->r[0] = 0x7fffffff;
    arm_dp(g, 0, 4, 1, 0, 2, 1, 0, 0);
    CHECK(g->r[2] == 0x80000000);
    CHECK((g->cpsr & 0xf0000000) == 0x90000000);
    g->r[0] = 0;
    arm_dp(g, 0, 2, 1, 0, 2, 1, 0, 0);
    CHECK(g->r[2] == 0xffffffff);
    CHECK(!(g->cpsr & 0x20000000));
    g->r[0] = 0x80000001;
    g->r[1] = 32;
    thumb(g, 2, 2, 1, 0, 0);
    CHECK(g->r[0] == 0);
    CHECK(g->cpsr & 0x20000000);
    g->r[0] = 0x80000001;
    g->r[1] = 40;
    thumb(g, 2, 4, 1, 0, 0);
    CHECK(g->r[0] == 0xffffffff);
    g->r[0] = 0x80000001;
    g->r[1] = 32;
    thumb(g, 2, 7, 1, 0, 0);
    CHECK(g->r[0] == 0x80000001);
    CHECK(g->cpsr & 0x20000000);
    wr32(g, 0x02000000, 0x12345678);
    CHECK(rd32(g, 0x02000001) == 0x78123456);
    CHECK(rd32(g, 0x02040000) == 0x12345678);
    wr8(g, 0x06000001, 0x33);
    CHECK(rd16(g, 0x06000000) == 0x3333);
    wr8(g, 0x07000000, 77);
    CHECK(rd16(g, 0x07000000) == 0);
    wr32(g, 0x040000d4, 0x02000000);
    wr32(g, 0x040000d8, 0x03000000);
    wr32(g, 0x040000dc, 0x84000001);
    CHECK(rd32(g, 0x03000000) == 0x12345678);
    CHECK(!(rd16(g, 0x040000de) & 0x8000));
    wr16(g, 0x04000100, 0xfffe);
    wr16(g, 0x04000102, 0x00c0);
    hardware_advance(g, 2);
    CHECK(rd16(g, 0x04000100) == 0xfffe);
    CHECK(rd16(g, 0x04000202) & 8);
    wr16(g, 0x04000202, 8);
    CHECK(!(rd16(g, 0x04000202) & 8));
    g->r[0] = 0x02000000;
    g->r[1] = 0x02000100;
    g->r[2] = 0x05000004;
    bios(g, 0xb);
    CHECK(rd32(g, 0x0200010c) == 0x12345678);
    g->r[0] = 0xfffffff9;
    g->r[1] = 3;
    bios(g, 6);
    CHECK(g->r[0] == 0xfffffffe);
    CHECK(g->r[1] == 0xffffffff);
    g->r[0] = 65536;
    bios(g, 8);
    CHECK(g->r[0] == 256);
    // Execute the actual fallback decoder, including THUMB BL state and PC pipeline.
    g->r[15] = 0x02000200;
    g->cpsr = 0x3f;
    wr16(g, 0x02000200, 0x2007);
    g->quota = 10;
    fallback(g);
    CHECK(g->r[0] == 7 && g->r[15] == 0x02000202);
    wr16(g, 0x02000202, 0xf000);
    wr16(g, 0x02000204, 0xf801);
    fallback(g);
    fallback(g);
    CHECK(g->r[15] == 0x02000208 && g->r[14] == 0x02000207);
    // Mode 4 palette scanout at identity affine matrix.
    memset(g->io, 0, sizeof(g->io));
    wr16(g, 0x04000000, 0x0404);
    wr16(g, 0x04000020, 256);
    wr16(g, 0x04000026, 256);
    wr16(g, 0x05000002, 31);
    wr16(g, 0x06000000, 0x0101);
    g->line = 0;
    scanline(g);
    CHECK(g->pixels[0] == 0xffff0000);
    // EEPROM DMA serial write/read round trip, six address bits, eight data bytes.
    memset(g->eeprom, 255, sizeof(g->eeprom));
    u32 ad = 0x02001000;
    unsigned bits[73] = {1, 0};
    for (unsigned i = 0; i < 64; i++)
        bits[8 + i] = (0xa5 >> (7 - (i & 7))) & 1;
    for (unsigned i = 0; i < 73; i++)
        wr16(g, ad + i * 2, bits[i]);
    wr32(g, 0x040000d4, ad);
    wr32(g, 0x040000d8, 0x0d000000);
    wr32(g, 0x040000dc, 0x80400049);
    CHECK(g->eeprom[0] == 0xa5 && g->eeprom[7] == 0xa5);
    unsigned cmd[9] = {1, 1};
    for (unsigned i = 0; i < 9; i++)
        wr16(g, ad + i * 2, cmd[i]);
    wr32(g, 0x040000d4, ad);
    wr32(g, 0x040000d8, 0x0d000000);
    wr32(g, 0x040000dc, 0x80400009);
    for (unsigned i = 0; i < 4; i++)
        CHECK(rd16(g, 0x0d000000) == 0);
    u32 data = 0;
    for (unsigned i = 0; i < 8; i++)
        data = (data << 1) | rd16(g, 0x0d000000);
    CHECK(data == 0xa5);
    g->save_path = "build/test-eeprom.sav";
    eeprom_flush(g);
    FILE *saved = fopen(g->save_path, "rb");
    CHECK(saved != NULL);
    uint8_t persisted[8192];
    size_t loaded = fread(persisted, 1, sizeof(persisted), saved);
    fclose(saved);
    CHECK(loaded == sizeof(persisted) && persisted[0] == 0xa5 && persisted[7] == 0xa5 &&
          !g->save_dirty);
    // Repeated IRQ bank switches must restore the top of the IRQ stack each time.
    memset(g->io, 0, sizeof(g->io));
    g->cpsr = 0x1f;
    g->r[13] = 0x03007f00;
    g->r[15] = 0x08000100;
    g->bank_sp[0x12] = 0x03007fa0;
    wr32(g, 0x03007ffc, 0x03000100);
    wr16(g, 0x04000200, 1);
    wr16(g, 0x04000208, 1);
    g->io[0x202] = 1;
    for (unsigned i = 0; i < 32; i++) {
        irq_check(g);
        CHECK(g->in_irq);
        arm_block(g, 1, 0, 0, 1, 0, 13, 0x4001);
        arm_status(g, 1, 0, 1, 0x1001f);
        arm_status(g, 1, 0, 1, 0x10092);
        arm_block(g, 0, 1, 0, 1, 1, 13, 0x4001);
        g->r[15] = 0x138;
        dispatch(g);
        CHECK(g->bank_sp[0x12] == 0x03007fa0 && g->r[13] == 0x03007f00 && g->r[15] == 0x08000100);
    }
    // DMA masks address alignment instead of applying CPU unaligned rotations.
    wr32(g, 0x02002000, 0x87654321);
    wr32(g, 0x040000d4, 0x02002001);
    wr32(g, 0x040000d8, 0x03002003);
    wr32(g, 0x040000dc, 0x84000001);
    CHECK(rd32(g, 0x03002000) == 0x87654321);
    // Batched timing must match clock-at-a-time operation, including cascades.
    GBA *a = calloc(1, sizeof(*a)), *b = calloc(1, sizeof(*b));
    wr16(a, 0x04000100, 0xfffd); wr16(a, 0x04000102, 0xc0);
    wr16(a, 0x04000104, 0xfffc); wr16(a, 0x04000106, 0xc4);
    memcpy(b, a, sizeof(*a));
    hardware_advance(a, 280896 * 3 + 987);
    for (unsigned i = 0; i < 280896 * 3 + 987; i++) hardware_advance(b, 1);
    CHECK(a->cycles == b->cycles && a->frame == b->frame && a->line == b->line);
    CHECK(a->line_cycles == b->line_cycles && !memcmp(a->io, b->io, sizeof(a->io)));
    CHECK(!memcmp(a->timer_value, b->timer_value, sizeof(a->timer_value)));
    CHECK(a->audio_samples == a->cycles / 512 && a->audio_hash == b->audio_hash);
    CHECK(a->line == 0 && a->line_cycles == 987 && a->frame == 3);
    free(a); free(b);
    // Every prescaler: exact quotient/remainder at partial and overflow edges.
    // Expected values deliberately use division, independently of the runtime.
    static const unsigned scales[] = {1, 64, 256, 1024};
    a = calloc(1, sizeof(*a)); b = calloc(1, sizeof(*b));
    for (unsigned prescale = 0; prescale < 4; prescale++) {
        unsigned scale = scales[prescale];
        unsigned elapsed[] = {0, 1, scale - 1, scale, scale + 1,
                              3 * scale - 1, 3 * scale, 7 * scale + 1};
        for (unsigned edge = 0; edge < sizeof(elapsed) / sizeof(*elapsed); edge++) {
            memset(a, 0, sizeof(*a));
            // All four independent timers, plus FIFO and IRQ side effects.
            for (unsigned timer = 0; timer < 4; timer++) {
                wr16(a, 0x04000100 + timer * 4, 0xfffd);
                wr16(a, 0x04000102 + timer * 4, 0xc0 | prescale);
            }
            memcpy(b, a, sizeof(*a));
            hardware_advance(a, elapsed[edge]);
            for (unsigned cycle = 0; cycle < elapsed[edge]; cycle++)
                hardware_advance(b, 1);
            CHECK(!memcmp(a, b, sizeof(*a)));
            for (unsigned timer = 0; timer < 4; timer++) {
                CHECK(a->timer_frac[timer] == elapsed[edge] % scale);
                CHECK(a->timer_value[timer] == 0xfffd + (elapsed[edge] / scale) % 3);
            }
            CHECK((rd16(a, 0x04000202) & 0x78) ==
                  (elapsed[edge] / scale >= 3 ? 0x78 : 0));
        }
        // Prescaled source with three cascades; cross scanline/sample edges,
        // then change the prescaler while enabled (fraction is retained).
        memset(a, 0, sizeof(*a));
        wr16(a, 0x04000100, 0xfffd);
        wr16(a, 0x04000102, 0xc0 | prescale);
        for (unsigned timer = 1; timer < 4; timer++) {
            wr16(a, 0x04000100 + timer * 4, 0xfffe);
            wr16(a, 0x04000102 + timer * 4, 0xc4);
        }
        memcpy(b, a, sizeof(*a));
        hardware_advance(a, 29 * scale + 13);
        for (unsigned cycle = 0; cycle < 29 * scale + 13; cycle++) hardware_advance(b, 1);
        CHECK(!memcmp(a, b, sizeof(*a)));
        unsigned next_prescale = prescale < 3 ? prescale + 1 : prescale;
        wr16(a, 0x04000102, 0xc0 | next_prescale);
        wr16(b, 0x04000102, 0xc0 | next_prescale);
        hardware_advance(a, 1233);
        for (unsigned cycle = 0; cycle < 1233; cycle++) hardware_advance(b, 1);
        CHECK(!memcmp(a, b, sizeof(*a)));
    }
    free(a); free(b);
    // A FIFO request must not also refill the other FIFO's DMA channel.
    memset(g, 0, sizeof(*g));
    wr32(g, 0x02000000, 0x12345678);
    wr32(g, 0x040000bc, 0x02000000); wr32(g, 0x040000c0, 0x040000a0);
    wr32(g, 0x040000c4, 0xb6400000);
    wr32(g, 0x040000c8, 0x02000000); wr32(g, 0x040000cc, 0x040000a4);
    wr32(g, 0x040000d0, 0xb6400000);
    dma_event(g, 4);
    CHECK(g->fifo_size[0] == 16 && g->fifo_size[1] == 0);
    dma_event(g, 5);
    CHECK(g->fifo_size[0] == 16 && g->fifo_size[1] == 16);
    // DirectSound is independently routed to the left and right speakers.
    wr16(g, 0x04000084, 128); wr16(g, 0x04000082, 0x0204);
    g->fifo_sample[0] = 100; audio_tick(g, 512);
    CHECK(g->audio_len == 2 && g->audio[0] == 4800 && g->audio[1] == 0);
    // Negative PSG samples must remain signed when applying speaker gains.
    memset(g, 0, sizeof(*g));
    wr16(g, 0x04000084, 128); wr16(g, 0x04000080, 0x0107);
    wr16(g, 0x04000082, 2); wr16(g, 0x04000062, 0xf000);
    wr16(g, 0x04000064, 0x8000); g->audio_phase[0] = .5f;
    audio_tick(g, 512);
    CHECK(g->audio[0] == 0 && g->audio[1] == -1200);
    // Byte writes must trigger the same timer and sound side effects as halfwords.
    wr16(g, 0x04000100, 0xfffe); wr8(g, 0x04000102, 128);
    CHECK(g->timer_value[0] == 0xfffe);
    g->timer_reload[0] = 0xabcd; g->timer_value[0] = 0x1234;
    g->io[0x100] = 0xcd; g->io[0x101] = 0xab;
    wr8(g, 0x04000100, 0xef);
    CHECK(g->timer_reload[0] == 0xabef && g->timer_value[0] == 0x1234);
    // Window masks crop BG2, and suppress brightness outside the window.
    memset(g, 0, sizeof(*g));
    wr16(g, 0x04000000, 0x2404); wr16(g, 0x04000020, 256);
    wr16(g, 0x04000026, 256); wr16(g, 0x05000002, 31);
    memset(g->vram, 1, 240);
    wr16(g, 0x04000040, 0x0a14); wr16(g, 0x04000044, 0x0001);
    wr16(g, 0x04000048, 4); wr16(g, 0x0400004a, 0);
    scanline(g);
    CHECK(g->pixels[9] == 0xff000000 && g->pixels[10] == 0xffff0000);
    CHECK(g->pixels[19] == 0xffff0000 && g->pixels[20] == 0xff000000);
    wr16(g, 0x04000040, 0xf00a); scanline(g);
    CHECK(g->pixels[0] == 0xffff0000 && g->pixels[10] == 0xff000000);
    // Affine reference writes latch a signed 28-bit value immediately.
    wr32(g, 0x04000028, 0x0fffff00);
    CHECK(g->affine_x[0] == -256);
    wr32(g, 0x04000028, 0); wr16(g, 0x04000022, 256);
    hardware_advance(g, 1008);
    CHECK(g->affine_x[0] == 256);
    // Object windows must reveal BG2 before the normal object pass.
    memset(g, 0, sizeof(*g));
    wr16(g, 0x04000000, 0x9404); wr16(g, 0x04000020, 256);
    wr16(g, 0x05000002, 31); memset(g->vram, 1, 240);
    memset(g->vram + 0x14000, 0x11, 32);
    wr16(g, 0x07000000, 0x0800); wr16(g, 0x07000004, 512);
    wr16(g, 0x0400004a, 0x0400); scanline(g);
    CHECK(g->pixels[0] == 0xffff0000 && g->pixels[8] == 0xff000000);
    // Only the top OBJ participates in compositing; a hidden OBJ is not the second layer.
    wr16(g, 0x04000000, 0x1404); wr16(g, 0x07000000, 0x0400);
    wr16(g, 0x05000202, 0x7c00); wr16(g, 0x05000204, 0x03e0);
    wr16(g, 0x07000008, 0x0400); wr16(g, 0x0700000c, 513);
    memset(g->vram + 0x14020, 0x22, 32);
    wr16(g, 0x04000050, 0x0450); wr16(g, 0x04000052, 0x0808);
    scanline(g);
    CHECK(g->pixels[0] == 0xff7b007b);
    printf("%u runtime assertions passed\n", tests);
    free(g);
    return 0;
}

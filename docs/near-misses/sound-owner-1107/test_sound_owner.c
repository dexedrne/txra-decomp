#define _GNU_SOURCE
#include <assert.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
#include "func_080064A4.c"

FadeLevels g_0801FF00 = {{0, 32, 64, 96, 128, 160, 192, 224, 256}};
SoundSequence g_03007590[4];
SoundVoice g_03007770[8];
s32 g_030079B4, g_03007400, g_030079B0, g_03007570, g_03006A98;
u32 g_03007574, g_03007404, g_03007578, g_030079C0;
u32 *g_03007580;
s8 g_03007410[352];
u32 g_083C19C0[8];
u8 g_083C100D[256], g_083C0FAC[256];
/* The linker names the second word g_08333324; rest-note index -1 is real. */
s32 test_steps[258];
SoundSample g_083B8698[8];
static unsigned callbacks[2], fade_stops;
static unsigned char *arena;
static size_t used;
static void callback_a(s32 n) { assert(n == 4); callbacks[0]++; }
static void callback_b(s32 n) { assert(n == 0 || n == 1); callbacks[1]++; }
void (*g_08332E9C)(s32) = callback_a, (*g_08332EA0)(s32) = callback_b;
void func_08005F8C(s32 n) { assert(n == 0); fade_stops++; }
static u32 put(const void *data, size_t size) {
    u32 address;
    used = (used + 3) & ~(size_t)3;
    assert(used + size < 65536);
    memcpy(arena + used, data, size);
    address = (u32)(uintptr_t)(arena + used);
    assert((uintptr_t)(arena + used) == address);
    used += size;
    return address;
}
static u32 words(const u32 *data, size_t count) { return put(data, count * sizeof(*data)); }
static u32 shorts(const s16 *data, size_t count) { return put(data, count * sizeof(*data)); }
static void reset(void) {
    unsigned i;
    memset(g_03007770, 0, sizeof(g_03007770));
    memset(g_03007590, 0, sizeof(g_03007590));
    memset((void *)(uintptr_t)0x04000000, 0, 4096);
    memset(callbacks, 0, sizeof(callbacks));
    memset(g_03007410, 0, sizeof(g_03007410));
    g_030079B4 = g_03007400 = g_03007570 = g_03006A98 = 0;
    g_03007574 = 0; g_03007404 = 256; g_030079B0 = 7;
    g_03007578 = g_030079C0 = fade_stops = 0; used = 0;
    for (i = 0; i < 256; i++) { g_083C100D[i] = i + 1; g_083C0FAC[i] = i * 3; }
    for (i = 0; i < 258; i++) test_steps[i] = 1000 + i;
    for (i = 0; i < 8; i++) {
        SoundInstrument instrument = {1, 0x12, 0x34, 0, 0, 0, 0, 0, 0};
        g_083C19C0[i] = put(&instrument, sizeof(instrument));
        g_083B8698[i].length = 100 + i;
    }
    { const u32 durations[] = {1, 2, 3, 4}; g_03007580 = ADDRESS(u32, words(durations, 4)); }
}
static u32 pitch(unsigned note) { return ((u32)g_083C100D[note] << 8) | g_083C0FAC[note]; }
static void start(unsigned index, u32 commands) {
    g_03007770[index].enabled = g_03007770[index].output = 1;
    g_03007770[index].commands = commands;
}
static void test_gate_and_prefix(void) {
    reset(); g_03007404 = 0; g_03007574 = 255;
    start(4, words((u32[]){0x61}, 1)); g_03007770[4].pitch_cursor = 20;
    func_080064A4(); assert(g_03007770[4].pitch_cursor == 20);
    assert(callbacks[0] == 1 && callbacks[1] == 2);
    g_03007404 = 1; func_080064A4(); assert(g_03007574 == 0); assert(g_03007770[4].pitch_cursor == -1);
    /* The fixed-point gate consumes only one tick even if its sum exceeds 511. */
    g_03007574 = 512; g_03007404 = 0; func_080064A4(); assert(g_03007574 == 256);
    reset(); g_03007570 = 1; memset(g_03007410, 0x35, sizeof(g_03007410));
    func_080064A4(); for (unsigned i = 0; i < 176; i++) assert(g_03007410[176+i] == 0);
    assert(g_03007410[0] == 0x35 && callbacks[0] == 0 && callbacks[1] == 2);
    reset(); g_030079B4 = 1; g_03007400 = 15; g_030079B0 = 1;
    SOUND_REG(0x04000080) = 0xabff; func_080064A4();
    assert(fade_stops == 1 && g_030079B4 == 0 && g_030079B0 == 7);
    assert(SOUND_REG(0x04000080) == 0xab00);
}
static void test_commands_and_pcm(void) {
    reset();
    u32 events = put((u8[]){50, 2, 1, 0x65}, 4);
    u32 commands = words((u32[]){0x67, 3, 0x69, 128, 0x66, 9, 0x60, 99, 88,
                                     0x62, 11, 0x64, events, 2, 1, 0x61}, 16);
    start(4, commands); func_080064A4();
    SoundVoice *v = &g_03007770[4];
    assert(g_03007578 == (3u << 8) + 7u * 17 && SOUND_REG(0x04000080) == g_03007578);
    assert(g_03007404 == 128 && g_030079C0 == 9);
    assert(v->command == 15 && v->note == 52 && v->instrument == 2 && v->delay == 2 && v->cursor == 3);
    assert(v->pitch == (s32)pitch(52));
    assert(v->arpeggio_cursor == g_08333324[95-52]);
    assert(v->pitch_delay == (102-4)*16384 && v->pitch_cursor == 0 && v->volume_delay == 1);
    /* Delay countdown does not consume another note until it reaches zero. */
    g_03007404 = 256; func_080064A4(); assert(v->delay == 1 && v->cursor == 3);
    func_080064A4(); assert(v->events == 0 && v->pitch_cursor == -1 && v->command == 15);
    /* The output-disabled stop and channels 6/7 preserve the sample position. */
    for (unsigned n = 4; n < 8; n++) {
        reset(); start(n, words((u32[]){0x61}, 1));
        g_03007770[n].pitch_cursor = 123;
        if (n == 4) g_03007770[n].output = 0;
        func_080064A4(); assert(g_03007770[n].pitch_cursor == (n == 5 ? -1 : 123));
    }
    /* Rest uses note 96 for 4/5, note 48 for 6/7; unsigned sample index gate. */
    for (unsigned n = 4; n < 8; n++) {
        reset(); events = put((u8[]){0x60, 0, 0}, 3);
        start(n, words((u32[]){0x64, events, 200, 1, 0x61}, 5)); func_080064A4();
        assert(g_03007770[n].note == (n < 6 ? 96 : 48));
        assert(g_03007770[n].pitch_cursor == (n < 6 ? -1 : 0));
    }
}
static void test_repeat_chaining_and_wrap(void) {
    reset();
    u32 a = put((u8[]){255, 0, 0, 0x65}, 4), b = put((u8[]){64, 1, 0, 0x65}, 4);
    start(7, words((u32[]){0x64, a, 2, 2, 0x64, b, 1, 1, 0x61}, 9));
    func_080064A4(); assert(g_03007770[7].note == 1); /* byte truncation */
    func_080064A4(); assert(g_03007770[7].note == 1 && g_03007770[7].repeats == 1);
    func_080064A4(); assert(g_03007770[7].note == 65 && g_03007770[7].command == 8);
    assert(g_03007770[7].cursor == 3); /* note 65 is not a byte-stream marker */
    reset(); g_03007574 = 0xffffffff; g_03007404 = 1;
    start(4, words((u32[]){0x61}, 1)); g_03007770[4].pitch_cursor = 1;
    func_080064A4(); assert(g_03007574 == 0 && g_03007770[4].pitch_cursor == 1);
}
static void test_envelopes(void) {
    reset();
    SoundVoice *v = &g_03007770[0];
    SoundInstrument *ins = ADDRESS(SoundInstrument, g_083C19C0[0]);
    u32 arp = shorts((s16[]){7, 0, 254, 4, 2, -1, 255, 0}, 8);
    u32 slide = shorts((s16[]){0, 1, -2, 3, 255, 0}, 6);
    u32 volume = shorts((s16[]){1, 1, 254, 4, 9, 5, 255, 0}, 8);
    ins->arpeggio = arp; ins->slide = slide; ins->volume = volume;
    start(0, words((u32[]){0x61}, 1)); v->events = put((u8[]){40, 0, 0}, 3);
    v->delay = 3; v->note = 40; v->pitch = 600; v->arpeggio_delay = v->pitch_delay = v->volume_delay = 1;
    v->output = 1; /* This fixture exercises enabled continuation envelopes. */
    func_080064A4();
    /* Independent scalar reference: jump arp to index4 -> note39, then signed -2 slide. */
    assert(v->pitch == (s32)pitch(39)-2 && v->arpeggio_delay == 2 && v->arpeggio_cursor == 4);
    assert(v->pitch_delay == 3 && v->volume_delay == 5 && v->volume_cursor == 4);
    assert(SOUND_REG(0x04000062) == 0x0912);
    assert(SOUND_REG(0x04000064) == (u16)((pitch(39)-2) | 0x8100));
    v->arpeggio_delay = v->pitch_delay = v->volume_delay = 1;
    v->delay = 3; func_080064A4();
    assert(v->arpeggio_cursor == 4 && v->pitch_cursor == 2 && v->volume_cursor == 4); /* 255 holds */
    reset(); v = &g_03007770[3]; ins = ADDRESS(SoundInstrument, g_083C19C0[0]);
    ins->slide = shorts((s16[]){2, 1, 254, 6}, 4);
    ins->volume = shorts((s16[]){2, 1, 255, 0}, 4);
    start(3, words((u32[]){0x61}, 1)); v->events = put((u8[]){40, 0, 0}, 3);
    v->delay = 2; v->pitch_delay = v->volume_delay = 1;
    func_080064A4();
    assert(v->pitch_cursor == 2 && v->pitch_delay == 6); /* Noise treats254 as data, not jump. */
    assert(SOUND_REG(0x0400007C) == 0x1fe && v->volume_cursor == 0);
}
static void test_output_gate(void) {
    for (unsigned n = 0; n < 4; n++) for (int delay = 1; delay <= 2; delay++) {
        reset(); SoundVoice *v = &g_03007770[n];
        SoundInstrument *ins = ADDRESS(SoundInstrument, g_083C19C0[0]);
        ins->arpeggio = shorts((s16[]){7, 0, 2, -1}, 4);
        ins->slide = shorts((s16[]){0, 1, -2, 3}, 4);
        ins->volume = shorts((s16[]){1, 1, 9, 5}, 4);
        start(n, words((u32[]){0x66, 77, 0x61}, 3));
        v->output = 0; v->delay = delay; v->note = 40; v->pitch = 600;
        v->arpeggio_delay = v->pitch_delay = v->volume_delay = 1;
        memset((void *)(uintptr_t)0x04000000, 0x35, 4096);
        func_080064A4();
        assert(v->delay == delay - 1 && v->pitch == 600);
        assert(v->arpeggio_cursor == 0 && v->pitch_cursor == 0 && v->volume_cursor == 0);
        assert(v->arpeggio_delay == 1 && v->pitch_delay == 1 && v->volume_delay == 1);
        assert(g_030079C0 == (delay == 1 ? 77 : 0));
        for (unsigned offset = 0x60; offset <= 0x80; offset += 2)
            assert(SOUND_REG(0x04000000 + offset) == 0x3535);
    }
}
static void test_terminal_delay(void) {
    for (unsigned n = 0; n < 4; n++) {
        reset(); SoundVoice *v = &g_03007770[n];
        SoundInstrument *ins = ADDRESS(SoundInstrument, g_083C19C0[0]);
        ins->arpeggio = shorts((s16[]){7, 0, 2, -1}, 4);
        ins->slide = shorts((s16[]){0, 1, -2, 3}, 4);
        ins->volume = shorts((s16[]){1, 1, 9, 5}, 4);
        start(n, words((u32[]){0x66, 77, 0x61}, 3));
        v->delay = 1; v->note = 40; v->pitch = 600;
        v->arpeggio_delay = v->pitch_delay = v->volume_delay = 1;
        func_080064A4();
        assert(v->delay == 0 && g_030079C0 == 77 && v->command == 2);
        assert(v->pitch_cursor == 2 && v->pitch_delay == 3);
        assert(v->volume_cursor == 2 && v->volume_delay == 5);
        if (n < 3) {
            assert(v->arpeggio_cursor == 2 && v->arpeggio_delay == 2);
            assert(v->pitch == (s32)pitch(39)-2);
        } else assert(v->pitch == 600 && v->arpeggio_cursor == 0 && v->arpeggio_delay == 1);
        /* Final envelope state survives, then the stop command clears hardware. */
        const unsigned controls[] = {0x62, 0x68, 0x72, 0x78};
        const unsigned pitches[] = {0x64, 0x6c, 0x74, 0x7c};
        assert(SOUND_REG(0x04000000 + controls[n]) == 0);
        assert(SOUND_REG(0x04000000 + pitches[n]) == 0);
    }
}
static void test_hardware_sequences_and_start(void) {
    reset();
    u32 events = shorts((s16[]){254, 6, 0, 0, 0, 4, 0x34, 0x12, 0x56, 0x78}, 10);
    g_03007590[0].events = events; g_03007590[0].cursor = -5;
    func_080064A4(); assert(g_03007590[0].cursor == 5 && g_03007590[0].delay == 4);
    assert(SOUND_REG(0x04000062) == 0x1234 && SOUND_REG(0x04000064) == 0x5678);
    reset(); g_03007590[3].events = shorts((s16[]){254, 253, 0, 0, 0}, 5);
    g_03007590[3].cursor = -5; func_080064A4();
    assert(g_03007590[3].events == 0 && g_03007770[3].output == 1);
    for (unsigned n = 0; n < 4; n++) {
        reset(); SoundInstrument *ins = ADDRESS(SoundInstrument, g_083C19C0[0]);
        ins->volume = shorts((s16[]){3, 4}, 2);
        ins->slide = shorts((s16[]){5, 6}, 2);
        ins->arpeggio = shorts((s16[]){7, -1}, 2);
        events = put((u8[]){40, 0, 0}, 3);
        start(n, words((u32[]){0x64, events, 0, 1, 0x61}, 5));
        func_080064A4();
        assert(g_03007770[n].volume_delay == 4 && g_03007770[n].pitch_delay == 6);
        if (n < 3) assert(g_03007770[n].pitch == (s32)pitch(39));
        else assert(g_03007770[n].pitch == (s32)pitch(40));
        const unsigned control_register[] = {0x62, 0x68, 0x72, 0x78};
        const unsigned pitch_register[] = {0x64, 0x6c, 0x74, 0x7c};
        assert(SOUND_REG(0x04000000 + control_register[n]) == 0x0312);
        assert(SOUND_REG(0x04000000 + pitch_register[n]) == (u16)(0x8105 | (n < 3 ? pitch(39) : 0)));
        /* ADD -32768 and OR 32768 differ when the sequence's high bit is set. */
        ADDRESS(s16, ins->slide)[0] = (s16)-28672; /* unsigned halfword 0x9000 */
        g_03007770[n].delay = 0; g_03007770[n].cursor = 0;
        func_080064A4();
        u32 trigger = n == 0 || n == 3 ? 0x1100 : 0x9100;
        assert(SOUND_REG(0x04000000 + pitch_register[n]) == (u16)(trigger | (n < 3 ? pitch(39) : 0)));
    }
}
int main(void) {
    assert(sizeof(SoundVoice) == 72 && sizeof(SoundSequence) == 12 && sizeof(SoundInstrument) == 36 && sizeof(SoundSample) == 16);
    assert(offsetof(SoundVoice, commands) == 32 && offsetof(SoundVoice, pitch_cursor) == 56);
    arena = mmap((void *)(uintptr_t)0x02000000, 65536, PROT_READ|PROT_WRITE,
                 MAP_PRIVATE|MAP_ANONYMOUS|MAP_FIXED_NOREPLACE, -1, 0);
    assert(arena == (void *)(uintptr_t)0x02000000);
    void *io = mmap((void *)(uintptr_t)0x04000000, 4096, PROT_READ|PROT_WRITE,
                    MAP_PRIVATE|MAP_ANONYMOUS|MAP_FIXED_NOREPLACE, -1, 0);
    assert(io == (void *)(uintptr_t)0x04000000);
    test_output_gate(); test_terminal_delay();
    test_gate_and_prefix(); test_commands_and_pcm(); test_repeat_chaining_and_wrap();
    test_envelopes(); test_hardware_sequences_and_start();
    assert(munmap(arena, 65536) == 0 && munmap(io, 4096) == 0);
    puts("7 sound-owner synthetic groups passed (actual complete C candidate; no ROM)");
}

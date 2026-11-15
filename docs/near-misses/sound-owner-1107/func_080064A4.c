/* Complete source candidate for 080064A4..08007398; uninstalled, not byte-verified. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u16 vu16;
/* All stored addresses and fields are 32-bit, including on the host test build. */
typedef struct { s32 gain[9]; } FadeLevels;
typedef struct { u32 events; s32 cursor, delay; } SoundSequence;
typedef struct {
    s32 enabled, output, command, cursor, delay, note, pitch, instrument;
    u32 commands, events;
    s32 transpose, repeats, volume_cursor, volume_delay;
    s32 pitch_cursor, pitch_delay, arpeggio_cursor, arpeggio_delay;
} SoundVoice;
typedef struct {
    u32 flags, control, control_high, unknown_0c, volume;
    u32 unknown_14, slide, unknown_1c, arpeggio;
} SoundInstrument;
typedef struct { u32 data, length, loop, unknown_0c; } SoundSample;
#define ADDRESS(type, value) ((type *)(unsigned long)(u32)(value))
#define SOUND_REG(address) (*(vu16 *)(unsigned long)(address))
#define PLUS(a, b) ((s32)((u32)(a) + (u32)(b)))
#define MINUS(a, b) ((s32)((u32)(a) - (u32)(b)))
extern FadeLevels g_0801FF00;
extern SoundSequence g_03007590[4];
extern SoundVoice g_03007770[8];
extern s32 g_030079B4, g_03007400, g_030079B0, g_03007570, g_03006A98;
extern u32 g_03007574, g_03007404, g_03007578, g_030079C0;
extern u32 *g_03007580;
extern s8 g_03007410[];
extern void (*g_08332E9C)(s32), (*g_08332EA0)(s32);
extern void func_08005F8C(s32);
extern u32 g_083C19C0[];
extern u8 g_083C100D[], g_083C0FAC[];
extern s32 g_08333324[];
extern SoundSample g_083B8698[];
#define INSTRUMENT(table, index) ADDRESS(SoundInstrument, (table)[index])
#define FREQUENCY(hi, lo, index) (((u32)(hi)[index] << 8) | (lo)[index])

/* Macros keep these blocks in their enclosing function, with constant channel addresses. */
#define TICK_TONE(channel, table, control_reg, pitch_reg) \
    if (i == channel) { \
        instrument = INSTRUMENT(table, voice->instrument); \
        sequence = ADDRESS(s16, instrument->arpeggio); \
        if (sequence && (voice->arpeggio_delay = MINUS(voice->arpeggio_delay, 1)) == 0) { \
            voice->arpeggio_cursor = PLUS(voice->arpeggio_cursor, 2); \
            if ((u16)sequence[voice->arpeggio_cursor] == 254) \
                voice->arpeggio_cursor = sequence[voice->arpeggio_cursor + 1]; \
            if (sequence[voice->arpeggio_cursor] <= 253) { \
                index = PLUS(voice->note, sequence[voice->arpeggio_cursor + 1]); \
                voice->pitch = FREQUENCY(g_083C100D, g_083C0FAC, index); \
                voice->arpeggio_delay = sequence[voice->arpeggio_cursor]; \
                SOUND_REG(pitch_reg) = voice->pitch | ((instrument->flags & 255) << 8); \
            } \
            if ((u16)sequence[voice->arpeggio_cursor] == 255) \
                voice->arpeggio_cursor = MINUS(voice->arpeggio_cursor, 2); \
        } \
        sequence = ADDRESS(s16, instrument->slide); \
        if (sequence && (voice->pitch_delay = MINUS(voice->pitch_delay, 1)) == 0) { \
            voice->pitch_cursor = PLUS(voice->pitch_cursor, 2); \
            if ((u16)sequence[voice->pitch_cursor] == 254) \
                voice->pitch_cursor = sequence[voice->pitch_cursor + 1]; \
            if (sequence[voice->pitch_cursor] <= 253) { \
                voice->pitch_delay = sequence[voice->pitch_cursor + 1]; \
                voice->pitch = PLUS(voice->pitch, sequence[voice->pitch_cursor]); \
                SOUND_REG(pitch_reg) = voice->pitch | (instrument->flags << 8); \
            } \
            if ((u16)sequence[voice->pitch_cursor] == 255) \
                voice->pitch_cursor = MINUS(voice->pitch_cursor, 2); \
        } \
        sequence = ADDRESS(s16, instrument->volume); \
        if (sequence && (voice->volume_delay = MINUS(voice->volume_delay, 1)) == 0) { \
            voice->volume_cursor = PLUS(voice->volume_cursor, 2); \
            if ((u16)sequence[voice->volume_cursor] == 254) \
                voice->volume_cursor = sequence[voice->volume_cursor + 1]; \
            if (sequence[voice->volume_cursor] <= 253) { \
                SOUND_REG(control_reg) = ((u32)(u16)sequence[voice->volume_cursor] << 8) | (u16)instrument->control; \
                voice->volume_delay = sequence[voice->volume_cursor + 1]; \
                SOUND_REG(pitch_reg) = voice->pitch | (instrument->flags << 8) | 0x8000; \
            } \
            if ((u16)sequence[voice->volume_cursor] == 255) \
                voice->volume_cursor = MINUS(voice->volume_cursor, 2); \
        } \
    }
#define START_TONE(channel, table, high, control_reg, pitch_reg) \
    if (i == channel) { \
        instrument = INSTRUMENT(table, voice->instrument); \
        control = instrument->control + (instrument->control_high << 8); \
        sequence = ADDRESS(s16, instrument->volume); \
        if (sequence) { \
            control = (control & 255) | ((u32)(u16)sequence[0] << 8); \
            voice->volume_cursor = 0; \
            voice->volume_delay = sequence[1]; \
        } \
        if (voice->output) SOUND_REG(control_reg) = control; \
        sequence = ADDRESS(s16, instrument->arpeggio); \
        if (sequence) { \
            index = PLUS(note, sequence[1]); \
            voice->pitch = FREQUENCY(high, g_083C0FAC, index); \
            voice->arpeggio_cursor = 0; \
            voice->arpeggio_delay = sequence[0]; \
        } \
        control = (instrument->flags & 255) << 8; \
        sequence = ADDRESS(s16, instrument->slide); \
        if (sequence) { \
            if (channel == 0) control |= (u32)(u16)sequence[0] - 0x8000u; \
            else control |= (u32)(u16)sequence[0] | 0x8000; \
            voice->pitch_cursor = 0; \
            voice->pitch_delay = sequence[1]; \
        } else control |= 0x8000; \
        if (voice->output) SOUND_REG(pitch_reg) = voice->pitch | control; \
    }
void func_080064A4(void)
{
    s32 i = 0, note, index, command, marker;
    u32 control, frequency;
    s16 *sequence;
    u32 *commands;
    u8 *events;
    SoundVoice *voice;
    SoundInstrument *instrument;
    if (g_030079B4 == 1) {
        g_03007400 = PLUS(g_03007400, 1) & 15;
        if (g_03007400 == 0) {
            if (g_030079B0 != 0) g_030079B0 = MINUS(g_030079B0, 1);
            SOUND_REG(0x04000080) = (SOUND_REG(0x04000080) & 0xFF00) | ((u32)g_030079B0 * 17);
            if (g_030079B0 == 0) {
                func_08005F8C(0);
                g_030079B4 = i;
                g_030079B0 = 7;
            }
        }
    }
    if (g_03007570 == 0) {
        if (g_030079B4 == 0 || g_030079B0 != 0) g_08332E9C(4);
        if (g_030079B4 && g_030079B0 != 0 && g_030079B0 != 7) {
            FadeLevels levels = g_0801FF00;
            s32 gain = levels.gain[g_030079B0];
            s8 *out = g_03007410 + ((((u32)g_03006A98 + 1) & 1) * 176);
            s32 left = 175;
            do {
                *out = (s32)((u32)(s32)*out * (u32)gain) >> 8;
                out++;
            } while (--left >= 0);
        }
    } else {
        s8 *out = g_03007410 + ((((u32)g_03006A98 + 1) & 1) * 176) + 175;
        i = 175;
        do { *out-- = 0; } while (--i >= 0);
    }
    for (i = 0; i <= 1; i++) g_08332EA0(i);
    for (i = 0; i <= 3; i++) {
        SoundSequence *seq = &g_03007590[i];
        if (seq->events != 0) {
            if (seq->delay != 0) {
                seq->delay = MINUS(seq->delay, 1);
                if (seq->delay != 0) continue;
            }
            seq->cursor = PLUS(seq->cursor, 5);
            {
                s32 stopped = 0;
                u16 *event = ADDRESS(u16, seq->events) + seq->cursor;
                if (event[0] == 254) {
                    if (event[1] == 253) stopped = 255;
                    else seq->cursor = (s32)event[1] - 1;
                }
                event = ADDRESS(u16, seq->events) + seq->cursor;
                if (event[0] == 255) stopped = 255;
                if (stopped == 255) {
                    seq->events = 0;
                    control = frequency = 0;
                    g_03007770[i].output = 1;
                } else {
                    seq->delay = event[0];
                    control = ((u32)event[2] << 8) | event[1];
                    frequency = ((u32)event[3] << 8) | event[4];
                }
                if (i == 0) { SOUND_REG(0x04000062) = control; SOUND_REG(0x04000064) = frequency; }
                if (i == 1) { SOUND_REG(0x04000068) = control; SOUND_REG(0x0400006C) = frequency; }
                if (i == 2) { SOUND_REG(0x04000072) = control; SOUND_REG(0x04000074) = frequency; }
                if (i == 3) { SOUND_REG(0x04000078) = control; SOUND_REG(0x0400007C) = frequency; }
            }
        }
    }
    if (g_03007570 != 0) return;
    g_03007574 += g_03007404;
    if (g_03007574 <= 255) return;
    g_03007574 -= 256;
    for (i = 0; i <= 7; i++) {
        voice = &g_03007770[i];
        if (voice->enabled != 1 || voice->commands == 0) continue;
        /* 06740 refreshes these pointers after a byte-stream terminator. */
    prepare_voice:
        marker = 0x60;
        if (voice->delay != 0) {
            voice->delay = MINUS(voice->delay, 1);
            if (voice->output != 0) {
                TICK_TONE(0, g_083C19C0, 0x04000062, 0x04000064)
                TICK_TONE(1, g_083C19C0, 0x04000068, 0x0400006C)
                TICK_TONE(2, g_083C19C0, 0x04000072, 0x04000074)
                if (i == 3) {
                    instrument = INSTRUMENT(g_083C19C0, voice->instrument);
                    sequence = ADDRESS(s16, instrument->slide);
                    if (sequence && (voice->pitch_delay = MINUS(voice->pitch_delay, 1)) == 0) {
                        index = voice->pitch_cursor;
                        voice->pitch_cursor = PLUS(index, 2);
                        if ((u16)sequence[voice->pitch_cursor] == 255) voice->pitch_cursor = index;
                        else {
                            SOUND_REG(0x0400007C) = (instrument->flags << 8) | (u16)sequence[voice->pitch_cursor];
                            voice->pitch_delay = sequence[voice->pitch_cursor + 1];
                        }
                    }
                    sequence = ADDRESS(s16, instrument->volume);
                    if (sequence && (voice->volume_delay = MINUS(voice->volume_delay, 1)) == 0) {
                        index = voice->volume_cursor;
                        voice->volume_cursor = PLUS(index, 2);
                        if ((u16)sequence[voice->volume_cursor] == 255) voice->volume_cursor = index;
                        else {
                            SOUND_REG(0x04000078) = instrument->control | ((u32)(u16)sequence[voice->volume_cursor] << 8);
                            voice->volume_delay = sequence[voice->volume_cursor + 1];
                            SOUND_REG(0x0400007C) |= 0x8000;
                        }
                    }
                }
            }
            /* 06D58 checks the remaining delay after the output-gated envelopes. */
            if (voice->delay != 0) goto next_voice;
        }
        if (voice->events == 0) {
            commands = ADDRESS(u32, voice->commands);
            do {
                command = commands[voice->command];
                if (command == 0x67) {
                    g_03007578 = (commands[voice->command + 1] << 8) + (u32)g_030079B0 * 17;
                    SOUND_REG(0x04000080) = g_03007578;
                    voice->command = PLUS(voice->command, 2);
                }
                if (command == 0x69) {
                    g_03007404 = commands[voice->command + 1];
                    voice->command = PLUS(voice->command, 2);
                }
                if (command == 0x60) voice->command = PLUS(voice->command, 3);
                if (command == 0x66) {
                    g_030079C0 = commands[voice->command + 1];
                    voice->command = PLUS(voice->command, 2);
                }
                if (command == 0x61 && voice->output) {
                    if (i == 0) { SOUND_REG(0x04000062) = 0; SOUND_REG(0x04000064) = 0; }
                    if (i == 1) { SOUND_REG(0x04000068) = 0; SOUND_REG(0x0400006C) = 0; }
                    if (i == 2) { SOUND_REG(0x04000072) = 0; SOUND_REG(0x04000074) = 0; }
                    if (i == 3) { SOUND_REG(0x04000078) = 0; SOUND_REG(0x0400007C) = 0; }
                    if ((u32)(i - 4) <= 1) voice->pitch_cursor = -1;
                }
                if (command == 0x64) {
                    voice->transpose = commands[voice->command + 2];
                    voice->events = commands[voice->command + 1];
                    voice->repeats = commands[voice->command + 3];
                    voice->cursor = voice->delay = 0;
                    voice->command = PLUS(voice->command, 4);
                }
                if (command == 0x62) voice->command = commands[voice->command + 1];
            } while (command != 0x61 && command != 0x64);
            if (voice->events == 0) goto next_voice;
        }
        events = ADDRESS(u8, voice->events);
        marker = events[voice->cursor];
        if (marker == 0x65) {
            if (voice->repeats != 0) {
                voice->repeats = MINUS(voice->repeats, 1);
                if (voice->repeats != 0) {
                    voice->cursor = 0;
                    marker = events[0];
                } else voice->events = voice->cursor = 0;
            } else voice->events = voice->cursor = 0;
            if (marker == 0x65) goto prepare_voice;
        }
        note = events[voice->cursor];
        if (note != 0x60) note = (u8)PLUS(note, voice->transpose);
        else {
            note = 0x30;
            if ((u32)(i - 4) <= 1) note = 0x60;
        }
        voice->note = note;
        voice->pitch = FREQUENCY(g_083C100D, g_083C0FAC, note);
        voice->instrument = events[voice->cursor + 1];
        voice->delay = g_03007580[events[voice->cursor + 2]];
        voice->cursor = PLUS(voice->cursor, 3);
        START_TONE(0, g_083C19C0, g_083C100D, 0x04000062, 0x04000064)
        START_TONE(1, g_083C19C0, g_083C100D, 0x04000068, 0x0400006C)
        START_TONE(2, g_083C19C0, g_083C100D, 0x04000072, 0x04000074)
        if (i == 3) {
            instrument = INSTRUMENT(g_083C19C0, voice->instrument);
            control = instrument->control + (instrument->control_high << 8);
            sequence = ADDRESS(s16, instrument->volume);
            if (sequence) {
                control = (control & 255) | ((u32)(u16)sequence[0] << 8);
                voice->volume_cursor = 0;
                voice->volume_delay = sequence[1];
            }
            if (voice->output) SOUND_REG(0x04000078) = control;
            control = (instrument->flags & 255) << 8;
            sequence = ADDRESS(s16, instrument->slide);
            if (sequence) {
                control |= (u32)(u16)sequence[0] - 0x8000u;
                voice->pitch_cursor = 0;
                voice->pitch_delay = sequence[1];
                if (voice->output) SOUND_REG(0x0400007C) = control;
            }
        }
        if ((u32)(i - 4) <= 3) {
            voice->arpeggio_cursor = g_08333324[95 - voice->note];
            voice->volume_delay = 1;
            voice->pitch_cursor = 0;
            voice->pitch_delay = (g_083B8698[voice->instrument].length - 4) << 14;
            if (voice->note == 0x60) voice->pitch_cursor = -1;
        }
    next_voice:
        if (marker == 0x65) goto prepare_voice;
    }
}

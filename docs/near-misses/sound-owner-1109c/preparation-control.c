/* Complete source candidate for 080064A4..08007398; uninstalled, not byte-verified. */
typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed char s8;
typedef signed short s16;
typedef signed int s32;
typedef volatile u16 vu16;
/* All stored addresses and fields are 32-bit, including on the host test build. */
typedef struct {
    s32 gain[9];
} FadeLevels;
typedef struct {
    u32 events;
    s32 cursor, delay;
} SoundSequence;
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
typedef struct {
    u32 data, length, loop, unknown_0c;
} SoundSample;
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
#define TICK_TONE(channel, table, control_reg, pitch_reg)                                          \
    if (i == channel) {                                                                            \
        SoundInstrument *tick_instrument;                                                          \
        s16 *tick_sequence;                                                                        \
        tick_instrument = INSTRUMENT(table, g_03007770[channel].instrument);                       \
        tick_sequence = ADDRESS(s16, tick_instrument->arpeggio);                                   \
        if (tick_sequence && (g_03007770[channel].arpeggio_delay =                                 \
                                  MINUS(g_03007770[channel].arpeggio_delay, 1)) == 0) {            \
            g_03007770[channel].arpeggio_cursor = PLUS(g_03007770[channel].arpeggio_cursor, 2);    \
            if ((u16)tick_sequence[g_03007770[channel].arpeggio_cursor] == 254)                    \
                g_03007770[channel].arpeggio_cursor =                                              \
                    tick_sequence[g_03007770[channel].arpeggio_cursor + 1];                        \
            if (tick_sequence[g_03007770[channel].arpeggio_cursor] <= 253) {                       \
                index = PLUS(g_03007770[channel].note,                                             \
                             tick_sequence[g_03007770[channel].arpeggio_cursor + 1]);              \
                g_03007770[channel].pitch = FREQUENCY(g_083C100D, g_083C0FAC, index);              \
                g_03007770[channel].arpeggio_delay =                                               \
                    tick_sequence[g_03007770[channel].arpeggio_cursor];                            \
                SOUND_REG(pitch_reg) =                                                             \
                    g_03007770[channel].pitch | ((tick_instrument->flags & 255) << 8);             \
            }                                                                                      \
            if ((u16)tick_sequence[g_03007770[channel].arpeggio_cursor] == 255)                    \
                g_03007770[channel].arpeggio_cursor =                                              \
                    MINUS(g_03007770[channel].arpeggio_cursor, 2);                                 \
        }                                                                                          \
        tick_sequence = ADDRESS(s16, tick_instrument->slide);                                      \
        if (tick_sequence && (VOICE_pitch_delay(i) = MINUS(VOICE_pitch_delay(i), 1)) == 0) {       \
            VOICE_pitch_cursor(i) = PLUS(VOICE_pitch_cursor(i), 2);                                \
            if ((u16)tick_sequence[VOICE_pitch_cursor(i)] == 254)                                  \
                VOICE_pitch_cursor(i) = tick_sequence[VOICE_pitch_cursor(i) + 1];                  \
            if (tick_sequence[VOICE_pitch_cursor(i)] <= 253) {                                     \
                VOICE_pitch_delay(i) = tick_sequence[VOICE_pitch_cursor(i) + 1];                   \
                g_03007770[channel].pitch =                                                        \
                    PLUS(g_03007770[channel].pitch, tick_sequence[VOICE_pitch_cursor(i)]);         \
                SOUND_REG(pitch_reg) = g_03007770[channel].pitch | (tick_instrument->flags << 8);  \
            }                                                                                      \
            if ((u16)tick_sequence[VOICE_pitch_cursor(i)] == 255)                                  \
                VOICE_pitch_cursor(i) = MINUS(VOICE_pitch_cursor(i), 2);                           \
        }                                                                                          \
        tick_sequence = ADDRESS(s16, tick_instrument->volume);                                     \
        if (tick_sequence && (VOICE_volume_delay(i) = MINUS(VOICE_volume_delay(i), 1)) == 0) {     \
            VOICE_volume_cursor(i) = PLUS(VOICE_volume_cursor(i), 2);                              \
            if ((u16)tick_sequence[VOICE_volume_cursor(i)] == 254)                                 \
                VOICE_volume_cursor(i) = tick_sequence[VOICE_volume_cursor(i) + 1];                \
            if (tick_sequence[VOICE_volume_cursor(i)] <= 253) {                                    \
                SOUND_REG(control_reg) = ((u32)(u16)tick_sequence[VOICE_volume_cursor(i)] << 8) |  \
                                         (u16)tick_instrument->control;                            \
                VOICE_volume_delay(i) = tick_sequence[VOICE_volume_cursor(i) + 1];                 \
                SOUND_REG(pitch_reg) =                                                             \
                    g_03007770[channel].pitch | (tick_instrument->flags << 8) | 0x8000;            \
            }                                                                                      \
            if ((u16)tick_sequence[VOICE_volume_cursor(i)] == 255)                                 \
                VOICE_volume_cursor(i) = MINUS(VOICE_volume_cursor(i), 2);                         \
        }                                                                                          \
    }
#define START_TONE(channel, table, high, control_reg, pitch_reg)                                   \
    if (i == channel) {                                                                            \
        s32 start_index;                                                                           \
        instrument = INSTRUMENT(table, g_03007770[channel].instrument);                            \
        control = instrument->control + (instrument->control_high << 8);                           \
        sequence = ADDRESS(s16, instrument->volume);                                               \
        if (sequence) {                                                                            \
            control = (control & 255) | ((u32)(u16)sequence[0] << 8);                              \
            g_03007770[channel].volume_cursor = 0;                                                 \
            g_03007770[channel].volume_delay = sequence[1];                                        \
        }                                                                                          \
        if (g_03007770[channel].output)                                                            \
            SOUND_REG(control_reg) = control;                                                      \
        sequence = ADDRESS(s16, instrument->arpeggio);                                             \
        if (sequence) {                                                                            \
            start_index = PLUS(note, sequence[1]);                                                 \
            g_03007770[channel].pitch = FREQUENCY(high, g_083C0FAC, start_index);                  \
            g_03007770[channel].arpeggio_cursor = 0;                                               \
            g_03007770[channel].arpeggio_delay = sequence[0];                                      \
        }                                                                                          \
        control = (instrument->flags & 255) << 8;                                                  \
        sequence = ADDRESS(s16, instrument->slide);                                                \
        if (sequence) {                                                                            \
            if (channel == 0)                                                                      \
                control |= (u32)(u16)sequence[0] - 0x8000u;                                        \
            else                                                                                   \
                control |= (u32)(u16)sequence[0] | 0x8000;                                         \
            g_03007770[channel].pitch_cursor = 0;                                                  \
            g_03007770[channel].pitch_delay = sequence[1];                                         \
        } else                                                                                     \
            control |= 0x8000;                                                                     \
        if (g_03007770[channel].output)                                                            \
            SOUND_REG(pitch_reg) = g_03007770[channel].pitch | control;                            \
    }
extern s32 g_03007780[];
#define VOICE_delay(n) (*delay_field)
extern u32 g_03007794[];
#define VOICE_events(n) (*events_field)
extern s32 g_03007784[];
#define VOICE_note(n) (*note_field)
extern s32 g_03007788[];
#define VOICE_pitch(n) (*pitch_field)
extern s32 g_030077B0[];
#define VOICE_arpeggio_cursor(n) g_03007770[n].arpeggio_cursor
extern s32 g_030077AC[];
#define VOICE_pitch_delay(n) (*pitch_delay_field)
extern s32 g_03007778[];
#define VOICE_command(n) g_03007770[n].command
extern s32 g_030077A8[];
#define VOICE_pitch_cursor(n) g_03007770[n].pitch_cursor
extern s32 g_03007798[];
#define VOICE_transpose(n) g_03007770[n].transpose
extern s32 g_0300777C[];
#define VOICE_cursor(n) g_03007770[n].cursor
extern s32 g_03007774[];
#define VOICE_output(n) g_03007770[n].output
extern s32 g_0300778C[];
#define VOICE_instrument(n) g_03007770[n].instrument
extern s32 g_0300779C[];
#define VOICE_repeats(n) g_03007770[n].repeats
extern s32 g_030077A0[];
#define VOICE_volume_cursor(n) (*volume_cursor_field)
extern s32 g_030077A4[];
#define VOICE_volume_delay(n) g_03007770[n].volume_delay
extern s32 g_030077B4[];
extern u32 g_03007790[];
#define VOICE_commands(n) g_03007770[n].commands
void func_080064A4(void) {
    s32 i = 0, note, index, command, marker;
    u32 control;
    s16 *sequence;
    u32 *commands;
    u8 *events;
    SoundVoice *voice;
    SoundInstrument *instrument;
    u32 volume_piece;
    s32 original_command;
    s32 index8, index9;
    u32 byte_index;
    s32 *delay_field;
    u32 *events_field;
    s32 *note_field;
    s32 *pitch_field;
    s32 *pitch_delay_field;
    s32 *volume_cursor_field;

    if (g_030079B4 == 1) {
        g_03007400 = PLUS(g_03007400, 1) & 15;
        if (g_03007400 == 0) {
            if (g_030079B0 != 0)
                g_030079B0 = MINUS(g_030079B0, 1);
            SOUND_REG(0x04000080) = (SOUND_REG(0x04000080) & 0xFF00) | ((u32)g_030079B0 * 17);
            if (g_030079B0 == 0) {
                func_08005F8C(0);
                g_030079B4 = i;
                g_030079B0 = 7;
            }
        }
    }
    if (g_03007570 == 0) {
        if (g_030079B4 == 0 || g_030079B0 != 0)
            g_08332E9C(4);
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
        do {
            *out-- = 0;
        } while (--i >= 0);
    }
    for (i = 0; i <= 1; i++)
        g_08332EA0(i);
    {
        SoundSequence *seq = g_03007590;
        u32 sequence_byte_offset = 0;
        SoundSequence *sequence_base = g_03007590;
        s32 *seq_cursor = &g_03007590[0].cursor;
        for (i = 0; i <= 3; i++, seq++, sequence_byte_offset += 12, seq_cursor += 3) {
            u16 hardware_control, hardware_frequency;
            if (seq->events != 0) {
                if ((*(s32 *)((u8 *)sequence_base + sequence_byte_offset + 8)) != 0) {
                    (*(s32 *)((u8 *)sequence_base + sequence_byte_offset + 8)) =
                        MINUS((*(s32 *)((u8 *)sequence_base + sequence_byte_offset + 8)), 1);
                    if ((*(s32 *)((u8 *)sequence_base + sequence_byte_offset + 8)) != 0)
                        continue;
                }
                seq->cursor = PLUS(seq->cursor, 5);
                {
                    s32 stopped = 0;
                    u32 event_address = seq->events;
                    u16 *event = ADDRESS(u16, event_address) + seq->cursor;
                    if (event[0] == 254) {
                        if (event[1] == 253)
                            stopped = 255;
                        else
                            (*seq_cursor) = (s32)event[1] - 1;
                    }
                    event = ADDRESS(u16, event_address) + (*seq_cursor);
                    if (event[0] == 255)
                        stopped = 255;
                    if (stopped == 255) {
                        (*(u32 *)((u8 *)g_03007590 + sequence_byte_offset)) = 0;
                        hardware_control = hardware_frequency = 0;
                        g_03007770[i].output = 1;
                    } else {
                        (*(s32 *)((u8 *)sequence_base + sequence_byte_offset + 8)) = event[0];
                        hardware_control = ((u32)event[2] << 8) | event[1];
                        hardware_frequency = ((u32)event[3] << 8) | event[4];
                    }
                    if (i == 0) {
                        SOUND_REG(0x04000062) = hardware_control;
                        SOUND_REG(0x04000064) = hardware_frequency;
                    }
                    if (i == 1) {
                        SOUND_REG(0x04000068) = hardware_control;
                        SOUND_REG(0x0400006C) = hardware_frequency;
                    }
                    if (i == 2) {
                        SOUND_REG(0x04000072) = hardware_control;
                        SOUND_REG(0x04000074) = hardware_frequency;
                    }
                    if (i == 3) {
                        SOUND_REG(0x04000078) = hardware_control;
                        SOUND_REG(0x0400007C) = hardware_frequency;
                    }
                }
            }
        }
    }
    if (g_03007570 != 0)
        return;
    g_03007574 += g_03007404;
    if (g_03007574 <= 255)
        return;
    g_03007574 -= 256;
    for (i = 0; i <= 7; i++) {
        index8 = i * 8;
        voice = &g_03007770[index8 / 8];
        if (voice->enabled != 1 || voice->commands == 0)
            continue;
        /* 06740 refreshes these pointers after a byte-stream terminator. */
    prepare_voice:
        index9 = index8 + i;
        byte_index = (u32)index9 * 8;
        delay_field = ADDRESS(s32, (u32)(unsigned long)g_03007770 + 16 + byte_index);
        events_field = ADDRESS(u32, (u32)(unsigned long)g_03007794 + byte_index);
        note_field = ADDRESS(s32, (u32)(unsigned long)g_03007770 + 20 + byte_index);
        pitch_field = ADDRESS(s32, (u32)(unsigned long)g_03007788 + byte_index);

        volume_cursor_field = ADDRESS(s32, (u32)(unsigned long)g_030077A0 + byte_index);
        pitch_delay_field = ADDRESS(s32, (u32)(unsigned long)g_030077AC + byte_index);

        marker = 0x60;
        if (VOICE_delay(i) != 0) {
            VOICE_delay(i) = MINUS(VOICE_delay(i), 1);
            if (VOICE_output(i) != 0) {
                TICK_TONE(0, g_083C19C0, 0x04000062, 0x04000064)
                TICK_TONE(1, g_083C19C0, 0x04000068, 0x0400006C)
                TICK_TONE(2, g_083C19C0, 0x04000072, 0x04000074)
                if (i == 3) {
                    s32 noise1_index;
                    instrument = INSTRUMENT(g_083C19C0, VOICE_instrument(i));
                    sequence = ADDRESS(s16, instrument->slide);
                    if (sequence && (VOICE_pitch_delay(i) = MINUS(VOICE_pitch_delay(i), 1)) == 0) {
                        noise1_index = VOICE_pitch_cursor(i);
                        VOICE_pitch_cursor(i) = PLUS(noise1_index, 2);
                        if ((u16)sequence[VOICE_pitch_cursor(i)] == 255)
                            VOICE_pitch_cursor(i) = noise1_index;
                        else {
                            SOUND_REG(0x0400007C) =
                                (instrument->flags << 8) | (u16)sequence[VOICE_pitch_cursor(i)];
                            VOICE_pitch_delay(i) = sequence[VOICE_pitch_cursor(i) + 1];
                        }
                    }
                    sequence = ADDRESS(s16, instrument->volume);
                    if (sequence &&
                        (VOICE_volume_delay(i) = MINUS(VOICE_volume_delay(i), 1)) == 0) {
                        noise1_index = VOICE_volume_cursor(i);
                        VOICE_volume_cursor(i) = PLUS(noise1_index, 2);
                        if ((u16)sequence[VOICE_volume_cursor(i)] == 255)
                            VOICE_volume_cursor(i) = noise1_index;
                        else {
                            SOUND_REG(0x04000078) =
                                instrument->control |
                                ((u32)(u16)sequence[VOICE_volume_cursor(i)] << 8);
                            VOICE_volume_delay(i) = sequence[VOICE_volume_cursor(i) + 1];
                            SOUND_REG(0x0400007C) |= 0x8000;
                        }
                    }
                }
            }
            /* 06D58 checks the remaining delay after the output-gated envelopes. */
            if (VOICE_delay(i) != 0)
                goto next_voice;
        }
        if (VOICE_events(i) == 0) {

            do {
                commands = ADDRESS(u32, VOICE_commands(i));
                original_command = VOICE_command(i);
                command = commands[original_command];
                if (command == 0x67) {
                    volume_piece = commands[original_command + 1] << 8;
                    volume_piece += (u32)g_030079B0;
                    g_03007578 = volume_piece + ((u32)g_030079B0 << 4);
                    SOUND_REG(0x04000080) = g_03007578;
                    VOICE_command(i) = PLUS(original_command, 2);
                }
                if (command == 0x69) {
                    g_03007404 = commands[VOICE_command(i) + 1];
                    VOICE_command(i) = PLUS(VOICE_command(i), 2);
                }
                if (command == 0x60)
                    VOICE_command(i) = PLUS(VOICE_command(i), 3);
                if (command == 0x66) {
                    g_030079C0 = commands[VOICE_command(i) + 1];
                    VOICE_command(i) = PLUS(VOICE_command(i), 2);
                }
                if (command == 0x61 && VOICE_output(i)) {
                    if (i == 0) {
                        SOUND_REG(0x04000062) = 0;
                        SOUND_REG(0x04000064) = 0;
                    }
                    if (i == 1) {
                        SOUND_REG(0x04000068) = 0;
                        SOUND_REG(0x0400006C) = 0;
                    }
                    if (i == 2) {
                        SOUND_REG(0x04000072) = 0;
                        SOUND_REG(0x04000074) = 0;
                    }
                    if (i == 3) {
                        SOUND_REG(0x04000078) = 0;
                        SOUND_REG(0x0400007C) = 0;
                    }
                    if ((u32)(i - 4) <= 1)
                        VOICE_pitch_cursor(i) = -1;
                }
                if (command == 0x64) {
                    VOICE_transpose(i) = commands[VOICE_command(i) + 2];
                    VOICE_events(i) = commands[VOICE_command(i) + 1];
                    VOICE_repeats(i) = commands[VOICE_command(i) + 3];
                    VOICE_cursor(i) = VOICE_delay(i) = 0;
                    VOICE_command(i) = PLUS(VOICE_command(i), 4);
                }
                if (command == 0x62)
                    VOICE_command(i) = commands[VOICE_command(i) + 1];
            } while (command != 0x61 && command != 0x64);
            if (VOICE_events(i) == 0)
                goto next_voice;
        }
        events = ADDRESS(u8, VOICE_events(i));
        marker = events[VOICE_cursor(i)];
        if (marker == 0x65) {
            if (VOICE_repeats(i) != 0) {
                VOICE_repeats(i) = MINUS(VOICE_repeats(i), 1);
                if (VOICE_repeats(i) != 0) {
                    VOICE_cursor(i) = 0;
                    marker = events[0];
                } else
                    VOICE_events(i) = VOICE_cursor(i) = 0;
            } else
                VOICE_events(i) = VOICE_cursor(i) = 0;
            if (marker == 0x65)
                goto prepare_voice;
        }
        note = events[VOICE_cursor(i)];
        if (note != 0x60)
            note = (u8)PLUS(note, VOICE_transpose(i));
        else {
            note = 0x30;
            if ((u32)(i - 4) <= 1)
                note = 0x60;
        }
        VOICE_note(i) = note;
        VOICE_pitch(i) = FREQUENCY(g_083C100D, g_083C0FAC, note);
        VOICE_instrument(i) = events[VOICE_cursor(i) + 1];
        VOICE_delay(i) = g_03007580[events[VOICE_cursor(i) + 2]];
        VOICE_cursor(i) = PLUS(VOICE_cursor(i), 3);
        START_TONE(0, g_083C19C0, g_083C100D, 0x04000062, 0x04000064)
        START_TONE(1, g_083C19C0, g_083C100D, 0x04000068, 0x0400006C)
        START_TONE(2, g_083C19C0, g_083C100D, 0x04000072, 0x04000074)
        if (i == 3) {
            u32 noise2_control;
            instrument = INSTRUMENT(g_083C19C0, VOICE_instrument(i));
            noise2_control = instrument->control + (instrument->control_high << 8);
            sequence = ADDRESS(s16, instrument->volume);
            if (sequence) {
                noise2_control = (noise2_control & 255) | ((u32)(u16)sequence[0] << 8);
                VOICE_volume_cursor(i) = 0;
                VOICE_volume_delay(i) = sequence[1];
            }
            if (VOICE_output(i))
                SOUND_REG(0x04000078) = noise2_control;
            noise2_control = (instrument->flags & 255) << 8;
            sequence = ADDRESS(s16, instrument->slide);
            if (sequence) {
                noise2_control |= (u32)(u16)sequence[0] - 0x8000u;
                VOICE_pitch_cursor(i) = 0;
                VOICE_pitch_delay(i) = sequence[1];
                if (VOICE_output(i))
                    SOUND_REG(0x0400007C) = noise2_control;
            }
        }
        if ((u32)(i - 4) <= 3) {
            VOICE_arpeggio_cursor(i) = g_08333324[95 - VOICE_note(i)];
            VOICE_volume_delay(i) = 1;
            VOICE_pitch_cursor(i) = 0;
            VOICE_pitch_delay(i) = (g_083B8698[VOICE_instrument(i)].length - 4) << 14;
            if (VOICE_note(i) == 0x60)
                VOICE_pitch_cursor(i) = -1;
        }
    next_voice:
        if (marker == 0x65)
            goto prepare_voice;
    }
}

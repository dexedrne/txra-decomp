/* 080064A4..08007398 (sound owner), complete natural-C source.  Uninstalled near-miss:
 * not byte-exact.  old_agbcc -O2 -mthumb-interwork.  Written from the original statement
 * order; locals are declared in the innermost block that uses them (see README.md). */
typedef unsigned char u8;
typedef unsigned short u16;
typedef unsigned int u32;
typedef signed char s8;
typedef signed short s16;
typedef signed int s32;
typedef volatile u16 vu16;

typedef struct {
    s32 enabled, output, command, cursor, delay, note, pitch, instrument;
    u32 *commands;
    u8 *events;
    s32 transpose, repeats;
    s32 volume_cursor, volume_delay, pitch_cursor, pitch_delay, arp_cursor, arp_delay;
} Voice;

typedef struct {
    u16 *events;
    s32 cursor, delay;
} Effect;

typedef struct {
    u32 flags, control, control_high, unused_0c;
    s16 *volume;
    u32 unused_14;
    s16 *slide;
    u32 unused_1c;
    s16 *arp;
} Instrument;

typedef struct {
    u32 data, length, loop, unused_0c;
} Sample;

typedef struct {
    s32 gain[9];
} FadeTable;

#define gFadeActive g_030079B4
#define gFadeTimer g_03007400
#define gFadeLevel g_030079B0
#define gSoundPaused g_03007570
#define gMixBank g_03006A98
#define gMixBuffer g_03007410
#define gFadeTable g_0801FF00
#define gMixHook g_08332E9C
#define gChannelHook g_08332EA0
#define gEffects g_03007590
#define gVoices g_03007770
#define gTempoCounter g_03007574
#define gTempo g_03007404
#define gMasterVolume g_03007578
#define gDurations g_03007580
#define gInstruments g_083C19C0
#define gFreqLo g_083C0FAC
#define gFreqHi g_083C100D
#define gSampleSteps g_08333324
#define gSamples g_083B8698
extern s32 gFadeActive;      /* 030079B4 */
extern s32 gFadeTimer;       /* 03007400 */
extern s32 gFadeLevel;       /* 030079B0 */
extern s32 gSoundPaused;     /* 03007570 */
extern s32 gMixBank;         /* 03006A98 */
extern s8 gMixBuffer[];      /* 03007410 */
extern const FadeTable gFadeTable; /* 0801FF00 */
extern void (*gMixHook)(s32);      /* 08332E9C */
extern void (*gChannelHook)(s32);  /* 08332EA0 */
extern Effect gEffects[4];   /* 03007590 */
extern Voice gVoices[8];     /* 03007770 */
extern u32 gTempoCounter;    /* 03007574 */
extern u32 gTempo;           /* 03007404 */
extern u32 gMasterVolume;    /* 03007578 */
extern u32 g_030079C0;
extern s32 *gDurations;      /* 03007580 */
extern Instrument *gInstruments[];  /* 083C19C0 */
extern const u8 gFreqLo[];   /* 083C0FAC */
extern const u8 gFreqHi[];   /* 083C100D */
extern const s32 gSampleSteps[];    /* 08333324 */
extern const Sample gSamples[];     /* 083B8698 */
extern void func_08005F8C(s32);

#define REG(a) (*(vu16 *)(a))

#define TICK_TONE(c, ctl, frq, ARPWRITE)                                                             \
    if (i == c) {                                                                                    \
        inst = gInstruments[gVoices[c].instrument];                                                  \
         seq = inst->arp;                                                                            \
        if (seq != 0 && --gVoices[c].arp_delay == 0) {                                               \
            gVoices[c].arp_cursor += 2;                                                              \
            if (seq[gVoices[c].arp_cursor] == 254)                                                   \
                gVoices[c].arp_cursor = seq[gVoices[c].arp_cursor + 1];                              \
            if (seq[gVoices[c].arp_cursor] <= 253) {                                                 \
                gVoices[c].pitch = (gFreqHi[gVoices[c].note + seq[gVoices[c].arp_cursor + 1]] << 8) | gFreqLo[gVoices[c].note + seq[gVoices[c].arp_cursor + 1]]; \
                gVoices[c].arp_delay = seq[gVoices[c].arp_cursor];                                   \
                ARPWRITE(c, frq)                                                                     \
            }                                                                                        \
            if (seq[gVoices[c].arp_cursor] == 255)                                                   \
                gVoices[c].arp_cursor -= 2;                                                          \
        }                                                                                            \
         slide = inst->slide;                                                                        \
        if (slide != 0 && --gVoices[i].pitch_delay == 0) {                                           \
            gVoices[i].pitch_cursor += 2;                                                            \
            if (slide[gVoices[i].pitch_cursor] == 254)                                               \
                gVoices[i].pitch_cursor = slide[gVoices[i].pitch_cursor + 1];                        \
            if (slide[gVoices[i].pitch_cursor] <= 253) {                                             \
                gVoices[i].pitch_delay = slide[gVoices[i].pitch_cursor + 1];                         \
                p = gVoices[i].pitch; p += slide[gVoices[i].pitch_cursor]; gVoices[i].pitch = p;         \
                val = gVoices[i].pitch;                                                              \
                val |= inst->flags << 8;                                                             \
                REG(frq) = val;                                                                      \
            }                                                                                        \
            if (slide[gVoices[i].pitch_cursor] == 255)                                               \
                gVoices[i].pitch_cursor -= 2;                                                        \
        }                                                                                            \
         seq = inst->volume;                                                                         \
        if (seq != 0 && --gVoices[i].volume_delay == 0) {                                            \
            gVoices[i].volume_cursor += 2;                                                           \
            if (seq[gVoices[i].volume_cursor] == 254)                                                \
                gVoices[i].volume_cursor = seq[gVoices[i].volume_cursor + 1];                        \
            if (seq[gVoices[i].volume_cursor] <= 253) {                                              \
                val = inst->control;                                                                 \
                val |= seq[gVoices[i].volume_cursor] << 8;                                           \
                REG(ctl) = val;                                                                      \
                gVoices[i].volume_delay = seq[gVoices[i].volume_cursor + 1];                         \
                REG(frq) = (inst->flags << 8) | gVoices[i].pitch | 0x8000;                           \
            }                                                                                        \
            if (seq[gVoices[i].volume_cursor] == 255)                                                \
                gVoices[i].volume_cursor -= 2;                                                       \
        }                                                                                            \
     }
#define ARP_DIRECT(c, frq)  { u16 t = inst->flags << 8; REG(frq) = t | gVoices[c].pitch; }
#define ARP_VAL(c, frq)     val = gVoices[c].pitch; val |= inst->flags << 8; REG(frq) = val;

#define START_TONE(c, ctl, frq, SLIDEBIT)                                                            \
    if (i == c) {  s16 *seq;                                                                         \
        inst = gInstruments[gVoices[c].instrument];                                                  \
        val = inst->control + (inst->control_high << 8);                                             \
        seq = inst->volume;                                                                          \
        if (seq != 0) {                                                                              \
            val &= 255;                                                                              \
            val |= (u16)seq[0] << 8;                                                                 \
            gVoices[c].volume_cursor = 0;                                                            \
            gVoices[c].volume_delay = seq[1];                                                        \
        }                                                                                            \
        if (gVoices[c].output != 0)                                                                  \
            REG(ctl) = val;                                                                          \
        seq = inst->arp;                                                                             \
        if (seq != 0) {                                                                              \
            { s32 n; n = note + seq[1]; gVoices[c].pitch = (gFreqHi[n] << 8) | gFreqLo[n]; }         \
            gVoices[c].arp_cursor = 0;                                                               \
            gVoices[c].arp_delay = seq[0];                                                           \
        }                                                                                            \
        val = inst->flags << 8;                                                                      \
        seq = inst->slide;                                                                           \
        if (seq != 0) {                                                                              \
            SLIDEBIT                                                                                 \
            gVoices[c].pitch_cursor = 0;                                                             \
            gVoices[c].pitch_delay = seq[1];                                                         \
            val |= gVoices[c].pitch;                                                                 \
            if (gVoices[c].output != 0)                                                              \
                REG(frq) = val;                                                                      \
        } else {                                                                                     \
            val |= 0x8000;                                                                           \
            val |= gVoices[c].pitch;                                                                 \
            if (gVoices[c].output != 0)                                                              \
                REG(frq) = val;                                                                      \
        }                                                                                            \
    }

void func_080064A4(void) {
    s32 i;
    s32 p;
    s32 j;
    u16 val;
    s32 marker;
    s32 command = 0;
    s32 index;
    u32 piece;
    u8 note;
    u8 *events;
    u32 *commands;
    s16 *seq;
    s8 *buffer;
    s32 gain;
    Instrument *inst;
    Effect *effect;
    s32 cidx;
    s16 *slide;

    if (gFadeActive == 1) {
        gFadeTimer = (gFadeTimer + 1) & 15;
        if (gFadeTimer == 0) {
            if (gFadeLevel != 0)
                gFadeLevel--;
            val = (REG(0x04000080) & 0xFF00) | (gFadeLevel + (gFadeLevel << 4));
            REG(0x04000080) = val;
            if (gFadeLevel == 0) {
                func_08005F8C(0);
                gFadeActive = command;
                gFadeLevel = 7;
            }
        }
    }

    if (gSoundPaused == 0) {
        if (gFadeActive == 0 || gFadeLevel != 0)
            gMixHook(4);
        if (gFadeActive != 0 && gFadeLevel != 0 && gFadeLevel != 7) {
            FadeTable table = gFadeTable;
            gain = table.gain[gFadeLevel];
            «sb@{\n                s32 idx = (gMixBank + 1) & 1;\n                buffer = gMixBuffer;\n                buffer += idx * 176;\n            }@{\n                s32 idx = (gMixBank + 1) & 1;\n                buffer = gMixBuffer + idx * 176;\n            }@{\n                s32 idx = (gMixBank + 1) & 1;\n                buffer = &gMixBuffer[idx * 176];\n            }@buffer = &gMixBuffer[((gMixBank + 1) & 1) * 176];»
            for (j = 175; j >= 0; j--) {
                *buffer = (*buffer * gain) >> 8;
                buffer++;
            }
        }
    } else {
        «cb@{\n            s32 idx = (gMixBank + 1) & 1;\n            buffer = gMixBuffer;\n            i = 175;\n            buffer += idx * 176 + i;\n        }@{\n            s32 idx = (gMixBank + 1) & 1;\n            buffer = &gMixBuffer[idx * 176] + 175;\n            i = 175;\n        }@{\n            s32 idx = (gMixBank + 1) & 1;\n            i = 175;\n            buffer = &gMixBuffer[idx * 176] + i;\n        }@{\n            s32 idx = (gMixBank + 1) & 1;\n            buffer = &gMixBuffer[idx * 176 + 175];\n            i = 175;\n        }@{\n            s32 idx = (gMixBank + 1) & 1;\n            buffer = gMixBuffer + idx * 176 + 175;\n            i = 175;\n        }@buffer = &gMixBuffer[((gMixBank + 1) & 1) * 176] + 175;\n        i = 175;»
        «cz@do {\n            *buffer-- = 0;\n        } while (--i >= 0);@for (; i >= 0; i--)\n            *buffer-- = 0;@do {\n            *buffer = 0;\n            buffer--;\n        } while (--i >= 0);»
    }

    for (i = 0; i <= 1; i++)
        gChannelHook(i);

    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s32 stop;
        u16 val;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
            if (i == 0) {
                REG(0x04000062) = val;
                REG(0x04000064) = freq;
            }
            if (i == 1) {
                REG(0x04000068) = val;
                REG(0x0400006C) = freq;
            }
            if (i == 2) {
                REG(0x04000072) = val;
                REG(0x04000074) = freq;
            }
            if (i == 3) {
                REG(0x04000078) = val;
                REG(0x0400007C) = freq;
            }
        }
    }

    if (gSoundPaused != 0)
        return;
    gTempoCounter += gTempo;
    if (gTempoCounter <= 255)
        return;
    gTempoCounter -= 256;

    for (i = 0; i <= 7; i++) {
        if (gVoices[i].enabled != 1)
            continue;
        if (gVoices[i].commands == 0)
            continue;
    restart:
        do {
            marker = 0x60;
            if (gVoices[i].delay != 0) {
                gVoices[i].delay--;
                if (gVoices[i].output != 0) {
                    TICK_TONE(0, 0x04000062, 0x04000064, ARP_DIRECT)
                    TICK_TONE(1, 0x04000068, 0x0400006C, ARP_VAL)
                    TICK_TONE(2, 0x04000072, 0x04000074, ARP_DIRECT)
                    if (i == 3) {
                        s16 *seq;

                        inst = gInstruments[gVoices[3].instrument];
                        seq = inst->slide;
                        if (seq != 0 && --gVoices[3].pitch_delay == 0) {
                            s32 index;

                            index = gVoices[3].pitch_cursor;
                            gVoices[3].pitch_cursor = index + 2;
                            if (seq[gVoices[3].pitch_cursor] == 255)
                                gVoices[3].pitch_cursor = index;
                            else {
                                {
                                    s32 t = seq[gVoices[3].pitch_cursor];
                                    val = (inst->flags << 8) | t;
                                }
                                gVoices[3].pitch_delay = seq[gVoices[3].pitch_cursor + 1];
                                REG(0x0400007C) = val;
                            }
                        }
                        seq = inst->volume;
                        if (seq != 0 && --gVoices[i].volume_delay == 0) {
                            s32 index;

                            index = gVoices[i].volume_cursor;
                            gVoices[i].volume_cursor = index + 2;
                            if (seq[gVoices[i].volume_cursor] == 255)
                                gVoices[i].volume_cursor = index;
                            else {
                                val = inst->control | ((u16)seq[gVoices[i].volume_cursor] << 8);
                                REG(0x04000078) = val;
                                gVoices[i].volume_delay = seq[gVoices[i].volume_cursor + 1];
                                REG(0x0400007C) |= 0x8000;
                            }
                        }
                    }
                }
                if (gVoices[i].delay != 0)
                    continue;
            }
            if (gVoices[i].events == 0) {
                do {
                    commands = gVoices[i].commands;
                    cidx = gVoices[i].command;
                    command = commands[cidx];
                    if (command == 0x67) {
                        piece = commands[cidx + 1] * 256;
                        piece += gFadeLevel;
                        gMasterVolume = piece + (gFadeLevel << 4);
                        REG(0x04000080) = gMasterVolume;
                        gVoices[i].command = cidx + 2;
                    }
                    if (command == 0x69) {
                        gTempo = commands[gVoices[i].command + 1];
                        gVoices[i].command += 2;
                    }
                    if (command == 0x60)
                        gVoices[i].command += 3;
                    if (command == 0x66) {
                        g_030079C0 = commands[gVoices[i].command + 1];
                        gVoices[i].command += 2;
                    }
                    if (command == 0x61 && gVoices[i].output != 0) {
                        if (i == 0) {
                            REG(0x04000062) = 0;
                            REG(0x04000064) = 0;
                        }
                        if (i == 1) {
                            REG(0x04000068) = 0;
                            REG(0x0400006C) = 0;
                        }
                        if (i == 2) {
                            REG(0x04000072) = 0;
                            REG(0x04000074) = 0;
                        }
                        if (i == 3) {
                            REG(0x04000078) = 0;
                            REG(0x0400007C) = 0;
                        }
                        if (i == 4 || i == 5)
                            gVoices[i].pitch_cursor = -1;
                    }
                    if (command == 0x64) {
                        gVoices[i].transpose = commands[gVoices[i].command + 2];
                        gVoices[i].events = (u8 *)commands[gVoices[i].command + 1];
                        gVoices[i].repeats = commands[gVoices[i].command + 3];
                        gVoices[i].cursor = 0;
                        gVoices[i].delay = 0;
                        gVoices[i].command += 4;
                    }
                    if (command == 0x62)
                        gVoices[i].command = commands[gVoices[i].command + 1];
                } while (command != 0x64 && command != 0x61);
                if (gVoices[i].events == 0)
                    continue;
            }
            events = gVoices[i].events;
            marker = events[gVoices[i].cursor];
            if (marker == 0x65) {
                if (gVoices[i].repeats != 0) {
                    if (--gVoices[i].repeats != 0) {
                        gVoices[i].cursor = 0;
                        marker = events[0];
                    } else {
                        gVoices[i].events = 0;
                        gVoices[i].cursor = 0;
                    }
                } else {
                    gVoices[i].events = 0;
                    gVoices[i].cursor = 0;
                }
                if (marker == 0x65)
                    goto restart;
            }
            note = events[gVoices[i].cursor];
            if (note != 0x60)
                note += gVoices[i].transpose;
            else {
                note = 48;
                if (i == 4 || i == 5)
                    note = 96;
            }
            {
                s32 *durations = gDurations;
                gVoices[i].note = note;
                gVoices[i].pitch = (gFreqHi[note] << 8) | gFreqLo[note];
                gVoices[i].instrument = (events + gVoices[i].cursor)[1];
                gVoices[i].delay = durations[(events + gVoices[i].cursor)[2]];
                gVoices[i].cursor += 3;
            }
            START_TONE(0, 0x04000062, 0x04000064, val |= (u16)seq[0] - 0x8000;)
            START_TONE(1, 0x04000068, 0x0400006C, val |= (u16)seq[0] | 0x8000;)
            START_TONE(2, 0x04000072, 0x04000074, val |= (u16)seq[0] | 0x8000;)
            if (i == 3) {
                inst = gInstruments[gVoices[3].instrument];
                val = inst->control + (inst->control_high << 8);
                seq = inst->volume;
                if (seq != 0) {
                    val &= 255;
                    val |= (u16)seq[0] << 8;
                    gVoices[3].volume_cursor = 0;
                    gVoices[3].volume_delay = seq[1];
                }
                if (gVoices[3].output != 0)
                    REG(0x04000078) = val;
                val = inst->flags << 8;
                seq = inst->slide;
                if (seq != 0) {
                    val |= (u16)seq[0] - 0x8000;
                    gVoices[i].pitch_cursor = 0;
                    gVoices[i].pitch_delay = seq[1];
                    if (gVoices[3].output != 0)
                        REG(0x0400007C) = val;
                }
            }
            if (i >= 4 && i <= 7) {
                gVoices[i].volume_cursor = gSampleSteps[95 - gVoices[i].note];
                gVoices[i].volume_delay = 1;
                gVoices[i].pitch_cursor = 0;
                gVoices[i].pitch_delay = (gSamples[gVoices[i].instrument].length - 4) << 14;
                if (gVoices[i].note == 96)
                    gVoices[i].pitch_cursor = -1;
            }
        } while (marker == 0x65);
    }
}

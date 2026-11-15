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

#define SA «sas@seq@seqa»
#define SST «sss@seq@seqs@seqa»
#define SVT «ssv@seq@seqv@seqa@seqs»
#define TICK_TONE(c, ctl, frq, ARPWRITE)                                                         \
    if (i == c) { «tinst@@Instrument *inst;»«tval@@ u16 val;»                                                    \
        inst = gInstruments[gVoices[c].instrument];                                              \
        «tseq@@{ s16 *seq;» SA = inst->arp;                                                      \
        if (SA != 0 && --gVoices[c].arp_delay == 0) {                                           \
            gVoices[c].arp_cursor += 2;                                                          \
            if (SA[gVoices[c].arp_cursor] == 254)                                               \
                gVoices[c].arp_cursor = SA[gVoices[c].arp_cursor + 1];                          \
            if (SA[gVoices[c].arp_cursor] <= 253) {                                             \
                «tarp@index = gVoices[c].note + SA[gVoices[c].arp_cursor + 1]; gVoices[c].pitch = (gFreqHi[index] << 8) | gFreqLo[index];@aidx = gVoices[c].note + SA[gVoices[c].arp_cursor + 1]; gVoices[c].pitch = (gFreqHi[aidx] << 8) | gFreqLo[aidx];@{ s32 n; n = gVoices[c].note + SA[gVoices[c].arp_cursor + 1]; gVoices[c].pitch = (gFreqHi[n] << 8) | gFreqLo[n]; }@gVoices[c].pitch = (gFreqHi[gVoices[c].note + SA[gVoices[c].arp_cursor + 1]] << 8) | gFreqLo[gVoices[c].note + SA[gVoices[c].arp_cursor + 1]];»     \
                gVoices[c].arp_delay = SA[gVoices[c].arp_cursor];                               \
                ARPWRITE(c, frq)                                                                 \
            }                                                                                    \
            if (SA[gVoices[c].arp_cursor] == 255)                                               \
                gVoices[c].arp_cursor -= 2;                                                      \
        }                                                                                        \
        «tseq@@}{ s16 *seq;»«tss@@{ s16 *seqs;@{ s16 *seq;» SST = inst->slide;                                                  \
        if (SST != 0 && --gVoices[i].pitch_delay == 0) {                                         \
            gVoices[i].pitch_cursor += 2;                                                        \
            if (SST[gVoices[i].pitch_cursor] == 254)                                             \
                gVoices[i].pitch_cursor = SST[gVoices[i].pitch_cursor + 1];                      \
            if (SST[gVoices[i].pitch_cursor] <= 253) {                                           \
                gVoices[i].pitch_delay = SST[gVoices[i].pitch_cursor + 1];                       \
                «padd@gVoices[i].pitch += SST[gVoices[i].pitch_cursor];@gVoices[i].pitch = gVoices[i].pitch + SST[gVoices[i].pitch_cursor];@{ s32 p = gVoices[i].pitch; p += SST[gVoices[i].pitch_cursor]; gVoices[i].pitch = p; }@{ s32 p = gVoices[i].pitch; gVoices[i].pitch = p + SST[gVoices[i].pitch_cursor]; }» \
                val = gVoices[i].pitch;                                                          \
                val |= inst->flags << 8;                                                         \
                REG(frq) = val;                                                                  \
            }                                                                                    \
            if (SST[gVoices[i].pitch_cursor] == 255)                                             \
                gVoices[i].pitch_cursor -= 2;                                                    \
        }                                                                                        \
        «tss@@}@}»«tseq@@}{ s16 *seq;»«tsv@@{ s16 *seqv;@{ s16 *seq;» SVT = inst->volume;                                                 \
        if (SVT != 0 && --gVoices[i].volume_delay == 0) {                                        \
            gVoices[i].volume_cursor += 2;                                                       \
            if (SVT[gVoices[i].volume_cursor] == 254)                                            \
                gVoices[i].volume_cursor = SVT[gVoices[i].volume_cursor + 1];                    \
            if (SVT[gVoices[i].volume_cursor] <= 253) {                                          \
                val = inst->control;                                                             \
                val |= SVT[gVoices[i].volume_cursor] << 8;                                       \
                REG(ctl) = val;                                                                  \
                gVoices[i].volume_delay = SVT[gVoices[i].volume_cursor + 1];                     \
                REG(frq) = (inst->flags << 8) | gVoices[i].pitch | 0x8000;                       \
            }                                                                                    \
            if (SVT[gVoices[i].volume_cursor] == 255)                                            \
                gVoices[i].volume_cursor -= 2;                                                   \
        }                                                                                        \
    «tsv@@}@}»«tseq@@}» }
#define ARP_DIRECT(c, frq)  «arpw@val = inst->flags << 8; REG(frq) = val | gVoices[c].pitch;@freq = inst->flags << 8; REG(frq) = freq | gVoices[c].pitch;@{ u16 t = inst->flags << 8; REG(frq) = t | gVoices[c].pitch; }@REG(frq) = (u16)(inst->flags << 8) | gVoices[c].pitch;@REG(frq) = gVoices[c].pitch | (u16)(inst->flags << 8);»
#define ARP_VAL(c, frq)     «arpv@val = gVoices[c].pitch; val |= inst->flags << 8; REG(frq) = val;@{ u16 t = gVoices[c].pitch; t |= inst->flags << 8; REG(frq) = t; }@freq = gVoices[c].pitch; freq |= inst->flags << 8; REG(frq) = freq;»

#define SV(c) gVoices[«stf@c@i»]
#define START_TONE(c, ctl, frq, SLIDEBIT)                                                        \
    if (i == c) { «sinst@@Instrument *inst;»«sval@@ u16 val;»«sseq@@ s16 *seq;»                         \
        inst = gInstruments[gVoices[c].instrument];                                              \
        val = inst->control + (inst->control_high << 8);                                         \
        seq = inst->volume;                                                                      \
        if (seq != 0) {                                                                          \
            val &= 255;                                                                          \
            val |= (u16)seq[0] << 8;                                                             \
            SV(c).volume_cursor = 0;                                                        \
            SV(c).volume_delay = seq[1];                                                    \
        }                                                                                        \
        if (SV(c).output != 0)                                                              \
            REG(ctl) = val;                                                                      \
        seq = inst->arp;                                                                         \
        if (seq != 0) {                                                                          \
            «sarp@index = note + seq[1]; SV(c).pitch = (gFreqHi[index] << 8) | gFreqLo[index];@aidx = note + seq[1]; SV(c).pitch = (gFreqHi[aidx] << 8) | gFreqLo[aidx];@{ s32 n; n = note + seq[1]; SV(c).pitch = (gFreqHi[n] << 8) | gFreqLo[n]; }@SV(c).pitch = (gFreqHi[note + seq[1]] << 8) | gFreqLo[note + seq[1]];»    \
            SV(c).arp_cursor = 0;                                                           \
            SV(c).arp_delay = seq[0];                                                       \
        }                                                                                        \
        val = inst->flags << 8;                                                                  \
        seq = inst->slide;                                                                       \
        if (seq != 0) {                                                                          \
            SLIDEBIT                                                                             \
            SV(c).pitch_cursor = 0;                                                         \
            SV(c).pitch_delay = seq[1];                                                     \
            val |= SV(c).pitch;                                                             \
            if (SV(c).output != 0)                                                          \
                REG(frq) = val;                                                                  \
        } else {                                                                                 \
            val |= 0x8000;                                                                       \
            val |= SV(c).pitch;                                                             \
            if (SV(c).output != 0)                                                          \
                REG(frq) = val;                                                                  \
        }                                                                                        \
    }

void func_080064A4(void) {
«decl@    s32 i;\n    s32 j;\n    u16 val;\n    u16 freq;\n    s32 stop;\n    s32 marker;\n    s32 command = 0;\n    s32 index;\n    u32 piece;\n    u8 note;\n    u8 *events;\n    u32 *commands;\n    s16 *seq;\n    s8 *buffer;\n    s32 gain;\n    Instrument *inst;\n    Effect *effect;\n    u16 *event;\n    u16 *events16;\n    s32 aidx;\n    s32 old;\n    s32 cidx;\n    s16 *seqa;\n    s16 *seqs;\n    s16 *seqv;\n    s32 *durations16;@    s32 marker;\n    u16 *event;\n    s32 old;\n    Instrument *inst;\n    s32 index;\n    s32 gain;\n    s32 cidx;\n    s16 *seqa;\n    s16 *seqs;\n    s16 *seqv;\n    s32 *durations16;\n    s32 aidx;\n    s32 command = 0;\n    u16 *events16;\n    s8 *buffer;\n    Effect *effect;\n    u32 piece;\n    s32 i;\n    u8 note;\n    u32 *commands;\n    u16 freq;\n    u16 val;\n    s32 j;\n    s16 *seq;\n    s32 stop;\n    u8 *events;@    u16 freq;\n    s32 marker;\n    s32 gain;\n    Instrument *inst;\n    u8 *events;\n    u8 note;\n    u32 *commands;\n    Effect *effect;\n    s8 *buffer;\n    u16 *event;\n    s32 command = 0;\n    s32 stop;\n    u16 val;\n    u32 piece;\n    s32 i;\n    s32 cidx;\n    s16 *seqa;\n    s16 *seqs;\n    s16 *seqv;\n    s32 *durations16;\n    s32 aidx;\n    s16 *seq;\n    s32 j;\n    u16 *events16;\n    s32 old;\n    s32 index;@    s16 *seq;\n    s32 old;\n    s32 i;\n    s32 stop;\n    s8 *buffer;\n    s32 aidx;\n    u16 *events16;\n    s32 cidx;\n    s16 *seqa;\n    s16 *seqs;\n    s16 *seqv;\n    s32 *durations16;\n    s32 gain;\n    u8 note;\n    s32 index;\n    s32 marker;\n    Effect *effect;\n    u32 piece;\n    u8 *events;\n    Instrument *inst;\n    s32 command = 0;\n    s32 j;\n    u16 val;\n    u16 *event;\n    u16 freq;\n    u32 *commands;@    u16 *events16;\n    s32 old;\n    s32 j;\n    s32 aidx;\n    s32 stop;\n    u16 *event;\n    u32 *commands;\n    s32 i;\n    s8 *buffer;\n    s32 index;\n    s16 *seq;\n    s32 marker;\n    s32 cidx;\n    s16 *seqa;\n    s16 *seqs;\n    s16 *seqv;\n    s32 *durations16;\n    s32 command = 0;\n    u32 piece;\n    u16 freq;\n    u16 val;\n    u8 note;\n    s32 gain;\n    u8 *events;\n    Instrument *inst;\n    Effect *effect;@    s32 command = 0;\n    s32 old;\n    s8 *buffer;\n    s16 *seq;\n    Effect *effect;\n    u16 freq;\n    s32 marker;\n    u8 note;\n    s32 cidx;\n    s16 *seqa;\n    s16 *seqs;\n    s16 *seqv;\n    s32 *durations16;\n    s32 stop;\n    s32 i;\n    s32 j;\n    u8 *events;\n    u32 *commands;\n    s32 index;\n    u32 piece;\n    u16 *event;\n    u16 val;\n    s32 gain;\n    u16 *events16;\n    Instrument *inst;\n    s32 aidx;@    s32 cidx;\n    s16 *seqa;\n    s16 *seqs;\n    s16 *seqv;\n    s32 *durations16;\n    u32 piece;\n    s32 i;\n    u16 *events16;\n    s32 stop;\n    u8 *events;\n    s16 *seq;\n    s32 gain;\n    u16 *event;\n    s32 index;\n    s8 *buffer;\n    Effect *effect;\n    s32 old;\n    u32 *commands;\n    u16 val;\n    u8 note;\n    s32 command = 0;\n    s32 j;\n    Instrument *inst;\n    u16 freq;\n    s32 aidx;\n    s32 marker;@    u8 note;\n    s32 old;\n    s32 marker;\n    s32 cidx;\n    s16 *seqa;\n    s16 *seqs;\n    s16 *seqv;\n    s32 *durations16;\n    s32 gain;\n    Instrument *inst;\n    s32 command = 0;\n    Effect *effect;\n    s32 i;\n    u16 *events16;\n    u8 *events;\n    u16 freq;\n    s32 aidx;\n    u16 val;\n    s32 j;\n    s32 stop;\n    s32 index;\n    s16 *seq;\n    u32 *commands;\n    s8 *buffer;\n    u32 piece;\n    u16 *event;@    Instrument *inst;\n    u16 val;\n    s32 marker;\n    Effect *effect;\n    s32 gain;\n    s32 i;\n    u16 freq;\n    u16 *events16;\n    u8 note;\n    s32 command = 0;\n    u32 piece;\n    s32 aidx;\n    s16 *seq;\n    s32 old;\n    s32 index;\n    s32 j;\n    s32 cidx;\n    s16 *seqa;\n    s16 *seqs;\n    s16 *seqv;\n    s32 *durations16;\n    u8 *events;\n    u32 *commands;\n    u16 *event;\n    s8 *buffer;\n    s32 stop;@    u32 *commands;\n    Effect *effect;\n    s32 old;\n    u16 *event;\n    s32 stop;\n    s16 *seq;\n    s32 index;\n    s8 *buffer;\n    u16 *events16;\n    s32 aidx;\n    u32 piece;\n    s32 cidx;\n    s16 *seqa;\n    s16 *seqs;\n    s16 *seqv;\n    s32 *durations16;\n    u8 note;\n    s32 i;\n    Instrument *inst;\n    s32 j;\n    u8 *events;\n    u16 freq;\n    s32 marker;\n    s32 gain;\n    s32 command = 0;\n    u16 val;»

    if (gFadeActive == 1) {
        gFadeTimer = (gFadeTimer + 1) & 15;
        if (gFadeTimer == 0) { «fdl@@u16 val;»
            if (gFadeLevel != 0)
                gFadeLevel--;
            val = (REG(0x04000080) & 0xFF00) | (gFadeLevel * 17);
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
            FadeTable table = gFadeTable; «scl@@s32 gain; s8 *buffer; s32 j;@s32 gain; s8 *buffer;@s8 *buffer; s32 j;»
            gain = table.gain[gFadeLevel];
            «scale@buffer = &gMixBuffer[((gMixBank + 1) & 1) * 176];@buffer = gMixBuffer + ((gMixBank + 1) & 1) * 176;@buffer = gMixBuffer; buffer += ((gMixBank + 1) & 1) * 176;»
            for (j = 175; j >= 0; j--) {
                *buffer = (*buffer * gain) >> 8;
                buffer++;
            }
        }
    } else { «cll@@s8 *buffer;»
        «clear@buffer = &gMixBuffer[((gMixBank + 1) & 1) * 176] + 175;\n        for (i = 175; i >= 0; i--)\n            *buffer-- = 0;@buffer = &gMixBuffer[((gMixBank + 1) & 1) * 176];\n        i = 175;\n        buffer += i;\n        do {\n            *buffer-- = 0;\n        } while (--i >= 0);@buffer = gMixBuffer;\n        buffer += ((gMixBank + 1) & 1) * 176;\n        i = 175;\n        buffer += i;\n        do {\n            *buffer-- = 0;\n        } while (--i >= 0);@buffer = &gMixBuffer[((gMixBank + 1) & 1) * 176];\n        for (i = 175, buffer += i; i >= 0; i--)\n            *buffer-- = 0;»
    }

    for (i = 0; i <= 1; i++)
        gChannelHook(i);

    effect = gEffects;
    for (i = 0; i <= 3; «einc@i++, effect++@effect++, i++») {
        «efl@@u16 *events16; u16 *event; s32 stop;@u16 *events16; u16 *event; s32 stop; u16 val; u16 freq;@u16 *events16; u16 *event; s32 stop; u16 freq;@u16 *event; s32 stop; u16 freq;@u16 *events16; s32 stop; u16 freq;»
        events16 = «eev@effect->events@gEffects[i].events»;
        if (events16 != 0) {
            if («edl@gEffects[i].delay@effect->delay» != 0) {
                if (--«edl@gEffects[i].delay@effect->delay» != 0)
                    continue;
            }
            «ecu@effect->cursor@gEffects[i].cursor» += 5;
            stop = 0;
            event = &events16[«ecu@effect->cursor@gEffects[i].cursor»];
            if (event[0] == 254) {
                if (event[1] == 253)
                    stop = 255;
                else
                    «ecs@gEffects[i].cursor@effect->cursor» = event[1] - 1;
            }
            event = &events16[«ecr@effect->cursor@gEffects[i].cursor»];
            if (event[0] == 255)
                stop = 255;
            if (stop == 255) {
                «eclr@gEffects[i].events@effect->events» = 0;
                «effz@val = freq = 0;@freq = val = 0;@val = 0;\n                freq = 0;»
                gVoices[i].output = 1;
            } else {
                «edl@gEffects[i].delay@effect->delay» = event[0];
                event = &events16[«ecs@gEffects[i].cursor@effect->cursor»];
                val = (event[2] << 8) | event[1];
                freq = (event[3] << 8) | event[4];
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

    for (i = 0; i <= 7; i++) { «vll@@s32 marker;»
        «en@if (gVoices[i].enabled != 1)\n            continue;\n        if (gVoices[i].commands == 0)\n            continue;@if (gVoices[i].enabled != 1 || gVoices[i].commands == 0)\n            continue;»
    restart:
        do { «dwl@@u8 *events; u8 note;@u8 *events;@u8 note;»
            marker = 0x60;
            if (gVoices[i].delay != 0) {
                gVoices[i].delay--;
                if (gVoices[i].output != 0) {
                    TICK_TONE(0, 0x04000062, 0x04000064, ARP_DIRECT)
                    TICK_TONE(1, 0x04000068, 0x0400006C, ARP_VAL)
                    TICK_TONE(2, 0x04000072, 0x04000074, ARP_DIRECT)
                    if (i == 3) { «c3l@@Instrument *inst; s16 *seq; u16 val;@Instrument *inst; s16 *seq; u16 val; s32 old;@Instrument *inst; s16 *seq;@Instrument *inst; s16 *seq; s32 old;@s16 *seq;@Instrument *inst;»
                        inst = gInstruments[gVoices[3].instrument];
                        seq = inst->slide;
                        if (seq != 0 && --gVoices[3].pitch_delay == 0) {
                            «spo@index@old» = gVoices[3].pitch_cursor;
                            gVoices[3].pitch_cursor = «spo@index@old» + 2;
                            if (seq[gVoices[3].pitch_cursor] == 255)
                                gVoices[3].pitch_cursor = «spo@index@old»;
                            else {
                                «c3c@val = (inst->flags << 8) | (u16)seq[gVoices[3].pitch_cursor];@{ s32 t = seq[gVoices[3].pitch_cursor]; val = (inst->flags << 8) | t; }@{ s32 t = seq[gVoices[3].pitch_cursor]; val = t | (inst->flags << 8); }@val = (inst->flags << 8) | seq[gVoices[3].pitch_cursor];@val = inst->flags << 8; val |= (u16)seq[gVoices[3].pitch_cursor];@val = (u16)seq[gVoices[3].pitch_cursor] | (inst->flags << 8);»
                                gVoices[3].pitch_delay = seq[gVoices[3].pitch_cursor + 1];
                                REG(0x0400007C) = val;
                            }
                        }
                        seq = inst->volume;
                        if (seq != 0 && --gVoices[i].volume_delay == 0) {
                            «spo@index@old» = gVoices[i].volume_cursor;
                            gVoices[i].volume_cursor = «spo@index@old» + 2;
                            if (seq[gVoices[i].volume_cursor] == 255)
                                gVoices[i].volume_cursor = «spo@index@old»;
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
                    «cml@@u32 *commands; s32 cidx; s32 index; u32 piece;@u32 *commands; s32 cidx; s32 index;»
                    commands = gVoices[i].commands;
                    «spc@index@cidx» = gVoices[i].command;
                    command = commands[«spc@index@cidx»];
                    if (command == 0x67) {
                        piece = commands[«spc@index@cidx» + 1] << 8;
                        «pcs@piece += gFadeLevel;\n                        gMasterVolume = piece + (gFadeLevel << 4);@gMasterVolume = (piece += gFadeLevel) + (gFadeLevel << 4);»
                        REG(0x04000080) = gMasterVolume;
                        gVoices[i].command = «spc@index@cidx» + 2;
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
                        if («vox@i == 4 || i == 5@(u32)(i - 4) <= 1@i >= 4 && i <= 5»)
                            gVoices[i].pitch_cursor = -1;
                    }
                    if (command == 0x64) {
                        gVoices[i].transpose = commands[gVoices[i].command + 2];
                        gVoices[i].events = (u8 *)commands[gVoices[i].command + 1];
                        gVoices[i].repeats = commands[gVoices[i].command + 3];
                        «cur1@gVoices[i].cursor = 0;\n                        gVoices[i].delay = 0;@gVoices[i].cursor = gVoices[i].delay = 0;@gVoices[i].delay = gVoices[i].cursor = 0;»
                        gVoices[i].command += 4;
                    }
                    if (command == 0x62)
                        gVoices[i].command = commands[gVoices[i].command + 1];
                } while («cmdt@command != 0x64 && command != 0x61@command != 0x61 && command != 0x64»);
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
                if («vox@i == 4 || i == 5@(u32)(i - 4) <= 1@i >= 4 && i <= 5»)
                    note = 96;
            }
            
            «dur2@@{ s32 *durations = gDurations;@durations16 = gDurations;»
            gVoices[i].note = note;
            gVoices[i].pitch = (gFreqHi[note] << 8) | gFreqLo[note];
            gVoices[i].instrument = «cur2@events[gVoices[i].cursor + 1]@(events + gVoices[i].cursor)[1]»;
            gVoices[i].delay = «dur2@gDurations@durations@durations16»[«cur2@events[gVoices[i].cursor + 2]@(events + gVoices[i].cursor)[2]»];
            «cur3@gVoices[i].cursor += 3;@gVoices[i].cursor = gVoices[i].cursor + 3;»
            «dur2@@}@»
            START_TONE(0, 0x04000062, 0x04000064, val |= (u16)seq[0] - 0x8000;)
            START_TONE(1, 0x04000068, 0x0400006C, val |= (u16)seq[0] | 0x8000;)
            START_TONE(2, 0x04000072, 0x04000074, val |= (u16)seq[0] | 0x8000;)
            if (i == 3) { «c3sl@@Instrument *inst; s16 *seq; u16 val;@Instrument *inst; s16 *seq;@s16 *seq;»
                inst = gInstruments[gVoices[3].instrument];
                val = inst->control + (inst->control_high << 8);
                seq = inst->volume;
                if (seq != 0) {
                    val &= 255;
                    val |= (u16)seq[0] << 8;
                    gVoices[«c3v@3@i»].volume_cursor = 0;
                    gVoices[«c3v@3@i»].volume_delay = seq[1];
                }
                if (gVoices[«c3o@3@i»].output != 0)
                    REG(0x04000078) = val;
                val = inst->flags << 8;
                seq = inst->slide;
                if (seq != 0) {
                    val |= (u16)seq[0] - 0x8000;
                    gVoices[«c3s@3@i»].pitch_cursor = 0;
                    gVoices[«c3s@3@i»].pitch_delay = seq[1];
                    if (gVoices[«c3o@3@i»].output != 0)
                        REG(0x0400007C) = val;
                }
            }
            if («pcm@i >= 4 && i <= 7@(u32)(i - 4) <= 3») { «pcml@@s32 *p;»
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

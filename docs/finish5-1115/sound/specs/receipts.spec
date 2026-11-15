@@ r1_pitchsum_gain
<<<-
p = gVoices[i].pitch; p += slide[gVoices[i].pitch_cursor]; gVoices[i].pitch = p;
===
gain = gVoices[i].pitch; gain += slide[gVoices[i].pitch_cursor]; gVoices[i].pitch = gain;
>>>
@@ r2_notestart_slide
<<<
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

===
#define START_TONE(c, ctl, frq, SLIDEBIT)                                                            \
    if (i == c) {                                                                                    \
        inst = gInstruments[gVoices[c].instrument];                                                  \
        val = inst->control + (inst->control_high << 8);                                             \
        slide = inst->volume;                                                                          \
        if (slide != 0) {                                                                              \
            val &= 255;                                                                              \
            val |= (u16)slide[0] << 8;                                                                 \
            gVoices[c].volume_cursor = 0;                                                            \
            gVoices[c].volume_delay = slide[1];                                                        \
        }                                                                                            \
        if (gVoices[c].output != 0)                                                                  \
            REG(ctl) = val;                                                                          \
        slide = inst->arp;                                                                             \
        if (slide != 0) {                                                                              \
            { s32 n; n = note + slide[1]; gVoices[c].pitch = (gFreqHi[n] << 8) | gFreqLo[n]; }         \
            gVoices[c].arp_cursor = 0;                                                               \
            gVoices[c].arp_delay = slide[0];                                                           \
        }                                                                                            \
        val = inst->flags << 8;                                                                      \
        slide = inst->slide;                                                                           \
        if (slide != 0) {                                                                              \
            SLIDEBIT                                                                                 \
            gVoices[c].pitch_cursor = 0;                                                             \
            gVoices[c].pitch_delay = slide[1];                                                         \
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

>>>
<<<
            START_TONE(0, 0x04000062, 0x04000064, val |= (u16)seq[0] - 0x8000;)
            START_TONE(1, 0x04000068, 0x0400006C, val |= (u16)seq[0] | 0x8000;)
            START_TONE(2, 0x04000072, 0x04000074, val |= (u16)seq[0] | 0x8000;)
===
            START_TONE(0, 0x04000062, 0x04000064, val |= (u16)slide[0] - 0x8000;)
            START_TONE(1, 0x04000068, 0x0400006C, val |= (u16)slide[0] | 0x8000;)
            START_TONE(2, 0x04000072, 0x04000074, val |= (u16)slide[0] | 0x8000;)
>>>
@@ +r3_both
<<<-
p = gVoices[i].pitch; p += slide[gVoices[i].pitch_cursor]; gVoices[i].pitch = p;
===
gain = gVoices[i].pitch; gain += slide[gVoices[i].pitch_cursor]; gVoices[i].pitch = gain;
>>>
@@ +r4_t69temp
<<<
                        gTempo = commands[gVoices[i].command + 1];
===
                        { u32 t = commands[gVoices[i].command + 1]; gTempo = t; }
>>>
@@ +r5_tempo_pluseq
<<<
    gTempoCounter = gTempo + gTempoCounter;
===
    gTempoCounter += gTempo;
>>>
@@ +r6_stop_in_gain
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
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

===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            gain = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    gain = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                gain = 255;
            if (gain == 255) {
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

>>>
@@ s_tempo_only
<<<
    gTempoCounter = gTempo + gTempoCounter;
===
    gTempoCounter += gTempo;
>>>
@@ s_t69_only
<<<
                        gTempo = commands[gVoices[i].command + 1];
===
                        { u32 t = commands[gVoices[i].command + 1]; gTempo = t; }
>>>
@@ s_stop_only
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
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

===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            gain = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    gain = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                gain = 255;
            if (gain == 255) {
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

>>>

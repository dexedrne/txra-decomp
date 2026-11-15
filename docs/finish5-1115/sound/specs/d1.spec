@@ p_command
<<<
p = gVoices[i].pitch; p += slide[gVoices[i].pitch_cursor]; gVoices[i].pitch = p;
===
command = gVoices[i].pitch; command += slide[gVoices[i].pitch_cursor]; gVoices[i].pitch = command;
>>>
@@ p_j
<<<
p = gVoices[i].pitch; p += slide[gVoices[i].pitch_cursor]; gVoices[i].pitch = p;
===
j = gVoices[i].pitch; j += slide[gVoices[i].pitch_cursor]; gVoices[i].pitch = j;
>>>
@@ p_cidx
<<<
p = gVoices[i].pitch; p += slide[gVoices[i].pitch_cursor]; gVoices[i].pitch = p;
===
cidx = gVoices[i].pitch; cidx += slide[gVoices[i].pitch_cursor]; gVoices[i].pitch = cidx;
>>>
@@ p_marker
<<<
p = gVoices[i].pitch; p += slide[gVoices[i].pitch_cursor]; gVoices[i].pitch = p;
===
marker = gVoices[i].pitch; marker += slide[gVoices[i].pitch_cursor]; gVoices[i].pitch = marker;
>>>
@@ st_slide
<<<
    if (i == c) {  s16 *seq;                                                                         \
===
    if (i == c) {                                                                                    \
>>>
@@ st_fseq
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

>>>
@@ st_slide
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
@@ st_slidepart
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
@@ stn_slide
<<<
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
===
            if (i == 3) {
                inst = gInstruments[gVoices[3].instrument];
                val = inst->control + (inst->control_high << 8);
                slide = inst->volume;
                if (slide != 0) {
                    val &= 255;
                    val |= (u16)slide[0] << 8;
                    gVoices[3].volume_cursor = 0;
                    gVoices[3].volume_delay = slide[1];
                }
                if (gVoices[3].output != 0)
                    REG(0x04000078) = val;
                val = inst->flags << 8;
                slide = inst->slide;
                if (slide != 0) {
                    val |= (u16)slide[0] - 0x8000;
                    gVoices[i].pitch_cursor = 0;
                    gVoices[i].pitch_delay = slide[1];
                    if (gVoices[3].output != 0)
                        REG(0x0400007C) = val;
                }
            }
>>>
@@ stn_slidepart
<<<
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
===
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
                slide = inst->slide;
                if (slide != 0) {
                    val |= (u16)slide[0] - 0x8000;
                    gVoices[i].pitch_cursor = 0;
                    gVoices[i].pitch_delay = slide[1];
                    if (gVoices[3].output != 0)
                        REG(0x0400007C) = val;
                }
            }
>>>

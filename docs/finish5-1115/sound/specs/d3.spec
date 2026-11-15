@@ m_vol
<<<
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
===
         slide = inst->volume;                                                                         \
        if (slide != 0 && --gVoices[i].volume_delay == 0) {                                            \
            gVoices[i].volume_cursor += 2;                                                           \
            if (slide[gVoices[i].volume_cursor] == 254)                                                \
                gVoices[i].volume_cursor = slide[gVoices[i].volume_cursor + 1];                        \
            if (slide[gVoices[i].volume_cursor] <= 253) {                                              \
                val = inst->control;                                                                 \
                val |= slide[gVoices[i].volume_cursor] << 8;                                           \
                REG(ctl) = val;                                                                      \
                gVoices[i].volume_delay = slide[gVoices[i].volume_cursor + 1];                         \
                REG(frq) = (inst->flags << 8) | gVoices[i].pitch | 0x8000;                           \
            }                                                                                        \
            if (slide[gVoices[i].volume_cursor] == 255)                                                \
                gVoices[i].volume_cursor -= 2;                                                       \
        }                                                                                            \
     }
>>>
@@ m_arp
<<<
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
===
         slide = inst->arp;                                                                            \
        if (slide != 0 && --gVoices[c].arp_delay == 0) {                                               \
            gVoices[c].arp_cursor += 2;                                                              \
            if (slide[gVoices[c].arp_cursor] == 254)                                                   \
                gVoices[c].arp_cursor = slide[gVoices[c].arp_cursor + 1];                              \
            if (slide[gVoices[c].arp_cursor] <= 253) {                                                 \
                gVoices[c].pitch = (gFreqHi[gVoices[c].note + slide[gVoices[c].arp_cursor + 1]] << 8) | gFreqLo[gVoices[c].note + slide[gVoices[c].arp_cursor + 1]]; \
                gVoices[c].arp_delay = slide[gVoices[c].arp_cursor];                                   \
                ARPWRITE(c, frq)                                                                     \
            }                                                                                        \
            if (slide[gVoices[c].arp_cursor] == 255)                                                   \
                gVoices[c].arp_cursor -= 2;                                                          \
        }                                                                                            \
>>>
@@ m_all
<<<
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
===
         slide = inst->arp;                                                                            \
        if (slide != 0 && --gVoices[c].arp_delay == 0) {                                               \
            gVoices[c].arp_cursor += 2;                                                              \
            if (slide[gVoices[c].arp_cursor] == 254)                                                   \
                gVoices[c].arp_cursor = slide[gVoices[c].arp_cursor + 1];                              \
            if (slide[gVoices[c].arp_cursor] <= 253) {                                                 \
                gVoices[c].pitch = (gFreqHi[gVoices[c].note + slide[gVoices[c].arp_cursor + 1]] << 8) | gFreqLo[gVoices[c].note + slide[gVoices[c].arp_cursor + 1]]; \
                gVoices[c].arp_delay = slide[gVoices[c].arp_cursor];                                   \
                ARPWRITE(c, frq)                                                                     \
            }                                                                                        \
            if (slide[gVoices[c].arp_cursor] == 255)                                                   \
                gVoices[c].arp_cursor -= 2;                                                          \
        }                                                                                            \
>>>
<<<
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
===
         slide = inst->volume;                                                                         \
        if (slide != 0 && --gVoices[i].volume_delay == 0) {                                            \
            gVoices[i].volume_cursor += 2;                                                           \
            if (slide[gVoices[i].volume_cursor] == 254)                                                \
                gVoices[i].volume_cursor = slide[gVoices[i].volume_cursor + 1];                        \
            if (slide[gVoices[i].volume_cursor] <= 253) {                                              \
                val = inst->control;                                                                 \
                val |= slide[gVoices[i].volume_cursor] << 8;                                           \
                REG(ctl) = val;                                                                      \
                gVoices[i].volume_delay = slide[gVoices[i].volume_cursor + 1];                         \
                REG(frq) = (inst->flags << 8) | gVoices[i].pitch | 0x8000;                           \
            }                                                                                        \
            if (slide[gVoices[i].volume_cursor] == 255)                                                \
                gVoices[i].volume_cursor -= 2;                                                       \
        }                                                                                            \
     }
>>>

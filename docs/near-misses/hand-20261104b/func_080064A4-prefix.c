/* INCOMPLETE enclosing-body recovery, not an installed replacement.
 * Source-level prefix 080064A4..08006712. The eight-voice PCM body is still
 * absent; the final return below is a diagnostic stopping point, not the
 * original behavior. Frame allocation and complete bytes DO NOT match. */
typedef struct { s32 gain[9]; } FadeLevels;
typedef struct { u16 *events; s32 cursor, delay; } SoundSequence;
typedef struct {
    s32 unknown_00, retrigger;
    u8 unknown_08[64];
} SequenceVoice;
extern FadeLevels g_0801FF00;
extern SoundSequence g_03007590[];
extern SequenceVoice g_03007770[];
extern s32 g_030079B4, g_03007400, g_030079B0, g_03007570;
extern u32 g_03007574, g_03007404;
extern s32 g_03006A98;
extern s8 g_03007410[];
extern void (*g_08332E9C)(s32);
extern void (*g_08332EA0)(s32);
extern void func_08005F8C(s32);
void func_080064A4(void)
{
    s32 i = 0;
    if (g_030079B4 == 1) {
        g_03007400 = (g_03007400 + 1) & 15;
        if (g_03007400 == 0) {
            if (g_030079B0 != 0) g_030079B0--;
            *(vu16 *)0x04000080 = (*(vu16 *)0x04000080 & 0xFF00)
                                | (g_030079B0 * 17);
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
            s8 *out = g_03007410 + (((g_03006A98 + 1) & 1) * 176);
            s32 left = 175;
            do {
                *out = (*out * gain) >> 8;
                out++;
            } while (--left >= 0);
        }
    } else {
        s8 *out = g_03007410 + (((g_03006A98 + 1) & 1) * 176) + 175;
        i = 175;
        do { *out-- = 0; } while (--i >= 0);
    }
    for (i = 0; i <= 1; i++) g_08332EA0(i);
    for (i = 0; i <= 3; i++) {
        SoundSequence *seq = &g_03007590[i];
        if (seq->events != 0) {
            if (seq->delay != 0) {
                seq->delay--;
                if (seq->delay != 0) continue;
            }
            seq->cursor += 5;
            {
                s32 stopped = 0;
                u16 *event = seq->events + seq->cursor;
                u16 control, frequency;
                if (event[0] == 254) {
                    if (event[1] == 253) stopped = 255;
                    else seq->cursor = event[1] - 1;
                }
                event = seq->events + seq->cursor;
                if (event[0] == 255) stopped = 255;
                if (stopped == 255) {
                    seq->events = 0;
                    control = 0;
                    frequency = 0;
                    g_03007770[i].retrigger = 1;
                } else {
                    seq->delay = event[0];
                    control = (event[2] << 8) | event[1];
                    frequency = (event[3] << 8) | event[4];
                }
                if (i == 0) {
                    *(vu16 *)0x04000062 = control;
                    *(vu16 *)0x04000064 = frequency;
                }
                if (i == 1) {
                    *(vu16 *)0x04000068 = control;
                    *(vu16 *)0x0400006C = frequency;
                }
                if (i == 2) {
                    *(vu16 *)0x04000072 = control;
                    *(vu16 *)0x04000074 = frequency;
                }
                if (i == 3) {
                    *(vu16 *)0x04000078 = control;
                    *(vu16 *)0x0400007C = frequency;
                }
            }
        }
    }
    if (g_03007570 != 0) return;
    g_03007574 += g_03007404;
    if (g_03007574 <= 255u) return;
    g_03007574 -= 256;
    /* 08006712: the enclosing eight-voice PCM loop belongs here. Do not
     * install or count this prefix as the complete original routine. */
}

#include "hdr2.h"
void test(void) {
    s32 i, c;
    u32 *cmds;
    if (gSoundPaused != 0) return;
    gTempoCounter = gTempo + gTempoCounter;
    if (gTempoCounter <= 255) return;
    gTempoCounter -= 256;
    for (i = 0; i <= 7; i++) {
        if (gV[i].enabled != 1) continue;
        cmds = gV[i].commands;
        c = cmds[gV[i].command];
        if (c == 0x69) { gTempo = cmds[gV[i].command + 1]; gV[i].command += 2; }
        if (c == 0x66) { gA = cmds[gV[i].command + 1]; gV[i].command += 2; }
        if (c == 0x60) gV[i].command += 3;
    }
}

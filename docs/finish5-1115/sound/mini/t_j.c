#include "hdr.h"
void test(void) {
    s32 i;
    if (gSoundPaused != 0) return;
    { s32 c = gTempoCounter, t = gTempo; c += t; gTempoCounter = c; if ((u32)c <= 255) return; gTempoCounter = c - 256; }
    for (i = 0; i <= 7; i++)
        f(i);
}

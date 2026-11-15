#include "hdr.h"
void test(void) {
    s32 i;
    if (gSoundPaused != 0) return;
    { u32 c = gTempoCounter; c += gTempo; gTempoCounter = c; if (c <= 255) return; gTempoCounter = c - 256; }
    for (i = 0; i <= 7; i++)
        f(i);
}

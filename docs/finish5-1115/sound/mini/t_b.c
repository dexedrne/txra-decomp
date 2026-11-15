#include "hdr.h"
void test(void) {
    s32 i;
    if (gSoundPaused != 0) return;
    gTempoCounter = gTempoCounter + gTempo;
    if (gTempoCounter < 256) return;
    gTempoCounter = gTempoCounter - 256;
    for (i = 0; i <= 7; i++)
        f(i);
}

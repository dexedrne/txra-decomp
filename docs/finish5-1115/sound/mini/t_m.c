#include "hdr.h"
void test(void) {
    s32 i;
    if (gSoundPaused != 0) return;
    gTempoCounter += *&gTempo;
    if (gTempoCounter <= 255) return;
    gTempoCounter -= 256;
    for (i = 0; i <= 7; i++)
        f(i);
}

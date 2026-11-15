#include "hdr.h"
void test(void) {
    s32 i;
    if (gSoundPaused != 0) return;
    { u32 *tp = &gTempo; u32 *cp = &gTempoCounter; *cp += *tp; if (*cp <= 255) return; *cp -= 256; }
    for (i = 0; i <= 7; i++)
        f(i);
}

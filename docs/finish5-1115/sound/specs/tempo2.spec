@@ t_fsp_a
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u32 *tp;
>>>
<<<
    gTempoCounter = gTempo + gTempoCounter;
    if (gTempoCounter <= 255)
        return;
    gTempoCounter -= 256;
===
    tp = &gTempo;
    gTempoCounter = *tp + gTempoCounter;
    if (gTempoCounter <= 255)
        return;
    gTempoCounter -= 256;
>>>
<<<
                        gTempo = commands[gVoices[i].command + 1];
===
                        *tp = commands[gVoices[i].command + 1];
>>>
@@ t_fsp0_a
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u32 *tp = &gTempo;
>>>
<<<
    gTempoCounter = gTempo + gTempoCounter;
    if (gTempoCounter <= 255)
        return;
    gTempoCounter -= 256;
===
    gTempoCounter = *tp + gTempoCounter;
    if (gTempoCounter <= 255)
        return;
    gTempoCounter -= 256;
>>>
<<<
                        gTempo = commands[gVoices[i].command + 1];
===
                        *tp = commands[gVoices[i].command + 1];
>>>
@@ t_fspn_a
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u32 *tp;
>>>
<<<
    gTempoCounter = gTempo + gTempoCounter;
    if (gTempoCounter <= 255)
        return;
    gTempoCounter -= 256;
===
    tp = &gTempo;
    gTempoCounter = *tp + gTempoCounter;
    if (gTempoCounter <= 255)
        return;
    gTempoCounter -= 256;
>>>
@@ t_fsp_b
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u32 *tp;
>>>
<<<
    gTempoCounter = gTempo + gTempoCounter;
    if (gTempoCounter <= 255)
        return;
    gTempoCounter -= 256;
===
    tp = &gTempo;
    gTempoCounter += *tp;
    if (gTempoCounter <= 255)
        return;
    gTempoCounter -= 256;
>>>
<<<
                        gTempo = commands[gVoices[i].command + 1];
===
                        *tp = commands[gVoices[i].command + 1];
>>>
@@ t_fsp0_b
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u32 *tp = &gTempo;
>>>
<<<
    gTempoCounter = gTempo + gTempoCounter;
    if (gTempoCounter <= 255)
        return;
    gTempoCounter -= 256;
===
    gTempoCounter += *tp;
    if (gTempoCounter <= 255)
        return;
    gTempoCounter -= 256;
>>>
<<<
                        gTempo = commands[gVoices[i].command + 1];
===
                        *tp = commands[gVoices[i].command + 1];
>>>
@@ t_fspn_b
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u32 *tp;
>>>
<<<
    gTempoCounter = gTempo + gTempoCounter;
    if (gTempoCounter <= 255)
        return;
    gTempoCounter -= 256;
===
    tp = &gTempo;
    gTempoCounter += *tp;
    if (gTempoCounter <= 255)
        return;
    gTempoCounter -= 256;
>>>
@@ t_fsp_c
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u32 *tp;
>>>
<<<
    gTempoCounter = gTempo + gTempoCounter;
    if (gTempoCounter <= 255)
        return;
    gTempoCounter -= 256;
===
    tp = &gTempo;
    gTempoCounter = gTempoCounter + *tp;
    if (gTempoCounter <= 255)
        return;
    gTempoCounter -= 256;
>>>
<<<
                        gTempo = commands[gVoices[i].command + 1];
===
                        *tp = commands[gVoices[i].command + 1];
>>>
@@ t_fsp0_c
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u32 *tp = &gTempo;
>>>
<<<
    gTempoCounter = gTempo + gTempoCounter;
    if (gTempoCounter <= 255)
        return;
    gTempoCounter -= 256;
===
    gTempoCounter = gTempoCounter + *tp;
    if (gTempoCounter <= 255)
        return;
    gTempoCounter -= 256;
>>>
<<<
                        gTempo = commands[gVoices[i].command + 1];
===
                        *tp = commands[gVoices[i].command + 1];
>>>
@@ t_fspn_c
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u32 *tp;
>>>
<<<
    gTempoCounter = gTempo + gTempoCounter;
    if (gTempoCounter <= 255)
        return;
    gTempoCounter -= 256;
===
    tp = &gTempo;
    gTempoCounter = gTempoCounter + *tp;
    if (gTempoCounter <= 255)
        return;
    gTempoCounter -= 256;
>>>

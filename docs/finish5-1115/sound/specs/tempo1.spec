@@ t_a
<<<
    gTempoCounter = gTempo + gTempoCounter;
    if (gTempoCounter <= 255)
        return;
    gTempoCounter -= 256;
===
    gTempoCounter = gTempo + gTempoCounter;
    if (gTempoCounter <= 255)
        return;
    gTempoCounter -= 256;
>>>
@@ t_fsp_a
<<<
    s16 *slide;
===
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
    s16 *slide;
===
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
    s16 *slide;
===
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
@@ t_cp_a
<<<
    gTempoCounter = gTempo + gTempoCounter;
    if (gTempoCounter <= 255)
        return;
    gTempoCounter -= 256;
===
    { u32 *cp = &gTempoCounter;
    *cp = gTempo + *cp;
    if (*cp <= 255)
        return;
    *cp -= 256; }
>>>
@@ t_b
<<<
    gTempoCounter = gTempo + gTempoCounter;
    if (gTempoCounter <= 255)
        return;
    gTempoCounter -= 256;
===
    gTempoCounter += gTempo;
    if (gTempoCounter <= 255)
        return;
    gTempoCounter -= 256;
>>>
@@ t_fsp_b
<<<
    s16 *slide;
===
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
    s16 *slide;
===
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
    s16 *slide;
===
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
@@ t_cp_b
<<<
    gTempoCounter = gTempo + gTempoCounter;
    if (gTempoCounter <= 255)
        return;
    gTempoCounter -= 256;
===
    { u32 *cp = &gTempoCounter;
    *cp += gTempo;
    if (*cp <= 255)
        return;
    *cp -= 256; }
>>>
@@ t_c
<<<
    gTempoCounter = gTempo + gTempoCounter;
    if (gTempoCounter <= 255)
        return;
    gTempoCounter -= 256;
===
    gTempoCounter = gTempoCounter + gTempo;
    if (gTempoCounter <= 255)
        return;
    gTempoCounter -= 256;
>>>
@@ t_fsp_c
<<<
    s16 *slide;
===
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
    s16 *slide;
===
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
    s16 *slide;
===
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
@@ t_cp_c
<<<
    gTempoCounter = gTempo + gTempoCounter;
    if (gTempoCounter <= 255)
        return;
    gTempoCounter -= 256;
===
    { u32 *cp = &gTempoCounter;
    *cp = *cp + gTempo;
    if (*cp <= 255)
        return;
    *cp -= 256; }
>>>
@@ t_var1
<<<
    gTempoCounter = gTempo + gTempoCounter;
    if (gTempoCounter <= 255)
        return;
    gTempoCounter -= 256;
===
    { u32 t = gTempoCounter + gTempo; gTempoCounter = t; if (t <= 255) return; gTempoCounter = t - 256; }
>>>
@@ t_var2
<<<
    gTempoCounter = gTempo + gTempoCounter;
    if (gTempoCounter <= 255)
        return;
    gTempoCounter -= 256;
===
    { u32 t = gTempo + gTempoCounter; gTempoCounter = t; if (t <= 255) return; gTempoCounter = t - 256; }
>>>
@@ t_var3
<<<
    gTempoCounter = gTempo + gTempoCounter;
    if (gTempoCounter <= 255)
        return;
    gTempoCounter -= 256;
===
    { u32 t = gTempoCounter; t += gTempo; gTempoCounter = t; if (t <= 255) return; gTempoCounter = t - 256; }
>>>
@@ t_var4
<<<
    gTempoCounter = gTempo + gTempoCounter;
    if (gTempoCounter <= 255)
        return;
    gTempoCounter -= 256;
===
    { u32 t = gTempo; t += gTempoCounter; gTempoCounter = t; if (t <= 255) return; gTempoCounter = t - 256; }
>>>
@@ t_var5
<<<
    gTempoCounter = gTempo + gTempoCounter;
    if (gTempoCounter <= 255)
        return;
    gTempoCounter -= 256;
===
    { u32 t = gTempo; u32 c = gTempoCounter; c += t; gTempoCounter = c; if (c <= 255) return; gTempoCounter = c - 256; }
>>>
@@ t_var6
<<<
    gTempoCounter = gTempo + gTempoCounter;
    if (gTempoCounter <= 255)
        return;
    gTempoCounter -= 256;
===
    { u32 c = gTempoCounter; u32 t = gTempo; c += t; gTempoCounter = c; if (c <= 255) return; gTempoCounter = c - 256; }
>>>
@@ t_pre
<<<
    gTempoCounter = gTempo + gTempoCounter;
    if (gTempoCounter <= 255)
        return;
    gTempoCounter -= 256;
===
    if ((gTempoCounter += gTempo) <= 255)
        return;
    gTempoCounter -= 256;
>>>

@@ e_v_pre_111_fn
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
>>>
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u16 *events16;
>>>
@@ e_v_pre_110_loc
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = gEffects[i].events[gEffects[i].cursor];
                val = (gEffects[i].events[gEffects[i].cursor + 2] << 8) | gEffects[i].events[gEffects[i].cursor + 1];
                freq = (gEffects[i].events[gEffects[i].cursor + 3] << 8) | gEffects[i].events[gEffects[i].cursor + 4];
            }
>>>
@@ e_v_pre_110_fn
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = gEffects[i].events[gEffects[i].cursor];
                val = (gEffects[i].events[gEffects[i].cursor + 2] << 8) | gEffects[i].events[gEffects[i].cursor + 1];
                freq = (gEffects[i].events[gEffects[i].cursor + 3] << 8) | gEffects[i].events[gEffects[i].cursor + 4];
            }
>>>
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u16 *events16;
>>>
@@ e_v_pre_101_loc
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (gEffects[i].events[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
>>>
@@ e_v_pre_101_fn
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (gEffects[i].events[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
>>>
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u16 *events16;
>>>
@@ e_v_pre_100_loc
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (gEffects[i].events[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = gEffects[i].events[gEffects[i].cursor];
                val = (gEffects[i].events[gEffects[i].cursor + 2] << 8) | gEffects[i].events[gEffects[i].cursor + 1];
                freq = (gEffects[i].events[gEffects[i].cursor + 3] << 8) | gEffects[i].events[gEffects[i].cursor + 4];
            }
>>>
@@ e_v_pre_100_fn
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (gEffects[i].events[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = gEffects[i].events[gEffects[i].cursor];
                val = (gEffects[i].events[gEffects[i].cursor + 2] << 8) | gEffects[i].events[gEffects[i].cursor + 1];
                freq = (gEffects[i].events[gEffects[i].cursor + 3] << 8) | gEffects[i].events[gEffects[i].cursor + 4];
            }
>>>
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u16 *events16;
>>>
@@ e_v_pre_011_loc
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (gEffects[i].events[gEffects[i].cursor] == 254) {
                if (gEffects[i].events[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = gEffects[i].events[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
>>>
@@ e_v_pre_011_fn
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (gEffects[i].events[gEffects[i].cursor] == 254) {
                if (gEffects[i].events[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = gEffects[i].events[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
>>>
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u16 *events16;
>>>
@@ e_v_pre_010_loc
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (gEffects[i].events[gEffects[i].cursor] == 254) {
                if (gEffects[i].events[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = gEffects[i].events[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = gEffects[i].events[gEffects[i].cursor];
                val = (gEffects[i].events[gEffects[i].cursor + 2] << 8) | gEffects[i].events[gEffects[i].cursor + 1];
                freq = (gEffects[i].events[gEffects[i].cursor + 3] << 8) | gEffects[i].events[gEffects[i].cursor + 4];
            }
>>>
@@ e_v_pre_010_fn
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (gEffects[i].events[gEffects[i].cursor] == 254) {
                if (gEffects[i].events[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = gEffects[i].events[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = gEffects[i].events[gEffects[i].cursor];
                val = (gEffects[i].events[gEffects[i].cursor + 2] << 8) | gEffects[i].events[gEffects[i].cursor + 1];
                freq = (gEffects[i].events[gEffects[i].cursor + 3] << 8) | gEffects[i].events[gEffects[i].cursor + 4];
            }
>>>
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u16 *events16;
>>>
@@ e_v_pre_001_loc
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (gEffects[i].events[gEffects[i].cursor] == 254) {
                if (gEffects[i].events[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = gEffects[i].events[gEffects[i].cursor + 1] - 1;
            }
            if (gEffects[i].events[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
>>>
@@ e_v_pre_001_fn
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (gEffects[i].events[gEffects[i].cursor] == 254) {
                if (gEffects[i].events[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = gEffects[i].events[gEffects[i].cursor + 1] - 1;
            }
            if (gEffects[i].events[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
>>>
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u16 *events16;
>>>
@@ e_v_pre_000_loc
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (gEffects[i].events[gEffects[i].cursor] == 254) {
                if (gEffects[i].events[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = gEffects[i].events[gEffects[i].cursor + 1] - 1;
            }
            if (gEffects[i].events[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = gEffects[i].events[gEffects[i].cursor];
                val = (gEffects[i].events[gEffects[i].cursor + 2] << 8) | gEffects[i].events[gEffects[i].cursor + 1];
                freq = (gEffects[i].events[gEffects[i].cursor + 3] << 8) | gEffects[i].events[gEffects[i].cursor + 4];
            }
>>>
@@ e_v_pre_000_fn
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (gEffects[i].events[gEffects[i].cursor] == 254) {
                if (gEffects[i].events[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = gEffects[i].events[gEffects[i].cursor + 1] - 1;
            }
            if (gEffects[i].events[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = gEffects[i].events[gEffects[i].cursor];
                val = (gEffects[i].events[gEffects[i].cursor + 2] << 8) | gEffects[i].events[gEffects[i].cursor + 1];
                freq = (gEffects[i].events[gEffects[i].cursor + 3] << 8) | gEffects[i].events[gEffects[i].cursor + 4];
            }
>>>
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u16 *events16;
>>>
@@ e_d_pre_111_loc
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (gEffects[i].events != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
>>>
@@ e_d_pre_111_fn
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (gEffects[i].events != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
>>>
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u16 *events16;
>>>
@@ e_d_pre_110_loc
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (gEffects[i].events != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = gEffects[i].events[gEffects[i].cursor];
                val = (gEffects[i].events[gEffects[i].cursor + 2] << 8) | gEffects[i].events[gEffects[i].cursor + 1];
                freq = (gEffects[i].events[gEffects[i].cursor + 3] << 8) | gEffects[i].events[gEffects[i].cursor + 4];
            }
>>>
@@ e_d_pre_110_fn
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (gEffects[i].events != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = gEffects[i].events[gEffects[i].cursor];
                val = (gEffects[i].events[gEffects[i].cursor + 2] << 8) | gEffects[i].events[gEffects[i].cursor + 1];
                freq = (gEffects[i].events[gEffects[i].cursor + 3] << 8) | gEffects[i].events[gEffects[i].cursor + 4];
            }
>>>
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u16 *events16;
>>>
@@ e_d_pre_101_loc
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (gEffects[i].events != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (gEffects[i].events[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
>>>
@@ e_d_pre_101_fn
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (gEffects[i].events != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (gEffects[i].events[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
>>>
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u16 *events16;
>>>
@@ e_d_pre_100_loc
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (gEffects[i].events != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (gEffects[i].events[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = gEffects[i].events[gEffects[i].cursor];
                val = (gEffects[i].events[gEffects[i].cursor + 2] << 8) | gEffects[i].events[gEffects[i].cursor + 1];
                freq = (gEffects[i].events[gEffects[i].cursor + 3] << 8) | gEffects[i].events[gEffects[i].cursor + 4];
            }
>>>
@@ e_d_pre_100_fn
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (gEffects[i].events != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (gEffects[i].events[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = gEffects[i].events[gEffects[i].cursor];
                val = (gEffects[i].events[gEffects[i].cursor + 2] << 8) | gEffects[i].events[gEffects[i].cursor + 1];
                freq = (gEffects[i].events[gEffects[i].cursor + 3] << 8) | gEffects[i].events[gEffects[i].cursor + 4];
            }
>>>
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u16 *events16;
>>>
@@ e_d_pre_011_loc
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (gEffects[i].events != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (gEffects[i].events[gEffects[i].cursor] == 254) {
                if (gEffects[i].events[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = gEffects[i].events[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
>>>
@@ e_d_pre_011_fn
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (gEffects[i].events != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (gEffects[i].events[gEffects[i].cursor] == 254) {
                if (gEffects[i].events[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = gEffects[i].events[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
>>>
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u16 *events16;
>>>
@@ e_d_pre_010_loc
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (gEffects[i].events != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (gEffects[i].events[gEffects[i].cursor] == 254) {
                if (gEffects[i].events[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = gEffects[i].events[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = gEffects[i].events[gEffects[i].cursor];
                val = (gEffects[i].events[gEffects[i].cursor + 2] << 8) | gEffects[i].events[gEffects[i].cursor + 1];
                freq = (gEffects[i].events[gEffects[i].cursor + 3] << 8) | gEffects[i].events[gEffects[i].cursor + 4];
            }
>>>
@@ e_d_pre_010_fn
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (gEffects[i].events != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (gEffects[i].events[gEffects[i].cursor] == 254) {
                if (gEffects[i].events[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = gEffects[i].events[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = gEffects[i].events[gEffects[i].cursor];
                val = (gEffects[i].events[gEffects[i].cursor + 2] << 8) | gEffects[i].events[gEffects[i].cursor + 1];
                freq = (gEffects[i].events[gEffects[i].cursor + 3] << 8) | gEffects[i].events[gEffects[i].cursor + 4];
            }
>>>
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u16 *events16;
>>>
@@ e_d_pre_001_loc
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (gEffects[i].events != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (gEffects[i].events[gEffects[i].cursor] == 254) {
                if (gEffects[i].events[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = gEffects[i].events[gEffects[i].cursor + 1] - 1;
            }
            if (gEffects[i].events[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
>>>
@@ e_d_pre_001_fn
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (gEffects[i].events != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (gEffects[i].events[gEffects[i].cursor] == 254) {
                if (gEffects[i].events[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = gEffects[i].events[gEffects[i].cursor + 1] - 1;
            }
            if (gEffects[i].events[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
>>>
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u16 *events16;
>>>
@@ e_d_pre_000_loc
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (gEffects[i].events != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (gEffects[i].events[gEffects[i].cursor] == 254) {
                if (gEffects[i].events[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = gEffects[i].events[gEffects[i].cursor + 1] - 1;
            }
            if (gEffects[i].events[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = gEffects[i].events[gEffects[i].cursor];
                val = (gEffects[i].events[gEffects[i].cursor + 2] << 8) | gEffects[i].events[gEffects[i].cursor + 1];
                freq = (gEffects[i].events[gEffects[i].cursor + 3] << 8) | gEffects[i].events[gEffects[i].cursor + 4];
            }
>>>
@@ e_d_pre_000_fn
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (gEffects[i].events != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (gEffects[i].events[gEffects[i].cursor] == 254) {
                if (gEffects[i].events[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = gEffects[i].events[gEffects[i].cursor + 1] - 1;
            }
            if (gEffects[i].events[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = gEffects[i].events[gEffects[i].cursor];
                val = (gEffects[i].events[gEffects[i].cursor + 2] << 8) | gEffects[i].events[gEffects[i].cursor + 1];
                freq = (gEffects[i].events[gEffects[i].cursor + 3] << 8) | gEffects[i].events[gEffects[i].cursor + 4];
            }
>>>
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u16 *events16;
>>>
@@ e_d_in_111_loc
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        if (gEffects[i].events != 0) {
            events16 = gEffects[i].events;
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
>>>
@@ e_d_in_111_fn
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        s16 stop;
        u16 freq;

        if (gEffects[i].events != 0) {
            events16 = gEffects[i].events;
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
>>>
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u16 *events16;
>>>
@@ e_d_in_110_loc
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        if (gEffects[i].events != 0) {
            events16 = gEffects[i].events;
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = gEffects[i].events[gEffects[i].cursor];
                val = (gEffects[i].events[gEffects[i].cursor + 2] << 8) | gEffects[i].events[gEffects[i].cursor + 1];
                freq = (gEffects[i].events[gEffects[i].cursor + 3] << 8) | gEffects[i].events[gEffects[i].cursor + 4];
            }
>>>
@@ e_d_in_110_fn
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        s16 stop;
        u16 freq;

        if (gEffects[i].events != 0) {
            events16 = gEffects[i].events;
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = gEffects[i].events[gEffects[i].cursor];
                val = (gEffects[i].events[gEffects[i].cursor + 2] << 8) | gEffects[i].events[gEffects[i].cursor + 1];
                freq = (gEffects[i].events[gEffects[i].cursor + 3] << 8) | gEffects[i].events[gEffects[i].cursor + 4];
            }
>>>
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u16 *events16;
>>>
@@ e_d_in_101_loc
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        if (gEffects[i].events != 0) {
            events16 = gEffects[i].events;
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (gEffects[i].events[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
>>>
@@ e_d_in_101_fn
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        s16 stop;
        u16 freq;

        if (gEffects[i].events != 0) {
            events16 = gEffects[i].events;
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (gEffects[i].events[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
>>>
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u16 *events16;
>>>
@@ e_d_in_100_loc
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        if (gEffects[i].events != 0) {
            events16 = gEffects[i].events;
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (gEffects[i].events[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = gEffects[i].events[gEffects[i].cursor];
                val = (gEffects[i].events[gEffects[i].cursor + 2] << 8) | gEffects[i].events[gEffects[i].cursor + 1];
                freq = (gEffects[i].events[gEffects[i].cursor + 3] << 8) | gEffects[i].events[gEffects[i].cursor + 4];
            }
>>>
@@ e_d_in_100_fn
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        s16 stop;
        u16 freq;

        if (gEffects[i].events != 0) {
            events16 = gEffects[i].events;
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (gEffects[i].events[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = gEffects[i].events[gEffects[i].cursor];
                val = (gEffects[i].events[gEffects[i].cursor + 2] << 8) | gEffects[i].events[gEffects[i].cursor + 1];
                freq = (gEffects[i].events[gEffects[i].cursor + 3] << 8) | gEffects[i].events[gEffects[i].cursor + 4];
            }
>>>
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u16 *events16;
>>>
@@ e_d_in_011_loc
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        if (gEffects[i].events != 0) {
            events16 = gEffects[i].events;
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (gEffects[i].events[gEffects[i].cursor] == 254) {
                if (gEffects[i].events[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = gEffects[i].events[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
>>>
@@ e_d_in_011_fn
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        s16 stop;
        u16 freq;

        if (gEffects[i].events != 0) {
            events16 = gEffects[i].events;
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (gEffects[i].events[gEffects[i].cursor] == 254) {
                if (gEffects[i].events[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = gEffects[i].events[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
>>>
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u16 *events16;
>>>
@@ e_d_in_010_loc
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        if (gEffects[i].events != 0) {
            events16 = gEffects[i].events;
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (gEffects[i].events[gEffects[i].cursor] == 254) {
                if (gEffects[i].events[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = gEffects[i].events[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = gEffects[i].events[gEffects[i].cursor];
                val = (gEffects[i].events[gEffects[i].cursor + 2] << 8) | gEffects[i].events[gEffects[i].cursor + 1];
                freq = (gEffects[i].events[gEffects[i].cursor + 3] << 8) | gEffects[i].events[gEffects[i].cursor + 4];
            }
>>>
@@ e_d_in_010_fn
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        s16 stop;
        u16 freq;

        if (gEffects[i].events != 0) {
            events16 = gEffects[i].events;
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (gEffects[i].events[gEffects[i].cursor] == 254) {
                if (gEffects[i].events[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = gEffects[i].events[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = gEffects[i].events[gEffects[i].cursor];
                val = (gEffects[i].events[gEffects[i].cursor + 2] << 8) | gEffects[i].events[gEffects[i].cursor + 1];
                freq = (gEffects[i].events[gEffects[i].cursor + 3] << 8) | gEffects[i].events[gEffects[i].cursor + 4];
            }
>>>
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u16 *events16;
>>>
@@ e_d_in_001_loc
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        if (gEffects[i].events != 0) {
            events16 = gEffects[i].events;
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (gEffects[i].events[gEffects[i].cursor] == 254) {
                if (gEffects[i].events[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = gEffects[i].events[gEffects[i].cursor + 1] - 1;
            }
            if (gEffects[i].events[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
>>>
@@ e_d_in_001_fn
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        s16 stop;
        u16 freq;

        if (gEffects[i].events != 0) {
            events16 = gEffects[i].events;
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (gEffects[i].events[gEffects[i].cursor] == 254) {
                if (gEffects[i].events[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = gEffects[i].events[gEffects[i].cursor + 1] - 1;
            }
            if (gEffects[i].events[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
>>>
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u16 *events16;
>>>
@@ e_d_in_000_loc
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        if (gEffects[i].events != 0) {
            events16 = gEffects[i].events;
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (gEffects[i].events[gEffects[i].cursor] == 254) {
                if (gEffects[i].events[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = gEffects[i].events[gEffects[i].cursor + 1] - 1;
            }
            if (gEffects[i].events[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = gEffects[i].events[gEffects[i].cursor];
                val = (gEffects[i].events[gEffects[i].cursor + 2] << 8) | gEffects[i].events[gEffects[i].cursor + 1];
                freq = (gEffects[i].events[gEffects[i].cursor + 3] << 8) | gEffects[i].events[gEffects[i].cursor + 4];
            }
>>>
@@ e_d_in_000_fn
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        s16 stop;
        u16 freq;

        if (gEffects[i].events != 0) {
            events16 = gEffects[i].events;
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (gEffects[i].events[gEffects[i].cursor] == 254) {
                if (gEffects[i].events[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = gEffects[i].events[gEffects[i].cursor + 1] - 1;
            }
            if (gEffects[i].events[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = gEffects[i].events[gEffects[i].cursor];
                val = (gEffects[i].events[gEffects[i].cursor + 2] << 8) | gEffects[i].events[gEffects[i].cursor + 1];
                freq = (gEffects[i].events[gEffects[i].cursor + 3] << 8) | gEffects[i].events[gEffects[i].cursor + 4];
            }
>>>
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u16 *events16;
>>>
@@ e_d_late_111_loc
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        if (gEffects[i].events != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            events16 = gEffects[i].events;
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
>>>
@@ e_d_late_111_fn
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        s16 stop;
        u16 freq;

        if (gEffects[i].events != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            events16 = gEffects[i].events;
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
>>>
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u16 *events16;
>>>
@@ e_d_late_110_loc
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        if (gEffects[i].events != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            events16 = gEffects[i].events;
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = gEffects[i].events[gEffects[i].cursor];
                val = (gEffects[i].events[gEffects[i].cursor + 2] << 8) | gEffects[i].events[gEffects[i].cursor + 1];
                freq = (gEffects[i].events[gEffects[i].cursor + 3] << 8) | gEffects[i].events[gEffects[i].cursor + 4];
            }
>>>
@@ e_d_late_110_fn
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        s16 stop;
        u16 freq;

        if (gEffects[i].events != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            events16 = gEffects[i].events;
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = gEffects[i].events[gEffects[i].cursor];
                val = (gEffects[i].events[gEffects[i].cursor + 2] << 8) | gEffects[i].events[gEffects[i].cursor + 1];
                freq = (gEffects[i].events[gEffects[i].cursor + 3] << 8) | gEffects[i].events[gEffects[i].cursor + 4];
            }
>>>
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u16 *events16;
>>>
@@ e_d_late_101_loc
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        if (gEffects[i].events != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            events16 = gEffects[i].events;
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (gEffects[i].events[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
>>>
@@ e_d_late_101_fn
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        s16 stop;
        u16 freq;

        if (gEffects[i].events != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            events16 = gEffects[i].events;
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (gEffects[i].events[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
>>>
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u16 *events16;
>>>
@@ e_d_late_100_loc
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        if (gEffects[i].events != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            events16 = gEffects[i].events;
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (gEffects[i].events[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = gEffects[i].events[gEffects[i].cursor];
                val = (gEffects[i].events[gEffects[i].cursor + 2] << 8) | gEffects[i].events[gEffects[i].cursor + 1];
                freq = (gEffects[i].events[gEffects[i].cursor + 3] << 8) | gEffects[i].events[gEffects[i].cursor + 4];
            }
>>>
@@ e_d_late_100_fn
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        s16 stop;
        u16 freq;

        if (gEffects[i].events != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            events16 = gEffects[i].events;
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (gEffects[i].events[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = gEffects[i].events[gEffects[i].cursor];
                val = (gEffects[i].events[gEffects[i].cursor + 2] << 8) | gEffects[i].events[gEffects[i].cursor + 1];
                freq = (gEffects[i].events[gEffects[i].cursor + 3] << 8) | gEffects[i].events[gEffects[i].cursor + 4];
            }
>>>
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u16 *events16;
>>>
@@ e_d_late_011_loc
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        if (gEffects[i].events != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            events16 = gEffects[i].events;
            gEffects[i].cursor += 5;
            stop = 0;
            if (gEffects[i].events[gEffects[i].cursor] == 254) {
                if (gEffects[i].events[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = gEffects[i].events[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
>>>
@@ e_d_late_011_fn
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        s16 stop;
        u16 freq;

        if (gEffects[i].events != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            events16 = gEffects[i].events;
            gEffects[i].cursor += 5;
            stop = 0;
            if (gEffects[i].events[gEffects[i].cursor] == 254) {
                if (gEffects[i].events[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = gEffects[i].events[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
>>>
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u16 *events16;
>>>
@@ e_d_late_010_loc
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        if (gEffects[i].events != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            events16 = gEffects[i].events;
            gEffects[i].cursor += 5;
            stop = 0;
            if (gEffects[i].events[gEffects[i].cursor] == 254) {
                if (gEffects[i].events[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = gEffects[i].events[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = gEffects[i].events[gEffects[i].cursor];
                val = (gEffects[i].events[gEffects[i].cursor + 2] << 8) | gEffects[i].events[gEffects[i].cursor + 1];
                freq = (gEffects[i].events[gEffects[i].cursor + 3] << 8) | gEffects[i].events[gEffects[i].cursor + 4];
            }
>>>
@@ e_d_late_010_fn
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        s16 stop;
        u16 freq;

        if (gEffects[i].events != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            events16 = gEffects[i].events;
            gEffects[i].cursor += 5;
            stop = 0;
            if (gEffects[i].events[gEffects[i].cursor] == 254) {
                if (gEffects[i].events[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = gEffects[i].events[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = gEffects[i].events[gEffects[i].cursor];
                val = (gEffects[i].events[gEffects[i].cursor + 2] << 8) | gEffects[i].events[gEffects[i].cursor + 1];
                freq = (gEffects[i].events[gEffects[i].cursor + 3] << 8) | gEffects[i].events[gEffects[i].cursor + 4];
            }
>>>
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u16 *events16;
>>>
@@ e_d_late_001_loc
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        if (gEffects[i].events != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            events16 = gEffects[i].events;
            gEffects[i].cursor += 5;
            stop = 0;
            if (gEffects[i].events[gEffects[i].cursor] == 254) {
                if (gEffects[i].events[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = gEffects[i].events[gEffects[i].cursor + 1] - 1;
            }
            if (gEffects[i].events[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
>>>
@@ e_d_late_001_fn
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        s16 stop;
        u16 freq;

        if (gEffects[i].events != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            events16 = gEffects[i].events;
            gEffects[i].cursor += 5;
            stop = 0;
            if (gEffects[i].events[gEffects[i].cursor] == 254) {
                if (gEffects[i].events[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = gEffects[i].events[gEffects[i].cursor + 1] - 1;
            }
            if (gEffects[i].events[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
>>>
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u16 *events16;
>>>
@@ e_d_late_000_loc
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        if (gEffects[i].events != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            events16 = gEffects[i].events;
            gEffects[i].cursor += 5;
            stop = 0;
            if (gEffects[i].events[gEffects[i].cursor] == 254) {
                if (gEffects[i].events[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = gEffects[i].events[gEffects[i].cursor + 1] - 1;
            }
            if (gEffects[i].events[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = gEffects[i].events[gEffects[i].cursor];
                val = (gEffects[i].events[gEffects[i].cursor + 2] << 8) | gEffects[i].events[gEffects[i].cursor + 1];
                freq = (gEffects[i].events[gEffects[i].cursor + 3] << 8) | gEffects[i].events[gEffects[i].cursor + 4];
            }
>>>
@@ e_d_late_000_fn
<<<
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        s16 stop;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        s16 stop;
        u16 freq;

        if (gEffects[i].events != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            events16 = gEffects[i].events;
            gEffects[i].cursor += 5;
            stop = 0;
            if (gEffects[i].events[gEffects[i].cursor] == 254) {
                if (gEffects[i].events[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = gEffects[i].events[gEffects[i].cursor + 1] - 1;
            }
            if (gEffects[i].events[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = gEffects[i].events[gEffects[i].cursor];
                val = (gEffects[i].events[gEffects[i].cursor + 2] << 8) | gEffects[i].events[gEffects[i].cursor + 1];
                freq = (gEffects[i].events[gEffects[i].cursor + 3] << 8) | gEffects[i].events[gEffects[i].cursor + 4];
            }
>>>
<<<
    s32 cidx;
    s16 *slide;
===
    s32 cidx;
    s16 *slide;
    u16 *events16;
>>>

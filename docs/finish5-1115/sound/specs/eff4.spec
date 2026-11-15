@@ h_s16u
<<<
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
        s16 * events16;
        s16 stop;
        u16 freq;

        events16 = (s16 *)gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if ((u16)events16[gEffects[i].cursor] == 254) {
                if ((u16)events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = (u16)events16[gEffects[i].cursor + 1] - 1;
            }
            if ((u16)events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = (u16)events16[gEffects[i].cursor];
                val = ((u16)events16[gEffects[i].cursor + 2] << 8) | (u16)events16[gEffects[i].cursor + 1];
                freq = ((u16)events16[gEffects[i].cursor + 3] << 8) | (u16)events16[gEffects[i].cursor + 4];
            }
>>>
@@ h_u16u
<<<
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
        u16 * events16;
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
            if ((u16)events16[gEffects[i].cursor] == 254) {
                if ((u16)events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = (u16)events16[gEffects[i].cursor + 1] - 1;
            }
            if ((u16)events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = (u16)events16[gEffects[i].cursor];
                val = ((u16)events16[gEffects[i].cursor + 2] << 8) | (u16)events16[gEffects[i].cursor + 1];
                freq = ((u16)events16[gEffects[i].cursor + 3] << 8) | (u16)events16[gEffects[i].cursor + 4];
            }
>>>
@@ h_u16i
<<<
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
        u16 * events16;
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
            if ((s32)events16[gEffects[i].cursor] == 254) {
                if ((s32)events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = (s32)events16[gEffects[i].cursor + 1] - 1;
            }
            if ((s32)events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = (s32)events16[gEffects[i].cursor];
                val = ((s32)events16[gEffects[i].cursor + 2] << 8) | (s32)events16[gEffects[i].cursor + 1];
                freq = ((s32)events16[gEffects[i].cursor + 3] << 8) | (s32)events16[gEffects[i].cursor + 4];
            }
>>>
@@ h_u16uu
<<<
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
        u16 * events16;
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
            if ((u32)(u16)events16[gEffects[i].cursor] == 254) {
                if ((u32)(u16)events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = (u32)(u16)events16[gEffects[i].cursor + 1] - 1;
            }
            if ((u32)(u16)events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = (u32)(u16)events16[gEffects[i].cursor];
                val = ((u32)(u16)events16[gEffects[i].cursor + 2] << 8) | (u32)(u16)events16[gEffects[i].cursor + 1];
                freq = ((u32)(u16)events16[gEffects[i].cursor + 3] << 8) | (u32)(u16)events16[gEffects[i].cursor + 4];
            }
>>>
@@ h_s16uu
<<<
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
        s16 * events16;
        s16 stop;
        u16 freq;

        events16 = (s16 *)gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if ((u32)(u16)events16[gEffects[i].cursor] == 254) {
                if ((u32)(u16)events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = (u32)(u16)events16[gEffects[i].cursor + 1] - 1;
            }
            if ((u32)(u16)events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = (u32)(u16)events16[gEffects[i].cursor];
                val = ((u32)(u16)events16[gEffects[i].cursor + 2] << 8) | (u32)(u16)events16[gEffects[i].cursor + 1];
                freq = ((u32)(u16)events16[gEffects[i].cursor + 3] << 8) | (u32)(u16)events16[gEffects[i].cursor + 4];
            }
>>>
@@ h_s16ui
<<<
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
        s16 * events16;
        s16 stop;
        u16 freq;

        events16 = (s16 *)gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if ((s32)(u16)events16[gEffects[i].cursor] == 254) {
                if ((s32)(u16)events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = (s32)(u16)events16[gEffects[i].cursor + 1] - 1;
            }
            if ((s32)(u16)events16[gEffects[i].cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = (s32)(u16)events16[gEffects[i].cursor];
                val = ((s32)(u16)events16[gEffects[i].cursor + 2] << 8) | (s32)(u16)events16[gEffects[i].cursor + 1];
                freq = ((s32)(u16)events16[gEffects[i].cursor + 3] << 8) | (s32)(u16)events16[gEffects[i].cursor + 4];
            }
>>>
@@ h_u16x
<<<
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
        u16 * events16;
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
            if (((events16[gEffects[i]) & 0xFFFF).cursor] == 254) {
                if (((events16[gEffects[i]) & 0xFFFF).cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = ((events16[gEffects[i]) & 0xFFFF).cursor + 1] - 1;
            }
            if (((events16[gEffects[i]) & 0xFFFF).cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = ((events16[gEffects[i]) & 0xFFFF).cursor];
                val = (((events16[gEffects[i]) & 0xFFFF).cursor + 2] << 8) | ((events16[gEffects[i]) & 0xFFFF).cursor + 1];
                freq = (((events16[gEffects[i]) & 0xFFFF).cursor + 3] << 8) | ((events16[gEffects[i]) & 0xFFFF).cursor + 4];
            }
>>>
@@ h_s16x
<<<
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
        s16 * events16;
        s16 stop;
        u16 freq;

        events16 = (s16 *)gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            stop = 0;
            if (((events16[gEffects[i]) & 0xFFFF).cursor] == 254) {
                if (((events16[gEffects[i]) & 0xFFFF).cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = ((events16[gEffects[i]) & 0xFFFF).cursor + 1] - 1;
            }
            if (((events16[gEffects[i]) & 0xFFFF).cursor] == 255)
                stop = 255;
            if (stop == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = ((events16[gEffects[i]) & 0xFFFF).cursor];
                val = (((events16[gEffects[i]) & 0xFFFF).cursor + 2] << 8) | ((events16[gEffects[i]) & 0xFFFF).cursor + 1];
                freq = (((events16[gEffects[i]) & 0xFFFF).cursor + 3] << 8) | ((events16[gEffects[i]) & 0xFFFF).cursor + 4];
            }
>>>

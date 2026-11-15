@@ g_pab
<<<
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
===
            gEffects[i].cursor = gEffects[i].cursor + 5;
            stop = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                stop = 255;
>>>
@@ g_ppa
<<<
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
===
            gEffects[i].cursor += 5;
            stop = 0;
            if (*(events16 + gEffects[i].cursor) == 254) {
                if (*(events16 + gEffects[i].cursor + 1) == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = *(events16 + gEffects[i].cursor + 1) - 1;
            }
            if (*(events16 + gEffects[i].cursor) == 255)
                stop = 255;
>>>
@@ g_ppb
<<<
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
===
            gEffects[i].cursor = gEffects[i].cursor + 5;
            stop = 0;
            if (*(events16 + gEffects[i].cursor) == 254) {
                if (*(events16 + gEffects[i].cursor + 1) == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = *(events16 + gEffects[i].cursor + 1) - 1;
            }
            if (*(events16 + gEffects[i].cursor) == 255)
                stop = 255;
>>>
@@ g_iaa
<<<
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
===
            gEffects[i].cursor += 5;
            stop = 0;
            if ((s32)events16[gEffects[i].cursor] == 254) {
                if ((s32)events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if ((s32)events16[gEffects[i].cursor] == 255)
                stop = 255;
>>>
@@ g_iab
<<<
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
===
            gEffects[i].cursor = gEffects[i].cursor + 5;
            stop = 0;
            if ((s32)events16[gEffects[i].cursor] == 254) {
                if ((s32)events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if ((s32)events16[gEffects[i].cursor] == 255)
                stop = 255;
>>>
@@ g_ipa
<<<
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
===
            gEffects[i].cursor += 5;
            stop = 0;
            if ((s32)*(events16 + gEffects[i].cursor) == 254) {
                if ((s32)*(events16 + gEffects[i].cursor + 1) == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = *(events16 + gEffects[i].cursor + 1) - 1;
            }
            if ((s32)*(events16 + gEffects[i].cursor) == 255)
                stop = 255;
>>>
@@ g_ipb
<<<
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
===
            gEffects[i].cursor = gEffects[i].cursor + 5;
            stop = 0;
            if ((s32)*(events16 + gEffects[i].cursor) == 254) {
                if ((s32)*(events16 + gEffects[i].cursor + 1) == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = *(events16 + gEffects[i].cursor + 1) - 1;
            }
            if ((s32)*(events16 + gEffects[i].cursor) == 255)
                stop = 255;
>>>
@@ g_uaa
<<<
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
===
            gEffects[i].cursor += 5;
            stop = 0;
            if ((u32)events16[gEffects[i].cursor] == 254) {
                if ((u32)events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if ((u32)events16[gEffects[i].cursor] == 255)
                stop = 255;
>>>
@@ g_uab
<<<
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
===
            gEffects[i].cursor = gEffects[i].cursor + 5;
            stop = 0;
            if ((u32)events16[gEffects[i].cursor] == 254) {
                if ((u32)events16[gEffects[i].cursor + 1] == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if ((u32)events16[gEffects[i].cursor] == 255)
                stop = 255;
>>>
@@ g_upa
<<<
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
===
            gEffects[i].cursor += 5;
            stop = 0;
            if ((u32)*(events16 + gEffects[i].cursor) == 254) {
                if ((u32)*(events16 + gEffects[i].cursor + 1) == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = *(events16 + gEffects[i].cursor + 1) - 1;
            }
            if ((u32)*(events16 + gEffects[i].cursor) == 255)
                stop = 255;
>>>
@@ g_upb
<<<
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
===
            gEffects[i].cursor = gEffects[i].cursor + 5;
            stop = 0;
            if ((u32)*(events16 + gEffects[i].cursor) == 254) {
                if ((u32)*(events16 + gEffects[i].cursor + 1) == 253)
                    stop = 255;
                else
                    gEffects[i].cursor = *(events16 + gEffects[i].cursor + 1) - 1;
            }
            if ((u32)*(events16 + gEffects[i].cursor) == 255)
                stop = 255;
>>>

@@ sv_gain
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
            if (i == 0) {
                REG(0x04000062) = val;
                REG(0x04000064) = freq;
            }
            if (i == 1) {
                REG(0x04000068) = val;
                REG(0x0400006C) = freq;
            }
            if (i == 2) {
                REG(0x04000072) = val;
                REG(0x04000074) = freq;
            }
            if (i == 3) {
                REG(0x04000078) = val;
                REG(0x0400007C) = freq;
            }
        }
    }

===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            gain = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    gain = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                gain = 255;
            if (gain == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
            if (i == 0) {
                REG(0x04000062) = val;
                REG(0x04000064) = freq;
            }
            if (i == 1) {
                REG(0x04000068) = val;
                REG(0x0400006C) = freq;
            }
            if (i == 2) {
                REG(0x04000072) = val;
                REG(0x04000074) = freq;
            }
            if (i == 3) {
                REG(0x04000078) = val;
                REG(0x0400007C) = freq;
            }
        }
    }

>>>
@@ sv_j
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
            if (i == 0) {
                REG(0x04000062) = val;
                REG(0x04000064) = freq;
            }
            if (i == 1) {
                REG(0x04000068) = val;
                REG(0x0400006C) = freq;
            }
            if (i == 2) {
                REG(0x04000072) = val;
                REG(0x04000074) = freq;
            }
            if (i == 3) {
                REG(0x04000078) = val;
                REG(0x0400007C) = freq;
            }
        }
    }

===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            j = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    j = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                j = 255;
            if (j == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
            if (i == 0) {
                REG(0x04000062) = val;
                REG(0x04000064) = freq;
            }
            if (i == 1) {
                REG(0x04000068) = val;
                REG(0x0400006C) = freq;
            }
            if (i == 2) {
                REG(0x04000072) = val;
                REG(0x04000074) = freq;
            }
            if (i == 3) {
                REG(0x04000078) = val;
                REG(0x0400007C) = freq;
            }
        }
    }

>>>
@@ sv_command
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
            if (i == 0) {
                REG(0x04000062) = val;
                REG(0x04000064) = freq;
            }
            if (i == 1) {
                REG(0x04000068) = val;
                REG(0x0400006C) = freq;
            }
            if (i == 2) {
                REG(0x04000072) = val;
                REG(0x04000074) = freq;
            }
            if (i == 3) {
                REG(0x04000078) = val;
                REG(0x0400007C) = freq;
            }
        }
    }

===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            command = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    command = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                command = 255;
            if (command == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
            if (i == 0) {
                REG(0x04000062) = val;
                REG(0x04000064) = freq;
            }
            if (i == 1) {
                REG(0x04000068) = val;
                REG(0x0400006C) = freq;
            }
            if (i == 2) {
                REG(0x04000072) = val;
                REG(0x04000074) = freq;
            }
            if (i == 3) {
                REG(0x04000078) = val;
                REG(0x0400007C) = freq;
            }
        }
    }

>>>
@@ sv_cidx
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
            if (i == 0) {
                REG(0x04000062) = val;
                REG(0x04000064) = freq;
            }
            if (i == 1) {
                REG(0x04000068) = val;
                REG(0x0400006C) = freq;
            }
            if (i == 2) {
                REG(0x04000072) = val;
                REG(0x04000074) = freq;
            }
            if (i == 3) {
                REG(0x04000078) = val;
                REG(0x0400007C) = freq;
            }
        }
    }

===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            cidx = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    cidx = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                cidx = 255;
            if (cidx == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
            if (i == 0) {
                REG(0x04000062) = val;
                REG(0x04000064) = freq;
            }
            if (i == 1) {
                REG(0x04000068) = val;
                REG(0x0400006C) = freq;
            }
            if (i == 2) {
                REG(0x04000072) = val;
                REG(0x04000074) = freq;
            }
            if (i == 3) {
                REG(0x04000078) = val;
                REG(0x0400007C) = freq;
            }
        }
    }

>>>
@@ sv_marker
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
            if (i == 0) {
                REG(0x04000062) = val;
                REG(0x04000064) = freq;
            }
            if (i == 1) {
                REG(0x04000068) = val;
                REG(0x0400006C) = freq;
            }
            if (i == 2) {
                REG(0x04000072) = val;
                REG(0x04000074) = freq;
            }
            if (i == 3) {
                REG(0x04000078) = val;
                REG(0x0400007C) = freq;
            }
        }
    }

===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            marker = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    marker = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                marker = 255;
            if (marker == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
            if (i == 0) {
                REG(0x04000062) = val;
                REG(0x04000064) = freq;
            }
            if (i == 1) {
                REG(0x04000068) = val;
                REG(0x0400006C) = freq;
            }
            if (i == 2) {
                REG(0x04000072) = val;
                REG(0x04000074) = freq;
            }
            if (i == 3) {
                REG(0x04000078) = val;
                REG(0x0400007C) = freq;
            }
        }
    }

>>>
@@ sv_piece
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
            if (i == 0) {
                REG(0x04000062) = val;
                REG(0x04000064) = freq;
            }
            if (i == 1) {
                REG(0x04000068) = val;
                REG(0x0400006C) = freq;
            }
            if (i == 2) {
                REG(0x04000072) = val;
                REG(0x04000074) = freq;
            }
            if (i == 3) {
                REG(0x04000078) = val;
                REG(0x0400007C) = freq;
            }
        }
    }

===
    effect = gEffects;
    for (i = 0; i <= 3; effect++, i++) {
        u16 *events16;
        u16 freq;

        events16 = gEffects[i].events;
        if (events16 != 0) {
            if (gEffects[i].delay != 0) {
                if (--gEffects[i].delay != 0)
                    continue;
            }
            gEffects[i].cursor += 5;
            piece = 0;
            if (events16[gEffects[i].cursor] == 254) {
                if (events16[gEffects[i].cursor + 1] == 253)
                    piece = 255;
                else
                    gEffects[i].cursor = events16[gEffects[i].cursor + 1] - 1;
            }
            if (events16[gEffects[i].cursor] == 255)
                piece = 255;
            if (piece == 255) {
                gEffects[i].events = 0;
                val = freq = 0;
                gVoices[i].output = 1;
            } else {
                gEffects[i].delay = events16[gEffects[i].cursor];
                val = (events16[gEffects[i].cursor + 2] << 8) | events16[gEffects[i].cursor + 1];
                freq = (events16[gEffects[i].cursor + 3] << 8) | events16[gEffects[i].cursor + 4];
            }
            if (i == 0) {
                REG(0x04000062) = val;
                REG(0x04000064) = freq;
            }
            if (i == 1) {
                REG(0x04000068) = val;
                REG(0x0400006C) = freq;
            }
            if (i == 2) {
                REG(0x04000072) = val;
                REG(0x04000074) = freq;
            }
            if (i == 3) {
                REG(0x04000078) = val;
                REG(0x0400007C) = freq;
            }
        }
    }

>>>

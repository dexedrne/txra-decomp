extern s32 g_03001E6C[][25];
extern s32 g_03001E64[][25];
extern TxraRecord g_03001E60[];
extern TxraTriple g_030057A0[];
extern s32 g_03005F90[], g_080202E4[], g_08020B04[], g_08020B08[];
extern s32 g_083D2280[], g_083C2280[];
extern s16 g_030021CC;
s32 func_080181C0(void)
{
    s32 j;
    s32 i;
    s32 angle;
    s32 width;
    s32 height;
    s32 mask;
    s32 result;
    s32 known;
    s32 zpos;
    s32 s1;
    s32 c1;
    s32 c2;
    s32 k;
    s32 model;
    s32 a;
    result = 0;
    mask = 0;
    i = 0;
    angle = (-g_03001E60[0].field_20) & 0x3FFF;
    do {
        if (g_03001E60[i].field_00) {
            j = 0;
            do {
                known = 0;
                if (g_03005F90[0] == i + j * 16 || g_03005F90[0] == j + i * 16) known = 1;
                if (g_03005F90[1] == i + j * 16 || g_03005F90[1] == j + i * 16) known = 1;
                if (g_03005F90[2] == i + j * 16 || g_03005F90[2] == j + i * 16) known = 1;
                if (g_03005F90[3] == i + j * 16 || g_03005F90[3] == j + i * 16) known = 1;
                if (mask & g_080202E4[i]) goto next_pair;
                if (mask & g_080202E4[j]) goto next_pair;
                if (!g_03001E60[j].field_00) goto next_pair;
                if (j == i) goto next_pair;
                g_030057A0[0].field_00 = -64;
                g_030057A0[0].field_08 = -192;
                g_030057A0[1].field_00 = 64;
                g_030057A0[1].field_08 = -192;
                g_030057A0[2].field_00 = -64;
                g_030057A0[3].field_00 = 64;
                g_030057A0[4].field_00 = -64;
                g_030057A0[4].field_08 = 0;
                g_030057A0[5].field_00 = 64;
                g_030057A0[5].field_08 = 0;
                g_030057A0[2].field_08 = 192;
                g_030057A0[3].field_08 = 192;
                zpos = g_03001E6C[j][0];
                model = g_03001E60[j].field_02;
                width = g_08020B04[model * 2];
                height = g_08020B08[model * 2];
                a = g_03001E60[j].field_20 & 0x3FFF;
                s1 = g_083D2280[a];
                c1 = g_083C2280[a];
                c2 = g_083C2280[angle];
                {
 TxraTriple *p = g_030057A0;
                k = 5;
                do {
                    s32 x;
                    s32 z;
                    s32 xx;
                    s32 zz;
                    x = p->field_00;
                    z = p->field_08;
                    xx = (s1 * x - c1 * z) >> 12;
                    zz = (s1 * z + c1 * x) >> 12;
                    xx += g_03001E60[j].field_04 - g_03001E60[i].field_04;
                    zz += zpos - g_03001E6C[i][0];
                    p->field_00 = (g_083D2280[angle] * xx - c2 * zz) >> 12;
                    p->field_08 = (g_083D2280[angle] * zz + c2 * xx) >> 12;
                    p++;
                }
 while (--k >= 0);
                }
                for (k = 0; k <= 5; k++) {
                    if (g_030057A0[k].field_00 > -width && g_030057A0[k].field_00 < width
                     && g_030057A0[k].field_08 > -height && g_030057A0[k].field_08 < height) {
                        if (known) {
 mask |= g_080202E4[i];
 goto next_pair;
 }
                        g_03001E60[i].field_3c = g_03001E60[j].field_28 + 560;
                        g_03001E60[j].field_3c = g_03001E60[i].field_28 + 560;
                        g_03001E60[i].field_3e = g_03001E60[i].field_20;
                        g_03001E60[j].field_3e = g_03001E60[j].field_20;
                        g_03001E60[i].field_3a = g_03001E60[j].field_20 & ~0xC000;
                        g_03001E60[j].field_3a = g_03001E60[i].field_20 & ~0xC000;
                        if (g_030057A0[k].field_00 > 32) {
                            g_03001E60[i].field_3a = (g_03001E60[i].field_3a - 256) & ~0xC000;
                            g_03001E60[i].field_3e = (g_03001E60[i].field_3e - 256) & ~0xC000;
                            g_03001E60[j].field_3a = (g_03001E60[j].field_3a + 256) & ~0xC000;
                            g_03001E60[j].field_3e = (g_03001E60[j].field_3e + 256) & ~0xC000;
                        }
                        if (g_030057A0[k].field_00 < -32) {
                            g_03001E60[i].field_3a = (g_03001E60[i].field_3a + 256) & ~0xC000;
                            g_03001E60[i].field_3e = (g_03001E60[i].field_3e + 256) & ~0xC000;
                            g_03001E60[j].field_3a = (g_03001E60[j].field_3a - 256) & ~0xC000;
                            g_03001E60[j].field_3e = (g_03001E60[j].field_3e - 256) & ~0xC000;
                        }
                        if (g_03001E60[i].field_3c < 0) {
                            if (i != 0) g_03001E60[i].field_3c <<= 2;
                        }
                        if (g_03001E60[j].field_3c < 0) {
                            if (j != 0) g_03001E60[j].field_3c <<= 2;
                        }
                        {
 s32 speed = g_03001E60[i].field_28;
                          s32 other = g_03001E60[j].field_28;
                          g_03001E60[j].field_28 = speed >> 1;
                          g_03001E60[i].field_28 = other >> 1;
                        }
                        if (!g_030021CC) {
                            if (j == 0 || i == 0) result = 1;
                        }
                        mask |= g_080202E4[i];
                        if (known) goto next_pair;
                        for (k = 0; k <= 3; k++) {
                            if (g_03005F90[k] == 0) g_03005F90[k] = i + j * 16;
                        }
                        goto next_pair;
                    }
                }
            next_pair:
                j++;
            }
 while (j <= 7);
        }
        i++;
    }
 while (i <= 7);
    if (!mask) {
        for (j = 3; j >= 0; j--) g_03005F90[j] = 0;
    }
    return result;
}

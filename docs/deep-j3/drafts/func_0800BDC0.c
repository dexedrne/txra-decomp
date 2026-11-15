/* Unmatched draft (j4: 48 normalized rows; the g_03001E60 base and the index product swap r6/r8, and one loop pointer is offset 16 instead of 10); excluded from the ROM build. */
extern TxraRecord g_03001E60[];
extern TxraRow28 *g_03006874;
extern s16 g_03005F54, g_030001BC, g_030021CC, g_03002330, g_03002A1C;
extern u16 g_030014BC, g_0300218C;
extern s32 g_03001B1C;
extern s32 func_08014614(s32, s32);
extern void func_0801604C(s32, s32);
void func_0800BDC0(s32 index)
{
    s32 angle, diff, i;
    u32 small;
    if ((u16)g_03001E60[index].field_4c == 2 || (index == 0 && g_03005F54 != 0) || (g_030001BC & 32)) {
        small = index - 1;
        if (small <= 2) {
            TxraRecord *r = &g_03001E60[index];
            s16 *t = &r->field_4a;
            *t += 1;
            *t &= 511;
            if (*t == 0) {
                s16 *lane = t - 1;
                switch (*lane) {
                case 48:
                    if (g_03001B1C & 1) *lane = 10;
                    else *lane = 84;
                    break;
                case 10: case 84:
                    *lane = 48;
                    break;
                }
            }
        }
        if (index == 0 && (g_030014BC & 1)) {
            if ((u16)g_03005F54 == 32) g_03005F54 = 31;
            g_03001E60[0].field_4c = index;
        }
        angle = (g_03006874[g_03001E60[index].field_38].field_0c + 4096) & 16383;
        i = g_03001E60[index].field_42 - g_03001E60[index].field_48;
        if ((u32)(i + 11) <= 22) angle += i << 3;
        angle &= 16383;
        diff = func_08014614((g_03001E60[index].field_34 >> 3) & 16383, angle);
        if (diff > 8191) diff -= 16384;
        g_03001E60[index].field_44 = 0;
        if (index == 0) {
            if (g_030001BC == 0 && g_03005F54 != 0) {
                if (g_03001E60[0].field_28 <= 2559) g_03001E60[0].field_44 |= 1;
            } else if (g_03001E60[index].field_28 <= 2239) g_03001E60[index].field_44 |= 1;
        } else if (index <= 3) {
            if (g_03001E60[index].field_28 <= 2559) g_03001E60[index].field_44 = 1;
        } else if (g_030001BC == 0) {
            if (g_03001E60[index].field_28 <= 1919) g_03001E60[index].field_44 = 1;
        } else if (g_030001BC == index || g_03001E60[index].field_28 <= 2239) g_03001E60[index].field_44 = 1;
        if ((g_030001BC & 32) && index == (g_030001BC & 7) && g_030021CC == 0
            && g_03001E60[index].field_38 > g_03001E60[0].field_38 + 2 && g_03001E60[index].field_28 > 1280)
            g_03001E60[index].field_44 = ((s16)g_03001E60[index].field_44 & ~1) | 2;
        if (index == 0 && (g_030001BC & 32) && g_03001E60[0].field_38 > g_03001E60[g_030001BC & 7].field_38 - 4
            && g_03001E60[0].field_28 > 960 && g_030021CC == 0)
            g_03001E60[0].field_44 |= 2;
        if (g_03001E60[index].field_42 < g_03001E60[index].field_48 - 10 && diff <= 199 && g_030021CC == 0) {
            g_03001E60[index].field_44 |= 16;
            if (g_03001E60[index].field_28 > 1600 && diff <= 349 && index <= 3) g_03001E60[index].field_44 |= 2;
        }
        if (g_03001E60[index].field_42 > g_03001E60[index].field_48 + 10 && diff > -200 && g_030021CC == 0) {
            g_03001E60[index].field_44 |= 32;
            if (g_03001E60[index].field_28 > 1600 && diff > -350 && index <= 3) g_03001E60[index].field_44 |= 2;
        }
        if (g_03001E60[index].field_42 >= g_03001E60[index].field_48 - 10 && g_03001E60[index].field_42 <= g_03001E60[index].field_48 + 10) {
            if (diff < -4) {
                if (small <= 2) { if (g_03001E60[index].field_28 > 600) g_03001E60[index].field_44 |= 16; }
                else g_03001E60[index].field_44 |= 16;
            }
            if (diff > 4) {
                if (small <= 2) { if (g_03001E60[index].field_28 > 600) g_03001E60[index].field_44 |= 32; }
                else g_03001E60[index].field_44 |= 32;
            }
        }
        for (i = 0; i <= 7; i++) {
            if (g_03001E60[i].field_00 != 0 && i != index
                && g_03001E60[i].field_38 < g_03001E60[index].field_38 + 6 && g_03001E60[i].field_38 > g_03001E60[index].field_38 - 1
                && g_03001E60[index].field_48 >= g_03001E60[i].field_48 - 8 && g_03001E60[index].field_48 <= g_03001E60[i].field_48 + 8) {
                if (g_030001BC != 0 && index == 0 && i == (g_030001BC & 7)) continue;
                if (g_03001E60[index].field_48 <= 44) g_03001E60[index].field_48 = 48;
                else if (g_03001E60[index].field_48 > 51) g_03001E60[index].field_48 = 48;
                else if (g_03001B1C & 1) g_03001E60[index].field_48 = 10;
                else g_03001E60[index].field_48 = 84;
            }
        }
        if (small <= 2) for (i = 0; i <= 7; i++) {
            if (i != index && g_03001E60[i].field_00 != 0
                && g_03001E60[i].field_42 > g_03001E60[index].field_42 - 18 && g_03001E60[i].field_42 < g_03001E60[index].field_42 + 18
                && g_03001E60[i].field_38 < g_03001E60[index].field_38 + 3 && g_03001E60[i].field_38 > g_03001E60[index].field_38 - 1) {
                if (g_03001E60[index].field_28 > 0) g_03001E60[index].field_44 = 2;
                else g_03001E60[index].field_44 = 0;
            }
        }
    }
    if (g_03001E60[index].field_4c == 0 && g_030021CC == 0 && g_03005F54 == 0 && g_03002330 == 0) {
        g_03001E60[index].field_44 = g_030014BC;
        if ((g_03002A1C == 0 && (g_0300218C & 256)) || (g_03002A1C == 1 && (g_0300218C & 64))) {
            if (g_030001BC == 0) func_0801604C(17, 1);
            else func_0801604C(17, 1);
        }
    }
}

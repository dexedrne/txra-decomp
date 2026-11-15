extern TxraRecord g_03001E60[];
extern s16 g_030046E0[][10];
extern const s16 g_080205C4[][14];
#define SCALE(x, k) { s32 d = ((x) << 5) * (level * factor[k]) / 100; (x) += d / 32; }
void func_0800AC3C(s32 index)
{
    s32 grade;
    s32 level;
    const s16 *factor;
    grade = g_03001E60[index].field_62 / 32;
    factor = g_080205C4[grade];
    g_03001E60[index].field_5a = 6 - grade;
    level = g_03001E60[index].field_62 / 16;
    SCALE(g_030046E0[index][0], 0);
    SCALE(g_030046E0[index][2], 1);
    SCALE(g_030046E0[index][4], 2);
    SCALE(g_030046E0[index][6], 3);
    SCALE(g_030046E0[index][8], 4);
    level = g_03001E60[index].field_62 / 64;
    SCALE(g_030046E0[index][1], 5);
    SCALE(g_030046E0[index][3], 6);
    SCALE(g_030046E0[index][5], 7);
    SCALE(g_030046E0[index][7], 8);
    SCALE(g_030046E0[index][9], 9);
    SCALE(g_03001E60[index].field_60, 10);
    level = (s16)(g_03001E60[index].field_62 / 12);
    SCALE(g_03001E60[index].field_58, 11);
    level = g_03001E60[index].field_62 / 32;
    SCALE(g_03001E60[index].field_56, 12);
}

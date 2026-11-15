extern u32 g_030079D0[], g_03006A88[], g_03006890[], g_030075E8[];
typedef struct { u32 field_00, field_04, field_08, field_0c, field_10; } Row20b;
extern TxraRow20 g_083B8378[];
extern s32 g_03006A98, g_03006A80;
extern u32 g_0300757C;
extern s8 g_03007600[];
void func_08006270(s32 ch)
{
    s8 *src;
    s32 buf, i;
    u32 pos;
    src = (s8 *)g_03006A88[ch];
    if (src) {
        if (g_03006890[ch] == 0) {
            if (g_030075E8[ch] == 0) {
                src = 0;
                g_03006A88[ch] = (u32)src;
            } else {
                g_03006A88[ch] = g_083B8378[g_030079D0[ch]].field_00;
                g_03006890[ch] = g_083B8378[g_030079D0[ch]].field_04 - 1;
                src = (s8 *)g_03006A88[ch];
            }
        } else {
            g_03006890[ch]--;
        }
    }
    buf = (g_03006A98 + 1) & 1;
    if (ch == 0) {
        if (src == 0) return;
        pos = g_0300757C;
        for (i = 0; i < 176; i++) {
            g_03007600[buf * 176 + i] = src[(s32)pos >> 4];
            pos += g_03006A80;
            if (pos >= *(u32 *)((u8 *)&g_083B8378[g_030079D0[0]] + 16)) pos = 0;
        }
        g_0300757C = pos;
        g_03006890[ch] = 4;
    } else if (src) {
        for (i = 0; i < 176; i++) {
            { s32 v = g_03007600[buf * 176 + i] + *src; src++; g_03007600[buf * 176 + i] = v >> 1; }
        }
    } else {
        for (i = 0; i < 176; i++) {
            s32 v = g_03007600[buf * 176 + i];
            g_03007600[buf * 176 + i] = v >> 1;
        }
    }
    g_03006A88[ch] = (u32)src;
}

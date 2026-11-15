/* Uninstalled C hypothesis. Full-byte comparison fails; not part of the build. */
typedef struct {
    s32 f00, f04, f08, f0c, f10, f14, f18, f1c, f20, f24, f28, f2c, f30, f34, f38, f3c, f40, f44;
} SoundSlot;
extern SoundSlot g_03007770[8];
extern s32 g_083C1070[][9];
extern s32 g_03007580,g_030079C0,g_030075F0,g_030079B0,g_030079B4;
void func_08005F8C(s32 index) {
    s32 *base = (s32 *)g_083C1070;
    s32 *source = &g_083C1070[index][0];
    s32 scaled = index << 3;
    s32 i;
    for (i=0;i<8;i++) {
        g_03007770[i].f20 = *source++;
        g_03007770[i].f08 = 0;
        g_03007770[i].f24 = 0;
        g_03007770[i].f0c = 0;
        g_03007770[i].f14 = 96;
        g_03007770[i].f10 = 0;
        g_03007770[i].f00 = 1;
        g_03007770[i].f04 = 1;
        g_03007770[i].f38 = -1;
        g_03007770[i].f30 = 0;
    }
    g_03007580 = *(s32 *)((scaled + index) * 4 + (s32)(base + 8));
    g_030079C0 = 0;
    g_030075F0 = index;
    g_030079B0 = 7;
    g_030079B4 = 0;
}

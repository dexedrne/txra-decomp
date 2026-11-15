extern s32 g_030001C8;
extern u32 g_030079E0, g_03007A00, g_03005FD0;
extern u8 g_030079F0[], g_03007A10[];
extern u32 func_080148B0(void *, void *);
u32 func_0801466C(void)
{
u32 i;
u32 offset;
u32 result;
u8 *p;
    if (g_030001C8 > 1) return 0;
    g_03007A00 = g_030079E0;
    g_030079E0 = func_080148B0(g_030079F0, g_03007A10);
    i = 0;
offset = 0;
p = g_03007A10;
    for (; i <= 1; i++) {
        if ((g_030079E0 & (1 << i)) && !g_03007A10[offset]) {
            if (g_030079E0 & 128) {
                if (i == 1) g_03005FD0 = g_03007A10[17];
            }
 else if (i == 0) g_03005FD0 = g_03007A10[1];
        }
        result = 0;
        *p = result;
        p += 16;
        offset += 16;
    }
    return result;
}

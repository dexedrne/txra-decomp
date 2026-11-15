extern u32 g_03001B24, g_0300667C;
extern u8 gOamShadow[], g_030001F0[];
void func_08015200(void)
{
    u32 i;
    u8 *dest;
    u8 *source;
    u8 *third;
    u8 *base;
    i = 0;
    if (i < g_03001B24) {
        dest = gOamShadow;
        base = g_030001F0;
        third = base + 8;
        dest += 96;
        source = base + 4;
        do {
            *(u16 *)dest = *(u16 *)source;
            *(u16 *)(dest + 2) = *(u16 *)(source + 2);
            *(u16 *)(dest + 4) = *(u16 *)third;
            dest += 8;
            third += 12;
            source += 12;
            i++;
        } while (i < g_03001B24);
    }
    g_0300667C = 1;
}

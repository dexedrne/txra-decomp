extern u8 g_03000B60[];
extern u32 g_03000B58, g_03000AC8, g_03005FD4;
void func_080142AC(u32 slot)
{
    u8 *source = g_03000B60;
    u8 *dest;
    u32 i;
    u8 t;
    if (slot == 0) dest = source + g_03000B58 * 32;
    if (slot == 1) dest = source + g_03000AC8 * 32;
    if (slot == 2) dest = source + g_03005FD4 * 32;
    for (i = 0; i <= 31; i++) {
        t = *source;
        *source = *dest;
        *dest = t;
        dest++;
        source++;
    }
}

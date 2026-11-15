extern s32 g_083D2280[], g_083C2280[];
void func_08005DD4(s32 *source, s32 *dest, s32 scale, u32 angle)
{
    s32 *table = g_083D2280;
    u32 i = angle & 0x3FFF;
    dest[0] = source[0] + ((scale * table[i]) >> 12);
    dest[1] = source[1];
    dest[2] = source[2] + ((scale * g_083C2280[i]) >> 12);
}

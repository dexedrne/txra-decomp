extern u16 g_0300218C, g_030014BC;
void func_08015D78(void)
{
    u16 keys = ~*(vu16 *)0x04000130;
    g_0300218C = keys & ~g_030014BC;
    g_030014BC = keys;
}

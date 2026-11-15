extern u8 g_03002E30[];
extern s16 g_03005F5C;
extern u32 g_030014B4;
void func_080143CC(void)
{
    g_03002E30[g_03005F5C] = g_030014B4;
    g_03005F5C++;
    if (g_03005F5C > 15) g_03005F5C = 15;
    g_03002E30[g_03005F5C] = 0;
}

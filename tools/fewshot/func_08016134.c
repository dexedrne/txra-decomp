extern u32 g_03005FC0;
extern void func_080160C4(u32, u32, u32, u32, u32);
void func_08016134(u32 source)
{
    if (g_03005FC0 == 0) func_080160C4(3, source, 0x0600A000, 0x9600, 32);
    else func_080160C4(3, source, 0x06000000, 0x9600, 32);
}

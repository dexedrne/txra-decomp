void func_08005D9C(u32 x, s32 y, u16 value, u32 page)
{
    u16 *base = (u16 *)0x06000000;
    if (page == 0) base = (u16 *)0x0600A000;
    if (x <= 119 && y >= 0 && y <= 159) *(u16 *)((u32)(base + x) + y * 240) = value;
}

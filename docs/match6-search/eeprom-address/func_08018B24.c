extern u16 *g_03007B50;
extern void func_08018AA4(void *, void *, u16);
u16 func_08018B24(u16 address, u16 *dest)
{
    u16 buffer[68];
    u16 *p;
    u8 i, j;
    u16 value;
    if (address >= g_03007B50[2]) return 0x80FF;
    p = buffer + *((u8 *)g_03007B50 + 8) + 1;
    for (i = 0; i < *((u8 *)g_03007B50 + 8); i++) {
        *p-- = address;
        address >>= 1;
    }
    *p-- = 1;
    *p = 1;
    func_08018AA4(buffer, (void *)0x0D000000, *((u8 *)g_03007B50 + 8) + 3);
    func_08018AA4((void *)0x0D000000, buffer, 68);
    p = buffer + 4;
    dest += 3;
    for (i = 0; i < 4; i++) {
        value = 0;
        for (j = 0; j < 16; j++) {
            value <<= 1;
            value |= *p++ & 1;
        }
        *dest-- = value;
    }
    return 0;
}

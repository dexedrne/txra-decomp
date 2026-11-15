extern u16 *g_03007B50;
extern u16 func_08018B24(u16, u16 *);
u16 func_08018D48(u16 index, u16 *source)
{
    u16 buffer[4];
    u8 i;
    u16 result = 0;
    u16 *p;
    if (index >= g_03007B50[2]) return 0x80FF;
    func_08018B24(index, buffer);
    p = buffer;
    for (i = 0; i < 4; i++) {
        if (*source++ != *p++) { result = 0x8000; break; }
    }
    return result;
}

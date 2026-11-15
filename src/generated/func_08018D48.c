/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
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

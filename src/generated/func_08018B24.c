/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern u16 *g_03007B50;
extern void func_08018AA4(void *, void *, u16);
u16 func_08018B24(u16 address, u16 *dest)
{
    u16 buffer[68];
    u16 *p;
    u8 i, j;
    u16 value;
    u32 offset;
    if (address >= g_03007B50[2]) return 0x80FF;
    offset = *((u8 *)g_03007B50 + 8) * 2;
    p = (u16 *)(offset + (u32)buffer);
    p++;
    for (i = 0; i < *((u8 *)g_03007B50 + 8); i++) {
        *p-- = address;
        address >>= 1;
    }
    *p-- = 1;
    *p = 1;
    func_08018AA4(buffer, (void *)0x0D000000, *((u8 *)g_03007B50 + 8) + 3);
    func_08018AA4((void *)0x0D000000, buffer, 68);
    p = (u16 *)buffer + 4;
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

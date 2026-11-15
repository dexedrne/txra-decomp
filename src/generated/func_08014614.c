/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
s32 func_08014614(s32 a, s32 b)
{
    s32 result;
    if (b >= a) {
        if (b <= a + 8192) return b - a;
    }
    if (a >= b) {
        if (a < b + 8192) return b - a;
    }
    if (b > a + 8192) result = b - (a + 16384);
    else if (b > a - 8192) result = 0;
    else result = b + 16384 - a;
    return result;
}

/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern u16 func_08018BD4(u16, u16 *);
extern u16 func_08018D48(u16, u16 *);
u16 func_08018DA0(u16 index, u16 *source)
{
    u8 attempt;
    u16 result;
    for (attempt = 0; attempt < 3; attempt++) {
        result = func_08018BD4(index, source);
        if (result != 0) continue;
        result = func_08018D48(index, source);
        if (result == 0) break;
    }
    return result;
}

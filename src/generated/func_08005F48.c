/* Byte-verified C; provisional field offsets are declared in types.h. */
#ifndef TXRA_BASIC_TYPES
#define TXRA_BASIC_TYPES
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#endif
#include "types.h"
extern s32 g_083D2280[], g_083C2280[];
void func_08005F48(TxraTriple *source, TxraTriple *dest, s32 scale, u32 angle, s32 y)
{
    s32 *table = g_083D2280;
    u32 i = angle & 0x3FFF;
    dest->field_00 = source->field_00 + ((scale * table[i]) >> 12);
    dest->field_04 = source->field_04 + y;
    dest->field_08 = source->field_08 + ((scale * g_083C2280[i]) >> 12);
}

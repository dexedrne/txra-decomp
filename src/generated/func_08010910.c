/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern u8 g_03000A70[];
extern u32 g_03001B18,g_03002E58,g_030066D4;
extern void func_080154AC(TxraTextRecord *);
void func_08010910(u32 x, u32 y, u32 flags, s32 value)
{
    u8 *cursor = g_03000A70;
    u32 emitted = 0;
    g_03001B18 = flags & 7;
    g_03002190.field_00 = x;
    g_03002190.field_01 = y;
    /* Always zero, but only combine proves it: a literal 0 would be
       CSE'd into the flag register initialised above. */
    g_03002E58 = (u8)x >> 8;
    g_030066D4 = y;
    g_03002190.field_04 = cursor;
    g_03002190.field_08 = 1;
    g_03002190.field_09 = 1;
    if (flags & 8) { g_03002190.field_01 = 80; g_03002190.field_00 = 8; }
    if (!(flags & 16)) *cursor = 36; else *cursor = 35;
    cursor++;
    if (value > 99999 || emitted == 1) {
        s32 digit; flags = 100000; digit = value / (s32)flags;
        value -= digit * flags;
        *cursor++ = digit + 48;
        emitted = 1;
    }
    if (value > 9999 || emitted == 1) {
        s32 digit; flags = 10000; digit = value / (s32)flags;
        value -= digit * flags;
        *cursor++ = digit + 48;
        emitted = 1;
    }
    if (value > 999 || emitted == 1) {
        s32 digit = value / 1000;
        value -= digit * 1000;
        *cursor++ = digit + 48;
        emitted = 1;
    }
    if (value > 99 || emitted == 1) {
        s32 digit; flags = 100; digit = value / (s32)flags;
        value -= digit * flags;
        *cursor++ = digit + 48;
        emitted = 1;
    }
    if (value > 9 || emitted == 1) {
        s32 digit = value / 10;
        value -= digit * 10;
        *cursor++ = digit + 48;
    }
    cursor[0] = value + 48;
    cursor[1] = 0;
    func_080154AC(&g_03002190);
}

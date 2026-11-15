/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern TxraRecord g_03001E60;
extern u8 g_03000B60[];
extern void func_080086C0(s32, s32);
extern void func_08008780(s32, s32);
extern void func_0800D2F4(s32, s32);
extern void func_08008838(s32, s32);
void func_0800D3B4(void)
{
    s32 v = g_03001E60.field_02 - 16;
    func_080086C0(v, g_03000B60[21] - 1);
    func_08008780(v, g_03000B60[22] - 1);
    func_0800D2F4(v, g_03000B60[24] - 1);
    func_08008838(v, g_03000B60[19] - 1);
}

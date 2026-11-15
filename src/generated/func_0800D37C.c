/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern TxraRecord g_03001E60;

extern void func_0801604C(u32, u32);
void func_0800D37C(void)
{
    if (((u8 *)g_03006874)[g_03001E60.field_38 * 28 + 22] == 0) func_0801604C(31, 0);
    else func_0801604C(32, 0);
}

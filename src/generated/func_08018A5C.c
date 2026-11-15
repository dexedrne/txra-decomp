/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern u32 g_0801FF90[],g_0801FF9C[];
u16 func_08018A5C(u16 a)
{
    u16 result=0;
    if(a==4) gEepromGeometry=(TxraEepromGeometry *)g_0801FF90;
    else if(a==64) gEepromGeometry=(TxraEepromGeometry *)g_0801FF9C;
    else {gEepromGeometry=(TxraEepromGeometry *)g_0801FF90;result=1;}
    return result;
}

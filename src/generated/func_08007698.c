/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
typedef struct { s32 words[9]; } Table9;
extern Table9 g_0801FF00;
extern s32 g_030079B0,g_03006A98;
extern s8 g_03007410[2][176];
void func_08007698(void)
{
    Table9 table=g_0801FF00;
    s32 scale=table.words[g_030079B0];
    s32 index=(g_03006A98+1)&1;
    s8 *base=(s8 *)g_03007410;
    s8 *p=(s8 *)(index*176+(s32)base);
    s32 i;
    for(i=175;i>=0;i--) {
        *p=(*p*scale)>>8;
        p++;
    }
}

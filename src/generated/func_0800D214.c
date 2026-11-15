/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
extern u16 g_030001BC;
extern s16 g_03002330,g_03004780;
extern u32 g_03002E58,g_030066D4,g_03001B18;
#include "types.h"
extern TxraRecord g_03001E60[];
extern u32 g_08178704[][4];
extern void func_080154AC(u32);
void func_0800D214(void)
{
    if (((g_030001BC&32) && g_03002330>95) || (u16)(g_030001BC-1)<=2) {
        g_03002E58=0;
        g_030066D4=18;
        g_03001B18=1;
        func_080154AC(g_08178704[g_03001E60[g_03004780].field_62][0]);
    }
}

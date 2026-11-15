/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
extern u32 g_030079D0[],g_03006A88[],g_03006890[],g_030075E8[],g_030075D8[],g_03007760[];
#include "types.h"
extern TxraRow20 g_083B8378[];
void func_0800761C(u32 a,u32 i)
{
    g_030079D0[i]=a;
    g_03006A88[i]=g_083B8378[a].field_00;
    g_03006890[i]=g_083B8378[a].field_04-1;
    g_030075E8[i]=g_083B8378[a].field_08;
    g_030075D8[i]=1;
    g_03007760[i]=1;
    *(vu16 *)0x04000082=(*(vu16 *)0x04000082 & 0xfffb)|4;
}

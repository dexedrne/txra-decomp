/* Byte-verified C; address name retained pending semantic review. */
#ifndef TXRA_BASIC_TYPES
#define TXRA_BASIC_TYPES
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#endif
extern s32 g_03006680,g_083D2280[],g_083C2280[],g_03000B5C,g_03002338;
extern s16 g_03005B40[];
void func_08005CF4(u32 angle,s32 xscale,s32 yscale,s32 x,s32 y)
{
    s32 slot=g_03006680*16;
    s32 a;
    s32 b;
    g_03005B40[slot+3]=a=(g_083D2280[angle]*xscale)>>8;
    g_03005B40[slot+7]=b=(g_083C2280[angle]*xscale)>>8;
    g_03000B5C=a*x-b*y;
    g_03005B40[slot+11]=(g_083C2280[angle]*-yscale)>>8;
    g_03005B40[slot+15]=b=(g_083D2280[angle]*yscale)>>8;
    a=(g_083C2280[angle]*yscale)>>8;
    g_03002338=a*x+b*y;
}

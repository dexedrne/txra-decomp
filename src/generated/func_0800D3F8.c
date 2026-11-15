/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern u8 g_03005680[][2];
extern s16 g_03001E50;
s32 func_0800D3F8(s32 start)
{
 s32 found=-1,i;
 for(i=start;i<128;i++)if(!g_03005680[i][0] && g_03005680[i][1]==g_03001E50){found=i;break;}
 if(found==-1)for(i=start;i<128;i++)if(g_03005680[i][1]==g_03001E50){found=i;break;}
 return found;
}

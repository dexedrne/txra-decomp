/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern s8 g_03005790[5];
extern u8 g_03005FA0[][5];
extern s16 g_03001E50;
u32 func_0800D1B8(void)
{
 u32 result=0;
 if(g_03005790[0]<=g_03005FA0[g_03001E50][0]) {
 u8 *q=g_03005FA0[g_03001E50];
 s8 *p=g_03005790,*end=p+4;
 do {
 if(*p<*q){result=1;break;}
 q++;p++;
 }while((s32)p<=(s32)end && *p<=*q);
 }
 return result;
}

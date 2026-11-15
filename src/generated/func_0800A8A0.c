/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern u16 g_03005788;
void func_0800A8A0(u32 unused,void *source,void *dest,s32 n)
{
 s32 count=n;
 s16 *src=source;u16 *dst=dest;
 s16 amount=g_03005788,i;
 for(i=0;i<count;i+=2){
 s16 c=*src++,r=c&31,g=(c>>5)&31,b=(c>>10)&31;
 r-=amount;if(r<0)r=0;
 g-=amount;if(g<0)g=0;
 b-=amount;if(b<0)b=0;
 *dst++=r+(g<<5)+(b<<10);
 }
}

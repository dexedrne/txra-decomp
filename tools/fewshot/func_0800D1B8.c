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

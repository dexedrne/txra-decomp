/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern u32 g_03005FC0,g_030021C8;
void func_08015C2C(s32 x,s32 y,u8 *src)
{
 s32 base;
 u8 *dst;
 s32 i,j;
 if(!(g_03005FC0&1))base=0x0600a000+y*240;
 else base=0x06000000+y*240;
 dst=(u8 *)(x+base);
 for(i=0;i<=7;){
 s32 next=i+1;
 for(j=7;j>=0;j--){
 if(*src){
 if((u32)dst&1){u8 *p=dst-1;*(u16 *)p=((*src+g_030021C8)<<8)|*p;}
 else *(u16 *)dst=(*(u16 *)dst&65280)|(*src+g_030021C8);
 }
 dst++;src++;
 }
 dst+=232; i=next;
 }
}

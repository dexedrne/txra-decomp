/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern u8 g_030079F0[],g_03007A10[],g_030079E4;
extern void func_080147D0(void);
void func_080146F4(void)
{
 u8 *first=g_030079F0;
 u32 zero=0;
 u8 *row=g_03007A10,*end=row+16,*base=row;
 u32 j;
 do {
 u8 *cursor;
 *row=zero;
 j=1;cursor=base+1;
 do {*cursor++=zero;j++;}while(j<=15);
 row+=16;base+=16;
 }while(row<=end);
 j=0;first[0]=j;
 j=1;base=first;
 do {*(u8 *)(j+(u32)base)=0;j++;}while(j<=15);
 func_080147D0();g_030079E4=1;
}

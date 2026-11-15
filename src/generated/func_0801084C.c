/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
#include "types.h"
extern u8 g_03000A70[];
extern s32 g_03002180,g_030001C0;
extern void func_080154AC(TxraTextRecord *);
void func_0801084C(u32 *arg)
{
 u8 *src; s32 i; s32 *offset;
 g_03002190.field_00=0;g_03002190.field_01=151;g_03002190.field_04=g_03000A70;g_03002190.field_08=1;g_03002190.field_09=1;
 src=(u8 *)arg[1];offset=&g_03002180;i=0;
 if(g_03002180<=39){for(;i<40-g_03002180;i++)g_03000A70[i]=32;}
 else {src+=*offset-40;if(!*src)*offset=0;}
 for(;i<=39;i++)g_03000A70[i]=*src++;
 g_03000A70[i]=0;
 g_030001C0++;if(g_030001C0>2)g_030001C0=0;
 if(!g_030001C0)g_03002180++;
 func_080154AC(&g_03002190);
}

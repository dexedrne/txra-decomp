/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern s32 g_03005F50,g_03002E4C,g_030021D4,g_03001E5C;
extern TxraRow28 *g_03006874;
extern TxraTriple g_030057A0,g_030055F0;
extern void func_080164D0(u32);
void func_08009F84(void)
{
    s32 i=g_03005F50+192;
    TxraRow28 *p,*base;
    TxraTriple *dest;
    if (i>=g_03002E4C) i-=g_03002E4C;
    dest=&g_030057A0;
    base=g_03006874;
    p=(TxraRow28 *)(i*28+(s32)base);
    dest->field_00=p->field_00;
    dest->field_04=p->field_04;
    dest->field_08=p->field_08;
    func_080164D0(0);
    if (g_030021D4==0) g_03001E5C=g_030055F0.field_04-266;
    if (g_030021D4==1) g_03001E5C=-218;
    else g_03001E5C=-204;
}

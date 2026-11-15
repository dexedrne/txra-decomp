/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern TxraRecord g_03001E60;
extern s32 g_03005F50;
extern TxraRow28 *g_03006874;
void func_0800A5C4(void)
{
    TxraRecord *p=&g_03001E60;
    s32 i=g_03005F50;
    TxraRow28 *base=g_03006874;
    TxraRow28 *q=(TxraRow28 *)(i*28+(s32)base);
    p->field_04=q->field_00;
    p->field_08=q->field_04;
    p->field_0c=q->field_08;
    p->field_38=i;
    p->field_34=((q->field_0c+4096)&16383)<<3;
    p->field_20=p->field_34>>3;
    p->field_48=48;
    p->field_3c=0;
    p->field_52=3;
    p->field_28=2000;
}

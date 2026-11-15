/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern void func_08018A58(void *, void *, u32);
void func_080147D0(void)
{
    u32 zero;
    s32 i;
    *(vu16 *)0x04000208 = 0;
    *(vu16 *)0x04000200 &= 0xFF3F;
    *(vu16 *)0x04000208 = 1;
    *(vu16 *)0x04000134 = 0;
    *(vu32 *)0x04000128 = 0x2000;
    *(vu16 *)0x04000128 |= 0x4003;
    zero = 0;
    func_08018A58(&zero, &g_03007A30, 0x05000048);
    g_03007A30.field_14 = -1;
    g_03007A30.field_28 = g_03007A30.field_60;
    g_03007A30.field_2c = g_03007A30.field_78;
    for (i = 0; i < 2; i++) {
        g_03007A30.field_30[i] = g_03007A30.field_90[i].field_00;
        g_03007A30.field_40[i] = g_03007A30.field_90[i].field_18;
        g_03007A30.field_50[i] = g_03007A30.field_90[i].field_30;
    }
    *(vu16 *)0x04000208 = 0;
    *(vu16 *)0x04000200 |= 0x80;
    *(vu16 *)0x04000208 = 1;
}

/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern void func_08018A58(void *, void *, u32);
/* TxraLinkState viewed from field_04; member names keep the outer offsets. */
typedef struct {
    u32 field_04;
    u8 unknown_08[0x38];
    u8 *field_40[4];
    u8 *field_50[4];
} LinkTail;
u32 func_080149FC(u8 *out)
{
    vu32 pad;
    u8 flags[4];
    u32 zero;
    s32 i;
    LinkTail *t;
    pad = 0;
    *(vu16 *)0x04000208 = 0;
    t = (LinkTail *)&g_03007A30.field_04;
    for (i = 0; i < 4; i++) {
        u8 *x = t->field_50[i];
        t->field_50[i] = t->field_40[i];
        t->field_40[i] = x;
    }
    t = (LinkTail *)&g_03007A30.field_04;
    *(u32 *)flags = t->field_04;
    t->field_04 = 0;
    *(vu16 *)0x04000208 = 1;
    g_03007A30.field_03 = 0;
    for (i = 0; i <= 1; i++) {
        u32 sum = 0;
        u32 j;
        for (j = 0; j <= 9; j++)
            sum += ((u16 *)g_03007A30.field_50[i])[j];
        if (flags[i] && (s16)sum == -1) {
            func_08018A58(g_03007A30.field_50[i] + 4, out + i * 16, 0x04000004);
            g_03007A30.field_03 |= 1 << i;
        }
        zero = 0;
        func_08018A58(&zero, g_03007A30.field_50[i] + 4, 0x05000004);
    }
    g_03007A30.field_02 |= g_03007A30.field_03;
    return g_03007A30.field_03;
}

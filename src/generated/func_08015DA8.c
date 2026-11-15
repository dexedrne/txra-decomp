/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern TxraTransfer g_030061F0[];
extern s32 g_030067E4;
void func_08015DA8(void)
{
    u32 i;
    for (i = 0; i <= 96; i++) {
        u32 src = g_030061F0[i].field_00;
        u32 dst, size;
        if (src == 0) { g_030061F0[0].field_00 = 0; goto done; }
        dst = g_030061F0[i].field_04;
        size = g_030061F0[i].field_08;
        {
            vu32 *dma = (vu32 *)0x040000D4;
            dma[0] = src;
            dma[1] = dst;
            dma[2] = 0x84000000 | (size >> 2);
            dma[2];
        }
    }
done:
    g_030061F0[0].field_00 = 0;
    g_030067E4 = 0;
}

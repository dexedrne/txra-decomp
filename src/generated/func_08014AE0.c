/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
/* Serial (multi-player) interrupt: sends the next halfword of the outgoing
 * packet, or the 0xFEFE marker and a buffer swap, and stores both received
 * halfwords into the per-player receive buffers, swapping them when ten
 * have arrived. One temporary `t` serves both buffer swaps: being set in two
 * blocks it is allocated globally, which leaves three local quantities in
 * the marker block and the original r0/r1 choice for the marker store. */
typedef unsigned long long u64;
typedef struct {
    u16 baud:2, si:1, sd:1, id:2, error:1, enable:1, unused8:4, mode:2, irq:1, unused15:1;
    u16 data;
} SioMultiCnt;
#define LINK g_03007A30
#define RECV_COUNT(i) (((s32 *)LINK.unknown_18)[i])
void func_08014AE0(void)
{
    u64 recv = *(u64 *)0x04000120;
    s32 i;
    u8 *t;
    if (LINK.field_14 == -1) {
        ((SioMultiCnt *)0x04000128)->data = 0xFEFE;
        t = LINK.field_2c;
        LINK.field_2c = LINK.field_28;
        LINK.field_28 = t;
    } else if (LINK.field_14 >= 0) {
        ((SioMultiCnt *)0x04000128)->data = ((u16 *)LINK.field_2c)[LINK.field_14];
    }
    if (LINK.field_14 <= 10) LINK.field_14++;
    for (i = 0; i <= 1; i++) {
        if (((u16 *)&recv)[i] == 0xFEFE && RECV_COUNT(i) > 9) {
            RECV_COUNT(i) = -1;
        } else {
            ((u16 *)LINK.field_30[i])[RECV_COUNT(i)] = ((u16 *)&recv)[i];
            if (RECV_COUNT(i) == 9) {
                t = LINK.field_40[i];
                LINK.field_40[i] = LINK.field_30[i];
                LINK.field_30[i] = t;
                ((u8 *)&LINK.field_04)[i] = 1;
            }
        }
        if (RECV_COUNT(i) <= 10) RECV_COUNT(i)++;
    }
    if (LINK.field_00 == 8) {
        *(vu16 *)0x0400010E = 0;
        *(vu16 *)0x04000128 |= 0x80;
        *(vu16 *)0x0400010E = 0xC0;
    }
}

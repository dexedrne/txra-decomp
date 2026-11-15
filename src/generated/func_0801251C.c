/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"

void func_0801251C(u32 r0, u32 r1, u32 r2) {
    u32 r3;
    u32 r4;
    u32 r5;
    u32 r6;
    u32 r7;
    u32 r8;
    u32 r12;
    r12 = r0;
    r6 = r1;
    r1 = *(u8 *)(r0 + 5);
    r0 = r1 << 8;
    r3 = r12;
    r3 = *(u8 *)(r3 + 4);
    r0 |= r3;
    r0 += 3;
    r2 -= 1;
    r7 = 0xC0;
    r1 = 0x3F;
    r8 = r1;
    r4 = r2 + r6;
    r3 = r12;
    r2 = r0 + r3;
    while (1) {
        r5 = *(u8 *)r2;
        if ((r5 & r7) != 0xC0) goto backward_run;
        r3 = r5;
        r0 = r8;
        r3 &= r0;
        r2 -= 1;
        r1 = *(u8 *)r2;
        r0 = r1 << 8;
        r2 -= 1;
        r1 = *(u8 *)r2;
        r0 |= r1;
        r2 -= 1;
        r1 = r6 + r0;
        if (r3 == 0) goto backward_run;
        r0 = r3;
        do {
            r3 = *(u8 *)r1;
            *(u8 *)r4 = (u8)r3;
            r4 -= 1;
            r1 += 1;
            r0 -= 1;
        }
        while (r0 != 0);
    backward_run:
        r0 = r5;
        r0 &= r7;
        if (r0 != 0x80) goto fill_run;
        r3 = r5;
        r0 = r8;
        r3 &= r0;
        r2 -= 1;
        r1 = *(u8 *)r2;
        r0 = r1 << 8;
        r2 -= 1;
        r1 = *(u8 *)r2;
        r0 |= r1;
        r2 -= 1;
        {
            u32 addend = r0;
            r0 = r6 + addend;
        }
        r0 += r3;
        r1 = r0 - 1;
        if (r3 == 0) goto fill_run;
        r0 = r3;
        do {
            r3 = *(u8 *)r1;
            *(u8 *)r4 = (u8)r3;
            r4 -= 1;
            r1 -= 1;
            r0 -= 1;
        }
        while (r0 != 0);
    fill_run:
        r0 = r5;
        r0 &= r7;
        if (r0 != 0x40) goto literal_run;
        r3 = r5;
        r0 = r8;
        r3 &= r0;
        r2 -= 1;
        r1 = *(u8 *)r2;
        r2 -= 1;
        if (r3 == 0) goto literal_run;
        r0 = r3;
        do {
            *(u8 *)r4 = (u8)r1;
            r4 -= 1;
            r0 -= 1;
        }
        while (r0 != 0);
    literal_run:
        r0 = r5;
        r0 &= r7;
        if (r0 != 0) goto next_packet;
        r2 -= 1;
        if (r5 == 0) goto next_packet;
        r0 = r5;
        do {
            r3 = *(u8 *)r2;
            *(u8 *)r4 = (u8)r3;
            r2 -= 1;
            r4 -= 1;
            r0 -= 1;
        }
        while (r0 != 0);
    next_packet:
        if ((s32)r2 <= (s32)r12) break;
        if ((s32)r4 <= (s32)r6) break;
    }
    return;
}

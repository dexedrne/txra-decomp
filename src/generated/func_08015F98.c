/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
#define FILL(value, destination, control) { \
    fill = (value); \
    { vu32 *dma = (vu32 *)0x040000D4; \
    dma[0] = (u32)&fill; \
    dma[1] = (u32)(destination); \
    dma[2] = (control); \
    dma[2]; } \
}
void func_08015F98(s32 page)
{
    u32 fill;
    if (page == 0) {
        FILL(0, 0x0600A000, 0x850021C0);
        FILL(0, 0x06012700, 0x850003C0);
    } else {
        FILL(0, 0x06000000, 0x850021C0);
        FILL(0, 0x06008700, 0x850003C0);
    }
}

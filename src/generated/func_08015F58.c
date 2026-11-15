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
void func_08015F58(s32 page)
{
    u32 pattern = 0xB1B1B1B1;
    u32 fill;
    if (page == 0) {
        FILL(pattern, 0x0600A000, 0x85002580);
    } else {
        FILL(pattern, 0x06000000, 0x85002580);
    }
}

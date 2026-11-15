/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
extern void func_08018AA4(void *, void *, u16);
u16 func_08018BE8(u16 address, u16 *data, u8 wait)
{
    u16 buffer[82];
    vu16 ready, previous, current;
    vu32 elapsed;
    u16 *p;
    u8 i, j;
    u16 value;
    u16 status;
    u32 offset;
    if (address >= gEepromGeometry->block_count) return 0x80FF;
    offset = gEepromGeometry->address_bits * 2;
    p = (u16 *)(offset + (u32)buffer);
    p += 66;
    *p-- = 0;
    for (i = 0; i < 4; i++) {
        value = *data++;
        for (j = 0; j < 16; j++) {
            *p-- = value;
            value >>= 1;
        }
    }
    for (i = 0; i < gEepromGeometry->address_bits; i++) {
        *p-- = address;
        address >>= 1;
    }
    *p-- = 0;
    *p = 1;
    func_08018AA4(buffer, (void *)0x0D000000, gEepromGeometry->address_bits + 67);
    status = 0;
    ready = 0;
    previous = *(vu16 *)0x04000006;
    elapsed = 0;
    for (;;) {
        if (!ready && (*(vu16 *)0x0D000000 & 1)) {
            ready++;
            if (!wait) break;
        }
        current = *(vu16 *)0x04000006;
        if (current != previous) {
            if (current > previous) elapsed += current - previous;
            else elapsed += current + (228 - previous);
            if (elapsed > 136) {
                if (!ready && !(*(vu16 *)0x0D000000 & 1)) status = 0xC001;
                break;
            }
            previous = current;
        }
    }
    return status;
}

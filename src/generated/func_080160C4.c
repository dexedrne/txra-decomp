/* Byte-verified C; address name retained pending semantic review. */
typedef unsigned char u8; typedef unsigned short u16; typedef unsigned int u32;
typedef signed char s8; typedef signed short s16; typedef signed int s32;
typedef volatile u8 vu8; typedef volatile u16 vu16; typedef volatile u32 vu32;
#include "types.h"
void func_080160C4(u32 unused,u8 *source,u8 *dest,u32 size)
{
    u32 done=0;

    s32 chunk;
    vu32 *dma;
    for(;done<size;) {
 register u32 max=2047;
        chunk=size-done;
        if((u32)chunk>max) chunk=2048;
        dma=(vu32 *)0x040000D4;
        dma[0]=(u32)source;
        dma[1]=(u32)dest;
        dma[2]=(chunk/4)|0x84000000;
        dma[2];
        {vu32 *wait=dma;while(wait[2]&0x80000000) {}}
        done+=chunk;source+=chunk;dest+=chunk;
    }
}

void func_08016210(u32 unused, u32 value, u8 *dest, u32 size)
{
    u32 done=0;
    s32 chunk;
    vu32 *dma;
    while (done < size) {
        volatile u32 word;
        chunk=size-done;
        if ((u32)chunk > 0x7ff) chunk=0x800;
        word=value;
        dma=(vu32 *)0x040000D4;
        dma[0]=(u32)&word;
        dma[1]=(u32)dest;
        dma[2]=(chunk/4)|0x85000000;
        dma[2];
        done+=chunk;
        dest+=chunk;
    }
}

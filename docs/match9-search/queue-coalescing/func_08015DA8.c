extern u32 g_030061F0[],g_030067E4;
void func_08015DA8(void)
{
    u32 i = 0;
    u32 base = (u32)g_030061F0;
    u32 endmarker = (u32)&g_030067E4;
    vu32 *dma = (vu32 *)0x040000D4;
    u32 cursor = base;
    u32 offset = 0;
    u32 destbase = base + 4;
u32 work;
u32 dest;
u32 count;
u32 source;
    do {
        source = *(u32 *)cursor;
        if (!source) { *(u32 *)base = source; break; }
        count = destbase;
        work = offset + count;
        dest = *(u32 *)work;
        work = base; work += 8;
        { u32 addend = work; work = offset + addend; }
        count = *(u32 *)work;
        dma[0] = source;
        dma[1] = dest;
        count >>= 2;
        work = 0x84000000;
        count |= work;
        dma[2] = count;
        work = dma[2];
        cursor += 12;
        offset += 12;
        i++;
    } while (i <= 96);
    *(u32 *)base = 0;
    *(u32 *)endmarker = 0;
}
